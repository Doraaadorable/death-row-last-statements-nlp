"""Collect a small sample of TDCJ last-statement pages for inspection."""

import json
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
HTML = RAW / "html"
HTML.mkdir(parents=True, exist_ok=True)

INDEX_URL = "https://www.tdcj.texas.gov/death_row/executed_inmates.html"
SAMPLE_SIZE = 10

session = requests.Session()
session.headers.update({
    "User-Agent": "LastStatementsResearch/0.1 (academic portfolio pilot)"
})


def fetch(url, destination):
    """Reuse local HTML when available to avoid repeated requests."""
    if destination.exists():
        return destination.read_bytes(), "cache"

    time.sleep(2)
    response = session.get(url, timeout=30)
    response.raise_for_status()

    if "html" not in response.headers.get("Content-Type", "").lower():
        raise ValueError("Expected an HTML page")

    destination.write_bytes(response.content)
    return response.content, "network"


def extract_statement(html):
    """Extract a candidate statement between explicit page markers."""
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    lines = [
        " ".join(line.split())
        for line in soup.get_text("\n").splitlines()
        if line.strip()
    ]

    starts = [
        i for i, line in enumerate(lines)
        if line.casefold() == "last statement:"
    ]

    if len(starts) != 1:
        raise ValueError("Could not identify one exact statement marker")

    start = starts[0] + 1
    end = next(
        (
            i for i in range(start, len(lines))
            if lines[i].casefold() == "compact with texans"
        ),
        None,
    )

    if end is None:
        raise ValueError("Footer boundary missing; manual inspection needed")

    text = "\n".join(lines[start:end]).strip()
    if not text:
        raise ValueError("Empty statement section; manual inspection needed")

    return text


index_html, _ = fetch(INDEX_URL, RAW / "executed_inmates.html")
soup = BeautifulSoup(index_html, "html.parser")

links = list(dict.fromkeys(
    urljoin(INDEX_URL, a["href"])
    for a in soup.find_all("a", href=True)
    if " ".join(a.stripped_strings).casefold() == "last statement"
))

if not links:
    raise RuntimeError("No statement links found; inspect the saved index")

records = []

for number, url in enumerate(links[:SAMPLE_SIZE], start=1):
    filename = Path(urlparse(url).path).name
    destination = HTML / filename

    record = {
        "source_url": url,
        "html_file": str(destination.relative_to(ROOT)),
        "processed_at_utc": datetime.now(timezone.utc).isoformat(),
        "statement_text": None,
        "extraction_status": "error",
        "manual_review_status": "pending",
        "error": None,
    }

    try:
        html, source = fetch(url, destination)
        record["html_source"] = source
        record["statement_text"] = extract_statement(html)
        record["extraction_status"] = "candidate_extracted"
    except (requests.RequestException, ValueError) as exc:
        record["error"] = str(exc)

    records.append(record)

    print(f"\n[{number}/{SAMPLE_SIZE}] {filename}")
    print("Status:", record["extraction_status"])
    print("Preview:", (record["statement_text"] or record["error"])[:180])

output = RAW / "sample_statements.json"
output.write_text(
    json.dumps(records, ensure_ascii=False, indent=2),
    encoding="utf-8",
)

extracted = sum(
    r["extraction_status"] == "candidate_extracted" for r in records
)

print(f"\nCandidate extractions: {extracted}/{len(records)}")
print("Manual review: pending for every record")
print("Saved to:", output)
