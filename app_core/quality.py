from __future__ import annotations

from dataclasses import dataclass
import math

import pandas as pd


COMPLETENESS_WEIGHT = 0.50
DUPLICATE_WEIGHT = 0.30
TYPE_VALIDITY_WEIGHT = 0.20


@dataclass(frozen=True)
class QualityCheck:
    """One transparent component of the dataset quality score."""

    name: str
    score: float
    weight: float
    issue_count: int
    explanation: str
    recommendation: str

    @property
    def weighted_points(self) -> float:
        return round(self.score * self.weight, 1)


@dataclass(frozen=True)
class DataQualityReport:
    """Complete, user-facing assessment of one dataframe."""

    score: float
    status: str
    rows: int
    columns: int
    missing_cells: int
    duplicate_rows: int
    invalid_type_cells: int
    checks: tuple[QualityCheck, ...]

    @property
    def issue_count(self) -> int:
        return (
            self.missing_cells
            + self.duplicate_rows
            + self.invalid_type_cells
        )


def _bounded_percentage(value: float) -> float:
    return round(max(0.0, min(100.0, value)), 1)


def _quality_status(score: float) -> str:
    if score >= 90:
        return "Excellent"
    if score >= 75:
        return "Good"
    if score >= 60:
        return "Needs attention"
    return "Critical"


def _invalid_type_mask(series: pd.Series) -> pd.Series:
    """Flag non-null values that conflict with a column's dtype.

    Parsed numeric columns are checked for finite values. Object columns are
    treated as mixed when a value does not match the most common Python type.
    Datetime, boolean and pandas string columns are already type-consistent.
    """

    non_null = series.dropna()
    invalid = pd.Series(False, index=series.index, dtype=bool)

    if non_null.empty:
        return invalid

    if pd.api.types.is_numeric_dtype(series):
        invalid.loc[non_null.index] = ~non_null.map(
            lambda value: math.isfinite(float(value))
        )
        return invalid

    if (
        pd.api.types.is_datetime64_any_dtype(series)
        or pd.api.types.is_bool_dtype(series)
        or isinstance(series.dtype, pd.StringDtype)
        or isinstance(series.dtype, pd.CategoricalDtype)
    ):
        return invalid

    type_counts = non_null.map(type).value_counts()
    expected_type = type_counts.index[0]
    invalid.loc[non_null.index] = ~non_null.map(
        lambda value: isinstance(value, expected_type)
    )
    return invalid


def _invalid_type_count(dataframe: pd.DataFrame) -> int:
    return sum(
        int(_invalid_type_mask(dataframe[column]).sum())
        for column in dataframe.columns
    )


def calculate_quality_score(
    dataframe: pd.DataFrame,
) -> DataQualityReport:
    """Calculate a transparent 0–100 dataset quality score.

    The score is intentionally rule-based:

    - completeness: 50%;
    - duplicate-free rows: 30%;
    - type validity: 20%.

    Every component is returned separately so the UI never presents an opaque
    number.
    """

    rows, columns = dataframe.shape
    total_cells = rows * columns
    missing_cells = int(dataframe.isna().sum().sum())
    duplicate_rows = int(dataframe.duplicated().sum())
    invalid_type_cells = _invalid_type_count(dataframe)
    non_null_cells = max(total_cells - missing_cells, 0)

    completeness_score = (
        (1 - missing_cells / total_cells) * 100
        if total_cells
        else 0.0
    )
    duplicate_score = (
        (1 - duplicate_rows / rows) * 100
        if rows
        else 0.0
    )
    type_validity_score = (
        (1 - invalid_type_cells / non_null_cells) * 100
        if non_null_cells
        else 0.0
    )

    checks = (
        QualityCheck(
            name="Completeness",
            score=_bounded_percentage(completeness_score),
            weight=COMPLETENESS_WEIGHT,
            issue_count=missing_cells,
            explanation=(
                f"{missing_cells:,} of {total_cells:,} cells are missing."
            ),
            recommendation=(
                "Review missing fields before drawing conclusions."
                if missing_cells
                else "No missing cells were detected."
            ),
        ),
        QualityCheck(
            name="Duplicate-free rows",
            score=_bounded_percentage(duplicate_score),
            weight=DUPLICATE_WEIGHT,
            issue_count=duplicate_rows,
            explanation=(
                f"{duplicate_rows:,} of {rows:,} rows are duplicates."
            ),
            recommendation=(
                "Confirm whether duplicate rows are expected before removal."
                if duplicate_rows
                else "No duplicate rows were detected."
            ),
        ),
        QualityCheck(
            name="Type validity",
            score=_bounded_percentage(type_validity_score),
            weight=TYPE_VALIDITY_WEIGHT,
            issue_count=invalid_type_cells,
            explanation=(
                f"{invalid_type_cells:,} non-null cells conflict with their "
                "column type."
            ),
            recommendation=(
                "Inspect non-finite numeric values and mixed-type columns."
                if invalid_type_cells
                else "No type-consistency issues were detected."
            ),
        ),
    )

    score = round(
        sum(check.weighted_points for check in checks),
        1,
    )

    return DataQualityReport(
        score=score,
        status=_quality_status(score),
        rows=rows,
        columns=columns,
        missing_cells=missing_cells,
        duplicate_rows=duplicate_rows,
        invalid_type_cells=invalid_type_cells,
        checks=checks,
    )


def quality_checks_table(
    report: DataQualityReport,
) -> pd.DataFrame:
    """Return the scoring formula in a display-ready table."""

    return pd.DataFrame(
        [
            {
                "Check": check.name,
                "Score": check.score,
                "Weight": check.weight,
                "Weighted points": check.weighted_points,
                "Issues": check.issue_count,
                "What was checked": check.explanation,
                "Recommended action": check.recommendation,
            }
            for check in report.checks
        ]
    )


def quality_summary(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Return column-level quality details."""

    row_count = len(dataframe)
    rows: list[dict[str, object]] = []

    for column in dataframe.columns:
        missing = int(dataframe[column].isna().sum())
        invalid = int(_invalid_type_mask(dataframe[column]).sum())
        completeness = (
            (1 - missing / row_count) * 100
            if row_count
            else 0.0
        )

        if missing == 0 and invalid == 0:
            status = "Healthy"
        elif completeness >= 90 and invalid == 0:
            status = "Review"
        else:
            status = "Needs attention"

        rows.append(
            {
                "Column": column,
                "Data type": str(dataframe[column].dtype),
                "Missing values": missing,
                "Missing %": (
                    missing / row_count * 100
                    if row_count
                    else 0.0
                ),
                "Invalid type values": invalid,
                "Unique values": int(
                    dataframe[column].nunique(dropna=True)
                ),
                "Status": status,
            }
        )

    return pd.DataFrame(rows)


def duplicate_count(dataframe: pd.DataFrame) -> int:
    """Return the number of fully duplicated rows."""

    return int(dataframe.duplicated().sum())
