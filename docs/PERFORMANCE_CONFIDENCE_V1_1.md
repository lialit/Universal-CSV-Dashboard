# v1.1 Performance Confidence

This document records GH-08C for Issue #16 — performance confidence for medium and large CSV workloads.

## Existing optimization baseline

The current application already avoids repeated full-dataframe recomputation in the main analytical flow:

- derived results are cached per Streamlit session;
- cache identity follows the in-memory dataset object rather than hashing or copying the full dataframe;
- changing the loaded dataset starts a fresh cache;
- Executive Overview reuses expensive derived payloads and avoids a full-size filtered copy when controls still represent the complete dataset;
- browser-side distribution charts use a deterministic labelled sample for large datasets while calculations continue to use the full data.

These behaviours are already covered by automated tests and remain the performance architecture for v1.1.

## Repeatable profile suite

GH-08C adds `scripts/performance_suite.py`, which generates deterministic temporary CSV fixtures and measures the core analysis path for three profiles:

| Profile | Target size | Purpose |
| --- | ---: | --- |
| small | 1 MB | normal quick analysis |
| medium | 10 MB | realistic heavier workflow |
| large | 24 MB | near the supported 25 MB upload boundary |

Run:

```powershell
python scripts/performance_suite.py
```

To store a machine-readable baseline:

```powershell
python scripts/performance_suite.py --json-output performance_baseline.json
```

The report records file size, dataframe shape, CSV parsing time, field-detection time, Data Quality time, total core-analysis time, detected field roles and quality result.

Elapsed seconds are comparison evidence for a documented environment, not a universal SLA.

## Manual revisit check

The CLI suite measures deterministic core analysis. Before v1.1 release, also verify Streamlit page reuse manually:

1. run `python -m streamlit run app.py`;
2. load a representative synthetic large CSV;
3. visit Executive Overview, Business Insights, Analysis Assistant and Data Quality once;
4. revisit the same pages without changing dataset or configuration;
5. confirm revisits do not trigger avoidable full recomputation;
6. load a different dataset and confirm stale derived results are not reused;
7. confirm metrics, insights and quality outputs are unchanged by cache reuse.

## Historical reference

The earlier v1.0 Windows reference check measured 4.07 seconds of core analysis for a 24 MB synthetic fixture containing 738,965 rows. After the first analytical page calculations populated the session cache, the reviewed pages reopened immediately in that observed session.

That result is retained as historical evidence only; hardware, Python version, storage and dataset shape can change timings.

## Acceptance mapping for Issue #16

- Performance baseline for representative datasets: covered by the small / medium / large suite.
- Revisited pages avoid unnecessary full recomputation: preserved by the existing session-cache architecture and tests, plus manual revisit verification.
- Executive Overview and heavy pages remain responsive: verified against the supported large synthetic profile in the manual check.
- Optimization does not change dashboard results: GH-08C does not alter analytical calculations; cache reuse remains result-preserving and tested.
- Performance smoke checks are documented and repeatable: covered by the suite, JSON output and this procedure.

## Regression triggers

Repeat this review when any of the following changes materially:

- the 25 MB supported upload boundary;
- CSV parsing implementation;
- pandas major version or dataframe-copy behaviour;
- session-cache implementation;
- Executive Overview filtering or KPI computation;
- browser-side chart sampling;
- supported Python or operating-system matrix.

## Decision

Issue #16 can close when the GH-08C pull request passes CI and the repeatable performance procedure is accepted as the v1.1 baseline. Any environment-specific timing captured later should be recorded as evidence without turning it into an unsupported global performance promise.
