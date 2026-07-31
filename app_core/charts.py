"""Plotly chart builders with bounded browser-side payloads."""

import pandas as pd
import plotly.express as px


MAX_VISUAL_ROWS = 50_000
AGGREGATION_FUNCTIONS = {
    "Sum": "sum",
    "Mean": "mean",
    "Median": "median",
    "Count": "count",
}


def layout(figure, height: int = 380):
    figure.update_layout(
        height=height,
        margin=dict(l=20, r=20, t=60, b=20),
        paper_bgcolor="#FFF",
        plot_bgcolor="#FFF",
        font=dict(
            family="Inter, Arial, sans-serif",
            color="#334155",
        ),
        title_font=dict(size=17, color="#102348"),
        legend_title_text="",
        hoverlabel=dict(bgcolor="#FFF"),
    )
    figure.update_xaxes(gridcolor="#E8EDF4", zeroline=False)
    figure.update_yaxes(gridcolor="#E8EDF4", zeroline=False)
    return figure


def time_series_chart(
    dataframe,
    date_column,
    metric_column,
    aggregation,
):
    function = AGGREGATION_FUNCTIONS[aggregation]
    grouped = (
        dataframe.dropna(subset=[date_column])
        .set_index(date_column)
        .resample("D")[metric_column]
        .agg(function)
        .reset_index()
    )
    figure = px.line(
        grouped,
        x=date_column,
        y=metric_column,
        title=f"{aggregation} of {metric_column} over time",
    )
    figure.update_traces(line=dict(width=2.5), fill="tozeroy")
    return layout(figure)


def category_chart(
    dataframe,
    category_column,
    metric_column,
    aggregation,
    limit=15,
):
    function = AGGREGATION_FUNCTIONS[aggregation]
    grouped = (
        dataframe.groupby(
            category_column,
            dropna=False,
            as_index=False,
        )[metric_column]
        .agg(function)
        .nlargest(limit, metric_column)
        .sort_values(metric_column)
    )
    grouped[category_column] = (
        grouped[category_column]
        .astype("string")
        .fillna("Missing")
    )
    figure = px.bar(
        grouped,
        x=metric_column,
        y=category_column,
        orientation="h",
        title=(
            f"Top {limit} {category_column} values by "
            f"{aggregation.lower()} {metric_column}"
        ),
    )
    return layout(figure)


def visualization_sample(
    dataframe: pd.DataFrame,
    max_rows: int = MAX_VISUAL_ROWS,
) -> tuple[pd.DataFrame, bool]:
    """Return a deterministic evenly spaced sample for browser rendering."""
    if max_rows <= 0:
        raise ValueError("max_rows must be positive.")
    if len(dataframe) <= max_rows:
        return dataframe, False

    if max_rows == 1:
        return dataframe.iloc[[0]], True

    positions = (
        pd.Series(range(max_rows), dtype="int64")
        .mul(len(dataframe) - 1)
        .floordiv(max_rows - 1)
        .astype("int64")
        .tolist()
    )
    return dataframe.iloc[positions], True


def distribution_chart(dataframe, metric_column):
    chart_data, sampled = visualization_sample(
        dataframe[[metric_column]].dropna(),
    )
    title = f"Distribution of {metric_column}"
    if sampled:
        title += (
            f" (visual sample: {len(chart_data):,} of "
            f"{dataframe[metric_column].notna().sum():,} values)"
        )
    figure = px.histogram(
        chart_data,
        x=metric_column,
        nbins=35,
        marginal="box",
        title=title,
    )
    return layout(figure)


def missing_values_chart(dataframe):
    grouped = (
        dataframe.isna()
        .mean()
        .mul(100)
        .sort_values(ascending=False)
        .rename("missing_pct")
        .reset_index()
        .rename(columns={"index": "column"})
    )
    figure = px.bar(
        grouped,
        x="missing_pct",
        y="column",
        orientation="h",
        title="Missing values by column",
        labels={"missing_pct": "Missing (%)"},
    )
    return layout(figure, max(380, len(grouped) * 28))


def correlation_chart(dataframe, numeric_columns):
    correlation = (
        dataframe[numeric_columns]
        .apply(pd.to_numeric, errors="coerce")
        .corr()
    )
    figure = px.imshow(
        correlation,
        text_auto=".2f",
        aspect="auto",
        title="Numeric correlation matrix",
        color_continuous_scale="RdBu_r",
        zmin=-1,
        zmax=1,
    )
    return layout(figure, max(420, len(numeric_columns) * 60))
