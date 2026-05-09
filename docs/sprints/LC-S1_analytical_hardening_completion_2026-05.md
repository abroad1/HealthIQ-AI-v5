# LC-S1 — Launch-core analytical hardening (completion note)

**Work package:** `LC-S1-ANALYTICAL-HARDENING`  
**Branch:** `feature/lc-s1-analytical-hardening`  
**Date:** 2026-05-09  

## 1. Approved launch-core signal slice (exact IDs)

Authoritative biology slice from the closed Pre-Sprint 1 gate (homocysteine / methylation / cardiometabolic / lipid cluster), expressed as **runtime `signal_id` values**:

| Gate / verification wording | Canonical runtime `signal_id` | LC-S1 WHY status |
|---------------------------|-----------------------------|------------------|
| Lead homocysteine context | `signal_homocysteine_elevation_context` | Existing `hcy_hypotheses_v1.yaml` (unchanged) |
| Rank-2 homocysteine leaf | `signal_homocysteine_high` | **Mapped** to same governed asset via `load_hcy_hypotheses_v1` |
| Rank-3 MCV | `signal_mcv_high` | **New** `mcv_high_hypotheses_v1.yaml` + compiler target |
| Rank-5 ApoA1 cardio | `signal_apoa1_cardio_risk` | **New** `apoa1_cardio_risk_hypotheses_v1.yaml` + compiler target (KB-S45d package-backed signal) |
| Rank-7 LDL (gate text `signal_ldl_high`) | **`signal_ldl_cholesterol_high`** | Existing `ldl_cholesterol_high_hypotheses_v1.yaml` — **canonical LDL lane ID** |
| VR co-primary ALP low | `signal_alp_low` | Existing `alp_low_hypotheses_v1.yaml` (unchanged) |
| VR co-primary cortisol pattern | `signal_hypercortisolism` | **New** `hypercortisolism_hypotheses_v1.yaml` + compiler target |

**Mandatory LDL naming resolution:** The gate pack shorthand “`signal_ldl_high`” corresponds to investigation/KB labelling in several YAML packages; the **root-cause compiler and phenotype edges use `signal_ldl_cholesterol_high`** as the fired dyslipidaemia leaf. No SSOT rename was performed in LC-S1.

**ApoA1 vs lipid-transport:** `signal_apoa1_cardio_risk` remains a **distinct registered leaf** (KB-S45d). Governed WHY here **complements** `signal_lipid_transport_dysfunction` where both fire; LC-S1 does **not** collapse ApoA1 into the lipid-transport narrative.

## 2. Assets added or updated

| Path | Change |
|------|--------|
| `knowledge_bus/root_cause/hypotheses/mcv_high_hypotheses_v1.yaml` | New governed WHY pack |
| `knowledge_bus/root_cause/hypotheses/apoa1_cardio_risk_hypotheses_v1.yaml` | New governed WHY pack |
| `knowledge_bus/root_cause/hypotheses/hypercortisolism_hypotheses_v1.yaml` | New governed WHY pack |
| `knowledge_bus/registries/confirmatory_tests_v1.yaml` | Added lipid-axis assets: `test_apoa1_repeat_panel_context_v1`, `test_apob_apoa1_repeat_coord_panel_v1`, `test_lipoprotein_a_serum_context_v1`, `test_cortisol_repeat_context_v1` |
| `backend/core/knowledge/load_root_cause_hypotheses.py` | Loaders for the three new packs |
| `backend/core/analytics/root_cause_compiler_v1.py` | Targets: `signal_homocysteine_high`, `signal_mcv_high`, `signal_apoa1_cardio_risk`, `signal_hypercortisolism` |
| `backend/tests/unit/test_lc_s1_root_cause_slice_signals.py` | Bounded regression |

## 3. Explicitly out of scope (unchanged)

- Statin / drug modifier engine and questionnaire expansion beyond proving minimum  
- Frontend / Layer C prose redesign  
- Broad WHY Wave 2 beyond this slice  

## 4. Follow-ons

- **Pre-Sprint 2 statin gate:** no modifier implementation started here.  
- Optional hygiene: align legacy KB/investigation strings that still say `signal_ldl_high` with runtime canonical naming in a **docs/KB-only** tranche (non-blocking for LC-S1).

## 5. A-1 correction (GPT — ApoB:ApoA1 ratio hypothesis)

`apoa1_ratio_adverse_pattern_v1` confirmatory tests remain **lipid / particle axis only**: **`test_apob_apoa1_repeat_coord_panel_v1`** (coordinated repeat ApoB + ApoA1) and **`test_lipoprotein_a_serum_context_v1`** (Lp(a) layering). Liver-enzyme and HbA1c registry entries are **not** used for this hypothesis.

## 6. Verification

- `python -m pytest tests/unit/test_lc_s1_root_cause_slice_signals.py` — PASS (local).
- `python -m pytest tests/unit/test_root_cause_v1_homocysteine.py::test_root_cause_v1_text_fields_respect_safety_denylist` — PASS (local).
