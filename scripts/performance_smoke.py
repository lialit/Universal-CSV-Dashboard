"""Measure core CSV analysis at the supported v1.0 boundary."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys
from time import perf_counter


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app_core.csv_parser import parse_csv_bytes  # noqa: E402
from app_core.quality import calculate_quality_score  # noqa: E402
from app_core.smart_detection import detect_dataset  # noqa: E402


def elapsed(start: float) -> float:
    return perf_counter() - start


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run a local performance smoke test for one CSV."
    )
    parser.add_argument("csv_path", type=Path)
    args = parser.parse_args()

    payload = args.csv_path.read_bytes()
    total_start = perf_counter()

    parse_start = perf_counter()
    dataframe = parse_csv_bytes(payload)
    parse_seconds = elapsed(parse_start)

    detection_start = perf_counter()
    detection = detect_dataset(dataframe)
    detection_seconds = elapsed(detection_start)

    quality_start = perf_counter()
    quality = calculate_quality_score(dataframe)
    quality_seconds = elapsed(quality_start)

    print(f"File: {args.csv_path.resolve()}")
    print(f"Size: {len(payload) / (1024 * 1024):.2f} MB")
    print(f"Shape: {len(dataframe):,} rows × {len(dataframe.columns)} columns")
    print(f"CSV parsing: {parse_seconds:.2f} s")
    print(f"Field detection: {detection_seconds:.2f} s")
    print(f"Quality analysis: {quality_seconds:.2f} s")
    print(f"Total core analysis: {elapsed(total_start):.2f} s")
    print(f"Detected date: {detection.date_column or 'None'}")
    print(f"Detected metric: {detection.metric_column or 'None'}")
    print(f"Quality score: {quality.score:.1f}/100 ({quality.status})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
