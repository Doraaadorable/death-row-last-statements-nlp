"""Freeze the study design before coding starts, and check it later.

    python study/measurement_validity/freeze.py                       # first freeze (version 1.0)
    python study/measurement_validity/freeze.py --check               # verify nothing frozen has changed
    python study/measurement_validity/freeze.py --new-version 1.1 --reason "..."
        # amend the design: keeps the previous lock as protocol_lock_v<old>.json

An amendment is allowed only before any coding results exist, and the reason must also be
recorded under "Amendments" in PROTOCOL.md.
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
    "study/measurement_validity/OSF_REGISTRATION.md",
    "study/measurement_validity/methods.py",
    "study/measurement_validity/analyze.py",
    "study/measurement_validity/llm_classify.py",
    "study/measurement_validity/bert_classify.py",
    "study/measurement_validity/tfidf_classify.py",
    "study/measurement_validity/make_training_sample.py",
    "study/measurement_validity/training_sample.csv",
    "study/measurement_validity/freeze.py",
    "study/measurement_validity/sample.csv",
    "study/measurement_validity/exposure.csv",
    "results/nmf_v2/document_weights_k6.csv",
]
RESULT_FILES = ["coding/coder_A_completed.xlsx", "coding/coder_B_completed.xlsx", "outputs/agreement.csv",
                "outputs/llm_predictions.csv", "outputs/method_metrics.csv",
                "coding/train_A_completed.xlsx", "coding/train_B_completed.xlsx",
                "outputs/bert_predictions_eaton_theuer.csv", "outputs/bert_predictions_own.csv",
                "outputs/tfidf_predictions_eaton_theuer.csv", "outputs/tfidf_predictions_own.csv"]


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
    """Return True if every frozen file matches protocol_lock.json."""
    if not LOCK.exists():
        print("WARNING: protocol_lock.json does not exist; the design has not been frozen.")
        return False
    lock = json.loads(LOCK.read_text())
    changed = [p for p, h in lock["files"].items() if not (ROOT / p).exists() or sha(p) != h]
    if (ROOT / "data/processed/person_corpus_exploratory_v1.csv").exists() and \
            sample_text_hash() != lock["sample_text_sha256"]:
        changed.append("sampled statement texts")
    if changed:
        print("WARNING: changed since the design was frozen:", ", ".join(changed))
        return False
    print(f"Design version {lock.get('version', '1.0')} unchanged since {lock['frozen_at_utc']}.")
    return True


def write_lock(version, reason):
    lock = {"version": version,
            "frozen_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
            "reason": reason,
            "files": {p: sha(p) for p in FROZEN},
            "sample_text_sha256": sample_text_hash()}
    LOCK.write_text(json.dumps(lock, indent=2) + "\n")
    print(f"Version {version} frozen at {lock['frozen_at_utc']}. Commit the lock file(s) before coding starts.")


def freeze():
    if LOCK.exists():
        raise SystemExit("protocol_lock.json already exists. Use --new-version to amend the design.")
    codebook = (HERE / "CODEBOOK.md").read_text()
    if "_To be filled in before freezing._" in codebook:
        raise SystemExit("Fill in 'Differences from Eaton & Theuer' in CODEBOOK.md first.")
    write_lock("1.0", "initial design")


def amend(version, reason):
    if not LOCK.exists():
        raise SystemExit("Nothing to amend; run freeze.py first.")
    existing = [f for f in RESULT_FILES if (HERE / f).exists()]
    if existing:
        raise SystemExit(f"Coding or results already exist ({', '.join(existing)}); record a deviation instead.")
    if f"### Version {version}" not in (HERE / "PROTOCOL.md").read_text():
        raise SystemExit(f"Add a '### Version {version}' entry under Amendments in PROTOCOL.md first.")
    old = json.loads(LOCK.read_text())
    archived = HERE / f"protocol_lock_v{old.get('version', '1.0')}.json"
    archived.write_text(LOCK.read_text())
    print(f"Previous lock kept as {archived.name}.")
    write_lock(version, reason)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--new-version")
    parser.add_argument("--reason", default="")
    args = parser.parse_args()
    if args.check:
        raise SystemExit(0 if check() else 1)
    if args.new_version:
        if not args.reason:
            raise SystemExit("--reason is required with --new-version")
        amend(args.new_version, args.reason)
    else:
        freeze()
