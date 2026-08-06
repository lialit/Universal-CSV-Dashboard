# Contributing

Thank you for helping improve Universal CSV Dashboard. Focused bug fixes,
tests, documentation improvements and carefully scoped product changes are
welcome.

## Before you start

- Read `START_HERE.md`, `PRODUCT.md` and `docs/06_ARCHITECTURE.md`.
- Search existing issues and pull requests before opening a new one.
- Use the repository issue forms for bugs, features and documentation changes.
- Open a feature request before implementing a large capability or changing a
  documented product boundary.
- Comment on an existing issue before starting substantial work so effort is not
  duplicated.
- Never post confidential CSV files, credentials, secrets or private export
  contents.

## Development setup

### Windows PowerShell

```powershell
git clone https://github.com/lialit/Universal-CSV-Dashboard.git
cd Universal-CSV-Dashboard
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt -r requirements-security.txt
python -m streamlit run app.py
```

If PowerShell blocks virtual-environment activation, run this once for the
current terminal session:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

### macOS or Linux

```bash
git clone https://github.com/lialit/Universal-CSV-Dashboard.git
cd Universal-CSV-Dashboard
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt -r requirements-security.txt
python -m streamlit run app.py
```

Use `sample_data/sample_sales.csv` or a synthetic, non-confidential fixture for
public reproduction steps and screenshots.

## Issue workflow

Every implementation should normally correspond to an issue.

- Use `bug`, `feature`, `enhancement`, `documentation`, `performance`,
  `refactor`, `testing` or `dependencies` to describe the work type.
- Use one `area:` label to identify the affected product area.
- Use one `priority:` label when the work has been triaged.
- Use a `release:` label and milestone only after the work has been scheduled.
- Do not apply `good first issue` unless the task is small, clearly scoped and
  documented well enough for a new contributor.

## Branches

Create a short-lived branch from the latest `main`.

```bash
git switch main
git pull --ff-only
git switch -c feature/descriptive-name
```

Recommended prefixes:

- `fix/` for bug fixes;
- `feature/` for new capabilities;
- `perf/` for performance work;
- `docs/` for documentation;
- `refactor/` for internal restructuring;
- `test/` for test-only changes;
- `chore/` for maintenance.

Use lowercase kebab-case and keep the name concise, for example
`perf/cache-executive-overview`.

## Commits

Write concise, imperative commit messages that explain the outcome.

Good examples:

```text
Improve large CSV loading feedback
Fix duplicate chart calculations
Add Excel export validation
Document Windows development setup
```

Keep unrelated changes in separate commits and never commit generated exports,
virtual environments, IDE metadata, secrets or real user datasets.

## Make a focused change

1. Keep one clear purpose per pull request.
2. Put reusable calculations in `app_core/`; keep Streamlit views thin.
3. Preserve offline-first and privacy-first behavior.
4. Add or update tests for behavioral changes.
5. Update documentation, screenshots or release notes when public behavior
   changes.
6. Review privacy, export, performance and compatibility implications.
7. Rebase or merge the latest `main` before requesting final review when needed.

## Validation

Use the smallest useful check set while developing, then run the complete
pull-request readiness set before requesting review.

Fast feedback:

```bash
python -m ruff check .
python -m pytest -q
```

Pull-request readiness:

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

Dependency or security changes also require:

```bash
python -m pip_audit -r requirements.txt --strict
```

See [`docs/CONTRIBUTOR_VALIDATION.md`](docs/CONTRIBUTOR_VALIDATION.md) for the
CI mapping, documentation-only checks and performance evidence expectations.

If a check cannot run, explain why in the pull request. Do not weaken a gate to
make an unrelated change pass.

## Pull requests

- Link the relevant issue with `Closes #123` when the pull request fully resolves
  it.
- Describe the user problem, implementation, validation and known limitations.
- List exact validation commands and their outcomes.
- Include screenshots for visible UI changes using synthetic data.
- Include before/after measurements for performance changes.
- Keep the pull request reasonably small and reviewable.
- Complete every applicable item in the pull request template.
- Mark the pull request as draft while substantial work remains.

A pull request is ready to merge when its scope is clear, required checks pass,
documentation is current and no unresolved review comments remain.

## Review expectations

Review focuses on correctness, user impact, maintainability, privacy, security,
performance and compatibility. Feedback should be specific and constructive.
Changes may be requested when a pull request is too broad, lacks validation or
conflicts with documented product boundaries.

## License

By contributing, you agree that your contribution may be distributed under the
repository's published license.
