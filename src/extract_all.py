"""Extract statement candidates and create a reviewable execution dataset."""

import re
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

import pandas as pd
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/processed"
inventory = pd.read_csv(OUT / "execution_inventory.csv")

# Only exact, observed wording is classified automatically.
NO_STATEMENT_NOTICES = {
    "no last statement provided.",
}

rows = []

for item in inventory.to_dict("records"):
    url = item["statement_url"]
    filename = Path(urlparse(url).path).name
    html_path = ROOT / "data/raw/html" / filename

    record = {
        "execution_number": item["execution_number"],
        "index_date": item["index_date"],
        "statement_page_date": None,
        "date_check": "not_checked",
        "source_url": url,
        "html_file": str(html_path.relative_to(ROOT)),
        "content_status": "needs_review",
        "statement_section_raw": None,
        "statement_text_candidate": None,
        "word_count": None,
        "has_media_heading": False,
        "has_spoken_heading": False,
        "has_written_heading": False,
        "has_spanish_marker": False,
        "has_possible_editorial_note": False,
        "manual_review_status": "pending",
        "error": None,
    }

    try:
        soup = BeautifulSoup(html_path.read_bytes(), "html.parser")
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()

        lines = [
            " ".join(line.split())
            for line in soup.get_text("\n").splitlines()
            if line.strip()
        ]
        page_text = " ".join(lines)

        # Shared pages must never become personal statement text.
        if filename == "no_last_statement.html":
            record["content_status"] = "shared_notice_link"
            record["date_check"] = "not_applicable"
            rows.append(record)
            continue

        date_match = re.search(
            r"Date of Execution:\s*([A-Za-z]+\s+\d{1,2},\s+\d{4})",
            page_text,
            flags=re.IGNORECASE,
        )
        if date_match:
            try:
                date = datetime.strptime(
                    date_match.group(1), "%B %d, %Y"
                ).date().isoformat()
                record["statement_page_date"] = date
                record["date_check"] = (
                    "match" if date == item["index_date"] else "conflict"
                )
            except ValueError:
                record["date_check"] = "unparsed"
        else:
            record["date_check"] = "missing_on_statement_page"

        starts = [
            i for i, line in enumerate(lines)
            if line.casefold() == "last statement:"
        ]
        if len(starts) != 1:
            raise ValueError("Expected one exact Last Statement marker")

        start = starts[0] + 1
        end = next(
            (
                i for i in range(start, len(lines))
                if lines[i].casefold() == "compact with texans"
            ),
            None,
        )
        if end is None:
            raise ValueError("Footer boundary missing")

        section = "\n".join(lines[start:end]).strip()
        if not section:
            raise ValueError("Empty statement section")

        text = " ".join(section.split())
        record["statement_section_raw"] = section

        if text.casefold() in NO_STATEMENT_NOTICES:
            record["content_status"] = "no_statement_reported"
        else:
            record["content_status"] = "statement_candidate"
            record["statement_text_candidate"] = text
            record["word_count"] = len(text.split())

        # These are review flags, not confirmed annotations.
        record["has_media_heading"] = bool(
            re.search(r"statement to the media\s*:", text, re.I)
        )
        record["has_spoken_heading"] = bool(
            re.search(r"\bspoken\s*:", text, re.I)
        )
        record["has_written_heading"] = bool(
            re.search(r"\bwritten(?: statement)?\s*:", text, re.I)
        )
        record["has_spanish_marker"] = bool(
            re.search(r"\(spanish\)", text, re.I)
        )
        record["has_possible_editorial_note"] = bool(
            re.search(
                r"when asked|he replied|she replied|"
                r"then he|then she|\(pause\)",
                text,
                re.I,
            )
        )

    except (OSError, ValueError) as exc:
        record["error"] = str(exc)

    rows.append(record)

df = pd.DataFrame(rows)
df["word_count"] = df["word_count"].astype("Int64")

if len(df) != len(inventory):
    raise RuntimeError("Output row count does not match inventory")
if df["execution_number"].duplicated().any():
    raise RuntimeError("Duplicate execution numbers")

df.to_csv(
    OUT / "statements_extracted.csv",
    index=False,
    encoding="utf-8-sig",
)

flags = [
    "has_media_heading", "has_spoken_heading",
    "has_written_heading", "has_spanish_marker",
    "has_possible_editorial_note",
]

review_mask = (
    df["content_status"].eq("needs_review")
    | df["date_check"].isin(
        ["conflict", "unparsed", "missing_on_statement_page"]
    )
    | df[flags].any(axis=1)
    | (
        df["content_status"].eq("statement_candidate")
        & df["word_count"].lt(10).fillna(False)
    )
)

df.loc[review_mask].to_csv(
    OUT / "priority_review_queue.csv",
    index=False,
    encoding="utf-8-sig",
)

print("\nContent status:")
print(df["content_status"].value_counts().to_string())

print("\nDate checks:")
print(df["date_check"].value_counts().to_string())

print("\nReview flags (may overlap):")
print(df[flags].sum().to_string())

print("\nPriority review records:", int(review_mask.sum()))
print("Total execution records:", len(df))

errors = df.loc[
    df["error"].notna(),
    ["execution_number", "source_url", "error"],
]
if not errors.empty:
    print("\nExtraction errors:")
    print(errors.to_string(index=False))

print("\nSaved: data/processed/statements_extracted.csv")
print("Saved: data/processed/priority_review_queue.csv")
