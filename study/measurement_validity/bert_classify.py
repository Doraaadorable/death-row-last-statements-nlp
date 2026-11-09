"""Supervised method (protocol version 1.3): fine-tuned BERT, one binary classifier per construct.

Trains on human-coded statements outside the study sample and predicts the 150 sample items.
Run on a GPU (Colab) after both coders have finished the study sample:

    python study/measurement_validity/bert_classify.py --labels own
    python study/measurement_validity/bert_classify.py --labels eaton_theuer

Training labels:
  own            coding/train_A_completed.xlsx (coder A, frozen codebook, items in training_sample.csv)
  eaton_theuer   coding/eaton_theuer_labels.csv (execution_number, apology, innocence as 1/0/u),
                 converted from Eaton & Theuer's codes; statements in the study sample are dropped

Writes outputs/bert_predictions_<labels>.csv (item_id, construct, training_size, seed, prob)
and outputs/bert_run_<labels>.json (model revision, library versions, training counts).
"""
import argparse
import json
import random
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import methods  # noqa: E402

ROOT = HERE.parents[1]
CODING = HERE / "coding"
OUTPUTS = HERE / "outputs"
CORPUS = ROOT / "data/processed/person_corpus_exploratory_v1.csv"

MODEL = "google-bert/bert-base-uncased"
MAX_TOKENS = 512           # including [CLS] and [SEP]
HEAD_TOKENS = 128          # longer statements keep the first 128 and the last 382 tokens
LEARNING_RATE = 2e-5
EPOCHS = 4
BATCH_SIZE = 16
WEIGHT_DECAY = 0.01
WARMUP_FRACTION = 0.1
SEEDS = (1, 2, 3, 4, 5)
CURVE_FRACTIONS = (0.25, 0.5)   # learning curve: nested random subsets, plus the full set
CURVE_SEED = 20261111


# ---------------------------------------------------------------- data

def texts_by_execution():
    corpus = pd.read_csv(CORPUS, keep_default_na=False)
    return corpus.set_index("execution_number").candidate_text


def training_labels(source):
    """Training statements with labels as strings 1/0/u, indexed by execution_number."""
    sample = set(pd.read_csv(HERE / "sample.csv").execution_number)
    if source == "own":
        sheet = pd.read_excel(CODING / "train_A_completed.xlsx", sheet_name="coding", dtype=str)
        sheet = sheet.merge(pd.read_csv(HERE / "training_sample.csv", dtype={"item_id": str}), on="item_id")
        labels = sheet.set_index("execution_number")[list(methods.CONSTRUCTS)]
        dropped = labels.index.isin(sample).sum()
        if dropped:
            raise SystemExit(f"{dropped} training statements are in the study sample.")
    else:
        labels = pd.read_csv(CODING / "eaton_theuer_labels.csv", dtype=str)
        labels["execution_number"] = labels.execution_number.astype(int)
        labels = labels.set_index("execution_number")[list(methods.CONSTRUCTS)]
        dropped = int(labels.index.isin(sample).sum())
        labels = labels[~labels.index.isin(sample)]
    labels = labels.fillna("").apply(lambda c: c.str.strip().str.lower().replace({"1.0": "1", "0.0": "0"}))
    bad = set(labels.stack()) - {"1", "0", "u"}
    if bad:
        raise SystemExit(f"Training labels must be 1, 0 or u; found {sorted(bad)}")
    return labels, int(dropped)


def curve_subsets(index, fractions=CURVE_FRACTIONS, seed=CURVE_SEED):
    """Nested random subsets of the training statements: each smaller set lies inside the larger."""
    order = np.random.default_rng(seed).permutation(np.asarray(index))
    sizes = sorted({max(1, int(round(f * len(order)))) for f in fractions} | {len(order)})
    return {n: set(order[:n]) for n in sizes}


# ---------------------------------------------------------------- model

def encode(tokenizer, text):
    """Token ids with [CLS]/[SEP]; long statements keep their beginning and end."""
    ids = tokenizer(text, add_special_tokens=False)["input_ids"]
    room = MAX_TOKENS - 2
    if len(ids) > room:
        ids = ids[:HEAD_TOKENS] + ids[-(room - HEAD_TOKENS):]
    return [tokenizer.cls_token_id, *ids, tokenizer.sep_token_id]


def batches(encoded, labels, size, generator=None):
    import torch
    order = torch.randperm(len(encoded), generator=generator) if generator is not None else torch.arange(len(encoded))
    for start in range(0, len(encoded), size):
        idx = order[start:start + size].tolist()
        width = max(len(encoded[i]) for i in idx)
        ids = torch.zeros(len(idx), width, dtype=torch.long)
        mask = torch.zeros(len(idx), width, dtype=torch.long)
        for row, i in enumerate(idx):
            ids[row, :len(encoded[i])] = torch.tensor(encoded[i])
            mask[row, :len(encoded[i])] = 1
        yield ids, mask, (torch.tensor([labels[i] for i in idx]) if labels is not None else None)


def train_and_predict(model_name, train_texts, train_y, test_texts, seed, device):
    """Fine-tune one classifier and return the positive-class probability for each test text."""
    import torch
    from transformers import AutoModelForSequenceClassification, AutoTokenizer, get_linear_schedule_with_warmup

    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2).to(device)

    train_enc = [encode(tokenizer, t) for t in train_texts]
    test_enc = [encode(tokenizer, t) for t in test_texts]
    y = [int(v) for v in train_y]
    positives = sum(y)
    if positives == 0 or positives == len(y):
        raise ValueError("training labels contain a single class")
    # Weight the positive class by the negative/positive ratio, so rare constructs are not ignored.
    weight = torch.tensor([1.0, (len(y) - positives) / positives], device=device)
    loss_fn = torch.nn.CrossEntropyLoss(weight=weight)

    no_decay = ("bias", "LayerNorm.weight")
    groups = [
        {"params": [p for n, p in model.named_parameters() if not n.endswith(no_decay)], "weight_decay": WEIGHT_DECAY},
        {"params": [p for n, p in model.named_parameters() if n.endswith(no_decay)], "weight_decay": 0.0},
    ]
    optimizer = torch.optim.AdamW(groups, lr=LEARNING_RATE)
    steps = EPOCHS * -(-len(y) // BATCH_SIZE)
    scheduler = get_linear_schedule_with_warmup(optimizer, int(WARMUP_FRACTION * steps), steps)
    generator = torch.Generator().manual_seed(seed)

    model.train()
    for _ in range(EPOCHS):
        for ids, mask, labels in batches(train_enc, y, BATCH_SIZE, generator):
            ids, mask, labels = ids.to(device), mask.to(device), labels.to(device)
            with torch.autocast(device_type=device, dtype=torch.float16, enabled=device == "cuda"):
                logits = model(input_ids=ids, attention_mask=mask).logits
            loss = loss_fn(logits.float(), labels)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()
            scheduler.step()
            optimizer.zero_grad()

    model.eval()
    probs = []
    with torch.no_grad():
        for ids, mask, _ in batches(test_enc, None, BATCH_SIZE * 2):
            logits = model(input_ids=ids.to(device), attention_mask=mask.to(device)).logits.float()
            probs.extend(torch.softmax(logits, dim=-1)[:, 1].cpu().tolist())
    revision = getattr(model.config, "_commit_hash", None)
    return probs, revision


# ---------------------------------------------------------------- run

def run(source, model_name=MODEL, seeds=SEEDS):
    import torch
    import transformers

    missing = [f for f in ("coder_A_completed.xlsx", "coder_B_completed.xlsx") if not (CODING / f).exists()]
    if missing:
        raise SystemExit(f"Automated methods run only after both coders finish; missing {missing}.")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    texts = texts_by_execution()
    sample = pd.read_csv(HERE / "sample.csv")
    test_texts = sample.execution_number.map(texts).tolist()
    labels, dropped = training_labels(source)

    rows, counts, revision = [], {}, None
    for construct in methods.CONSTRUCTS:
        coded = labels[construct][labels[construct] != "u"]
        counts[construct] = {"statements": int(len(coded)), "positives": int((coded == "1").sum()),
                             "excluded_u": int((labels[construct] == "u").sum())}
        subsets = curve_subsets(coded.index) if source == "own" else {len(coded): set(coded.index)}
        for size, members in subsets.items():
            subset = coded[coded.index.isin(members)]
            for seed in seeds:
                probs, revision = train_and_predict(model_name, subset.index.map(texts).tolist(),
                                                    subset.tolist(), test_texts, seed, device)
                rows += [{"item_id": i, "construct": construct, "training_size": size, "seed": seed, "prob": p}
                         for i, p in zip(sample.item_id, probs)]
                print(f"{construct}: trained on {size} statements, seed {seed}")

    OUTPUTS.mkdir(exist_ok=True)
    pd.DataFrame(rows).to_csv(OUTPUTS / f"bert_predictions_{source}.csv", index=False)
    meta = {"labels": source, "model": model_name, "model_revision": revision, "device": device,
            "gpu": torch.cuda.get_device_name(0) if device == "cuda" else None,
            "torch": torch.__version__, "transformers": transformers.__version__,
            "training": counts, "dropped_study_sample_statements": dropped,
            "settings": {"max_tokens": MAX_TOKENS, "head_tokens": HEAD_TOKENS, "learning_rate": LEARNING_RATE,
                         "epochs": EPOCHS, "batch_size": BATCH_SIZE, "weight_decay": WEIGHT_DECAY,
                         "warmup_fraction": WARMUP_FRACTION, "seeds": list(seeds)}}
    (OUTPUTS / f"bert_run_{source}.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(json.dumps(meta["training"], indent=2))


if __name__ == "__main__":
    import freeze
    parser = argparse.ArgumentParser()
    parser.add_argument("--labels", choices=["own", "eaton_theuer"], required=True)
    parser.add_argument("--allow-unfrozen", action="store_true",
                        help="run even if the design differs from protocol_lock.json (for testing only)")
    args = parser.parse_args()
    if not freeze.check() and not args.allow_unfrozen:
        raise SystemExit("Stopped: the design does not match protocol_lock.json.")
    run(args.labels)
