"""Tests for the supervised method added in protocol version 1.3 (study/measurement_validity/bert_classify.py).

The end-to-end test builds a tiny BERT locally, so it needs torch and transformers but no download.
"""
import importlib
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
STUDY = ROOT / "study/measurement_validity"
sys.path.insert(0, str(STUDY))
import methods  # noqa: E402

bert = importlib.import_module("bert_classify")
analyze = importlib.import_module("analyze")
HAS_DATA = (ROOT / "data/processed/person_corpus_exploratory_v1.csv").exists()
HAS_TORCH = importlib.util.find_spec("torch") is not None and importlib.util.find_spec("transformers") is not None
needs_data = pytest.mark.skipif(not HAS_DATA, reason="needs the data-v1 snapshot in data/processed/")


@needs_data
def test_training_set_is_disjoint_from_study_and_development_samples():
    training = pd.read_csv(STUDY / "training_sample.csv")
    sample = set(pd.read_csv(STUDY / "sample.csv").execution_number)
    development = set(pd.read_csv(ROOT / "data/processed/annotation_development_v2.csv").execution_number)
    corpus = pd.read_csv(ROOT / "data/processed/person_corpus_exploratory_v1.csv")
    assert len(training) == training.execution_number.nunique() == 280
    assert not set(training.execution_number) & (sample | development)
    assert set(training.execution_number) | sample | development == set(corpus.execution_number)


class _Tokenizer:
    """Stand-in tokenizer: one token per word."""
    cls_token_id, sep_token_id = -1, -2

    def __call__(self, text, add_special_tokens=False):
        return {"input_ids": list(range(len(text.split())))}


def test_long_statements_keep_head_and_tail():
    short = bert.encode(_Tokenizer(), "word " * 10)
    assert len(short) == 12
    ids = bert.encode(_Tokenizer(), "word " * 2000)
    assert len(ids) == bert.MAX_TOKENS
    body = ids[1:-1]
    assert body[:bert.HEAD_TOKENS] == list(range(bert.HEAD_TOKENS))
    assert body[-1] == 1999


def test_learning_curve_subsets_are_nested():
    subsets = bert.curve_subsets(range(200))
    sizes = sorted(subsets)
    assert sizes == [50, 100, 200]
    assert subsets[50] < subsets[100] < subsets[200]
    assert bert.curve_subsets(range(200)) == subsets  # fixed seed


def _tiny_bert(path, texts):
    from transformers import BertConfig, BertForSequenceClassification, BertTokenizerFast
    words = sorted({w for t in texts for w in t.lower().split()})
    vocab = ["[PAD]", "[UNK]", "[CLS]", "[SEP]", "[MASK]", *words[:3000]]
    path.mkdir()
    (path / "vocab.txt").write_text("\n".join(vocab))
    BertTokenizerFast(vocab_file=str(path / "vocab.txt")).save_pretrained(path)
    config = BertConfig(vocab_size=len(vocab), hidden_size=16, num_hidden_layers=1, num_attention_heads=2,
                        intermediate_size=32, max_position_embeddings=512, num_labels=2)
    BertForSequenceClassification(config).save_pretrained(path)


def _simulated_coding(coding, texts, rng):
    for coder in ("A", "B"):
        df = pd.DataFrame({"item_id": texts.item_id, "text": texts.candidate_text})
        for col in methods.CONSTRUCTS:
            truth = texts.candidate_text.map(lambda t, c=col: methods.dictionary_label(t, c)).astype(str)
            df[col] = np.where(rng.random(len(df)) < 0.1, rng.choice(["1", "0"], len(df)), truth)
        df["innocence_type"] = np.where(df.innocence == "1", "F", "")
        df.to_excel(coding / f"coder_{coder}_completed.xlsx", sheet_name="coding", index=False)
    df.to_excel(coding / "adjudication_completed.xlsx", sheet_name="coding", index=False)  # B's labels agreed


@needs_data
@pytest.mark.skipif(not HAS_TORCH, reason="needs torch and transformers")
def test_bert_end_to_end(tmp_path, monkeypatch):
    coding, outputs = tmp_path / "coding", tmp_path / "outputs"
    coding.mkdir()
    for module in (bert, analyze):
        monkeypatch.setattr(module, "CODING", coding)
        monkeypatch.setattr(module, "OUTPUTS", outputs)
    corpus = pd.read_csv(ROOT / "data/processed/person_corpus_exploratory_v1.csv", keep_default_na=False)
    sample = pd.read_csv(STUDY / "sample.csv")
    texts = sample.merge(corpus, on="execution_number")[["item_id", "candidate_text"]]
    rng = np.random.default_rng(3)

    # Both coders must finish before any automated method runs.
    with pytest.raises(SystemExit, match="both coders"):
        bert.run("own")
    _simulated_coding(coding, texts, rng)

    training = pd.read_csv(STUDY / "training_sample.csv").merge(corpus, on="execution_number")
    sheet = pd.DataFrame({"item_id": training.item_id, "text": training.candidate_text})
    for col in methods.CONSTRUCTS:
        sheet[col] = training.candidate_text.map(lambda t, c=col: methods.dictionary_label(t, c)).astype(str)
    sheet.loc[:4, "apology"] = "u"
    sheet.to_excel(coding / "train_A_completed.xlsx", sheet_name="coding", index=False)

    model_dir = tmp_path / "tiny-bert"
    _tiny_bert(model_dir, corpus.candidate_text)
    bert.run("own", model_name=str(model_dir), seeds=(1, 2))
    preds = pd.read_csv(outputs / "bert_predictions_own.csv")
    assert set(preds.training_size[preds.construct == "apology"]) == {69, 138, 275}  # 5 items coded u
    assert len(preds) == 2 * 3 * 2 * 150
    assert preds.prob.between(0, 1).all()

    # Eaton & Theuer's codes: study-sample statements are dropped from training.
    et = corpus[["execution_number"]].copy()
    for col in methods.CONSTRUCTS:
        et[col] = corpus.candidate_text.map(lambda t, c=col: methods.dictionary_label(t, c)).astype(str)
    et.to_csv(coding / "eaton_theuer_labels.csv", index=False)
    bert.run("eaton_theuer", model_name=str(model_dir), seeds=(1,))
    meta = pd.read_json(outputs / "bert_run_eaton_theuer.json", typ="series")
    assert meta["dropped_study_sample_statements"] == 150

    analyze.evaluate()
    metrics = pd.read_csv(outputs / "method_metrics.csv")
    assert {"bert", "bert_et"} <= set(metrics.method)
    seeds = pd.read_csv(outputs / "bert_seed_metrics.csv")
    assert set(seeds[seeds.method == "bert"].training_size) == {69, 138, 275, 70, 140, 280}
    coder = pd.read_csv(outputs / "coder_specific_f1.csv")
    assert set(coder.coder) == {"A", "B"} and "bert" in set(coder.method)
    agreement = pd.read_csv(outputs / "eaton_theuer_agreement.csv")
    assert (agreement.n_overlap == 150).all()


def test_training_labels_reject_invalid_values(tmp_path, monkeypatch):
    monkeypatch.setattr(bert, "CODING", tmp_path)
    pd.DataFrame({"execution_number": [1], "apology": ["yes"], "innocence": ["0"]}).to_csv(
        tmp_path / "eaton_theuer_labels.csv", index=False)
    with pytest.raises(SystemExit, match="1, 0 or u"):
        bert.training_labels("eaton_theuer")
