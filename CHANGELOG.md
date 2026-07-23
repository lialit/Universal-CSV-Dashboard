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

### Documentation

- Clarified the difference between available, planned and exploratory
  capabilities.
- Added local-first privacy guidance.
- Added product decision guardrails and success measures.
- Added explicit boundaries describing what the product is not.

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

