"""Write the training sheet for the supervised (BERT) method, protocol version 1.3.

Run once from the repository root:
    python study/measurement_validity/make_training_sample.py

The training set is every statement outside the study sample and the development sample
(280 statements), split at random into 140 for each coder. Each coder codes their half alone
with the frozen codebook after adjudication of the study sample. No training statement is in
the study sample.

Outputs (in study/measurement_validity/):
  training_sample.csv         item_id -> execution_number, coder
  coding/train_A.xlsx         coder A's 140 items in random order
  coding/train_B.xlsx         coder B's 140 items in random order
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
    half = N_ITEMS // 2
    training = pd.DataFrame({"item_id": [f"T{i:03d}" for i in range(1, N_ITEMS + 1)],
                             "execution_number": order.execution_number.to_numpy(),
                             "coder": ["A"] * half + ["B"] * half,
                             "text": order.candidate_text.to_numpy()})
    training[["item_id", "execution_number", "coder"]].to_csv(HERE / "training_sample.csv", index=False)
    for coder, items in training.groupby("coder"):
        write_sheet(HERE / f"coding/train_{coder}.xlsx", list(zip(items.item_id, items.text)),
                    f"Coder {coder}: training set for the supervised method, {len(items)} statements")
    print(f"Training set: {N_ITEMS} statements, {half} per coder; median {int(pool.word_count.median())} words.")


if __name__ == "__main__":
    main()
