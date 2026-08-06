# Contributor Experience Review

This document records the acceptance criteria for the repository's public contributor journey. It is intended for maintainers reviewing onboarding changes and for future regression checks.

## Supported contributor journey

A new contributor should be able to complete this path without comparing conflicting instructions:

1. Understand the product from `README.md`.
2. Install and run the application from `START_HERE.md`.
3. Browse detailed documentation from `docs/README.md`.
4. Choose the correct public issue form or private security route.
5. Follow the branch, implementation, and review workflow in `CONTRIBUTING.md`.
6. Select the appropriate local validation level from `docs/CONTRIBUTOR_VALIDATION.md`.
7. Open a pull request with exact validation evidence and privacy-impact notes.
8. Pass CI, documentation-link checks, labeling, and project automation.

## Final GH-05 review

| Area | Acceptance criterion | Status |
|---|---|---|
| Product entry point | README explains the product and provides a minimal runnable quick start | Passed |
| First-use onboarding | START_HERE owns installation, first tour, and setup troubleshooting | Passed |
| Documentation discovery | `docs/README.md` provides goal-based navigation | Passed |
| Documentation ownership | Canonical document responsibilities are explicit | Passed |
| Link integrity | Repository-local Markdown and HTML targets are checked automatically | Passed |
| Freshness | Stable `v1.0.0` is recorded as the canonical public release | Passed |
| Contributor setup | CONTRIBUTING provides current development and branch guidance | Passed |
| Validation clarity | Local commands are mapped to the real CI gates | Passed |
| Pull-request evidence | The PR template requests exact commands, outcomes, and skipped-check explanations | Passed |
| Issue routing | Structured issue forms replace duplicate legacy templates | Passed |
| Security reporting | Suspected vulnerabilities are routed to private advisories | Passed |
| Data safety | Public examples, logs, screenshots, and fixtures must be synthetic or redacted | Passed |

## Regression checklist

Re-run this review when entry-point documents, issue forms, the pull-request template, CI gates, supported Python versions, release status, privacy boundaries, or repository automation change.

Confirm that:

- all canonical entry points link to the current documents;
- setup commands match supported dependencies and Python versions;
- issue forms request reproducible evidence without encouraging private-data uploads;
- the private security route remains available;
- CONTRIBUTING and the PR template match current CI expectations;
- `python scripts/check_markdown_links.py` passes;
- no legacy template duplicates have returned;
- public release wording matches the current stable release.

## Ownership

`README.md`, `START_HERE.md`, `CONTRIBUTING.md`, and `docs/README.md` remain the primary contributor entry points. This review records acceptance criteria; it does not replace the detailed procedures in those documents.
