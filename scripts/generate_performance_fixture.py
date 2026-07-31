"""Generate a safe synthetic CSV close to the supported upload boundary."""

from __future__ import annotations

import argparse
from datetime import date, timedelta
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app_core.csv_parser import MAX_UPLOAD_SIZE_MB  # noqa: E402


HEADER = "date,region,product,sales,orders,marketing_spend\n"
REGIONS = ("North", "South", "East", "West")
PRODUCTS = ("Alpha", "Beta", "Gamma", "Delta")


def generate_fixture(output: Path, target_mb: float) -> tuple[int, int]:
    """Write deterministic rows until the fixture reaches the target size."""
    target_bytes = int(target_mb * 1024 * 1024)
    rows = 0
    start_date = date(2024, 1, 1)

    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="") as csv_file:
        csv_file.write(HEADER)
        while csv_file.tell() < target_bytes:
            current_date = start_date + timedelta(days=rows % 730)
            region = REGIONS[rows % len(REGIONS)]
            product = PRODUCTS[(rows // len(REGIONS)) % len(PRODUCTS)]
            sales = 800 + rows % 2400
            orders = 10 + rows % 90
            marketing_spend = 50 + rows % 450
            csv_file.write(
                f"{current_date.isoformat()},{region},{product},"
                f"{sales},{orders},{marketing_spend}\n"
            )
            rows += 1

    return rows, output.stat().st_size


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a synthetic CSV for the v1.0 performance check."
    )
    parser.add_argument(
        "--target-mb",
        type=float,
        default=float(MAX_UPLOAD_SIZE_MB - 1),
        help="Target size below the supported upload limit (default: 24).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("performance_sample_24mb.csv"),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not 0 < args.target_mb < MAX_UPLOAD_SIZE_MB:
        raise SystemExit(
            f"--target-mb must be greater than 0 and below "
            f"{MAX_UPLOAD_SIZE_MB} MB."
        )

    rows, size_bytes = generate_fixture(args.output, args.target_mb)
    print(f"Created: {args.output.resolve()}")
    print(f"Rows: {rows:,}")
    print(f"Size: {size_bytes / (1024 * 1024):.2f} MB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
