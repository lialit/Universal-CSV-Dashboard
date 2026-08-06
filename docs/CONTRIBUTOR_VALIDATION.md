# Contributor Validation

This guide maps local contributor checks to the repository's GitHub Actions gates.

## Choose the right validation level

### Fast feedback

Use while developing a focused change:

```bash
python -m ruff check .
python -m pytest -q
```

For documentation-only changes, also run:

```bash
python scripts/check_markdown_links.py
```

### Pull-request readiness

Run before opening or updating a pull request:

```bash
python -m pip check
python -m ruff check .
python scripts/validate_project_automation.py
python -m compileall -q app.py app_core pages scripts tests
python -m pytest -q
python scripts/security_review.py --root .
python scripts/release_readiness.py --root .
python scripts/check_markdown_links.py
```

Install `requirements-security.txt` before running the security-specific tools.

### Dependency and security changes

When dependencies or security controls change, also run:

```bash
python -m pip_audit -r requirements.txt --strict
```

### Performance changes

Run the relevant smoke or benchmark script and include:

- the command used;
- representative input size;
- before and after measurements;
- operating system and Python version;
- any known measurement limitations.

## CI mapping

| CI gate | Main checks |
|---|---|
| Lint and configuration | Ruff, Project automation validation, Python compilation |
| Tests | dependency compatibility, core imports, pytest on Linux and Windows with Python 3.11/3.12 |
| Security and dependencies | pip check, pip-audit, local-first security review |
| Release readiness | requires the other CI gates, then publishes readiness evidence |
| Documentation links | repository-local Markdown and HTML targets |

CI remains the source of truth. If this document and a workflow disagree, update the documentation in the same pull request that changes the workflow.

## Reporting validation in a pull request

List exact commands and outcomes. Do not write only “tests pass.” Mention skipped checks and explain why they were not applicable or could not run.

Examples:

```text
python -m ruff check . — passed
python -m pytest -q — 176 passed
python scripts/check_markdown_links.py — passed
pip-audit — not applicable; dependencies unchanged
```

Never weaken or remove a gate merely to make an unrelated pull request pass.