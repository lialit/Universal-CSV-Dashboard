# Dependency Maintenance

This document defines the GH-07A baseline for reviewing automated dependency updates in Universal CSV Dashboard.

## Goals

Dependency maintenance should keep the project secure and current without turning a green CI result into an automatic approval for compatibility-breaking upgrades.

The project distinguishes between routine updates and compatibility migrations.

## Update classes

### Minor and patch updates

Minor and patch updates may be grouped by Dependabot when they remain inside the supported version ranges in `requirements.txt` or update an existing GitHub Action without changing its major contract.

Before merge:

1. CI must pass on every supported Python/OS job.
2. The dependency audit must pass.
3. Documentation checks must remain green when documentation changes are included.
4. Application imports and automated tests must pass.
5. The PR must not silently widen a supported major-version boundary.

### Major updates

Major dependency updates are migration work, not routine maintenance.

They must be reviewed separately because they can change APIs, defaults, serialization, rendering, export behaviour, runtime requirements or GitHub Actions security semantics.

A major update should normally have its own PR and include:

- release-note review for breaking changes;
- explicit comparison with the current supported range;
- full CI on Python 3.11 and 3.12 plus Windows coverage;
- targeted smoke testing for the affected product path;
- export checks when pandas, openpyxl, reportlab or pypdf changes major version;
- dashboard/UI checks when Streamlit or Plotly changes major version;
- workflow-security review when a GitHub Action changes major version;
- documentation and release-boundary updates if the supported range changes.

Do not merge a mixed dependency PR that combines several unrelated major migrations merely because CI is green.

## Current supported application ranges

The canonical ranges are defined in `requirements.txt`. At the GH-07A review they include:

- Streamlit 1.x;
- pandas 2.x;
- Plotly 6.x;
- openpyxl 3.x;
- ReportLab 4.x;
- pypdf 5.x or 6.x;
- pytest 9.x;
- Ruff 0.x.

Changing one of these major boundaries requires an explicit compatibility decision rather than an incidental Dependabot merge.

## Dependabot configuration

`.github/dependabot.yml` intentionally groups only minor and patch updates. Major updates should remain individually visible for review.

If an old Dependabot PR predates the current grouping policy, do not treat its structure as the current policy. Close or supersede stale mixed-major PRs and allow Dependabot to regenerate updates under the current configuration when appropriate.

## GH-07A audit of existing automated PRs

The maintenance review found three older open Dependabot PRs:

- **#4** — `actions/checkout` 5 → 7. This crosses major versions and includes changed safety behaviour for `pull_request_target`; review separately as a workflow-security migration.
- **#5** — `actions/setup-python` 6 → 7. This is a major GitHub Action migration; review separately before changing all workflows.
- **#6** — grouped Python dependency update covering nine packages. It includes major boundary changes such as pandas 2 → 3 and ReportLab 4 → 5, so it must not be merged as a routine grouped update.

These PRs are candidates to be closed/superseded rather than merged wholesale. Their individual upgrades can be revisited in later GH-07 packages with focused validation.

## Review order

For routine maintenance, prefer this sequence:

1. security-relevant patch updates;
2. compatible application minor/patch updates;
3. development-tool updates;
4. GitHub Action minor/patch updates;
5. one major migration at a time.

This keeps failures attributable and rollback simple.

## Merge evidence

A dependency PR is ready only when the reviewer can answer all of the following:

- What changed and why is it needed?
- Is this inside the current supported major range?
- Which product paths can this dependency affect?
- Did CI and dependency auditing pass?
- Were targeted smoke checks completed for a major migration?
- Does the documented support boundary still match reality?

## Regression checklist

Review this policy when:

1. Dependabot grouping changes;
2. a supported dependency major range changes;
3. Python support changes;
4. a GitHub Action changes major version;
5. dependency audit tooling changes;
6. a stable release is prepared.

Dependency freshness is useful only when compatibility and the local-first security boundary remain explicit.