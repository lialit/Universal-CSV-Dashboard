from pathlib import Path

import pytest

from app_core.csv_parser import parse_csv_bytes
from app_core.smart_detection import detect_dataset


EXAMPLE_FILES = (
    *sorted(Path("examples").glob("*.csv")),
    *sorted(Path("examples").glob("*/sample.csv")),
)


@pytest.mark.parametrize("path", EXAMPLE_FILES, ids=str)
def test_public_example_supports_primary_workflow(path: Path) -> None:
    dataframe = parse_csv_bytes(path.read_bytes())
    detection = detect_dataset(dataframe)

    assert len(dataframe) >= 5
    assert detection.date_column is not None
    assert detection.metric_column is not None
    assert detection.category_column is not None
