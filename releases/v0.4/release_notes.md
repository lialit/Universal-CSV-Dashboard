# v0.4 — Explain

> **Status: Planned — not released**

This document describes intended direction. Scope may change after the
`v0.3 Understand` release is validated.

## Release outcome

Universal CSV Dashboard should help users understand why a pattern deserves
attention, which evidence supports it and what limits the conclusion.

The release moves the product from:

> “Here is the metric.”

to:

> “Here is what changed, where the change is concentrated and which limitations
> affect the observation.”

## Why this release

Metrics and charts create visibility, but not always understanding.

Users need help connecting:

- a trend to the relevant period;
- a total to the categories that contribute to it;
- an observation to its source calculation;
- a conclusion to the quality of the underlying data.

`v0.4` should make those connections without pretending to possess missing
business context.

## Candidate scope

### Evidence-based observations

- [ ] Period-over-period comparisons
- [ ] Trend-change detection
- [ ] Category contribution analysis
- [ ] Distribution-shift observations
- [ ] Outlier context
- [ ] Quality-aware observation filtering

### Explanations

- [ ] Plain-language chart descriptions
- [ ] Calculation and field references
- [ ] Visible comparison periods
- [ ] Confidence and limitation labels
- [ ] “Why am I seeing this?” details

### Next-question guidance

- [ ] Suggest relevant follow-up views
- [ ] Identify questions supported by available fields
- [ ] Identify questions the dataset cannot answer
- [ ] Separate investigation prompts from recommendations

### Insight presentation

- [ ] Evidence-linked insight cards
- [ ] Visual distinction between fact and interpretation
- [ ] Consistent language across pages and exports
- [ ] Prioritization without hiding lower-ranked observations

## Non-goals

This release does not include:

- causal inference;
- predictive modeling;
- autonomous business recommendations;
- an AI chat interface;
- external web research;
- report persistence or collaboration.

## Product requirements

- Every observation must be traceable to a calculation.
- Correlation must never be described as causation.
- Quality limitations must accompany affected observations.
- The interface must distinguish fact, interpretation and suggestion.
- The user must be able to inspect the selected fields and comparison period.

## Validation plan

### Analytical

- [ ] Verify calculations against independent Pandas checks
- [ ] Test stable, rising, falling and irregular time series
- [ ] Test sparse and highly imbalanced categories
- [ ] Test observations affected by missing values
- [ ] Review false-positive anomaly language

### Language

- [ ] Remove unsupported causal wording
- [ ] Confirm uncertainty is visible
- [ ] Check explanations with non-technical users
- [ ] Verify consistent terminology with the manifesto

### Experience and engineering

- [ ] Confirm insight cards do not overwhelm the overview
- [ ] Confirm details are progressively disclosed
- [ ] Automated tests pass
- [ ] Performance reviewed
- [ ] Documentation and changelog updated

## Known risks

| Risk | Mitigation |
|---|---|
| Observation sounds like a recommendation | Use explicit content types and labels |
| Anomaly rule produces noise | Rank cautiously and expose thresholds |
| Explanation hides the calculation | Provide evidence and field details |
| Too many insights reduce clarity | Prioritize and use progressive disclosure |

## Exit criteria

`v0.4` is ready when every displayed observation can be reproduced, explained
and interpreted with its relevant limitations.

## Release record

| Field | Value |
|---|---|
| Release date | — |
| Git tag | — |
| GitHub Release | — |
| Migration required | To be determined |

