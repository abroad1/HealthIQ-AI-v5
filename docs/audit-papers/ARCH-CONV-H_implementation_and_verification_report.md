# ARCH-CONV-H — Implementation and Verification Report

**Work ID:** `ARCH-CONV-H`  
**Branch:** `feature/arch-conv-h-hba1c-compiled-why-authority`  
**Risk / change type:** HIGH / MIXED  
**Gate 1:** `ARCH-CONV-H-GATE1-HMR-2026-08-01` (`APPROVED_WITH_NARROWING`)  
**Gate 2:** `ARCH-CONV-H-GATE2-ANTHONY-2026-08-01` (`APPROVED`)  
**Hardening:** `automation_bus/latest_prompt_hardening.json` — `HARDENED`  
**Implementation owner:** Cursor (`healthiq-core-engine`)

## 1. Baseline proof

| Check | Result |
|---|---|
| Phase 0 baseline counts | `COMPILED_ACTIVE=24`, `LEGACY_RETIRED=19`, `REJECTED=1`, frames=44 |
| HbA1c register / artefact / pilot membership | Absent before implementation |
| Active WP | Resumed without re-`start` after Gate 2 recording |
| Stash | Empty throughout |

## 2. Source-to-runtime rule map

| Ratified rule | Runtime representation |
|---|---|
| `signal_hba1c_high::inv_hba1c_high_glycaemia` | `COMPILED_ACTIVE` + artefact `inv_hba1c_high_glycaemia.yaml` |
| `why_role: morphology_context` | Flat register role; no `conditional_why_role` |
| No diabetes diagnosis / subtype / complications / chronicity / causal attribution / treatment directives | Artefact caveats + summary prohibitions; regression suite |
| Competitor diabetes-range hyperglycemia frame | `LEGACY_RETIRED` → `skip`; WHY-only |
| HbA1c `>= 48 mmol/mol` | Diabetes-range concern requiring clinical confirmation only |
| TG/HDL metabolic override | Subordinate metabolic-pattern context only; no metabolic-syndrome diagnosis |
| Adjacent identities | `signal_hba1c_pct_high`, `signal_glucose_dysregulation_hba1c_context` unchanged |
| Urate compiled authority | Unchanged |

## 3. Files changed (implementation)

- `knowledge_bus/governance/compiled_why_authority_register_v1.yaml`
- `backend/core/knowledge/why_authority_v1.py`
- `knowledge_bus/compiled/hypotheses/inv_hba1c_high_glycaemia.yaml`
- `knowledge_bus/compiled/manifests/arch_conv_h_hba1c_high.yaml`
- `knowledge_bus/compiled/estate_index_v1.yaml`
- `knowledge_bus/governance/root_cause_authority_register_v1.yaml`
- `backend/scripts/validate_compiled_why_authority_gate.py`
- `backend/tests/regression/test_arch_conv_h_hba1c_stop_c.py`
- `backend/tests/regression/test_arch_conv_g_urate_stop_c.py` (HbA1c exclusion updated for H migration)
- `backend/tests/regression/test_arch_conv_f_haematology_stop_c.py` (HbA1c exclusion updated for H migration)
- `backend/tests/unit/test_why_authority_pkg3.py`
- `backend/tests/unit/test_arch_rt5_launch_gate.py`
- `backend/tests/fixtures/panels/phenotypes/phenotype_expectations_v1.yaml` (`ph_hba1c_metabolic_stress_v1` min hypotheses 2→1)
- Gate / evidence / Build Deliverables / Active Carry-Forward docs

Unchanged: compiler, root_cause_registry, packages, PSI, SSOT, frontend, urate artefacts.

## 4. Before / after counts

| Metric | Before | After | Delta |
|---|---|---|---|
| `COMPILED_ACTIVE` | 24 | 25 | **+1** |
| `LEGACY_RETIRED` | 19 | 20 | **+1** |
| `REJECTED` | 1 | 1 | 0 |
| Total frames | 44 | 46 | +2 |
| Loaded compiled frames | 24 | 25 | +1 |

## 5. Hashes

| Artefact | SHA-256 |
|---|---|
| Source `inv_hba1c_high_glycaemia_v1.yaml` | `2CFA335DEBBA2F430C12E2F0605823B9752A3AD78389F32A7D978B8286501247` |
| Compiled `inv_hba1c_high_glycaemia.yaml` | `DC51047680319B5835F6944FDB7FA49F6C0380837A3FC038E76D3C31CA0921EE` |

## 6. Validators / tests

```text
python backend/scripts/validate_compiled_why_authority_gate.py
→ PASS frames=46 compiled_active=25 rejected=1 legacy_retired=20

python backend/scripts/validate_knowledge_package.py --package-dir knowledge_bus/packages/pkg_s24_hba1c_high_glycaemia
→ PASS

python backend/scripts/validate_knowledge_package.py --package-dir knowledge_bus/packages/pkg_kb52c_hba1c_high_diabetes_range_hyperglycemia
→ PASS

python -m pytest backend/tests/regression/test_arch_conv_h_hba1c_stop_c.py \
  backend/tests/regression/test_arch_conv_g_urate_stop_c.py \
  backend/tests/unit/test_why_authority_pkg3.py \
  backend/tests/unit/test_arch_rt5_launch_gate.py -q
→ passed

Sibling ARCH-CONV regression suites (A1/A2/B/C/F/G) + unit count gates → passed

Phenotype expectation update:
`backend/tests/fixtures/panels/phenotypes/phenotype_expectations_v1.yaml`
`ph_hba1c_metabolic_stress_v1` `min_hypothesis_count` 2 → 1 (Gate-approved single compiled morphology_context hypothesis).
```

## 7. Proof statements

- No runtime research-file read introduced (static check in H suite).
- Package / PSI paths unchanged (`git diff` empty under packages).
- No new medical rule/threshold invented; `>=48` and TG/HDL overrides pre-existing.
- Deterministic repeatability asserted.
- No forged approvals; Gate refs recorded before implementation resume.
- Adjacent pct / glucose-dysregulation identities absent from compiled-WHY register.

## 8. Closure posture

Finish after evidence commit. Kernel COMPLETE status commit per SOP §6.8.1. No merge by Cursor.
