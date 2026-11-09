"""Tests for the measurement-validity study code (study/measurement_validity)."""
import importlib
import shutil
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from sklearn.metrics import cohen_kappa_score

ROOT = Path(__file__).resolve().parents[1]
STUDY = ROOT / "study/measurement_validity"
sys.path.insert(0, str(STUDY))
import methods  # noqa: E402

analyze = importlib.import_module("analyze")
HAS_DATA = (ROOT / "data/processed/person_corpus_exploratory_v1.csv").exists()


@pytest.mark.parametrize("text,expected", [
    ("I'm sorry for what I did.", 1),
    ("I am so sorry to the Smith family", 1),
    ("I apologize to everyone I hurt", 1),
    ("I want to offer my apologies.", 1),
    ("I am not sorry for anything", 0),
    ("I'm not really sorry", 0),
    ("Please forgive me.", 0),
    ("I love you all. I'm ready, Warden.", 0),
    ("I’m sorry", 1),
])
def test_dictionary_apology(text, expected):
    assert methods.dictionary_label(text, "apology") == expected


@pytest.mark.parametrize("text,expected", [
    ("I am an innocent man.", 1),
    ("I didn't kill anybody.", 1),
    ("I did not do it", 1),
    ("You are executing the wrong man.", 1),
    ("I never killed her.", 1),
    ("The death penalty is wrong.", 0),
    ("I killed him and I am sorry.", 0),
    ("Innocent people suffer.", 0),
])
def test_dictionary_innocence(text, expected):
    assert methods.dictionary_label(text, "innocence") == expected


def test_nmf_rule_uses_dominant_topic():
    row = {f"topic_{i}": 0.0 for i in range(1, 7)}
    assert methods.nmf_label(row, "apology") == 0  # zero-feature document
    row.update(topic_1=0.5, topic_2=0.2)
    assert methods.nmf_label(row, "apology") == 1
    assert methods.nmf_label(row, "innocence") == 0
    row.update(topic_3=0.9)
    assert methods.nmf_label(row, "innocence") == 1


def test_kappa_matches_sklearn():
    rng = np.random.default_rng(0)
    a = rng.choice(["1", "0", "u"], 200, p=[0.3, 0.6, 0.1])
    b = np.where(rng.random(200) < 0.8, a, rng.choice(["1", "0", "u"], 200))
    assert analyze.cohen_kappa(a, b) == pytest.approx(cohen_kappa_score(a, b))
    assert analyze.cohen_kappa(a, a) == pytest.approx(1.0)


def test_classification_metrics_and_wilson():
    m = analyze.classification_metrics([1, 1, 0, 0, 1], [1, 0, 0, 1, 1])
    assert (m["tp"], m["fp"], m["fn"], m["tn"]) == (2, 1, 1, 1)
    assert m["precision"] == pytest.approx(2 / 3) and m["recall"] == pytest.approx(2 / 3)
    lo, hi = analyze.wilson(30, 100)
    assert lo == pytest.approx(0.2189, abs=1e-3) and hi == pytest.approx(0.3958, abs=1e-3)


def test_llm_prompt_and_schema_are_consistent():
    assert "{text}" in methods.LLM_INSTRUCTIONS
    assert set(methods.LLM_SCHEMA["required"]) == set(methods.CONSTRUCTS)
    assert set(methods.LLM_VALUE) == set(methods.LLM_SCHEMA["properties"]["apology"]["enum"])


@pytest.mark.skipif(not HAS_DATA, reason="needs the data-v1 snapshot")
def test_end_to_end_with_simulated_coders(tmp_path, monkeypatch):
    """Simulate two coders, run agreement, adjudicate, then evaluate."""
    coding, outputs = tmp_path / "coding", tmp_path / "outputs"
    coding.mkdir()
    monkeypatch.setattr(analyze, "CODING", coding)
    monkeypatch.setattr(analyze, "OUTPUTS", outputs)

    sample = pd.read_csv(STUDY / "sample.csv")
    corpus = pd.read_csv(ROOT / "data/processed/person_corpus_exploratory_v1.csv", keep_default_na=False)
    texts = sample.merge(corpus, on="execution_number")[["item_id", "candidate_text"]]
    rng = np.random.default_rng(1)
    for coder in ("A", "B"):
        df = pd.DataFrame({"item_id": texts.item_id, "text": texts.candidate_text})
        for col in methods.CONSTRUCTS:
            truth = texts.candidate_text.map(lambda t, c=col: methods.dictionary_label(t, c)).astype(str)
            flip = rng.random(len(df)) < 0.1
            df[col] = np.where(flip, rng.choice(["1", "0", "u"], len(df)), truth)
        df["innocence_type"] = np.where(df.innocence == "1", rng.choice(["F", "L"], len(df), p=[0.8, 0.2]), "")
        df["note"] = ""
        df.to_excel(coding / f"coder_{coder}_completed.xlsx", sheet_name="coding", index=False)

    analyze.agreement()
    agreement = pd.read_csv(outputs / "agreement.csv")
    assert set(methods.CONSTRUCTS) <= set(agreement.construct)
    main = agreement[agreement.construct.isin(methods.CONSTRUCTS)]
    assert (main.kappa_three_category > 0.2).all()  # rare categories give lower kappa

    adj = pd.read_excel(coding / "adjudication.xlsx", sheet_name="coding", dtype=str)
    adj["apology"] = adj["A_apology"].replace({"u": "0"})
    adj["innocence"] = adj["A_innocence"].replace({"u": "0"})
    adj["innocence_type"] = np.where(adj.innocence == "1", adj["A_type"].fillna("F").replace("", "F"), "")
    adj.to_excel(coding / "adjudication_completed.xlsx", sheet_name="coding", index=False)

    # Simulated LLM output with every kind of non-answer.
    outputs.mkdir(exist_ok=True)
    llm_rows = []
    for k, item in enumerate(sample.item_id):
        answer = {0: "refused", 1: "failed", 2: "invalid", 3: "uncertain"}.get(k, "yes" if k % 3 else "no")
        llm_rows.append({"run": 1, "item_id": item, "apology": answer, "innocence": answer, "status": "ok"})
    pd.DataFrame(llm_rows).to_csv(outputs / "llm_predictions.csv", index=False)

    analyze.evaluate()
    metrics = pd.read_csv(outputs / "method_metrics.csv")
    assert set(metrics.method) == {"dictionary", "nmf", "nmf_top2", "llm", "llm_uncertain_as_1"}
    assert set(metrics.construct) == {"apology", "innocence", "innocence_factual"}
    llm = metrics[(metrics.method == "llm") & (metrics.construct == "apology")].iloc[0]
    assert llm.n_no_answer >= 1 and llm.n_evaluated <= 147  # refused/failed/invalid excluded, not scored 0
    dictionary = metrics[(metrics.method == "dictionary") & (metrics.construct == "apology")].iloc[0]
    assert dictionary.n_no_answer == 0
    coverage = pd.read_csv(outputs / "llm_coverage.csv")
    assert {"refused", "failed", "invalid", "uncertain"} <= set(coverage.answer)
    sensitivity = pd.read_csv(outputs / "exposure_sensitivity.csv")
    assert set(sensitivity.group) == {"documented project exposure", "no documented exposure"}
    for name in ("errors.csv", "prevalence.csv", "method_differences.csv"):
        assert (outputs / name).exists()

    # An unexpected LLM answer must stop the evaluation rather than be scored.
    bad = pd.DataFrame(llm_rows)
    bad.loc[5, "apology"] = "maybe"
    bad.to_csv(outputs / "llm_predictions.csv", index=False)
    with pytest.raises(SystemExit):
        analyze.evaluate()


def test_bootstrap_degenerate_data_is_not_estimable():
    zeros = np.array(["0"] * 150)
    assert np.isnan(analyze.cohen_kappa(zeros, zeros))
    lo, hi = analyze.bootstrap(lambda i: analyze.cohen_kappa(zeros[i], zeros[i]), 150)
    assert np.isnan(lo) and np.isnan(hi)
    assert all(np.isnan(analyze.bootstrap(lambda i: 1.0, 0)))
    y = np.zeros(20, int)  # no positives: recall undefined in every resample
    assert all(np.isnan(analyze.bootstrap(lambda i: analyze.classification_metrics(y[i], y[i])["recall"], 20)))


def test_nmf_top2_rule():
    row = {"topic_1": 0.2, "topic_2": 0.5, "topic_3": 0.1, "topic_4": 0.0, "topic_5": 0.0, "topic_6": 0.0}
    assert methods.nmf_label(row, "apology") == 0      # not the largest topic
    assert methods.nmf_top2_label(row, "apology") == 1  # but present among the top two
    assert methods.nmf_top2_label(row, "innocence") == 0
    assert methods.nmf_top2_label({f"topic_{i}": 0.0 for i in range(1, 7)}, "apology") == 0


def test_freeze_check_detects_changes(tmp_path, monkeypatch):
    import json
    freeze = importlib.import_module("freeze")
    lock = json.loads((STUDY / "protocol_lock.json").read_text())
    lock["files"]["study/measurement_validity/methods.py"] = "0" * 64
    fake = tmp_path / "protocol_lock.json"
    fake.write_text(json.dumps(lock))
    monkeypatch.setattr(freeze, "LOCK", fake)
    assert freeze.check() is False
    monkeypatch.setattr(freeze, "LOCK", tmp_path / "missing.json")
    assert freeze.check() is False


def test_amendment_refused_once_results_exist(tmp_path, monkeypatch):
    freeze = importlib.import_module("freeze")
    (tmp_path / "coding").mkdir()
    (tmp_path / "coding" / "coder_A_completed.xlsx").write_text("x")
    (tmp_path / "protocol_lock.json").write_text("{}")
    monkeypatch.setattr(freeze, "HERE", tmp_path)
    monkeypatch.setattr(freeze, "LOCK", tmp_path / "protocol_lock.json")
    with pytest.raises(SystemExit, match="record a deviation"):
        freeze.amend("9.9", "test")
