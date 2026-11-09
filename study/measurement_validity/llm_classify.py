"""Run the frozen LLM classifier on the study sample.

Needs the data-v1 snapshot and Anthropic API credentials (ANTHROPIC_API_KEY or an
`ant auth login` profile). Run after both coders have finished:
    python study/measurement_validity/llm_classify.py

Writes outputs/llm_predictions.csv with one row per item and run. Re-running skips
rows that already exist, so an interrupted run can be resumed.
"""
import json
import sys
import time
from pathlib import Path

import anthropic
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import methods  # noqa: E402

ROOT = HERE.parents[1]
OUT = HERE / "outputs" / "llm_predictions.csv"


def classify(client, text):
    # Server-side fallback: if the model declines, the API re-runs the request on a
    # fallback model. The served model is recorded so such items can be reported.
    response = client.beta.messages.create(
        model=methods.LLM_MODEL,
        max_tokens=2000,
        betas=["server-side-fallback-2026-07-01"],
        fallbacks="default",
        system=methods.LLM_SYSTEM,
        output_config={
            "effort": methods.LLM_EFFORT,
            "format": {"type": "json_schema", "schema": methods.LLM_SCHEMA},
        },
        messages=[{"role": "user", "content": methods.LLM_INSTRUCTIONS.format(text=text)}],
    )
    row = {"served_model": response.model, "stop_reason": response.stop_reason,
           "input_tokens": response.usage.input_tokens, "output_tokens": response.usage.output_tokens,
           "request_id": response._request_id}
    if response.stop_reason == "refusal":
        row.update(apology="refused", innocence="refused")
        return row
    text_block = next(b.text for b in response.content if b.type == "text")
    row.update(json.loads(text_block))
    return row


def main():
    sample = pd.read_csv(HERE / "sample.csv")
    corpus = pd.read_csv(ROOT / "data/processed/person_corpus_exploratory_v1.csv", keep_default_na=False)
    texts = sample.merge(corpus[["execution_number", "candidate_text"]], on="execution_number")
    assert len(texts) == len(sample)

    done = pd.read_csv(OUT) if OUT.exists() else pd.DataFrame(columns=["run", "item_id"])
    finished = set(zip(done["run"], done["item_id"]))
    OUT.parent.mkdir(exist_ok=True)

    client = anthropic.Anthropic()
    rows = []
    for run in range(1, methods.LLM_REPEATS + 1):
        for item in texts.itertuples():
            if (run, item.item_id) in finished:
                continue
            for attempt in range(3):
                try:
                    result = classify(client, item.candidate_text)
                    break
                except (anthropic.APIConnectionError, anthropic.RateLimitError, anthropic.InternalServerError):
                    if attempt == 2:
                        raise
                    time.sleep(10 * (attempt + 1))
            rows.append({"run": run, "item_id": item.item_id, **result})
            if len(rows) % 25 == 0:
                print(f"run {run}: {len(rows)} new rows", flush=True)
                pd.concat([done, pd.DataFrame(rows)]).to_csv(OUT, index=False)
    final = pd.concat([done, pd.DataFrame(rows)]).sort_values(["run", "item_id"])
    final.to_csv(OUT, index=False)
    print(f"Saved {len(final)} rows to {OUT}")
    print(final.groupby("run")[["input_tokens", "output_tokens"]].sum())


if __name__ == "__main__":
    main()
