"""Describe the provisional corpus at the execution-record level."""

from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/processed"
REPORTS = ROOT / "reports"
REPORTS.mkdir(parents=True, exist_ok=True)

executions = pd.read_csv(
    OUT / "statements_clean_v1.csv",
    keep_default_na=False,
)
segments = pd.read_csv(
    OUT / "statement_segments_v1.csv",
    keep_default_na=False,
)

# Exclude ambiguous segments, including King's spoken "No."
usable = segments[
    segments["segment_status"].eq("text_candidate")
].sort_values(["execution_number", "segment_order"])

# One document per person; preserve segment order.
people = (
    usable.groupby("execution_number", as_index=False)
    .agg(
        candidate_text=("segment_text", lambda x: "\n\n".join(x)),
        candidate_segment_count=("segment_id", "size"),
        recorded_modes=(
            "statement_mode",
            lambda x: " | ".join(dict.fromkeys(x)),
        ),
    )
)

people = people.merge(
    executions[["execution_number", "index_date", "source_url"]],
    on="execution_number",
    how="left",
    validate="one_to_one",
)

people["word_count"] = people["candidate_text"].str.split().str.len()
people["year"] = pd.to_datetime(
    people["index_date"], format="%Y-%m-%d", errors="raise"
).dt.year
people["decade"] = (people["year"] // 10) * 10

# Index dates define exploratory year groups; conflicts remain unresolved.
executions["year"] = pd.to_datetime(
    executions["index_date"], format="%Y-%m-%d", errors="raise"
).dt.year
executions["decade"] = (executions["year"] // 10) * 10

coverage = (
    executions.groupby("decade")
    .size()
    .rename("execution_records")
    .to_frame()
    .join(
        people.groupby("decade").size().rename("candidate_people")
    )
    .fillna(0)
)

coverage["candidate_people"] = coverage["candidate_people"].astype(int)
coverage["candidate_coverage_pct"] = (
    100 * coverage["candidate_people"] / coverage["execution_records"]
).round(1)

# Compare normalized text, without changing the saved candidate text.
people["comparison_key"] = (
    people["candidate_text"]
    .str.replace(r"\s+", " ", regex=True)
    .str.strip()
    .str.casefold()
)

duplicates = people[
    people["comparison_key"].duplicated(keep=False)
].sort_values("comparison_key")

people.drop(columns="comparison_key").to_csv(
    OUT / "person_corpus_exploratory_v1.csv",
    index=False,
    encoding="utf-8-sig",
)
coverage.to_csv(REPORTS / "coverage_by_decade_v1.csv")
duplicates.drop(columns="comparison_key").to_csv(
    OUT / "duplicate_text_review.csv",
    index=False,
    encoding="utf-8-sig",
)

print("\nCORPUS SIZE")
print("People:", len(people))
print("Included segments:", len(usable))

print("\nWORDS PER PERSON")
print(
    people["word_count"]
    .describe(percentiles=[0.25, 0.5, 0.75, 0.9, 0.95])
    .round(1)
    .to_string()
)

print("\nCOVERAGE BY DECADE — PROVISIONAL")
print(coverage.to_string())

print("\nSHORTEST DOCUMENTS")
print(people.nsmallest(10, "word_count")[[
    "execution_number", "word_count", "candidate_text"
]].to_string(index=False))

print("\nDUPLICATE NORMALIZED TEXT")
print("People in duplicate groups:", len(duplicates))
if not duplicates.empty:
    print(duplicates[[
        "execution_number", "word_count", "candidate_text"
    ]].to_string(index=False))

print("\nSaved exploratory corpus, coverage table, and duplicate review.")
