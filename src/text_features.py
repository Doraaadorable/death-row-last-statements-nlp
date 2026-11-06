"""Shared v2 features and numerical checks; fitting retains every column."""
import hashlib
import json
import platform
import re
from pathlib import Path
import numpy as np
import pandas as pd
import sklearn
from scipy.optimize import linear_sum_assignment
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF

def normalize(text):
    text = text.replace("’", "'").replace("‘", "'").lower()

    # Normalize alternative spellings of plural "you".
    text = re.sub(r"\b(?:y'all|ya'll)s\b", "your", text)
    text = re.sub(r"\b(?:y'all|ya'll)\b", "you all", text)

    # Preserve negation while expanding standard contractions.
    text = re.sub(r"\bwon't\b", "will not", text)
    text = re.sub(r"\bcan't\b", "can not", text)
    text = re.sub(r"\bshan't\b", "shall not", text)

    # "Ain't" has several possible auxiliaries; retain only
    # its clear negation rather than inventing an auxiliary.
    text = re.sub(r"\bain't\b", "not", text)
    text = re.sub(r"n't\b", " not", text)

    text = re.sub(r"\bi'm\b", "i am", text)
    text = re.sub(r"\blet's\b", "let us", text)
    text = re.sub(r"\bma'am\b", "madam", text)

    text = re.sub(r"'re\b", " are", text)
    text = re.sub(r"'ve\b", " have", text)
    text = re.sub(r"'ll\b", " will", text)

    # 'd may mean had/would. Remove the suffix without
    # choosing an interpretation. Both are baseline stopwords.
    text = re.sub(r"'d\b", "", text)

    # 's can be possessive or is/has. Retain the base word;
    # do not assign a grammatical interpretation.
    text = re.sub(r"'s\b", "", text)

    return text

def make_vectorizer(params):
    params = dict(params)
    params['ngram_range'] = tuple(params['ngram_range'])
    return TfidfVectorizer(preprocessor=normalize, lowercase=False,
        token_pattern=r"(?u)\b[a-z][a-z]+\b", **params)


def identical_column_groups(X):
    matrix = X.tocsc(copy=True)
    matrix.sum_duplicates()
    matrix.sort_indices()
    groups = {}
    for j in range(matrix.shape[1]):
        start, end = matrix.indptr[j:j+2]
        key = (matrix.indices[start:end].tobytes(), matrix.data[start:end].tobytes())
        groups.setdefault(key, []).append(j)
    return list(groups.values())


def top_groups(weights, terms, groups, n=15):
    scores = np.array([np.mean(weights[g]) for g in groups])
    representatives = np.array([min(terms[g]) for g in groups])
    return set(np.lexsort((representatives, -np.round(scores, 10)))[:n])


def group_jaccard(left, right, terms, groups):
    a = top_groups(left, terms, groups)
    b = top_groups(right, terms, groups)
    return len(a & b) / len(a | b)


def verify_reference(base, k, H, terms, X):
    """Validate published partial evidence, then save/check regenerated full H.

    The historical release did not save full H. Never describe this file as
    a recovered historical matrix. Its first validation is necessarily partial.
    """
    saved = pd.read_csv(base / f'topic_terms_k{k}.csv')
    lookup = {term: i for i, term in enumerate(terms)}
    for t in range(k):
        part = saved.loc[saved.topic.eq(t+1)]
        ids = [lookup[term] for term in part.term]
        if not np.allclose(H[t, ids], part.term_weight, rtol=1e-8, atol=1e-12):
            raise ValueError('Published term weights differ from regenerated reference')
        # Every omitted term must be no larger than the saved cutoff, allowing ties.
        omitted = np.ones(len(terms), dtype=bool)
        omitted[ids] = False
        if H[t, omitted].max(initial=0) > part.term_weight.min() + 1e-10:
            raise ValueError('Published top-term cutoff differs')
    published = pd.read_csv(base / f'document_weights_k{k}.csv')
    W = published[[f'topic_{i+1}' for i in range(k)]].to_numpy()
    model = NMF(n_components=k, init='nndsvda', random_state=42,
                max_iter=1000, tol=1e-4)
    raw_W = model.fit_transform(X)
    norms = np.linalg.norm(model.components_, axis=1)
    actual_W = raw_W * norms[None, :]
    actual_H = model.components_ / np.where(norms > 0, norms, 1)[:, None]
    if not np.allclose(actual_H, H, rtol=1e-8, atol=1e-12):
        raise ValueError('Regenerated reference differs from reference fit')
    if not np.allclose(actual_W, W, rtol=1e-8, atol=1e-10):
        raise ValueError('Published document coefficients differ')
    reference_dir = base.parent / 'reference_numeric_v1'
    reference_dir.mkdir(exist_ok=True)
    vocab = reference_dir / 'vocabulary.json'
    vocabulary = terms.tolist()
    if vocab.exists() and json.loads(vocab.read_text()) != vocabulary:
        raise ValueError('Ordered vocabulary changed')
    path = reference_dir / f'topic_term_k{k}.csv.gz'
    minimum_cosine = None
    if path.exists():
        old = pd.read_csv(path).to_numpy()
        if old.shape != H.shape:
            raise ValueError('Full reference matrix shape changed')
        similarities = old @ H.T
        rows, cols = linear_sum_assignment(-similarities)
        minimum_cosine = float(similarities[rows, cols].min())
        if minimum_cosine < 1 - 1e-8:
            raise ValueError('Full-vector reference cosine check failed')
    else:
        pd.DataFrame(H, columns=terms).to_csv(path, index=False)
    if not vocab.exists():
        vocab.write_text(json.dumps(vocabulary) + '\n')
    return minimum_cosine

