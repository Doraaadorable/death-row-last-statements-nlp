"""Conservative cleaning: preserve source text and label known notices."""

import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/processed"

# Preserve literal strings such as "N/A", "None", and "NA".
df = pd.read_csv(
    OUT / "statements_extracted.csv",
    keep_default_na=False,
)

def normalize(text):
    return re.sub(r"\s+", " ", text).strip()

def key(text):
    return normalize(text).casefold().rstrip(".")

notices = {
    key(text) for text in [
        "No last statement provided.",
        "No last statement given.",
        "No statement was made.",
        "No statement given.",
        "No last statement.",
        "This inmate declined to make a last statement.",
    ]
}

# Observed recorder summaries or references, not verbatim statements.
summary_records = {
    387: "Recorder summary of profanity",
    241: "Recorder reports an Irish utterance and its translation",
    50: "Poem title/reference; full recited text not supplied here",
    48: "Recorder summary of thanks",
}

df["cleaning_status"] = df["content_status"]
df["cleaning_note"] = ""
df["analysis_text_v1"] = ""

for i, row in df.iterrows():
    if row["content_status"] != "statement_candidate":
        continue

    text = normalize(row["statement_section_raw"])
    number = int(row["execution_number"])

    if key(text) in notices:
        df.at[i, "cleaning_status"] = "no_statement_reported"

    elif number in summary_records:
        df.at[i, "cleaning_status"] = "summary_or_reference"
        df.at[i, "cleaning_note"] = summary_records[number]

    elif key(text) in {"", "no", "none", "n/a", "na", "nan", "null"}:
        df.at[i, "cleaning_status"] = "ambiguous_short_response"
        df.at[i, "cleaning_note"] = (
            "Inspect source context before classifying"
        )

    else:
        df.at[i, "cleaning_status"] = "text_candidate"
        df.at[i, "analysis_text_v1"] = text

df.to_csv(
    OUT / "statements_clean_v1.csv",
    index=False,
    encoding="utf-8-sig",
)

print("\nCleaning status:")
print(df["cleaning_status"].value_counts().to_string())

print("\nAmbiguous short responses:")
ambiguous = df[
    df["cleaning_status"].eq("ambiguous_short_response")
]
for _, row in ambiguous.iterrows():
    print(
        row["execution_number"],
        repr(row["statement_section_raw"]),
        row["source_url"],
    )

print("\nKnown short refusal responses retained for now:")
for number in [475, 15]:
    rows = df[df["execution_number"].eq(number)]
    for _, row in rows.iterrows():
        print(number, repr(row["statement_section_raw"]))

print("\nDate conflicts:")
conflicts = df[df["date_check"].eq("conflict")].copy()
conflicts["same_year"] = (
    conflicts["index_date"].str[:4]
    == conflicts["statement_page_date"].str[:4]
)
print(conflicts[[
    "execution_number", "index_date",
    "statement_page_date", "same_year"
]].to_string(index=False))

print("\nSaved: data/processed/statements_clean_v1.csv")
