import streamlit as st
from app_core.theme import render_header
render_header("About This Template","A reusable CSV analytics dashboard for freelancers and small teams.")
st.markdown("""### What this product does
- Uploads CSV files directly in the browser
- Detects common encodings and separators
- Lets users map date, metric and category columns
- Generates KPI cards and interactive Plotly charts
- Displays descriptive statistics and correlations
- Produces a column-level data-quality report
- Exports a de-duplicated CSV file

### Ideal use cases
Sales, marketing, inventory, operations, surveys, startup KPIs and fast client prototypes.

### Included technology
Python, Pandas, Plotly and Streamlit.""")
