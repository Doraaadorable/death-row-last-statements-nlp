"""Flag sampled statements that earlier project work had already touched (protocol v1.1).

    python study/measurement_validity/build_exposure.py

Writes exposure.csv: one row per sampled item with
  project_exposure  1 if the statement appears in any earlier project record
  coder_a_excerpts  1 if Coder A confirmed decisions on excerpts of it (earlier claim review)
  sources           which records mention it
Statements with no record are "no documented exposure", which is not proof of being unseen.
"""
import json
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def exposure_sources():
    sources = {}

    def add(ids, name):
        for i in ids:
            sources.setdefault(int(i), set()).add(name)

    ledger = json.loads((ROOT / "reports/evaluation_exposure_readiness_v1.json").read_text())
    for name, ids in ledger["source_ids"].items():
        add(ids, f"ledger:{name}")
    smoke = json.loads((ROOT / "reports/sampled_focus_smoke_v1.json").read_text())

    def walk(obj, key=""):
        if isinstance(obj, dict):
            for k, v in obj.items():
                walk(v, k)
        elif isinstance(obj, list):
            for v in obj:
                walk(v, key)
        elif isinstance(obj, int) and "execution" in key.lower():
            add([obj], "smoke_test_sample")

    walk(smoke)
    for version in ("v1", "v2"):
        method = json.loads((ROOT / f"results/prayer_sensitivity_{version}/method.json").read_text())
        walk_ids = []

        def collect(obj, key=""):
            if isinstance(obj, dict):
                for k, v in obj.items():
                    collect(v, k)
            elif isinstance(obj, list):
                for v in obj:
                    collect(v, key)
            elif isinstance(obj, int) and "execution" in key.lower():
                walk_ids.append(obj)

        collect(method)
        add(walk_ids, "prayer_sensitivity_selection")
    owner = set()
    for f in ("semantic_owner_decisions_v3_discussion.csv", "semantic_pilot_decisions_v1.csv"):
        df = pd.read_csv(ROOT / "reports" / f)
        owner |= set(df.execution_number)
    return sources, owner


def main():
    sample = pd.read_csv(HERE / "sample.csv")
    sources, owner = exposure_sources()
    rows = []
    for item in sample.itertuples():
        s = sorted(sources.get(item.execution_number, set()))
        rows.append({"item_id": item.item_id, "execution_number": item.execution_number,
                     "project_exposure": int(bool(s)),
                     "coder_a_excerpts": int(item.execution_number in owner),
                     "sources": ";".join(s)})
    out = pd.DataFrame(rows)
    out.to_csv(HERE / "exposure.csv", index=False)
    print(f"{out.project_exposure.sum()} of {len(out)} items have documented project exposure; "
          f"{out.coder_a_excerpts.sum()} have Coder A decisions on excerpts.")


if __name__ == "__main__":
    main()
