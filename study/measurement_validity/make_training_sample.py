"""Write the training sheet for the supervised (BERT) method, protocol version 1.3.

Run once from the repository root:
    python study/measurement_validity/make_training_sample.py

The training set is every statement outside the study sample and the development sample
(280 statements). Coder A codes them with the frozen codebook after adjudication of the
study sample. No training statement is in the study sample.

Outputs (in study/measurement_validity/):
  training_sample.csv         item_id -> execution_number
  coding/train_A.xlsx         280 items in random order
"""
from pathlib import Path

import numpy as np
import pandas as pd

from make_sample import CORPUS, DEVELOPMENT, write_sheet

HERE = Path(__file__).resolve().parent
SEED = 20261111
N_ITEMS = 280


def main():
    corpus = pd.read_csv(CORPUS, keep_default_na=False)
    excluded = set(pd.read_csv(DEVELOPMENT).execution_number) | set(pd.read_csv(HERE / "sample.csv").execution_number)
    pool = corpus[~corpus.execution_number.isin(excluded)].sort_values("execution_number")
    assert len(pool) == N_ITEMS, len(pool)

    rng = np.random.default_rng(SEED)
    order = pool.iloc[rng.permutation(len(pool))]
    ids = [f"T{i:03d}" for i in range(1, N_ITEMS + 1)]
    pd.DataFrame({"item_id": ids, "execution_number": order.execution_number.to_numpy()}).to_csv(
        HERE / "training_sample.csv", index=False)
    write_sheet(HERE / "coding/train_A.xlsx", list(zip(ids, order.candidate_text)),
                f"Coder A: training set for the supervised method, {N_ITEMS} statements")
    print(f"Training set: {N_ITEMS} statements; median {int(pool.word_count.median())} words.")


if __name__ == "__main__":
    main()
