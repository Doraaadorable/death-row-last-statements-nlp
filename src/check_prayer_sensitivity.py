"""Selected-prayer record sensitivity; source corpus unchanged."""

import hashlib
import json
import re
import warnings
from run_provenance import code_provenance
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import linear_sum_assignment
from sklearn.decomposition import NMF
from sklearn.exceptions import ConvergenceWarning
from text_features import make_vectorizer, identical_column_groups, group_jaccard, verify_reference

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "results/nmf_v2"
OUT = ROOT / "results/prayer_sensitivity_v2"
OUT.mkdir(parents=True, exist_ok=True)

source = ROOT / "data/processed/model_corpus_v1.csv"
manifest = json.loads((BASE / "run_manifest.json").read_text())

if hashlib.sha256(source.read_bytes()).hexdigest() != manifest["source_sha256"]:
    raise ValueError("Source differs from the v2 run")

df = pd.read_csv(source, keep_default_na=False)
df = df.loc[
    df["preparation_status"].eq("ready_for_exploration")
].sort_values("execution_number").reset_index(drop=True)

vectorizer = make_vectorizer(manifest["vectorizer_parameters"])
X = vectorizer.fit_transform(df["model_text"])
nonzero = np.asarray(X.getnnz(axis=1)).ravel() > 0
df = df.loc[nonzero].reset_index(drop=True)
X = X[nonzero]
terms = vectorizer.get_feature_names_out()
groups = identical_column_groups(X)

if X.shape != (manifest["documents_modeled"], manifest["features"]):
    raise ValueError("Feature matrix differs from v2")

prayer_pattern = (
    r"\bthe lord is my shepherd\b|"
    r"\bour father\b.{0,40}\bheaven\b"
)
flagged = df["model_text"].str.contains(
    prayer_pattern, case=False, regex=True
)
keep = (~flagged).to_numpy()

print("\nRecords containing selected prayer phrases:")
print(
    df.loc[
        flagged,
        ["execution_number", "model_word_count", "source_url"]
    ].to_string(index=False)
)
df.loc[~keep, ["execution_number", "model_word_count", "model_text"]].to_csv(
    OUT / "selected_prayer_records.csv",
    index=False, encoding="utf-8-sig",
)

def fit(matrix, k):
    model = NMF(
        n_components=k, init="nndsvda", random_state=42,
        max_iter=1000, tol=1e-4,
    )
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always", ConvergenceWarning)
        model.fit(matrix)

    H = model.components_
    norms = np.linalg.norm(H, axis=1, keepdims=True)
    H = H / np.where(norms > 0, norms, 1)

    converged = not any(
        issubclass(w.category, ConvergenceWarning) for w in caught
    )
    return H, converged

rows = []
print("Full modeled documents:", len(df))
print("Documents without selected prayer phrases:", int(keep.sum()))
print("Selected prayer records omitted in this comparison:", int((~keep).sum()))

for k in [6, 8]:
    reference, reference_ok = fit(X, k)
    alternative, alternative_ok = fit(X[keep], k)

    verify_reference(BASE, k, reference, terms, X)

    similarity = reference @ alternative.T
    left_ids, right_ids = linear_sum_assignment(-similarity)

    print(f"\n=== k={k} ===")
    print("Both fits converged:", reference_ok and alternative_ok)

    for left, right in zip(left_ids, right_ids):
        cosine = float(similarity[left, right])
        jaccard = group_jaccard(reference[left], alternative[right], terms, groups)

        rows.append({
            "k": k,
            "reference_topic": int(left + 1),
            "matched_topic": int(right + 1),
            "cosine_similarity": cosine,
            "top15_group_jaccard": jaccard,
            "reference_converged": reference_ok,
            "alternative_converged": alternative_ok,
        })

        keywords = terms[
            alternative[right].argsort()[::-1][:10]
        ]
        print(
            f"Reference topic {left+1}: "
            f"cosine={cosine:.3f}, top15 group Jaccard={jaccard:.3f}"
        )
        print("Matched terms:", ", ".join(keywords))

pd.DataFrame(rows).to_csv(
    OUT / "matched_topics.csv",
    index=False, encoding="utf-8-sig",
)

(OUT / "method.json").write_text(
    json.dumps({
        "source_sha256": manifest["source_sha256"],
        "execution_provenance": code_provenance(__file__),
        "selected_phrase_pattern": prayer_pattern,
        "omitted_execution_numbers":
            df.loc[~keep, "execution_number"].astype(int).tolist(),
        "removal_unit": "Entire record, including its non-prayer content",
        "features": "Fixed vocabulary and IDF fitted on full eligible corpus",
        "initialization": "nndsvda, random_state=42",
        "scope": (
            "Selected-prayer record-removal sensitivity, including any "
            "resulting initialization changes. Not a population test."
        ),
    }, indent=2) + "\n",
    encoding="utf-8",
)

print("\nSaved:", OUT)
print("Main corpus, manual labels and previous results were not modified.")


