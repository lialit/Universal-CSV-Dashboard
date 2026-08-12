# Maintenance Readiness Final Review

This document records GH-07G, the final acceptance review for GH-07 — Maintenance and Dependency Readiness.

## Scope

GH-07 established a repeatable dependency-maintenance baseline and then applied it to the major-version boundaries that were already pending in the repository.

Completed packages:

- GH-07A — dependency update audit and maintenance policy;
- GH-07B — cleanup of stale Dependabot pull requests and migration queue;
- GH-07C — `actions/checkout` v7 migration;
- GH-07D — `actions/setup-python` v7 migration;
- GH-07E — pandas 3 migration;
- GH-07F — ReportLab 5 migration.

## Final baseline

At the time of this review, the supported application dependency ranges are:

- `streamlit>=1.59,<2`;
- `pandas>=3,<4`;
- `plotly>=6,<7`;
- `openpyxl>=3.1,<4`;
- `reportlab>=5,<6`;
- `pypdf>=5,<7`;
- `pytest>=9.0.3,<10`;
- `ruff>=0.12,<1`.

The main CI workflow uses:

- `actions/checkout@v7`;
- `actions/setup-python@v7`;
- Ubuntu Python 3.11 and 3.12 test coverage;
- Windows Python 3.11 test coverage;
- `pip check`;
- dependency vulnerability audit;
- local-first privacy review;
- release-readiness gating.

## Dependabot baseline

Dependabot remains enabled for both Python packages and GitHub Actions.

Routine updates are intentionally grouped only for minor and patch releases. Major-version changes are not grouped into routine maintenance PRs and must be reviewed as isolated migration packages with explicit compatibility evidence and rollback guidance.

The stale mixed-major Dependabot pull requests identified at the start of GH-07 were closed without merge. At this review there are no open Dependabot pull requests from that stale queue.

## Acceptance matrix

| Area | Acceptance result |
| --- | --- |
| Dependency maintenance policy exists | Pass |
| Stale mixed-major Dependabot PRs removed | Pass |
| Major updates isolated one boundary at a time | Pass |
| `actions/checkout` current reviewed major | Pass — v7 |
| `actions/setup-python` current reviewed major | Pass — v7 |
| pandas reviewed major boundary | Pass — 3.x |
| ReportLab reviewed major boundary | Pass — 5.x |
| CI covers Linux and Windows | Pass |
| CI verifies dependency compatibility | Pass |
| CI includes security/dependency audit | Pass |
| Major migrations include rollback guidance | Pass |
| Routine Dependabot grouping excludes majors | Pass |

## Maintenance rule going forward

For minor and patch updates, use the normal Dependabot review path and require green CI before merge.

For any future major update:

1. change one major dependency boundary per PR;
2. identify the product or automation path affected by that dependency;
3. preserve existing tests as behavioural evidence rather than weakening them to make the upgrade pass;
4. add focused compatibility notes when the dependency is central to product behaviour;
5. require the complete relevant CI gates to pass;
6. document a simple rollback path;
7. merge only after the PR is fully green.

If multiple major updates arrive together, split them before review unless they are technically inseparable and that coupling is explicitly documented.

## Regression checklist

Re-run this maintenance review when any of the following changes materially:

- Dependabot grouping or schedule;
- supported Python versions;
- GitHub Actions major versions;
- pandas or another core dataframe dependency major version;
- PDF/export rendering dependencies;
- CI dependency-install or `pip check` behaviour;
- vulnerability-audit tooling;
- release-readiness gates;
- supported operating-system matrix.

Before a stable release, confirm that `requirements.txt`, CI workflow versions and the migration records still describe the actual supported baseline.

## Decision

GH-07 is accepted as complete when this review PR passes the repository checks and is merged into `main`.

The repository now has a controlled dependency-maintenance process: routine updates remain lightweight, major migrations are isolated and attributable, and compatibility decisions are backed by CI evidence and explicit rollback paths.
