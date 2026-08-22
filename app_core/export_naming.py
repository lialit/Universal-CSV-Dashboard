from __future__ import annotations

from pathlib import PurePath
import re


_INVALID_FILENAME_CHARS = re.compile(r"[<>:\"/\\|?*\x00-\x1f]+")
_WHITESPACE = re.compile(r"\s+")


def safe_export_stem(source_name: str) -> str:
    """Return a deterministic, filesystem-safe stem for generated exports."""
    base = PurePath(str(source_name).replace("\\", "/")).name
    stem = base.rsplit(".", 1)[0] if "." in base else base
    stem = _INVALID_FILENAME_CHARS.sub("_", stem)
    stem = _WHITESPACE.sub("_", stem).strip(" ._")
    return stem[:80] or "dashboard"


def export_filename(source_name: str, suffix: str, extension: str) -> str:
    """Build a safe deterministic export filename from the source name."""
    clean_suffix = suffix.strip(" _.")
    clean_extension = extension.lstrip(".")
    return f"{safe_export_stem(source_name)}_{clean_suffix}.{clean_extension}"
