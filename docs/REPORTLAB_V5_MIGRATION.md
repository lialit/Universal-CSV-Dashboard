# ReportLab 5 Migration

This document records GH-07F, the focused migration from the supported ReportLab 4.x range to ReportLab 5.x.

## Scope

This package changes one PDF dependency major-version boundary only:

- before: `reportlab>=4.2,<5`;
- after: `reportlab>=5,<6`.

No other dependency major range changes in this package.

## Why ReportLab needs a dedicated migration

ReportLab is the rendering engine for the executive PDF export. A successful import is not enough evidence because major-version changes can affect document layout, font registration, flowables, tables, paragraph rendering and generated PDF structure.

The dashboard uses ReportLab directly in `app_core/pdf_exports.py` for:

- A4 document generation;
- Paragraph and style rendering;
- Table and TableStyle layout;
- page footers and canvas drawing;
- custom font registration through `TTFont`;
- theme colours and spacing;
- multi-page executive report output.

## Compatibility boundary

Expected behaviour remains unchanged:

- PDF export generates valid bytes;
- executive reports remain readable and multi-page where required;
- report themes continue to render;
- table widths, padding and borders remain usable;
- fonts register on supported Linux and Windows runners, with Helvetica fallback when local fonts are unavailable;
- page footers and page numbering remain present;
- non-ASCII text handling does not regress;
- no CSV, analytics, privacy or release behaviour changes.

## Acceptance evidence

Before merge, require all of the following:

1. dependency installation succeeds on all CI jobs;
2. `python -m pip check` succeeds;
3. application and ReportLab imports succeed;
4. Ruff and compile checks succeed;
5. Ubuntu Python 3.11 tests succeed;
6. Ubuntu Python 3.12 tests succeed;
7. Windows Python 3.11 tests succeed;
8. existing PDF/export tests succeed;
9. security/dependency audit succeeds;
10. release readiness succeeds;
11. Documentation links succeeds;
12. Project automation succeeds for the pull request.

A green CI result is required. Any PDF test failure must be treated as a compatibility regression rather than bypassed by weakening the test.

## Product-path review

Pay special attention to failures involving:

- `SimpleDocTemplate` construction and build;
- `Table`, `TableStyle` and `KeepTogether` behaviour;
- paragraph styling and text wrapping;
- `TTFont` registration or fallback fonts;
- canvas page callbacks and footer drawing;
- colours and unit conversions;
- PDF byte generation and pypdf validation;
- reports with long text, multiple insights or multiple pages;
- report themes and non-ASCII content.

If ReportLab 5 changes a default that alters user-visible PDF output, prefer an explicit compatibility fix in the export code rather than accepting silent layout drift.

## Rollback

If compatibility regressions cannot be resolved cleanly, revert the requirement boundary to `reportlab>=4.2,<5`. No other dependency rollback is required because this package changes ReportLab only.

## Decision

GH-07F is acceptable only when the complete CI matrix and existing PDF/export checks pass with ReportLab 5. The migration is isolated and reversible so any rendering regression remains attributable.
