import pandas as pd

from app_core.executive_summary import (
    build_executive_summary,
)


def sample_dataframe() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "date": pd.date_range(
                "2026-01-01",
                periods=10,
                freq="D",
            ),
            "region": [
                "North",
                "North",
                "North",
                "North",
                "North",
                "North",
                "South",
                "South",
                "West",
                "West",
            ],
            "sales": [
                10,
                12,
                11,
                13,
                15,
                18,
                20,
                25,
                60,
                100,
            ],
        }
    )


def sample_config() -> dict[str, object]:
    return {
        "date_column": "date",
        "metric_column": "sales",
        "category_column": "region",
        "aggregation": "Sum",
    }


def test_summary_contains_verified_dataset_facts() -> None:
    summary = build_executive_summary(
        sample_dataframe(),
        sample_config(),
    )
    titles = {statement.title for statement in summary.facts}

    assert "Dataset structure" in titles
    assert "Technical quality" in titles
    assert "Primary metric" in titles
    assert "Date coverage" in titles
    assert "Category coverage" in titles
    assert "10 rows" in summary.headline


def test_interpretations_are_evidence_linked() -> None:
    summary = build_executive_summary(
        sample_dataframe(),
        sample_config(),
    )

    assert summary.interpretations
    assert all(
        statement.evidence
        for statement in summary.interpretations
    )


def test_missing_dimensions_are_reported_as_limitations() -> None:
    config = {
        "metric_column": "sales",
        "date_column": None,
        "category_column": None,
    }
    summary = build_executive_summary(
        sample_dataframe(),
        config,
    )
    titles = {
        statement.title
        for statement in summary.limitations
    }

    assert "No date dimension" in titles
    assert "No category dimension" in titles


def test_missing_metric_values_are_disclosed() -> None:
    dataframe = sample_dataframe()
    dataframe.loc[:6, "sales"] = None

    summary = build_executive_summary(
        dataframe,
        sample_config(),
    )
    titles = {
        statement.title
        for statement in summary.limitations
    }

    assert "Incomplete primary metric" in titles
    assert "Data quality requires review" in titles


def test_invalid_metric_configuration_fails_safely() -> None:
    config = {
        "metric_column": "missing_column",
        "date_column": "date",
        "category_column": "region",
    }

    summary = build_executive_summary(
        sample_dataframe(),
        config,
    )

    assert not summary.interpretations
    assert summary.limitations[0].title == (
        "Primary metric unavailable"
    )
    assert summary.next_steps == (
        "Return to Upload & Configure and select a primary metric.",
    )


def test_small_sample_is_disclosed() -> None:
    summary = build_executive_summary(
        sample_dataframe(),
        sample_config(),
    )

    assert any(
        statement.title == "Small sample"
        for statement in summary.limitations
    )


def test_summary_is_deterministic() -> None:
    first = build_executive_summary(
        sample_dataframe(),
        sample_config(),
    )
    second = build_executive_summary(
        sample_dataframe(),
        sample_config(),
    )

    assert first == second
