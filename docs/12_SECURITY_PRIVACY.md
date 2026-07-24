# Security and Privacy

Universal CSV Dashboard is designed around a local-first trust model.

This document describes what the current release candidate does, what it does
not do and which responsibilities remain with the user or deployment operator.

## Data-flow summary

The default workflow is:

1. the user selects a CSV in the Streamlit file uploader;
2. the application receives the uploaded bytes in the active session;
3. pandas parses those bytes through an in-memory `BytesIO` buffer;
4. the prepared dataframe and configuration are stored in Streamlit session
   state;
5. analysis modules calculate metrics, quality checks and explanations;
6. optional PDF, Excel, JSON or project artifacts are generated on request;
7. the user decides whether and where to download or share an export.

The runtime does not require an external analytics API, AI model, telemetry
service or cloud database.

## Uploaded CSV data

Uploaded row-level values are used for the active analysis. The application
does not intentionally:

- transmit CSV values to an external AI service;
- write the uploaded CSV to a project-controlled temporary file;
- persist the dataframe to a product database;
- include raw rows in a saved project/configuration JSON file.

The dataframe remains available in Streamlit session state until the session
is cleared, replaced or terminated. Browser, operating-system, reverse-proxy
and hosting-platform behavior is outside the application's direct control.

## Temporary files and memory

The application parses uploads from bytes and does not create its own
row-level temporary CSV. Python, Streamlit, the browser or a hosting platform
may still use caches, swap space, request buffers or logs.

For sensitive work:

- prefer a trusted local machine;
- avoid shared browser profiles and shared operating-system accounts;
- close the Streamlit session when analysis is complete;
- remove downloaded exports that are no longer required;
- do not upload data to a hosted deployment unless its operator is trusted.

## Saved projects and configurations

A saved project contains:

- product and schema versions;
- source filename and shape;
- column names and inferred types;
- analysis configuration;
- a statement that raw rows are not included.

Reopening a project requires the user to supply the source CSV again. The
application reports source-name, row-count and schema differences rather than
silently treating a different file as identical.

Column names, filenames and schema metadata can themselves be sensitive. Saved
project files should still be reviewed before sharing.

## PDF and Excel exports

Exports are created locally in the active session.

- PDF reports contain summaries, evidence, limitations and source metadata.
- Excel workbooks contain the exported row-level dataset in addition to
  analysis sheets.

An Excel export should receive the same protection as the original CSV.
Recipients can copy, modify and redistribute exported data. The application
cannot revoke a file after download.

Formula-like CSV text is escaped in Excel exports to reduce spreadsheet
formula injection risk.

## External processing

The current release candidate does not call an external AI model or analytics
API. The Analysis Assistant is deterministic and local.

Any future external processing must be:

- optional;
- disabled by default;
- clearly identified before data leaves the session;
- limited to the minimum necessary fields;
- protected by explicit user consent and provider-specific documentation.

External processing must never be introduced behind a generic loading state
or silently enabled by an upgrade.

## Errors, logs and secrets

Streamlit client error details are disabled in `.streamlit/config.toml`.
Repository checks look for common secret filenames and credential-like values.

Users and contributors must not commit:

- `.env` files;
- `.streamlit/secrets.toml`;
- API keys, passwords or private keys;
- real confidential CSV files;
- exports containing client or personal data.

Synthetic datasets should be used for bug reports and automated tests.

## Dependency security

Runtime and quality dependencies use intentional compatible ranges.

The repository uses:

- `pip check` for installed-package compatibility;
- `pip-audit` for known Python dependency vulnerabilities;
- Dependabot for proposed Python and GitHub Actions updates;
- Ruff, pytest and the release-readiness audit as CI quality gates.

A clean vulnerability scan does not prove that a dependency or application is
free of unknown vulnerabilities. Findings require human review for reachability
and impact.

## Deployment trust boundary

Local execution and hosted execution are not equivalent.

When the application is hosted, the deployment operator may control:

- the server and its memory;
- network and proxy logs;
- TLS termination;
- access controls;
- backups and monitoring;
- Streamlit configuration and secrets.

The public project does not claim compliance with GDPR, HIPAA, PCI DSS or
another regulated-data framework. Organizations must perform their own legal,
security and retention review.

## User checklist

Before opening sensitive data:

1. confirm that the application is running in a trusted environment;
2. verify the repository source and installed dependencies;
3. remove unnecessary identifiers from the CSV;
4. avoid real data in screenshots, issues and test fixtures;
5. review every export before sharing;
6. delete local copies according to the applicable retention policy.

## Reporting concerns

Report suspected vulnerabilities through the private process in
[`.github/SECURITY.md`](../.github/SECURITY.md).
