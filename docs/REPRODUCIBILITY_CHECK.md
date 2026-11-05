# Reproducibility evidence and scope

The original project owner reported executing a fresh clone and curated data
snapshot in a separate virtual environment. The submitted rerun notebook was
inspected; its execution counts were 1 through 6, with no stored errors and
three PNG outputs. That original artifact is not committed here, so it must
not be described as an independently accessible execution artifact.

A [machine-generated inspection record](evidence/notebook_inspection_v1.json)
records the supplied notebook hash and observable output counts. This is
inspection of a user-supplied artifact, not execution by this audit process.
The repository's historical main notebook is a different artifact and contains
older outputs, including local paths.

The [follow-up audit](FOLLOWUP_AUDIT.md) documents actual script executions,
versions, input hashes, regenerated numerical references and separate new
result directories. The supplementary notebook has no saved outputs; its
independent execution remains to be completed. Neither notebook reproduction
nor downstream model reproduction establishes source collection accuracy.
Raw HTML and upstream extraction decisions are not included in the release.
