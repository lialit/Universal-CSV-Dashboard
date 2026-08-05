from __future__ import annotations

import argparse
import re
from pathlib import Path

SEMVER_RE = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$")


def read_version() -> str:
    version = Path("VERSION").read_text(encoding="utf-8").strip()
    if not SEMVER_RE.fullmatch(version):
        raise SystemExit(f"VERSION is not valid Semantic Versioning: {version!r}")
    return version


def validate_changelog(version: str) -> None:
    changelog = Path("CHANGELOG.md").read_text(encoding="utf-8")
    if "## [Unreleased]" not in changelog:
        raise SystemExit("CHANGELOG.md must contain an [Unreleased] section.")
    if f"## [{version}]" not in changelog:
        raise SystemExit(f"CHANGELOG.md has no section for version {version}.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate release metadata.")
    parser.add_argument("--tag", help="Optional tag to validate, for example v1.0.0")
    args = parser.parse_args()

    version = read_version()
    validate_changelog(version)

    if args.tag and args.tag != f"v{version}":
        raise SystemExit(f"Tag {args.tag!r} does not match VERSION v{version}.")

    print(f"Release metadata is valid for v{version}.")


if __name__ == "__main__":
    main()
