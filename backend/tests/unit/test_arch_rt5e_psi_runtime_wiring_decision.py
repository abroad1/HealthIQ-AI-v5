"""ARCH-RT-5E — PSI launch decision: deferred; launch-critical paths must not import PSI loader."""

from __future__ import annotations

from pathlib import Path

_REPO = Path(__file__).resolve().parents[3]

# Intelligence Core modules on the governed Wave 1 launch path.
_LAUNCH_CRITICAL_REL_PATHS = (
    "backend/core/knowledge/health_system_card_evidence.py",
    "backend/core/knowledge/compiled_hypothesis.py",
    "backend/core/knowledge/load_root_cause_hypotheses.py",
    "backend/core/analytics/root_cause_compiler_v1.py",
    "backend/core/analytics/report_compiler_v1.py",
    "backend/core/analytics/domain_narrative_wave1.py",
    "backend/core/analytics/signal_evaluator.py",
    "backend/core/pipeline/orchestrator.py",
    "backend/core/pipeline/orchestrator_phases_v1.py",
)

_FORBIDDEN_IMPORT_MARKERS = (
    "load_promoted_signal_intelligence",
    "from core.knowledge.load_promoted_signal_intelligence",
)


def test_launch_critical_modules_do_not_import_psi_loader() -> None:
    for rel in _LAUNCH_CRITICAL_REL_PATHS:
        path = _REPO / rel
        assert path.is_file(), f"missing launch-critical module: {rel}"
        text = path.read_text(encoding="utf-8")
        for marker in _FORBIDDEN_IMPORT_MARKERS:
            assert marker not in text, f"{rel} must not import PSI loader ({marker!r})"


def test_authority_manifest_psi_deferred_classification() -> None:
    manifest = (_REPO / "docs/audit-papers/active_intelligence_authority_manifest.md").read_text(
        encoding="utf-8"
    )
    assert "ARCH-RT-5E" in manifest
    assert "deferred_non_launch_blocker" in manifest
    assert "Not consumed" in manifest or "not consumed" in manifest.lower()


def test_arch_rt5e_audit_decision_is_deferred_non_launch_blocker() -> None:
    audit = (
        _REPO / "docs/audit-papers/ARCH-RT-5E_psi_runtime_wiring_decision_audit.md"
    ).read_text(encoding="utf-8")
    assert "deferred_non_launch_blocker" in audit
    assert "**Yes**" in audit  # selected row in classification table
