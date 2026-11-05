# Notebook reproducibility check

Verification recorded: 5 November 2026.

## Scope

This check reruns the presentation notebook using a fresh Git clone, the public data-v1 Release attachment, and a separate virtual environment. It verifies consumption of the curated inputs and published model outputs. It does not refit NMF or reconstruct the upstream website collection and extraction.

## Evidence

- The user downloaded data_snapshot_v1.zip from the public Release and verified SHA-256 c56a4be1915cdaefd5ea1878da47d009f0cb9de8082401f7de241d42a7266168.
- The separate environment's `python -m pip check` reported no broken requirements.
- The submitted rerun notebook reports a Python executable inside the fresh clone's `.venv/bin/python` and a project root ending in `death-row-repro-check`, rather than the original working project.
- All six code cells have consecutive execution counts 1–6, no saved error outputs, and three embedded PNG figures.
- The notebook's model-corpus SHA-256 check passed against the published NMF manifest; the displayed vocabulary contains 3,196 features.
- The output contains 479 ready-for-exploration records and one excluded indirect summary. The analysis overview distinguishes the 603-record inventory, 480-person candidate corpus, 477 fitted documents and 50-person development sample.
- Source cells are English-only and contain no temporary Git-management commands.

The notebook was executed by the project owner and its saved sources and outputs were inspected with AI assistance. This is not an independent third-party replication or a controlled dependency-lock test. The later notebook file is retained as verification evidence, not substituted for the main analysis notebook.

## Outcome and limits

**Passed: fresh-clone notebook execution from the published curated snapshot and saved model results.**

This check does not validate psychological interpretations, annotation agreement, model generalization or exact reproducibility of every fitting result across software versions. Dependencies are not locked. Full model refitting and robustness reruns are separate commands documented in the [README](../README.md#reproduction).

Data access: [Data snapshot v1](https://github.com/Doraaadorable/death-row-last-statements-nlp/releases/tag/data-v1).
