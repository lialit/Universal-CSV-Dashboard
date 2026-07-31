# Contributing

Thank you for helping improve Universal CSV Dashboard. Focused bug fixes,
tests, documentation and carefully scoped product improvements are welcome.

## Before you start

- Read `START_HERE.md`, `PRODUCT.md` and `docs/06_ARCHITECTURE.md`.
- Search existing issues and pull requests.
- Open a feature request before implementing a large capability or changing a
  documented product boundary.
- Never post confidential CSV files, credentials or private export contents.

## Development setup

```bash
git clone https://github.com/lialit/Universal-CSV-Dashboard.git
cd Universal-CSV-Dashboard
python -m venv .venv
python -m pip install --upgrade pip
python -m pip install -r requirements.txt -r requirements-security.txt
```

Activate `.venv`, then run:

```bash
python -m streamlit run app.py
```

Use `sample_data/sample_sales.csv` or a synthetic, non-confidential fixture for
public reproduction steps and screenshots.

## Make a focused change

1. Create a descriptive branch from current `main`.
2. Keep one clear purpose per pull request.
3. Put reusable calculations in `app_core/`; keep Streamlit views thin.
4. Add or update tests for behavioral changes.
5. Update documentation, screenshots or release notes when public behavior
   changes.
6. Review privacy, export and compatibility implications.

## Required checks

```bash
python -m pip check
python -m ruff check .
python -m pytest -q
python scripts/security_review.py --root .
python scripts/release_readiness.py --root .
```

If a check cannot run, explain why in the pull request. Do not weaken a gate to
make an unrelated change pass.

## Pull requests

Describe the user problem, implementation, validation and known limitations.
Include screenshots for visible UI changes. Keep generated files, virtual
environments, IDE metadata and real datasets out of the repository.

By contributing, you agree that your contribution may be distributed under
the repository's published license.
