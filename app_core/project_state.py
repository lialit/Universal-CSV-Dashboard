from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Mapping

import pandas as pd

from app_core.configuration import (
    ConfigurationValidation,
    configuration_for_export,
    validate_configuration,
)


PROJECT_FORMAT = "universal_csv_dashboard_project"
PROJECT_SCHEMA_VERSION = 1
PRODUCT_VERSION = "0.5-dev"


@dataclass(frozen=True)
class ProjectValidation:
    """Validated project metadata and runtime configuration."""

    config: dict[str, object]
    metadata: dict[str, object]
    errors: tuple[str, ...]
    warnings: tuple[str, ...]

    @property
    def is_valid(self) -> bool:
        return not self.errors


def _safe_project_name(source_name: str) -> str:
    stem = Path(source_name).stem.strip()
    return stem or "Untitled analysis"


def build_project_state(
    dataframe: pd.DataFrame,
    config: Mapping[str, object],
    source_name: str = "uploaded.csv",
) -> dict[str, object]:
    """Build a portable project description without storing row-level data."""

    columns = [str(column) for column in dataframe.columns]
    column_types = {
        str(column): str(dtype)
        for column, dtype in dataframe.dtypes.items()
    }
    return {
        "format": PROJECT_FORMAT,
        "schema_version": PROJECT_SCHEMA_VERSION,
        "product_version": PRODUCT_VERSION,
        "created_at_utc": datetime.now(timezone.utc).isoformat(
            timespec="seconds"
        ),
        "project_name": _safe_project_name(source_name),
        "source": {
            "file_name": source_name,
            "row_count": len(dataframe),
            "column_count": len(columns),
            "columns": columns,
            "column_types": column_types,
        },
        "configuration": configuration_for_export(
            config,
            columns,
        ),
        "privacy": {
            "contains_raw_data": False,
            "note": (
                "This project file stores configuration and schema metadata "
                "only. Reopen it with the source CSV."
            ),
        },
    }


def project_state_to_json(
    dataframe: pd.DataFrame,
    config: Mapping[str, object],
    source_name: str = "uploaded.csv",
) -> str:
    """Serialize a saved project with stable, human-readable formatting."""

    return json.dumps(
        build_project_state(dataframe, config, source_name),
        ensure_ascii=False,
        indent=2,
    )


def _parse_project(
    payload: bytes | str | Mapping[str, object],
) -> tuple[dict[str, object] | None, str | None]:
    if isinstance(payload, Mapping):
        return dict(payload), None

    try:
        text = (
            payload.decode("utf-8-sig")
            if isinstance(payload, bytes)
            else payload
        )
        parsed = json.loads(text)
    except (UnicodeDecodeError, json.JSONDecodeError, TypeError):
        return None, "The project file is not valid UTF-8 JSON."

    if not isinstance(parsed, dict):
        return None, "The project root must be a JSON object."

    return parsed, None


def is_project_state(
    payload: bytes | str | Mapping[str, object],
) -> bool:
    """Return whether a JSON payload identifies itself as a saved project."""

    parsed, _ = _parse_project(payload)
    return bool(parsed and parsed.get("format") == PROJECT_FORMAT)


def _empty_validation(error: str) -> ProjectValidation:
    return ProjectValidation(
        config={},
        metadata={},
        errors=(error,),
        warnings=(),
    )


def _merge_configuration_result(
    result: ConfigurationValidation,
    metadata: dict[str, object],
    errors: list[str],
    warnings: list[str],
) -> ProjectValidation:
    errors.extend(result.errors)
    warnings.extend(result.warnings)
    return ProjectValidation(
        config=result.config if not errors else {},
        metadata=metadata if not errors else {},
        errors=tuple(dict.fromkeys(errors)),
        warnings=tuple(dict.fromkeys(warnings)),
    )


def validate_project_state(
    payload: bytes | str | Mapping[str, object],
    dataframe: pd.DataFrame,
    current_source_name: str = "uploaded.csv",
) -> ProjectValidation:
    """Validate a saved project against the currently uploaded CSV."""

    parsed, parse_error = _parse_project(payload)
    if parsed is None:
        return _empty_validation(
            parse_error or "Unable to read the project file."
        )

    errors: list[str] = []
    warnings: list[str] = []

    if parsed.get("format") != PROJECT_FORMAT:
        return _empty_validation(
            "This JSON file is not a Universal CSV Dashboard project."
        )

    version = parsed.get("schema_version")
    if not isinstance(version, int) or version < 1:
        errors.append("The project schema version is invalid.")
    elif version > PROJECT_SCHEMA_VERSION:
        errors.append(
            f"Project schema version {version} is newer than the supported "
            f"version {PROJECT_SCHEMA_VERSION}."
        )

    source = parsed.get("source")
    if not isinstance(source, Mapping):
        errors.append("The project source metadata is missing or malformed.")
        source = {}

    configuration = parsed.get("configuration")
    if not isinstance(configuration, Mapping):
        errors.append(
            "The project configuration is missing or malformed."
        )
        configuration = {}

    current_columns = [str(column) for column in dataframe.columns]
    saved_name = source.get("file_name")
    if (
        isinstance(saved_name, str)
        and saved_name != current_source_name
    ):
        warnings.append(
            f"The project was created for '{saved_name}', but the current "
            f"file is '{current_source_name}'."
        )

    saved_rows = source.get("row_count")
    if isinstance(saved_rows, int) and saved_rows != len(dataframe):
        warnings.append(
            f"The row count changed from {saved_rows:,} to "
            f"{len(dataframe):,}."
        )

    saved_types = source.get("column_types")
    if isinstance(saved_types, Mapping):
        changed_types = [
            column
            for column, dtype in dataframe.dtypes.items()
            if (
                str(column) in saved_types
                and str(saved_types[str(column)]) != str(dtype)
            )
        ]
        if changed_types:
            warnings.append(
                f"{len(changed_types)} column type(s) changed since the "
                "project was saved."
            )

    config_result = validate_configuration(
        configuration,
        current_columns,
    )
    metadata = {
        "project_name": parsed.get("project_name", "Untitled analysis"),
        "created_at_utc": parsed.get("created_at_utc"),
        "product_version": parsed.get("product_version"),
        "saved_source_name": saved_name,
        "current_source_name": current_source_name,
    }
    return _merge_configuration_result(
        config_result,
        metadata,
        errors,
        warnings,
    )
