import pandas as pd
import pytest

from app_core.csv_parser import (
    MAX_UPLOAD_SIZE_BYTES,
    MAX_UPLOAD_SIZE_MB,
    parse_csv_bytes,
    validate_upload_size,
)
from app_core.data import prepare_dataframe


def test_supported_upload_boundary_is_25_mb() -> None:
    assert MAX_UPLOAD_SIZE_MB == 25
    assert MAX_UPLOAD_SIZE_BYTES == 25 * 1024 * 1024


def test_upload_size_accepts_exact_boundary() -> None:
    validate_upload_size(b"1234", max_size_bytes=4)


def test_upload_size_rejects_payload_above_boundary() -> None:
    with pytest.raises(ValueError, match="maximum supported size is 4 MB"):
        validate_upload_size(
            b"x" * (4 * 1024 * 1024 + 1),
            max_size_bytes=4 * 1024 * 1024,
        )


def test_read_csv_file_reads_supported_csv() -> None:
    dataframe = parse_csv_bytes(b"date,sales\n2026-01-01,10\n")

    assert dataframe.to_dict(orient="records") == [
        {"date": "2026-01-01", "sales": 10}
    ]


def test_prepare_dataframe_applies_confirmed_roles() -> None:
    dataframe = pd.DataFrame(
        {
            "date": ["2026-01-01"],
            "sales": ["10"],
            "region": ["North"],
        }
    )

    prepared = prepare_dataframe(dataframe, "date", ["sales"])

    assert pd.api.types.is_datetime64_any_dtype(prepared["date"])
    assert pd.api.types.is_numeric_dtype(prepared["sales"])
