from app_core.demo import DEMO_FILE_NAME, load_demo_project


def test_bundled_demo_builds_ready_project() -> None:
    dataframe, config, file_name = load_demo_project()

    assert file_name == DEMO_FILE_NAME
    assert len(dataframe) >= 30
    assert config["date_column"] == "date"
    assert config["metric_column"] == "revenue"
    assert config["category_column"] == "region"
    assert config["aggregation"] == "Sum"
    assert config["numeric_columns"] == ["revenue", "orders", "margin"]
    assert config["kpi_cards"]
    assert config["chart_types"]
    assert dataframe["date"].notna().all()
    assert dataframe[["revenue", "orders", "margin"]].notna().all().all()


def test_bundled_demo_contains_only_expected_synthetic_fields() -> None:
    dataframe, _, _ = load_demo_project()

    assert list(dataframe.columns) == [
        "date",
        "region",
        "channel",
        "revenue",
        "orders",
        "margin",
    ]
    assert set(dataframe["region"]) == {"North", "South", "West"}
    assert set(dataframe["channel"]) == {"Online", "Retail", "Partner"}
