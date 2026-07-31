"""Lightweight per-session result caching for large in-memory datasets.

Streamlit's data cache hashes function arguments and returns copied values.
That is useful for file bytes, but expensive when the argument is a large
DataFrame already held in session state.  This module instead keys results by
the identity of that in-memory dataset and never hashes or copies its rows.
"""

from collections.abc import Callable, Hashable, Mapping
import json
from typing import TypeVar

import streamlit as st


T = TypeVar("T")
_CACHE_KEY = "_analysis_session_cache"


def stable_mapping_key(mapping: Mapping) -> str:
    """Return a deterministic, compact key for small configuration mappings."""

    return json.dumps(
        mapping,
        sort_keys=True,
        separators=(",", ":"),
        default=str,
    )


def _session_state():
    return st.session_state


def session_result(
    dataset,
    key: Hashable,
    factory: Callable[[], T],
) -> T:
    """Return a result cached for the current in-memory dataset and session.

    The dataset itself is retained only as the same object reference already
    present in Streamlit session state.  A newly uploaded/prepared DataFrame
    automatically starts a fresh cache.
    """

    state = _session_state()
    cache = state.get(_CACHE_KEY)
    if not isinstance(cache, dict) or cache.get("dataset") is not dataset:
        cache = {"dataset": dataset, "results": {}}
        state[_CACHE_KEY] = cache

    results = cache["results"]
    if key not in results:
        results[key] = factory()
    return results[key]


def clear_session_results() -> None:
    """Discard cached analysis results in the active Streamlit session."""

    _session_state().pop(_CACHE_KEY, None)
