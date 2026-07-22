from __future__ import annotations

from dataclasses import asdict, dataclass
import re
from typing import Literal

import pandas as pd


ColumnRole = Literal[
    "date",
    "metric",
    "category",
    "identifier",
    "boolean",
    "text",
    "numeric",
    "unknown",
]


DATE_TERMS = {
    "date": 1.00,
    "datetime": 1.00,
    "timestamp": 1.00,
    "created_at": 0.98,
    "updated_at": 0.95,
    "order_date": 0.98,
    "invoice_date": 0.98,
    "purchase_date": 0.98,
    "transaction_date": 0.97,
    "event_date": 0.95,
    "time": 0.82,
}

METRIC_TERMS = {
    "sales": 1.00,
    "revenue": 1.00,
    "profit": 0.98,
    "amount": 0.94,
    "gmv": 0.96,
    "turnover": 0.94,
    "income": 0.92,
    "cost": 0.90,
    "expense": 0.90,
    "expenses": 0.90,
    "price": 0.86,
    "quantity": 0.90,
    "qty": 0.90,
    "orders": 0.92,
    "units": 0.88,
    "spend": 0.88,
    "marketing_spend": 0.94,
    "clicks": 0.84,
    "visits": 0.82,
    "margin": 0.90,
}

CATEGORY_TERMS = {
    "category": 1.00,
    "product": 0.98,
    "product_name": 1.00,
    "region": 0.98,
    "country": 0.96,
    "city": 0.94,
    "store": 0.96,
    "segment": 0.96,
    "channel": 0.94,
    "department": 0.94,
    "brand": 0.96,
    "campaign": 0.92,
    "status": 0.86,
    "type": 0.80,
}

ID_TERMS = {
    "id": 1.00,
    "uuid": 1.00,
    "customer_id": 1.00,
    "order_id": 1.00,
    "product_id": 1.00,
    "store_id": 1.00,
    "user_id": 1.00,
    "transaction_id": 1.00,
    "invoice_id": 1.00,
}

BOOLEAN_TERMS = {
    "is_active": 1.00,
    "is_promo": 1.00,
    "promo": 0.94,
    "promotion": 0.90,
    "returned": 0.92,
    "cancelled": 0.92,
    "canceled": 0.92,
    "stockout": 0.94,
    "is_stockout": 1.00,
    "flag": 0.84,
}

TEXT_TERMS = {
    "description": 1.00,
    "comment": 0.98,
    "comments": 0.98,
    "review": 0.96,
    "notes": 0.96,
    "note": 0.96,
    "message": 0.92,
    "feedback": 0.94,
}


@dataclass(frozen=True)
class ColumnDetection:
    column: str
    role: ColumnRole
    confidence: float
    reason: str

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True)
class DatasetDetection:
    date_column: str | None
    metric_column: str | None
    category_column: str | None
    identifier_columns: tuple[str, ...]
    boolean_columns: tuple[str, ...]
    numeric_columns: tuple[str, ...]
    detections: tuple[ColumnDetection, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "date_column": self.date_column,
            "metric_column": self.metric_column,
            "category_column": self.category_column,
            "identifier_columns": list(self.identifier_columns),
            "boolean_columns": list(self.boolean_columns),
            "numeric_columns": list(self.numeric_columns),
            "detections": [
                detection.to_dict()
                for detection in self.detections
            ],
        }


def normalize_name(name: str) -> str:
    """Convert a column name to a normalized snake-like token."""
    normalized = re.sub(
        r"[^a-zA-Z0-9]+",
        "_",
        str(name).strip().lower(),
    )
    return normalized.strip("_")


def _name_score(
    normalized_name: str,
    terms: dict[str, float],
) -> tuple[float, str]:
    if normalized_name in terms:
        return terms[normalized_name], (
            f"column name matches '{normalized_name}'"
        )

    tokens = set(normalized_name.split("_"))
    best_score = 0.0
    best_term = ""

    for term, score in terms.items():
        term_tokens = set(term.split("_"))

        if term_tokens.issubset(tokens):
            adjusted = score * 0.92
            if adjusted > best_score:
                best_score = adjusted
                best_term = term

        elif term in normalized_name:
            adjusted = score * 0.84
            if adjusted > best_score:
                best_score = adjusted
                best_term = term

    if best_score:
        return best_score, (
            f"column name contains '{best_term}'"
        )

    return 0.0, ""


def _date_parse_ratio(series: pd.Series) -> float:
    sample = series.dropna().head(500)

    if sample.empty:
        return 0.0

    if pd.api.types.is_datetime64_any_dtype(sample):
        return 1.0

    import warnings

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        parsed = pd.to_datetime(
            sample,
            errors="coerce",
        )
        
    return float(parsed.notna().mean())


def _numeric_parse_ratio(series: pd.Series) -> float:
    sample = series.dropna().head(1000)

    if sample.empty:
        return 0.0

    if pd.api.types.is_numeric_dtype(sample):
        return 1.0

    parsed = pd.to_numeric(
        sample.astype("string").str.replace(
            ",",
            "",
            regex=False,
        ),
        errors="coerce",
    )
    return float(parsed.notna().mean())


def _boolean_ratio(series: pd.Series) -> float:
    sample = (
        series.dropna()
        .astype("string")
        .str.strip()
        .str.lower()
        .head(1000)
    )

    if sample.empty:
        return 0.0

    allowed = {
        "true", "false", "yes", "no",
        "y", "n", "1", "0",
    }
    return float(sample.isin(allowed).mean())


def _uniqueness_ratio(series: pd.Series) -> float:
    non_null = series.dropna()

    if non_null.empty:
        return 0.0

    return float(
        non_null.nunique(dropna=True) / len(non_null)
    )


def detect_column(
    dataframe: pd.DataFrame,
    column: str,
) -> ColumnDetection:
    """Infer one column's most likely semantic role."""
    series = dataframe[column]
    normalized = normalize_name(column)

    candidates: list[tuple[ColumnRole, float, str]] = []

    date_name, date_reason = _name_score(
        normalized,
        DATE_TERMS,
    )
    date_ratio = _date_parse_ratio(series)
    date_score = min(
        1.0,
        date_name * 0.60 + date_ratio * 0.55,
    )
    if date_score >= 0.65:
        candidates.append(
            (
                "date",
                date_score,
                (
                    f"{date_reason}; "
                    f"{date_ratio:.0%} values parse as dates"
                ).strip("; "),
            )
        )

    id_name, id_reason = _name_score(
        normalized,
        ID_TERMS,
    )
    uniqueness = _uniqueness_ratio(series)
    id_score = min(
        1.0,
        id_name * 0.80 + uniqueness * 0.25,
    )
    if id_score >= 0.70:
        candidates.append(
            (
                "identifier",
                id_score,
                (
                    f"{id_reason}; "
                    f"{uniqueness:.0%} values are unique"
                ).strip("; "),
            )
        )

    bool_name, bool_reason = _name_score(
        normalized,
        BOOLEAN_TERMS,
    )
    bool_ratio = _boolean_ratio(series)
    bool_score = min(
        1.0,
        bool_name * 0.70 + bool_ratio * 0.45,
    )
    if bool_score >= 0.72:
        candidates.append(
            (
                "boolean",
                bool_score,
                (
                    f"{bool_reason}; "
                    f"{bool_ratio:.0%} boolean-like values"
                ).strip("; "),
            )
        )

    numeric_ratio = _numeric_parse_ratio(series)
    metric_name, metric_reason = _name_score(
        normalized,
        METRIC_TERMS,
    )
    metric_score = min(
        1.0,
        metric_name * 0.72 + numeric_ratio * 0.42,
    )
    if metric_score >= 0.64:
        candidates.append(
            (
                "metric",
                metric_score,
                (
                    f"{metric_reason}; "
                    f"{numeric_ratio:.0%} values are numeric"
                ).strip("; "),
            )
        )

    category_name, category_reason = _name_score(
        normalized,
        CATEGORY_TERMS,
    )
    unique_count = int(series.nunique(dropna=True))
    row_count = max(len(series), 1)
    category_density = 1 - min(
        unique_count / row_count,
        1.0,
    )
    category_score = min(
        1.0,
        category_name * 0.76
        + category_density * 0.30,
    )
    if category_score >= 0.62:
        candidates.append(
            (
                "category",
                category_score,
                (
                    f"{category_reason}; "
                    f"{unique_count:,} unique values"
                ).strip("; "),
            )
        )

    text_name, text_reason = _name_score(
        normalized,
        TEXT_TERMS,
    )
    average_length = (
        series.dropna()
        .astype("string")
        .str.len()
        .mean()
    )
    average_length = (
        float(average_length)
        if pd.notna(average_length)
        else 0.0
    )
    text_score = min(
        1.0,
        text_name * 0.80
        + min(average_length / 80, 1.0) * 0.35,
    )
    if text_score >= 0.64:
        candidates.append(
            (
                "text",
                text_score,
                (
                    f"{text_reason}; "
                    f"average text length {average_length:.0f}"
                ).strip("; "),
            )
        )

    if numeric_ratio >= 0.92:
        candidates.append(
            (
                "numeric",
                min(0.88, numeric_ratio * 0.88),
                f"{numeric_ratio:.0%} values are numeric",
            )
        )

    if not candidates:
        return ColumnDetection(
            column=column,
            role="unknown",
            confidence=0.30,
            reason="no strong semantic pattern detected",
        )

    role, confidence, reason = max(
        candidates,
        key=lambda item: item[1],
    )

    return ColumnDetection(
        column=column,
        role=role,
        confidence=round(confidence, 3),
        reason=reason,
    )


def detect_dataset(
    dataframe: pd.DataFrame,
) -> DatasetDetection:
    """Infer dashboard configuration for an entire dataset."""
    detections = tuple(
        detect_column(dataframe, column)
        for column in dataframe.columns
    )

    date_candidates = sorted(
        (
            detection
            for detection in detections
            if detection.role == "date"
        ),
        key=lambda item: item.confidence,
        reverse=True,
    )

    metric_candidates = sorted(
        (
            detection
            for detection in detections
            if detection.role == "metric"
        ),
        key=lambda item: item.confidence,
        reverse=True,
    )

    category_candidates = sorted(
        (
            detection
            for detection in detections
            if detection.role == "category"
        ),
        key=lambda item: item.confidence,
        reverse=True,
    )

    identifier_columns = tuple(
        detection.column
        for detection in detections
        if detection.role == "identifier"
    )

    boolean_columns = tuple(
        detection.column
        for detection in detections
        if detection.role == "boolean"
    )

    numeric_columns = tuple(
        detection.column
        for detection in detections
        if detection.role in {"metric", "numeric"}
    )

    return DatasetDetection(
        date_column=(
            date_candidates[0].column
            if date_candidates
            else None
        ),
        metric_column=(
            metric_candidates[0].column
            if metric_candidates
            else (
                numeric_columns[0]
                if numeric_columns
                else None
            )
        ),
        category_column=(
            category_candidates[0].column
            if category_candidates
            else None
        ),
        identifier_columns=identifier_columns,
        boolean_columns=boolean_columns,
        numeric_columns=numeric_columns,
        detections=detections,
    )


def detection_table(
    detection: DatasetDetection,
) -> pd.DataFrame:
    """Create a user-facing table from detection results."""
    return pd.DataFrame(
        [
            {
                "Column": item.column,
                "Suggested role": item.role.title(),
                "Confidence": item.confidence,
                "Reason": item.reason,
            }
            for item in detection.detections
        ]
    ).sort_values(
        ["Suggested role", "Confidence"],
        ascending=[True, False],
    )
