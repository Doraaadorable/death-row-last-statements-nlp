"""Create a reproducible, decade-balanced development sample."""

from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/processed"
DEST = OUT / "annotation_development_v1.csv"

# Protect any annotations already entered.
if DEST.exists():
    raise SystemExit(
        "Annotation file already exists. It was not overwritten."
    )

df = pd.read_csv(
    OUT / "person_corpus_exploratory_v1.csv",
    keep_default_na=False,
)

samples = []

for decade, group in df.groupby("decade", sort=True):
    chosen = (
        group.sort_values("execution_number")
        .sample(n=min(10, len(group)), random_state=42)
    )
    samples.append(chosen)

sample = pd.concat(samples, ignore_index=True).sort_values(
    ["decade", "execution_number"]
)

labels = [
    "relational_affection",
    "gratitude",
    "faith_spirituality",
    "apology_forgiveness",
    "harm_acknowledgment",
    "innocence_dispute",
    "justice_criticism",
    "farewell_readiness",
]

sample["sample_role"] = "annotation_guideline_development"

for label in labels:
    sample[label] = ""

sample["evidence_notes"] = ""
sample["other_theme_notes"] = ""
sample["text_quality_notes"] = ""
sample["annotation_status"] = "pending"

sample.to_csv(DEST, index=False, encoding="utf-8-sig")

print("Development sample by decade:")
print(sample.groupby("decade").size().to_string())
print("\nTotal:", len(sample))
print("Saved:", DEST)

print("\nFirst 5 records for discussion:")
for _, row in sample.head(5).iterrows():
    print("\nExecution:", row["execution_number"])
    print("Modes:", row["recorded_modes"])
    print(row["candidate_text"])
