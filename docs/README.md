# Documentation

This directory contains the product, engineering, design, security and release documentation for Universal CSV Dashboard.

Use the root documents first:

- [`../README.md`](../README.md) — product overview, screenshots and quick start;
- [`../START_HERE.md`](../START_HERE.md) — installation, first product tour and common setup problems;
- [`../SUPPORT.md`](../SUPPORT.md) — bugs, usage help, feature requests and security routing;
- [`../CONTRIBUTING.md`](../CONTRIBUTING.md) — development workflow, validation and pull-request expectations;
- [`../PRODUCT.md`](../PRODUCT.md) — product scope, audience and value;
- [`../ROADMAP.md`](../ROADMAP.md) — current delivery direction.

## Choose documentation by goal

### Understand the product

- [`01_VISION.md`](01_VISION.md) — long-term product vision;
- [`02_POSITIONING.md`](02_POSITIONING.md) — positioning and product promise;
- [`03_PRODUCT_PRINCIPLES.md`](03_PRODUCT_PRINCIPLES.md) — product decision principles;
- [`04_USER_PERSONAS.md`](04_USER_PERSONAS.md) — intended user groups;
- [`05_PRODUCT_ROADMAP.md`](05_PRODUCT_ROADMAP.md) — detailed product roadmap;
- [`11_COMPETITORS.md`](11_COMPETITORS.md) — competitive context.

### Understand the implementation

- [`06_ARCHITECTURE.md`](06_ARCHITECTURE.md) — application architecture and module boundaries;
- [`11_ENGINEERING_QUALITY.md`](11_ENGINEERING_QUALITY.md) — tests, CI, dependency and readiness gates;
- [`CONTRIBUTOR_VALIDATION.md`](CONTRIBUTOR_VALIDATION.md) — local check levels and CI mapping;
- [`ISSUE_AND_PR_GUIDE.md`](ISSUE_AND_PR_GUIDE.md) — issue routes, required evidence and pull-request expectations;
- [`CONTRIBUTOR_EXPERIENCE_REVIEW.md`](CONTRIBUTOR_EXPERIENCE_REVIEW.md) — end-to-end onboarding acceptance and regression checklist;
- [`13_PERFORMANCE_BOUNDARY.md`](13_PERFORMANCE_BOUNDARY.md) — validated CSV size boundary and performance procedure;
- [`12_SECURITY_PRIVACY.md`](12_SECURITY_PRIVACY.md) — local data flow, privacy and security boundaries.

### Work on design and communication

- [`07_UX_PRINCIPLES.md`](07_UX_PRINCIPLES.md) — UX principles;
- [`08_BRANDING.md`](08_BRANDING.md) — brand overview;
- [`branding/BRAND_BOOK.md`](branding/BRAND_BOOK.md) — complete visual identity rules;
- [`09_PRICING.md`](09_PRICING.md) — pricing direction;
- [`12_DEVLOG.md`](12_DEVLOG.md) — development notes.

### Operate releases and repository automation

- [`10_RELEASE_PROCESS.md`](10_RELEASE_PROCESS.md) — release policy and readiness flow;
- [`RELEASE_WORKFLOW_OPERATIONS.md`](RELEASE_WORKFLOW_OPERATIONS.md) — workflow modes and smoke cleanup;
- [`RELEASE_NOTES_PREVIEW_VALIDATION.md`](RELEASE_NOTES_PREVIEW_VALIDATION.md) — generated-note category validation;
- [`PR_LABELING.md`](PR_LABELING.md) — automatic and semantic pull-request labels;
- [`PROJECT_AUTOMATION.md`](PROJECT_AUTOMATION.md) — GitHub Project synchronization behavior;
- [`DEPENDENCY_MAINTENANCE.md`](DEPENDENCY_MAINTENANCE.md) — routine dependency updates, major-migration rules and Dependabot review baseline;
- [`DEPENDABOT_CLEANUP.md`](DEPENDABOT_CLEANUP.md) — GH-07B cleanup record and major-migration review order;
- [`CHECKOUT_V7_MIGRATION.md`](CHECKOUT_V7_MIGRATION.md) — GH-07C checkout v7 security review, acceptance evidence and rollback plan;
- [`SETUP_PYTHON_V7_MIGRATION.md`](SETUP_PYTHON_V7_MIGRATION.md) — GH-07D setup-python v7 compatibility review, acceptance evidence and rollback plan;
- [`PANDAS_V3_MIGRATION.md`](PANDAS_V3_MIGRATION.md) — GH-07E pandas 3 compatibility boundary, validation evidence and rollback plan;
- [`REPORTLAB_V5_MIGRATION.md`](REPORTLAB_V5_MIGRATION.md) — GH-07F ReportLab 5 PDF compatibility boundary, validation evidence and rollback plan;
- [`MAINTENANCE_READINESS_FINAL_REVIEW.md`](MAINTENANCE_READINESS_FINAL_REVIEW.md) — GH-07G final maintenance acceptance result and regression baseline;
- [`V1_1_EXECUTION_READINESS.md`](V1_1_EXECUTION_READINESS.md) — GH-08A v1.1 backlog sequencing, dependency order and delivery rules;
- [`PUBLIC_REPOSITORY_PROFILE.md`](PUBLIC_REPOSITORY_PROFILE.md) — About metadata, topics, public features and trust-signal checklist;
- [`TRUST_BADGES.md`](TRUST_BADGES.md) — approved README badges, evidence links and maintenance rules;
- [`RELEASE_COMMUNITY_TRUST_AUDIT.md`](RELEASE_COMMUNITY_TRUST_AUDIT.md) — stable release, support, security and community acceptance review;
- [`PUBLIC_CONVERSION_AUDIT.md`](PUBLIC_CONVERSION_AUDIT.md) — first-screen calls to action and visitor-path regression checklist;
- [`PUBLIC_TRUST_FINAL_REVIEW.md`](PUBLIC_TRUST_FINAL_REVIEW.md) — complete GH-06 acceptance result and maintenance baseline.

## Document ownership

Each topic should have one canonical document. Other pages should link to it instead of copying complete procedures.

- Product introduction belongs in `README.md`.
- Installation and first-use guidance belongs in `START_HERE.md`.
- Public help and support boundaries belong in `SUPPORT.md`.
- Contributor rules belong in `CONTRIBUTING.md`.
- Detailed technical and operational guidance belongs under `docs/`.
- Release-specific assets and records belong under `releases/`.

When public behavior changes, update the canonical document in the same pull request. Keep examples synthetic and never add confidential datasets, credentials or private export contents.
