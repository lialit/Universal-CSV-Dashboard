# v0.5 — Share

> **Status: Delivered to `main` — not separately tagged**

This is the historical scope record for the Share milestone. Checked items are
included in `1.0.0-rc.1`; unchecked items were deferred. No standalone `v0.5`
tag or GitHub Release was published.

## Release outcome

Users should be able to save, reopen and communicate an analysis without losing
the assumptions, filters and data-quality limitations that produced it.

The release moves the product from:

> “I can explore this file now.”

to:

> “I can preserve this work and share a result that another person can
> understand responsibly.”

## Why this release

A screenshot communicates appearance but often loses:

- selected fields;
- aggregation rules;
- active filters;
- quality warnings;
- calculation context;
- version information.

`v0.5` should make analysis portable without turning an attractive report into
unsupported certainty.

## Candidate scope

### Saved work

- [x] Import saved dashboard configuration
- [x] Validate configuration against the current file
- [x] Detect renamed or missing columns
- [ ] Save selected filters and display options
- [x] Define a minimal project-state format

### PDF reporting

- [x] Executive summary page
- [x] KPI snapshot
- [x] Data-quality summary
- [x] Methodology and assumptions
- [x] Generation timestamp and product version
- [ ] Accessible page structure

### Excel export

- [x] Summary worksheet
- [x] Prepared-data worksheet
- [x] Data-quality worksheet
- [x] Configuration worksheet
- [x] Safe and descriptive filenames

### Branding

- [ ] Optional report logo
- [x] Controlled accent colors
- [x] Light, dark and corporate presentation presets
- [ ] Clear distinction between product and customer branding

## Non-goals

This release does not include:

- real-time collaborative editing;
- cloud project synchronization;
- enterprise role management;
- scheduled reports;
- email delivery;
- public dashboard hosting.

## Product requirements

- Exports must identify metric, aggregation and filters.
- Relevant quality limitations must remain visible.
- The source CSV must never be overwritten.
- Saved state must fail safely when the schema changes.
- Reopening an analysis must not silently change calculations.

## Validation plan

### Persistence

- [ ] Reopen configuration with an unchanged file
- [ ] Handle renamed, missing and added columns
- [ ] Handle changed data types
- [ ] Confirm invalid state produces recovery guidance

### Reports

- [ ] Compare report totals with the live dashboard
- [ ] Verify filters and date ranges
- [ ] Review pagination and long labels
- [ ] Confirm quality context is included
- [ ] Test report opening on common viewers

### Privacy and engineering

- [x] Confirm saved state does not contain unintended raw data
- [x] Confirm the application does not create row-level temporary export files
- [x] Automated tests pass
- [x] Installation and export dependencies documented
- [x] Changelog updated
- [ ] Final screenshots updated

## Known risks

| Risk | Mitigation |
|---|---|
| Saved configuration no longer matches the CSV | Validate schema and require confirmation |
| Export loses analytical context | Include assumptions, filters and quality summary |
| Branding reduces readability | Restrict configurable colors and test contrast |
| Project files expose source data | Minimize stored content and document the format |

## Exit criteria

`v0.5` is ready when an analysis can be saved or exported and another person
can identify how the result was produced and which limitations apply.

## Release record

| Field | Value |
|---|---|
| Release date | — |
| Git tag | — |
| GitHub Release | — |
| Migration required | To be determined |
