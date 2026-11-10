"""Analysis for the measurement study, in two steps.

1. After both coders finish (sheets saved in coding/):
       python study/measurement_validity/analyze.py agreement
   Writes outputs/agreement.csv and coding/adjudication.xlsx (items to discuss).

2. After adjudication is filled in and saved as coding/adjudication_completed.xlsx:
       python study/measurement_validity/analyze.py evaluate
   Writes outputs/gold_labels.csv, outputs/auto_predictions.csv, outputs/method_metrics.csv,
   outputs/method_differences.csv, outputs/prevalence.csv and outputs/errors.csv; with BERT
   predictions, also outputs/bert_seed_metrics.csv and outputs/coder_specific_f1.csv; with
   Eaton & Theuer's codes, outputs/eaton_theuer_agreement.csv.
"""
import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import methods  # noqa: E402

ROOT = HERE.parents[1]
CODING = HERE / "coding"
OUTPUTS = HERE / "outputs"
N_BOOT = 2000
BOOT_SEED = 20261110
VALUES = ("1", "0", "u")


# ---------------------------------------------------------------- statistics

def cohen_kappa(a, b, categories=VALUES):
    a, b = np.asarray(a), np.asarray(b)
    if len(a) == 0:
        return float("nan")
    observed = np.mean(a == b)
    expected = sum(np.mean(a == c) * np.mean(b == c) for c in categories)
    return float("nan") if expected == 1 else float((observed - expected) / (1 - expected))


MIN_DEFINED_SHARE = 0.95  # protocol v1.1


def bootstrap(stat, n, n_boot=N_BOOT, seed=BOOT_SEED):
    """Percentile 95% interval of stat(index_array) over resampled items.

    Returns (nan, nan), meaning "not estimable", when there are no items or when fewer
    than 95% of resamples give a defined value (for example kappa when every resample
    has a single category, or recall when resamples contain no positives).
    """
    if n == 0:
        return float("nan"), float("nan")
    rng = np.random.default_rng(seed)
    draws = np.array([stat(rng.integers(0, n, n)) for _ in range(n_boot)], dtype=float)
    defined = draws[~np.isnan(draws)]
    if len(defined) < MIN_DEFINED_SHARE * n_boot:
        return float("nan"), float("nan")
    return float(np.percentile(defined, 2.5)), float(np.percentile(defined, 97.5))


def classification_metrics(gold, pred):
    gold, pred = np.asarray(gold, int), np.asarray(pred, int)
    tp = int(((gold == 1) & (pred == 1)).sum())
    fp = int(((gold == 0) & (pred == 1)).sum())
    fn = int(((gold == 1) & (pred == 0)).sum())
    precision = tp / (tp + fp) if tp + fp else float("nan")
    recall = tp / (tp + fn) if tp + fn else float("nan")
    f1 = 2 * tp / (2 * tp + fp + fn) if tp + fp + fn else float("nan")
    return {"tp": tp, "fp": fp, "fn": fn, "tn": int(len(gold) - tp - fp - fn),
            "precision": precision, "recall": recall, "f1": f1,
            "accuracy": float(np.mean(gold == pred))}


def wilson(k, n, z=1.959964):
    if n == 0:
        return float("nan"), float("nan")
    p = k / n
    centre = (p + z * z / (2 * n)) / (1 + z * z / n)
    half = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return float(centre - half), float(centre + half)


# ---------------------------------------------------------------- inputs

def read_sheet(path):
    df = pd.read_excel(path, sheet_name="coding", dtype=str).fillna("")
    for col in methods.CONSTRUCTS:
        df[col] = df[col].str.strip().str.lower().replace({"1.0": "1", "0.0": "0"})
    if "innocence_type" not in df.columns:
        df["innocence_type"] = ""
    df["innocence_type"] = df["innocence_type"].str.strip().str.upper()
    if "note" not in df.columns:
        df["note"] = ""
    return df.set_index("item_id").sort_index()


def check_complete(df, name):
    for col in methods.CONSTRUCTS:
        bad = df.index[~df[col].isin(VALUES)].tolist()
        if bad:
            raise SystemExit(f"{name}: {col} has missing or invalid values for {bad[:10]}")
    bad_type = df.index[(df.innocence == "1") & ~df.innocence_type.isin(["F", "L"])].tolist()
    if bad_type:
        raise SystemExit(f"{name}: innocence is 1 but innocence_type is not F or L for {bad_type[:10]}")


def find_sheet(coder):
    for name in (f"coder_{coder}_completed.xlsx", f"coder_{coder}.xlsx"):
        if (CODING / name).exists():
            return CODING / name
    raise SystemExit(f"No sheet for coder {coder} in {CODING}")


# ---------------------------------------------------------------- step 1

def agreement():
    a, b = read_sheet(find_sheet("A")), read_sheet(find_sheet("B"))
    assert list(a.index) == list(b.index), "The two sheets contain different items"
    check_complete(a, "coder A")
    check_complete(b, "coder B")
    n = len(a)
    rows = []
    for col in methods.CONSTRUCTS:
        x, y = a[col].to_numpy(), b[col].to_numpy()
        k3 = cohen_kappa(x, y)
        lo3, hi3 = bootstrap(lambda i: cohen_kappa(x[i], y[i]), n)
        both = (x != "u") & (y != "u")
        xb, yb = x[both], y[both]
        k2 = cohen_kappa(xb, yb, ("1", "0"))
        lo2, hi2 = bootstrap(lambda i: cohen_kappa(xb[i], yb[i], ("1", "0")), int(both.sum()))
        rows.append({"construct": col, "n_items": n, "percent_agreement": float(np.mean(x == y)),
                     "kappa_three_category": k3, "kappa3_ci_low": lo3, "kappa3_ci_high": hi3,
                     "n_without_u": int(both.sum()), "kappa_binary": k2,
                     "kappa2_ci_low": lo2, "kappa2_ci_high": hi2,
                     "coder_A_u": int((x == "u").sum()), "coder_B_u": int((y == "u").sum()),
                     "coder_A_positive": int((x == "1").sum()), "coder_B_positive": int((y == "1").sum())})
    exposure = pd.read_csv(HERE / "exposure.csv").set_index("item_id").project_exposure.reindex(a.index)
    for col in methods.CONSTRUCTS:
        for group, flag in (("documented project exposure", 1), ("no documented exposure", 0)):
            m = (exposure == flag).to_numpy()
            x, y = a[col].to_numpy()[m], b[col].to_numpy()[m]
            rows.append({"construct": f"{col} [{group}]", "n_items": int(m.sum()),
                         "percent_agreement": float(np.mean(x == y)) if m.any() else float("nan"),
                         "kappa_three_category": cohen_kappa(x, y)})
    both_innocent = (a.innocence == "1") & (b.innocence == "1")
    rows.append({"construct": "innocence_type (items both coded 1)", "n_items": int(both_innocent.sum()),
                 "percent_agreement": float(np.mean(a.innocence_type[both_innocent] == b.innocence_type[both_innocent]))
                 if both_innocent.any() else float("nan")})
    OUTPUTS.mkdir(exist_ok=True)
    result = pd.DataFrame(rows)
    result.to_csv(OUTPUTS / "agreement.csv", index=False)
    print(result.round(3).to_string(index=False))

    need = a.index[(a.apology != b.apology) | (a.innocence != b.innocence)
                   | (a.apology == "u") | (a.innocence == "u")
                   | (b.apology == "u") | (b.innocence == "u")
                   | (both_innocent & (a.innocence_type != b.innocence_type))]
    wb = Workbook()
    ws = wb.active
    ws.title = "coding"
    ws.append(["item_id", "text", "A_apology", "B_apology", "apology", "A_innocence", "B_innocence",
               "innocence", "A_type", "B_type", "innocence_type", "A_note", "B_note", "decision_note"])
    for cell in ws[1]:
        cell.font = Font(bold=True)
    for item in need:
        ws.append([item, a.at[item, "text"], a.at[item, "apology"], b.at[item, "apology"], None,
                   a.at[item, "innocence"], b.at[item, "innocence"], None,
                   a.at[item, "innocence_type"], b.at[item, "innocence_type"], None,
                   a.at[item, "note"], b.at[item, "note"], None])
    for col, width in {"A": 9, "B": 80, "E": 10, "H": 10, "K": 14, "L": 30, "M": 30, "N": 40}.items():
        ws.column_dimensions[col].width = width
    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = Alignment(wrap_text=True, vertical="top")
    wb.save(CODING / "adjudication.xlsx")
    print(f"\n{len(need)} items need discussion -> {CODING / 'adjudication.xlsx'}")
    print("Fill the apology and innocence columns with the agreed value (1, 0 or u) for every row,")
    print("and innocence_type (F or L) wherever the agreed innocence value is 1,")
    print("then save it as coding/adjudication_completed.xlsx.")


# ---------------------------------------------------------------- step 2

def gold_labels():
    a, b = read_sheet(find_sheet("A")), read_sheet(find_sheet("B"))
    gold = pd.DataFrame(index=a.index)
    for col in methods.CONSTRUCTS:
        gold[col] = np.where(a[col] == b[col], a[col], "")
    gold["innocence_type"] = np.where(a.innocence_type == b.innocence_type, a.innocence_type, "")
    path = CODING / "adjudication_completed.xlsx"
    if path.exists():
        adj = read_sheet(path)
        for col in [*methods.CONSTRUCTS, "innocence_type"]:
            gold.loc[adj.index, col] = adj[col]
    gold.loc[gold.innocence != "1", "innocence_type"] = ""
    missing_type = gold.index[(gold.innocence == "1") & ~gold.innocence_type.isin(["F", "L"])].tolist()
    if missing_type:
        raise SystemExit(f"innocence_type missing for adjudicated innocence claims: {missing_type[:10]}")
    for col in methods.CONSTRUCTS:
        missing = gold.index[~gold[col].isin(VALUES)].tolist()
        if missing:
            raise SystemExit(f"Adjudication missing for {col}: {missing[:10]}")
        # Items both coders marked u, and items still u after discussion, are excluded.
        still_u = gold.index[gold[col] == "u"]
        if len(still_u) and not path.exists():
            raise SystemExit("Some items are u for both coders; resolve them in adjudication first.")
    return gold


def automated_predictions(sample):
    corpus = pd.read_csv(ROOT / "data/processed/person_corpus_exploratory_v1.csv", keep_default_na=False)
    weights = pd.read_csv(ROOT / "results/nmf_v2/document_weights_k6.csv").set_index("execution_number")
    df = sample.merge(corpus[["execution_number", "candidate_text"]], on="execution_number")
    rows = []
    for item in df.itertuples():
        w = weights.loc[item.execution_number].to_dict() if item.execution_number in weights.index else {}
        for col in methods.CONSTRUCTS:
            rows.append({"item_id": item.item_id, "construct": col,
                         "dictionary": methods.dictionary_label(item.candidate_text, col),
                         "nmf": methods.nmf_label(w, col),
                         "nmf_top2": methods.nmf_top2_label(w, col)})
    return pd.DataFrame(rows)


def evaluate():
    sample = pd.read_csv(HERE / "sample.csv")
    gold = gold_labels()
    auto = automated_predictions(sample)
    llm_path = OUTPUTS / "llm_predictions.csv"
    if llm_path.exists():
        llm = pd.read_csv(llm_path, dtype=str)
        coverage = (llm.melt(id_vars=["run", "item_id"], value_vars=list(methods.CONSTRUCTS),
                             var_name="construct", value_name="answer")
                    .groupby(["run", "construct", "answer"]).size().rename("count").reset_index())
        coverage.to_csv(OUTPUTS / "llm_coverage.csv", index=False)
        print(coverage.pivot_table(index=["run", "construct"], columns="answer", values="count", fill_value=0))
        run1 = llm[llm.run == "1"].set_index("item_id")
        for col in methods.CONSTRUCTS:
            answers = auto.loc[auto.construct == col, "item_id"].map(run1[col])
            # Non-answers (refused, failed, invalid) stay missing; they are never scored as 0.
            auto.loc[auto.construct == col, "llm"] = answers.map(methods.LLM_VALUE)
            auto.loc[auto.construct == col, "llm_uncertain_as_1"] = answers.map(
                {**methods.LLM_VALUE, "uncertain": 1})
        unexpected = set(llm[list(methods.CONSTRUCTS)].stack()) - set(methods.LLM_VALUE) - set(methods.LLM_NON_ANSWERS)
        if unexpected:
            raise SystemExit(f"Unexpected LLM answers: {sorted(unexpected)}")
    else:
        print("No LLM predictions found; evaluating dictionary and NMF only.")
    bert_runs = {}
    for source, name in (("own", "bert"), ("eaton_theuer", "bert_et")):
        path = OUTPUTS / f"bert_predictions_{source}.csv"
        if path.exists():
            runs = pd.read_csv(path, dtype={"item_id": str})
            bert_runs[name] = runs
            full = runs[runs.training_size == runs.groupby("construct").training_size.transform("max")]
            mean_prob = full.groupby(["item_id", "construct"]).prob.mean()
            auto[name] = [int(mean_prob[(i, c)] >= methods.BERT_THRESHOLD)
                          for i, c in zip(auto.item_id, auto.construct)]
    method_cols = [m for m in ("dictionary", "nmf", "nmf_top2", "llm", "llm_uncertain_as_1", "bert", "bert_et")
                   if m in auto.columns]
    coders = {c: read_sheet(find_sheet(c)) for c in ("A", "B")}
    auto.to_csv(OUTPUTS / "auto_predictions.csv", index=False)
    gold.reset_index().to_csv(OUTPUTS / "gold_labels.csv", index=False)

    metric_rows, diff_rows, prev_rows, error_rows, exposure_rows = [], [], [], [], []
    seed_rows, coder_rows, et_rows = [], [], []
    exposure = pd.read_csv(HERE / "exposure.csv").set_index("item_id").project_exposure
    texts = sample.merge(pd.read_csv(ROOT / "data/processed/person_corpus_exploratory_v1.csv",
                                     keep_default_na=False)[["execution_number", "candidate_text"]],
                         on="execution_number").set_index("item_id").candidate_text
    # Secondary target: factual innocence only (legal-justification claims are excluded).
    gold["innocence_factual"] = np.where(gold.innocence_type == "L", "u", gold.innocence)
    targets = {"apology": "apology", "innocence": "innocence", "innocence_factual": "innocence"}
    for col, pred_col in targets.items():
        g = gold[col]
        kept = g.index[g != "u"]
        y = g.loc[kept].astype(int).to_numpy()
        lo, hi = wilson(int(y.sum()), len(y))
        prev_rows.append({"construct": col, "n": len(y), "excluded_u": int((g == "u").sum()),
                          "positives": int(y.sum()), "prevalence": float(y.mean()), "ci_low": lo, "ci_high": hi})
        preds = auto[auto.construct == pred_col].set_index("item_id").loc[kept, method_cols]
        gold_y = pd.Series(y, index=kept)
        for m in method_cols:
            answered = preds[m].notna()
            yy, p = gold_y[answered].to_numpy(), preds.loc[answered, m].astype(int).to_numpy()
            res = classification_metrics(yy, p)
            for stat in ("precision", "recall", "f1"):
                res[f"{stat}_ci_low"], res[f"{stat}_ci_high"] = bootstrap(
                    lambda i, s=stat: classification_metrics(yy[i], p[i])[s], len(yy))
            metric_rows.append({"construct": col, "method": m, "n_evaluated": int(answered.sum()),
                                "n_no_answer": int((~answered).sum()), **res})
            for item, gv, pv in zip(preds.index[answered], yy, p):
                if gv != pv:
                    error_rows.append({"construct": col, "method": m, "item_id": item,
                                       "error": "false_positive" if pv else "false_negative",
                                       "text": texts.loc[item]})
            for group, flag in (("documented project exposure", 1), ("no documented exposure", 0)):
                in_group = answered & (exposure.reindex(preds.index) == flag).to_numpy()
                g_res = classification_metrics(gold_y[in_group].to_numpy(),
                                               preds.loc[in_group, m].astype(int).to_numpy())
                exposure_rows.append({"construct": col, "method": m, "group": group,
                                      "n": int(in_group.sum()), **g_res})
        # BERT: every seed and training-set size separately (seed spread and learning curve).
        for name, runs in bert_runs.items():
            for (size, seed), run in runs[runs.construct == pred_col].groupby(["training_size", "seed"]):
                prob = run.set_index("item_id").prob.reindex(kept)
                seed_rows.append({"construct": col, "method": name, "training_size": size, "seed": seed,
                                  **classification_metrics(y, (prob >= methods.BERT_THRESHOLD).astype(int))})
        # Each method against each coder's own labels, before adjudication. A method trained on
        # coder A's labels may agree more with coder A than with coder B.
        if col in methods.CONSTRUCTS:
            all_preds = auto[auto.construct == col].set_index("item_id")
            for m in method_cols:
                for coder, sheet in coders.items():
                    raw = sheet[col].reindex(all_preds.index)
                    use = raw.isin(["1", "0"]) & all_preds[m].notna()
                    coder_rows.append({"construct": col, "method": m, "coder": coder, "n": int(use.sum()),
                                       **classification_metrics(raw[use].astype(int), all_preds.loc[use, m].astype(int))})
        for i, m1 in enumerate(method_cols):
            for m2 in method_cols[i + 1:]:
                both = preds[m1].notna() & preds[m2].notna()
                yy = gold_y[both].to_numpy()
                p1, p2 = preds.loc[both, m1].astype(int).to_numpy(), preds.loc[both, m2].astype(int).to_numpy()
                delta = classification_metrics(yy, p2)["f1"] - classification_metrics(yy, p1)["f1"]
                lo_d, hi_d = bootstrap(lambda i: classification_metrics(yy[i], p2[i])["f1"]
                                       - classification_metrics(yy[i], p1[i])["f1"], len(yy))
                diff_rows.append({"construct": col, "comparison": f"{m2} minus {m1}", "n_items": int(both.sum()),
                                  "f1_difference": delta, "ci_low": lo_d, "ci_high": hi_d})
    # Eaton & Theuer's codes against the adjudicated labels, for sample statements they coded.
    et_path = CODING / "eaton_theuer_labels.csv"
    if et_path.exists():
        et = pd.read_csv(et_path, dtype=str).fillna("")
        et["execution_number"] = et.execution_number.astype(int)
        et = sample.merge(et, on="execution_number").set_index("item_id")
        for col, et_col in targets.items():
            both = gold.index.intersection(et.index)
            g, e = gold.loc[both, col], et.loc[both, et_col].str.strip().str.lower()
            use = g.isin(["1", "0"]) & e.isin(["1", "0"])
            et_rows.append({"construct": col, "n_overlap": len(both), "n_compared": int(use.sum()),
                            "agreement": float((g[use] == e[use]).mean()) if use.any() else float("nan"),
                            "kappa": cohen_kappa(g[use], e[use], ("1", "0")),
                            "both_1": int(((g[use] == "1") & (e[use] == "1")).sum()),
                            "only_human_1": int(((g[use] == "1") & (e[use] == "0")).sum()),
                            "only_eaton_theuer_1": int(((g[use] == "0") & (e[use] == "1")).sum())})
        pd.DataFrame(et_rows).to_csv(OUTPUTS / "eaton_theuer_agreement.csv", index=False)
    if seed_rows:
        pd.DataFrame(seed_rows).to_csv(OUTPUTS / "bert_seed_metrics.csv", index=False)
    pd.DataFrame(coder_rows).to_csv(OUTPUTS / "coder_specific_f1.csv", index=False)
    pd.DataFrame(prev_rows).to_csv(OUTPUTS / "prevalence.csv", index=False)
    metrics_df = pd.DataFrame(metric_rows)
    metrics_df.to_csv(OUTPUTS / "method_metrics.csv", index=False)
    pd.DataFrame(diff_rows).to_csv(OUTPUTS / "method_differences.csv", index=False)
    pd.DataFrame(error_rows).to_csv(OUTPUTS / "errors.csv", index=False)
    pd.DataFrame(exposure_rows).to_csv(OUTPUTS / "exposure_sensitivity.csv", index=False)
    print(pd.DataFrame(prev_rows).round(3).to_string(index=False))
    print(metrics_df[["construct", "method", "precision", "recall", "f1", "f1_ci_low", "f1_ci_high"]]
          .round(3).to_string(index=False))


if __name__ == "__main__":
    import freeze
    parser = argparse.ArgumentParser()
    parser.add_argument("step", choices=["agreement", "evaluate"])
    parser.add_argument("--allow-unfrozen", action="store_true",
                        help="run even if the design differs from protocol_lock.json (for testing only)")
    args = parser.parse_args()
    if not freeze.check() and not args.allow_unfrozen:
        raise SystemExit("Stopped: the design does not match protocol_lock.json.")
    {"agreement": agreement, "evaluate": evaluate}[args.step]()
