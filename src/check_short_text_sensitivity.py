"""Fixed-feature sensitivity check; does not alter the main corpus."""

import ast
import hashlib
import json
import re
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import linear_sum_assignment
from sklearn.decomposition import NMF
from sklearn.exceptions import ConvergenceWarning
from sklearn.feature_extraction.text import TfidfVectorizer

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "results/nmf_v2"
OUT = ROOT / "results/short_text_sensitivity_v1"
OUT.mkdir(parents=True, exist_ok=True)

source = ROOT / "data/processed/model_corpus_v1.csv"
manifest = json.loads((BASE / "run_manifest.json").read_text())

if hashlib.sha256(source.read_bytes()).hexdigest() != manifest["source_sha256"]:
    raise ValueError("Source differs from the v2 run")

script = (ROOT / "src/run_nmf_v2.py").read_text(encoding="utf-8")
nodes = [
    n for n in ast.parse(script).body
    if isinstance(n, ast.FunctionDef) and n.name == "normalize"
]
if len(nodes) != 1:
    raise ValueError("Expected one normalization function")

namespace = {"re": re}
exec(
    compile(ast.get_source_segment(script, nodes[0]), "<normalize>", "exec"),
    namespace,
)

df = pd.read_csv(source, keep_default_na=False)
df = df.loc[
    df["preparation_status"].eq("ready_for_exploration")
].sort_values("execution_number").reset_index(drop=True)

params = manifest["vectorizer_parameters"].copy()
params["ngram_range"] = tuple(params["ngram_range"])

vectorizer = TfidfVectorizer(
    preprocessor=namespace["normalize"],
    lowercase=False,
    token_pattern=r"(?u)\b[a-z][a-z]+\b",
    **params,
)
X = vectorizer.fit_transform(df["model_text"])
nonzero = np.asarray(X.getnnz(axis=1)).ravel() > 0
df = df.loc[nonzero].reset_index(drop=True)
X = X[nonzero]
terms = vectorizer.get_feature_names_out()

if X.shape != (manifest["documents_modeled"], manifest["features"]):
    raise ValueError("Feature matrix differs from v2")

keep = df["model_word_count"].ge(10).to_numpy()
df.loc[~keep, ["execution_number", "model_word_count", "model_text"]].to_csv(
    OUT / "short_records_in_comparison.csv",
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
print("Documents of at least 10 words:", int(keep.sum()))
print("Short documents omitted in this comparison:", int((~keep).sum()))

for k in [6, 8]:
    reference, reference_ok = fit(X, k)
    alternative, alternative_ok = fit(X[keep], k)

    saved = pd.read_csv(BASE / f"topic_terms_k{k}.csv")
    for topic in range(k):
        expected = saved.loc[
            saved["topic"].eq(topic + 1)
        ].sort_values("rank")["term"].tolist()
        actual = terms[
            reference[topic].argsort()[::-1][:len(expected)]
        ].tolist()
        if actual != expected:
            raise ValueError("Reference does not reproduce saved v2")

    similarity = reference @ alternative.T
    left_ids, right_ids = linear_sum_assignment(-similarity)

    print(f"\n=== k={k} ===")
    print("Both fits converged:", reference_ok and alternative_ok)

    for left, right in zip(left_ids, right_ids):
        top_left = set(reference[left].argsort()[-15:])
        top_right = set(alternative[right].argsort()[-15:])
        cosine = float(similarity[left, right])
        jaccard = len(top_left & top_right) / len(top_left | top_right)

        rows.append({
            "k": k,
            "reference_topic": int(left + 1),
            "matched_topic": int(right + 1),
            "cosine_similarity": cosine,
            "top15_jaccard": jaccard,
            "reference_converged": reference_ok,
            "alternative_converged": alternative_ok,
        })

        keywords = terms[
            alternative[right].argsort()[::-1][:10]
        ]
        print(
            f"Reference topic {left+1}: "
            f"cosine={cosine:.3f}, top15 Jaccard={jaccard:.3f}"
        )
        print("Matched terms:", ", ".join(keywords))

pd.DataFrame(rows).to_csv(
    OUT / "matched_topics.csv",
    index=False, encoding="utf-8-sig",
)

(OUT / "method.json").write_text(
    json.dumps({
        "source_sha256": manifest["source_sha256"],
        "minimum_words_comparison": 10,
        "features": "Fixed vocabulary and IDF fitted on full eligible corpus",
        "initialization": "nndsvda, random_state=42",
        "scope": (
            "Exploratory document-removal sensitivity, including any "
            "resulting initialization changes. Not a population test."
        ),
    }, indent=2) + "\n",
    encoding="utf-8",
)

print("\nSaved:", OUT)
print("Main corpus, manual labels and previous results were not modified.")
