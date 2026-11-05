"""Check initialization stability on a fixed corpus and vocabulary."""

import ast
import hashlib
import json
import re
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import sklearn
from scipy.optimize import linear_sum_assignment
from sklearn.decomposition import NMF
from sklearn.exceptions import ConvergenceWarning
from sklearn.feature_extraction.text import TfidfVectorizer

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "results/nmf_v2"
OUT = ROOT / "results/nmf_stability_v1"
OUT.mkdir(parents=True, exist_ok=True)

source = ROOT / "data/processed/model_corpus_v1.csv"
manifest = json.loads((BASE / "run_manifest.json").read_text())

digest = hashlib.sha256(source.read_bytes()).hexdigest()
if digest != manifest["source_sha256"]:
    raise ValueError("Model corpus changed since the v2 run")

# Load only the reviewed normalization function, without running v2.
script_path = ROOT / "src/run_nmf_v2.py"
script = script_path.read_text(encoding="utf-8")
tree = ast.parse(script)
functions = [
    node for node in tree.body
    if isinstance(node, ast.FunctionDef) and node.name == "normalize"
]
if len(functions) != 1:
    raise ValueError("Expected one normalize function")

namespace = {"re": re}
exec(
    compile(ast.get_source_segment(script, functions[0]),
            str(script_path), "exec"),
    namespace,
)
normalize = namespace["normalize"]

df = pd.read_csv(source, keep_default_na=False)
df = df.loc[
    df["preparation_status"].eq("ready_for_exploration")
].sort_values("execution_number").reset_index(drop=True)

params = manifest["vectorizer_parameters"].copy()
params["ngram_range"] = tuple(params["ngram_range"])

vectorizer = TfidfVectorizer(
    preprocessor=normalize,
    lowercase=False,
    token_pattern=r"(?u)\b[a-z][a-z]+\b",
    **params,
)

X = vectorizer.fit_transform(df["model_text"])
X = X[np.asarray(X.getnnz(axis=1)).ravel() > 0]
terms = vectorizer.get_feature_names_out()

if X.shape != (
    manifest["documents_modeled"], manifest["features"]
):
    raise ValueError("Feature matrix shape differs from v2")

def fit(k, init, seed):
    model = NMF(
        n_components=k,
        init=init,
        random_state=seed,
        max_iter=1000,
        tol=1e-4,
    )
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always", ConvergenceWarning)
        model.fit(X)

    converged = not any(
        issubclass(w.category, ConvergenceWarning)
        for w in caught
    )
    H = model.components_
    norms = np.linalg.norm(H, axis=1, keepdims=True)
    H = H / np.where(norms > 0, norms, 1)
    return model, H, converged

details = []
runs = []

for k in [4, 6, 8]:
    reference, H_ref, reference_ok = fit(k, "nndsvda", 42)

    # Check that reference topic ordering reproduces the saved v2 terms.
    saved = pd.read_csv(BASE / f"topic_terms_k{k}.csv")
    for topic in range(k):
        expected = saved.loc[
            saved["topic"].eq(topic + 1)
        ].sort_values("rank")["term"].tolist()
        actual = terms[
            H_ref[topic].argsort()[::-1][:len(expected)]
        ].tolist()
        if actual != expected:
            raise ValueError(
                f"k={k}: reference terms differ from saved v2"
            )

    for seed in [0, 1, 2, 3, 4]:
        model, H_new, converged = fit(k, "random", seed)

        # Topic numbers may change between runs.
        similarity = H_ref @ H_new.T
        ref_ids, new_ids = linear_sum_assignment(-similarity)

        matched = []
        for ref_id, new_id in zip(ref_ids, new_ids):
            cosine = float(similarity[ref_id, new_id])
            left = set(H_ref[ref_id].argsort()[-15:])
            right = set(H_new[new_id].argsort()[-15:])
            jaccard = len(left & right) / len(left | right)

            details.append({
                "k": k,
                "seed": seed,
                "reference_topic": int(ref_id + 1),
                "matched_topic": int(new_id + 1),
                "cosine_similarity": cosine,
                "top15_jaccard": jaccard,
                "converged": converged,
                "reference_converged": reference_ok,
            })
            matched.append(cosine)

        runs.append({
            "k": k,
            "seed": seed,
            "mean_matched_cosine": float(np.mean(matched)),
            "minimum_matched_cosine": float(np.min(matched)),
            "reconstruction_error": float(model.reconstruction_err_),
            "iterations": int(model.n_iter_),
            "converged": converged,
            "reference_converged": reference_ok,
        })

detail_df = pd.DataFrame(details)
run_df = pd.DataFrame(runs)

detail_df.to_csv(
    OUT / "matched_topics.csv", index=False, encoding="utf-8-sig"
)
run_df.to_csv(
    OUT / "runs.csv", index=False, encoding="utf-8-sig"
)

summary = run_df.groupby("k").agg(
    mean_similarity=("mean_matched_cosine", "mean"),
    weakest_match=("minimum_matched_cosine", "min"),
    converged_runs=("converged", "sum"),
)

topic_summary = detail_df.groupby(
    ["k", "reference_topic"]
).agg(
    mean_cosine=("cosine_similarity", "mean"),
    minimum_cosine=("cosine_similarity", "min"),
    mean_top15_jaccard=("top15_jaccard", "mean"),
)

print("\nOVERALL INITIALIZATION STABILITY")
print(summary.round(3).to_string())

print("\nPER-TOPIC STABILITY")
print(topic_summary.round(3).to_string())

(OUT / "manifest.json").write_text(
    json.dumps({
        "source_sha256": digest,
        "normalization_script_sha256":
            hashlib.sha256(script_path.read_bytes()).hexdigest(),
        "sklearn": sklearn.__version__,
        "seeds": [0, 1, 2, 3, 4],
        "comparison": "Random initialization versus v2 NNDSVDa reference",
        "scope": "Fixed-data initialization stability only; not semantic validity or sampling robustness.",
    }, indent=2) + "\n",
    encoding="utf-8",
)

print("\nSaved:", OUT)
print("Source data, manual labels and v2 results were not modified.")
