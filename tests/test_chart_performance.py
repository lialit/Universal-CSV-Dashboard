import pandas as pd
import pytest

from app_core.charts import (
    MAX_VISUAL_ROWS,
    distribution_chart,
    visualization_sample,
)


def test_small_visualization_uses_every_row() -> None:
    dataframe = pd.DataFrame({"sales": range(10)})

    sampled, was_sampled = visualization_sample(dataframe)

    assert sampled.equals(dataframe)
    assert was_sampled is False


def test_large_visualization_uses_deterministic_limit() -> None:
    dataframe = pd.DataFrame({"sales": range(MAX_VISUAL_ROWS + 100)})

    first, first_sampled = visualization_sample(dataframe)
    second, second_sampled = visualization_sample(dataframe)

    assert len(first) == MAX_VISUAL_ROWS
    assert first.equals(second)
    assert first_sampled is second_sampled is True
    assert first.iloc[0, 0] == dataframe.iloc[0, 0]
    assert first.iloc[-1, 0] == dataframe.iloc[-1, 0]


def test_distribution_title_discloses_visual_sample() -> None:
    dataframe = pd.DataFrame({"sales": range(MAX_VISUAL_ROWS + 100)})

    figure = distribution_chart(dataframe, "sales")

    assert "visual sample" in figure.layout.title.text
    assert f"{MAX_VISUAL_ROWS:,}" in figure.layout.title.text


def test_visualization_limit_must_be_positive() -> None:
    with pytest.raises(ValueError, match="positive"):
        visualization_sample(pd.DataFrame({"sales": [1]}), max_rows=0)


def test_single_row_visualization_limit_is_supported() -> None:
    dataframe = pd.DataFrame({"sales": [10, 20]})

    sampled, was_sampled = visualization_sample(dataframe, max_rows=1)

    assert sampled["sales"].tolist() == [10]
    assert was_sampled is True
