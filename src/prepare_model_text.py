"""Prepare exploratory modeling text without modifying source or labels."""

import hashlib
import json
import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/processed/person_corpus_exploratory_v1.csv"
OUT = ROOT / "data/processed"

df = pd.read_csv(SOURCE, keep_default_na=False)
assert df["execution_number"].is_unique

brackets = re.compile(r"\(([^()]*)\)|\[([^\[\]]*)\]")

# Reviewed substantive additions: retain their content.
keep_content = {
    "sanders", "have", "by", "god", "niv",
    "my honor is my life",
}

# Reviewed explanatory glosses: do not count alongside the original words.
remove_gloss = {
    "dad",
    "spanish - god, i command my spirit to go with you.",
    "spanish - we all praise god.",
    "take care of my family.",
    "vietnamese for let's get out of here.",
}

# Stage directions, transcription notes, headings, and source annotations.
editorial = re.compile(
    r"^(?:"
    r"he called the names|mouthed|a couple of sentences garbled|"
    r"first two or three words|i gave warden|names of children|"
    r"there were some unintelligible|some words about allah|"
    r"couldn.t understand|some more allah mumbling|"
    r"not sure of name|formely known as|formerly known as|"
    r"name unknown|statement amended|several names listed|"
    r"inmate stopped speaking|"
    r"remaining portion of statement omitted|"
    r"portion of statement omitted|"
    r"expletive deleted|"
    r"mumbled|mumbles|mumbling|more mumbling|"
    r"garbled|unintelligible|illegible|unknown tongues|"
    r"cough|pauses?|crying|"
    r"quiet singing|singing|began singing|sings\b|"
    r"recites the lord.s prayer|"
    r"talked to family|end of statement|"
    r"written statement|spoken statement|"
    r"speaking in french|in spanish|spanish|english"
    r")",
    re.IGNORECASE,
)

logs = []
prepared = []

for _, row in df.iterrows():
    number = int(row["execution_number"])
    original = row["candidate_text"]
    unresolved = []
    text = original

    def log(before, after, action):
        logs.append({
            "execution_number": number,
            "action": action,
            "source_span": before,
            "replacement": after,
        })

    if number == 82:
        # Entire entry is an indirect transcription summary.
        text = ""
        log(original, "", "exclude_indirect_summary")
        status = "excluded_indirect_summary"

    else:
        if number == 425:
            note = (
                "(After the official last statement ended, "
                "he said I love you Mom.)"
            )
            if text.count(note) != 1:
                raise ValueError("Execution 425 source differs; inspect first")
            text = text.replace(note, "I love you Mom.")
            log(
                note, "I love you Mom.",
                "retain_reported_words_remove_editorial_wrapper",
            )

        # Reviewed multilingual entry: execution 192.
        if number == 192:
            prefix, separator, translation = text.partition("(Translation:")
            if not separator or " German:" not in prefix:
                raise ValueError("Execution 192 source differs; inspect first")

            english_sections, german = prefix.split(" German:", 1)
            english_sections = re.sub(
                r"\b(?:English|Spanish):\s*", "", english_sections
            )
            replacement = (
                english_sections.strip() + " " + translation.strip()
            )
            log(
                text, replacement,
                "use_supplied_english_translation_for_german_section",
            )
            text = replacement

        def replace(match):
            content = (
                match.group(1)
                if match.group(1) is not None
                else match.group(2)
            ).strip()

            key = content.casefold()

            if key in keep_content:
                log(match.group(0), content, "retain_content_unwrap")
                return content

            if key in remove_gloss or editorial.search(content):
                log(match.group(0), "", "remove_editorial_or_gloss")
                # A sentence boundary prevents artificial phrase joining.
                return " . "

            # Preserve unknown content and keep the record out of modeling.
            unresolved.append(match.group(0))
            log(match.group(0), match.group(0), "unresolved_keep_for_review")
            return match.group(0)

        text = brackets.sub(replace, text)
        text = " ".join(text.split())

        # Catch nested/unmatched brackets not handled by the simple pattern.
        if re.search(r"[\[\]()]", text) and not unresolved:
            unresolved.append("Residual bracket characters")

        status = (
            "pending_editorial_review"
            if unresolved else "ready_for_exploration"
        )

    prepared.append({
        "execution_number": number,
        "index_date": row["index_date"],
        "source_url": row["source_url"],
        "model_text": text,
        "model_word_count": len(text.split()),
        "preparation_status": status,
        "unresolved_spans": json.dumps(unresolved, ensure_ascii=False),
    })

result = pd.DataFrame(prepared)

assert len(result) == len(df)
assert result["execution_number"].is_unique
assert result.loc[
    result["preparation_status"].eq("ready_for_exploration"),
    "model_text",
].str.strip().ne("").all()

result.to_csv(
    OUT / "model_corpus_v1.csv",
    index=False, encoding="utf-8-sig",
)

pd.DataFrame(
    logs,
    columns=["execution_number", "action", "source_span", "replacement"],
).to_csv(
    OUT / "model_text_changes_v1.csv",
    index=False, encoding="utf-8-sig",
)

manifest = {
    "source_file": SOURCE.name,
    "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
    "status_counts": result["preparation_status"].value_counts().to_dict(),
    "note": (
        "Exploratory derivative. Source and frozen labels unchanged. "
        "Ready status does not certify all speaker attribution or translation."
    ),
}
(OUT / "model_text_manifest_v1.json").write_text(
    json.dumps(manifest, indent=2) + "\n",
    encoding="utf-8",
)

print("\nPreparation status:")
print(result["preparation_status"].value_counts().to_string())

pending = result[
    result["preparation_status"].eq("pending_editorial_review")
]
print("\nUnresolved records:")
if pending.empty:
    print("None")
else:
    print(
        pending[["execution_number", "unresolved_spans"]]
        .to_string(index=False)
    )

print("\nSpecial records:")
for number in [49, 82, 425]:
    row = result.loc[result["execution_number"].eq(number)].iloc[0]
    print(f"\nExecution {number}: {row['preparation_status']}")
    print(row["model_text"] or "(Excluded from first topic model)")

print("\nSaved model corpus, change log, and source manifest.")
print("Source corpus and annotation files were not modified.")
