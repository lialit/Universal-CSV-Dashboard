# actions/setup-python v7 Migration

This document records GH-07D, the focused migration from `actions/setup-python@v6` to `actions/setup-python@v7`.

## Scope

This package changes one GitHub Actions major-version boundary only. `actions/checkout@v7` remains unchanged from GH-07C.

Updated workflows:

- `.github/workflows/ci.yml`;
- `.github/workflows/documentation-links.yml`;
- `.github/workflows/release.yml`.

`project-automation.yml` does not use `actions/setup-python`, so it requires no change.

## Compatibility review

The repository uses only the standard setup inputs needed by the current workflows:

- `python-version`;
- `cache: pip`;
- `cache-dependency-path` where dependency caching is enabled.

The workflows do not use the removed `pip-install` input identified in the v7 release notes. Dependency installation remains explicit through `python -m pip install ...` commands after Python setup.

The migration therefore does not change package resolution, supported Python versions, dependency ranges, test commands or release semantics.

## Runtime coverage

The CI matrix remains:

- Ubuntu with Python 3.11;
- Ubuntu with Python 3.12;
- Windows with Python 3.11.

The lint, security and release-readiness jobs continue to use Python 3.11.

## Acceptance evidence

Before merge, require:

1. lint and configuration succeeds;
2. Ubuntu Python 3.11 tests succeed;
3. Ubuntu Python 3.12 tests succeed;
4. Windows Python 3.11 tests succeed;
5. dependency compatibility and security audit succeed;
6. release readiness succeeds;
7. Documentation links succeeds;
8. Project automation succeeds for the pull request;
9. pip caching initializes successfully where configured.

## Scope boundaries

GH-07D does not change:

- application code;
- Python package version ranges;
- CSV parsing or analytics behaviour;
- exports;
- privacy controls;
- Project field mappings;
- release inputs or draft-release behaviour.

## Rollback

If setup or cache behaviour regresses on GitHub-hosted runners, revert the affected workflow references from `actions/setup-python@v7` to `actions/setup-python@v6`. No application or Python dependency rollback is required.

## Decision

GH-07D is acceptable when all repository checks pass. The migration is isolated, observable and reversible, and completes the two GitHub Actions major migrations identified during GH-07B cleanup.
