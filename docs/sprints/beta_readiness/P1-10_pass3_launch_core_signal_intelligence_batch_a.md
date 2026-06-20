# P1-10 — Pass 3 Launch-Core Signal Intelligence Batch A

## 1. Executive summary

- **Why this sprint was run:** P1-9 quantified a rich Pass 3 research estate with a large unpromoted signal-intelligence tail. P1-10 is the first governed batch promotion of that research into the `promoted_signal_intelligence` contract without runtime activation.
- **What Batch A promoted:** **16** new `promoted_signal_intelligence.yaml` artefacts across **5** launch-core clusters (lipid derived, homocysteine/one-carbon, liver enzymes, kidney urea, ApoB/non-HDL depth), staged under `knowledge_bus/generated_pilot/p1_10_batch_a/`. A **6th** cluster (kidney eGFR) was classified as **enriched** — production kb47 PSI already exists; scoring remains blocked per P1-9.
- **Authoritative signal repository found?** **Yes.** Primary authority: per-package `promoted_signal_intelligence.yaml` opt-in via `package_manifest.yaml` (ADR-008). Batch A staging follows the KB-UTIL-2 pilot pattern in `knowledge_bus/generated_pilot/` with `runtime_active: false` compile manifests.
- **Runtime activation unchanged?** **Yes.** No manifest opt-in to production packages; no `governance_runtime_activation_status: runtime_active_*` on new artefacts; no scoring policy, DTO, assembler, or compiled card changes.
- **Estate-level value:** Deterministic Pass 3 → PSI translation preserves contradiction markers, supporting-marker roles, missing-data policies, override rules, and evidence blocks for 16 launch-core signals — establishing the repeatable batch promotion factory P1-9 recommended.
- **Recommended next sprint:** **P1-SCORING-HORMONAL-POLICY** (scoring blocker for eGFR/thyroid) plus **P1-11 — Pass 3 Signal Intelligence Batch B** (CBC/iron frame-adjudication cohort manifest opt-in).

## 2. Programme context

| Prior work | Relationship |
|---|---|
| Eight-block programme | Industrialises research → governed runtime promotion factory; P1-10 is first batch production use |
| P1-7 adequacy gate | Established runtime-facing promotion gaps Batch A addresses |
| P1-8 lab-range engine | Enables future scoring-policy entries; Batch A does not add policy |
| P1-9 exploitation map | Authoritative cluster selection and deferral rationale |

This sprint is **batch-based** (6 clusters, 16 PSI entries) rather than one-marker-at-a-time, matching P1-9 cohort strategy while respecting the 4–8 cluster ceiling.

## 3. Signal repository discovery

### Paths searched

`knowledge_bus/packages/`, `knowledge_bus/generated_pilot/`, `knowledge_bus/schema/`, `knowledge_bus/governance/`, `backend/core/knowledge/`, `backend/scripts/`, `docs/architecture/`, `docs/intelligence/`.

### Authoritative signal repository

| Layer | Path | Role |
|---|---|---|
| Production | `knowledge_bus/packages/<package_id>/promoted_signal_intelligence.yaml` | Governed PSI when manifest opts in |
| Staging (Batch A) | `knowledge_bus/generated_pilot/p1_10_batch_a/<package_id>/` | Non-runtime promoted PSI + compile manifest |
| Index | `knowledge_bus/generated_pilot/p1_10_batch_a/p1_10_batch_a_compile_manifest_index_v1.yaml` | Batch audit trail |

### Loader / validator

| Component | Path |
|---|---|
| Schema | `knowledge_bus/schema/promoted_signal_intelligence_schema_v1.yaml` |
| Validator | `backend/scripts/validate_promoted_signal_intelligence.py` |
| Loader | `backend/core/knowledge/load_promoted_signal_intelligence.py` |
| Translator | `backend/core/knowledge/investigation_spec_to_promoted_signal.py` |
| ADR | `architecture/ADR-008-promoted-signal-intelligence-contract-v1.md` |

### Duplicate / legacy authority check

- `signal_library.yaml` remains authoritative for **activation mechanics** at runtime.
- `intelligence_model.yaml` is a separate optional path (hypotheses allowed); not used in Batch A.
- `generated_pilot/kb_util_2_pilot/` is prior pilot staging — not overwritten; Batch A uses sibling `p1_10_batch_a/` root.
- No duplicate repository created.

### STOP concerns

None. Schema supports inactive staging via compile manifest `runtime_active: false`. Production packages were not modified (no accidental opt-in).

## 4. Batch A selection rationale

### Clusters considered (from P1-9)

Lipid derived, homocysteine, liver enzymes, kidney urea, kidney eGFR, ApoB depth, metabolic glycaemic residual, CBC/hematology, thyroid axis, thyroid antibodies, hormone/androgen, inflammation/eosinophil.

### Clusters selected (6)

| Cluster | Entries | Rationale |
|---|---|---|
| Lipid derived | 5 | P1-9 `RESEARCH_PRESENT_SIGNAL_INTELLIGENCE_MISSING`; kb60 packages lack PSI |
| Homocysteine / one-carbon | 2 | MED-REV-1 hidden subsystem; strong Batch_6 Pass 3 |
| Liver enzymes | 5 | MED-REV-1 hidden; ALT/GGT frames in Batch_5/6 |
| Kidney urea | 2 | Launch-adjacent; medical-review blocked but safe inactive PSI |
| ApoB / non-HDL depth | 2 | CV launch-core lipid depth gap |
| Kidney eGFR (reference) | 0 new | Existing kb47 PSI; `RESEARCH_PRESENT_SCORING_BLOCKED` |

### Clusters deferred (5)

CBC/hematology (frame adjudication), thyroid axis (scoring blocked), thyroid antibodies (governance), hormone/androgen (context model), inflammation/eosinophil (second-wave unmapped).

### Right-sized batch

16 PSI files across 6 programme clusters sits within P1-9 cohort discipline — meaningful breadth without sitewide mass promotion.

## 5. Pass 3 source inspection

### Lipid derived (`lipid_derived_pass_3.json`)

- **Specs inspected:** 5 matched to kb60 packages.
- **Biomarkers:** total_cholesterol, tc_hdl_ratio, ldl_cholesterol.
- **Themes:** atherogenic burden vs HDL-dominant elevation; hypocholesterolaemia context; TC:HDL discordance patterns; contradiction markers on ratio direction.
- **Limitations:** ApoB/Lp(a) specs in same file deferred to partial coverage via separate ApoB cluster.

### Homocysteine (`Batch_6_Pass_3.json`)

- **Specs:** B-vitamin methylation impairment; renal clearance reduction.
- **Biomarkers:** homocysteine, vitamin_b12, folate, creatinine.
- **Themes:** one-carbon cycle impairment; renal excretion context; corroborating B-vitamin markers.
- **Limitations:** folate/B12 standalone specs not in Batch A scope.

### Liver enzymes (`Batch_5_Pass_3.json`, `Batch_6_Pass_3.json`)

- **Specs:** ALT hepatocellular, metabolic steatotic, muscle/exertional; GGT cholestatic, alcohol/induction.
- **Biomarkers:** alt, ggt, ast, alp (referenced in supporting markers).
- **Themes:** differential injury vs steatosis vs muscle source; cholestatic vs enzyme induction patterns.
- **Limitations:** bilirubin/ALP frames not in this batch tranche.

### Kidney urea (`Batch_7_Pass_3.json`)

- **Specs:** urea high prerenal/catabolic; urea low protein/urea-cycle.
- **Biomarkers:** urea, albumin, creatinine.
- **Themes:** contextual urea interpretation; albumin corroboration; non-diagnostic framing.
- **Limitations:** medical-review and frame adjudication block runtime activation.

### ApoB / non-HDL (`Batch_5_Pass_3.json`, `Batch_7_Pass_3.json`)

- **Specs:** apob low hypobetalipoproteinemia; non-HDL high atherogenic burden.
- **Biomarkers:** apob, non_hdl_cholesterol, ldl_cholesterol.
- **Themes:** atherogenic lipoprotein pool; malabsorption differential.
- **Limitations:** Lp(a) specs deferred to Batch B.

### Kidney eGFR (reference only)

- **Pass 3:** Batch_2/6 eGFR specs — content cross-read against existing kb47 PSI.
- **Finding:** Production PSI already captures filtration reduction patterns; central blocker is scoring-policy wiring (P1-9 reclassification).

## 6. Promotion implementation

### Lipid derived (5 created)

| Package | State | Scoring | Med review | Runtime |
|---|---|---|---|---|
| pkg_kb60_total_cholesterol_high_atherogenic_hypercholesterolemia | staged inactive | partial | partial | unchanged |
| pkg_kb60_total_cholesterol_high_hdl_dominant_elevation_pattern | staged inactive | partial | partial | unchanged |
| pkg_kb60_total_cholesterol_low_hypocholesterolemia_context | staged inactive | partial | partial | unchanged |
| pkg_kb60_tc_hdl_ratio_high_atherogenic_discordance_pattern | staged inactive | partial | partial | unchanged |
| pkg_kb60_tc_hdl_ratio_low_hdl_dominant_pattern | staged inactive | partial | partial | unchanged |

- **Subsystem:** `wave1_cv_lipid_transport`
- **WHY substrate:** physiological_claim, threshold_notes, supporting_marker rationales preserved in PSI evidence block
- **Validation:** all 5 pass `validate_promoted_signal_intelligence.py`

### Homocysteine (2 created)

- **Subsystem:** `wave1_cv_homocysteine_methylation` (compiled hidden)
- **State:** inactive; med review required
- **Tests:** validator pass; no new runtime tests (staging only)

### Liver enzymes (5 created)

- **Subsystem:** hepatic enzyme / cholestatic patterns
- **State:** inactive; MED-REV-1 promotion pending
- **WHY:** contradiction markers for muscle-source ALT, alcohol GGT context preserved

### Kidney urea (2 created)

- **State:** blocked (medical review + adjudication)
- **Scoring:** partial; no policy change

### ApoB depth (2 created)

- **State:** inactive
- **Scoring:** ready on existing lipid scoring rails

### Kidney eGFR (enriched — no new files)

- **Reference:** `pkg_kb47_egfr_low_chronic_kidney_function_reduction`, `pkg_kb47_egfr_low_hemodynamic_filtration_drop`
- **State:** production PSI exists; runtime active on kb47 but scoring blocked for policy wiring sprint

## 7. Safety and non-activation confirmation

Confirmed:

- No runtime activation of newly staged PSI (no production manifest opt-in)
- No frontend / Gemini / fallback parser change
- No `scoring_policy.yaml` change
- No compiled card change
- No DTO / replay contract change
- No Pass 3 source file change
- No Knowledge Bus source package file change (`research_brief`, `signal_library`, `package_manifest` untouched)
- No global/default reference ranges or placeholder bands added
- No diagnostic or treatment claims introduced (PSI uses non-diagnostic physiological_claim framing from Pass 3)

## 8. Validation

| Check | Result |
|---|---|
| Manifest YAML parse | **PASS** |
| PSI validator (16 files) | **PASS** (all `validate_promoted_signal_intelligence.py`) |
| `runtime_active` in new compile manifests | **false** (16/16) |
| Production package manifests modified | **none** |
| `scoring_policy.yaml` diff | **none** |
| Backend runtime prohibited paths | **unchanged** |

### Limitations

- Staged PSI not yet wired to production manifests (intentional non-activation)
- No broad test suite run; validator is structural contract check only
- Kidney eGFR cluster documented by reference, not re-compiled

## 9. Business value delivered

- **Richness captured:** 16 Pass 3 investigation specs reduced to governed PSI with full signal-layer primitives (supporting markers, contradictions, missing-data policies, override rules, confirmatory tests, evidence).
- **Defensibility:** Deterministic translation via `investigation_spec_to_promoted_signal.py` with source hashes in compile manifests — auditable provenance chain.
- **Safety:** Promotion decoupled from activation; user-visible behaviour unchanged.
- **Pattern for future batches:** `generated_pilot/p1_10_batch_a/` + compile index + manifest opt-in as separate activation sprint.

## 10. Carry-forwards

| Item | Blocker type |
|---|---|
| CBC / iron / oxygen cluster | Frame adjudication |
| Thyroid axis + antibodies | Scoring policy + TSH authority |
| Hormone / androgen | Context model |
| Inflammation / eosinophil | Second-wave mapping |
| Batch A manifest opt-in to production | Medical review + dedicated wiring sprint |
| eGFR scoring policy | P1-SCORING-HORMONAL-POLICY / eGFR policy cohort |
| Prose / WHY consumer uplift | Separate prose sprint |

## 11. Recommended next sprint

### P1-SCORING-HORMONAL-POLICY

| Field | Value |
|---|---|
| risk_level | HIGH |
| change_type | MIXED |
| scope | Populate hormonal `lab_range_only` scoring-policy entries; TSH authority; no FT3/antibody activation |
| STOP gates | No thyroid domain card; no antibody launch; no FT3 low activation |
| rationale | Closes P1-9 cohort 1 blocker; prerequisite for thyroid Pass 3 monetisation |

### P1-11 — Pass 3 Signal Intelligence Batch B (parallel after policy sprint starts)

| Field | Value |
|---|---|
| risk_level | STANDARD |
| change_type | CONTENT |
| scope | CBC/iron frame-adjudication cohort PSI + manifest opt-in for cleared Batch A lipid/liver entries |
| STOP gates | No KB-S57-blocked WBC activation; no runtime activation without explicit authorisation |
| rationale | Continues batch factory; unlocks P1-3 blood/iron depth |

Machine-readable manifest: `docs/sprints/beta_readiness/P1-10_signal_intelligence_batch_a_manifest.yaml`
