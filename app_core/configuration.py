from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Mapping, Sequence

from app_core.recommendations import CHART_OPTIONS, KPI_OPTIONS


CONFIG_SCHEMA_VERSION = 1
AGGREGATION_OPTIONS = ("Sum", "Mean", "Median", "Count")


@dataclass(frozen=True)
class ConfigurationValidation:
    """Validated runtime configuration and visible compatibility messages."""

    config: dict[str, object]
    errors: tuple[str, ...]
    warnings: tuple[str, ...]

    @property
    def is_valid(self) -> bool:
        return not self.errors


def configuration_for_export(
    config: Mapping[str, object],
    source_columns: Sequence[str],
) -> dict[str, object]:
    """Add version and source schema metadata to a runtime configuration."""

    return {
        "schema_version": CONFIG_SCHEMA_VERSION,
        "source_columns": list(source_columns),
        **dict(config),
    }


def _parse_payload(
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
        return None, "The configuration file is not valid UTF-8 JSON."

    if not isinstance(parsed, dict):
        return None, "The configuration root must be a JSON object."

    return parsed, None


def validate_configuration(
    payload: bytes | str | Mapping[str, object],
    current_columns: Sequence[str],
) -> ConfigurationValidation:
    """Validate and safely adapt a saved configuration to a new CSV."""

    parsed, parse_error = _parse_payload(payload)
    if parsed is None:
        return ConfigurationValidation(
            config={},
            errors=(parse_error or "Unable to read configuration.",),
            warnings=(),
        )

    columns = list(current_columns)
    column_set = set(columns)
    errors: list[str] = []
    warnings: list[str] = []

    version = parsed.get("schema_version", 1)
    if not isinstance(version, int) or version < 1:
        errors.append("The configuration schema version is invalid.")
    elif version > CONFIG_SCHEMA_VERSION:
        errors.append(
            f"Schema version {version} is newer than the supported "
            f"version {CONFIG_SCHEMA_VERSION}."
        )

    saved_columns = parsed.get("source_columns")
    if isinstance(saved_columns, list):
        missing_saved = [
            column
            for column in saved_columns
            if isinstance(column, str) and column not in column_set
        ]
        added_current = [
            column for column in columns if column not in saved_columns
        ]
        if missing_saved or added_current:
            warnings.append(
                "The CSV schema differs from the file used to create this "
                f"configuration: {len(missing_saved)} saved columns missing "
                f"and {len(added_current)} new columns detected."
            )

    metric = parsed.get("metric_column")
    if not isinstance(metric, str) or metric not in column_set:
        errors.append(
            "The saved primary metric is not available in the current CSV."
        )

    runtime: dict[str, object] = {
        "metric_column": metric,
    }

    for key, label in (
        ("date_column", "date column"),
        ("category_column", "category column"),
    ):
        value = parsed.get(key)
        if value is None:
            runtime[key] = None
        elif isinstance(value, str) and value in column_set:
            runtime[key] = value
        else:
            runtime[key] = None
            warnings.append(
                f"The saved {label} is unavailable and will be cleared."
            )

    numeric_values = parsed.get("numeric_columns", [])
    if not isinstance(numeric_values, list):
        numeric_values = []
        warnings.append(
            "Saved numeric columns were malformed and will be rebuilt."
        )

    numeric_columns = [
        value
        for value in numeric_values
        if isinstance(value, str) and value in column_set
    ]
    if isinstance(metric, str) and metric in column_set:
        numeric_columns = list(
            dict.fromkeys([metric, *numeric_columns])
        )
    runtime["numeric_columns"] = numeric_columns

    removed_numeric = len(numeric_values) - len(
        [
            value
            for value in numeric_values
            if isinstance(value, str) and value in column_set
        ]
    )
    if removed_numeric:
        warnings.append(
            f"{removed_numeric} unavailable numeric field(s) were removed."
        )

    aggregation = parsed.get("aggregation", "Sum")
    if aggregation not in AGGREGATION_OPTIONS:
        aggregation = "Sum"
        warnings.append(
            "The saved aggregation is unsupported; Sum will be used."
        )
    runtime["aggregation"] = aggregation

    for key, allowed, label in (
        ("kpi_cards", KPI_OPTIONS, "KPI"),
        ("chart_types", CHART_OPTIONS, "chart"),
    ):
        values = parsed.get(key)
        if values is None:
            continue
        if not isinstance(values, list):
            warnings.append(
                f"Saved {label} selections were malformed and ignored."
            )
            continue
        accepted = [
            value for value in values if value in allowed
        ]
        runtime[key] = list(dict.fromkeys(accepted))
        if len(accepted) != len(values):
            warnings.append(
                f"Unsupported saved {label} selections were removed."
            )

    return ConfigurationValidation(
        config=runtime if not errors else {},
        errors=tuple(dict.fromkeys(errors)),
        warnings=tuple(dict.fromkeys(warnings)),
    )
