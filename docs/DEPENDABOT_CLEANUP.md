# Dependabot Cleanup Record

This document records GH-07B cleanup of stale automated dependency pull requests and defines the order for future major migrations.

## Cleanup result

The repository had three older Dependabot pull requests that predated the current dependency-maintenance policy:

- **#4** — `actions/checkout` 5 → 7;
- **#5** — `actions/setup-python` 6 → 7;
- **#6** — a grouped Python update spanning nine packages, including pandas 2 → 3 and ReportLab 4 → 5.

All three were closed without merge because they crossed major compatibility boundaries or combined unrelated major migrations. Each PR contains a closure comment explaining that the update was superseded by the GH-07 maintenance policy.

After cleanup, no open Dependabot pull requests remained.

## Why closing is safer than merging

A stale automated PR can contain valid upstream releases while still being a poor merge unit. Closing it does not reject the dependency forever; it rejects the unsafe grouping or outdated review context.

Major updates must remain attributable. One migration should change one major compatibility boundary whenever practical, so failures and regressions can be traced and rolled back cleanly.

## Major migration queue

Evaluate future major updates in this order:

1. **GitHub Actions runtime migrations** — review workflow security and runner compatibility first.
2. **pandas 3.x** — validate parsing, transformations, data-quality calculations, exports and tests.
3. **ReportLab 5.x** — validate PDF generation, layout, fonts and all report themes.
4. **Other application major versions** — handle individually according to the affected product path.

The queue is not a requirement to upgrade. A major version should be adopted only when it provides enough maintenance, compatibility or security value to justify the migration risk.

## Acceptance rules for a major migration

Before merge:

- review upstream breaking changes and runtime requirements;
- change only the intended major boundary where practical;
- run the full CI matrix;
- run targeted smoke checks for affected product paths;
- validate exports when pandas, openpyxl, ReportLab or pypdf are involved;
- validate workflow security when GitHub Actions change major version;
- update documentation when the supported dependency range changes;
- keep rollback straightforward.

A green CI result is necessary but not sufficient for a major migration.

## Routine maintenance after cleanup

The current Dependabot configuration groups minor and patch updates while leaving major updates visible for separate review. This is the desired steady state.

When a new automated PR appears:

1. confirm whether it stays within the supported major range;
2. review release notes and affected product paths;
3. require CI and dependency auditing;
4. merge routine updates only when the evidence is clear;
5. convert major updates into focused migration work rather than broad grouped maintenance.

## GH-07B decision

GH-07B passes. The stale automated backlog is cleared, the repository has no open Dependabot PRs at the time of review, and future major dependency work has an explicit review order.
