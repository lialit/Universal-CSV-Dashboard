from app_core import session_cache


def test_session_result_reuses_value_for_same_dataset_and_key(
    monkeypatch,
) -> None:
    state = {}
    monkeypatch.setattr(session_cache, "_session_state", lambda: state)
    dataset = object()
    calls = 0

    def factory():
        nonlocal calls
        calls += 1
        return {"result": calls}

    first = session_cache.session_result(dataset, "quality", factory)
    second = session_cache.session_result(dataset, "quality", factory)

    assert first is second
    assert calls == 1


def test_session_result_uses_distinct_operation_keys(monkeypatch) -> None:
    state = {}
    monkeypatch.setattr(session_cache, "_session_state", lambda: state)
    dataset = object()

    first = session_cache.session_result(dataset, "first", lambda: 1)
    second = session_cache.session_result(dataset, "second", lambda: 2)

    assert first == 1
    assert second == 2


def test_new_dataset_starts_fresh_result_cache(monkeypatch) -> None:
    state = {}
    monkeypatch.setattr(session_cache, "_session_state", lambda: state)

    first = session_cache.session_result(object(), "quality", lambda: 1)
    second = session_cache.session_result(object(), "quality", lambda: 2)

    assert first == 1
    assert second == 2


def test_mapping_key_is_stable_for_equivalent_configuration() -> None:
    left = {"metric": "sales", "columns": ["sales", "orders"]}
    right = {"columns": ["sales", "orders"], "metric": "sales"}

    assert session_cache.stable_mapping_key(left) == (
        session_cache.stable_mapping_key(right)
    )


def test_clear_session_results_removes_only_analysis_cache(
    monkeypatch,
) -> None:
    state = {"keep": "value", session_cache._CACHE_KEY: {"results": {}}}
    monkeypatch.setattr(session_cache, "_session_state", lambda: state)

    session_cache.clear_session_results()

    assert state == {"keep": "value"}
