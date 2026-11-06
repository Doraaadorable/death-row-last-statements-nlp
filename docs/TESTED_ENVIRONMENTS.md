# Tested environments and code provenance

## Evidence levels

| Evidence | Python | NumPy | pandas | SciPy | scikit-learn |
|---|---|---|---|---|---|
| Original v2 manifest | 3.13.9 | 2.5.4 | 3.1.0 | Not recorded in that manifest | 1.9.1 |
| Executed follow-up and metadata-repair diagnostics | 3.12.14 | 2.3.5 | 2.2.3 | 1.17.0 | 1.8.0 |
| Reviewer-reported updated-package rerun | 3.12.3 | 2.5.4 | 3.0.6 | 1.18.1 | 1.9.1 |

The first row records historical generation metadata, not a new execution.
The second row is recorded by the executed diagnostic scripts and follow-up
manifest. The third row comes from the reviewer report supplied by the owner;
it has not been independently repeated in that exact environment here.
The reviewer reported all three notebooks executing and numerical agreement
around 1e-15. Their temporary environment and original execution log are not
bundled. These observations do not guarantee arbitrary-version portability
and do not constitute a complete dependency lock.

## Metadata repair
The previously published stability manifest recorded the following
normalization source hash:

`7a75986fc5d341054306cfd199f30babfaf7ad0d092479693b3b937c9fcacb43`

The corresponding source bytes were not preserved in the package. This is an
unresolved historical provenance gap; no current source hash is substituted
as evidence of what originally generated those results.

All three diagnostics were rerun in a temporary copy after adding consistent
execution metadata. Each new manifest/method file records the actual script,
shared feature module and provenance helper hashes, timestamp and numerical
library versions. A Git HEAD is recorded only if available in the execution
copy. Source-byte hashes remain authoritative even when there is no .git folder
or the working tree differs from its last commit. Shared feature logic and
model fitting are unchanged; incidental source whitespace is included in hashes.

The rerun metadata replaces metadata for the diagnostic rerun, not the
historical v2 NMF reference. The published matched-topic CSVs are retained
unchanged. The [verification record](../reports/release_audit_verification.json)
compares 90 initialization matches and 14 matches in each removal experiment
against their published counterparts; maximum numeric difference was zero.
Every recorded source hash was checked against the exact bytes prepared for
this commit.

## Reproducible checks
Run from the repository root:

```bash
python -m unittest discover -s tests -v
```

The three tests cover exact versus near-equal columns, deterministic group
cutoff ordering and overlap invariance to within-group weight swaps. They do
not constitute a complete model-validation suite. Full numerical references
are checked by the three diagnostic scripts using the curated Release inputs.

## Scope still open
- Broad cross-k component interpretation has not been completed.
- Original raw HTML is not in the Release.
- The historical v1-to-v2 annotation revision log is incomplete.
- The follow-up manifest's protocol commit and reference-provenance sentence
  are declared descriptive metadata, not runtime verification of Git history.
- Historical v1 topic output is not bundled. The v1/v2 normalization comparison
  requires rerunning the supplied model scripts in a separate copy.
- Ranked term exports still use historical argsort conventions; tied term
  order is not used for numerical reference validation. Group-set overlap is
  used only where explicitly named.
