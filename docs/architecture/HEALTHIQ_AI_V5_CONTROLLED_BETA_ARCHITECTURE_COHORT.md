# HealthIQ AI v5 — Controlled-Beta Architecture Cohort

**Work ID:** `ARCH-CONV-GATE0`  
**Branch:** `feature/arch-conv-gate0-cohort-viability`  
**Baseline HEAD:** `d798beab9b2bb7dcad9b48ed0f0a4f0153be8948`  
**Status:** PROPOSED — awaiting human ratification  
**Authority:** Gate 0 of `docs/planning-papers/HEALTHIQ_AI_V5_FINAL_ARCHITECTURE_CONVERGENCE_AND_SALVAGE_OR_REBUILD_PLAN.md`  
**Does not authorise:** controlled beta, Package 1 implementation, medical-content promotion, or beta-readiness declaration

---

## 1. Purpose

Enumerate the exact architecture cohort that must be made identity-safe, provenance-honest, and WHY-bounded before any controlled-beta claim.

This document is a planning inventory. Dispositions are recommendations for human approval. They do not change runtime behaviour.

---

## 2. Cohort boundary definition

### In scope (architecture-critical)

| Layer | Boundary rule | Evidence basis |
|---|---|---|
| Product surface | Six Wave 1 consumer domains | Baseline 2026-07-25 §6; `domain_score_assembler.py` |
| Launch-critical provenance | All `pkg_kb47_*` packages (gate prefix) | `validate_identity_provenance_gate.py`; ARCH-RT-IDENTITY-PROV-1 inventory |
| Identity pressure | Multi-frame families that can reach the five residual consumers | Live registry + consumer code inspection |
| WHY anchor | Existing compiled pilot + bounded legacy targets for Package 3 | `compiled_hypothesis.py`; `root_cause_registry_v1.py` |

### Explicitly out of scope for this architecture cohort

- Estate-wide migration of all **139** signal families / **197** activation frames
- Full migration of all **40** legacy WHY YAML assets
- PSI wiring, prose generation, MR-BATCH-001B promotion
- Frontend-only product polish

### Live estate counts (verified this package)

| Metric | Count | Method |
|---|---:|---|
| Activation keys | **197** | `SignalRegistry.get_all_signals()` |
| Unique signal families | **139** | unique `signal_id` |
| Multi-frame families | **51** | families with >1 activation key |
| `pkg_kb47_*` packages / frames | **20 / 20** | disk + registry |
| Launch-critical inventory BLOCKED rows | **16** | ARCH-RT-IDENTITY-PROV-1 inventory |
| Explicit manifest `source_spec_id` | **0** | prior reconciliation; unchanged premise |
| Compiled WHY / legacy YAML / registry targets | **1 / 40 / 41** | estate + registry |

---

## 3. Recommended cohort tiers

| Tier | Meaning | Architecture implication |
|---|---|---|
| **INCLUDE** | Must be covered by Packages 1–2 before any beta claim that depends on that surface | Identity + provenance honesty required |
| **REQUIRES_LINEAGE** | May remain loadable, but cannot support an explicit beta claim until lineage is attached | Package 2 EXTRACT_AND_ATTACH |
| **REQUIRES_MEDICAL_REVIEW** | Architecture may proceed; beta claim blocked pending medical/context gate | Not an engineering-only close |
| **DEFER** | Not required for the initial controlled-beta architecture claim | Remain loadable unless a later product decision says otherwise |
| **EXCLUDE** | Outside Gate 0 architecture cohort | Do not pull into Packages 1–3 by default |
| **UNVERIFIABLE** | Evidence insufficient for a silent estimate | Escalate; do not invent |

---

## 4. Exact launch-critical inventory (`pkg_kb47_*`)

All **20/20** packages:

- have `signal_library.yaml` and load via `SignalRegistry` (no provenance filter);
- carry inferred `source_spec_id` / `activation_key` at load time;
- have canonical Pass 3 content recoverable from `knowledge_bus/research/investigation_specs/multi_llm_research/Batch_2_Pass_3.json` (`batch=True` for every row below);
- lack standalone `inv_*.yaml` extraction today (`yaml=False`).

Current firing status is **loadable / can evaluate when biomarkers present**. Representative/golden fixture files do **not** name `pkg_kb47` packages; whether a live golden run emits these signals is **UNVERIFIABLE without re-running golden outputs** (fixtures contain no package_id strings).

| signal_id | activation_key | source_spec_id | biomarker / domain | package_id | runtime reachability | current firing status | launch relevance | provenance status | explicit lineage availability | WHY authority type | medical-review requirement | recommended disposition |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| signal_creatine_kinase_high | signal_creatine_kinase_high::inv_creatine_kinase_high_exertional_muscle_injury | inv_creatine_kinase_high_exertional_muscle_injury | creatine_kinase / muscle | pkg_kb47_creatine_kinase_high_exertional_muscle_injury | loadable | evaluates if CK present | launch-critical prefix; not Wave 1 domain | BLOCKED | Recoverable from Batch_2_Pass_3.json | none in root-cause registry | Required before beta claim | REQUIRES_LINEAGE + DEFER from Wave 1 beta surface |
| signal_creatine_kinase_high | signal_creatine_kinase_high::inv_creatine_kinase_high_persistent_nonexertional_muscle_injury | inv_creatine_kinase_high_persistent_nonexertional_muscle_injury | creatine_kinase / muscle | pkg_kb47_creatine_kinase_high_persistent_nonexertional_muscle_injury | loadable | evaluates if CK present | launch-critical prefix; multi-frame peer | BLOCKED | Recoverable from Batch_2_Pass_3.json | none in root-cause registry | Required before beta claim | REQUIRES_LINEAGE + DEFER from Wave 1 beta surface |
| signal_dhea_high | signal_dhea_high::inv_dhea_high_androgen_excess_context | inv_dhea_high_androgen_excess_context | dhea / androgen | pkg_kb47_dhea_high_androgen_excess_context | loadable | context-gated historically | androgen panel | BLOCKED | Recoverable from Batch_2_Pass_3.json | none in root-cause registry | BATCH2-MEDREVIEW-1 reviewed; still context-blocked | REQUIRES_LINEAGE + REQUIRES_MEDICAL_REVIEW |
| signal_dhea_low | signal_dhea_low::inv_dhea_low_adrenal_androgen_reduction | inv_dhea_low_adrenal_androgen_reduction | dhea / androgen | pkg_kb47_dhea_low_adrenal_androgen_reduction | loadable | context-gated historically | androgen panel | batch_json_blocked class (not in 16-row inventory table) | Recoverable from Batch_2_Pass_3.json | none | BATCH2-MEDREVIEW-1 | REQUIRES_LINEAGE + REQUIRES_MEDICAL_REVIEW |
| signal_egfr_low | signal_egfr_low::inv_egfr_low_chronic_kidney_function_reduction | inv_egfr_low_chronic_kidney_function_reduction | egfr / kidney Wave 1 | pkg_kb47_egfr_low_chronic_kidney_function_reduction | loadable | evaluates if egfr present | **Wave 1 kidney** | BLOCKED | Recoverable from Batch_2_Pass_3.json | none in root-cause registry | Required before beta claim on kidney card | **INCLUDE** + REQUIRES_LINEAGE |
| signal_egfr_low | signal_egfr_low::inv_egfr_low_hemodynamic_filtration_drop | inv_egfr_low_hemodynamic_filtration_drop | egfr / kidney Wave 1 | pkg_kb47_egfr_low_hemodynamic_filtration_drop | loadable | evaluates if egfr present | **Wave 1 kidney**; multi-frame peer | BLOCKED | Recoverable from Batch_2_Pass_3.json | none in root-cause registry | Required before beta claim | **INCLUDE** + REQUIRES_LINEAGE |
| signal_eosinophil_pct_high | signal_eosinophil_pct_high::inv_eosinophil_pct_high_reactive_atopic_eosinophilia | inv_eosinophil_pct_high_reactive_atopic_eosinophilia | eosinophil_pct / haematology | pkg_kb47_eosinophil_pct_high_reactive_atopic_eosinophilia | loadable | evaluates if eosinophils present | launch-critical prefix; not Wave 1 domain | BLOCKED | Recoverable from Batch_2_Pass_3.json | none | Required before beta claim | REQUIRES_LINEAGE + DEFER from Wave 1 beta surface |
| signal_eosinophil_pct_high | signal_eosinophil_pct_high::inv_eosinophil_pct_high_secondary_or_systemic_eosinophilia | inv_eosinophil_pct_high_secondary_or_systemic_eosinophilia | eosinophil_pct / haematology | pkg_kb47_eosinophil_pct_high_secondary_or_systemic_eosinophilia | loadable | evaluates if eosinophils present | multi-frame peer | BLOCKED | Recoverable from Batch_2_Pass_3.json | none | Required before beta claim | REQUIRES_LINEAGE + DEFER from Wave 1 beta surface |
| signal_eosinophils_abs_high | signal_eosinophils_abs_high::inv_eosinophils_abs_high_hypereosinophilic_or_secondary_eosinophilia | inv_eosinophils_abs_high_hypereosinophilic_or_secondary_eosinophilia | eosinophils_abs / haematology | pkg_kb47_eosinophils_abs_high_hypereosinophilic_or_secondary_eosinophilia | loadable | evaluates if eosinophils present | launch-critical prefix | BLOCKED | Recoverable from Batch_2_Pass_3.json | none | Required before beta claim | REQUIRES_LINEAGE + DEFER from Wave 1 beta surface |
| signal_eosinophils_abs_high | signal_eosinophils_abs_high::inv_eosinophils_abs_high_reactive_eosinophilic_inflammation | inv_eosinophils_abs_high_reactive_eosinophilic_inflammation | eosinophils_abs / haematology | pkg_kb47_eosinophils_abs_high_reactive_eosinophilic_inflammation | loadable | evaluates if eosinophils present | multi-frame peer | BLOCKED | Recoverable from Batch_2_Pass_3.json | none | Required before beta claim | REQUIRES_LINEAGE + DEFER from Wave 1 beta surface |
| signal_fai_high | signal_fai_high::inv_fai_high_biochemical_hyperandrogenism | inv_fai_high_biochemical_hyperandrogenism | fai / androgen | pkg_kb47_fai_high_biochemical_hyperandrogenism | loadable | context-gated historically | androgen panel | BLOCKED | Recoverable from Batch_2_Pass_3.json | none | BATCH2-MEDREVIEW-1 | REQUIRES_LINEAGE + REQUIRES_MEDICAL_REVIEW |
| signal_fai_low | signal_fai_low::inv_fai_low_reduced_free_androgen_availability | inv_fai_low_reduced_free_androgen_availability | fai / androgen | pkg_kb47_fai_low_reduced_free_androgen_availability | loadable | context-gated historically | androgen panel | batch_json_blocked class | Recoverable from Batch_2_Pass_3.json | none | BATCH2-MEDREVIEW-1 | REQUIRES_LINEAGE + REQUIRES_MEDICAL_REVIEW |
| signal_free_t3_high | signal_free_t3_high::inv_free_t3_high_t3_predominant_thyrotoxicosis | inv_free_t3_high_t3_predominant_thyrotoxicosis | free_t3 / thyroid Wave 1 | pkg_kb47_free_t3_high_t3_predominant_thyrotoxicosis | loadable | evaluates if free_t3 present | **Wave 1 thyroid** | BLOCKED | Recoverable from Batch_2_Pass_3.json | legacy YAML | Required before beta claim | **INCLUDE** + REQUIRES_LINEAGE |
| signal_free_t3_low | signal_free_t3_low::inv_free_t3_low_low_t3_syndrome | inv_free_t3_low_low_t3_syndrome | free_t3 / thyroid Wave 1 | pkg_kb47_free_t3_low_low_t3_syndrome | loadable | evaluates if free_t3 present | **Wave 1 thyroid**; narrative lead hint | BLOCKED | Recoverable from Batch_2_Pass_3.json | legacy YAML | Required before beta claim | **INCLUDE** + REQUIRES_LINEAGE |
| signal_free_t4_high | signal_free_t4_high::inv_free_t4_high_thyrotoxicosis_context | inv_free_t4_high_thyrotoxicosis_context | free_t4 / thyroid Wave 1 | pkg_kb47_free_t4_high_thyrotoxicosis_context | loadable | evaluates if free_t4 present | **Wave 1 thyroid** | BLOCKED | Recoverable from Batch_2_Pass_3.json | legacy YAML | Required before beta claim | **INCLUDE** + REQUIRES_LINEAGE |
| signal_free_t4_low | signal_free_t4_low::inv_free_t4_low_thyroid_hormone_deficiency | inv_free_t4_low_thyroid_hormone_deficiency | free_t4 / thyroid Wave 1 | pkg_kb47_free_t4_low_thyroid_hormone_deficiency | loadable | evaluates if free_t4 present | **Wave 1 thyroid** | BLOCKED | Recoverable from Batch_2_Pass_3.json | legacy YAML | Required before beta claim | **INCLUDE** + REQUIRES_LINEAGE |
| signal_free_testosterone_high | signal_free_testosterone_high::inv_free_testosterone_high_androgen_excess_context | inv_free_testosterone_high_androgen_excess_context | free_testosterone / androgen | pkg_kb47_free_testosterone_high_androgen_excess_context | loadable | context-gated historically | androgen panel | BLOCKED | Recoverable from Batch_2_Pass_3.json | none | BATCH2-MEDREVIEW-1 | REQUIRES_LINEAGE + REQUIRES_MEDICAL_REVIEW |
| signal_free_testosterone_low | signal_free_testosterone_low::inv_free_testosterone_low_androgen_deficiency_context | inv_free_testosterone_low_androgen_deficiency_context | free_testosterone / androgen | pkg_kb47_free_testosterone_low_androgen_deficiency_context | loadable | context-gated historically | androgen panel | BLOCKED | Recoverable from Batch_2_Pass_3.json | none | BATCH2-MEDREVIEW-1 | REQUIRES_LINEAGE + REQUIRES_MEDICAL_REVIEW |
| signal_free_testosterone_pct_high | signal_free_testosterone_pct_high::inv_free_testosterone_pct_high_elevated_free_androgen_fraction | inv_free_testosterone_pct_high_elevated_free_androgen_fraction | free_testosterone_pct / androgen | pkg_kb47_free_testosterone_pct_high_elevated_free_androgen_fraction | loadable | context-gated historically | androgen panel | batch_json_blocked class | Recoverable from Batch_2_Pass_3.json | none | BATCH2-MEDREVIEW-1 | REQUIRES_LINEAGE + REQUIRES_MEDICAL_REVIEW |
| signal_free_testosterone_pct_low | signal_free_testosterone_pct_low::inv_free_testosterone_pct_low_reduced_free_androgen_fraction | inv_free_testosterone_pct_low_reduced_free_androgen_fraction | free_testosterone_pct / androgen | pkg_kb47_free_testosterone_pct_low_reduced_free_androgen_fraction | loadable | context-gated historically | androgen panel | batch_json_blocked class | Recoverable from Batch_2_Pass_3.json | none | BATCH2-MEDREVIEW-1 | REQUIRES_LINEAGE + REQUIRES_MEDICAL_REVIEW |

**Plus non-kb47 beta-eligible inventory row:**

| signal_id | activation_key | source_spec_id | package_id | provenance | WHY | disposition |
|---|---|---|---|---|---|---|
| signal_vitamin_d_low | signal_vitamin_d_low::inv_vitamin_d_low_deficiency | inv_vitamin_d_low_deficiency | pkg_s24_vitamin_d_low_deficiency | COMPILED_MANIFEST / beta_eligible True | **compiled** (runtime-promoted) | **INCLUDE** (WHY pilot anchor) |

---

## 5. Wave 1 identity-pressure multi-frame families (INCLUDE for Package 1)

These families are **INCLUDE** for activation-frame identity closure because they are multi-frame and intersect Wave 1 domains and/or narrative lead selection.

| signal_id | frames (LIVE) | Wave 1 / lead surface | WHY authority | Package 1 relevance | disposition |
|---|---:|---|---|---|---|
| signal_homocysteine_high | 3 | CV rail + `_LEAD_SIGNAL_HINTS` | legacy (`hcy_hypotheses_v1.yaml`) | High — lead + multi-frame collapse risk | INCLUDE |
| signal_mcv_high | 3 | adjacent haematology; `_LEAD_SIGNAL_HINTS` | legacy | High — lead + multi-frame | INCLUDE |
| signal_iron_low | 2 | Wave 1 blood iron oxygen | context/legacy iron assets | High — Wave 1 launch set | INCLUDE |
| signal_tpo_ab_high | 2 | Wave 1 thyroid | legacy | High — Wave 1 thyroid | INCLUDE |
| signal_egfr_low | 2 | Wave 1 kidney | none | High — Wave 1 + kb47 BLOCKED | INCLUDE + REQUIRES_LINEAGE |
| signal_alt_high | 4 | Wave 1 liver | legacy ALT/hepatic assets | High — liver multi-frame | INCLUDE |
| signal_ferritin_high | 3 | iron/hepatic adjacency | legacy | Medium-high | INCLUDE |
| signal_creatinine_high | 2 | Wave 1 kidney | legacy | High — Wave 1 kidney | INCLUDE |

Additional multi-frame families exist estate-wide (**51** total). They are **DEFER** unless they enter a Wave 1 predicate or lead-hint path during Package 1 adversarial testing.

---

## 6. Activation-frame inventory (architecture cohort summary)

| Cohort slice | Signal families | Activation frames | Active multi-frame in slice |
|---|---:|---:|---:|
| Wave 1 thyroid launch IDs | 7 (`_THYROID_LAUNCH_SIGNAL_IDS`) | 7 single-frame + multi-frame tpo only among them | 1 (`signal_tpo_ab_high`) |
| Wave 1 blood iron oxygen launch IDs | 3 | 4 (iron_low×2, iron_high×1, transferrin_high×1) | 1 |
| Wave 1 kidney core (`egfr`/`creatinine`) | 2+ | ≥4 | ≥2 |
| Launch-critical kb47 | 16 families | 20 | 4 (CK, egfr, eos pct, eos abs) |
| kb47 ∩ Wave 1 (thyroid+kidney) INCLUDE core | 6 families | 6 frames (4 thyroid single + egfr×2) | 1 (`egfr_low`) |
| Proposed Package 1 pressure set (§5) | 8 families | 22 frames | 8 |

---

## 7. Inclusions and exclusions (decision view)

### INCLUDE for controlled-beta architecture claim (proposed)

1. Six Wave 1 domain surfaces and their launch signal sets as wired today.
2. Package 1 pressure multi-frame families in §5.
3. kb47 thyroid + egfr frames (Wave 1 overlap) after lineage attach or honest non-claim.
4. `signal_vitamin_d_low` compiled WHY path.

### REQUIRES_LINEAGE before any explicit beta claim on those packages

All **16** BLOCKED inventory rows (and the **4** additional kb47 androgen/`pct` packages in the same batch-JSON class).

Recommended Package 2 action for Wave 1-overlapping BLOCKED rows: **EXTRACT_AND_ATTACH**.  
Recommended action for non-Wave-1 BLOCKED rows until product decides otherwise: **EXTRACT_AND_ATTACH** *or* **EXCLUDE_FROM_BETA_COHORT** (keep loadable; no beta claim). Do **not** remove in Gate 0.

### REQUIRES_MEDICAL_REVIEW

Androgen panel (`dhea` / `fai` / `free_testosterone` / `pct`) — historical BATCH2-MEDREVIEW-1 exists; context modifier / clinical sign-off still open.

### DEFER from initial beta surface

CK and eosinophil kb47 families (launch-critical for provenance gate, not Wave 1 domain cards).

### EXCLUDE from architecture packages 1–3 by default

Estate remainder outside Wave 1 + launch-critical kb47 + WHY pilot (do not attempt all 40 legacy hypotheses; do not regenerate `pkg_kb52c_*` estate in this programme).

---

## 8. Unresolved evidence

| Item | Status |
|---|---|
| Concurrent live multi-frame firing that reaches all five consumers in production traffic | UNVERIFIABLE as product fact; mechanism defect verified |
| Golden/representative **output** dependence on BLOCKED kb47 packages | UNVERIFIABLE without golden re-run (fixtures have no package_id mentions) |
| Medical-review owner / capacity for WHY pilot | UNRESOLVED — see viability assessment |
| Product policy: suppress vs attach for non-Wave-1 BLOCKED packages | Requires human product decision (not invented here) |
| Exact Wave 1 CV/metabolic/liver predicate signal census as a frozen list | Predicate-based (not a frozen allow-list) except thyroid/iron sets |

---

## 9. Quantitative totals (this document)

| Item | Count |
|---|---:|
| Proposed beta signal families (architecture INCLUDE core, Wave 1 + §5 + vitamin_d) | **≈15–25** families (predicate-bounded; exact CV/liver sets are runtime-predicate, not a frozen enum) |
| Launch-critical kb47 frames | **20** |
| BLOCKED inventory rows | **16** |
| kb47 frames with recoverable batch lineage | **20 / 20** |
| Activation frames estate-wide | **197** |
| Multi-frame families estate-wide | **51** |
| Multi-frame families in Package 1 pressure set | **8** |

Where a single frozen Wave 1 allow-list count is requested for CV/liver/metabolic: **not reliable** — those domains use predicate functions, not frozensets (unlike thyroid/iron).
