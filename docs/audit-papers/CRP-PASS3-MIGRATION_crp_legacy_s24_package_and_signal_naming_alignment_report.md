# CRP-PASS3-MIGRATION — CRP Legacy s24 Package and Signal Naming Alignment

**Work ID:** `CRP-PASS3-MIGRATION_crp_legacy_s24_package_and_signal_naming_alignment`  
**Branch:** `work/CRP-PASS3-MIGRATION-crp-legacy-s24-package-and-signal-naming-alignment`  
**Status:** Complete (2026-05-31)

## Authority decision

**Outcome B + C (combined):** Pass 3 CRP investigation frames exist in `Batch_4_Pass_3.json` but are **not semantically compiled** into a runtime package equivalent to `pkg_s24_crp_high_inflammation`. Runtime authority for `signal_crp_high` **remains** the s24 translation from `inv_crp_high_inflammation_v1.yaml`, now **explicitly classified** in `knowledge_bus/governance/crp_runtime_authority_v1.yaml`.

**Outcome D:** `signal_crp_high` and `signal_systemic_inflammation` are **distinct clinical constructs**, not aliases:

| Signal | Role | Activation | Runtime package(s) | Root cause |
|---|---|---|---|---|
| `signal_crp_high` | Acute-phase CRP investigation | `lab_range_exceeded` | `pkg_s24_crp_high_inflammation` only | No |
| `signal_systemic_inflammation` | Chronic low-grade inflammation construct | `deterministic_threshold` | `KBP-0001`, `pkg_chronic_inflammation` (multi-frame via `activation_key`) | Yes — `systemic_inflammation_hypotheses_v1.yaml` |
| `signal_inflammation_crp_context` | CRP context escalation | `lab_range_exceeded` | `pkg_inflammation_crp_context` | No |

**Migration performed:** Metadata classification + validator/test guards. **Not performed:** Package pointer swap to Pass 3 (deferred — `CF-CRPPASS3-001`).

## Preflight inventory

### CRP-related signals (runtime libraries)

- `signal_crp_high` — `pkg_s24_crp_high_inflammation` (sole holder)
- `signal_systemic_inflammation` — `KBP-0001`, `pkg_chronic_inflammation`
- `signal_inflammation_crp_context` — `pkg_inflammation_crp_context`

### CRP-related packages

- `pkg_s24_crp_high_inflammation` — **active** runtime authority for `signal_crp_high`
- `pkg_inflammation_crp_context` — context signal only
- `KBP-0001` / `pkg_chronic_inflammation` — systemic inflammation frames

### Pass 3 specs (research only)

- `inv_crp_high_active_inflammatory_or_infective_state` — `Batch_4_Pass_3.json`
- `inv_crp_high_residual_cardiometabolic_inflammatory_risk` — `Batch_4_Pass_3.json`
- Legacy v1: `inv_crp_high_inflammation_v1.yaml` (translated to s24)

### User-facing surfaces (MED-REV-1/2)

- `wave1_cv_vascular_strain` — `hidden_v1`; CRP does not appear as scored subsystem
- Cardiovascular card — lipid-led (`wave1_cv_lipid_transport` scored)
- Root cause — `signal_systemic_inflammation` only (not `signal_crp_high`)

## Files changed

- `knowledge_bus/governance/crp_runtime_authority_v1.yaml` (new)
- `backend/core/knowledge/crp_signal_authority_v1.py` (new)
- `knowledge_bus/packages/pkg_s24_crp_high_inflammation/package_manifest.yaml`
- `backend/scripts/validate_day_one_architecture.py`
- `backend/tests/regression/test_crp_pass3_migration_signal_authority.py` (new)
- `docs/sprints/launch_core_carry_forward_register.md`
- `docs/audit-papers/CRP-PASS3-MIGRATION_crp_legacy_s24_package_and_signal_naming_alignment_report.md`

## Validator / test changes

- Added `validate_crp_signal_authority` to ARCH-RT-6 validator
- New regression module `test_crp_pass3_migration_signal_authority.py`

## Confirmations

- No clinical thresholds, scoring rails, SignalEvaluator mathematics, or SSOT changes
- No raw Pass 3 runtime reads introduced
- No hidden subsystem re-surfacing
- Manual UAT not required (no user-facing output path change)

## Tests run

```powershell
python backend/scripts/validate_day_one_architecture.py
python -m pytest backend/tests/architecture/test_day_one_architecture_guardrails.py -q
python -m pytest backend/tests/regression/test_crp_pass3_migration_signal_authority.py -q
python -m pytest backend/tests/regression/test_med_rev1_wave1_subsystem_visibility.py -q
python -m pytest backend/tests/regression/test_med_rev2_domain_card_copy_and_regeneration.py -q
```

**Results:** PASS / PASS / PASS / PASS / PASS

## Remaining carry-forwards

- **CF-CRPPASS3-001** — Compile Pass 3 CRP frames to governed runtime package
- **CF-ARCHLEG1-001** — Root-cause YAML vs compiled promotion programme
- **CF-ARCHLEG1-004** — Root-cause promotion inventory validator (partial)
