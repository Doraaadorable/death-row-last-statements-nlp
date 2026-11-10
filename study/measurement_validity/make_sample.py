"""Draw the study sample and write blind coding sheets.

Run once from the repository root after extracting the data-v1 snapshot:
    python study/measurement_validity/make_sample.py

Outputs (in study/measurement_validity/):
  sample.csv                  item_id -> execution_number (coders should not open it)
  coding/coder_A.xlsx         150 items, coder A's random order
  coding/coder_B.xlsx         same items, a different random order
  coding/practice.xlsx        10 practice items from the development sample (not evaluated)
"""
from pathlib import Path

import numpy as np
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font
from openpyxl.worksheet.datavalidation import DataValidation

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
CORPUS = ROOT / "data/processed/person_corpus_exploratory_v1.csv"
DEVELOPMENT = ROOT / "data/processed/annotation_development_v2.csv"

SEED = 20261109
N_ITEMS = 150
N_PRACTICE = 10


def write_sheet(path, rows, title):
    wb = Workbook()
    ws = wb.active
    ws.title = "coding"
    headers = ["item_id", "text", "apology", "condolence", "innocence", "innocence_type", "note"]
    ws.append(headers)
    for cell in ws[1]:
        cell.font = Font(bold=True)
    for item_id, text in rows:
        ws.append([item_id, text, None, None, None, None, None])
    validation = DataValidation(type="list", formula1='"1,0,u"', allow_blank=True,
                                showErrorMessage=True, error="Use 1, 0 or u")
    ws.add_data_validation(validation)
    validation.add(f"C2:E{len(rows) + 1}")
    type_validation = DataValidation(type="list", formula1='"F,L"', allow_blank=True,
                                     showErrorMessage=True, error="Use F (factual) or L (legal), only when innocence is 1")
    ws.add_data_validation(type_validation)
    type_validation.add(f"F2:F{len(rows) + 1}")
    widths = {"A": 10, "B": 100, "C": 10, "D": 12, "E": 11, "F": 15, "G": 40}
    for col, width in widths.items():
        ws.column_dimensions[col].width = width
    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = Alignment(wrap_text=True, vertical="top")
    ws.freeze_panes = "C2"
    info = wb.create_sheet("read_me")
    info.append([title])
    info.append(["Code each statement with the codebook (study/measurement_validity/CODEBOOK.md)."])
    info.append(["Use 1, 0 or u in the apology, condolence and innocence columns. When innocence is 1, choose F (factual) or L (legal) in innocence_type."])
    info.append(["Read the English text; look up single words if needed, but do not use machine translation."])
    info.append(["Do not discuss items with the other coder until both sheets are finished."])
    path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(path)


def main():
    corpus = pd.read_csv(CORPUS, keep_default_na=False)
    development = set(pd.read_csv(DEVELOPMENT).execution_number)
    pool = corpus[~corpus.execution_number.isin(development)].sort_values("execution_number")
    assert len(pool) == 430, len(pool)

    rng = np.random.default_rng(SEED)
    chosen = pool.iloc[np.sort(rng.choice(len(pool), size=N_ITEMS, replace=False))]
    ids = [f"S{i:03d}" for i in rng.permutation(np.arange(1, N_ITEMS + 1))]
    sample = pd.DataFrame({"item_id": ids, "execution_number": chosen.execution_number.to_numpy(),
                           "text": chosen.candidate_text.to_numpy()}).sort_values("item_id")
    sample[["item_id", "execution_number"]].to_csv(HERE / "sample.csv", index=False)

    for coder in ("A", "B"):
        order = sample.iloc[rng.permutation(len(sample))]
        write_sheet(HERE / f"coding/coder_{coder}.xlsx", list(zip(order.item_id, order.text)),
                    f"Coder {coder}: measurement study, {N_ITEMS} statements")

    dev = corpus[corpus.execution_number.isin(development)].sort_values("execution_number")
    practice = dev.iloc[np.sort(rng.choice(len(dev), size=N_PRACTICE, replace=False))]
    write_sheet(HERE / "coding/practice.xlsx",
                [(f"P{i:02d}", t) for i, t in enumerate(practice.candidate_text, 1)],
                "Practice items (development sample; discuss together, not evaluated)")
    pd.DataFrame({"item_id": [f"P{i:02d}" for i in range(1, N_PRACTICE + 1)],
                  "execution_number": practice.execution_number.to_numpy()}).to_csv(
        HERE / "coding/practice_key.csv", index=False)

    print(f"Sample: {len(sample)} statements from a pool of {len(pool)} "
          f"(development sample excluded); median {int(chosen.word_count.median())} words.")


if __name__ == "__main__":
    main()
