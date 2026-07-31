"""Framework-independent CSV parsing and upload-size validation."""

from io import BytesIO

import pandas as pd


MAX_UPLOAD_SIZE_MB = 25
MAX_UPLOAD_SIZE_BYTES = MAX_UPLOAD_SIZE_MB * 1024 * 1024


def validate_upload_size(
    file_bytes: bytes,
    max_size_bytes: int = MAX_UPLOAD_SIZE_BYTES,
) -> None:
    """Reject a CSV payload above the supported in-memory boundary."""
    if max_size_bytes <= 0:
        raise ValueError("The maximum upload size must be positive.")

    file_size = len(file_bytes)
    if file_size <= max_size_bytes:
        return

    size_mb = file_size / (1024 * 1024)
    limit_mb = max_size_bytes / (1024 * 1024)
    raise ValueError(
        f"The CSV is {size_mb:.1f} MB. The maximum supported size is "
        f"{limit_mb:g} MB. Reduce or split the file before uploading."
    )


def parse_csv_bytes(file_bytes: bytes) -> pd.DataFrame:
    """Read a supported CSV payload using common encodings and delimiters."""
    validate_upload_size(file_bytes)

    for encoding in ("utf-8", "utf-8-sig", "cp1252", "latin-1"):
        for separator in (",", ";", "\t"):
            try:
                dataframe = pd.read_csv(
                    BytesIO(file_bytes),
                    encoding=encoding,
                    sep=separator,
                )
                if dataframe.shape[1] > 1:
                    return dataframe
            except Exception:
                continue

    raise ValueError(
        "The CSV could not be read with the supported encoding and "
        "separator combinations."
    )
