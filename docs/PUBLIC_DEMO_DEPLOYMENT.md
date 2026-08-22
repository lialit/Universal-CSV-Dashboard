# Public Demo Deployment

This document records GH-08F deployment readiness and activation for Issue #14 — a public live demo of Universal CSV Dashboard.

## Public URL

The public Streamlit Community Cloud deployment is available at:

https://universal-csv-dashboard-ujqkgrohd7vy4zexcxkuqg.streamlit.app/

## Hosting target

The v1.1 demo is hosted on Streamlit Community Cloud because the product already uses Streamlit, the repository is public, the application entrypoint is `app.py`, and all Python dependencies are declared in the root `requirements.txt`.

## Deployment inputs

The deployed application uses:

- Repository: `lialit/Universal-CSV-Dashboard`
- Branch: `main`
- Entry point: `app.py`
- Python: 3.11 preferred for parity with the primary supported local environment and CI.
- Secrets: none required.

The application is intentionally deployable without API keys, database credentials, external model credentials, or private datasets.

## Hosted upload boundary

The application-level supported upload boundary is 25 MB. The Streamlit server configuration is also set to 25 MB so hosted uploads are rejected at the same public boundary instead of allowing a much larger payload to enter the server before application validation runs.

The canonical application guard remains `app_core.csv_parser.MAX_UPLOAD_SIZE_MB`.

## Demo dataset

The bundled demo dataset introduced in GH-08B is synthetic and is the default public exploration path.

A clean visitor can:

1. open the app;
2. land on Start Here;
3. choose `Try demo data`;
4. reach Executive Overview without uploading a file;
5. visit Business Insights, Analysis Assistant, Data Quality, and Export & Share;
6. return to Start Here or upload a separate CSV if desired.

No confidential or customer-derived data may be bundled into the public demo.

## Hosted acceptance check

The public activation checklist is:

- Start Here renders without an exception;
- bundled demo data loads successfully;
- Executive Overview renders KPI cards, summary content, and charts;
- Business Insights renders evidence-linked content;
- Analysis Assistant renders its supported local guidance flow;
- Data Quality renders its score and issue details;
- Export & Share generates project JSON, Excel, and PDF downloads;
- navigation works at desktop and narrow browser widths;
- an upload over 25 MB is rejected at the documented boundary;
- no local filesystem path appears in the interface or generated export metadata;
- no secrets, credentials, private data, or session internals are exposed;
- a fresh browser session starts without inheriting another user's dataset or configuration.

The public URL has been created successfully. The repository activation PR adds the URL to the README and closes Issue #14 once repository CI is green and the PR is merged.

## Public activation

The activation package:

1. adds the live demo as the first public CTA in `README.md`;
2. adds an `Open Live Demo` badge near the existing trust badges;
3. records the final URL in this deployment document;
4. closes Issue #14 when the activation PR is merged.

The GitHub repository Homepage field should also point to the same verified URL:

https://universal-csv-dashboard-ujqkgrohd7vy4zexcxkuqg.streamlit.app/

## Operational notes

Community Cloud redeploys from repository updates. Dependency changes should therefore continue to pass the repository CI matrix before merge. If the hosted build behaves differently from CI, inspect the Community Cloud build/runtime logs before changing application behaviour.

A public demo is a convenience layer, not a replacement for the local-first product boundary. Users who need maximum control over sensitive data should continue to run the application locally.

## Decision

GH-08F is activation-ready: a real public URL exists, no deployment secrets are required, the bundled demo path is available, and repository documentation can now expose the live demo as the primary adoption CTA. Issue #14 closes through the activation PR after green CI.
