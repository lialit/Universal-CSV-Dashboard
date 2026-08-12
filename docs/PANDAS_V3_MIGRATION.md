# pandas 3 Migration

This document records GH-07E, the focused migration from the supported pandas 2.x range to pandas 3.x.

## Scope

This package changes one application dependency major-version boundary only:

- before: `pandas>=2.2,<3`;
- after: `pandas>=3,<4`.

No other dependency major range changes in this package.

## Why pandas needs a dedicated migration

pandas is part of the core data path for Universal CSV Dashboard. It can affect CSV parsing, type inference, transformations, metrics, filtering, data-quality logic, chart inputs and exported tabular data.

A green import check alone is not sufficient. The migration must pass the repository's full automated test matrix and the existing product-path tests.

## Compatibility boundary

The repository continues to support Python 3.11 and 3.12 in CI. The pandas migration does not change Streamlit, Plotly, openpyxl, ReportLab, pypdf, pytest or Ruff major ranges.

The expected product behaviour remains unchanged:

- CSV files load through the existing parser;
- derived metrics remain numerically consistent;
- missing-value and type handling stay deterministic;
- overview and insight calculations retain their current semantics;
- CSV/XLSX/PDF export paths continue to receive valid tabular inputs;
- local-first privacy behaviour is unchanged.

## Acceptance evidence

Before merge, require all of the following:

1. dependency installation succeeds on all supported CI jobs;
2. `python -m pip check` succeeds;
3. core imports succeed with pandas 3;
4. Ruff and compile checks succeed;
5. Ubuntu Python 3.11 tests succeed;
6. Ubuntu Python 3.12 tests succeed;
7. Windows Python 3.11 tests succeed;
8. security/dependency audit succeeds;
9. release readiness succeeds;
10. Documentation links succeeds;
11. Project automation succeeds for the pull request.

Any failing application test must be treated as a compatibility regression rather than bypassed by weakening the test.

## Product-path review

Pay special attention to failures involving:

- `read_csv` and parser options;
- dtype inference and nullable values;
- datetime conversion;
- groupby/aggregation behaviour;
- sorting and indexing;
- numeric coercion;
- DataFrame assignment/copy behaviour;
- CSV and Excel export inputs;
- equality or dtype assertions in tests.

If pandas 3 changes a default that alters user-visible results, prefer an explicit compatibility fix in application code over accepting silent behaviour drift.

## Rollback

If compatibility regressions cannot be resolved cleanly, revert the requirement boundary to `pandas>=2.2,<3`. No other dependency rollback is required because this package changes pandas only.

## Decision

GH-07E is acceptable only when the full CI matrix and existing product behaviour checks pass with pandas 3. The migration is intentionally isolated so any regression remains attributable and reversible.
