"""Cached CSV loading and dataframe preparation for the Streamlit UI."""

import pandas as pd
import streamlit as st

from app_core.csv_parser import parse_csv_bytes


@st.cache_data(show_spinner="Reading CSV...")
def read_csv_file(file_bytes: bytes) -> pd.DataFrame:
    """Cache the framework-independent parser for interactive reruns."""
    return parse_csv_bytes(file_bytes)


def prepare_dataframe(
    dataframe: pd.DataFrame,
    date_column: str | None,
    numeric_columns: list[str],
) -> pd.DataFrame:
    """Apply confirmed date and numeric roles to a dataframe copy."""
    result = dataframe.copy()
    if date_column:
        result[date_column] = pd.to_datetime(
            result[date_column],
            errors="coerce",
        )
    for column in numeric_columns:
        result[column] = pd.to_numeric(
            result[column],
            errors="coerce",
        )
    return result.convert_dtypes()
