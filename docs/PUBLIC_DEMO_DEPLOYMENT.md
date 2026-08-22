# Public Demo Deployment

This document records GH-08F deployment readiness for Issue #14 — a public live demo of Universal CSV Dashboard.

## Hosting target

The preferred host for v1.1 is Streamlit Community Cloud because the product already uses Streamlit, the repository is public, the application entrypoint is `app.py`, and all Python dependencies are declared in the root `requirements.txt`.

## Deployment inputs

Use the following values when creating the Community Cloud app:

- Repository: `lialit/Universal-CSV-Dashboard`
- Branch: `main`
- Entry point: `app.py`
- Python: 3.11 or 3.12; 3.11 is preferred for parity with the primary supported local environment and CI.
- Secrets: none required.

The application is intentionally deployable without API keys, database credentials, external model credentials, or private datasets.

## Hosted upload boundary

The application-level supported upload boundary is 25 MB. The Streamlit server configuration is also set to 25 MB so hosted uploads are rejected at the same public boundary instead of allowing a much larger payload to enter the server before application validation runs.

The canonical application guard remains `app_core.csv_parser.MAX_UPLOAD_SIZE_MB`.

## Demo dataset

The bundled demo dataset introduced in GH-08B is synthetic and is the default public exploration path.

A clean visitor should be able to:

1. open the app;
2. land on Start Here;
3. choose `Try demo data`;
4. reach Executive Overview without uploading a file;
5. visit Business Insights, Analysis Assistant, Data Quality, and Export & Share;
6. return to Start Here or upload a separate CSV if desired.

No confidential or customer-derived data may be bundled into the public demo.

## First deployment procedure

1. Sign in to Streamlit Community Cloud with the GitHub account that has admin access to this repository.
2. Create a new app from an existing repository.
3. Select the repository, `main` branch, and `app.py` entrypoint shown above.
4. Open Advanced settings and select Python 3.11 when available.
5. Do not add secrets.
6. Choose a stable public `streamlit.app` subdomain.
7. Deploy and wait for the first build to complete.
8. Open the resulting public URL in a clean/incognito browser session.

## Hosted acceptance check

Before adding the public URL to README, verify all of the following in a clean browser session:

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

## Public activation

Do not add a README `Open Live Demo` CTA until the hosted acceptance check passes.

Once the URL is verified:

1. add it as the first public CTA in `README.md`;
2. add an `Open Live Demo` badge or button near the existing trust badges;
3. set the GitHub repository Homepage field to the verified live-demo URL;
4. verify the README link from a logged-out browser;
5. record the final URL in Issue #14 and close it through the activation PR.

## Operational notes

Community Cloud redeploys from repository updates. Dependency changes should therefore continue to pass the repository CI matrix before merge. If the hosted build behaves differently from CI, inspect the Community Cloud build/runtime logs before changing application behaviour.

A public demo is a convenience layer, not a replacement for the local-first product boundary. Users who need maximum control over sensitive data should continue to run the application locally.

## Decision

The repository is deployment-ready when this package passes CI. Issue #14 remains open until a real public URL has been deployed, verified in a clean browser session, and added to the README and repository profile.
