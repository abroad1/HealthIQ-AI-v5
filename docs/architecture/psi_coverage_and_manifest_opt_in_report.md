# PSI Coverage and Manifest Opt-In Report

**Work package:** ARCH-RT-0  
**Generated:** 2026-05-28

## PSI artefact paths

| Role | Path |
|------|------|
| Schema | `knowledge_bus/schema/promoted_signal_intelligence_schema_v1.yaml` |
| Translation rules | `knowledge_bus/schema/signal_intelligence_translation_rules_v1.yaml` |
| Translator (compile-time) | `backend/core/knowledge/investigation_spec_to_promoted_signal.py` |
| Loader | `backend/core/knowledge/load_promoted_signal_intelligence.py` |
| Validator | `backend/scripts/validate_promoted_signal_intelligence.py` |
| Lifecycle contract checks | `backend/core/knowledge/kb_lifecycle_contract_v1.py` |
| ADR authority | `architecture/ADR-008-promoted-signal-intelligence-contract-v1.md` |

## Counts

| Metric | Count |
|--------|------:|
| `promoted_signal_intelligence.yaml` on disk | 20 |
| Packages with manifest PSI opt-in (`promoted_signal_intelligence:` key) | 20 |
| Package generation | **All `pkg_kb47_*`** |

Example PSI header (provenance in PSI, not manifest):

```yaml
investigation_spec_id: inv_free_t4_high_thyrotoxicosis_context
signal_id: signal_free_t4_high
```

## Runtime consumption status

| Question | Answer | Evidence |
|----------|--------|----------|
| Imported by `SignalRegistry` / `SignalEvaluator`? | **NO** | `backend/core/analytics/signal_evaluator.py` loads `signal_library.yaml` only |
| Imported by `orchestrator.py`? | **NO** | Grep: no PSI loader import on pipeline path |
| Imported by `domain_score_assembler.py` / `report_compiler_v1.py`? | **NO** | Grep: no runtime PSI consumption |
| Used anywhere in `backend/core`? | **Validators + lifecycle + translator only** | `load_promoted_signal_intelligence.py` called from tests/validators/ingest, not orchestrator |

**Conclusion:** PSI is **runtime-dead** for analytical output construction today. It is a **governed compile-time / validation artefact** for the KB-S47 cohort.

## PSI vs launch-critical claims

| Area | PSI required for launch? | Rationale |
|------|------------------------|-----------|
| Signal activation (firing) | **No** | Runtime uses `signal_library.yaml` via `SignalRegistry` |
| Signal-layer semantics (roles, overrides) | **Partially deferred** | PSI holds richer semantics; not wired to evaluator |
| Hypothesis / WHY | **No** | ADR-008 excludes hypotheses from PSI; root-cause YAML + compiler separate |
| Health Systems Card evidence | **No** | Subsystem evidence from `wave1_subsystem_evidence.py`, not PSI |

**Deferral:** Full PSI runtime wiring is **not launch-blocking** if day-one accepts compiled `signal_library` as activation authority; PSI gap closure is **post–ARCH-RT-1** (contracts + compile foundation).

## PSI gap closure candidates

All 20 `pkg_kb47_*` packages have PSI on disk. Packages **without** PSI (166 other `pkg_*` + legacy) are candidates for:

1. Batch PSI generation from investigation specs (translator exists), or  
2. Direct activation compile to `signal_library.yaml` without PSI (per ADR-008 separation).

## Uncertainty

- Whether any API route loads PSI outside `backend/core` was not exhaustively searched; **Intelligence Core path is confirmed dead**.
