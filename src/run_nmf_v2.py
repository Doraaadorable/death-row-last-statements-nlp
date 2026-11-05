"""Exploratory NMF baseline. Does not use or modify manual labels."""

import hashlib
import json
import platform
import re
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import sklearn
from sklearn.decomposition import NMF
from sklearn.exceptions import ConvergenceWarning
from sklearn.feature_extraction.text import (
    ENGLISH_STOP_WORDS,
)

from text_features import make_vectorizer

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/processed/model_corpus_v1.csv"
OUT = ROOT / "results/nmf_v2"
OUT.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(SOURCE, keep_default_na=False)
df = df.loc[
    df["preparation_status"].eq("ready_for_exploration")
].copy().sort_values("execution_number").reset_index(drop=True)

assert df["execution_number"].is_unique
assert df["model_text"].str.strip().ne("").all()

# Preserve common negation terms. TF-IDF still does not understand negation.
stop_words = sorted(
    set(ENGLISH_STOP_WORDS) - {"no", "not", "nor", "never"}
)

vectorizer = make_vectorizer({
    "stop_words": stop_words, "ngram_range": (1, 2), "min_df": 2,
    "max_df": 0.85, "max_features": 5000, "sublinear_tf": True,
})

X = vectorizer.fit_transform(df["model_text"])

# Some very short texts may have no retained vocabulary.
nonzero = np.asarray(X.getnnz(axis=1)).ravel() > 0
zero_records = df.loc[~nonzero, ["execution_number", "model_text"]]
zero_records.to_csv(
    OUT / "zero_feature_records.csv",
    index=False, encoding="utf-8-sig",
)

df = df.loc[nonzero].reset_index(drop=True)
X = X[nonzero]
terms = vectorizer.get_feature_names_out()

if min(X.shape) < 8:
    raise ValueError("Not enough documents or features for this comparison")

manifest = {
    "normalization_version": "v2",
    "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
    "python": platform.python_version(),
    "sklearn": sklearn.__version__,
    "numpy": np.__version__,
    "pandas": pd.__version__,
    "documents_modeled": len(df),
    "zero_feature_records": len(zero_records),
    "features": len(terms),
    "topic_counts": [4, 6, 8],
    "random_state": 42,
    "vectorizer_parameters": {
        "ngram_range": [1, 2],
        "min_df": 2,
        "max_df": 0.85,
        "max_features": 5000,
        "sublinear_tf": True,
        "stop_words": stop_words,
    },
    "runs": [],
}

print("Documents modeled:", len(df))
print("Zero-feature records:", len(zero_records))
print("Vocabulary features:", len(terms))

for k in [4, 6, 8]:
    model = NMF(
        n_components=k,
        init="nndsvda",
        random_state=42,
        max_iter=1000,
        tol=1e-4,
    )

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always", ConvergenceWarning)
        W = model.fit_transform(X)

    convergence_warning = any(
        issubclass(w.category, ConvergenceWarning) for w in caught
    )

    # Normalize each topic's term vector to unit length.
    # Adjust document coefficients to preserve the reconstructed matrix.
    norms = np.linalg.norm(model.components_, axis=1)
    H = model.components_ / np.where(norms > 0, norms, 1)[:, None]
    adjusted_W = W * norms[None, :]

    weights = pd.DataFrame(
        adjusted_W,
        columns=[f"topic_{t+1}" for t in range(k)],
    )
    weights.insert(0, "execution_number", df["execution_number"].to_numpy())
    weights.to_csv(
        OUT / f"document_weights_k{k}.csv",
        index=False, encoding="utf-8-sig",
    )

    topic_rows = []
    review = [
        f"# NMF candidate themes: k={k}",
        "",
        "Topic numbers are local to this run, not predefined labels.",
        "Coefficients are not probabilities or validated theme prevalence.",
        "Candidate examples prioritize texts of at least 20 words; "
        "shorter texts remain in fitting.",
        "",
    ]

    print(f"\n=== {k} TOPICS ===")

    for t in range(k):
        top = H[t].argsort()[::-1][:15]
        keywords = [str(terms[j]) for j in top]

        for rank, j in enumerate(top, start=1):
            topic_rows.append({
                "topic": t + 1,
                "rank": rank,
                "term": terms[j],
                "term_weight": float(H[t, j]),
            })

        # Rank by adjusted coefficient; avoid zero-weight examples.
        eligible = np.flatnonzero(
            (df["model_word_count"].to_numpy() >= 20)
            & (adjusted_W[:, t] > 0)
        )
        ranked = eligible[
            np.argsort(-adjusted_W[eligible, t], kind="stable")
        ][:3]

        print(f"Topic {t+1}: {', '.join(keywords)}")

        review.extend([
            f"## Topic {t+1}",
            "",
            "Top terms: " + ", ".join(keywords),
            "",
        ])

        for idx in ranked:
            row = df.iloc[idx]
            review.extend([
                f"### Execution {row['execution_number']}",
                "",
                f"Source: {row['source_url']}",
                "",
                row["model_text"],
                "",
            ])

    pd.DataFrame(topic_rows).to_csv(
        OUT / f"topic_terms_k{k}.csv",
        index=False, encoding="utf-8-sig",
    )

    (OUT / f"topic_review_k{k}.md").write_text(
        "\n".join(review), encoding="utf-8",
    )

    manifest["runs"].append({
        "k": k,
        "iterations": int(model.n_iter_),
        "reconstruction_error": float(model.reconstruction_err_),
        "convergence_warning": convergence_warning,
    })

    print("Iterations:", model.n_iter_)
    print("Convergence warning:", convergence_warning)

(OUT / "run_manifest.json").write_text(
    json.dumps(manifest, indent=2) + "\n",
    encoding="utf-8",
)

print("\nSaved:", OUT)
print("Manual labels were not used. Source files were not modified.")

