# v1.1 Export Hardening

This document records GH-08E for Issue #18 — Excel and PDF export hardening for real user workflows.

## Scope

The v1.1 export review covers:

- Excel workbook structure and limits;
- PDF pagination and text wrapping;
- missing values;
- long labels and wide tables;
- deterministic download filenames;
- source-name privacy;
- formula-injection protection;
- consistency between the current dashboard state and generated outputs.

## Existing safety baseline

Before GH-08E, the export layer already provided:

- Excel row and column limit guards;
- formula-like text escaping before workbook writes;
- complete prepared data in the Excel `Data` worksheet;
- traceable KPI formulas and methodology sheets;
- PDF signature and multi-page validation;
- Unicode source-name support;
- theme coverage for Excel and PDF;
- local generation with explicit sharing warnings.

GH-08E preserves those behaviours and adds focused edge-case coverage rather than replacing the export engines.

## Deterministic safe filenames

Generated project, Excel and PDF downloads now use one canonical filename helper.

The helper:

- strips directory components from source names;
- removes characters that are invalid on common desktop filesystems;
- normalizes whitespace;
- limits the generated stem length;
- produces deterministic suffixes for project, Excel and PDF outputs.

Examples:

- `Quarter 1: Sales?.csv` -> `Quarter_1_Sales_analysis.xlsx`;
- `Quarter 1: Sales?.csv` -> `Quarter_1_Sales_executive_report.pdf`.

## Privacy boundary

Only the source basename is passed into generated export metadata. A value such as:

`C:\\Users\\private\\customer\\sales.csv`

is reduced to:

`sales.csv`

before project, Excel or PDF generation. Local directory paths must not appear in generated files.

## Edge-case validation

Automated regression coverage now includes:

- missing numeric values in Excel and PDF inputs;
- deliberately long category labels;
- a wide Excel dataset with more than thirty columns;
- workbook shape and freeze-pane preservation;
- safe deterministic output names;
- path stripping from PDF metadata/text;
- valid multi-page PDF generation after edge-case inputs.

## Manual acceptance check

Before v1.1 release, use the bundled synthetic demo plus one synthetic edge-case CSV and verify:

1. Excel opens without a repair or corruption warning;
2. worksheet names and expected sheets remain intact;
3. long labels remain readable or wrapped rather than silently lost;
4. missing values appear as blanks where appropriate;
5. wide data remains accessible in the Data sheet;
6. PDF headings, cards and insight text are not visibly clipped;
7. multi-page PDF page numbers and footer remain present;
8. filenames are useful and contain no local path fragments;
9. exported content represents the currently loaded/configured dataset;
10. no credentials, local directory paths, session internals or unrelated data appear in the files.

## Acceptance mapping for Issue #18

| Acceptance criterion | GH-08E result |
| --- | --- |
| Excel opens without warnings | Existing valid-workbook tests retained; edge-case workbook generation added |
| PDF has no clipped headings/charts/tables in supported scenarios | Existing pagination/wrapping architecture retained; long-label multi-page regression added; final visual smoke remains a release check |
| Long labels and missing values handled gracefully | Covered by new Excel/PDF edge-case tests |
| Exported content matches visible dashboard state | Builders continue to receive the active dataframe and configuration; no alternate data path added |
| Privacy and security checks pass | Formula injection guard retained; source paths stripped before export; sharing warnings retained |

## Regression triggers

Repeat this review when any of the following changes materially:

- Excel workbook sheet structure;
- ReportLab layout, page size or fonts;
- report themes;
- filename generation;
- source metadata handling;
- dataframe export limits;
- project-state schema;
- security/privacy guidance for generated files.

## Decision

GH-08E establishes the v1.1 export reliability baseline. Issue #18 can close when this pull request passes full CI. Final visual verification of representative Excel/PDF files remains part of v1.1 release readiness so generated-file appearance is checked in addition to structural automated tests.
