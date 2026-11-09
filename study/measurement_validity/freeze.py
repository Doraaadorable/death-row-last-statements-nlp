"""Freeze the study design before coding starts, and check it later.

    python study/measurement_validity/freeze.py          # create protocol_lock.json (once)
    python study/measurement_validity/freeze.py --check  # verify nothing frozen has changed
"""
import argparse
import datetime
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LOCK = HERE / "protocol_lock.json"
FROZEN = [
    "study/measurement_validity/PROTOCOL.md",
    "study/measurement_validity/CODEBOOK.md",
    "study/measurement_validity/methods.py",
    "study/measurement_validity/analyze.py",
    "study/measurement_validity/sample.csv",
    "results/nmf_v2/document_weights_k6.csv",
]


def sha(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def sample_text_hash():
    """Hash of the sampled statement texts, so the coded material itself is fixed."""
    import pandas as pd
    sample = pd.read_csv(HERE / "sample.csv")
    corpus = pd.read_csv(ROOT / "data/processed/person_corpus_exploratory_v1.csv", keep_default_na=False)
    texts = sample.merge(corpus, on="execution_number").sort_values("item_id")
    blob = "\n".join(f"{i}\t{t}" for i, t in zip(texts.item_id, texts.candidate_text))
    return hashlib.sha256(blob.encode()).hexdigest()


def check():
    if not LOCK.exists():
        print("WARNING: protocol_lock.json does not exist; the design has not been frozen.")
        return False
    lock = json.loads(LOCK.read_text())
    changed = [p for p, h in lock["files"].items() if sha(p) != h]
    if (ROOT / "data/processed/person_corpus_exploratory_v1.csv").exists() and \
            sample_text_hash() != lock["sample_text_sha256"]:
        changed.append("sampled statement texts")
    if changed:
        print("WARNING: changed since the design was frozen:", ", ".join(changed))
        return False
    print(f"Design unchanged since {lock['frozen_at_utc']}.")
    return True


def freeze():
    if LOCK.exists():
        raise SystemExit("protocol_lock.json already exists. A new design needs a new version, not a re-freeze.")
    codebook = (HERE / "CODEBOOK.md").read_text()
    if "_To be filled in before freezing._" in codebook:
        raise SystemExit("Fill in 'Differences from Eaton & Theuer' in CODEBOOK.md first (write 'None' if there are none).")
    lock = {"frozen_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
            "files": {p: sha(p) for p in FROZEN},
            "sample_text_sha256": sample_text_hash()}
    LOCK.write_text(json.dumps(lock, indent=2) + "\n")
    print(f"Frozen at {lock['frozen_at_utc']}. Commit protocol_lock.json before anyone starts coding.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    if parser.parse_args().check:
        check()
    else:
        freeze()
