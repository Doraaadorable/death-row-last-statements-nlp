"""Prepare the pilot dataset and preserve a separate review record."""

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data/raw"
OUT = ROOT / "data/processed"
OUT.mkdir(parents=True, exist_ok=True)

records = json.loads(
    (RAW / "sample_statements.json").read_text(encoding="utf-8")
)

# Only these ten records were compared with user-supplied source text.
REVIEWED = {
    "howardjamaallast", "rameykerseanlast", "normanlejameslast",
    "busbyedwardlast", "broadnaxjameslast", "rickscedriclast",
    "thompsoncharleslast", "milamblainelast",
    "johnsonmatthewlast", "mendozamoiseslast",
}

rows = []
reviews = []

for record in records:
    record_id = Path(record["html_file"]).stem
    text = " ".join((record.get("statement_text") or "").split())
    extraction_ok = record["extraction_status"] == "candidate_extracted"

    if not extraction_ok or not text:
        content_status = "unclear"
    elif text.casefold() == "no last statement provided.":
        content_status = "no_statement_reported"
    else:
        content_status = "statement_present"

    analysis_text = text if content_status == "statement_present" else None

    # Parse metadata from saved HTML; no new network requests.
    html_path = ROOT / record["html_file"]
    execution_date = None

    if html_path.exists():
        soup = BeautifulSoup(html_path.read_bytes(), "html.parser")
        page_text = " ".join(soup.stripped_strings)
        match = re.search(
            r"Date of Execution:\s*([A-Za-z]+\s+\d{1,2},\s+\d{4})",
            page_text,
            re.IGNORECASE,
        )
        if match:
            try:
                execution_date = datetime.strptime(
                    match.group(1), "%B %d, %Y"
                ).date().isoformat()
            except ValueError:
                pass

    review_status = (
        "matches_user_supplied_source_ignoring_whitespace"
        if record_id in REVIEWED and extraction_ok
        else "pending"
    )

    rows.append({
        "record_id": record_id,
        "source_url": record["source_url"],
        "execution_date": execution_date,
        "content_status": content_status,
        "statement_mode": (
            "not_applicable"
            if content_status == "no_statement_reported"
            else "unspecified"
        ),
        "has_spanish_marker": "(spanish)" in text.casefold(),
        "statement_text": analysis_text,
        "word_count": len(analysis_text.split()) if analysis_text else None,
        "source_comparison_status": review_status,
        "date_verification_status": "pending",
    })

    reviews.append({
        "record_id": record_id,
        "source_url": record["source_url"],
        "normalized_text_sha256": hashlib.sha256(
            text.encode("utf-8")
        ).hexdigest(),
        "review_status": review_status,
        "review_basis": "User-copied webpage text compared in conversation",
    })

df = pd.DataFrame(rows)
df["word_count"] = df["word_count"].astype("Int64")
df.to_csv(OUT / "sample_prepared.csv", index=False, encoding="utf-8-sig")

# Keep a timestamped audit record so later runs do not overwrite this review.
stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
review_path = OUT / f"sample_review_{stamp}.json"
review_path.write_text(
    json.dumps(reviews, ensure_ascii=False, indent=2),
    encoding="utf-8",
)

print("\nContent status:")
print(df["content_status"].value_counts().to_string())

print("\nDates and approximate word counts:")
print(df[[
    "record_id", "execution_date", "word_count"
]].to_string(index=False))

print("\nMissing dates:", int(df["execution_date"].isna().sum()))
print("Saved:", OUT / "sample_prepared.csv")
print("Saved:", review_path)
