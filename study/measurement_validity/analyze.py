"""Analysis for the measurement study, in two steps.

1. After both coders finish (sheets saved in coding/):
       python study/measurement_validity/analyze.py agreement
   Writes outputs/agreement.csv and coding/adjudication.xlsx (items to discuss).

2. After adjudication is filled in and saved as coding/adjudication_completed.xlsx:
       python study/measurement_validity/analyze.py evaluate
   Writes outputs/gold_labels.csv, outputs/auto_predictions.csv, outputs/method_metrics.csv,
   outputs/method_differences.csv, outputs/prevalence.csv and outputs/errors.csv.
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


def bootstrap(stat, n, n_boot=N_BOOT, seed=BOOT_SEED):
    """Percentile 95% interval of stat(index_array) over resampled items."""
    rng = np.random.default_rng(seed)
    draws = np.array([stat(rng.integers(0, n, n)) for _ in range(n_boot)])
    draws = draws[~np.isnan(draws)]
    return float(np.percentile(draws, 2.5)), float(np.percentile(draws, 97.5))


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
                         "nmf": methods.nmf_label(w, col)})
    return pd.DataFrame(rows)


def evaluate():
    sample = pd.read_csv(HERE / "sample.csv")
    gold = gold_labels()
    auto = automated_predictions(sample)
    llm_path = OUTPUTS / "llm_predictions.csv"
    if llm_path.exists():
        llm = pd.read_csv(llm_path)
        for col in methods.CONSTRUCTS:
            primary = llm[llm.run == 1].set_index("item_id")[col]
            auto.loc[auto.construct == col, "llm"] = auto.loc[auto.construct == col, "item_id"].map(
                primary.map(lambda v: methods.LLM_VALUE.get(v, 0)))
    else:
        print("No LLM predictions found; evaluating dictionary and NMF only.")
    method_cols = [m for m in ("dictionary", "nmf", "llm") if m in auto.columns]
    auto.to_csv(OUTPUTS / "auto_predictions.csv", index=False)
    gold.reset_index().to_csv(OUTPUTS / "gold_labels.csv", index=False)

    metric_rows, diff_rows, prev_rows, error_rows = [], [], [], []
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
        preds = auto[auto.construct == pred_col].set_index("item_id").loc[kept, method_cols].astype(int)
        for m in method_cols:
            p = preds[m].to_numpy()
            res = classification_metrics(y, p)
            for stat in ("precision", "recall", "f1"):
                res[f"{stat}_ci_low"], res[f"{stat}_ci_high"] = bootstrap(
                    lambda i, s=stat: classification_metrics(y[i], p[i])[s], len(y))
            metric_rows.append({"construct": col, "method": m, **res})
            for item, gv, pv in zip(kept, y, p):
                if gv != pv:
                    error_rows.append({"construct": col, "method": m, "item_id": item,
                                       "error": "false_positive" if pv else "false_negative",
                                       "text": texts.loc[item]})
        for i, m1 in enumerate(method_cols):
            for m2 in method_cols[i + 1:]:
                p1, p2 = preds[m1].to_numpy(), preds[m2].to_numpy()
                delta = classification_metrics(y, p2)["f1"] - classification_metrics(y, p1)["f1"]
                lo_d, hi_d = bootstrap(lambda i: classification_metrics(y[i], p2[i])["f1"]
                                       - classification_metrics(y[i], p1[i])["f1"], len(y))
                diff_rows.append({"construct": col, "comparison": f"{m2} minus {m1}", "f1_difference": delta,
                                  "ci_low": lo_d, "ci_high": hi_d})
    pd.DataFrame(prev_rows).to_csv(OUTPUTS / "prevalence.csv", index=False)
    metrics_df = pd.DataFrame(metric_rows)
    metrics_df.to_csv(OUTPUTS / "method_metrics.csv", index=False)
    pd.DataFrame(diff_rows).to_csv(OUTPUTS / "method_differences.csv", index=False)
    pd.DataFrame(error_rows).to_csv(OUTPUTS / "errors.csv", index=False)
    print(pd.DataFrame(prev_rows).round(3).to_string(index=False))
    print(metrics_df[["construct", "method", "precision", "recall", "f1", "f1_ci_low", "f1_ci_high"]]
          .round(3).to_string(index=False))


if __name__ == "__main__":
    import freeze
    freeze.check()
    parser = argparse.ArgumentParser()
    parser.add_argument("step", choices=["agreement", "evaluate"])
    {"agreement": agreement, "evaluate": evaluate}[parser.parse_args().step]()
