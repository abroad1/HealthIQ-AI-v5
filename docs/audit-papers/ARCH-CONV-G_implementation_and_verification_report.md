# ARCH-CONV-G — Implementation and Verification Report

**Work ID:** `ARCH-CONV-G`  
**Branch:** `feature/arch-conv-g-urate-compiled-why`  
**Risk / change type:** HIGH / MIXED  
**Gate 1:** `ARCH-CONV-G-GATE1-HMR-2026-08-01` (`APPROVED_WITH_NARROWING`)  
**Gate 2:** `ARCH-CONV-G-GATE2-ANTHONY-2026-08-01` (`APPROVED`)  
**Hardening:** `automation_bus/latest_prompt_hardening.json` — `HARDENED`  
**Implementation owner:** Cursor (`healthiq-core-engine`)

## 1. Baseline proof

| Check | Result |
|---|---|
| Phase 0 baseline counts | `COMPILED_ACTIVE=23`, `LEGACY_RETIRED=18`, `REJECTED=1`, frames=42 |
| Urate register / artefact / pilot membership | Absent before implementation |
| Active WP | Resumed without re-`start` after gate recording |
| Stash | Empty throughout |

## 2. Source-to-runtime rule map

| Ratified rule | Runtime representation |
|---|---|
| `signal_urate_high::inv_uric_acid_high_metabolic` | `COMPILED_ACTIVE` + artefact `inv_uric_acid_high_metabolic.yaml` |
| `why_role: morphology_context` | Flat register role; no `conditional_why_role` |
| No gout / crystal / CKD / renal failure / specific metabolic disease / treatment-need diagnosis | Artefact caveats + summary prohibitions; regression suite |
| Competitor gout/crystal frame | `LEGACY_RETIRED` → `skip`; subordinate risk context only |
| `or_uric_acid_renal_risk` (`egfr < 60`) | Existing override retained; concern escalation only |
| Missing eGFR | Blocks renal-risk attribution/escalation; basic urate-context finding still emits |
| Urate vs uric acid naming | Existing convention only; no new alias |
| Creatinine / urea | Unchanged compiled authority |

## 3. Files changed (implementation)

- `knowledge_bus/governance/compiled_why_authority_register_v1.yaml`
- `backend/core/knowledge/why_authority_v1.py`
- `knowledge_bus/compiled/hypotheses/inv_uric_acid_high_metabolic.yaml`
- `knowledge_bus/compiled/manifests/arch_conv_g_urate_high.yaml`
- `knowledge_bus/compiled/estate_index_v1.yaml`
- `knowledge_bus/governance/root_cause_authority_register_v1.yaml`
- `backend/scripts/validate_compiled_why_authority_gate.py`
- `backend/tests/regression/test_arch_conv_g_urate_stop_c.py`
- `backend/tests/regression/test_arch_conv_b_renal_stop_c.py` (urate exclusion updated for G migration)
- `backend/tests/unit/test_why_authority_pkg3.py`
- `backend/tests/unit/test_arch_rt5_launch_gate.py`
- Gate / evidence / Build Deliverables / Active Carry-Forward docs

Unchanged: compiler, root_cause_registry, packages, PSI, SSOT, frontend, creatinine/urea artefacts.

## 4. Before / after counts

| Metric | Before | After | Delta |
|---|---|---|---|
| `COMPILED_ACTIVE` | 23 | 24 | **+1** |
| `LEGACY_RETIRED` | 18 | 19 | **+1** |
| `REJECTED` | 1 | 1 | 0 |
| Total frames | 42 | 44 | +2 |
| Loaded compiled frames | 23 | 24 | +1 |

## 5. Hashes

| Artefact | SHA-256 |
|---|---|
| Source `inv_uric_acid_high_metabolic.yaml` | `A7EDEF6EE3C28A4DA8BE1D79A2F5E36B0F80F7AF5C7B7E5A140418208FC078CD` |
| Compiled `inv_uric_acid_high_metabolic.yaml` | `9B67D762CC7C8F80A4E71AE0FAA7C182925C178D25AA0093204A684D2DFEF9F2` |

## 6. Validators / tests

```text
python backend/scripts/validate_compiled_why_authority_gate.py
→ PASS frames=44 compiled_active=24 rejected=1 legacy_retired=19

python backend/scripts/validate_knowledge_package.py --package-dir knowledge_bus/packages/pkg_s24_urate_high_metabolic
→ PASS

python backend/scripts/validate_knowledge_package.py --package-dir knowledge_bus/packages/pkg_kb52c_urate_high_gout_crystal_deposition_risk
→ PASS

python -m pytest backend/tests/regression/test_arch_conv_g_urate_stop_c.py \
  backend/tests/regression/test_arch_conv_b_renal_stop_c.py \
  backend/tests/unit/test_why_authority_pkg3.py \
  backend/tests/unit/test_arch_rt5_launch_gate.py -q
→ passed

python -m pytest backend/tests/regression/test_arch_conv_a_wave1_thyroid_stop_c.py \
  backend/tests/regression/test_arch_conv_a_wave2_lipid_stop_c.py \
  backend/tests/regression/test_arch_conv_c_alp_ggt_stop_c.py \
  backend/tests/regression/test_arch_conv_f_haematology_stop_c.py -q
→ passed (see closure evidence)
```

## 7. Proof statements

- No runtime research-file read introduced (static check in G suite).
- Package / PSI paths unchanged (`git diff` empty under packages).
- No new medical rule/threshold invented; eGFR `<60` override pre-existing.
- Deterministic repeatability asserted.
- No forged approvals; Gate refs recorded before implementation resume.

## 8. Closure posture

Finish after evidence commit. Kernel COMPLETE status commit per SOP §6.8.1. No merge by Cursor.
