# Engineering Quality Gates

Universal CSV Dashboard uses small, explicit quality gates that can be run
locally and in GitHub Actions.

## Supported environment

- Python 3.11
- dependencies installed from `requirements.txt`
- local-first execution; CI receives no user datasets or credentials

## Required checks

Run these commands from the repository root:

```powershell
python -m pip install -r requirements.txt
python -m pip install -r requirements-security.txt
python -m pip check
python -m pip_audit -r requirements.txt --strict
python -m ruff check .
python scripts/security_review.py --root .
python -m pytest -q
python scripts/release_readiness.py --root .
```

The first four commands must exit successfully before a change is merged.
The readiness audit may still report launch blockers while `v1.0` is being
prepared; its report remains visible in CI as release evidence.

## Security gates

`pip-audit` checks the resolved Python dependency tree against published
vulnerability advisories. `scripts/security_review.py` verifies repository
evidence for the local-first privacy contract:

- uploads are parsed from session bytes;
- no direct external network or AI client is configured;
- detailed Streamlit client errors remain hidden;
- security and privacy behavior is documented;
- the strict dependency audit remains present in CI.

The dependency scan requires network access to current advisory information.
The deterministic privacy review does not transmit a dataset or inspect user
files.

## Ruff baseline

The initial Ruff policy checks:

- `E9` — syntax-level failures;
- `F` — undefined names, invalid imports and other Pyflakes findings.

This focused baseline is intentional. It protects correctness immediately
without mixing release work with a repository-wide formatting rewrite.
Additional rules should be introduced in small, reviewed batches.

## Version source

`app_core/version.py` is the only product-version source.

The release-candidate value is reused by:

- saved project metadata;
- Excel export metadata;
- PDF export metadata.

Do not copy a version literal into another runtime module. Import
`PRODUCT_VERSION` instead.

## Repository hygiene

The repository must not track:

- virtual environments;
- IDE settings;
- Python bytecode or cache directories;
- Ruff, pytest or coverage caches;
- generated build artifacts;
- local Streamlit secrets.

If an ignored artifact was tracked in the past, remove it from the Git index
before committing the release change.
