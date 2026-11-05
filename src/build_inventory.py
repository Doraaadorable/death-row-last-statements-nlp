"""Build a complete execution inventory from the cached TDCJ index."""

import re
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin

import pandas as pd
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
INDEX_URL = "https://www.tdcj.texas.gov/death_row/executed_inmates.html"
OUT = ROOT / "data/processed"
OUT.mkdir(parents=True, exist_ok=True)

soup = BeautifulSoup(
    (ROOT / "data/raw/executed_inmates.html").read_bytes(),
    "html.parser",
)

records = []

for row in soup.select("tr"):
    cells = row.find_all("td")
    if not cells:
        continue

    values = [" ".join(cell.stripped_strings) for cell in cells]

    # Execution rows begin with a numeric execution number.
    if not re.fullmatch(r"\d+", values[0]):
        continue

    dates = [
        value for value in values
        if re.fullmatch(r"\d{1,2}/\d{1,2}/\d{4}", value)
    ]

    index_date = None
    if len(dates) == 1:
        try:
            index_date = datetime.strptime(
                dates[0], "%m/%d/%Y"
            ).date().isoformat()
        except ValueError:
            pass

    statement_links = list(dict.fromkeys(
        urljoin(INDEX_URL, a["href"])
        for a in row.find_all("a", href=True)
        if (
            re.sub(r"\s+", "", a.get_text()).casefold() == "laststatement"
            or re.search(
                r"/(?:[^/]+last|no_last_statement)\.html$",
                urljoin(INDEX_URL, a["href"]),
                re.IGNORECASE,
            )
        )
    ))

    records.append({
        "execution_number": int(values[0]),
        "index_date": index_date,
        "statement_url": (
            statement_links[0] if len(statement_links) == 1 else None
        ),
        "statement_link_count": len(statement_links),
        "row_status": (
            "ok"
            if index_date and len(statement_links) <= 1
            else "needs_review"
        ),
        "index_row_text": " | ".join(values),
        "index_source_url": INDEX_URL,
    })

if not records:
    raise RuntimeError("No execution rows identified; inspect index structure")

df = pd.DataFrame(records)

if df["execution_number"].duplicated().any():
    raise RuntimeError("Duplicate execution numbers; inspect before continuing")

output = OUT / "execution_inventory.csv"
df.to_csv(output, index=False, encoding="utf-8-sig")

print("Total execution records:", len(df))
print("Records with one statement link:",
      int((df["statement_link_count"] == 1).sum()))
print("Records without a statement link:",
      int((df["statement_link_count"] == 0).sum()))
print("Records needing review:",
      int((df["row_status"] == "needs_review").sum()))
print("Earliest index date:", df["index_date"].dropna().min())
print("Latest index date:", df["index_date"].dropna().max())
print("Saved:", output)
