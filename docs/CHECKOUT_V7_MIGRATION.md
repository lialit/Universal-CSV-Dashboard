# actions/checkout v7 Migration

This document records GH-07C, the focused migration from `actions/checkout@v5` to `actions/checkout@v7`.

## Scope

This migration changes one GitHub Actions major-version boundary only. `actions/setup-python` remains on v6 and will be evaluated separately.

Updated workflows:

- `.github/workflows/ci.yml`;
- `.github/workflows/documentation-links.yml`;
- `.github/workflows/project-automation.yml`;
- `.github/workflows/release.yml`.

`pr-labeler.yml` does not use `actions/checkout` and therefore requires no change.

## Security review

The repository uses `pull_request_target` in Project automation, so checkout behaviour deserves explicit review. That workflow does not request the pull request head ref; it checks out the repository configuration from the trusted base context and then validates repository-owned scripts and mapping files.

The v7 migration therefore keeps the existing trust boundary rather than adding checkout of untrusted fork code.

The ordinary CI workflow continues to run on `pull_request`, where untrusted changes are tested with read-only repository permissions.

## Compatibility assessment

The migration does not change:

- supported Python versions;
- dependency ranges;
- application code;
- export behaviour;
- release semantics;
- Project field mappings;
- workflow permissions.

Only the checkout action major version changes.

## Acceptance evidence

Before merge, require:

1. CI lint/configuration job succeeds.
2. Linux Python 3.11 and 3.12 tests succeed.
3. Windows Python 3.11 tests succeed.
4. Security/dependency audit succeeds.
5. Release readiness succeeds.
6. Documentation links succeeds.
7. Project automation succeeds for the pull request.
8. No workflow unexpectedly checks out a pull request head under `pull_request_target`.

## Rollback

If runner or checkout behaviour regresses, revert the four workflow references from `actions/checkout@v7` to `actions/checkout@v5`. No application or dependency rollback is required.

## Decision

GH-07C is acceptable when all repository checks pass. The migration is isolated, observable and reversible. `actions/setup-python@v6` remains intentionally unchanged for the next dedicated package.
