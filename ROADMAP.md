# Product Roadmap

> **From CSV to clarity — without losing control of the journey.**

This roadmap describes the intended development direction of Universal CSV
Dashboard.

It separates:

- what is available now;
- what is planned next;
- what remains exploratory;
- what must be true before the product is considered stable.

Roadmap items describe direction, not guaranteed delivery dates. Priorities may
change based on testing, user feedback, technical risk and product learning.

---

## Product destination

Universal CSV Dashboard is building toward the easiest trusted starting point
for understanding structured business data.

The product should help a user move from:

> “I have a file.”

to:

> “I understand what it contains, what may be wrong with it and what deserves
> attention next.”

The long-term product is a transparent business-understanding assistant, not an
opaque chart generator or autonomous decision-maker.

---

## Roadmap at a glance

| Version | Stage | Primary outcome | Status |
|---|---|---|---|
| `0.1` | Initial Product | A reusable multipage CSV dashboard | Completed |
| `0.2` | Smart Foundation | Explainable field detection and configurable analysis | Current foundation |
| `0.3` | Understand | Stronger automatic interpretation of structure and quality | Next |
| `0.4` | Explain | Evidence-based observations and clearer context | Planned |
| `0.5` | Share | Saved work and responsible report exports | Planned |
| `0.6` | Assist | Optional guided analysis with privacy controls | Exploratory |
| `1.0` | Launch | Stable, documented and dependable public product | Planned |
| Post-`1.0` | Ecosystem | Specialized analytical modules on a shared core | Directional |

---

## Guiding rules

Every roadmap item should support at least one of these outcomes:

1. reduce time to first useful understanding;
2. improve the reliability of that understanding;
3. make assumptions and limitations more visible;
4. preserve user control;
5. strengthen the local-first workflow;
6. improve the product's maintainability or accessibility.

Features should not be added only because they are technically possible.

---

## `0.1` — Initial Product

**Status: completed**

### Goal

Prove that one reusable Streamlit application can turn a configurable CSV into
a coherent first-pass dashboard.

### Delivered

- [x] Browser-based CSV upload
- [x] Multipage Streamlit navigation
- [x] Manual date, metric and category mapping
- [x] KPI cards
- [x] Time-series chart
- [x] Category comparison
- [x] Distribution analysis
- [x] Descriptive statistics
- [x] Correlation matrix
- [x] Missing-value reporting
- [x] Duplicate-row reporting
- [x] De-duplicated CSV export
- [x] Local-first application workflow

### Product learning

A useful dashboard foundation can be generalized across multiple business
contexts, but manual configuration still creates avoidable setup work.

---

## `0.2` — Smart Foundation

**Status: current foundation**

### Goal

Reduce manual setup while keeping important analytical assumptions visible and
editable.

### Delivered

- [x] Automatic date-column suggestions
- [x] Automatic primary-metric suggestions
- [x] Automatic category suggestions
- [x] Numeric-field recognition
- [x] Identifier, boolean and text-role detection
- [x] Detection confidence scores
- [x] Human-readable detection explanations
- [x] Smart defaults in the configuration flow
- [x] Editable detected fields
- [x] Downloadable dashboard configuration JSON
- [x] Unit tests for the detection engine
- [x] Structured application core and reusable views
- [x] Product brand system and visual assets
- [x] Professional repository README
- [x] Guided `START_HERE.md` onboarding
- [x] Full product specification
- [x] Mission, vision and manifesto

### Foundation-completion work

- [ ] Complete Product Foundation Pack
- [ ] Align remaining duplicate documentation
- [ ] Replace placeholder release notes with factual notes
- [ ] Confirm all documentation links
- [ ] Review installation from a clean environment
- [ ] Confirm the automated test suite on supported Python versions

### Exit criteria

The foundation is complete when a new user can:

1. understand the repository;
2. install the application;
3. upload a compatible CSV;
4. review and correct detected fields;
5. reach the core analytical views;
6. understand visible data-quality limitations;
7. report a problem using the documented workflow.

---

## `0.3` — Understand

**Status: next**

### Goal

Improve the product's ability to understand dataset structure and generate a
more useful first view.

### Planned capabilities

- [ ] Transparent Data Quality Score
- [ ] Rule-based executive summary
- [ ] Automatic KPI selection
- [ ] Automatic chart selection
- [ ] Better identifier detection
- [ ] Currency and percentage recognition
- [ ] Time-granularity recognition
- [ ] Improved date parsing and validation
- [ ] Aggregation recommendations
- [ ] Column-role correction feedback
- [ ] Clearer unsupported-dataset guidance

### Product requirements

- Every score must expose its contributing checks.
- Every automatic selection must remain editable.
- Summaries must separate observed facts from interpretation.
- The product must not imply domain knowledge it does not have.

### Exit criteria

A compatible dataset should produce a useful initial configuration and
business-readable summary with minimal correction.

---

## `0.4` — Explain

**Status: planned**

### Goal

Move from showing metrics to explaining what the evidence suggests and what it
cannot establish.

### Planned capabilities

- [ ] Trend-change detection
- [ ] Category contribution analysis
- [ ] Outlier and anomaly context
- [ ] Period-over-period comparisons
- [ ] Quality-aware observations
- [ ] Plain-language chart explanations
- [ ] Evidence-linked insight cards
- [ ] Suggested next analytical questions
- [ ] Confidence and limitation labels

### Product requirements

- Calculations must be traceable to source fields.
- Correlation must never be described as causation.
- Observations, interpretations and recommendations must be visually distinct.
- Quality limitations must travel with the affected insight.

### Exit criteria

Users should understand why an observation appears, which calculation supports
it and what limitations affect it.

---

## `0.5` — Share

**Status: planned**

### Goal

Preserve and communicate analytical work without losing assumptions or quality
context.

### Planned capabilities

- [ ] Import saved dashboard configuration
- [ ] Saved project state
- [ ] Executive PDF report
- [ ] Structured Excel export
- [ ] Branded report options
- [ ] Light, dark and corporate presentation themes
- [ ] Exported methodology and assumptions
- [ ] Exported data-quality summary
- [ ] Reproducible report metadata

### Product requirements

- Reports must identify the selected metric, aggregation and filters.
- Exports must preserve important limitations.
- The source file must never be overwritten.
- Saved state must fail safely when source columns change.

### Exit criteria

A user should be able to reopen or share an analysis and understand how its
results were produced.

---

## `0.6` — Assist

**Status: exploratory**

### Goal

Evaluate optional guided-analysis capabilities without weakening privacy,
evidence or user control.

### Potential capabilities

- [ ] Ask questions about the loaded dataset
- [ ] Explain metrics and calculations
- [ ] Draft evidence-based summaries
- [ ] Suggest next analyses
- [ ] Identify unsupported questions
- [ ] Optional local or external model providers
- [ ] Explicit privacy controls
- [ ] Usage and cost controls
- [ ] Source-linked responses
- [ ] Visible uncertainty

### Required guardrails

- AI functionality must be optional.
- The non-AI workflow must remain fully useful.
- Data handling must be explained before use.
- Generated text must distinguish evidence from inference.
- Unsupported conclusions must be refused clearly.
- The user must be able to inspect the underlying calculation.

### Decision gate

This stage proceeds only if it creates measurable analytical value beyond
rule-based explanations and can be implemented responsibly.

---

## `1.0` — Launch

**Status: planned**

### Goal

Deliver a stable public product with a dependable core, complete onboarding and
clear support expectations.

### Launch criteria

#### Product

- [ ] Core workflow validated with varied business datasets
- [ ] Clear supported-input boundaries
- [ ] Consistent empty, warning and error states
- [ ] Stable configuration behavior
- [ ] Responsible export workflow

#### Engineering

- [ ] Supported Python versions documented and tested
- [ ] Automated test suite green
- [ ] CI checks stable
- [ ] Dependency policy documented
- [ ] Performance reviewed for supported file sizes
- [ ] Security and privacy review completed

#### Experience

- [ ] Installation tested from a clean machine
- [ ] Accessibility review completed
- [ ] Responsive layout reviewed
- [ ] Key workflows documented with screenshots
- [ ] Example datasets cover primary use cases

#### Open source

- [ ] README, product documents and technical docs aligned
- [ ] Contribution workflow validated
- [ ] Issue and pull-request templates reviewed
- [ ] License and attribution confirmed
- [ ] Release notes complete
- [ ] Support boundaries documented

### Exit criteria

A new user should be able to discover, install, understand and use the product
without private guidance.

---

## Post-`1.0` — Ecosystem

**Status: directional**

After the core product is stable, the shared analytical foundation may support
specialized modules for:

- retail analytics;
- inventory analytics;
- marketing analytics;
- finance and operations;
- forecasting;
- client reporting.

Specialized experiences should reuse common detection, quality, explanation and
reporting foundations rather than becoming disconnected dashboards.

---

## Cross-cutting work

Some work applies to every stage.

### Reliability

- parsing and type-conversion tests;
- consistent calculations across views;
- clear failure recovery;
- no silent source-row loss.

### Privacy

- local-first core workflow;
- explicit external-processing consent;
- sensitive-data guidance;
- no unnecessary persistence.

### Accessibility

- readable contrast;
- keyboard-usable controls where supported;
- information not dependent on color alone;
- understandable labels and error states.

### Documentation

- behavior documented when shipped;
- roadmap updated when priorities change;
- changelog updated with notable changes;
- duplicate sources of truth removed.

### Product learning

- test with real but non-sensitive datasets;
- record field-detection corrections;
- observe where onboarding fails;
- measure time to first useful understanding.

---

## Success measures

The roadmap should improve:

| Measure | Why it matters |
|---|---|
| Upload success rate | Files must enter the workflow reliably |
| Configuration completion rate | Users must be able to reach analysis |
| Detection acceptance rate | Suggestions should reduce setup |
| Time to first overview | The product promise depends on speed |
| Error recovery rate | Failures should not become dead ends |
| Quality-view engagement | Users should see limitations before conclusions |
| Repeat usage | The workflow should be useful beyond a demo |

Numeric targets will be set after meaningful usage data exists.

---

## What is intentionally not on the roadmap

The product is not currently planning to become:

- a spreadsheet editor;
- a data warehouse;
- an enterprise semantic layer;
- a general ETL orchestrator;
- a statistical modeling suite;
- an autonomous business decision-maker;
- a cloud-only analytics platform.

These boundaries may be revisited only if the core product problem changes.

---

## How the roadmap changes

Roadmap updates should:

1. preserve completed history;
2. explain meaningful priority changes;
3. move shipped work into `CHANGELOG.md`;
4. avoid assigning dates without delivery confidence;
5. keep exploratory work clearly labeled;
6. remain consistent with [`PRODUCT.md`](PRODUCT.md),
   [`MISSION.md`](MISSION.md), [`VISION.md`](VISION.md) and
   [`MANIFESTO.md`](MANIFESTO.md).

---

## Current priority

The immediate priority is to finish and validate the `0.2` foundation before
expanding into `0.3`.

That means:

- complete the Foundation Pack;
- remove conflicting documentation;
- verify clean installation and tests;
- replace placeholder release materials;
- confirm that the current product promise matches actual behavior.

> **Build trust in the foundation before adding intelligence to the surface.**

