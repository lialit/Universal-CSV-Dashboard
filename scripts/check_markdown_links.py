"""Validate repository-local links in Markdown documents."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
HTML_LINK = re.compile(r"(?:href|src)=[\"']([^\"']+)[\"']", re.IGNORECASE)
IGNORED_PREFIXES = ("http://", "https://", "mailto:", "tel:", "data:", "#")
IGNORED_DIRS = {".git", ".venv", "venv", "node_modules", ".pytest_cache"}


def markdown_files() -> list[Path]:
    return sorted(
        path
        for path in ROOT.rglob("*.md")
        if not any(part in IGNORED_DIRS for part in path.parts)
    )


def extract_targets(text: str) -> list[str]:
    targets = [match.group(1).strip() for match in MARKDOWN_LINK.finditer(text)]
    targets.extend(match.group(1).strip() for match in HTML_LINK.finditer(text))
    return targets


def normalize_target(raw_target: str) -> str | None:
    target = raw_target.strip().strip("<>")
    if not target or target.startswith(IGNORED_PREFIXES):
        return None

    # Markdown titles may follow a quoted path: (path "title").
    if " \"" in target:
        target = target.split(" \"", 1)[0]
    elif " '" in target:
        target = target.split(" '", 1)[0]

    parsed = urlsplit(target)
    path = unquote(parsed.path)
    if not path or "${{" in path or "{{" in path:
        return None
    return path


def resolve(source: Path, target: str) -> Path:
    if target.startswith("/"):
        return ROOT / target.lstrip("/")
    return source.parent / target


def main() -> int:
    failures: list[str] = []
    checked = 0

    for source in markdown_files():
        text = source.read_text(encoding="utf-8")
        for raw_target in extract_targets(text):
            target = normalize_target(raw_target)
            if target is None:
                continue
            checked += 1
            destination = resolve(source, target)
            if not destination.exists():
                failures.append(
                    f"{source.relative_to(ROOT)} -> {raw_target} "
                    f"(missing: {destination.resolve()})"
                )

    if failures:
        print("Broken repository-local Markdown links:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    print(f"Markdown link check passed: {checked} local targets validated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
