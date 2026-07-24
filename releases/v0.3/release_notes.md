# v0.3 — Understand

> **Status: Delivered to `main` — not separately tagged**

This is the historical scope record for the Understand milestone. Checked
items are included in `1.0.0-rc.1`; unchecked items were deferred. No
standalone `v0.3` tag or GitHub Release was published.

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

- [x] Define a transparent scoring model
- [x] Show contributing checks
- [x] Avoid labeling a dataset simply “clean” or “bad”
- [x] Explain which issues affect interpretation
- [x] Test score calculations across representative datasets

### Automatic first view

- [x] Select candidate KPIs
- [x] Select suitable chart types
- [x] Keep every selection editable
- [x] Explain why each view was selected
- [x] Handle datasets without dates or categories gracefully

### Rule-based executive summary

- [x] Summarize dataset shape and coverage
- [x] State the selected metric and aggregation
- [x] Describe observed totals and ranges
- [x] Include relevant quality limitations
- [x] Separate facts from interpretation

### Unsupported input guidance

- [x] Explain why a dataset cannot produce a useful view
- [x] Suggest specific corrections
- [x] Preserve readable errors for parsing failures

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

- [x] Automated tests pass
- [ ] Clean installation verified
- [x] README features updated only after shipping
- [x] `CHANGELOG.md` updated with the delivered milestone
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
