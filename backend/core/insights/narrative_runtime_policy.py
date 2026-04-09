"""
Governed runtime policy for Layer C insight narrative (`insights[]` path) — BE-S1B.

Separates:
- **API / default orchestrator path** (`allow_llm=None`): requires explicit double opt-in
  (`HEALTHIQ_NARRATIVE_LLM` and `HEALTHIQ_ENABLE_LLM`) so production cannot accidentally
  activate network LLM through a single weak env default.
- **Explicit orchestrator opt-in** (`allow_llm=True`): used by golden runners and operators;
  still respects `HEALTHIQ_MODE=test` and `LLM_ENABLED`.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

from config.env import settings

_TRUTHY = frozenset({"1", "true", "yes", "on"})


def _env_truthy(name: str) -> bool:
    return os.getenv(name, "").strip().lower() in _TRUTHY


@dataclass(frozen=True)
class NarrativeRuntimeDecision:
    """Resolved gates for `InsightSynthesizer(allow_llm=...)`."""

    synthesizer_allow_llm: bool
    master_switch_narrative_llm: bool
    network_llm_env: bool
    healthiq_mode: str
    llm_enabled_setting: bool
    reason: str


def resolve_narrative_llm_allow_llm(
    orchestrator_explicit_allow_llm: Optional[bool] = None,
) -> NarrativeRuntimeDecision:
    """
    Resolve whether the synthesizer may use a live network LLM client (when no client is injected).

    Args:
        orchestrator_explicit_allow_llm: ``AnalysisOrchestrator(allow_llm=...)`` value.
    """
    mode = (settings.HEALTHIQ_MODE or "").strip().lower()
    master = _env_truthy("HEALTHIQ_NARRATIVE_LLM")
    network = _env_truthy("HEALTHIQ_ENABLE_LLM")
    llm_on = bool(getattr(settings, "LLM_ENABLED", True))

    if orchestrator_explicit_allow_llm is False:
        return NarrativeRuntimeDecision(
            synthesizer_allow_llm=False,
            master_switch_narrative_llm=master,
            network_llm_env=network,
            healthiq_mode=mode,
            llm_enabled_setting=llm_on,
            reason="orchestrator_explicit_false",
        )

    if orchestrator_explicit_allow_llm is True:
        if mode == "test":
            return NarrativeRuntimeDecision(
                synthesizer_allow_llm=False,
                master_switch_narrative_llm=master,
                network_llm_env=network,
                healthiq_mode=mode,
                llm_enabled_setting=llm_on,
                reason="test_mode_forces_mock",
            )
        if not llm_on:
            return NarrativeRuntimeDecision(
                synthesizer_allow_llm=False,
                master_switch_narrative_llm=master,
                network_llm_env=network,
                healthiq_mode=mode,
                llm_enabled_setting=False,
                reason="LLM_ENABLED_false",
            )
        return NarrativeRuntimeDecision(
            synthesizer_allow_llm=True,
            master_switch_narrative_llm=master,
            network_llm_env=network,
            healthiq_mode=mode,
            llm_enabled_setting=llm_on,
            reason="orchestrator_explicit_true",
        )

    if mode in {"test", "fixture", "fixtures"}:
        return NarrativeRuntimeDecision(
            synthesizer_allow_llm=False,
            master_switch_narrative_llm=master,
            network_llm_env=network,
            healthiq_mode=mode,
            llm_enabled_setting=llm_on,
            reason="fixture_or_test_mode_uses_mock",
        )

    if not master:
        return NarrativeRuntimeDecision(
            synthesizer_allow_llm=False,
            master_switch_narrative_llm=False,
            network_llm_env=network,
            healthiq_mode=mode,
            llm_enabled_setting=llm_on,
            reason="HEALTHIQ_NARRATIVE_LLM_not_set_default_off",
        )

    if not network:
        return NarrativeRuntimeDecision(
            synthesizer_allow_llm=False,
            master_switch_narrative_llm=master,
            network_llm_env=False,
            healthiq_mode=mode,
            llm_enabled_setting=llm_on,
            reason="HEALTHIQ_ENABLE_LLM_required_with_narrative_master",
        )

    if not llm_on:
        return NarrativeRuntimeDecision(
            synthesizer_allow_llm=False,
            master_switch_narrative_llm=master,
            network_llm_env=network,
            healthiq_mode=mode,
            llm_enabled_setting=False,
            reason="LLM_ENABLED_false",
        )

    return NarrativeRuntimeDecision(
        synthesizer_allow_llm=True,
        master_switch_narrative_llm=True,
        network_llm_env=True,
        healthiq_mode=mode,
        llm_enabled_setting=True,
        reason="api_path_double_opt_in_passed",
    )


def narrative_runtime_meta_from_decision(
    decision: NarrativeRuntimeDecision,
    llm_client: Any,
    *,
    client_injected: bool,
) -> Dict[str, Any]:
    """Stable, replay-friendly narrative runtime metadata (not user-facing narrative)."""
    cls_name = type(llm_client).__name__
    mod = type(llm_client).__module__
    if cls_name == "GeminiClient" and mod.endswith("gemini_client"):
        client_kind = "gemini"
        runtime_mode = "live_gemini"
    elif cls_name == "MockLLMClient":
        client_kind = "mock"
        runtime_mode = "deterministic_mock"
    else:
        client_kind = cls_name
        runtime_mode = "deterministic_mock"

    return {
        "policy_version": "1.0.0",
        "runtime_mode": runtime_mode,
        "client_kind": client_kind,
        "synthesizer_allow_llm_resolved": decision.synthesizer_allow_llm,
        "master_switch_HEALTHIQ_NARRATIVE_LLM": decision.master_switch_narrative_llm,
        "HEALTHIQ_ENABLE_LLM": decision.network_llm_env,
        "HEALTHIQ_MODE": decision.healthiq_mode or "",
        "LLM_ENABLED": decision.llm_enabled_setting,
        "policy_reason": decision.reason,
        "client_constructor_injected": client_injected,
    }
