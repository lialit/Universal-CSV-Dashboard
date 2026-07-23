# v0.3 — Understand

> **Status: Next — not released**

This is a working release plan. The capabilities below are proposed for the
next product stage and must not be described as currently available.

## Release outcome

Universal CSV Dashboard should produce a stronger, more transparent initial
interpretation of an unfamiliar dataset with less manual correction.

The release moves the product from:

> “The application suggests several field roles.”

to:

> “The application explains the dataset structure, selects a sensible first
> view and shows the user how that view was chosen.”

## Why this release

Version `0.2` established explainable field detection. The next problem is not
uploading the file; it is deciding which detected fields and views are most
useful.

`v0.3` focuses on the first layer of understanding:

- stronger type and role recognition;
- transparent quality assessment;
- better default metrics and charts;
- a factual executive summary.

## Candidate scope

### Dataset understanding

- [ ] Improve identifier detection
- [ ] Recognize currency-like fields
- [ ] Recognize percentage-like fields
- [ ] Detect likely time granularity
- [ ] Improve mixed-format date handling
- [ ] Validate suggested aggregations
- [ ] Capture user corrections for evaluation

### Data Quality Score

- [ ] Define a transparent scoring model
- [ ] Show contributing checks
- [ ] Avoid labeling a dataset simply “clean” or “bad”
- [ ] Explain which issues affect interpretation
- [ ] Test score stability across representative datasets

### Automatic first view

- [ ] Select candidate KPIs
- [ ] Select suitable chart types
- [ ] Keep every selection editable
- [ ] Explain why each view was selected
- [ ] Handle datasets without dates or categories gracefully

### Rule-based executive summary

- [ ] Summarize dataset shape and coverage
- [ ] State the selected metric and aggregation
- [ ] Describe observed totals and ranges
- [ ] Include relevant quality limitations
- [ ] Separate facts from interpretation

### Unsupported input guidance

- [ ] Explain why a dataset cannot produce a useful view
- [ ] Suggest specific corrections
- [ ] Preserve readable errors for parsing failures

## Non-goals

This release does not include:

- AI-generated conclusions;
- causal explanations;
- saved project state;
- PDF or Excel reports;
- autonomous recommendations;
- external data connectors.

## Product requirements

- Automatic choices must remain visible and editable.
- Every score must expose its components.
- The summary must be reproducible from deterministic calculations.
- Missing context must be presented as a limitation, not guessed.
- Local-first operation must remain complete.

## Validation plan

### Detection

- [ ] Evaluate sales, marketing, inventory, finance and operations samples
- [ ] Include datasets with no date field
- [ ] Include datasets with numeric identifiers
- [ ] Include currencies, percentages and mixed date formats
- [ ] Record false-positive role assignments

### Analytical consistency

- [ ] Confirm KPI values match the configured aggregation
- [ ] Confirm summaries match displayed charts
- [ ] Confirm filters update every affected view
- [ ] Confirm quality warnings remain visible

### Experience

- [ ] Measure time to first useful overview
- [ ] Test the flow with a first-time user
- [ ] Review empty and correction states
- [ ] Confirm explanations use business-readable language

### Engineering and documentation

- [ ] Automated tests pass
- [ ] Clean installation verified
- [ ] README features updated only after shipping
- [ ] `CHANGELOG.md` updated at release
- [ ] Final screenshots added

## Known risks

| Risk | Mitigation |
|---|---|
| Identifier treated as a metric | Add cardinality and naming checks; keep selection editable |
| Quality Score creates false confidence | Show components and avoid absolute labels |
| Summary overstates the evidence | Use deterministic facts and explicit limitations |
| Too many automatic decisions reduce trust | Explain every important choice |

## Exit criteria

`v0.3` is ready when representative datasets produce a useful, explainable
first view with minimal correction, and users can identify every assumption
that affects the result.

## Release record

| Field | Value |
|---|---|
| Release date | — |
| Git tag | — |
| GitHub Release | — |
| Migration required | To be determined |

