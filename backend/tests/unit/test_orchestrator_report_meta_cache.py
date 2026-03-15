from core.pipeline.orchestrator import AnalysisOrchestrator


def test_signal_registry_hash_sha256_cached_after_first_compute(monkeypatch):
    orchestrator = AnalysisOrchestrator()
    calls = {"n": 0}

    def _fake_get_all_signals():
        calls["n"] += 1
        return [{"signal_id": "signal_a"}, {"signal_id": "signal_b"}]

    monkeypatch.setattr(orchestrator.signal_registry, "get_all_signals", _fake_get_all_signals)
    first = orchestrator._get_signal_registry_hash_sha256()
    second = orchestrator._get_signal_registry_hash_sha256()
    assert first == second
    assert isinstance(first, str) and len(first) == 64
    assert calls["n"] == 1


def test_signal_registry_hash_sha256_returns_none_for_empty_registry(monkeypatch):
    orchestrator = AnalysisOrchestrator()
    monkeypatch.setattr(orchestrator.signal_registry, "get_all_signals", lambda: [])
    value = orchestrator._get_signal_registry_hash_sha256()
    assert value is None
