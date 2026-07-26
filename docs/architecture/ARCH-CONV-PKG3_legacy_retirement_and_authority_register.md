# ARCH-CONV-PKG3 — Legacy Retirement and Authority Register

**Work ID:** `ARCH-CONV-PKG3`  
**Status:** **ACTIVE — Gate C ratified; Phase 5 retirement recorded**  
**Anthony ratification date (UTC):** 2026-07-26  
**Ratification artefact:** `docs/Medical Research Documents/HEALTHIQ_AI_V5_WHY_PILOT_CONSOLIDATED_MEDICAL_REVIEW.md`  
**Runtime register:** `knowledge_bus/governance/compiled_why_authority_register_v1.yaml`

Legacy YAML files remain on disk for evidence/history. Runtime selection uses the authority register only. No dual compiled+legacy runtime authority is permitted for the same `activation_key`.

| activation_key | prior authority | replacement authority | retirement work_id | date (UTC) | notes |
|---|---|---|---|---|---|
| `signal_vitamin_d_low::inv_vitamin_d_low_deficiency` | Legacy YAML + compiled dual posture | `COMPILED_ACTIVE` → `signal_vitamin_d_low.yaml` | ARCH-CONV-PKG3 | 2026-07-26 | `LEGACY_RETIRED`; loader retained on disk; not selected when register is COMPILED_ACTIVE |
| `signal_homocysteine_high::inv_homocysteine_high_b_vitamin_related_methylation_impairment` | Shared `hcy_hypotheses_v1.yaml` | `COMPILED_ACTIVE` → `inv_homocysteine_high_b_vitamin_related_methylation_impairment.yaml` | ARCH-CONV-PKG3 | 2026-07-26 | `LEGACY_RETIRED_FOR_FRAME`; inflammation/renal hyps excluded |
| `signal_homocysteine_high::inv_homocysteine_high_metabolic` | Shared `hcy_hypotheses_v1.yaml` | **Inactive (`REJECTED`)** | ARCH-CONV-PKG3 | 2026-07-26 | No compiled artefact; no WHY-engine fallback; not a catch-all |
| `signal_homocysteine_high::inv_homocysteine_high_renal_clearance_reduction` | Shared `hcy_hypotheses_v1.yaml` | `COMPILED_ACTIVE` → `inv_homocysteine_high_renal_clearance_reduction.yaml` | ARCH-CONV-PKG3 | 2026-07-26 | `LEGACY_RETIRED_FOR_FRAME` |
| `signal_mcv_high::inv_mcv_high_macrocytosis` | Shared `mcv_high_hypotheses_v1.yaml` | `COMPILED_ACTIVE` → `inv_mcv_high_macrocytosis.yaml` | ARCH-CONV-PKG3 | 2026-07-26 | Morphology anchor only |
| `signal_mcv_high::inv_mcv_high_megaloblastic_macrocytosis` | Shared `mcv_high_hypotheses_v1.yaml` | `COMPILED_ACTIVE` → `inv_mcv_high_megaloblastic_macrocytosis.yaml` | ARCH-CONV-PKG3 | 2026-07-26 | `LEGACY_RETIRED_FOR_FRAME` |
| `signal_mcv_high::inv_mcv_high_nonmegaloblastic_macrocytosis` | Shared `mcv_high_hypotheses_v1.yaml` | `COMPILED_ACTIVE` → `inv_mcv_high_nonmegaloblastic_macrocytosis.yaml` | ARCH-CONV-PKG3 | 2026-07-26 | `LEGACY_RETIRED_FOR_FRAME` |
| `signal_free_t3_low::inv_free_t3_low_low_t3_syndrome` | `free_t3_low_hypotheses_v1.yaml` | `COMPILED_ACTIVE` → `inv_free_t3_low_low_t3_syndrome.yaml` | ARCH-CONV-PKG3 | 2026-07-26 | `LEGACY_RETIRED` |
| `signal_tpo_ab_high::inv_tpo_ab_high_autoimmune_hypothyroid_pattern` | Shared `tpo_ab_high_hypotheses_v1.yaml` | `COMPILED_ACTIVE` → `inv_tpo_ab_high_autoimmune_hypothyroid_pattern.yaml` | ARCH-CONV-PKG3 | 2026-07-26 | `LEGACY_RETIRED_FOR_FRAME` |
| `signal_tpo_ab_high::inv_tpo_ab_high_euthyroid_autoimmune_risk` | Shared `tpo_ab_high_hypotheses_v1.yaml` | `COMPILED_ACTIVE` → `inv_tpo_ab_high_euthyroid_autoimmune_risk.yaml` | ARCH-CONV-PKG3 | 2026-07-26 | `LEGACY_RETIRED_FOR_FRAME` |

## Dual-authority prevention

1. Selection is per `activation_key` via `resolve_frame_why_authority`.  
2. `REJECTED` / deferred frames resolve to `skip` and do not receive WHY-engine fallback.  
3. Multi-frame pilot signals without `activation_key` fail closed (no bare `signal_id` collapse).  
4. Shared legacy YAML may remain loadable for out-of-pilot signals (e.g. `signal_homocysteine_elevation_context`) but is not selected for retired pilot frames.
