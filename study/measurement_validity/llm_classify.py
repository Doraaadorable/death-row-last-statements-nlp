"""Run the frozen LLM classifier on the study sample.

Needs the data-v1 snapshot and Anthropic API credentials (ANTHROPIC_API_KEY or an
`ant auth login` profile). Run after both coders have finished:
    python study/measurement_validity/llm_classify.py

Writes outputs/llm_predictions.csv with one row per item and run. Every request is
recorded, including refusals, technical failures and invalid output, so coverage can
be reported. Re-running skips rows that already exist, so an interrupted run resumes.

Protocol v1.1: one model only (no server-side fallback), so results describe that model.
"""
import argparse
import json
import sys
import time
from pathlib import Path

import anthropic
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import freeze  # noqa: E402
import methods  # noqa: E402

ROOT = HERE.parents[1]
OUT = HERE / "outputs" / "llm_predictions.csv"
RETRYABLE = (anthropic.APIConnectionError, anthropic.RateLimitError, anthropic.InternalServerError)


def classify(client, text):
    """Return one row describing the outcome of a single request."""
    response = client.messages.create(
        model=methods.LLM_MODEL,
        max_tokens=2000,
        system=methods.LLM_SYSTEM,
        output_config={
            "effort": methods.LLM_EFFORT,
            "format": {"type": "json_schema", "schema": methods.LLM_SCHEMA},
        },
        messages=[{"role": "user", "content": methods.LLM_INSTRUCTIONS.format(text=text)}],
    )
    row = {"served_model": response.model, "stop_reason": response.stop_reason,
           "input_tokens": response.usage.input_tokens, "output_tokens": response.usage.output_tokens,
           "request_id": response._request_id, "error": ""}
    if response.stop_reason == "refusal":
        category = getattr(response.stop_details, "category", None) if response.stop_details else None
        return {**row, "status": "refused", "apology": "refused", "innocence": "refused",
                "error": f"refusal category: {category}"}
    try:
        text_block = next(b.text for b in response.content if b.type == "text")
        answer = json.loads(text_block)
        assert set(answer) == set(methods.CONSTRUCTS)
        assert all(v in methods.LLM_VALUE for v in answer.values())
    except (StopIteration, json.JSONDecodeError, AssertionError) as exc:
        return {**row, "status": "invalid", "apology": "invalid", "innocence": "invalid",
                "error": f"{type(exc).__name__}: stop_reason={response.stop_reason}"}
    return {**row, "status": "ok", **answer}


def classify_with_retries(client, text, attempts=3):
    for attempt in range(attempts):
        try:
            return classify(client, text)
        except RETRYABLE as exc:
            if attempt == attempts - 1:
                return {"status": "failed", "apology": "failed", "innocence": "failed",
                        "error": f"{type(exc).__name__}: {exc}"[:300]}
            time.sleep(10 * (attempt + 1))
        except anthropic.APIStatusError as exc:  # not retryable (for example 400)
            return {"status": "failed", "apology": "failed", "innocence": "failed",
                    "error": f"{type(exc).__name__} {exc.status_code}: {exc.message}"[:300]}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--allow-unfrozen", action="store_true",
                        help="run even if the design differs from protocol_lock.json (for testing only)")
    args = parser.parse_args()
    if not freeze.check() and not args.allow_unfrozen:
        raise SystemExit("Stopped: the design does not match protocol_lock.json.")

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
            rows.append({"run": run, "item_id": item.item_id, **classify_with_retries(client, item.candidate_text)})
            if len(rows) % 25 == 0:
                print(f"run {run}: {len(rows)} new rows", flush=True)
                pd.concat([done, pd.DataFrame(rows)]).to_csv(OUT, index=False)
    final = pd.concat([done, pd.DataFrame(rows)]).sort_values(["run", "item_id"])
    final.to_csv(OUT, index=False)
    print(f"Saved {len(final)} rows to {OUT}")
    print(final.groupby(["run", "status"]).size().unstack(fill_value=0))


if __name__ == "__main__":
    main()
