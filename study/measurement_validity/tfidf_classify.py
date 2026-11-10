"""Supervised baseline (protocol version 1.3): TF-IDF features with logistic regression.

Trained on exactly the same statements and labels as the BERT classifier, so the comparison
separates what BERT adds from what supervision on these labels alone achieves. Runs on a CPU
in seconds, after both coders have finished the study sample:

    python study/measurement_validity/tfidf_classify.py --labels eaton_theuer   # primary
    python study/measurement_validity/tfidf_classify.py --labels own            # fallback

Writes outputs/tfidf_predictions_<labels>.csv (item_id, construct, training_size, seed, prob)
and outputs/tfidf_run_<labels>.json (training counts and skipped runs).
The fit is deterministic; seed is recorded as 0.
"""
import argparse
import json
import sys
from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import bert_classify  # noqa: E402  (shares training labels, texts and learning-curve subsets)
import methods  # noqa: E402

CODING = HERE / "coding"
OUTPUTS = HERE / "outputs"

# Fixed in advance; no tuning.
NGRAMS = (1, 2)
MIN_DF = 2
C = 1.0


def model():
    return make_pipeline(
        TfidfVectorizer(lowercase=True, ngram_range=NGRAMS, min_df=MIN_DF, sublinear_tf=True),
        LogisticRegression(C=C, class_weight="balanced", solver="liblinear", max_iter=1000),
    )


def run(source):
    missing = [f for f in ("coder_A_completed.xlsx", "coder_B_completed.xlsx") if not (CODING / f).exists()]
    if missing:
        raise SystemExit(f"Automated methods run only after both coders finish; missing {missing}.")
    bert_classify.CODING = CODING
    texts = bert_classify.texts_by_execution()
    sample = pd.read_csv(HERE / "sample.csv")
    test_texts = sample.execution_number.map(texts).tolist()
    labels, dropped, _ = bert_classify.training_labels(source)

    rows, counts, skipped = [], {}, []
    for construct in methods.CONSTRUCTS:
        coded = labels[construct][labels[construct] != "u"]
        counts[construct] = {"statements": int(len(coded)), "positives": int((coded == "1").sum()),
                             "excluded_u": int((labels[construct] == "u").sum())}
        for size, members in bert_classify.curve_subsets(coded.index).items():
            subset = coded[coded.index.isin(members)]
            if not bert_classify.has_both_classes(subset):
                skipped.append({"construct": construct, "training_size": size, "reason": "single class"})
                continue
            fitted = model().fit(subset.index.map(texts).tolist(), subset.astype(int).to_numpy())
            probs = fitted.predict_proba(test_texts)[:, 1]
            rows += [{"item_id": i, "construct": construct, "training_size": size, "seed": 0, "prob": float(p)}
                     for i, p in zip(sample.item_id, probs)]
    OUTPUTS.mkdir(exist_ok=True)
    pd.DataFrame(rows).to_csv(OUTPUTS / f"tfidf_predictions_{source}.csv", index=False)
    meta = {"labels": source, "training": counts, "dropped_study_sample_statements": dropped,
            "skipped_runs": skipped, "settings": {"ngrams": list(NGRAMS), "min_df": MIN_DF, "C": C}}
    (OUTPUTS / f"tfidf_run_{source}.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(f"TF-IDF baseline trained on {source} labels; predictions written.")


if __name__ == "__main__":
    import freeze
    parser = argparse.ArgumentParser()
    parser.add_argument("--labels", choices=["own", "eaton_theuer"], required=True)
    parser.add_argument("--allow-unfrozen", action="store_true",
                        help="run even if the design differs from protocol_lock.json (for testing only)")
    args = parser.parse_args()
    if not freeze.check() and not args.allow_unfrozen:
        raise SystemExit("Stopped: the design does not match protocol_lock.json.")
    run(args.labels)
