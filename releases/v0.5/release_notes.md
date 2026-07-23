# v0.5 — Share

> **Status: Planned — not released**

This document describes intended direction. Scope depends on the validated
output of `v0.3 Understand` and `v0.4 Explain`.

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

- [ ] Import saved dashboard configuration
- [ ] Validate configuration against the current file
- [ ] Detect renamed or missing columns
- [ ] Save selected filters and display options
- [ ] Define a minimal project-state format

### PDF reporting

- [ ] Executive summary page
- [ ] KPI and primary-chart pages
- [ ] Data-quality summary
- [ ] Methodology and assumptions
- [ ] Generation timestamp and product version
- [ ] Accessible page structure

### Excel export

- [ ] Summary worksheet
- [ ] Filtered-data worksheet
- [ ] Data-quality worksheet
- [ ] Configuration worksheet
- [ ] Safe and descriptive filenames

### Branding

- [ ] Optional report logo
- [ ] Controlled accent colors
- [ ] Light, dark and corporate presentation presets
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

- [ ] Confirm saved state does not contain unintended raw data
- [ ] Confirm temporary files are cleaned safely
- [ ] Automated tests pass
- [ ] Installation and export dependencies documented
- [ ] Changelog and final screenshots updated

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

