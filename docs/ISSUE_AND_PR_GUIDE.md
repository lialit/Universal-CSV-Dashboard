# Issue and Pull Request Guide

Use the repository forms and templates to keep reports focused, reproducible, and safe to review.

## Before opening an issue

1. Search existing issues and pull requests.
2. Check `START_HERE.md` for setup and common CSV problems.
3. Reproduce the problem with the smallest safe example possible.
4. Remove credentials, client data, private exports, and sensitive screenshots.

Blank issues are disabled so each public report follows a structured route.

## Choose the correct issue form

### Bug report

Use for reproducible behavior that differs from the documented or expected result. Include:

- exact reproduction steps;
- expected and actual behavior;
- application version or commit SHA;
- operating system, Python version, browser, and deployment type;
- non-sensitive dataset characteristics;
- relevant logs or screenshots after redaction.

The validated v1.0 CSV boundary is 25 MB. Reports involving larger files should state the size clearly because they may describe an unsupported boundary rather than a regression.

### Feature request

Use for a user problem or product capability that is not already covered. Explain the desired outcome, who benefits, alternatives considered, privacy implications, and acceptance criteria.

### Documentation improvement

Use for missing, stale, conflicting, or unclear documentation. Identify the affected page, the reader goal, and the correction needed.

## Security reports

Never open a public issue for a suspected vulnerability. Use the private security-advisory link shown in the issue chooser and follow `.github/SECURITY.md`.

## Pull requests

Before requesting review:

- keep one clear purpose per pull request;
- link the relevant issue when one exists;
- complete every applicable template section;
- list exact validation commands and outcomes;
- explain skipped checks;
- include synthetic screenshots for visible changes;
- review privacy, security, export, compatibility, and performance effects.

See `CONTRIBUTING.md` and `docs/CONTRIBUTOR_VALIDATION.md` for the complete workflow.

## Triage expectations

Labels describe work type, affected area, priority, status, and planned release. `good first issue` is reserved for tasks that are small, clearly scoped, and documented well enough for a new contributor.
