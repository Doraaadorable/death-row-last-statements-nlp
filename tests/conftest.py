"""Skip tests whose inputs are not installed, instead of failing.

- Tests marked below need the data-v1 snapshot extracted into data/processed/.
- The syntax prototype tests need spaCy (pip install -r requirements-syntax.txt).
"""
import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
HAS_DATA = (ROOT / "data/processed/model_corpus_v1.csv").exists()
HAS_SPACY = importlib.util.find_spec("spacy") is not None

NEEDS_DATA = {"test_claim_consistency_audit.py", "test_prepare_confirmed_claims.py", "test_snapshot40.py"}
NEEDS_SPACY = {"test_syntactic_candidates_v1.py", "test_syntax_semantics_v1.py"}


def pytest_collection_modifyitems(config, items):
    for item in items:
        name = Path(str(item.fspath)).name
        if name in NEEDS_DATA and not HAS_DATA:
            item.add_marker(pytest.mark.skip(reason="needs the data-v1 snapshot in data/processed/"))
        if name in NEEDS_SPACY and not HAS_SPACY:
            item.add_marker(pytest.mark.skip(reason="needs spaCy: pip install -r requirements-syntax.txt"))
