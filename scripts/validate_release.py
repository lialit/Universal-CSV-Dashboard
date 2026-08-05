from __future__ import annotations

import argparse
import re
from pathlib import Path

SEMVER_RE = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$"
)
SMOKE_TAG_RE = re.compile(r"^v(?P<version>.+)-smoke\.(?P<number>[1-9]\d*)$")


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


def validate_tag(tag: str, version: str, allow_smoke_tag: bool) -> None:
    expected_tag = f"v{version}"
    if tag == expected_tag:
        return

    smoke_match = SMOKE_TAG_RE.fullmatch(tag)
    if allow_smoke_tag and smoke_match and smoke_match.group("version") == version:
        return

    suffix = f" or {expected_tag}-smoke.N" if allow_smoke_tag else ""
    raise SystemExit(
        f"Tag {tag!r} does not match VERSION {expected_tag}{suffix}."
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate release metadata.")
    parser.add_argument("--tag", help="Optional tag to validate, for example v1.0.0")
    parser.add_argument(
        "--allow-smoke-tag",
        action="store_true",
        help="Allow a non-publishable v<VERSION>-smoke.N draft tag.",
    )
    args = parser.parse_args()

    version = read_version()
    validate_changelog(version)

    if args.tag:
        validate_tag(args.tag, version, args.allow_smoke_tag)

    print(f"Release metadata is valid for v{version}.")


if __name__ == "__main__":
    main()
