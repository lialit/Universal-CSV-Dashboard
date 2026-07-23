<div align="center">
  <img src="./assets/brand/logo-horizontal.svg" alt="Universal CSV Dashboard" width="560">
</div>

<br>

<div align="center">

# Understand your business in under 60 seconds.

**Upload a CSV and turn it into clear metrics, trends, data-quality checks and
interactive business views — without building a dashboard from scratch.**

[Quick start](#quick-start) · [Features](#what-you-get) ·
[How it works](#how-it-works) · [Documentation](#documentation) ·
[Roadmap](#roadmap)

</div>

![Universal CSV Dashboard hero](./assets/brand/github-hero-light.png)

## Business data is easy to export. Understanding it is not.

The usual workflow starts with a CSV and quickly turns into manual cleaning,
pivot tables, chart formatting and repeated questions about what the numbers
actually mean.

Universal CSV Dashboard shortens that path:

- upload a CSV;
- confirm the detected fields;
- explore executive metrics and trends;
- inspect data quality;
- filter the results;
- decide what to investigate next.

It is designed for analysts, consultants, small teams and business owners who
need a useful first view of a dataset without setting up a BI project.

## What you get

| | Capability | Outcome |
|---|---|---|
| 📊 | **Executive overview** | Headline KPIs and an immediate picture of the dataset |
| ✨ | **Automatic field detection** | Suggested dates, metrics and dimensions with less setup |
| 📈 | **Data analysis** | Interactive trends, categories and distributions |
| ✅ | **Data quality** | Missing values, duplicates and column-level checks |
| 🎛️ | **Useful filters** | Focus by date and detected categorical fields |
| 🔒 | **Local-first workflow** | Run the app on your own machine and keep control of the file |

## Product preview

![Executive Overview](./assets/screenshots/executive-overview.png)

The interface is intentionally calm and consistent: a focused navigation rail,
clear KPI cards, useful filters and business-readable chart titles.

## Why not start in a spreadsheet?

Spreadsheets remain excellent for direct editing and detailed ad-hoc work.
Universal CSV Dashboard is for the earlier question: **“What is in this file,
and what deserves attention?”**

| Traditional first-pass analysis | Universal CSV Dashboard |
|---|---|
| Rebuild the same pivots and charts | Reusable automatic analysis |
| Decide every field manually | Field detection with user confirmation |
| Check missing data separately | Data-quality view included |
| Format a presentation before exploring | Explore a coherent dashboard immediately |
| Easy to lose the analytical trail | Repeatable workflow for every file |

## How it works

```mermaid
flowchart LR
    A["Upload CSV"] --> B["Detect fields"]
    B --> C["Validate data"]
    C --> D["Build business views"]
    D --> E["Explore and act"]
```

The application separates data understanding from presentation. Detection and
analysis live in reusable modules; Streamlit views render the results into a
consistent interface.

## Quick start

### Requirements

- Python 3.11+
- `pip`

### Install and run

```bash
git clone https://github.com/lialit/Universal-CSV-Dashboard.git
cd Universal-CSV-Dashboard

python -m venv .venv
```

Activate the environment:

```bash
# Windows PowerShell
.\.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate
```

Install the dependencies and launch the app:

```bash
pip install -r requirements.txt
streamlit run app.py
```

Open the local address shown by Streamlit, upload a CSV, and review the detected
configuration before exploring the dashboard.

## Try these pages first

1. **Upload & Configure** — load a file and inspect the detected fields.
2. **Executive Overview** — scan the main metrics and high-level trends.
3. **Data Analysis** — explore time and category patterns.
4. **Data Quality** — check missing cells, duplicate rows and column health.

Sample files are available in `sample_data/`.

## Built for many business contexts

| Retail | Marketing | Finance | Operations |
|---|---|---|---|
| Sales and product mix | Campaign and channel results | Revenue and cost trends | Volume and service metrics |
| Inventory signals | Lead and conversion patterns | Budget monitoring | Workload patterns |

The dashboard adapts to the columns it finds rather than assuming one fixed
industry schema.

## Project structure

```text
UniversalCSVDashboard/
├── app.py                  # Streamlit entry point
├── app_core/               # Detection and analysis logic
├── views/                  # Application pages and UI composition
├── sample_data/            # Safe example datasets
├── tests/                  # Automated checks
├── assets/                 # Brand, screenshots and visual resources
├── docs/                   # Product and engineering documentation
├── examples/               # Usage examples
├── releases/               # Release notes and release assets
├── marketing/              # Reusable launch materials
├── .streamlit/             # Streamlit configuration
└── requirements.txt
```

## Product principles

**Automation first.** Detect what can be detected, then let the user confirm.

**Business first.** A chart is useful only when it helps answer a real question.

**Explain everything.** Labels and summaries should be understandable without
reading the source code.

**Beautiful by default.** A useful report should not require manual formatting.

**Privacy first.** Local use should remain a first-class way to analyse a file.

## Technology

- [Streamlit](https://streamlit.io/) for the application experience
- [Pandas](https://pandas.pydata.org/) for data processing
- [Plotly](https://plotly.com/python/) for interactive visualisation
- Python 3.11+ for the core application

## Documentation

| Document | Purpose |
|---|---|
| [`START_HERE.md`](START_HERE.md) | Guided onboarding for users and contributors |
| [`PRODUCT.md`](PRODUCT.md) | Product scope, audience and value |
| [`MANIFESTO.md`](MANIFESTO.md) | Principles that guide product decisions |
| [`ROADMAP.md`](ROADMAP.md) | Planned product stages |
| [`docs/`](docs/) | Architecture, UX, brand and product documentation |
| [`docs/branding/BRAND_BOOK.md`](docs/branding/BRAND_BOOK.md) | Visual identity and usage rules |

## Roadmap

| Stage | Goal | Status |
|---|---|---|
| **Foundation** | Reliable upload, detection and core views | Active |
| **Understand** | Stronger automated business interpretation | Planned |
| **Explain** | Clearer insight context and recommendations | Planned |
| **Share** | Reusable reports and saved analysis | Planned |
| **Launch** | Stable public release | Planned |

See [`ROADMAP.md`](ROADMAP.md) for the working plan. Roadmap items describe
direction, not guaranteed release dates.

## Contributing

Contributions and thoughtful feedback are welcome. Please read
[`CONTRIBUTING.md`](CONTRIBUTING.md) before opening a pull request.

When reporting an issue, include:

- the expected and actual behaviour;
- a minimal, non-sensitive sample CSV when possible;
- your Python version and operating system;
- the full error message.

## License

See [`LICENSE`](LICENSE) for the project licence.

## Author

Created by **Olena Havrylova**  
[GitHub profile](https://github.com/lialit)

---

<div align="center">

### Save hours. Not spreadsheets.

If the project helps you understand a dataset faster, consider giving it a star.

</div>
