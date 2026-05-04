# Domain Narrative Contract — Wave 1 (Cardiovascular, Blood Sugar, Liver)

**Document type:** Repo-grounded domain narrative contract spec
**Date:** 2026-04-26
**Author:** Claude Code (research only — no implementation authority)
**Depends on:** `docs/STRATEGY_A_IMPLEMENTATION_BLUEPRINT.md`
**Status:** Draft for GPT architectural review and sprint planning

---

## Purpose

This document defines the domain narrative contract for the three Wave 1 Strategy A customer-facing health score domains:

1. Cardiovascular health
2. Blood sugar control
3. Liver health

It specifies exactly how the narrative components for each domain's consumer-facing card should be assembled from existing codebase truth — which fields supply each line, what can be sourced directly, what requires light assembly, and where gaps remain.

This is a contract spec, not a sprint prompt. It is not implementation authority. Its purpose is to give GPT the evidence base to author work packages.

---

## Pre-spec context: what the engine currently exposes

Before domain-level analysis, the following output structures are relevant.

### AnalysisDTO narrative fields (available today)

| Field | Path | What it contains |
|---|---|---|
| NarrativeReportV1 | `AnalysisDTO.narrative_report_v1` | lead_narrative, longitudinal_narrative, next_steps_narrative, body_overview, retail_summary (all compiled deterministically, N-8) |
| InterpretationDisplayLayerBundleV1 | `AnalysisDTO.interpretation_display_layer_v1` | IDL records with clinical_display_label, retail_display_label, subtitle, why_it_matters, severity_state, supporting_biomarkers_summary, user_safe_description |
| system_capacity_scores | `AnalysisDTO.system_capacity_scores` | Burden-derived 0-100 integer per system (cardiovascular, metabolic, hepatic, thyroid, renal, hematological, immune, etc.) |
| Layer3InsightsV1 | Via `AnalysisDTO.insights` assembly | InsightCard per system: title, severity (action/watch/info), confidence (high/medium/low), interpretation (deterministic text), next_steps (list) |
| RootCauseV1 | Via ClinicianReportV1 and root cause compiler | Per-signal findings with hypotheses, evidence_for, missing_data ({marker_id, reason}), confirmatory_tests ({display_name, rationale}), safety_class |
| ConfidenceModelV1 | Internal analytics output | cluster_confidence, biomarker_confidence, missing_required_biomarkers, system_confidence |
| ClinicianReportV1 | Via AnalysisDTO | data_quality.confidence_caveat, data_quality.missing_data items, Page1.top_hypothesis_line, Page1.confidence_and_missing_data |
| BiomarkerScore.status | `AnalysisDTO.biomarkers[]` | Per-biomarker: score, status, lab_band_label, reference_range, biomarker_educational_explainer |

### IDL records relevant to Wave 1 domains

| IDL internal_id | Domain | Clinical label | Retail label | why_it_matters (governed) |
|---|---|---|---|---|
| ph_metabolic_early_ir_v1 | Blood sugar | Early insulin-resistance phenotype | Insulin Resistance Phenotype | "Left unaddressed, early insulin resistance progresses toward prediabetes and cardiometabolic risk." |
| ph_hba1c_metabolic_stress_v1 | Blood sugar | Dysglycaemic metabolic stress | Blood Sugar Stress State | "Sustained glycaemic strain raises long-term metabolic and vascular risk." |
| ph_vascular_hcy_inflammation_v1 | Cardiovascular | Vascular inflammation risk (homocysteine-linked) | Vascular Inflammation Risk | "Accumulating vascular-risk signals warrant cardiometabolic review and lifestyle action." |
| ph_lipid_residual_ldl_favourable_transport_v1 | Cardiovascular | Residual LDL signal within a more favourable lipid transport picture | LDL in context (protective transport features) | — (no why_it_matters field in this record) |
| ph_hepatic_alt_inflammatory_v1 | Liver | Hepatic inflammatory pattern | Liver Stress Pattern | "Early liver-strain patterns are a key lane toward MASLD/fibrosis risk if ignored." |

### Layer3 system_pressure card IDs (from `layer3_insights_v1.py`)

These `InsightCard` objects already carry: `title`, `severity`, `confidence`, `interpretation`, `next_steps[]`, `evidence`.

- `cardiovascular__system_pressure`
- `metabolic__system_pressure`
- `hepatic__system_pressure`

### Functional interpretation KB assets (N-6, in `knowledge_bus/functional_interpretation_v1/`)

Two domains currently have governed functional interpretation assets:

- `lipid_transport_functional_v1` — covers: functional_reading, why_beyond_itself, confidence_supports_reading, confidence_limits, clarification_paths, monitoring_improvement_signals, monitoring_persistence_signals
- `one_carbon_methylation_functional_v1` — same structure, for homocysteine/methylation pathway

**These assets exist in the KB but are not currently exposed in any DTO field accessible to a consumer domain card.** They feed the `NarrativeReportV1` compiler only when the benchmark interpretation entities bind them. For Wave 1 domain cards, a routing step would be needed to surface them directly.

---

## Domain 1: Cardiovascular Health

**Consumer label:** Cardiovascular health
**Clinical label:** Cardiometabolic / Vascular Risk Status

---

### Narrative components

#### 1.1 Headline sentence

**Template (score-band driven):**

| Score band | Headline sentence |
|---|---|
| 80–100 | "Your cardiovascular health looks strong based on your current blood results." |
| 65–79 | "Your cardiovascular health looks broadly stable based on your current results." |
| 45–64 | "Your cardiovascular health shows some signals worth watching in your current results." |
| 0–44 | "Your cardiovascular health shows patterns that deserve closer review." |

**Source of truth:** `HealthSystemScore.overall_score` for the `cardiovascular` scoring system (scoring_policy.yaml). Score → band → sentence via deterministic lookup table in `domain_score_assembler.py`.

**Status: directly assemblable — no new contract work needed.**

---

#### 1.2 Why this score

**Logic:** The most clinically weighted active signal drives the contributor sentence. Priority order (from `root_cause_compiler_v1.py` signal ordering and burden weights):

1. `signal_lipid_transport_dysfunction` at_risk → "Your lipid transport pattern shows elevated atherogenic particle burden across multiple markers."
2. `signal_ldl_cholesterol_high` at_risk → "Your LDL cholesterol is above the optimal range, adding to longer-term cardiovascular exposure."
3. `signal_hdl_cholesterol_low` at_risk → "Your HDL is below the optimal range, reducing the protective component of your lipid picture."
4. `signal_triglycerides_high` at_risk → "Your triglycerides are elevated, which relates to remnant particle exposure and metabolic lipid handling."
5. `signal_homocysteine_elevation_context` at_risk → "Homocysteine is elevated, adding an endothelial strain signal alongside the lipid picture."
6. `signal_total_cholesterol_high` suboptimal only → "Total cholesterol is above the optimal range, though the full transport picture adds context."
7. No signals active → "Your key cardiovascular markers are within their reference ranges."

**Primary sources:**
- Signal states from `RootCauseFindingV1.signal_state` per signal (already in root cause output)
- IDL records: when `ph_vascular_hcy_inflammation_v1` or `ph_lipid_residual_ldl_favourable_transport_v1` are active in IDL bundle → use `InterpretationDisplayRecordV1.subtitle` as the contributor line
- `Layer3InsightCard.interpretation` for `cardiovascular__system_pressure` as fallback if IDL records are not populated

**Status: assemblable with light selection logic. Signal priority rule needs to be codified in the domain score assembler. IDL subtitle is the preferred source for the contributor line when an IDL record is active.**

---

#### 1.3 Confidence sentence

**Confidence level determination:**

| Condition | Level | Sentence |
|---|---|---|
| total_cholesterol + ldl + hdl + triglycerides all present AND derived ratio(s) computed | High | "Confidence is high — your full lipid panel plus derived ratios give a complete cardiovascular picture." |
| total_cholesterol + ldl + hdl present, triglycerides or ratios partial | Good | "Confidence is good — core lipid markers are present, though some transport markers are missing." |
| total_cholesterol + ldl present, HDL absent | Moderate | "Confidence is moderate — HDL and derived ratios would strengthen the cardiovascular assessment." |
| total_cholesterol only | Limited | "Confidence is limited — a fuller lipid panel including LDL and HDL would improve this picture." |

**What would improve confidence (expandable detail):**

Sourced from `RootCauseHypothesisV1.missing_data` items for active cardiovascular signals. Each missing_data item has `{marker_id, reason}` — this IS the "what would improve confidence" list. For example, for signal_lipid_transport_dysfunction with no ApoB: `{marker_id: "apob", reason: "ApoB would quantify atherogenic particle count directly."}`.

**Sources:**
- `ConfidenceModelV1.cluster_confidence["cardiovascular"]` (proportion of required markers present from clusters.yaml)
- Supplementary: count of cardiovascular burden_registry markers present (apob, apoa1, homocysteine, lipoprotein_a)
- `Layer3InsightCard.confidence` for `cardiovascular__system_pressure`
- `RootCauseHypothesisV1.missing_data[]` across active cardiovascular signals → "what would improve confidence" list
- `ClinicianReportV1.data_quality.confidence_caveat` is the existing governed confidence sentence but is clinician-facing in tone

**Status: confidence level is directly available from existing outputs. The consumer confidence sentence requires a small governed template bank (four sentences, as above). "What would improve confidence" detail is directly available from root cause missing_data.**

---

#### 1.4 What this may mean over time

**Primary source:** `InterpretationDisplayRecordV1.why_it_matters` for the primary active IDL record.

- If `ph_vascular_hcy_inflammation_v1` is active → "Accumulating vascular-risk signals warrant cardiometabolic review and lifestyle action."
- If only lipid transport signals active (no IDL record with a why_it_matters line for the dominant lipid pattern) → **gap: no ready-made consequence sentence in the current IDL for a lipid-dominant cardiovascular pattern without homocysteine.**

**Gap:** `ph_lipid_residual_ldl_favourable_transport_v1` IDL record does not have a `why_it_matters` field (it was not populated in the current idl_records_v1.yaml). The correct consequence text for a pure lipid-transport pattern exists in `functional_interpretation_v1/lipid_transport_functional_v1.monitoring_persistence_signals` but this is NOT currently wired to any DTO field.

**Bridging options:**
- Option A: Add `why_it_matters` field to `ph_lipid_residual_ldl_favourable_transport_v1` IDL record (CONTENT change, governed KB sprint)
- Option B: Route `functional_interpretation_v1.lipid_transport_functional_v1.monitoring_persistence_signals` into the domain score assembler as the consequence source for lipid-dominant patterns (requires new assembly logic)
- Option C: Add a new IDL record `ph_lipid_transport_cardiovascular_v1` with an explicit consequence sentence for lipid-dominant patterns

**Interim fallback (without KB change):** "Persistent lipid transport strain may increase long-term cardiovascular exposure if not addressed." — this is a safe, non-diagnostic sentence that could serve as a governed static fallback.

**Status: partial gap. Governed consequence text exists in KB but is not wired to the consumer domain card path for lipid-dominant cardiovascular patterns. Requires either IDL record update (low-risk CONTENT sprint) or new assembly routing.**

---

#### 1.5 What to do next

**Primary source:** `Layer3InsightCard.next_steps[0]` for `cardiovascular__system_pressure` card.

The Layer3 InsightCard is already compiled deterministically with next-step items. These are role-stratified by `safety_class` in the root cause output (monitoring / clinician_referral / lifestyle).

**Fallback source:** `NarrativeReportV1.next_steps_narrative` (compiled N-8 deterministic text).

**Alternative detail source:** `RootCauseHypothesisV1.confirmatory_tests[0].display_name` + `.rationale` — gives a specific test recommendation (e.g., "ApoB quantification — to confirm atherogenic particle burden when LDL alone is borderline").

**Status: directly available from existing Layer3InsightCard.next_steps. No new contract work needed for this component.**

---

### Source-of-truth mapping — cardiovascular

| Component | Primary source | Assembly needed | Gap |
|---|---|---|---|
| Headline sentence | `HealthSystemScore.overall_score` → band lookup | Deterministic lookup table | None |
| Contributor sentence | `Layer3InsightCard.interpretation` (cardiovascular__system_pressure) or `IDL.subtitle` of active record | Signal priority selection rule | None |
| Confidence sentence | `Layer3InsightCard.confidence` + ConfidenceModelV1.cluster_confidence["cardiovascular"] | Governed template bank (4 sentences) | None |
| What would improve confidence | `RootCauseHypothesisV1.missing_data[]` for active CV signals | Surface in DomainScore contract | None |
| Consequence sentence | `IDL.why_it_matters` of active IDL record (if present) | Select by active IDL record | **Gap: lipid-dominant pattern has no IDL why_it_matters. Needs new IDL content or functional_interpretation routing.** |
| Next-step sentence | `Layer3InsightCard.next_steps[0]` (cardiovascular__system_pressure) | Index selection | None |

---

### Confidence logic inputs — cardiovascular

1. `ConfidenceModelV1.cluster_confidence["cardiovascular"]` — proportion of required cluster markers present (total_cholesterol, ldl_cholesterol required; hdl_cholesterol important)
2. Supplementary coverage count: how many of {hdl_cholesterol, triglycerides, apob, apoa1, homocysteine, lipoprotein_a} are present
3. Signal coherence: multiple cardiovascular signals active and concordant in direction → escalates confidence
4. Derived ratios computed: tc_hdl_ratio, tg_hdl_ratio, ldl_hdl_ratio, non_hdl_cholesterol present → escalates
5. Active IDL record present → indicates pattern is strong enough to warrant named phenotype → confidence not Limited

---

### Safe claims — cardiovascular

The expanded card can truthfully say today:
- Whether LDL, HDL, total cholesterol, triglycerides are within or outside their scoring bands
- The direction and magnitude of each active signal (high/low)
- The atherogenic ratio values when derived (tc_hdl, tg_hdl) and whether they are optimal/borderline/high
- Whether a lipid transport dysfunction pattern is present (multi-marker, not single-marker)
- Whether homocysteine is elevated and what additional context it adds
- Which markers are missing and what they would add to the picture
- A specific test recommendation from confirmatory_tests (e.g., ApoB when not tested)
- The next clinical step framing (monitoring / lifestyle / clinician review) from safety_class

The card must NOT say:
- That the user has a specific cardiovascular condition or disease
- A predicted risk score or lifetime event probability
- That any marker alone is sufficient to diagnose or rule out disease

---

## Domain 2: Blood Sugar Control

**Consumer label:** Blood sugar control
**Clinical label:** Glycaemic Regulation / Insulin Resistance Status

---

### Narrative components

#### 2.1 Headline sentence

**Template (score-band driven):**

| Score band | Headline sentence |
|---|---|
| 80–100 | "Your blood sugar control looks strong based on your current results." |
| 65–79 | "Your blood sugar control looks broadly stable based on your current results." |
| 45–64 | "Your blood sugar control shows some signals worth watching." |
| 0–44 | "Your blood sugar control shows a pattern that deserves closer review." |

**Source of truth:** `HealthSystemScore.overall_score` for the `metabolic` scoring system. Note: do not use the metabolic burden capacity score (it includes electrolytes). Use scoring_policy system score only.

**Status: directly assemblable — no new contract work needed.**

---

#### 2.2 Why this score

**Logic:** Signal state and prediabetes override status drive the sentence.

Priority order:
1. `signal_hba1c_high` at_risk (or prediabetes override triggered) → "Your HbA1c shows sustained above-optimal blood sugar exposure over the past few months."
2. `signal_insulin_resistance` at_risk → "Your triglyceride-glucose pattern suggests early insulin resistance."
3. Both active → "Both your HbA1c and your triglyceride-glucose pattern suggest blood sugar handling is under strain."
4. `signal_hba1c_high` suboptimal only → "Your HbA1c is slightly above the optimal range, which is worth monitoring."
5. `signal_insulin_resistance` suboptimal only → "Your triglyceride-glucose index is in a suboptimal zone that warrants attention."
6. No signals active → "Your key blood sugar markers are within their reference ranges."

**Primary sources:**
- `RootCauseFindingV1.signal_state` for signal_hba1c_high and signal_insulin_resistance
- IDL records: `ph_metabolic_early_ir_v1.subtitle` = "A pattern suggesting early impaired sugar and lipid handling" (when IR signal active)
- IDL records: `ph_hba1c_metabolic_stress_v1.subtitle` = "A pattern suggesting sustained blood-sugar strain on the body" (when HbA1c signal active)
- `Layer3InsightCard.interpretation` for `metabolic__system_pressure` (fallback)

**Note on prediabetes override:** `signal_insulin_resistance` has a governed prediabetes override that fires when HbA1c ≥ 5.7% OR glucose ≥ 5.6 mmol/L (ADA Standards of Care 2026). When this override triggers, the signal_state is forced to at_risk regardless of TyG. The contributor sentence should reflect this: "Your blood sugar levels meet criteria for the prediabetes range."

**Status: assemblable with light selection logic. The override case needs explicit handling in the assembler. IDL subtitles are the preferred source for the contributor line.**

---

#### 2.3 Confidence sentence

**Confidence level determination:**

| Condition | Level | Sentence |
|---|---|---|
| Glucose + HbA1c + insulin + triglycerides all present | High | "Confidence is high — all key blood sugar markers and the triglyceride-glucose index are available." |
| Glucose + HbA1c present, triglycerides also present | Good | "Confidence is good — core glycaemic markers plus the insulin resistance index are present." |
| Glucose + HbA1c present, insulin and triglycerides absent | Moderate | "Confidence is moderate — adding insulin and triglycerides would complete the insulin resistance assessment." |
| Glucose only, HbA1c absent | Limited | "Confidence is limited — HbA1c is needed to assess longer-term glucose control." |

**What would improve confidence:**
- `RootCauseHypothesisV1.missing_data[]` for signal_insulin_resistance will list {marker_id: "insulin", reason: ...} and/or {marker_id: "triglycerides", reason: ...} when absent
- These are already generated by the root cause compiler; they just need to be surfaced in the domain score contract

**Sources:**
- `ConfidenceModelV1.cluster_confidence["metabolic"]` (glucose + hba1c required in clusters.yaml)
- Supplementary: insulin present → TyG index computable → HOMA-IR computable
- Triglycerides present → TyG full computation available
- `Layer3InsightCard.confidence` for `metabolic__system_pressure`
- `RootCauseHypothesisV1.missing_data[]` for active metabolic signals

**Status: directly available from existing outputs. Confidence sentence bank (four sentences above) is simple governed copy.**

---

#### 2.4 What this may mean over time

**Primary source — best of all three Wave 1 domains:**

- `ph_metabolic_early_ir_v1.why_it_matters` → "Left unaddressed, early insulin resistance progresses toward prediabetes and cardiometabolic risk."
- `ph_hba1c_metabolic_stress_v1.why_it_matters` → "Sustained glycaemic strain raises long-term metabolic and vascular risk."

**Selection logic:**
- If `signal_hba1c_high` at_risk → use ph_hba1c_metabolic_stress_v1.why_it_matters
- If `signal_insulin_resistance` at_risk and HbA1c not at_risk → use ph_metabolic_early_ir_v1.why_it_matters
- If both → prefer ph_hba1c_metabolic_stress_v1 (more urgent framing)
- If no signals active → "If blood sugar markers stay well controlled over time, this is a positive foundation."

**Status: consequence sentences are the most ready of all three Wave 1 domains. IDL why_it_matters fields are governed, available today, and appropriately calibrated. No gap.**

---

#### 2.5 What to do next

**Primary source:** `Layer3InsightCard.next_steps[0]` for `metabolic__system_pressure`.

**Safety class routing:**
- `signal_hba1c_high` with at_risk state → safety_class = "clinician_referral" → next step: "Consider discussing these results with a clinician, especially if this pattern persists."
- `signal_insulin_resistance` at_risk, HbA1c not at risk → safety_class may be "lifestyle" → next step: "Lifestyle changes that support insulin sensitivity — including dietary and activity improvements — are worth exploring."
- Both signals → "We'd recommend a structured conversation with a clinician about blood sugar and metabolic risk given this pattern."

**Confirmatory test source:** `RootCauseHypothesisV1.confirmatory_tests[]` for signal_insulin_resistance and signal_hba1c_high — may include OGTT, fasting insulin, c-peptide depending on hypothesis.

**Status: directly available from Layer3InsightCard.next_steps. Safety_class-based routing codifies the clinician-referral vs lifestyle distinction already present in the root cause output.**

---

### Source-of-truth mapping — blood sugar control

| Component | Primary source | Assembly needed | Gap |
|---|---|---|---|
| Headline sentence | `HealthSystemScore.overall_score` (metabolic) → band lookup | Deterministic lookup table | None |
| Contributor sentence | `IDL.subtitle` of primary active phenotype (ph_metabolic_early_ir_v1 or ph_hba1c_metabolic_stress_v1) | Signal + prediabetes override state selection | Prediabetes override path needs explicit handling |
| Confidence sentence | `Layer3InsightCard.confidence` + cluster_confidence["metabolic"] | Governed template bank (4 sentences) | None |
| What would improve confidence | `RootCauseHypothesisV1.missing_data[]` for active metabolic signals | Surface in DomainScore contract | None |
| Consequence sentence | `IDL.why_it_matters` of active phenotype | Select by dominant signal | None — both IDL records have governed consequence sentences |
| Next-step sentence | `Layer3InsightCard.next_steps[0]` (metabolic__system_pressure) | Safety_class routing | None |

---

### Confidence logic inputs — blood sugar control

1. `ConfidenceModelV1.cluster_confidence["metabolic"]` — glucose + hba1c required; both present = 1.0
2. Insulin present → TyG computable, HOMA-IR computable → escalates to High
3. Triglycerides present → full TyG computation → escalates to Good minimum
4. Prediabetes override triggered → confidence escalates (override is a governed ADA 2026 rule, not a marginal threshold)
5. `Layer3InsightCard.confidence` for metabolic__system_pressure
6. Active IDL record present → Good minimum

---

### Safe claims — blood sugar control

The expanded card can truthfully say today:
- Whether glucose and HbA1c are within their scoring bands and what band they are in
- Whether the TyG index suggests early insulin resistance (when triglycerides available)
- Whether HOMA-IR is computable and what it shows (when insulin available)
- Whether the pattern meets prediabetes criteria (HbA1c ≥ 5.7% or glucose ≥ 5.6 mmol/L)
- Which markers are missing (insulin, triglycerides) and what they would add
- The longer-term metabolic risk direction (drawn from IDL why_it_matters — prediabetes progression, cardiometabolic risk)
- Whether lifestyle or clinician consultation is the appropriate next step

The card must NOT say:
- That the user has diabetes or prediabetes as a medical diagnosis
- A specific A1c target or glucose treatment goal
- Any claim about medication need or specific treatment

---

## Domain 3: Liver Health

**Consumer label:** Liver health
**Clinical label:** Hepatic-Metabolic Strain Status

---

### Narrative components

#### 3.1 Headline sentence

**Template (score-band driven):**

| Score band | Headline sentence |
|---|---|
| 80–100 | "Your liver health looks strong based on your current enzyme markers." |
| 65–79 | "Your liver health looks broadly stable based on your current enzyme markers." |
| 45–64 | "Your liver enzyme pattern shows some signals worth watching." |
| 0–44 | "Your liver enzyme pattern shows a pattern that deserves closer review." |

**Important:** The phrase "enzyme markers" is required in this headline. The scoring_policy liver system is built only on ALT and AST — the headline must not imply a comprehensive liver assessment beyond what the markers support.

**Source of truth:** `HealthSystemScore.overall_score` for the `liver` scoring system. When GGT or ALP are also present, blend with `system_capacity_scores["hepatic"]` (hepatic burden capacity) and use the lower of the two as the domain score floor to avoid false reassurance.

**Status: assemblable with the blending logic described in the blueprint. The headline sentence template is safe as long as "enzyme markers" is used — not "liver health" alone as if it were a comprehensive organ assessment.**

---

#### 3.2 Contributor sentence

**Logic:** Signal type determines the contributor sentence. Hepatic signal priority:

1. `signal_hepatic_metabolic_stress` at_risk → "Both ALT and GGT are elevated together — a pattern consistent with metabolic liver strain."
2. `signal_hepatic_alt_context` at_risk + `signal_ggt_high` at_risk → "ALT and GGT are both elevated, suggesting combined liver cell and metabolic load."
3. `signal_hepatic_alt_context` at_risk alone → "Your ALT enzyme is elevated, indicating the liver is under some degree of cell-level strain."
4. `signal_ggt_high` at_risk alone → "GGT is elevated — a sensitive indicator of liver metabolic load or alcohol-related strain."
5. `signal_alp_high` at_risk → "ALP is elevated, which may indicate bile duct strain or bone-related turnover."
6. `signal_hepatic_alt_context` suboptimal only → "Your ALT is slightly above the optimal range — worth monitoring over time."
7. No signals active → "Your liver enzyme markers are within their reference ranges."

**Pattern differentiation (KB-supported):**
The KB packages `pkg_kb52c_alt_high_hepatocellular_injury_pattern`, `pkg_kb52c_alt_high_metabolic_steatotic_liver_pattern`, and `pkg_kb52c_alt_high_muscle_source_or_exertional_pattern` support three distinct ALT elevation contexts. When these phenotype-level distinctions are active (via IDL or root cause), the contributor sentence should reflect them:
- Steatotic pattern (ALT + triglycerides/metabolic load): "Your ALT elevation fits a metabolic-strain pattern, consistent with fatty liver-type loading."
- Hepatocellular pattern (AST/ALT ratio context): "Your liver enzyme pattern suggests hepatocellular stress rather than isolated metabolic load."
- Muscle-source pattern (CK co-elevated): "ALT elevation alongside muscle markers may reflect exertional or muscle-related enzyme release, not liver cell injury."

**Primary sources:**
- `RootCauseFindingV1.signal_state` for hepatic signals
- `IDL.subtitle` for `ph_hepatic_alt_inflammatory_v1` = "A pattern suggesting metabolic or inflammatory strain in the liver"
- `Layer3InsightCard.interpretation` for `hepatic__system_pressure` (fallback)
- `RootCauseHypothesisV1.title` of the top-ranked hypothesis for signal_hepatic_alt_context (provides the most specific pattern label)

**Status: assemblable with light signal selection logic. Pattern differentiation is already supported by the root cause output — the assembler needs to surface the correct hypothesis title.**

---

#### 3.3 Confidence sentence

**This is the one genuine gap in Wave 1 narrative confidence logic.**

**The problem:** `ConfidenceModelV1.cluster_confidence["hepatic"]` is structurally inadequate for the liver domain. The `hepatic` cluster in clusters.yaml only requires ALT. When ALT is present, `cluster_confidence["hepatic"] = 1.0` — regardless of whether GGT, ALP, albumin, bilirubin, or total protein are also available. This gives no signal about whether a 2-marker or 7-marker liver panel was provided.

**Required fix:** Domain-level confidence for liver must count hepatic burden-registry markers explicitly, not just the cluster schema markers. The relevant marker pool is: alt (required), ast (important), ggt, alp, albumin, bilirubin, total_protein, globulin.

**Proposed confidence logic (new, to be implemented in domain_score_assembler.py):**

| Present markers from hepatic pool | Level | Sentence |
|---|---|---|
| alt + ast + ggt + alp + albumin (5+) | High | "Confidence is high — your full liver function panel provides a well-rounded hepatic picture." |
| alt + ast + ggt (3–4) | Good | "Confidence is good — key liver enzymes are present, though a fuller panel would add depth." |
| alt + ast only (2) | Moderate | "Confidence is moderate — ALT and AST are present; GGT, ALP, and albumin would complete the liver picture." |
| alt only (1) | Limited | "Confidence is limited — a fuller liver function panel including AST, GGT, and albumin would significantly improve this picture." |

**What would improve confidence:**
- `RootCauseHypothesisV1.missing_data[]` for signal_hepatic_alt_context — will list missing hepatic markers and their roles (e.g., {marker_id: "ggt", reason: "GGT would clarify whether ALT elevation has a metabolic or alcohol-related component."})
- This list exists in the root cause output when GGT/ALP/albumin are absent

**Status: confidence level from existing outputs (Layer3InsightCard.confidence) is available but is based on the narrow cluster schema and will not reflect genuine hepatic panel depth. New domain-level confidence counting logic is needed. This is the one concrete confidence gap in Wave 1.**

---

#### 3.4 What this may mean over time

**Primary source — strongest of all three Wave 1 domains:**

`IDL.why_it_matters` for `ph_hepatic_alt_inflammatory_v1` = "Early liver-strain patterns are a key lane toward MASLD/fibrosis risk if ignored."

This is a governed, appropriately calibrated consequence sentence. It is already in the repo. It uses medically grounded language (MASLD) without being alarmist.

**Selection logic:**
- If `signal_hepatic_alt_context` at_risk or `signal_hepatic_metabolic_stress` at_risk → use `ph_hepatic_alt_inflammatory_v1.why_it_matters`
- If only `signal_ggt_high` active → "Persistently elevated GGT is worth monitoring — it can reflect ongoing metabolic, alcohol, or liver strain."
- If only `signal_alp_high` active → "Elevated ALP patterns warrant monitoring as they can reflect bile duct, bone, or liver-related changes."
- If no signals active → "Keeping liver enzymes within range over time supports long-term liver resilience."

**Status: fully ready. The IDL why_it_matters sentence for ph_hepatic_alt_inflammatory_v1 is the most complete single consequence statement in the Wave 1 set. No new KB work needed.**

---

#### 3.5 What to do next

**Primary source:** `Layer3InsightCard.next_steps[0]` for `hepatic__system_pressure`.

**Safety class routing:**
- `signal_hepatic_alt_context` at_risk + `signal_hepatic_metabolic_stress` → safety_class likely "clinician_referral" → "We'd recommend discussing these liver enzyme findings with a clinician, particularly if the pattern persists."
- `signal_hepatic_alt_context` suboptimal only → safety_class likely "monitoring" → "Monitoring ALT over time, alongside lifestyle factors like alcohol and diet, is a sensible next step."

**Confirmatory tests source:** `RootCauseHypothesisV1.confirmatory_tests[]` for signal_hepatic_alt_context will include: GGT (if absent), ALP, albumin, full LFT panel, potentially ultrasound if steatotic pattern.

**Status: directly available from Layer3InsightCard.next_steps. No new contract work needed.**

---

### Source-of-truth mapping — liver health

| Component | Primary source | Assembly needed | Gap |
|---|---|---|---|
| Headline sentence | `HealthSystemScore.overall_score` (liver) blended with hepatic burden capacity | Blending rule based on marker availability | None — blueprint defines the blend rule |
| Contributor sentence | `Layer3InsightCard.interpretation` (hepatic__system_pressure) or `IDL.subtitle` of active record | Signal type and pattern differentiation selection | None — root cause provides pattern labels |
| Confidence sentence | Domain-level marker count (hepatic burden pool) | **New domain confidence counter needed** | **Gap: cluster_confidence["hepatic"] is always 1.0 when ALT present — unsuitable for consumer confidence display** |
| What would improve confidence | `RootCauseHypothesisV1.missing_data[]` for active hepatic signals | Surface in DomainScore contract | None |
| Consequence sentence | `IDL.why_it_matters` of `ph_hepatic_alt_inflammatory_v1` | Select by active signal | None — best pre-built consequence sentence in Wave 1 |
| Next-step sentence | `Layer3InsightCard.next_steps[0]` (hepatic__system_pressure) | Safety_class routing | None |

---

### Confidence logic inputs — liver health

1. **New domain-level counter (required):** count present markers from the hepatic burden pool {alt, ast, ggt, alp, albumin, bilirubin, total_protein, globulin} — 1=Limited, 2=Moderate, 3–4=Good, 5+=High
2. `ConfidenceModelV1.cluster_confidence["hepatic"]` — structurally inadequate on its own (do not use as sole input)
3. `Layer3InsightCard.confidence` for `hepatic__system_pressure` — usable as one input
4. Signal concordance: multiple hepatic signals active and concordant → escalates confidence
5. Pattern differentiation available: steatotic, hepatocellular, or cholestatic pattern identified by root cause → Good minimum
6. Active IDL record present → Good minimum

---

### Safe claims — liver health

The expanded card can truthfully say today:
- Whether ALT (and AST if present) are within their scoring bands
- The pattern type (hepatocellular / metabolic-steatotic / muscle-source) if the root cause differentiates it
- Whether GGT and/or ALP are elevated and what they add to the picture (when present)
- The direction of the hepatic metabolic stress pattern when both ALT and GGT are elevated
- Which markers are missing and what they would clarify
- The specific consequence framing: MASLD/fibrosis risk if strain persists (from governed IDL)
- Whether monitoring or clinician review is the next step

The card must NOT say:
- That the user has MASLD, fibrosis, or any specific liver disease
- That alcohol use is definitely the cause of any elevation
- That any elevation alone is diagnostic

---

## Final Summary

### A. Shared narrative assembly template

All three Wave 1 domains use the same five-component structure. The assembly source per component follows a consistent pattern:

```
1. Band statement
   Source: scoring_policy system score → deterministic band lookup table
   Template: "[Domain] looks [band_label] based on your current [domain-appropriate marker descriptor]."

2. Contributor sentence
   Source: IDL.subtitle of primary active phenotype (preferred) OR Layer3InsightCard.interpretation
   Logic: select by dominant active signal; if multiple signals, use signal priority rule

3. Confidence sentence
   Source: domain-level confidence level → governed template bank (four sentences per domain)
   Detail: RootCauseHypothesisV1.missing_data[] → "what would improve confidence" expandable list

4. Consequence sentence
   Source: IDL.why_it_matters of primary active phenotype
   Fallback: governed static sentence when no IDL record is active

5. Next-step sentence
   Source: Layer3InsightCard.next_steps[0] for system pressure card
   Fallback: NarrativeReportV1.next_steps_narrative (first sentence)
```

---

### B. Domain-specific deviations

**Cardiovascular health:**
- Consequence sentence has a **gap for lipid-dominant patterns** (no IDL why_it_matters on ph_lipid_residual_ldl_favourable_transport_v1). Requires either: (a) IDL record update, or (b) functional_interpretation routing, or (c) governed static fallback sentence.
- Contributor sentence needs a **signal priority rule** that can differentiate between lipid transport dysfunction, isolated LDL, HDL-only, and homocysteine-dominant patterns.
- The richest extended-confidence depth of the three (ApoB, ApoA1, homocysteine, derived ratios all available when present).

**Blood sugar control:**
- The **prediabetes override** in signal_insulin_resistance requires explicit handling in the contributor sentence path — the override state is distinct from a high TyG reading and should surface its own sentence.
- Consequence sentences are the most ready (IDL why_it_matters fields for both metabolic phenotypes are complete and strong).
- No confidence gaps.

**Liver health:**
- The **confidence logic is the one concrete structural gap** in Wave 1. `cluster_confidence["hepatic"]` gives no panel depth information. A domain-level hepatic marker counter must be built into the domain score assembler.
- Pattern differentiation (steatotic vs hepatocellular vs muscle-source) is already supported in the root cause output and should be surfaced in the contributor sentence.
- Consequence sentence is fully ready — the best of the three domains for this component.

---

### C. Contract implications

The following additions to the AnalysisDTO / new component contracts are needed to support the Wave 1 domain narrative cleanly:

| Addition | Location | Why needed |
|---|---|---|
| `consumer_domain_scores: Optional[Dict[str, DomainScore]]` | AnalysisDTO | Primary new contract surface — holds all domain score data per domain |
| `DomainScore.score: int` (0–100) | DomainScore model | Consumer domain score value |
| `DomainScore.band_label: str` | DomainScore model | "Strong" / "Stable" / "Watch" / "Needs attention" |
| `DomainScore.confidence: Literal["high", "good", "moderate", "limited"]` | DomainScore model | Four-level domain confidence |
| `DomainScore.confidence_sentence: str` | DomainScore model | Pre-assembled governed confidence sentence |
| `DomainScore.contributor_sentence: str` | DomainScore model | Pre-assembled governed contributor sentence |
| `DomainScore.consequence_sentence: str` | DomainScore model | Pre-assembled governed consequence sentence (IDL why_it_matters) |
| `DomainScore.next_step_sentence: str` | DomainScore model | Pre-assembled from Layer3InsightCard.next_steps[0] |
| `DomainScore.missing_marker_ids: List[str]` | DomainScore model | Sourced from RootCauseHypothesisV1.missing_data[] — "what would improve confidence" |
| `DomainScore.active_signal_ids: List[str]` | DomainScore model | Active signals that contributed to this domain score |
| `DomainScore.primary_idl_record_id: Optional[str]` | DomainScore model | The IDL internal_id of the driving phenotype (nullable when no IDL record active) |
| New domain-level hepatic confidence counter | `domain_score_assembler.py` | Cluster_confidence["hepatic"] is inadequate — needs marker pool count |
| `ph_lipid_residual_ldl_favourable_transport_v1.why_it_matters` field | `knowledge_bus/interpretation_display_layer_v1/idl_records_v1.yaml` | Consequence sentence gap for lipid-dominant cardiovascular patterns |

**Existing fields that can be consumed directly (no contract addition needed):**
- `Layer3InsightCard.next_steps[]` for each system pressure card
- `IDL.why_it_matters` for ph_metabolic_early_ir_v1, ph_hba1c_metabolic_stress_v1, ph_hepatic_alt_inflammatory_v1
- `IDL.subtitle` for all three relevant phenotypes
- `RootCauseHypothesisV1.missing_data[]` per active signal
- `HealthSystemScore.overall_score` for cardiovascular, metabolic, liver
- `ConfidenceModelV1.cluster_confidence` (supplementary only for liver)

---

### D. Implementation readiness

| Domain | Component | Status |
|---|---|---|
| **Cardiovascular health** | Headline sentence | Narrative-ready now |
| | Contributor sentence | Narrative-ready with light assembly (signal priority selection rule) |
| | Confidence sentence | Narrative-ready with light assembly (governed template bank) |
| | Consequence sentence | **Partial gap** — needs IDL record update or functional_interpretation routing for lipid-dominant patterns |
| | Next-step sentence | Narrative-ready now |
| **Overall** | | **Narrative-ready with light assembly + one KB content gap** |
| **Blood sugar control** | Headline sentence | Narrative-ready now |
| | Contributor sentence | Narrative-ready with light assembly (prediabetes override handling) |
| | Confidence sentence | Narrative-ready with light assembly (governed template bank) |
| | Consequence sentence | **Narrative-ready now** — both IDL why_it_matters sentences are complete |
| | Next-step sentence | Narrative-ready now |
| **Overall** | | **Narrative-ready with light assembly — strongest of the three** |
| **Liver health** | Headline sentence | Narrative-ready with light assembly (blend rule from blueprint) |
| | Contributor sentence | Narrative-ready with light assembly (pattern differentiation) |
| | Confidence sentence | **Narrative-ready only after domain-level confidence counter built** — cluster_confidence["hepatic"] is structurally inadequate |
| | Consequence sentence | **Narrative-ready now** — IDL why_it_matters for ph_hepatic_alt_inflammatory_v1 is complete and strong |
| | Next-step sentence | Narrative-ready now |
| **Overall** | | **Narrative-ready with light assembly + one concrete confidence logic gap** |

---

## Appendix: Governed consequence sentences available today (no new KB work)

These sentences can be drawn from existing IDL why_it_matters fields without authoring new KB content:

| Domain | Condition | Source | Sentence |
|---|---|---|---|
| Blood sugar | IR signal active | ph_metabolic_early_ir_v1.why_it_matters | "Left unaddressed, early insulin resistance progresses toward prediabetes and cardiometabolic risk." |
| Blood sugar | HbA1c signal active | ph_hba1c_metabolic_stress_v1.why_it_matters | "Sustained glycaemic strain raises long-term metabolic and vascular risk." |
| Cardiovascular | Vascular/homocysteine signal active | ph_vascular_hcy_inflammation_v1.why_it_matters | "Accumulating vascular-risk signals warrant cardiometabolic review and lifestyle action." |
| Cardiovascular | Lipid-dominant, no homocysteine | ph_lipid_residual_ldl_favourable_transport_v1 | **Gap — no why_it_matters field present in current IDL record. Requires content addition.** |
| Liver | ALT/hepatic signal active | ph_hepatic_alt_inflammatory_v1.why_it_matters | "Early liver-strain patterns are a key lane toward MASLD/fibrosis risk if ignored." |

---

*End of contract spec. This document is research-only. All implementation requires GPT-authored work packages, Claude hardening, and kernel execution per Automation Bus SOP v1.3.1.*
