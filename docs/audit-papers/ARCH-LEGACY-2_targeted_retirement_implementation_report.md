# ARCH-LEGACY-2 — Targeted Legacy Pathway Retirement Implementation

**Work ID:** `ARCH-LEGACY-2_targeted_retirement_implementation`  
**Branch:** `work/ARCH-LEGACY-2-targeted-retirement-implementation`  
**Change type:** MIXED (behaviour retirement + validator + docs)  
**Status:** Complete (2026-05-31)

## Executive summary

Implemented the bounded ARCH-LEGACY-1 retirement slice: removed dead CV helper code, removed unreachable hard-coded Wave 1 subsystem fallback partition, tightened ARCH-RT-6 validator guards, and added regression tests. No clinical thresholds, scoring rails, SignalEvaluator, or SSOT changes. CRP package migration and root-cause dual-authority migration remain deferred.

## Items retired

| Item | Action |
|---|---|
| `cv_contributor` | Deleted from `domain_narrative_wave1.py` (zero call sites) |
| `confidence_sentence_cv_coherent` homocysteine bridge | Removed; delegates to `confidence_sentence_for` only |
| `_Wave1SubsystemDef` partition + `WAVE1_DOMAIN_SUBSYSTEM_DEFS` | Removed from `wave1_subsystem_evidence.py` |
| `_partition_subsystem_markers` hard-coded fallback | Removed |

## Items retained (with rationale)

| Item | Rationale |
|---|---|
| `cv_contributor_primary` / `_cv_contributor_signal_fallback` | Non-lipid-visible CV edge path; not launch-visible when MED-REV-2 lipid authority applies |
| `cv_contributor_for_lipid_visible_card` | Launch-default CV card path |
| Root-cause YAML estate (40 targets) | Out of scope — `CF-ARCHLEG1-001` |
| CRP `pkg_s24` legacy package | Out of scope — `CF-ARCHLEG1-002` |

## Files changed

- `backend/core/analytics/wave1_subsystem_evidence.py`
- `backend/core/analytics/domain_narrative_wave1.py`
- `backend/core/knowledge/launch_estate_v1.py`
- `backend/scripts/validate_day_one_architecture.py`
- `backend/tests/regression/test_arch_legacy2_targeted_retirement.py` (new)
- `backend/tests/regression/test_domain_ux1c_governed_subsystem_evidence.py`
- `backend/tests/unit/test_domain_narrative_wave1.py`
- `docs/sprints/launch_core_carry_forward_register.md`
- `docs/audit-papers/ARCH-LEGACY-2_targeted_retirement_implementation_report.md` (this file)

## Validator changes

- `validate_wave1_assembler_routing`: forbids `_Wave1SubsystemDef`, `_partition_subsystem_markers`, `WAVE1_DOMAIN_SUBSYSTEM_DEFS` in assembler module
- `validate_arch_legacy2_retirement`: forbids `cv_contributor` definition and homocysteine bridge in `confidence_sentence_cv_coherent`; asserts lipid-visible assembler gates and `domain_flat_card_evidence` presence

## Tests added/updated

- **New:** `backend/tests/regression/test_arch_legacy2_targeted_retirement.py`
- **Updated:** `test_domain_ux1c_governed_subsystem_evidence.py`, `test_domain_narrative_wave1.py`

## Carry-forward register updates

- **Resolved:** CF-MEDREV2-003, CF-ARCHLEG1-003
- **Partial / Open:** CF-ARCHLEG1-004 (bounded guards only)
- **Unchanged Open:** CF-ARCHLEG1-001, CF-ARCHLEG1-002

## Confirmations

- No clinical/scoring logic, SignalEvaluator, SignalRegistry, or biomarker SSOT changes
- Hidden MED-REV-1 subsystems remain `hidden_v1` and suppressed from visible DTO rows
- No raw Pass 3 runtime reads introduced
- Manual browser UAT not required (no user-facing output path change beyond retirement protection)

## Tests run

```powershell
python backend/scripts/validate_day_one_architecture.py
python -m pytest backend/tests/architecture/test_day_one_architecture_guardrails.py -q
python -m pytest backend/tests/regression/test_kb_util1_pass3_card_evidence_compile_and_consume.py -q
python -m pytest backend/tests/regression/test_med_rev1_wave1_subsystem_visibility.py -q
python -m pytest backend/tests/regression/test_med_rev2_domain_card_copy_and_regeneration.py -q
python -m pytest backend/tests/regression/test_arch_legacy2_targeted_retirement.py -q
```

## Remaining risks / carry-forwards

- CRP legacy package / signal naming split (`CF-ARCHLEG1-002`)
- Root-cause YAML vs compiled promotion estate (`CF-ARCHLEG1-001`)
- Full validator inventory for CRP migration and root-cause promotion counts (`CF-ARCHLEG1-004` partial)
