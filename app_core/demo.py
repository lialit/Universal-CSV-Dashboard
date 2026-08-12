from pathlib import Path

from app_core.data import prepare_dataframe, read_csv_file
from app_core.recommendations import recommend_analysis


DEMO_FILE_NAME = "demo_business.csv"
DEMO_PATH = Path(__file__).resolve().parents[1] / "data" / DEMO_FILE_NAME


def load_demo_project():
    """Load the bundled synthetic dataset and build a safe default config."""
    raw_dataframe = read_csv_file(DEMO_PATH.read_bytes())
    base_config = {
        "date_column": "date",
        "metric_column": "revenue",
        "numeric_columns": ["revenue", "orders", "margin"],
        "category_column": "region",
        "aggregation": "Sum",
    }
    prepared = prepare_dataframe(
        raw_dataframe,
        date_column=base_config["date_column"],
        numeric_columns=base_config["numeric_columns"],
    )
    recommendations = recommend_analysis(prepared, base_config)
    config = {
        **base_config,
        "kpi_cards": list(recommendations.kpis),
        "chart_types": list(recommendations.charts),
    }
    return prepared, config, DEMO_FILE_NAME
