"""Audit pilot dates and test statement extraction across decades."""

import json
import random
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse

import pandas as pd
import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data/raw"
OUT = ROOT / "data/processed"
HTML = RAW / "html"
OUT.mkdir(parents=True, exist_ok=True)
HTML.mkdir(parents=True, exist_ok=True)

INDEX_URL = "https://www.tdcj.texas.gov/death_row/executed_inmates.html"

soup = BeautifulSoup(
    (RAW / "executed_inmates.html").read_bytes(), "html.parser"
)

# Build a link inventory with dates from the index page.
inventory = {}

for row in soup.select("tr"):
    links = [
        a for a in row.find_all("a", href=True)
        if " ".join(a.stripped_strings).casefold() == "last statement"
    ]
    if not links:
        continue

    dates = [
        " ".join(cell.stripped_strings)
        for cell in row.find_all(["td", "th"])
        if re.fullmatch(
            r"\d{1,2}/\d{1,2}/\d{4}",
            " ".join(cell.stripped_strings),
        )
    ]

    index_date = None
    if len(dates) == 1:
        index_date = datetime.strptime(
            dates[0], "%m/%d/%Y"
        ).date().isoformat()

    for a in links:
        url = urljoin(INDEX_URL, a["href"])
        inventory[url] = {
            "record_id": Path(urlparse(url).path).stem,
            "source_url": url,
            "index_date": index_date,
        }

# Preserve both date sources in a separate pilot audit.
pilot = pd.read_csv(OUT / "sample_prepared.csv")
pilot = pilot.rename(columns={"execution_date": "statement_page_date"})
pilot["index_date"] = pilot["source_url"].map(
    {url: item["index_date"] for url, item in inventory.items()}
)

def date_check(row):
    if pd.isna(row["index_date"]) or pd.isna(row["statement_page_date"]):
        return "missing"
    return (
        "match"
        if row["index_date"] == row["statement_page_date"]
        else "conflict"
    )

pilot["date_check"] = pilot.apply(date_check, axis=1)
pilot.to_csv(
    OUT / "sample_date_audit.csv", index=False, encoding="utf-8-sig"
)

# Select up to three previously untested pages per decade.
pilot_urls = set(pilot["source_url"])
groups = {}

for item in inventory.values():
    if item["index_date"] and item["source_url"] not in pilot_urls:
        decade = (int(item["index_date"][:4]) // 10) * 10
        groups.setdefault(decade, []).append(item)

rng = random.Random(42)
selected = []

for decade, items in sorted(groups.items()):
    sample = rng.sample(
        sorted(items, key=lambda x: x["source_url"]),
        min(3, len(items)),
    )
    selected.extend(dict(item, decade=decade) for item in sample)

session = requests.Session()
session.headers["User-Agent"] = (
    "LastStatementsResearch/0.1 (academic portfolio pilot)"
)

def extract(html):
    page = BeautifulSoup(html, "html.parser")
    for tag in page(["script", "style", "noscript"]):
        tag.decompose()

    lines = [
        " ".join(line.split())
        for line in page.get_text("\n").splitlines()
        if line.strip()
    ]

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

    text = "\n".join(lines[start:end]).strip()
    if not text:
        raise ValueError("Empty statement section")

    return text

results = []

for item in selected:
    result = dict(
        item,
        processed_at_utc=datetime.now(timezone.utc).isoformat(),
        extraction_status="error",
        manual_review_status="pending",
        statement_text=None,
        error=None,
    )

    destination = HTML / f"{item['record_id']}.html"
    result["html_file"] = str(destination.relative_to(ROOT))

    try:
        if destination.exists():
            html = destination.read_bytes()
            result["html_source"] = "cache"
        else:
            time.sleep(2)
            response = session.get(item["source_url"], timeout=30)
            response.raise_for_status()

            if "html" not in response.headers.get(
                "Content-Type", ""
            ).lower():
                raise ValueError("Expected HTML")

            html = response.content
            destination.write_bytes(html)
            result["html_source"] = "network"

        result["statement_text"] = extract(html)
        result["extraction_status"] = "candidate_extracted"

    except (requests.RequestException, ValueError) as exc:
        result["error"] = str(exc)

    results.append(result)
    print(
        f"{item['decade']}s | {item['record_id']} | "
        f"{result['extraction_status']}"
    )
    if result["error"]:
        print("  Reason:", result["error"])

    # Stop further requests if the server refuses access or rate-limits.
    if result["error"] and "response" in locals():
        if response.status_code in (403, 429):
            print("Access restriction detected; stopping this run.")
            break

output = RAW / "historical_sample.json"
output.write_text(
    json.dumps(results, ensure_ascii=False, indent=2),
    encoding="utf-8",
)

print("\nHistorical sample summary:")
if results:
    print(pd.crosstab(
        pd.Series([r["decade"] for r in results], name="decade"),
        pd.Series(
            [r["extraction_status"] for r in results],
            name="status",
        ),
    ).to_string())

print("\nIndex links without a parsed date:",
      sum(x["index_date"] is None for x in inventory.values()))
print("Saved:", OUT / "sample_date_audit.csv")
print("Saved:", output)
