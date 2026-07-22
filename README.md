# Universal CSV Analytics Dashboard

A reusable Streamlit template that turns CSV data into an interactive business dashboard without code changes.

## Features
CSV upload, automatic delimiter/encoding fallback, column mapping, KPI cards, time-series analysis, category analysis, distributions, correlation matrix, data-quality report and cleaned CSV export.

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

Use `sample_data/sample_sales.csv` for a quick test.


## Smart Detection Engine

Version 0.2 automatically suggests:

- Date or timestamp column
- Primary business metric
- Category column
- Identifier columns
- Boolean columns
- Additional numeric columns

Every suggestion includes a confidence score and an explanation. Users
can accept the proposed configuration or adjust it before opening the
dashboard.

## Run tests

```bash
pytest
```
