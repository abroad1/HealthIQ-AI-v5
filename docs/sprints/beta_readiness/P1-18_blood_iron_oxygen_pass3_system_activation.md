# P1-18 — Blood/Iron/Oxygen Pass 3 System Activation Pack

**Work ID:** P1-18  
**Branch:** `sprint/P1-18-blood-iron-oxygen-pass3-system-activation`  
**Date:** 2026-06-21  
**Status:** IMPLEMENTATION_COMPLETE  
**Agent:** healthiq-core-engine  
**Change type:** MIXED (BEHAVIOUR controls)

---

## 1. Runtime reality map

| Component | Path | Finding |
|-----------|------|---------|
| Domain assembler | `backend/core/analytics/domain_score_assembler.py` | `wave1_blood_iron_oxygen` fifth domain block on cbc scoring rail; `_BLOOD_IRON_OXYGEN_LAUNCH_SIGNAL_IDS` was empty frozenset (P1-3 carry-forward) |
| Subsystem evidence | `backend/core/analytics/wave1_subsystem_evidence.py:37-39` | Single subsystem `wave1_bio_oxygen_carrying_capacity` from compiled card evidence |
| Signal registry | `backend/core/analytics/signal_evaluator.py:31-36` | Loads all `knowledge_bus/packages/*/signal_library.yaml` deterministically |
| pkg_kb61 signal | `knowledge_bus/packages/pkg_kb61_transferrin_high_iron_deficiency_transport_upregulation/signal_library.yaml` | `signal_transferrin_high` uses `lab_range_exceeded`; `transferrin_saturation` in `dependencies.biomarkers`, not `derived_metrics` |
| Activation validator | `backend/scripts/validate_staged_psi_activation_readiness.py:32` | Hardcoded `DERIVED_MARKER_IDS = {transferrin_saturation}` blocked 7 staged PSI despite SSOT canonicality |
| SSOT | `backend/ssot/biomarkers.yaml:1865` | `transferrin_saturation` is top-level canonical numeric marker |
| Runtime input | `backend/tests/fixtures/golden_panel_160.json:543` | Lab-provided `transferrin_saturation` with reference range already accepted |
| PSI runtime | N/A in blood/iron/oxygen path | PSI is validation-only until production opt-in; signal_library is the firing mechanism |
| Existing tests | `test_p1_3_blood_iron_oxygen_domain_card.py` | Domain card, subsystem evidence, empty allowlist exclusion tests |

---

## 2. Selected build target

**Primary target:** Transferrin / iron transport subsystem firing via `signal_transferrin_high` (pkg_kb61).

**Why this target:**
1. P1-17 handoff identified pkg_kb61 as highest-readiness derived cohort candidate (ID-matched production host package).
2. Hardening confirmed STOP gate 2 option A: validator policy correction only, not medical content change.
3. `signal_library.yaml` already lists `transferrin_saturation` as lab biomarker dependency.
4. Safe to add to launch allowlist without frame-adjudication blockers affecting this signal.

**Not selected (STOP gates):**
- CBC pkg_kb52c staged PSI — package identity unresolved (STOP gate 1).
- Iron Batch C PSI — medical-review carry-forwards (STOP gate 1).
- Hemoglobin / ferritin launch signals — frame adjudication backlog (STOP gate 1).

---

## 3. Implementation summary

| Change | File | Description |
|--------|------|-------------|
| Validator policy | `validate_staged_psi_activation_readiness.py` | Emptied `DERIVED_MARKER_IDS`; lab-provided SSOT-canonical markers no longer hard-blocked |
| Launch allowlist | `domain_score_assembler.py` | Added `signal_transferrin_high` to `_BLOOD_IRON_OXYGEN_LAUNCH_SIGNAL_IDS` |
| Tests | `test_p1_18_blood_iron_oxygen_pass3_system_activation.py` | Signal firing, domain active_signal_ids, lab-provided TSAT, control/partial panels |
| Tests | `test_validate_staged_psi_activation_readiness.py` | Updated estate counts (7 activation-ready, 34 blocked); pkg_kb61 activation-ready fixture |

**Not implemented (by design):**
- Knowledge Bus PSI opt-in to production package (KB agent scope).
- Frontend changes.
- Calculated `transferrin_saturation` when lab value absent.
- Additional CBC/iron launch signals beyond `signal_transferrin_high`.

---

## 4. Pass 3 intelligence now represented

- `signal_transferrin_high` from pkg_kb61 Pass 3 research now fires at runtime via existing signal_library when transferrin exceeds lab upper bound.
- Domain card `active_signal_ids` includes the signal when evaluated active; hemoglobin/ferritin/WBC signals remain excluded.
- Staged PSI for 7 transferrin_saturation-dependent candidates now pass derived-marker gate (activation-ready count 0→7); PSI content unchanged.

---

## 5. transferrin_saturation policy decision

**Decision:** Option A — lab-provided SSOT-canonical marker; remove incorrect derived-marker validator block.

**Evidence:**
- SSOT canonical at `biomarkers.yaml:1865`.
- Golden panel accepts lab-provided values.
- pkg_kb61 signal_library uses `dependencies.biomarkers`, not `derived_metrics`.

**Calculation mode:** Carry-forward — no governed formula exists (STOP gate 2).

---

## 6. Tests and validation

```powershell
python -m pytest backend/tests/unit/test_p1_18_blood_iron_oxygen_pass3_system_activation.py backend/tests/unit/test_validate_staged_psi_activation_readiness.py backend/tests/unit/test_p1_3_blood_iron_oxygen_domain_card.py backend/tests/unit/test_domain_score_assembler_v1.py -q
```

**Result:** 24 passed.

```powershell
python backend/scripts/validate_staged_psi_activation_readiness.py
```

**Result:** exit 0 — `activation_ready_count: 7`, `blocked_count: 34`.

---

## 7. Pass 3 richness preservation

No Pass 3 research was watered down. Unimplemented rich content (override rules, contradiction markers, lifestyle modifiers, iron Batch C frames, CBC identity cohort) is recorded in `P1-18_pass3_system_activation_carry_forward.yaml` with owner and blocker class.

---

## 8. Recommended next build package

**P1-19-KB61-PSI-OPT-IN-1** (Knowledge Bus agent): Opt-in staged PSI for `pkg_kb61_transferrin_high_iron_deficiency_transport_upregulation` now that validator policy is resolved.

**Parallel:** P1-CBC-PACKAGE-PROVENANCE-1 for KB-S52c vs KB-S58 identity cohort.

---

## 9. Scope confirmations

| Check | Status |
|-------|--------|
| No frontend edits | Confirmed |
| No Knowledge Bus medical content edits | Confirmed |
| No raw Pass 3 runtime reads | Confirmed |
| No global/default reference ranges introduced | Confirmed |
| No medical-review-blocked content activated | Confirmed |
| No scoring policy changes | Confirmed |
