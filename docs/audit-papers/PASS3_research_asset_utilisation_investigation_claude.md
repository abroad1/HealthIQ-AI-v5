# Pass 3 Research Asset Utilisation Investigation

**Date:** 2026-05-28
**Author:** Claude Code (investigation only — no code changes)
**Scope:** Read-only codebase audit. No files modified.
**Companion:** `docs/audit-papers/PASS3_research_asset_utilisation_investigation_cursor.md` (Cursor-authored parallel investigation)

---

## 1. Executive verdict

HealthIQ is **weakly utilising Pass 3 research assets** for the product surfaces that users see — specifically the Wave 1 Health Systems Cards. The rich structured content authored in Pass 3 (ranked hypotheses, contradiction markers, `relationship_kind`, `missing_data.policy`, `physiological_claim`, confirmatory tests) was authored correctly in the `investigation_spec` format but the pipeline from there to the Health Systems Card UI omits almost all of it.

The situation by layer:

| Layer | Status | Summary |
|---|---|---|
| Pass 3 JSON files | Complete | 117 specs across 5 batch files, 47 unique primary markers, full schema v3.0.0 compliance |
| Pass 3 → pkg signal_library | **Partial** | Activation logic, override rules, and flat `explanation` block carried; hypotheses, contradiction_markers, relationship_kind, confirmatory tests, evidence_strength per hypothesis — **not carried** |
| pkg signal_library → runtime evaluator | **Partial** | `SignalEvaluator` uses activation and override_rules only; `explanation` block is loaded into `SignalResult` but not consumed downstream by Health Systems Cards |
| Root-cause hypothesis layer | **Separate pipeline, good coverage** | 40 hand-authored `*_hypotheses_v1.yaml` files under `knowledge_bus/root_cause/hypotheses/` serve the `root_cause_compiler_v1.py`; these are independent from Pass 3 and have no automated bridge back to it |
| Health Systems Cards (Wave 1) | **Weak** | Subsystem evidence is a hard-coded marker inclusion/missing list (`wave1_subsystem_evidence.py`). `evidence_role` is always `null`. No per-marker roles, rationale, or hypothesis content shown. |

---

## 2. Pass 3 asset inventory

### 2.1 Files and scale

Five batch files in `knowledge_bus/research/investigation_specs/multi_llm_research/`:

| File | Markers covered (sample) |
|---|---|
| `Batch_3_Pass_3.json` | fsh, globulin, hba1c_pct, hematocrit, iron |
| `Batch_4_Pass_3.json` | albumin, creatinine, crp, ferritin, hdl, ldl, triglycerides, tsh, vitamin_b12 |
| `Batch_5_Pass_3.json` | active_b12, alp, alt, apoa1, apob, apob_apoa1_ratio, basophils, bilirubin, calcium, chloride, cortisol, folate, ggt, hba1c, hgb, homocysteine, lym |
| `Batch_6_Pass_3.json` | chloride, corrected_calcium, lymphocytes, magnesium, mcv, neutrophils, non_hdl, plt, tyg_index, urate, urea, wbc |
| `Batch_7_Pass_3.json` | neutrophils, lym, plt, wbc (additional hypothesis frames) |

Total: **117 investigation specs** covering **47 unique primary biomarkers**. All carry `investigation_spec_contract_version: 3.0.0`.

### 2.2 Structured field catalogue (all 117 specs unless noted)

| Field group | Sub-fields | Notes |
|---|---|---|
| `primary_marker` | `biomarker_id`, `rationale`, `signal_system` | Per-spec primary marker with interpretive rationale |
| `trigger_direction` | high / low / bidirectional / context_dependent | Governs which bound activates |
| `activation` + `states` | `activation_logic`, `activation_config`, `baseline_state`, `escalation_state` | Lab-range activation config |
| `supporting_markers[]` | `biomarker_id`, `expected_direction`, **`role`**, **`relationship_kind`**, **`availability`**, **`rationale`** | Rich per-marker semantics: role ∈ {corroborator, mechanism_marker, contextual_marker, severity_marker, differential_marker, exclusion_marker}; relationship_kind ∈ {mechanism, corroboration, severity, differential, exclusion} |
| `hypotheses[]` | `hypothesis_id`, `rank`, **`physiological_claim`**, `evidence_strength`, `caveats[]`, **`missing_data.policy`**, `supporting_marker_refs[]`, **`contradiction_markers[]`** | Multi-hypothesis ranked differential reasoning |
| `hypothesis_ranking` | `ordered_hypothesis_ids[]` | Deterministic hypothesis priority order |
| `confirmatory_tests[]` | `test_id`, `rationale` | What to test next with clinical reasoning |
| `override_rules[]` | `rule_id`, `resulting_state`, `description`, `conditions[]`, `source_refs[]` | Escalation rules with lab-range boundary semantics |
| `evidence` | `evidence_strength`, `sources[]`, `physiological_claim`, `threshold_notes` | Aggregate evidence with citations |
| `narrative` | `mechanism`, `biological_pathway`, `interpretation`, `implications`, `supporting_marker_roles` | Five structured prose fields; the product-visible interpretation layer |

Fields present in Pass 3 but **not defined in the pkg signal_library schema**: `hypotheses`, `hypothesis_ranking`, `contradiction_markers`, `missing_data.policy`, `relationship_kind`, `availability`, per-marker `rationale` in supporting_markers, `evidence.sources`, `confirmatory_tests` with source_refs.

---

## 3. Package propagation audit

### 3.1 What happens during ingestion

The KB-S24 ingestion sprint translated Pass 3 investigation specs into `pkg_s24_*` packages. The translation carried:

- `activation_logic` and `activation_config` → signal_library `activation_logic` and `activation_config`
- `override_rules` → signal_library `override_rules`
- `supporting_markers[].biomarker_id` → signal_library `supporting_metrics` (flat list, no role/relationship)
- `narrative.*` → signal_library `explanation.*` (five narrative prose fields mapped)
- `evidence.sources` + `physiological_claim` → `research_brief.yaml` (partial)

The translation **did not carry**:

- `supporting_markers[].role`
- `supporting_markers[].relationship_kind`
- `supporting_markers[].availability`
- `supporting_markers[].rationale`
- `hypotheses[]` (none of the hypothesis objects)
- `hypothesis_ranking`
- `contradiction_markers[]`
- `missing_data.policy` per hypothesis
- `evidence_strength` per hypothesis
- `caveats[]` per hypothesis
- `confirmatory_tests[]` with rationale
- `evidence.sources` citations in the signal_library itself

### 3.2 Field-level propagation table

| Pass 3 field | In pkg signal_library? | Where? | Preservation | Notes |
|---|---|---|---|---|
| `primary_marker.biomarker_id` | Yes | `primary_metric` | Full | Direct mapping |
| `primary_marker.rationale` | No | — | Lost | Not mapped to any pkg field |
| `primary_marker.signal_system` | Yes | `system` | Full | |
| `supporting_markers[].biomarker_id` | Yes | `supporting_metrics[]` | Full (id only) | Flat list, role stripped |
| `supporting_markers[].role` | No | — | Lost | Not in signal_library schema |
| `supporting_markers[].relationship_kind` | No | — | Lost | Not in signal_library schema |
| `supporting_markers[].availability` | No | — | Lost | Not in signal_library schema |
| `supporting_markers[].rationale` | No | — | Lost | Not in signal_library schema |
| `hypotheses[]` | No | — | Lost | Not carried to any pkg file |
| `hypothesis_ranking` | No | — | Lost | |
| `contradiction_markers[]` | No | — | Lost | |
| `missing_data.policy` | No | — | Lost | |
| `caveats[]` | No | — | Lost | |
| `evidence_strength` (per hypothesis) | No | — | Lost | |
| `confirmatory_tests[]` | No | — | Lost | Separate system in `knowledge_bus/root_cause/hypotheses/` covers some |
| `override_rules[]` | Yes | `override_rules[]` | Full | Best-preserved Pass 3 component |
| `activation.*` | Yes | `activation_logic`, `activation_config` | Full | |
| `evidence.sources` | Partial | `research_brief.yaml sources[]` | Partial (fewer sources) | Abbreviated in research_brief |
| `evidence.physiological_claim` | Partial | `research_brief.yaml physiological_claim` | Partial | Shortened version |
| `narrative.mechanism` | Yes | `explanation.mechanism` | Full prose | Mapped from Pass 3 narrative |
| `narrative.biological_pathway` | Yes | `explanation.biological_pathway` | Full prose | |
| `narrative.interpretation` | Yes | `explanation.interpretation` | Full prose | |
| `narrative.implications` | Yes | `explanation.implications` | Full prose | |
| `narrative.supporting_marker_roles` | Yes | `explanation.supporting_marker_roles` | Partial | Condensed flat string, not structured per-marker |

**Summary:** Of the 14 distinct Pass 3 field groups, 5 are fully preserved, 2 are partially preserved, and 7 are completely lost in the pkg translation.

### 3.3 The root-cause hypothesis layer — separate and independent

HealthIQ has a parallel hypothesis system at `knowledge_bus/root_cause/hypotheses/` (40 YAML files). This serves `root_cause_compiler_v1.py` via `root_cause_registry_v1.py`. These files use a different schema (`schema_version: v1` with `hypothesis_id`, `title`, `summary_template`, `evidence_for_rules`, `evidence_against_rules`, `missing_data_markers`, `confirmatory_tests`). They are **not derived from Pass 3** — they were hand-authored in a separate sprint (KB-S33 and extensions). The root_cause layer covers 40 signals including `hba1c_high`, `homocysteine_high`, `ggt_high`, `alt_context`, `triglycerides_high`, `ldl_cholesterol_high`, `tsh_high/low`, `ferritin_high/low`, etc. This system is active and feeds the report compiler. However it does not surface in the Health Systems Cards.

---

## 4. Runtime utilisation audit

### 4.1 What the Signal Evaluator actually reads

`backend/core/analytics/signal_evaluator.py` reads from pkg signal_library files via `SignalRegistry`. The evaluator uses:

- `activation_logic` (lab_range_exceeded vs deterministic_threshold)
- `activation_config.enable_upper_bound`, `upper_bound_state`, `enable_lower_bound`, `lower_bound_state`
- `thresholds[]` (value, operator, severity)
- `override_rules[]` (conditions with `comparator_type: lab_range_boundary` or numeric)
- `output.supporting_markers` (for confidence scoring only, via `signal_confidence_builder.py`)

The evaluator does **not** read: `explanation.*`, `supporting_metrics[].role`, `supporting_metrics[].relationship_kind`, `supporting_metrics[].rationale`, anything from `hypotheses` blocks (which don't exist in pkg files).

### 4.2 What the subsystem evidence layer reads

`backend/core/analytics/wave1_subsystem_evidence.py` uses a **hard-coded** Python dict (`WAVE1_DOMAIN_SUBSYSTEM_DEFS`) for all subsystem definitions. The only data it reads at runtime is whether a canonical marker ID appears in the biomarker panel. It does **not** read any pkg file, any Pass 3 file, or any knowledge_bus asset at all.

The `SubsystemEvidenceV1` model (`backend/core/models/results.py`, line 176) has an `evidence_role` field that is always `None` (set to `null` at line 168 in `wave1_subsystem_evidence.py`). This field is the correct hook for Pass 3 `relationship_kind` data but is never populated.

### 4.3 What the Health Systems Cards show

`frontend/app/components/results/Wave1DomainCards.tsx` renders:
- Domain score, band label, confidence tier
- `headline_sentence`, `contributor_sentence`, `confidence_sentence`, `consequence_sentence`, `next_step_sentence`
- Evidence completeness numerator/denominator
- Subsystem section (marker inclusion/missing lists via `Wave1SubsystemEvidenceSection.tsx`)

What it does **not** show and has no backend field for:
- Per-marker roles or relationship kinds
- Hypothesis frames or physiological claims
- Contradiction markers (e.g., "if prolactin is high, the FSH interpretation changes")
- Missing data policy guidance
- Confirmatory test suggestions at domain card level
- Evidence strength grading per finding
- Biological pathway text

### 4.4 Runtime utilisation table

| Pass 3 field / concept | Runtime-used? | File | Used for | Gap |
|---|---|---|---|---|
| Activation logic + config | Yes | `signal_evaluator.py` | Signal firing | Fully used |
| Override rules | Yes | `signal_evaluator.py` | State escalation | Fully used |
| `narrative.mechanism` | Partial | `signal_evaluator.py` loads into `SignalResult.explanation`; `report_compiler_v1.py` may use | Not on Health Systems Cards | Present in pkg but not surface-routed to domain cards |
| `narrative.biological_pathway` | Partial | Same as mechanism | Same gap | |
| `narrative.interpretation` | Partial | Same as mechanism | Same gap | |
| `narrative.implications` | Partial | Same as mechanism | Same gap | |
| `narrative.supporting_marker_roles` | No | Not consumed by any runtime analytics path | Nothing | Complete gap |
| Hypothesis ranked frames | No | Not in pkg files; root_cause layer is independent | Root-cause report only (not domain cards) | Major gap |
| `relationship_kind` | No | Never loaded or used | Nothing | Complete gap |
| Per-marker `rationale` | No | Never loaded or used | Nothing | Complete gap |
| `contradiction_markers` | No | Not in pkg files; not in runtime | Nothing | Complete gap |
| `missing_data.policy` | No | Not in pkg files; not in runtime | Nothing | Complete gap |
| `confirmatory_tests` (Pass 3) | No | Separate `confirmatory_tests_v1.yaml` registry for root-cause only | Root-cause only | Complete gap on domain cards |
| `evidence_strength` (Pass 3) | No | Not loaded by evaluator or domain assembler | Nothing | Complete gap |
| `SubsystemEvidenceV1.evidence_role` | No — always null | `wave1_subsystem_evidence.py` line 168 | Placeholder only | Ready hook, never filled |
| Supporting marker availability | No | Not in pkg; not read anywhere | Nothing | |

---

## 5. Health Systems Card opportunity analysis

### 5.1 What the current cards show

Each Wave 1 domain card shows: a coarse domain score, a band label, a confidence tier, one headline sentence, one contributor sentence, one consequence sentence, one next step sentence, and a collapsed subsystem section listing which markers were included/missing. The subsystem section is a marker presence list — it has no interpretation of what role each marker plays.

### 5.2 What Pass 3 adds that the cards could use

**Marker roles and relationship semantics.** Pass 3 classifies every supporting marker as `corroborator`, `mechanism_marker`, `differential_marker`, `severity_marker`, or `exclusion_marker`, and assigns a `relationship_kind` (mechanism, corroboration, severity, differential, exclusion). For example:

- CRP in the homocysteine spec: `role: mechanism_marker`, `relationship_kind: mechanism` — "Raised CRP supports inflammatory endothelial damage context when homocysteine is elevated."
- Triglycerides in the HbA1c spec: `role: mechanism_marker`, `relationship_kind: mechanism` — "Hypertriglyceridemia can support an insulin-resistant metabolic context."

The subsystem evidence section currently shows "Triglycerides — Included" with no further context. Pass 3 would support showing "Triglycerides — Metabolic context marker" or similar.

**Ranked hypothesis frames with physiological claims.** The HbA1c spec has two ranked hypotheses: (1) chronic hyperglycemia (evidence_strength: consensus), (2) iron deficiency red-cell bias (evidence_strength: moderate). The current HbA1c consequence sentence mentions the glycaemic exposure story but not the red-cell bias caveat, which is clinically important for users with concurrent low ferritin. Pass 3 provides the exact content for this.

**Contradiction markers.** For CRP (vascular context), Pass 3 specifies: if albumin is low, escalate (the negative acute-phase pattern). The current domain cards have no mechanism to surface contradiction-driven interpretation changes.

**Missing data policy.** Every Pass 3 hypothesis has a `missing_data.policy` — e.g., for high HbA1c: "Use glucose correlation and repeat testing where results and phenotype do not align." This is directly relevant to the domain card confidence section, which currently offers only a generic confidence tier label.

**Confirmatory tests.** Pass 3 specifies clinically grounded next tests for every signal (e.g., "repeat HbA1c with fasting glucose" for the chronic hyperglycemia frame). The current `next_step_sentence` is pulled from `insight_results` or a generic fallback. Pass 3 would ground this in the specific interpretation context.

### 5.3 Specific marker-by-marker relevance for Wave 1

**CRP (Cardiovascular / Vascular strain context subsystem)**
Pass 3 spec `inv_crp_high_residual_cardiometabolic_inflammatory_risk` (Batch_4) frames CRP as a vascular risk marker with specific relationships: LDL as `corroborator` (relationship_kind: corroboration), glucose as `mechanism_marker` (IR-driven inflammation), statin therapy marker as `differential_marker`. The current card shows CRP in the "Vascular strain context" subsystem with no role context. The residual vascular risk framing (distinguishing active inflammation from chronic low-grade residual risk) is entirely absent.

**Homocysteine (Cardiovascular / Homocysteine pathway subsystem)**
Pass 3 spec `inv_homocysteine_high_b_vitamin_related_methylation_impairment` classifies B12 as `mechanism_marker` (relationship_kind: mechanism) and folate as `corroborator`. The contradiction marker: high creatinine (renal clearance pathway, weakens B-vitamin cause). The current card shows "Homocysteine pathway" with homocysteine as the only included marker, no cause framing.

**Triglycerides (Blood Sugar / Insulin and metabolic context subsystem)**
Pass 3 spec `inv_triglycerides_high_insulin_resistant_hypertriglyceridemia` frames TG as primarily an IR-driven signal with insulin as `mechanism_marker` and HDL as `corroborator`. The contradiction: high LDL without IR markers weakens pure metabolic framing. The blood sugar card currently shows triglycerides as a plain included marker with no metabolic mechanism copy.

**Liver markers (ALT, AST, GGT, ALP, albumin, bilirubin)**
Pass 3 has 9 specs for liver markers (alt_hepatocellular, alt_metabolic_steatotic, alt_muscle_source, alp_cholestatic, alp_bone, ggt_hepatobiliary, ggt_alcohol/enzyme, bilirubin_gilbert, bilirubin_hemolytic, bilirubin_hepatobiliary). These provide differential frames that are clinically important — muscle-source ALT (differential_marker: CK, creatinine) vs hepatocellular ALT, for example. The current liver domain card has a single ALT-anchored consequence sentence with no differential framing.

**HbA1c / glucose**
As described above, the iron-deficiency HbA1c bias frame (Batch_3 spec `inv_hba1c_pct_high_red_cell_turnover_bias_or_iron_deficiency`) is completely absent from the blood sugar card even when ferritin is also low in the panel. This is a specific, documentable gap.

---

## 6. Examples of underused research richness

| Missed asset | Concrete example | Current UI weakness | Potential product value |
|---|---|---|---|
| HbA1c + iron deficiency bias frame | Pass 3 `inv_hba1c_pct_high_red_cell_turnover_bias_or_iron_deficiency`: low ferritin as mechanism_marker for HbA1c overestimation | Blood sugar card shows elevated HbA1c as chronic hyperglycemia framing; ferritin low on same panel produces no modifying signal | Users with iron deficiency may be over-alarmed. Showing "HbA1c may be elevated partly due to iron status — consider glucose alongside" is clinically defensible and differentiating |
| CRP residual vascular risk vs active inflammation | Pass 3 `inv_crp_high_residual_cardiometabolic_inflammatory_risk`: frames hs-CRP <10 as chronic residual risk vs active infection differential | Cardiovascular card shows CRP as a vascular strain context marker — no distinction between acute and chronic elevations | Distinguishing "chronic low-grade inflammation" from "possible active infection" is a primary consumer concern and currently collapsed |
| ALT muscle-source differential | Pass 3 `inv_alt_high_muscle_source_or_exertional_pattern`: CK as differential_marker; high ALT with low CK = hepatic; high ALT with high CK = muscle source | Liver enzyme pattern subsystem shows ALT included; no cause framing | Users who exercise heavily have elevated ALT regularly. Showing the muscle-source differential reduces unnecessary alarm and increases trust |
| GGT + ALP cholestatic pattern vs GGT alcohol/enzyme induction | Pass 3 has two distinct GGT hypothesis frames | GGT is shown as a plain included marker in the liver enzyme pattern subsystem | Two very different clinical stories (biliary vs alcohol/medication) use different supporting markers (ALP for cholestatic vs MCV for alcohol) |
| Homocysteine B12 vs renal clearance differential | Pass 3 `inv_homocysteine_high_renal_clearance_reduction`: creatinine as mechanism_marker — renal impairment increases HCY independently of B-vitamin status | Homocysteine pathway subsystem shows homocysteine with no cause framing | Users with elevated creatinine and elevated homocysteine receive no signal that these are mechanistically linked; B-vitamin supplementation framing is the wrong next step in this case |
| Triglycerides + IR vs severe pancreatitis risk | Pass 3 `inv_triglycerides_high_severe_hypertriglyceridemia_context` (evidence_strength: consensus) is distinct from `inv_triglycerides_high_insulin_resistant_hypertriglyceridemia` | Blood sugar card shows triglycerides as a metabolic context marker regardless of severity | At TG >5.6 mmol/L the clinical concern shifts to pancreatitis — this is handled by an override_rule in pkg_s24 but not exposed in domain card copy |
| Hypothesis ranking for differential | All 117 Pass 3 specs have ranked hypotheses. Rank 1 vs rank 2 hypotheses differ by evidence_strength (consensus vs moderate vs exploratory) | Health Systems Cards have no hypothesis framing at all | A rank-1 consensus-strength hypothesis (e.g., high HbA1c = chronic hyperglycemia) is presented with the same weight as an exploratory rank-2 frame (red-cell bias). No weighting is surfaced |
| Missing data policy | Every hypothesis has `missing_data.policy`. For crp_high: "Review clinical context before attributing to a specific cause without additional markers" | Confidence tier on cards is coarse (high/medium/low); missing data policy is never shown | The specific "what would help interpret this further" copy already exists in Pass 3 and is not reaching users |

---

## 7. Architecture options

| Option | Description | Pros | Cons | Risk | Recommendation |
|---|---|---|---|---|---|
| **A. Continue using only *pkg files** | No change. Pass 3 fields that weren't ingested remain offline | Zero implementation risk. No governance overhead | Permanently loses hypotheses, relationship_kind, contradiction logic. Wave 1 cards remain explanation-poor | Low (no change) | Reject. Creates product debt. |
| **B. Extend *pkg files to preserve more Pass 3 content** | Add `hypotheses[]`, `relationship_kind`, `contradiction_markers` to the signal_library schema and re-run KB-S24 ingestion for affected packages | Uses existing pkg pipeline. No new runtime layer needed. Schema extension is governed | Signal_library schema becomes very large. Hypothesis format in pkg is different from root_cause/hypotheses format — two competing formats. Schema migration touches 186 existing pkg files | STANDARD-HIGH. Schema change affects every signal_library consumer | Partially viable. Suitable for `relationship_kind` and `availability` on supporting_markers only. Not suitable for full hypothesis graphs. |
| **C. Compile selected Pass 3 fields into a new governed runtime evidence layer** | A new `pass3_evidence_layer.yaml` or per-signal JSON file carrying `relationship_kind`, `ranked_hypotheses`, `contradiction_markers` for Wave 1 signals specifically. Runtime loaded by a new assembler alongside the pkg evaluator | Clean separation. Pass 3 content is not forced into signal_library schema. Can be introduced incrementally | New layer = new schema, new loader, new validation, new governance sprint | HIGH if it touches Intelligence Core output. STANDARD if offline reference only for narrative generation | Best long-term architecture for full Pass 3 utilisation. Requires governed sprint with clear schema contract. |
| **D. Use Pass 3 only for offline research/reference** | Explicitly declare Pass 3 as research-only, not runtime-bound | No change needed. Simplest | Wastes the best-sourced clinical content in the repo. Contradicts HealthIQ's intelligence differentiation claim | None | Reject. Pass 3 contains directly product-relevant content. |
| **E. Extend subsystem evidence with Pass 3 marker roles only (minimal viable improvement)** | Populate `SubsystemEvidenceV1.evidence_role` from pkg `explanation.supporting_marker_roles` and signal_library `supporting_metrics`. Add `relationship_kind` field to the per-marker display contract | Targeted. Uses existing `evidence_role` hook in `SubsystemEvidenceV1`. Low schema impact | Only addresses marker role display; does not surface hypotheses, contradictions, or missing data policy | LOW-STANDARD | Best immediate next step. Uses an already-designed null field. |

---

## 8. Recommended next work package

**Proposed work_id:** `PASS3-E1` (or slot into Wave 1 domain card work stream)

**Title:** Extend Wave 1 subsystem evidence with governed marker roles from Pass 3

**Rationale:** The `SubsystemEvidenceV1.evidence_role` field (defined in `backend/core/models/results.py` line 206) is currently always `null` and was explicitly designed as the hook for future role information. Pass 3 provides `relationship_kind` and per-marker `rationale` for every supporting marker. The pkg `explanation.supporting_marker_roles` field is a condensed prose version. Populating `evidence_role` with the `relationship_kind` class for each included marker requires:

1. Extending pkg signal_library schema to add `relationship_kind` and `availability` to the `supporting_metrics` entries (these are two fields, not a full hypothesis graph)
2. Re-ingesting affected pkg_s24_* packages (or patching in-place under governance)
3. Modifying `wave1_subsystem_evidence.py` to read `relationship_kind` from the loaded signal registry when constructing `SubsystemEvidenceV1`
4. Frontend renders the `evidence_role` field (already present on `SubsystemEvidenceV1` type)

**Risk level:** STANDARD (touches signal_library schema and wave1_subsystem_evidence.py — the latter is governed but not Intelligence Core evaluation logic)

**Files likely touched:**
- `knowledge_bus/packages/pkg_s24_*/signal_library.yaml` (add `relationship_kind` per supporting_metric)
- `knowledge_bus/investigation_spec_schema_v3.0.0.yaml` — no change needed (schema already has relationship_kind)
- `backend/core/analytics/wave1_subsystem_evidence.py` — read relationship_kind from registry
- `backend/core/models/results.py` — `evidence_role` field already exists, no change needed
- `frontend/app/components/results/Wave1SubsystemEvidenceSection.tsx` — render evidence_role
- `frontend/types/analysis.ts` — `SubsystemEvidenceV1.evidence_role` type already exists

**Implementation principle:**
- `evidence_role` must be populated from governed pkg data, not inferred from heuristics
- The five relationship_kind values (mechanism, corroboration, severity, differential, exclusion) must be used as-is from Pass 3 — do not introduce new role vocabulary
- `wave1_subsystem_evidence.py` must not embed clinical knowledge — all role data comes from pkg files via SignalRegistry
- Only Wave 1 domain markers are in scope (cardiovascular, blood_sugar, liver subsystem definitions)

**What must not change:**
- Signal activation logic in `SignalEvaluator`
- Override rule evaluation
- Domain score or confidence tier calculation
- `SubsystemEvidenceV1.included_marker_ids` / `missing_marker_ids` partition logic
- Root-cause hypothesis layer (`root_cause_compiler_v1.py`)

---

## 9. STOP conditions

The following implementation shortcuts would be unsafe and must be rejected:

1. **Hard-coding role labels in `wave1_subsystem_evidence.py`** — roles must come from governed pkg data, not Python constants. Hard-coded roles are ungoverned and break the Pass 3 lineage traceability.

2. **Inferring relationship_kind from marker name patterns** — e.g., inferring "triglycerides = mechanism_marker for metabolic context" from string matching. Pass 3 assigned roles from research review. Inference would introduce unreviewed clinical claims into the analytical surface.

3. **Treating Pass 3 hypotheses as equivalent to root_cause/hypotheses v1 files** — the two schemas are different. Pass 3 `physiological_claim` is not a drop-in replacement for `summary_template`. A governed translation sprint is required before any Pass 3 hypothesis frames reach `root_cause_compiler_v1.py`.

4. **Adding Pass 3 narrative fields to `ConsumerDomainScoreV1` headline/consequence sentences without IDL governance** — the IDL layer governs what appears in domain card prose. Adding `narrative.implications` text from Pass 3 directly to `consequence_sentence` bypasses IDL governance and risks directive clinical language reaching retail users.

5. **Schema-extending signal_library.yaml with the full hypothesis graph** — the hypothesis graph (ranked frames, contradiction_markers, missing_data.policy) is too large and structurally complex for the signal_library schema without a dedicated schema version and validation sprint. Stuffing it in as YAML nested objects without a schema contract will create unmaintainable assets.

6. **Skipping kernel and gate for any file changes** — even the minimal `evidence_role` change requires a work package with `start`, implementation, `finish`, and gate passing.

---

## Appendix A — Pass 3 coverage vs root_cause registry coverage

| Signal | Pass 3 spec exists? | Root-cause hypothesis yaml exists? | Both? |
|---|---|---|---|
| alt_high | Yes (3 specs) | Yes (`alt_hypotheses_v1.yaml`) | Yes |
| crp_high | Yes (2 specs) | Yes (via `systemic_inflammation_hypotheses_v1.yaml`) | Partial |
| hba1c_high | Yes (3 specs) | Yes (`hba1c_hypotheses_v1.yaml`) | Yes |
| homocysteine_high | Yes (2 specs) | Yes (`hcy_hypotheses_v1.yaml`) | Yes |
| triglycerides_high | Yes (2 specs) | Yes (`triglycerides_high_hypotheses_v1.yaml`) | Yes |
| ggt_high | Yes (2 specs) | Yes (`ggt_high_hypotheses_v1.yaml`) | Yes |
| ldl_high | Yes (2 specs) | Yes (`ldl_cholesterol_high_hypotheses_v1.yaml`) | Yes |
| hdl_low | Yes (1 spec) | Yes (`hdl_cholesterol_low_hypotheses_v1.yaml`) | Yes |
| ferritin_high | Yes (2 specs) | Yes (`ferritin_high_hypotheses_v1.yaml`) | Yes |
| ferritin_low | Yes (1 spec) | Yes (`ferritin_low_hypotheses_v1.yaml`) | Yes |
| bilirubin_high | Yes (3 specs) | Yes (`bilirubin_high_hypotheses_v1.yaml`, `hyperbilirubinemia_hypotheses_v1.yaml`) | Yes |
| alp_high | Yes (2 specs) | Yes (`alp_high_hypotheses_v1.yaml`) | Yes |
| vitamin_b12_low | Yes (2 specs) | Yes (`vitamin_d_low_hypotheses_v1.yaml` for vitamin_d; no b12-specific file) | Partial |
| fsh_high/low | Yes | No | Pass 3 only |
| globulin_high/low | Yes | No | Pass 3 only |
| calcium_high/low | Yes | No | Pass 3 only |
| cortisol_high | Yes | Yes (`hypercortisolism_hypotheses_v1.yaml`) | Yes |
| lym_high/low | Yes | No | Pass 3 only |
| neutrophils_high/low | Yes | No | Pass 3 only |
| plt_high/low | Yes | No | Pass 3 only |

**Observation:** Where both Pass 3 and root_cause hypotheses exist, they were authored independently with different schemas and different hypothesis frames. There is no validated cross-check between them. The Pass 3 physiological claims and the root_cause summary_templates cover the same clinical territory but are not guaranteed to be consistent. A future pass should align these.

---

_End of investigation. No files were modified._
