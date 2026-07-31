# Performance Boundary

Universal CSV Dashboard `1.0.0-rc.1` supports CSV uploads up to **25 MB**.
The application enforces the same boundary in the Streamlit uploader and the
CSV parser.

## Why the upload limit is lower than memory capacity

A CSV file is a compressed textual representation of tabular values. Once
parsed into pandas, the dataframe, derived columns, grouping operations and
Plotly figures can require several times the original file size in memory.

The 25 MB boundary is therefore a reliability limit, not a claim that every
machine has identical performance. Dataset width, text length, category
cardinality and available RAM still affect responsiveness.

KPI, quality and insight calculations use the complete dataset. Browser-side
distribution charts use a deterministic, explicitly labelled visual sample of
at most 50,000 values when the dataset is larger. This limits browser payloads
without presenting the sampled chart as an exact full-data calculation.

Repeated page visits reuse derived results in the current Streamlit session.
The session cache is tied to the identity of the uploaded in-memory dataframe
and small configuration keys; it does not hash or copy the complete dataframe
on every page render. Uploading or preparing a new dataframe clears those
derived results automatically.

## Reference smoke test

Generate a synthetic 24 MB file from the project root:

```powershell
python scripts/generate_performance_fixture.py
```

Measure parsing, smart detection and Data Quality analysis:

```powershell
python scripts/performance_smoke.py performance_sample_24mb.csv
```

Then run the application and upload the same file:

```powershell
python -m streamlit run app.py
```

Review Upload & Configure, Executive Overview, Business Insights, Analysis
Assistant and Data Quality. Record the observed timings and any visible UI
delay in `releases/v1.0/readiness_audit.md`.

The fixture is synthetic and ignored by Git. Remove it after validation:

```powershell
Remove-Item performance_sample_24mb.csv
```

## Acceptance criteria

The reference check passes when:

- the 24 MB fixture loads without an exception or process crash;
- field detection and Data Quality analysis complete;
- navigation remains usable after the dataset is loaded;
- the application explains and rejects files above 25 MB;
- observed timings and the reference environment are documented;
- no universal speed or memory guarantee is inferred from one machine.

## Out-of-scope inputs

Files above 25 MB should be reduced, split or aggregated before upload. Future
versions may support larger inputs through chunked parsing, sampling or a
different execution architecture, but those capabilities are not part of the
v1.0 release candidate.
