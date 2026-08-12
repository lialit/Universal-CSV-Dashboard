from scripts.performance_suite import run_suite


def test_performance_suite_reports_core_results() -> None:
    reports = run_suite({"tiny": 0.01})

    assert len(reports) == 1
    report = reports[0]
    assert report["profile"] == "tiny"
    assert report["size_mb"] > 0
    assert report["rows"] >= 5
    assert report["columns"] == 6
    assert report["parse_seconds"] >= 0
    assert report["detection_seconds"] >= 0
    assert report["quality_seconds"] >= 0
    assert report["total_seconds"] >= 0
    assert report["detected_date"] == "date"
    assert report["detected_metric"] == "sales"
    assert report["detected_category"] in {"region", "product"}
    assert 0 <= report["quality_score"] <= 100
    assert report["quality_status"]
