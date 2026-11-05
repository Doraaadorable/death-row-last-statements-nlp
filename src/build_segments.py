"""Split explicitly labelled sections while preserving source offsets."""

import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/processed"

df = pd.read_csv(
    OUT / "statements_clean_v1.csv",
    keep_default_na=False,
)

# Match headings only at the start of a line.
heading = re.compile(
    r"^[ \t]*(?P<label>"
    r"Chaplain Brazzil recites written statement|"
    r"Last Verbal Statement|"
    r"Statement to the Media|"
    r"Spoken(?: Statement)?|"
    r"Verbal(?: Statement)?|"
    r"Written(?: Statement)?"
    r")[ \t]*:",
    flags=re.IGNORECASE | re.MULTILINE,
)

segments = []
split_records = []

for _, row in df.iterrows():
    if row["cleaning_status"] != "text_candidate":
        continue

    number = int(row["execution_number"])
    source = row["statement_section_raw"]
    matches = list(heading.finditer(source))
    parts = []

    # Preserve any text before the first heading instead of dropping it.
    if not matches:
        parts.append(("unspecified", "", 0, len(source)))
    else:
        if source[:matches[0].start()].strip():
            parts.append(("unspecified", "", 0, matches[0].start()))

        for i, match in enumerate(matches):
            end = (
                matches[i + 1].start()
                if i + 1 < len(matches) else len(source)
            )
            label = match.group("label")
            lower = label.casefold()

            if lower.startswith("chaplain"):
                mode = "written_read_by_chaplain"
            elif lower.startswith("written"):
                mode = "written"
            elif lower.startswith("statement to the media"):
                mode = "media_statement"
            else:
                mode = "spoken"

            parts.append((mode, label, match.end(), end))

    if matches:
        split_records.append({
            "execution_number": number,
            "segment_count": len(parts),
            "modes": " | ".join(p[0] for p in parts),
        })

    for order, (mode, label, start, end) in enumerate(parts, start=1):
        raw_text = source[start:end]
        text = " ".join(raw_text.split())

        status = "text_candidate"
        if not text:
            status = "empty_needs_review"
        elif text.casefold().rstrip(".") in {"no", "none", "n/a"}:
            status = "ambiguous_short_response"

        segments.append({
            "segment_id": f"execution_{number}_segment_{order}",
            "execution_number": number,
            "segment_order": order,
            "index_date": row["index_date"],
            "source_url": row["source_url"],
            "statement_mode": mode,
            "source_heading": label,
            "source_char_start": start,
            "source_char_end": end,
            "segment_text_raw": raw_text,
            "segment_text": text,
            "word_count": len(text.split()),
            "segment_status": status,
            "boundary_review_status": (
                "rule_based_pending_verification"
                if matches else "no_explicit_heading"
            ),
        })

result = pd.DataFrame(segments)

if result["segment_id"].duplicated().any():
    raise RuntimeError("Duplicate segment IDs")

expected_people = int(df["cleaning_status"].eq("text_candidate").sum())
if result["execution_number"].nunique() != expected_people:
    raise RuntimeError("A candidate execution was lost during splitting")

result.to_csv(
    OUT / "statement_segments_v1.csv",
    index=False,
    encoding="utf-8-sig",
)

print("\nSegment modes:")
print(result["statement_mode"].value_counts().to_string())

print("\nSegment status:")
print(result["segment_status"].value_counts().to_string())

print("\nExplicitly labelled records:")
print(pd.DataFrame(split_records).to_string(index=False))

print("\nExecution 211 boundary check:")
for _, row in result[result["execution_number"].eq(211)].iterrows():
    print(
        row["segment_id"],
        "|", row["statement_mode"],
        "|", row["word_count"], "words",
    )
    print("Start:", row["segment_text"][:100])
    print("End:  ", row["segment_text"][-100:])

print("\nPeople represented:", result["execution_number"].nunique())
print("Total segments:", len(result))
print("Saved: data/processed/statement_segments_v1.csv")
