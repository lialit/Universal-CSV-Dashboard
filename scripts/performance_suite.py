"""Run repeatable small, medium, and large synthetic performance checks."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
from time import perf_counter


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app_core.csv_parser import MAX_UPLOAD_SIZE_MB, parse_csv_bytes  # noqa: E402
from app_core.quality import calculate_quality_score  # noqa: E402
from app_core.smart_detection import detect_dataset  # noqa: E402
from scripts.generate_performance_fixture import generate_fixture  # noqa: E402


DEFAULT_PROFILES = {
    "small": 1.0,
    "medium": 10.0,
    "large": float(MAX_UPLOAD_SIZE_MB - 1),
}


def _seconds(start: float) -> float:
    return round(perf_counter() - start, 4)


def measure_fixture(path: Path, profile: str) -> dict[str, object]:
    """Measure the deterministic core analysis path for one fixture."""
    payload = path.read_bytes()
    total_start = perf_counter()

    parse_start = perf_counter()
    dataframe = parse_csv_bytes(payload)
    parse_seconds = _seconds(parse_start)

    detection_start = perf_counter()
    detection = detect_dataset(dataframe)
    detection_seconds = _seconds(detection_start)

    quality_start = perf_counter()
    quality = calculate_quality_score(dataframe)
    quality_seconds = _seconds(quality_start)

    return {
        "profile": profile,
        "size_mb": round(len(payload) / (1024 * 1024), 3),
        "rows": len(dataframe),
        "columns": len(dataframe.columns),
        "parse_seconds": parse_seconds,
        "detection_seconds": detection_seconds,
        "quality_seconds": quality_seconds,
        "total_seconds": _seconds(total_start),
        "detected_date": detection.date_column,
        "detected_metric": detection.metric_column,
        "detected_category": detection.category_column,
        "quality_score": round(float(quality.score), 2),
        "quality_status": quality.status,
    }


def run_suite(profiles: dict[str, float] | None = None) -> list[dict[str, object]]:
    """Generate temporary synthetic fixtures and return performance reports."""
    selected = profiles or DEFAULT_PROFILES
    reports: list[dict[str, object]] = []

    with TemporaryDirectory(prefix="csv-dashboard-perf-") as directory:
        root = Path(directory)
        for name, target_mb in selected.items():
            if not 0 < target_mb < MAX_UPLOAD_SIZE_MB:
                raise ValueError(
                    f"Profile {name!r} must be greater than 0 and below "
                    f"{MAX_UPLOAD_SIZE_MB} MB."
                )
            path = root / f"{name}.csv"
            generate_fixture(path, target_mb)
            reports.append(measure_fixture(path, name))

    return reports


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Generate synthetic small/medium/large CSV fixtures and measure "
            "the core analysis path."
        )
    )
    parser.add_argument(
        "--json-output",
        type=Path,
        help="Optional path for a machine-readable JSON baseline report.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    reports = run_suite()

    print("Universal CSV Dashboard performance suite")
    for report in reports:
        print(
            f"{report['profile']:>6}: {report['size_mb']:>6.2f} MB | "
            f"{report['rows']:>8,} rows | total {report['total_seconds']:.2f} s "
            f"(parse {report['parse_seconds']:.2f}, "
            f"detect {report['detection_seconds']:.2f}, "
            f"quality {report['quality_seconds']:.2f})"
        )

    if args.json_output:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(
            json.dumps(reports, indent=2),
            encoding="utf-8",
        )
        print(f"JSON report: {args.json_output.resolve()}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
