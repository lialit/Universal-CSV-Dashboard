# Changelog

All notable changes to Universal CSV Dashboard are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and the project intends to follow
[Semantic Versioning](https://semver.org/spec/v2.0.0.html) as formal releases
are established.

Version sections below record product milestones. The repository does not yet
have a stable `1.0` release.

---

## [Unreleased]

### Added

- Complete Product Foundation documentation:
  - professional product-focused `README.md`;
  - guided `START_HERE.md` onboarding;
  - full `PRODUCT.md` specification;
  - product `MANIFESTO.md`;
  - dedicated `MISSION.md`;
  - long-term `VISION.md`;
  - product-origin story in `WHY.md`;
  - expanded product `ROADMAP.md`.
- BP-01 visual brand system:
  - horizontal and icon logo variants;
  - light and dark GitHub hero assets;
  - Open Graph image;
  - social and launch graphics;
  - favicon assets;
  - screenshot frame;
  - brand book and integration guide.
- Repository documentation for architecture, UX, positioning, branding,
  principles, release process and product decisions.

### Changed

- Repositioned the product from a generic dashboard template to a transparent,
  local-first business-understanding assistant.
- Updated the README to use the complete visual brand and product narrative.
- Improved README hero alignment and asset paths for GitHub rendering.
- Expanded the short product description into a full product specification.
- Replaced the short manifesto with a complete set of product principles.
- Aligned `docs/01_VISION.md` with the canonical mission, vision, manifesto and
  product documents in the repository root.
- Reworked the roadmap around the stages Foundation, Understand, Explain, Share,
  Assist and Launch.
- Added the validated 25 MB upload boundary, bounded distribution rendering and
  lightweight per-session reuse of full-data analytical results.

### Documentation

- Clarified the difference between available, planned and exploratory
  capabilities.
- Added local-first privacy guidance.
- Added product decision guardrails and success measures.
- Added explicit boundaries describing what the product is not.

### Security

- Documented the local upload, session, export and hosted-deployment data flow.
- Added a private vulnerability-reporting policy.
- Added automated local-first privacy-contract checks.
- Added strict dependency vulnerability auditing with `pip-audit`.
- Added weekly dependency and monthly GitHub Actions update checks through
  Dependabot.
- Upgraded `pytest` to `9.0.3` or later to resolve `PYSEC-2026-1845`.

---

## [0.6.0] — Assist

> Delivered to `main` on 2026-07-24 and included in `1.0.0-rc.1`. This
> milestone was not published as a separate Git tag.

### Added

- Local deterministic Analysis Assistant with supported questions for:
  - the first facts to review;
  - primary-metric performance;
  - change over time;
  - leading segment contribution;
  - unusual values;
  - numeric relationships;
  - analysis reliability.
- Availability explanations when the configured dataset cannot support a
  question.
- Evidence-linked answers with confidence, limitations, next steps and a
  visible calculation method.
- Adaptive follow-up questions derived from material insights and quality
  context.
- Transparent Calculation Explainer with aggregation, fields, steps,
  assumptions and limitations.
- Evidence-based summary drafts for different audiences and detail levels.
- Markdown and plain-text summary export.
- Pre-share Claim Guard for unsupported causality, predictions, certainty,
  directive recommendations and invented business context.
- Automated tests for assistant answers, follow-up questions, calculation
  explanations, summary drafts and claim safety.

### Privacy

- Kept the complete assistant workflow local and deterministic.
- Added explicit interface guidance that CSV values are not sent to an external
  AI service.
- Preserved a fully useful non-assistant workflow.

### Product outcome

The application gained guided analysis without making its numeric claims
opaque or introducing external data transfer.

---

## [0.5.0] — Share

> Delivered to `main` on 2026-07-24 and included in `1.0.0-rc.1`. This
> milestone was not published as a separate Git tag.

### Added

- Reusable saved-project JSON containing configuration, schema and version
  metadata without CSV rows.
- Safe project-state loading with schema-change validation and recovery
  guidance.
- Structured Excel report containing:
  - overview and KPI formulas;
  - Data Quality Score details;
  - evidence-linked business insights;
  - selected configuration;
  - the prepared dataset;
  - methodology and responsible-use notes.
- Three-page executive PDF with KPI context, quality evidence, insights,
  suggested questions, methodology and limitations.
- Light, Corporate and Dark report themes shared by Excel and PDF exports.
- Report-theme persistence in saved project state.
- Safe filenames and visible warnings about row-level data in Excel exports.
- Automated project-state, Excel, PDF and report-theme tests.

### Changed

- Replaced the basic de-duplicated CSV-only sharing path with traceable project,
  workbook and executive-report outputs.
- Kept the source CSV unchanged during every export.

### Product outcome

Users can preserve or share an analysis while retaining its configuration,
quality context, evidence and methodological limitations.

---

## [0.4.0] — Explain

> Delivered to `main` on 2026-07-24 and included in `1.0.0-rc.1`. This
> milestone was not published as a separate Git tag.

### Added

- Business Insights page with deterministic observations for:
  - material period changes;
  - leading category contribution;
  - unusual values using the `1.5×IQR` screening rule;
  - material Pearson correlations.
- Separate observation, interpretation, evidence, limitation and next-question
  fields for each insight.
- Confidence labels derived from usable values, metric completeness and the
  Data Quality Score.
- Quality-aware limitations that travel with affected insights.
- Automated calculation and confidence tests for representative analytical
  cases.

### Changed

- Renamed the analytical navigation from generic Data Analysis to
  Business Insights.
- Made correlation language explicitly non-causal.
- Used progressive disclosure so supporting evidence remains inspectable
  without overwhelming the first view.

### Product outcome

The dashboard moved beyond isolated charts to reproducible observations whose
evidence and limits can be inspected.

---

## [0.3.0] — Understand

> Delivered to `main` on 2026-07-24 and included in `1.0.0-rc.1`. This
> milestone was not published as a separate Git tag.

### Added

- Transparent Data Quality Score combining:
  - completeness at a 50% weight;
  - duplicate-free rows at a 30% weight;
  - type validity at a 20% weight.
- Score breakdown with issue counts, checked evidence and recommended actions.
- Column-level missing-value and type-validity details.
- Rule-based executive summary separating verified facts, interpretations,
  limitations and recommended next steps.
- Automatic KPI and chart recommendations based on configured field roles.
- Editable dashboard composition with a visible explanation for each
  recommendation.
- Empty-state guidance when no missing values or supported patterns are found.
- Automated tests for quality scoring, executive summaries and analysis
  recommendations.

### Changed

- Updated Executive Overview to prioritize recommended KPIs and
  business-readable evidence.
- Replaced an empty zero-value missing-data chart with a clear success state.
- Clarified that technical quality does not prove accuracy, lack of bias or
  suitability for a business decision.

### Product outcome

A compatible CSV now produces a useful first view with transparent quality
evidence and deterministic executive context while keeping every important
selection editable.

---

## [0.2.0] — Smart Detection

### Added

- Automatic date-column detection.
- Automatic primary-metric detection.
- Automatic category detection.
- Identifier, boolean and text-column recognition.
- Numeric-column discovery.
- Confidence scores for detected field roles.
- Human-readable explanations for smart suggestions.
- Smart defaults in the Upload & Configure page.
- User controls to confirm or replace suggested fields.
- Downloadable `dashboard_config.json`.
- Unit tests for the detection engine.
- Initial product roadmap.

### Changed

- Reduced the amount of manual field configuration required before opening the
  dashboard.
- Separated reusable detection and data-processing logic from Streamlit views.
- Made detection suggestions visible instead of silently applying them.

### Product outcome

The application moved from a manually configured CSV dashboard to an
explainable smart foundation that proposes a dataset structure while keeping
the user in control.

---

## [0.1.0] — Initial Product

### Added

- Browser-based CSV upload.
- Support for common CSV separators and encodings.
- Multipage Streamlit application.
- Upload & Configure page.
- Executive Overview page.
- Data Analysis page.
- Data Quality page.
- Manual date, metric, additional numeric and category selection.
- Sum, mean, median and count aggregation options.
- KPI cards for total, average, median, row count and column count.
- Date-range filtering.
- Category filtering.
- Interactive time-series chart.
- Interactive category comparison.
- Distribution chart.
- Descriptive-statistics table.
- Correlation matrix for multiple numeric fields.
- Missing-value summary.
- Duplicate-row reporting.
- Column-level data-quality table.
- Filtered data preview.
- De-duplicated CSV export.
- Local-first execution through Streamlit.
- Initial project structure, requirements and test foundation.

### Product outcome

The first product milestone demonstrated that one reusable application could
turn a configurable CSV into a coherent first-pass business dashboard.

---

## Changelog policy

### What belongs here

Add an entry for changes that affect:

- user-visible behavior;
- supported inputs;
- analytical calculations;
- field detection;
- data quality;
- privacy or security;
- installation or compatibility;
- exported artifacts;
- public product documentation;
- deprecated or removed functionality.

### Change categories

Use these headings when applicable:

- `Added` for new capabilities;
- `Changed` for behavior changes;
- `Deprecated` for functionality that will be removed;
- `Removed` for deleted functionality;
- `Fixed` for corrections;
- `Security` for vulnerability-related changes;
- `Documentation` for significant public documentation changes.

### What does not need an entry

Minor formatting, internal refactoring without behavior changes and temporary
development experiments do not require individual changelog entries unless
they materially affect users or contributors.

### Release process

Before a formal release:

1. move relevant items from `Unreleased` into a versioned section;
2. add the release date in `YYYY-MM-DD` format;
3. confirm the version matches the release metadata;
4. verify installation and tests;
5. update release notes;
6. preserve previous entries without rewriting history.
