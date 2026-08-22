# Product Roadmap

> **From CSV to clarity — without losing control of the journey.**

This roadmap describes the intended development direction of Universal CSV
Dashboard. Roadmap items describe direction, not guaranteed delivery dates;
priorities may change based on testing, user feedback, technical risk and
product learning.

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
| `0.2` | Smart Foundation | Explainable field detection and configurable analysis | Completed |
| `0.3` | Understand | Transparent quality scoring and executive interpretation | Delivered in `v1.0.0` |
| `0.4` | Explain | Evidence-based observations with visible limitations | Delivered in `v1.0.0` |
| `0.5` | Share | Saved work and responsible report exports | Delivered in `v1.0.0` |
| `0.6` | Assist | Local deterministic guidance with privacy controls | Delivered in `v1.0.0` |
| `1.0` | Launch | Stable, documented and dependable public product | Released |
| `1.1` | Polish & Adoption | Faster first-run experience, public demo, UX polish and release-quality evidence | In progress |
| Post-`1.1` | Ecosystem | Specialized analytical modules on a shared core | Directional |

Detailed scope, validation plans and release criteria are maintained in the
[`Release Hub`](releases/README.md). Shipped changes remain recorded in
[`CHANGELOG.md`](CHANGELOG.md).

---

## Guiding rules

Every roadmap item should support at least one of these outcomes:

1. reduce time to first useful understanding;
2. improve the reliability of that understanding;
3. make assumptions and limitations more visible;
4. preserve user control;
5. strengthen the local-first workflow;
6. improve maintainability, accessibility or adoption.

Features should not be added only because they are technically possible.

---

## `0.1–0.2` — Foundation

**Status: completed**

The foundation established the reusable Streamlit application, CSV upload,
manual and automatic field-role configuration, core analytical views,
explainable detection, project structure, tests, brand system and public
repository documentation.

The product learning from this stage was clear: a generalized dashboard can
work across business contexts, but setup friction and trust signals matter as
much as chart generation.

---

## `0.3–0.6` — Understand, Explain, Share and Assist

**Status: delivered in `v1.0.0`; intermediate milestones were not separately tagged**

These stages added the trusted analytical layer that shipped in v1.0:

- transparent Data Quality Score and component evidence;
- rule-based executive summaries and automatic KPI/chart selection;
- evidence-linked trend, contribution, anomaly and relationship observations;
- confidence, limitations and explicit non-causal language;
- saved project state with schema validation;
- traceable Excel and executive PDF reports;
- deterministic local Analysis Assistant with inspectable calculations;
- privacy guidance and unsupported-question handling.

Important boundaries remain deliberate: no external model provider, no causal
claims, no autonomous recommendations, no cloud project synchronization and no
attempt to become a spreadsheet editor or enterprise BI platform.

---

## `1.0` — Launch

**Status: released (`v1.0.0`)**

### Goal

Deliver a stable public product with a dependable core, complete onboarding,
clear support expectations and reproducible release evidence.

### Delivered launch baseline

- stable CSV parsing and field configuration;
- consistent empty, warning and error states;
- responsible Excel/PDF export workflow;
- Python 3.11+ support with Linux and Windows CI;
- documented dependency, performance, security and privacy boundaries;
- contribution, issue, support and security-reporting workflows;
- stable GitHub Release automation and public trust documentation.

### Exit result

A new user can discover, install, understand and use the stable product without
private guidance.

---

## `1.1` — Polish & Adoption

**Status: in progress**

### Goal

Reduce friction between discovering the repository and reaching a useful
business view, while preserving the v1.0 reliability and privacy boundaries.

### Delivered to `main` so far

- [x] Guided **Start Here** page with two explicit paths: bundled demo data or user CSV.
- [x] Bundled synthetic `demo_business.csv` for safe first-run exploration.
- [x] Repeatable performance confidence suite for small, medium and near-boundary CSV profiles.
- [x] Responsive navigation and actionable empty states.
- [x] Excel and PDF export hardening, including safe deterministic filenames and edge-case tests.
- [x] Public Streamlit Community Cloud deployment with no required secrets.
- [x] Public **Open Live Demo** CTA in the repository README.
- [x] Hosted upload boundary aligned with the documented 25 MB application limit.
- [x] v1.1 release screenshot set captured from the synthetic demo workflow.

### Current completion work

- [ ] Finalize user documentation and release screenshots.
- [ ] Run targeted beta feedback and record reproducible issues.
- [ ] Complete the v1.1 release gate, changelog and release notes.

### v1.1 experience target

A first-time visitor should be able to:

1. open the public demo or run locally;
2. choose **Try demo data** without supplying a file;
3. reach Executive Overview quickly;
4. understand the evidence and limitations behind insights;
5. inspect data quality before acting on results;
6. export or save work without exposing local paths or source rows unexpectedly;
7. switch to their own compatible CSV when ready.

### Acceptance boundaries

- Public demo convenience must not replace the local-first option for sensitive data.
- The supported upload boundary remains 25 MB unless separately revalidated.
- Analytics remain deterministic, evidence-linked and non-causal.
- Major dependency upgrades continue to require dedicated migration evidence.
- Release screenshots must use synthetic data and match the actual interface.

See [`releases/v1.1/release_notes.md`](releases/v1.1/release_notes.md) for the
working release record.

---

## Post-`1.1` — Ecosystem

**Status: directional**

After the core product is stable and v1.1 adoption feedback is collected, the
shared analytical foundation may support specialized modules for:

- retail and inventory analytics;
- marketing analytics;
- finance and operations;
- forecasting;
- client reporting.

Specialized experiences should reuse common detection, quality, explanation and
reporting foundations rather than becoming disconnected dashboards.

---

## Cross-cutting work

### Reliability

- parsing and type-conversion tests;
- consistent calculations across views;
- clear failure recovery;
- no silent source-row loss.

### Privacy

- local-first workflow remains first-class;
- hosted demo uses no required secrets;
- sensitive-data guidance stays visible;
- no unnecessary persistence.

### Accessibility and UX

- readable contrast;
- understandable labels and error states;
- useful narrow-width behavior;
- information not dependent on color alone;
- no dead-end empty states.

### Documentation

- behavior documented when shipped;
- roadmap updated when priorities change;
- changelog updated with notable changes;
- screenshots represent the current product;
- duplicate sources of truth removed.

### Product learning

- test with real but non-sensitive datasets;
- record field-detection corrections;
- observe where onboarding fails;
- measure time to first useful understanding;
- collect beta feedback before expanding scope.

---

## Success measures

| Measure | Why it matters |
|---|---|
| Demo-to-overview completion | The public product should prove value quickly |
| Upload success rate | Compatible files must enter the workflow reliably |
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

## Current priority

The immediate priority is to finish **v1.1 — Polish & Adoption** without
expanding scope: finalize public documentation, collect structured beta feedback
and pass the release gate.

> **Polish the path. Verify the evidence. Release only what passed.**
