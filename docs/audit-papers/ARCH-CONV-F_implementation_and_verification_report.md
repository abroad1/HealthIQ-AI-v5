# ARCH-CONV-F — Implementation and Verification Report

**Work ID:** `ARCH-CONV-F`  
**Branch:** `feature/arch-conv-f-haematology-compiled-why`  
**Risk / change type:** HIGH / MIXED  
**Gate 1:** `ARCH-CONV-F-GATE1-HMR-2026-08-01` (`APPROVED_WITH_NARROWING`)  
**Gate 2:** `ARCH-CONV-F-GATE2-ANTHONY-2026-08-01` (`APPROVED`)  
**Hardening:** `automation_bus/latest_prompt_hardening.json` — `HARDENED`  
**Implementation owner:** Cursor (`healthiq-core-engine`)

## 1. Baseline proof

Before implementation (Stage 0 / kernel start):

| Check | Result |
|---|---|
| Working tree dirty only with bus prompt/hardening | Pass — staged as `chore(bus): stage ARCH-CONV-F work package` |
| Stash list | Empty |
| Active WP token | Absent before start; present after start for `ARCH-CONV-F` |
| `compiled_why_authority_register_v1.yaml` ferritin/hemoglobin rows | Zero |
| Baseline counts | `COMPILED_ACTIVE=21`, `LEGACY_RETIRED=15`, `REJECTED=1`, frames=37 |
| Competing frames already retired for WHY | No |
| Authoritative paths unique | Register + `why_authority_v1.py` + compiler consumer confirmed |

## 2. Authority and loader paths

| Role | Path |
|---|---|
| Compiled-WHY register | `knowledge_bus/governance/compiled_why_authority_register_v1.yaml` |
| Runtime resolver | `backend/core/knowledge/why_authority_v1.py` |
| Runtime consumer | `backend/core/analytics/root_cause_compiler_v1.py` (no mechanism change) |
| Legacy target registry | `backend/core/knowledge/root_cause_registry_v1.py` (unchanged) |
| Bookkeeping register | `knowledge_bus/governance/root_cause_authority_register_v1.yaml` |

## 3. Source-to-runtime rule mapping

### Haemoglobin — `signal_hemoglobin_low::inv_hgb_low_anemia`

| Ratified rule | Runtime representation |
|---|---|
| `why_role: causal` (anaemia / reduced oxygen-carrying) | Register `why_role: causal`; artefact hypothesis `hyp_hemoglobin_anaemia_reduced_oxygen_carrying` |
| MCV/RDW non-owning morphology only | Artefact evidence/caveats; no independent aetiology claim |
| No independent underproduction claim | Competitor `signal_hgb_low::inv_hgb_low_normocytic_underproduction_context` → `LEGACY_RETIRED` / `skip` |
| `<80 g/L` concern escalation only | Existing package override retained; presentation safeguards recorded in governance; no transfusion/treatment wording in compiled summary |
| Oxygen-carrying PSI gap remains open | Explicitly recorded; no PSI activation change |

### Ferritin — `signal_ferritin_high::inv_ferritin_high_overload`

| Ratified rule | Runtime representation |
|---|---|
| Flat `morphology_context` | Register `why_role: morphology_context`; no `conditional_why_role` |
| Never causal under any data state | Parametrised runtime tests across CRP/ALT/iron/TSAT/extreme ferritin |
| CRP/ALT/iron/TSAT context enrichment only | Artefact evidence_for / caveats (static enrichment; no role upgrade) |
| Missing corroboration fail-closed | Bare non-causal elevation wording; no attribution guess |
| `>1000` concern escalation only | Existing override on canonical frame retained; WHY remains morphology_context |
| Competing kb52c frames retired for WHY only | Two `LEGACY_RETIRED` rows; packages/PSI unchanged |

## 4. Files changed

### In scope

- `knowledge_bus/governance/compiled_why_authority_register_v1.yaml` (+2 COMPILED_ACTIVE, +3 LEGACY_RETIRED)
- `backend/core/knowledge/why_authority_v1.py` (pilot cohort: ferritin, hemoglobin, parallel `signal_hgb_low`)
- `knowledge_bus/compiled/hypotheses/inv_ferritin_high_overload.yaml`
- `knowledge_bus/compiled/hypotheses/inv_hgb_low_anemia.yaml`
- `knowledge_bus/compiled/manifests/arch_conv_f_ferritin_high.yaml`
- `knowledge_bus/compiled/manifests/arch_conv_f_hgb_low.yaml`
- `knowledge_bus/compiled/estate_index_v1.yaml`
- `knowledge_bus/governance/root_cause_authority_register_v1.yaml` (bookkeeping)
- `backend/scripts/validate_compiled_why_authority_gate.py`
- `backend/tests/regression/test_arch_conv_f_haematology_stop_c.py`
- `backend/tests/unit/test_why_authority_pkg3.py`
- `backend/tests/unit/test_arch_rt5_launch_gate.py`
- `docs/architecture/ARCH-CONV-F_medical_decision_register.yaml`
- `docs/architecture/ARCH-CONV-F_GATE_1_GATE_2_decision.md` (register_state update only)
- `docs/audit-papers/ARCH-CONV-F_implementation_and_verification_report.md` (this file)

### Explicitly unchanged

- `backend/core/knowledge/root_cause_registry_v1.py`
- `backend/core/analytics/root_cause_compiler_v1.py`
- All five package `signal_library.yaml` / `package_manifest.yaml` / PSI files
- Signal libraries, SSOT biomarkers, derived-metric registries, frontend

## 5. Before / after register counts

| Metric | Before | After | Delta |
|---|---|---|---|
| `COMPILED_ACTIVE` | 21 | 23 | **+2** |
| `LEGACY_RETIRED` | 15 | 18 | **+3** |
| `REJECTED` | 1 | 1 | 0 |
| Total frames | 37 | 42 | +5 |
| Loaded compiled frames (estate index artefacts) | 21 | 23 | +2 |
| Affected signal families newly in pilot cohort | — | `signal_ferritin_high`, `signal_hemoglobin_low` (+ parallel `signal_hgb_low` for skip) | — |

Register delta matches the mandated `+2 COMPILED_ACTIVE / +3 LEGACY_RETIRED`.

## 6. Source and output hashes

| Artefact | SHA-256 |
|---|---|
| `inv_ferritin_high_overload_v1.yaml` (source) | `758A939E08A0B816D8E995EA1BBBE3AED5F1868112E5D2345ED40A0E4F713E03` |
| `inv_hgb_low_anemia.yaml` (source) | `9FE3A27CED4FB977C928B64EC0F0AB173CC5BC39D61DD3A33DC274C64AB390F4` |
| `inv_ferritin_high_overload.yaml` (compiled) | `3EE6D3EA1F541D3883139EC21020D2FD911EF86A4A7E99B9A074D2FD67412522` |
| `inv_hgb_low_anemia.yaml` (compiled) | `02418D3ED5C7CAE844EBD621318F017A2013470AB263783E09354765686F1052` |

## 7. Validators

```text
python backend/scripts/validate_compiled_why_authority_gate.py
→ compiled_why_authority_gate: PASS
→ frames=42 compiled_active=23 rejected=1 legacy_retired=18
```

Package validators (all five affected packages): **PASS**

- `pkg_s24_ferritin_high_overload`
- `pkg_kb52c_ferritin_high_inflammatory_hyperferritinemia` (PSI validation PASS; unchanged)
- `pkg_kb52c_ferritin_high_iron_overload_context` (PSI validation PASS; unchanged)
- `pkg_s24_hgb_low_anemia`
- `pkg_kb52c_hgb_low_normocytic_underproduction_context`

## 8. Tests

### ARCH-CONV-F + authority unit

```text
python -m pytest backend/tests/regression/test_arch_conv_f_haematology_stop_c.py `
  backend/tests/unit/test_why_authority_pkg3.py `
  backend/tests/unit/test_arch_rt5_launch_gate.py -q --tb=line
→ 38 passed
```

### Existing compiled-WHY regressions (thyroid, lipid, renal, ALP/GGT)

```text
python -m pytest backend/tests/regression/test_arch_conv_a_wave1_thyroid_stop_c.py `
  backend/tests/regression/test_arch_conv_a_wave2_lipid_stop_c.py `
  backend/tests/regression/test_arch_conv_b_renal_stop_c.py `
  backend/tests/regression/test_arch_conv_c_alp_ggt_stop_c.py -q --tb=line
→ 55 passed
```

## 9. Proof statements

| Requirement | Proof |
|---|---|
| No runtime research-file read introduced | Static check in F suite against compiler + why_authority source text |
| No signal-library / package / PSI change | `git diff` empty for package manifests, signal libraries, PSI paths |
| No new medical rule or threshold invented | Overrides remain pre-existing `<80` / `>1000`; TSAT used as existing SSOT corroborator only |
| Haemoglobin oxygen-carrying PSI gap remains open | Recorded in medical decision register; no PSI activation edited |
| Deterministic repeatability | F suite repeat-run equality assertion |
| No forged human/medical approvals | Gate refs only; no new approval invented |

## 10. Mechanism note — `signal_hgb_low` pilot membership

The prompt requires retiring `pkg_kb52c_hgb_low_normocytic_underproduction_context` for WHY ownership (`skip`). That package uses signal_id `signal_hgb_low` (not `signal_hemoglobin_low`). Per the established lipid parallel-id pattern, `signal_hgb_low` was added to `_PILOT_SIGNAL_IDS` so `LEGACY_RETIRED` resolves to `skip` rather than falling through to legacy emit. This is established mechanism reuse, not a new compiler path.

## 11. Known unrelated baseline failures

None observed in the modules executed for this sprint. Full relevant modules were run; no cherry-picked node-only citations.

## 12. Closure posture

Finish readiness requires clean working tree after committing this evidence and implementation. Kernel `COMPLETE` status commit follows finish per SOP §6.8.1. No merge by Cursor.
