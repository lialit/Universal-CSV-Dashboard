# Start Here

Welcome to **Universal CSV Dashboard**.

This guide is the shortest path from cloning the repository to understanding
what the product does, how to run it, and where to go next.

> **Product promise:** Understand your business in under 60 seconds.

## What this project is

Universal CSV Dashboard is a local-first Streamlit application that turns a CSV
file into a structured first-pass business analysis.

You can:

1. upload a CSV;
2. review detected field roles;
3. inspect an executive overview;
4. explore evidence-linked insights;
5. review data quality;
6. save project settings or export traceable reports.

It accelerates the beginning of analysis. It does not replace detailed domain
investigation, spreadsheet editing, or a complete enterprise BI implementation.

## Who it is for

Start here if you are a business owner, consultant, freelancer, analyst,
developer, or contributor who needs a clear first view of business data.

## Five-minute quick start

### Requirements

- Python 3.11 or newer
- `pip`
- a terminal
- a modern web browser

### Clone and create an environment

```bash
git clone https://github.com/lialit/Universal-CSV-Dashboard.git
cd Universal-CSV-Dashboard
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Activate it on macOS or Linux:

```bash
source .venv/bin/activate
```

### Install and run

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m streamlit run app.py
```

Open the local address shown by Streamlit, usually
`http://localhost:8501`.

## Your first product tour

### 1. Upload & Configure

Upload a CSV, review the detected date, metric, and category fields, then adjust
the proposed configuration when necessary.

### 2. Executive Overview

Scan headline metrics, verified facts, rule-based interpretations, limitations,
and the main trend.

### 3. Business Insights

Review evidence-linked contributions, trends, anomalies, and numeric
relationships together with their confidence reasons and limitations.

### 4. Analysis Assistant

Choose a supported local question, inspect the calculation, follow suggested
next steps, and draft a reviewable evidence-based summary.

The assistant uses deterministic local rules. It does not send CSV values to an
external AI service.

### 5. Data Quality

Review missing cells, duplicate rows, column-level quality, and fields that may
need cleaning or reinterpretation.

### 6. Export & Share

Save reusable project configuration or create traceable Excel and executive PDF
reports with quality and methodology context.

### 7. About This Template

Review the product context, intended use, and dashboard guidance.

## Which CSV should I use?

For the first run, use `sample_data/sample_sales.csv` or another small,
non-sensitive file.

A useful starter dataset usually contains:

- one date or timestamp column;
- one or more numeric metrics;
- one or more categories;
- clear column names;
- several rows per category or time period;
- no more than 25 MB for the validated v1.0 workflow.

Avoid confidential production data until you have reviewed the code, your local
environment, and your organisation's data-handling requirements.

## Project map

```text
Universal-CSV-Dashboard/
├── app.py                  # Streamlit entry point and navigation
├── app_core/               # Detection, analysis, and shared logic
├── views/                  # Streamlit pages
├── sample_data/            # Quick-test data
├── examples/               # Example datasets and use cases
├── tests/                  # Automated tests
├── assets/                 # Brand assets and screenshots
├── docs/                   # Product and technical documentation
├── releases/               # Release notes and release materials
├── marketing/              # Launch and communication assets
├── .streamlit/             # Streamlit configuration
└── requirements.txt
```

Open `app.py` for navigation, `app_core/` for analytical behaviour, and `views/`
for page composition.

## Basic test

From the repository root:

```bash
python -m pytest -q
```

This is a useful first check. Contributors should follow the complete validation
levels in [`CONTRIBUTING.md`](CONTRIBUTING.md) and
[`docs/CONTRIBUTOR_VALIDATION.md`](docs/CONTRIBUTOR_VALIDATION.md).

## Common setup problems

### `streamlit` is not recognised

Confirm the virtual environment is active and reinstall dependencies:

```bash
pip install -r requirements.txt
python -m streamlit run app.py
```

### The wrong Python version is active

```bash
python --version
```

In PyCharm, select the project's `.venv` interpreter.

### The CSV does not parse correctly

Check the delimiter, encoding, column names, date formats, numeric fields, and
empty rows or columns. Try a small sample first.

### A chart or metric is missing

Return to **Upload & Configure** and review the detected field roles. A useful
view depends on compatible date, numeric, or categorical fields.

## Choose your next document

| Goal | Read next |
|---|---|
| Understand the complete product | [`README.md`](README.md) |
| Understand the product scope and audience | [`PRODUCT.md`](PRODUCT.md) |
| See the development direction | [`ROADMAP.md`](ROADMAP.md) |
| Browse detailed documentation | [`docs/README.md`](docs/README.md) |
| Contribute code or documentation | [`CONTRIBUTING.md`](CONTRIBUTING.md) |
| Choose an issue or PR route | [`docs/ISSUE_AND_PR_GUIDE.md`](docs/ISSUE_AND_PR_GUIDE.md) |
| Run the correct validation level | [`docs/CONTRIBUTOR_VALIDATION.md`](docs/CONTRIBUTOR_VALIDATION.md) |
| Learn the visual system | [`docs/branding/BRAND_BOOK.md`](docs/branding/BRAND_BOOK.md) |

## Before opening an issue or pull request

Use the structured issue forms and never post confidential datasets,
credentials, or private exports. Follow
[`docs/ISSUE_AND_PR_GUIDE.md`](docs/ISSUE_AND_PR_GUIDE.md) for evidence and
routing requirements.

For pull requests, use [`CONTRIBUTING.md`](CONTRIBUTING.md), record exact
validation commands and outcomes, and explain any skipped check.

## The product principle to remember

Universal CSV Dashboard is not successful because it creates more charts.

It is successful when a person reaches a useful understanding faster.

> **Save hours. Not spreadsheets.**
