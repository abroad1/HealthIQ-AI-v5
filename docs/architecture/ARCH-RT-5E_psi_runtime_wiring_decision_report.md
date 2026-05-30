# ARCH-RT-5E — PSI Runtime Wiring Decision Report

**Work package:** `ARCH-RT-5E_psi_runtime_wiring_decision`  
**Generated:** 2026-05-30

## Decision

**deferred** — PSI is **not** runtime-wired. Final classification: **`deferred_non_launch_blocker`**.

## Rationale

Repo evidence shows Promoted Signal Intelligence (PSI) is a governed Knowledge Bus artefact (20 `pkg_kb47_*` opt-in packages) with a deterministic loader and validator, but **no Intelligence Core consumer** on the Wave 1 launch path:

- Card evidence authority: compiled `health_system_cards` YAML via `health_system_card_evidence.py`.
- Root-cause authority: legacy YAML + one compiled hypothesis (`signal_vitamin_d_low`) via `compiled_hypothesis.py` / `root_cause_compiler_v1.py`.
- Signal activation: `signal_library.yaml` via `SignalRegistry` / `SignalEvaluator`.

No launch-critical user-facing claim was identified that requires PSI semantics at runtime. ARCH-RT-5 M4 deferral holds after ARCH-RT-5B/5C/5D estate completion.

## Launch-critical claim assessment

See `docs/audit-papers/ARCH-RT-5E_psi_runtime_wiring_decision_audit.md` § Launch-critical claim assessment.

**Verdict:** Launch slice does not require PSI runtime consumption.

## PSI artefact coverage

| Metric | Value |
|--------|------:|
| Schema | `promoted_signal_intelligence_schema_v1.yaml` v1.0.0 |
| On-disk PSI files | 20 |
| Manifest opt-ins | 20 |
| Cohort | `pkg_kb47_*` |

Reference: `docs/architecture/psi_coverage_and_manifest_opt_in_report.md` (counts re-verified 2026-05-30).

## Runtime consumption status

| Layer | Consumed at runtime? |
|-------|---------------------|
| PSI loader (`load_promoted_signal_intelligence_for_package`) | **No** on orchestrator / compiler / card / root-cause paths |
| PSI validator / package validation | Yes (offline validation only) |
| PSI translator (`investigation_spec_to_promoted_signal.py`) | Compile-time / ingest only |

## Identity join assessment

If a future sprint mandates Outcome B wiring, the governed join contract remains:

```text
activation_key  — primary activation-frame identity
source_spec_id  — provenance validation (explicit vs inferred)
signal_id       — family-level grouping only
package_id      — package provenance / debugging where needed
```

Unresolved provenance (ARCH-RT-5D register, 142 batch JSON packages without explicit manifest `source_spec_id`) would **block safe narrow wiring** until provenance quality is sufficient. That constraint does not affect deferral.

## Implementation changes

**None** to runtime modules, DTOs, or frontend.

Documentation updates only:

- `docs/audit-papers/ARCH-RT-5E_psi_runtime_wiring_decision_audit.md`
- `docs/audit-papers/active_intelligence_authority_manifest.md`
- `docs/audit-papers/day_one_architecture_launch_readiness_audit.md`
- `docs/sprints/healthiq_day_one_architecture_rework_sprint_plan_FINAL_updated.md` (carry-forward register)

## DTO / frontend impact

**None.**

## Tests

| Command | Purpose |
|---------|---------|
| `pytest backend/tests/unit/test_arch_rt5e_psi_runtime_wiring_decision.py -q` | Launch-critical PSI isolation guard |
| `pytest backend/tests/unit/test_promoted_signal_intelligence_kb_s47d.py -q` | Existing loader/validator regression |
| `pytest backend/tests/unit/test_arch_rt5_launch_gate.py backend/tests/unit/test_health_system_card_evidence_arch_rt5b.py backend/tests/unit/test_compiled_hypothesis_arch_rt5c.py -q` | Prior sprint protections |

## Remaining risks

| Risk | Mitigation |
|------|------------|
| Future sprint wires PSI without identity join | Enforce ADR-RT-002 + `psi_runtime_wiring_design.md` |
| API route outside `backend/core` loads PSI | Not found in this sprint; re-audit if new routes added |
| Drift: launch claim implicitly assumes PSI semantics | Authority manifest + guard test |

## Final carry-forward classification

```text
PSI runtime wiring → deferred_non_launch_blocker
```

Day-one launch slice remains **non-blocked** on PSI deferral.
