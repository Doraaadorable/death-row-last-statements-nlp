"""Download unique statement pages with caching and a progress manifest."""

import hashlib
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data/raw"
HTML = RAW / "html"
HTML.mkdir(parents=True, exist_ok=True)

MANIFEST = RAW / "download_manifest.json"
inventory = pd.read_csv(ROOT / "data/processed/execution_inventory.csv")
urls = inventory["statement_url"].dropna().drop_duplicates().tolist()

manifest = (
    json.loads(MANIFEST.read_text(encoding="utf-8"))
    if MANIFEST.exists() else {}
)

session = requests.Session()
session.headers["User-Agent"] = (
    "LastStatementsResearch/0.1 (academic portfolio project)"
)


def save_manifest():
    temporary = MANIFEST.with_suffix(".tmp")
    temporary.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    temporary.replace(MANIFEST)


# Check that distinct URLs will not overwrite the same local filename.
filenames = [Path(urlparse(url).path).name for url in urls]
if len(filenames) != len(set(filenames)):
    raise RuntimeError("Filename collision detected; inspect URLs first.")

try:
    for i, url in enumerate(urls, start=1):
        parsed = urlparse(url)
        if parsed.scheme != "https" or parsed.hostname != "www.tdcj.texas.gov":
            raise RuntimeError(f"Unexpected source URL: {url}")

        destination = HTML / Path(parsed.path).name
        previous = manifest.get(url, {})
        entry = {
            "source_url": url,
            "html_file": str(destination.relative_to(ROOT)),
            "checked_at_utc": datetime.now(timezone.utc).isoformat(),
            "downloaded_at_utc": previous.get("downloaded_at_utc"),
            "status": "error",
            "error": None,
        }
        stop = False

        try:
            if destination.exists() and destination.stat().st_size > 0:
                content = destination.read_bytes()
                entry["status"] = "cached"
            else:
                time.sleep(2)
                response = session.get(url, timeout=30)
                entry["http_status"] = response.status_code
                entry["final_url"] = response.url
                stop = response.status_code in (403, 429)
                response.raise_for_status()

                if "html" not in response.headers.get(
                    "Content-Type", ""
                ).lower():
                    raise ValueError("Expected an HTML response")

                content = response.content
                if not content:
                    raise ValueError("Empty response")

                temporary = destination.with_suffix(".html.tmp")
                temporary.write_bytes(content)
                temporary.replace(destination)

                entry["status"] = "downloaded"
                entry["downloaded_at_utc"] = (
                    datetime.now(timezone.utc).isoformat()
                )

            entry["bytes"] = len(content)
            entry["sha256"] = hashlib.sha256(content).hexdigest()

        except (requests.RequestException, ValueError) as exc:
            entry["error"] = str(exc)

        manifest[url] = entry
        save_manifest()

        print(
            f"[{i}/{len(urls)}] {destination.name}: {entry['status']}",
            flush=True,
        )
        if entry["error"]:
            print("  Reason:", entry["error"], flush=True)

        if stop:
            print("HTTP 403/429 detected. Stopped; progress saved.")
            break

except KeyboardInterrupt:
    print("\nInterrupted. Progress saved; rerun to continue.")

finally:
    save_manifest()
    statuses = pd.Series([
        manifest.get(url, {}).get("status", "not_attempted")
        for url in urls
    ])
    print("\nDownload summary:")
    print(statuses.value_counts().to_string())
    print("\nManifest:", MANIFEST)
