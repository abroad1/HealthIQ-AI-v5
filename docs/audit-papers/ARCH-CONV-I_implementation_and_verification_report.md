# ARCH-CONV-I — Implementation and Verification Report

**Work ID:** `ARCH-CONV-I`  
**Branch:** `feature/arch-conv-i-alt-compiled-why-identity-resolution`  
**Risk / change type:** HIGH / MIXED  
**Gate 1:** `ARCH-CONV-I-GATE1-HMR-2026-08-02` (`APPROVED_WITH_NARROWING`, Outcome A `MAP_AND_COMPILE`)  
**Gate 2:** `ARCH-CONV-I-GATE2-ANTHONY-2026-08-02` (`APPROVED`)  
**Hardening:** `automation_bus/latest_prompt_hardening.json` — `HARDENED`  
**Implementation owner:** Cursor (`healthiq-core-engine`)

## 1. Baseline proof

| Check | Result |
|---|---|
| Phase 0 baseline counts | `COMPILED_ACTIVE=25`, `LEGACY_RETIRED=20`, `REJECTED=1`, frames=46 |
| ALT / hepatic_alt compiled rows | Absent before implementation |
| Active WP | Resumed without re-`start` after Gate 2 recording |
| Stash | Empty throughout |

## 2. Source-to-runtime rule map

| Ratified rule | Runtime representation |
|---|---|
| `signal_alt_high::inv_alt_high_r_value_hepatocellular_biochemical_pattern` | `COMPILED_ACTIVE` + artefact |
| `why_role: morphology_context` | Flat register role |
| CRP / inflammatory-coupling | Excluded from artefact and transfer |
| Hard-coded AST/GGT/ALP/bilirubin thresholds | Absent from artefact |
| `signal_hepatic_alt_context::inv_alt_context` | `LEGACY_RETIRED` → `skip` |
| Live E2/E3 sibling `signal_alt_high` frames | `LEGACY_RETIRED` WHY-skip only; packages unchanged |
| No runtime alias | Separate signal_ids; no alias code |
| Prohibited claims | Artefact caveats + regression suite |

## 3. Files changed (implementation)

- `knowledge_bus/governance/compiled_why_authority_register_v1.yaml`
- `backend/core/knowledge/why_authority_v1.py`
- `backend/core/knowledge/root_cause_registry_v1.py`
- `backend/core/knowledge/load_root_cause_hypotheses.py`
- `knowledge_bus/root_cause/hypotheses/alt_high_hypotheses_v1.yaml` (registry stub only)
- `knowledge_bus/compiled/hypotheses/inv_alt_high_r_value_hepatocellular_biochemical_pattern.yaml`
- `knowledge_bus/compiled/manifests/arch_conv_i_alt_high_hepatocellular.yaml`
- `knowledge_bus/compiled/estate_index_v1.yaml`
- `knowledge_bus/governance/root_cause_authority_register_v1.yaml`
- `backend/scripts/validate_compiled_why_authority_gate.py`
- `backend/tests/regression/test_arch_conv_i_alt_stop_c.py`
- `backend/tests/unit/test_root_cause_v1_homocysteine.py` (ALT emission / retirement)
- `backend/tests/fixtures/panels/phenotypes/phenotype_expectations_v1.yaml`
- `backend/tests/unit/test_why_authority_pkg3.py`
- `backend/tests/unit/test_arch_rt5_launch_gate.py`
- Gate / evidence / Build Deliverables / Active Carry-Forward docs

Unchanged: compiler algorithm, packages, PSI, SSOT, frontend, R-value formula/bands, ALP/GGT primary authority.

## 4. Before / after counts

| Metric | Before | After | Delta |
|---|---|---|---|
| `COMPILED_ACTIVE` | 25 | 26 | **+1** |
| `LEGACY_RETIRED` | 20 | 25 | **+5** |
| `REJECTED` | 1 | 1 | 0 |
| Total frames | 46 | 52 | +6 |

(+1 hepatocellular active; +1 legacy hepatic_alt retirement; +4 sibling WHY-skip rows)

## 5. Hashes

| Artefact | SHA-256 |
|---|---|
| Source Pass 3 JSON | `7F20BF9A06B3427217AD7F753C4D9304E5D5A2C46C484699257778844B9D3267` |
| Compiled hepatocellular artefact | `8BB7624C10130EF231BEF9C63833700DC1A7AF56E49B3AD8935AE9973E1540EB` |

## 6. Validators / tests

```text
python backend/scripts/validate_compiled_why_authority_gate.py
→ PASS frames=52 compiled_active=26 rejected=1 legacy_retired=25

Focused ARCH-CONV-I + F/G/H + phenotype suites — see closure evidence.
```

## 7. Proof statements

- No runtime research-file read introduced.
- Package / PSI paths unchanged.
- No new medical rule/threshold invented; R-bands remain signal-layer.
- Sibling fail-closed hazard closed with WHY-skip rows only.
- Deterministic repeatability asserted.
- No forged approvals; Gate refs recorded before implementation resume.

## 8. Closure posture

Finish succeeded; kernel COMPLETE committed. Merged and published under explicit human authority.

## 9. Post-Implementation Closure (published)

| Check | Result |
|---|---|
| Branch at finish | `feature/arch-conv-i-alt-compiled-why-identity-resolution` |
| Working tree at merge | Clean |
| Stash | Empty |
| Tooling leakage | None in sprint commits |
| Merge commit | `bd04648` — `merge: ARCH-CONV-I ALT compiled-WHY identity resolution (Gate 2 ratified)` |
| Publish | `main` → `origin/main` |
| Equality | Verified after publish |
| Feature branch (local) | Retained: `feature/arch-conv-i-alt-compiled-why-identity-resolution` |
| Active WP token | Cleared |
