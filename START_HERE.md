# Start Here

Welcome to **Universal CSV Dashboard**.

This guide is the shortest path from cloning the repository to understanding
what the product does, how to run it and where to go next.

> **Product promise:** Understand your business in under 60 seconds.

## What this project is

Universal CSV Dashboard is a local-first Streamlit application that turns a CSV
file into a structured first-pass business analysis.

Instead of manually deciding which spreadsheet columns matter, creating the
same charts again and checking data quality separately, you can:

1. upload a CSV;
2. review the detected field roles;
3. open an executive overview;
4. explore trends and distributions;
5. inspect data quality.

The application is designed to accelerate the beginning of analysis. It does
not replace detailed domain investigation, spreadsheet editing or a complete
enterprise BI implementation.

## Who it is for

Start here if you are:

- a business owner who needs a clear first view of exported data;
- a consultant analysing client CSV files;
- a freelancer preparing a quick data review;
- an analyst who wants a reusable exploration workflow;
- a developer learning how the application is structured;
- a contributor preparing an issue or pull request.

## Five-minute quick start

### 1. Check the requirements

You need:

- Python 3.11 or newer;
- `pip`;
- a terminal;
- a modern web browser.

### 2. Clone the repository

```bash
git clone https://github.com/lialit/Universal-CSV-Dashboard.git
cd Universal-CSV-Dashboard
```

### 3. Create a virtual environment

```bash
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

### 4. Install the dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

The current application uses:

- Streamlit for the interface;
- Pandas for data processing;
- Plotly for interactive charts;
- Pytest for automated tests.

### 5. Run the application

```bash
streamlit run app.py
```

Streamlit will display a local address, usually:

```text
http://localhost:8501
```

Open it in your browser.

## Your first product tour

The application contains four core dashboard pages and one product page.

### 1. Upload & Configure

Start here.

- Upload a CSV file.
- Review the detected date, metric and category fields.
- Confirm or adjust the proposed configuration.
- Check whether the dataset was parsed as expected.

Automatic detection should save time, but the user remains in control.

### 2. Executive Overview

Use this page for the first business read.

- Review headline metrics.
- Scan the main trend.
- Check the most important category view.
- Apply available filters to narrow the analysis.

### 3. Data Analysis

Use this page when you need more detail.

- Explore trends over time.
- Compare categorical values.
- Inspect distributions and relationships supported by the dataset.

### 4. Data Quality

Open this page before trusting a conclusion.

- Review missing cells.
- Check duplicate rows.
- Inspect column-level quality.
- Identify fields that may need cleaning or reinterpretation.

### 5. About This Template

Use this page for product context and guidance about the dashboard.

## Which CSV should I use?

For the first run, use a small, non-sensitive file.

Good starter datasets usually contain:

- one date or timestamp column;
- one or more numeric business metrics;
- one or more categories;
- clear column names;
- at least several rows per category or date period.
- a file size of no more than 25 MB for the validated v1.0 workflow.

Examples include sales, marketing, inventory, finance and operational exports.
Sample files are available in `sample_data/` and `examples/`.

Avoid uploading confidential production data until you have reviewed the code,
your local environment and your organisation's data-handling requirements.

## Project map

```text
Universal-CSV-Dashboard/
├── app.py                  # Streamlit entry point and navigation
├── app_core/               # Detection, analysis and shared logic
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

If you want to understand application navigation first, open `app.py`.

If you want to understand the analytical behaviour, start in `app_core/`.

If you want to change a page, find the corresponding module in `views/`.

## Run the tests

From the repository root:

```bash
pytest
```

Run the tests before and after changing detection, analysis or shared
application logic.

## Common setup problems

### `streamlit` is not recognised

Confirm that the virtual environment is active, then run:

```bash
pip install -r requirements.txt
```

You can also launch Streamlit through Python:

```bash
python -m streamlit run app.py
```

### The wrong Python version is active

Check:

```bash
python --version
```

If PyCharm uses a different interpreter, select the project's `.venv`
interpreter in the Python interpreter settings.

### The CSV does not parse correctly

Check:

- delimiter and encoding;
- duplicate or empty column names;
- inconsistent date formats;
- numbers stored as text;
- completely empty rows or columns.

Try a small sample file first to determine whether the issue belongs to the
dataset or the application.

### A chart or metric is missing

Return to **Upload & Configure** and review the detected field roles. A useful
chart depends on the presence of compatible date, numeric or categorical
columns.

## Choose your next document

| Goal | Read next |
|---|---|
| Understand the product and its audience | [`PRODUCT.md`](PRODUCT.md) |
| See the current development plan | [`ROADMAP.md`](ROADMAP.md) |
| Understand product principles | [`MANIFESTO.md`](MANIFESTO.md) |
| Learn the visual system | [`docs/branding/BRAND_BOOK.md`](docs/branding/BRAND_BOOK.md) |
| Contribute code or documentation | [`CONTRIBUTING.md`](CONTRIBUTING.md) |
| Review the complete project introduction | [`README.md`](README.md) |

## Before opening an issue

Prepare:

- a clear description of the problem;
- the expected and actual behaviour;
- reproduction steps;
- your Python version and operating system;
- a minimal, non-sensitive sample CSV when possible;
- the complete error message.

Use the repository's issue templates for bug reports and feature requests.

## Before opening a pull request

1. Create a focused branch.
2. Keep the change limited to one clear purpose.
3. Add or update tests when behaviour changes.
4. Update relevant documentation.
5. Run `pytest`.
6. Review the final diff for unrelated files.

## The product principle to remember

Universal CSV Dashboard is not successful because it creates more charts.

It is successful when a person reaches a useful understanding faster.

> **Save hours. Not spreadsheets.**
