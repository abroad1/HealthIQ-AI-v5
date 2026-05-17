# LC-S11 — Forensic Human UAT Audit

**Date:** 2026-05-17  
**Auditor:** Claude Code (forensic product/architecture role)  
**Analysis ID reviewed:** `c440dfa2-12a1-4e29-95a5-ee07a2397c59`  
**Test account:** `test-user3@example.com`

---

## 1. Executive Verdict

**Verdict: PASS WITH GAPS**

The core analytical path for the launch-core homocysteine/methylation/vascular-risk finding is plausible, governed, and produces a coherent user-facing interpretation. The alcohol lifestyle bridge is working and visibly personalising the body overview. The Knowledge Bus assets for the lead finding are substantive.

However, the product has four categories of problem that must be addressed before external human testing:

1. **A legacy `insights[]` surface is still active with placeholder text.** The planning paper explicitly required this to be removed or gated before launch. It is still present in the JSON and — depending on which frontend surface renders it — represents an unsatisfied planning paper commitment.

2. **The blood sugar domain card surfaces narrative copy ("early impaired sugar and lipid handling") with zero active signals behind it.** This is fabricated confidence: the domain has no fired IDL record, `active_signal_ids: []`, and `primary_idl_record_id: null`.

3. **ApoA1 is classified as a cardiovascular risk signal when it is clinically protective.** ApoA1 1.73 g/L (above lab max 1.69 g/L) is flagged as `signal_apoa1_cardio_risk`. Elevated ApoA1 is associated with protective reverse cholesterol transport, not increased cardiovascular risk. The UI shows "ApoA1 · Elevated" alongside the lead homocysteine finding, implying it is a negative marker. It is not.

4. **ALT 7 U/L below the reference range minimum is classified "critical" (score 0.05/100) and drives the liver domain to 5/100 "Needs review" with alarming headline copy.** Low ALT is a non-finding clinically. The engine is penalising a low normal value at the same severity as a dangerously elevated one.

Together, gaps 2–4 would undermine trust with a medically literate user or clinician. Gap 1 is a planning-paper commitment that remains open.

---

## 2. Sources Reviewed

| Source | Location/Path |
|---|---|
| Planning paper | `docs/planning-papers/healthiq_launch_core_transformation_plan_FINAL.md` |
| Live results page | `http://localhost:3000/results?analysis_id=c440dfa2-12a1-4e29-95a5-ee07a2397c59` |
| Downloaded analysis JSON | `C:\Users\abroa\Downloads\healthiq-analysis-2026-05-17.json` |
| Homocysteine KB signal library | `knowledge_bus/packages/pkg_homocysteine_elevation_context/signal_library.yaml` |
| Homocysteine KB research brief | `knowledge_bus/packages/pkg_homocysteine_elevation_context/research_brief.yaml` |
| Knowledge Bus package inventory | `knowledge_bus/packages/**` (glob) |
| Analytics engine inventory | `backend/core/analytics/**` (glob) |

---

## 3. Planning Intent Summary

The planning paper (v5, 2026-05-06) describes a six-sprint programme to prove a **bounded but real vertical slice** of a personalised health pipeline. It is not a veneer MVP.

The slice must prove:
- Biomarkers fire correct signals; ranking chooses a believable lead finding
- Governed WHY appears where it should; honest fallback where it does not
- Lifestyle inputs **visibly** influence output
- Medication inputs visibly influence output (one bounded class)
- Layer B produces correct structured truth; Layer C polishes rather than reinterprets
- The UX carries that truth coherently
- Same inputs reproduce same outputs
- Regression tests protect the proven slice

The planning paper explicitly called out:
- `insights[]` must be **removed or gated** before launch (legacy placeholder surface)
- No "questionnaire theatre" — if the user provides context, it must visibly change output
- No contradiction between hero, overview, domain cards, clinician surface
- No placeholder confidence language without evidence behind it

The threshold for success is: *"the bounded launch-core report is genuinely personalised, the product visibly uses the core inputs it asks for, the full pipeline works end-to-end, and future work can be mostly additive."*

---

## 4. Human UI Review

### What works well

**Lead finding hero**: The "Primary finding" card is clear. "Homocysteine Elevation Context: warrants attention on this panel" is unambiguous. The "Strong Signal" badge and "Vascular Inflammation Risk" system label are coherent and appropriate.

**Summary section**: Readable. References the methylation pathway pattern directly. Appropriately hedged ("does not replace clinician judgement"). No overconfidence.

**"What's driving this" section**: Lists ApoA1, Homocysteine, Total Cholesterol, and Transferrin with values and status labels. Functionally useful, though ApoA1 being listed as a negative driver is clinically incorrect (see Section 13).

**Lifestyle personalisation in Body Overview**: The alcohol bridge is working. The text reads: *"Your questionnaire suggests moderate alcohol intake, which can be relevant when interpreting homocysteine because alcohol intake may increase demand on one-carbon nutrients such as folate and B vitamins."* This is correct, proportionate, and genuinely personalised. This is a meaningful success against the planning paper's Sprint 2 requirement.

**Lead narrative "What this means"**: The methylation pathway explanation is substantive — it covers one-carbon metabolism, remethylation vs transsulfuration, red-cell indices, the B12-associated and folate-associated hypotheses, and the renal and inflammatory context patterns. For a consumer product, this is unusually rich and credible.

**Root-cause hypotheses**: Four hypotheses rendered (B12-associated, folate-associated, renal clearance, inflammatory context). Each includes supporting evidence, limiting factors, and confirmatory test recommendations. The handling of "B12 within range but homocysteine elevated" is particularly well done — the engine correctly avoids false confidence.

**Confidence language**: Appropriate throughout. "confidence weight 0.60 — structured ranking only" is honest. Missing data caveats (MMA, FBC indices) are surfaced.

**Trust strip / Data quality**: "9 of 9 expected markers, quality checks passed" is a clear, positive trust signal.

**"Your system health" section**: Lists Hematological and Renal as broadly stable. Clear, proportionate.

**Clinician synthesis**: The fast-read header in the clinician section accurately names the lead pattern, primary marker, confidence score (0.95), and confidence drivers (ALL_SUPPORTING_MARKERS_PRESENT, ESCALATION_SINGLE_CONDITION). This is functionally correct.

### What is confusing or thin

**Blood sugar domain card**: Score 84/100, band "Strong", headline reads "A pattern suggesting early impaired sugar and lipid handling." No signals are active behind this. HbA1c is 26 mmol/mol (optimal). No glucose or insulin in the panel. The narrative is running on a fallback template with no evidence beneath it. The confidence note says "Limited confidence — additional glycaemic markers would strengthen the read," but the band still says "Strong." The combination of "Strong" band + "Limited confidence" + "early impaired sugar handling" copy when HbA1c is optimal is internally contradictory and would confuse a user.

**Cardiovascular domain: "Stable" band label vs active lead finding**: The cardiovascular domain shows "Stable / 73/100 / High confidence." The lead finding on this exact panel is in the cardiovascular system. "Stable" alongside the primary warning signal creates a tone mismatch. The headline copy tries to compensate ("not a simple all-clear: the leading pattern here still deserves clinical context"), but the band label does real damage to that message.

**Liver domain: "5/100 Needs Review" for low ALT**: The liver score is driven to 5/100 primarily by ALT = 7 U/L falling below the lab reference range minimum of 10 U/L. The UI displays "Needs review" with "Your liver enzyme pattern shows a pattern that deserves closer review." Low ALT is not clinically alarming. This will alarm a user unnecessarily and damage credibility with any medically informed reader.

**ApoA1 listed as a cardiovascular risk finding**: ApoA1 1.73 g/L is 0.04 above the lab upper range (1.69). Elevated ApoA1 is a protective marker — it is the major apolipoprotein of HDL particles. The signal `signal_apoa1_cardio_risk` fires, placing it in the "What's driving this" list alongside genuinely concerning markers. A UK or US clinician reviewing this would immediately notice that elevated ApoA1 is being treated as a risk factor.

**"Other patterns considered on this panel — Systemic Inflammation"**: The lead narrative section states "A systemic inflammation signal fired, indicating inflammatory context on this panel." CRP is 1.1 mg/L with status "normal" (scored 76.1/100). The signal library escalation rule for homocysteine fires at CRP ≥ 3.0. The statement that a systemic inflammation signal "fired" is not clearly reconciled with CRP being within the broad lab range (0–10 mg/L). Users and clinicians will notice this.

**Biomarker display labels**: Multiple labels are machine-generated and sub-professional (see Section 12).

**`secondary_systems` is empty string**: `narrative_report_v1.secondary_systems` is a string of length 0. Minor but indicates incomplete pipeline assembly.

**Fragmented report feel at the bottom**: The lower half of the page (Direction and follow-up, Clinician evidence) assembles text from multiple subsections without a clear progression. A user who reads top-to-bottom experiences some repetition and non-linear flow.

---

## 5. JSON / Payload Forensic Review

### Payload summary

| Field | Value/State |
|---|---|
| `analysis_id` | c440dfa2-12a1-4e29-95a5-ee07a2397c59 |
| `status` | completed |
| `result_version` | 1.0.0 |
| `overall_score` | 0.601 |
| `primary_driver_system_id` | cardiovascular_4_biomarkers |
| Biomarker count | 77 |
| Derived markers | 8 (tc_hdl_ratio, tg_hdl_ratio, ldl_hdl_ratio, non_hdl_cholesterol, apob_apoa1_ratio, remnant_cholesterol, urea_creatinine_ratio, testosterone_free_testosterone_ratio) |
| Active signals (CV domain) | signal_apoa1_cardio_risk, signal_homocysteine_elevation_context, signal_homocysteine_high, signal_total_cholesterol_high |
| Lead signal | signal_homocysteine_elevation_context |
| Lifestyle alcohol bridge | Active (moderate, 11 units/week) |
| Fasting/dietary bridge | Active (intermittent fasting, 13–14 hours) |
| Medication context | None (no medications in questionnaire) |
| Missing markers | metabolic: [glucose, insulin]; liver: [ast] |

### Structural observations

**`insights[]` is active with placeholder text.** Three entries present:
- "Metabolic focus: summarise structured signals; review with your clinician"
- "Cardiovascular focus: summarise structured signals; review with your clinician"
- "Inflammatory focus: summarise structured signals; review with your clinician"

All three have `biomarkers_involved: []`. These are generic LLM-translation stubs that were never resolved. The planning paper explicitly required this surface to be gated or removed.

**`narrative_report_v1.lead_narrative` is a flat string, not a structured object.** The entire multi-hypothesis WHY content is pre-serialised into a text blob. There are no machine-readable fields for `lead_signal_id`, `why_source`, `lifestyle_bridge`, or `root_cause_hypotheses`. This means Sprint 3 (governed payload shape) has not been implemented in structured form — the Layer B → Layer C boundary is carried by unstructured text concatenation.

**`narrative_report_v1.lifestyle_context` and `medication_context` are null.** Despite the alcohol bridge being active, the structured fields are not populated. Personalisation content lives only in `body_overview` text.

**`deferred_kb_content: "lipid_dominant_cv_why_it_matters_gap_deferred_sprint"` is exposed in consumer_domain_scores.** This internal sprint-management reference is leaking into the consumer-facing JSON payload.

**`narrative_payload_v1_digest.payload_analysis_id` ≠ top-level `analysis_id`.** The meta digest shows `9766d69e-57e9-4b8e-aaba-a6c9d8ce7e23` but the top-level `analysis_id` is `c440dfa2-12a1-4e29-95a5-ee07a2397c59`. This could be an intermediate vs final analysis ID artefact but warrants investigation.

**BMI 55.3456 in lifestyle modifier context.** This is a test account value. The lifestyle modifier is active on the metabolic system (capped at 0.07). Cannot fully assess BMI-driven personalisation with this test data.

---

## 6. Biomarker-by-Biomarker Plausibility Table

| Biomarker | Value / Range / Status | Triggered Systems / Signals | Plausible? | User-Facing Quality | Notes |
|---|---|---|---|---|---|
| Homocysteine | 16.23 µmol/L / 3.7–13.9 / elevated | Vascular, signal_homocysteine_elevation_context, signal_homocysteine_high | ✅ Yes | Good | Correctly identified as lead; hypothesis set is rich |
| MCV | 99.5 fL / 80–96 / elevated | Hematological (cluster), supporting marker for homocysteine signal | ✅ Yes | Good | Correctly cited as macrocytosis context for B12/folate hypotheses |
| Transferrin | 2.0 g/L / 2.15–3.65 / critical | Supporting marker in homocysteine signal (transport context) | ✅ Plausible | Adequate | Low transferrin as one-carbon pathway context is defensible; "Critical" label without standalone explanation may alarm users |
| Total Cholesterol | 5.26 mmol/L / 0–5.18 / elevated | Cardiovascular, signal_total_cholesterol_high | ✅ Yes | Adequate | Only marginally elevated; the secondary lipid transport narrative is justified |
| ApoA1 | 1.73 g/L / 0.79–1.69 / elevated | Cardiovascular, signal_apoa1_cardio_risk | ❌ NO | Poor | Elevated ApoA1 is protective, not a risk signal. Listing this as a cardiovascular risk driver is clinically incorrect. |
| ALT | 7 U/L / 10–49 / critical | Hepatic (score driver → 5/100) | ❌ NO | Poor | Low ALT is not a clinical danger signal. Classifying below-minimum ALT as equivalent severity to high ALT is a plausibility failure. |
| CRP | 1.1 mg/L / 0–10 / normal | Inflammatory context for homocysteine (limited) | ⚠️ Partial | Confusing | "Systemic Inflammation signal fired" stated in WHY copy despite CRP being within lab range. The hs-CRP 1.0–3.0 mg/L intermediate risk zone may be relevant but is not explained. |
| HbA1c | 26 mmol/mol / max 39 / optimal | Metabolic (via scoring rail only) | ✅ Yes | Good | Correctly not driving any active signal. Score 83.6/100 is appropriate. |
| LDL | 2.75 mmol/L / 2.59–3.34 / optimal | Cardiovascular cluster | ✅ Yes | Not prominently surfaced | Within range and correctly given low prominence |
| HDL | 2.22 mmol/L / min 1.55 / optimal | Cardiovascular cluster | ✅ Yes | Not surfaced | Very high HDL, correctly given no negative prominence |
| Triglycerides | 0.68 mmol/L / max 1.7 / optimal | Cardiovascular cluster | ✅ Yes | Not surfaced | Excellent trig level; correctly not surfaced |
| Creatinine | 87 µmol/L / 53–97 / optimal | Renal | ✅ Yes | Not prominently surfaced | In range; correctly stable |
| eGFR | 84 mL/min/1.73m² / low | Renal (stable, confidence: insufficient) | ⚠️ Partial | Not surfaced | mildly reduced eGFR in a person this age warrants mention; currently silent |
| Vitamin D | 89.13 nmol/L / low | Not surfaced as active signal | ⚠️ Partial | Not surfaced | Low by lab range but 89.13 nmol/L is clinically sufficient (≥50). Scoring as "low" may produce unnecessary user concern if this biomarker is ever surfaced. |
| TG/HDL ratio | 0.306 / low | Not surfaced | ⚠️ Worth noting | Not surfaced | "Low" TG/HDL is protective. System flagging this as "low" is directionally wrong for cardiovascular risk. Currently not surfaced — acceptable in this run but a latent issue. |
| Non-HDL | 3.04 mmol/L / 0–3.37 / elevated | Cardiovascular cluster | ⚠️ Unclear | Adequate | Within lab range (3.04 < 3.37) yet status "elevated" — inconsistency between score (89.2/100 = near-optimal) and status label suggests a threshold mismatch between scoring policy and status engine. |
| ALP | 46 U/L / 46–116 / low | Hepatic | ✅ Yes | Not surfaced | At the exact minimum boundary; low ALP is generally not clinically significant. |

---

## 7. System / Domain Plausibility Table

| System / Domain | Supporting Biomarkers | JSON Evidence | UI Evidence | Verdict | Notes |
|---|---|---|---|---|---|
| **Cardiovascular (lead)** | Homocysteine, Total Cholesterol, ApoA1, Transferrin (supporting) | `active_signal_ids` includes signal_homocysteine_elevation_context, signal_total_cholesterol_high, signal_apoa1_cardio_risk | "Cardiovascular health 73/100 Stable / High confidence" + lead finding card | ✅ Plausible with caveats | ApoA1 as risk signal is incorrect; rest is justified |
| **Hematological** | Hemoglobin, Hematocrit, WBC, Platelets (all optimal); MCV elevated | Balanced systems: "broadly within expected ranges, confidence: insufficient" | Listed as stable in "Your system health" | ✅ Yes | Correctly stable. MCV elevation contributing to homocysteine pathway is handled in lead narrative. |
| **Renal** | Creatinine (optimal), Urea (optimal); eGFR (low) | Balanced systems: "broadly within expected ranges, confidence: insufficient" | Listed as stable | ⚠️ Partial | Creatinine/urea are fine but eGFR 84 is flagged as "low" in JSON and not surfaced. Acceptable at this stage if not the primary focus. |
| **Hepatic** | ALT (7 U/L, critical — below minimum), ALP (46, at boundary) | System score 5/100; `signal_transferrin_low` active | "Liver health 5/100 Needs review" | ❌ Implausible as presented | The 5/100 score and "Needs review" copy are driven primarily by a LOW ALT, which is not a clinically alarming finding. Confidence is correctly labelled "Limited" but the score and headline are disproportionate. |
| **Metabolic / Blood Sugar** | HbA1c 26 mmol/mol (optimal); glucose and insulin MISSING | `active_signal_ids: []`, `primary_idl_record_id: null` | "Blood sugar control 84/100 Strong / Limited confidence" + "early impaired sugar and lipid handling" | ❌ Unsupported narrative | Active signals: none. IDL record: null. The narrative "early impaired sugar and lipid handling" is template copy with no evidence underneath. |
| **Vascular Inflammation (IDL phenotype)** | Homocysteine, CRP (contextual), ApoA1, transferrin | IDL record `ph_vascular_hcy_inflammation_v1`: severity_state strong_signal | "Primary finding / Vascular Inflammation Risk" | ✅ Yes | The strongest and best-evidenced surface in the report |

---

## 8. Lead Finding Analysis

**Lead finding:** Homocysteine Elevation Context (at_risk)  
**Signal:** `signal_homocysteine_elevation_context`  
**Governing KB package:** `pkg_homocysteine_elevation_context` (signal_library + research_brief present and substantive)

**Why it fired:** Homocysteine 16.23 µmol/L exceeds lab range maximum of 13.9 µmol/L. Activation logic is `lab_range_exceeded`. Escalation condition fires because transferrin 2.0 g/L triggers the transport deficit rule (< 2.0 threshold — value is at boundary; worth clarifying whether < or ≤ is intended).

**Should it be lead?** Yes. Homocysteine elevation combined with macrocytic red cells (MCV 99.5 fL) and low transferrin is a coherent multi-system finding that requires follow-up. It is the correct lead finding for this panel.

**WHY governance:** Strong. The knowledge bus signal library has mechanistic explanation, biological pathway, supporting marker roles, and override rules. The research brief cites two peer-reviewed papers (CCLM 2020, Nutrients 2019) and correctly categorises evidence as "moderate." The WHY generated in the lead narrative accurately reflects these governed assets.

**Frontend explanation:** Good for the primary consumer pathway. The hypothesis blocks are clear. The handling of "B12 within range but homocysteine elevated" is clinically sophisticated and honest. The B12/folate/renal/inflammatory hypothesis set is appropriate.

**Clinician report advantage:** Marginal. The clinician synthesis adds confidence score (0.95), confidence drivers (`ALL_SUPPORTING_MARKERS_PRESENT`, `ESCALATION_SINGLE_CONDITION`), and suppressed confirmatory test list. The consumer report is already substantive enough that the incremental clinician benefit is smaller than expected.

**Missing data / caveats:** Handled well. MMA explicitly noted as a confirmatory test. FBC indices recommended. Homocysteine repeat in 8–12 weeks noted. These are clinically appropriate.

**Confidence:** The 0.95 confidence score in the clinician report appears high given B12 is within range and the folate-associated hypothesis has confidence weight only 0.60. However, the narrative correctly communicates uncertainty — "confidence weight 0.60 — structured ranking only." The score may reflect that all expected supporting markers were present (ALL_SUPPORTING_MARKERS_PRESENT), not that the diagnosis is certain.

---

## 9. Runner-Up and Secondary Finding Analysis

**Lipid transport / vascular exposure (secondary narrative):** The secondary narrative covers lipid transport biology (VLDL/LDL/HDL particle framing, apoB, remnant exposure). This is substantive and governed content from the lipid transport Knowledge Bus. It is correctly subordinated to the homocysteine lead. Total Cholesterol 5.26 mmol/L, ApoB normal, ApoA1 elevated (HDL-linked), TG very low (0.68) — the framing of "residual LDL exposure in an otherwise favourable transport picture" is clinically accurate.

**Separation from lead:** Clear on page. The secondary narrative renders after the lead in the "What this means" section.

**Blood sugar domain (84/100 "Strong"):** As noted, there are no active signals behind this finding. With zero active signal IDs and `primary_idl_record_id: null`, the contributor sentence "A pattern suggesting early impaired sugar and lipid handling" is template copy without grounding. HbA1c is optimal. Glucose and insulin are absent (correctly noted as missing). This finding should either be suppressed, shown with a clear "insufficient evidence" framing, or linked to an honest fallback.

**Potentially buried findings:**
- **eGFR 84 mL/min/1.73m²**: In a middle-aged adult, mildly reduced eGFR (G2 range) warrants a comment, even if it's "stable on this panel — worth monitoring." Currently silent.
- **ALP 46 U/L at boundary**: Silently suppressed. Acceptable.
- **Vitamin D 89.13 nmol/L scored as "low"**: If surfaced in a future run, will need explanation of why it differs from clinical sufficiency thresholds.

---

## 10. Knowledge Bus / Deterministic Asset Richness

| Area | Asset Evidence | Richness Verdict | Gap |
|---|---|---|---|
| Lead finding — Homocysteine elevation | `pkg_homocysteine_elevation_context`: signal_library with 4 hypothesis types, override rules, supporting marker roles; research_brief with 2 cited papers | **Strong** | Confidence score (0.95) not fully justified in the WHY text relative to the 0.60 hypothesis weights |
| Lead system — Vascular / cardiovascular | IDL record `ph_vascular_hcy_inflammation_v1` with severity_state, subtitle, why_it_matters, supporting_biomarkers_summary | **Adequate** | `deferred_kb_content: lipid_dominant_cv_why_it_matters_gap_deferred_sprint` — lipid-dominant WHY explicitly deferred |
| Biomarker-to-system linkage | Contribution context fields present for most biomarkers (cluster_membership factual statements) | **Adequate** | Linkage language is mechanical ("this marker appears in the following pattern grouping") rather than explanatory |
| WHY hypotheses — homocysteine | Four hypotheses: B12-associated, folate-associated, renal clearance, inflammatory; each with evidence, limits, confirmatory tests | **Strong** | None significant |
| WHY hypotheses — lipid transport | Secondary narrative present and substantive | **Adequate** | Deferred per internal sprint tag |
| Lifestyle modifiers | Alcohol bridge active and surfaced; fasting bridge active | **Adequate** | Structured payload fields (lifestyle_context, medication_context) are null — bridges only appear in text blobs |
| Medication modifiers | No medications in this test case | **Not testable** | Cannot assess medication modifier pathway from this run |
| Missing data | Glucose/insulin (metabolic), AST (liver) explicitly flagged | **Adequate** | eGFR flagged as low but not surfaced as a missing data comment |
| Educational content (biomarker explainers) | Present for major markers (HbA1c, cholesterol fractions, LDL, HDL, creatinine, ALT, hemoglobin, ApoB, etc.) | **Adequate** | Generic structure; not tailored to findings |
| Confidence framing | Governed label (moderate_by_default) used correctly; strengthening/weakening conditions explained | **Strong** | None |
| Blood sugar / metabolic | No active signal; `primary_idl_record_id: null`; fallback narrative template in use | **Fallback only** | Sprint 1 WHY for metabolic/glycaemic domain appears unresolved |

---

## 11. Layer B → Layer C Fidelity

**Does Layer C preserve Layer B truth?**

Largely yes for the lead finding. The homocysteine signal state (at_risk), the four hypotheses, the supporting markers, and the lifestyle bridge all appear in the UI in a form consistent with the JSON payload.

**Does Layer C add unsupported interpretation?**

- The blood sugar domain adds "early impaired sugar and lipid handling" without any supporting signal. This is Layer C generating narrative from a template without Layer B truth behind it. **This is a Layer B → Layer C contract violation.**
- The "Systemic Inflammation signal fired" statement in the lead narrative appears to reference a signal activation that is not obviously supported by CRP 1.1 mg/L being within the broad lab range (0–10 mg/L).

**Does Layer C hide important Layer B findings?**

- The liver score of 5/100 is accurately carried (Layer C doesn't suppress it), but the clinical interpretation attached to a low ALT is misleading.
- eGFR 84 (low) appears in the JSON biomarker list but is not surfaced in any consumer-facing section.

**Does Layer C present canonical analysis in a user-friendly way?**

For the lead finding: yes, notably well. The methylation pathway explanation is clear and appropriately hedged. The hypothesis set is accessible.

**Is the report coherent across surfaces?**

Mostly. The hero, body overview, lead narrative, and clinician synthesis tell a consistent story about homocysteine. The domain cards diverge — the "Stable" band label on cardiovascular contradicts the active lead finding's severity framing.

**Sprint 3 (governed payload shape) status:** Not implemented in structured form. `lead_narrative`, `secondary_narratives`, `next_steps_narrative`, and `clinician_synthesis` are all flat string fields, not structured objects with machine-readable field separations. The planning paper's requirement for a payload where specific fields are "preserved byte-for-byte" vs. fields that "may be polished" cannot be enforced on a string blob.

---

## 12. Display / Unit / Label Fidelity

**Units:** Consistent between analytical and display for all key markers. Homocysteine shows `analytical_unit: "umol/L"` and `display_unit: "µmol/L"` — the µ character is the same thing rendered differently; the UI correctly shows "umol/L". No unit conversion errors observed.

**Reference ranges:** Consistent between analytical and display ranges for all inspected markers. Lab source correctly attributed throughout.

**Biomarker label quality — issues found:**

| Display Label (JSON) | Issue |
|---|---|
| `Alkaline Photosphatase Alp (venous)` | **TYPO**: "Photosphatase" should be "Phosphatase" |
| `C-reactive Protein Crp (venous)` | Capitalisation: "Crp" should be "CRP" |
| `Non Hdl Cholesterol Calculation (venous)` | "Hdl" → "HDL"; "Calculation" is unnecessary and technical |
| `Total Cholesterol/hdl Ratio Calculation (venous)` | "hdl" → "HDL"; "Calculation" is unnecessary |
| `Apob Apoa1 Ratio` | "Apob" → "ApoB"; "Apoa1" → "ApoA1" |
| `Low Density Lipoproteins (venous)` | Should be "LDL Cholesterol" for user clarity |
| `Hba1c (venous)` | "Hba1c" → "HbA1c" |
| `Alanine Aminotransferase Alt (venous)` | Verbose but acceptable; "Alt" → "ALT" preferred |
| `Leukocytes (wbc)` | Mixed naming convention (clinical + abbreviation) |
| `Haematocrit (hct)` | Acceptable UK spelling |
| `Haemoglobin (hgb)` | Acceptable UK spelling |

**"(venous)" suffix ubiquity**: Nearly every marker has "(venous)" appended. This is technically correct but creates a cluttered experience. A UK user will find this normal; a US user may find it slightly unusual but not disorienting.

**`display_is_uploaded_unit: false` for all markers**: This suggests no unit conversions were performed from an uploaded-unit representation. The upload was likely already in SI/standard units.

**`remnant_cholesterol`: `bounds_applied: false`, `bounds_source: null`, `bounds_rejected_reason: "policy_bounds_missing"`** — this derived marker has no reference range and is not surfaced in the UI. Acceptable as a non-surfaced derived value.

---

## 13. User Trust Risks

| Risk | Severity | Evidence |
|---|---|---|
| Blood sugar domain copy ("early impaired sugar and lipid handling") has zero active signals behind it | **BLOCKER** | JSON: `active_signal_ids: []`, `primary_idl_record_id: null`; HbA1c 26 optimal; no glucose/insulin |
| `insights[]` legacy placeholder text still present and active | **BLOCKER** | JSON: 3 entries with "summarise structured signals; review with your clinician", `biomarkers_involved: []` |
| ApoA1 elevated listed as a cardiovascular risk driver | **HIGH** | ApoA1 1.73 g/L flagged as `signal_apoa1_cardio_risk`; elevated ApoA1 is protective, not atherogenic |
| Liver 5/100 "Needs review" driven by low ALT | **HIGH** | ALT 7 U/L below reference minimum (10 U/L); low ALT is clinically uninformative; alarming score for a non-finding |
| "Systemic Inflammation signal fired" stated in WHY with CRP within normal lab range | **HIGH** | CRP 1.1 mg/L, status "normal", scored 76.1/100; signal assertion needs reconciliation against lab range vs hs-CRP thresholds |
| Cardiovascular domain "Stable" band label contradicts active lead finding severity | **MEDIUM** | band_label "stable" with active homocysteine elevation signal; headline copy partially corrects for it but band label dominates at a glance |
| `deferred_kb_content: "lipid_dominant_cv_why_it_matters_gap_deferred_sprint"` in consumer JSON | **MEDIUM** | Internal sprint management string leaking into consumer-facing download |
| `narrative_payload_v1_digest.payload_analysis_id` ≠ top-level `analysis_id` | **MEDIUM** | Two different UUIDs; may be intermediate vs final analysis ID; warrants investigation |
| Biomarker display labels with typo ("Photosphatase") and inconsistent capitalisation | **LOW** | Multiple instances; "Alkaline Photosphatase Alp (venous)" is the most visible |
| Non-HDL "elevated" status with in-range value (3.04 < 3.37) and score 89/100 | **LOW** | Status/score inconsistency; not currently surfaced prominently |
| `secondary_systems` in `narrative_report_v1` is empty string, not null or list | **LOW** | Structural type inconsistency |
| Lead narrative, secondary narratives, clinician synthesis all flat string blobs (no structured fields) | **LOW (now), HIGH (for Sprint 3)** | Cannot enforce Layer B → Layer C field-level preservation contract |
| Excessive "(venous)" labels on every marker | **POLISH** | Visual clutter; correct clinically but noisy for a consumer product |
| Display label capitalisation inconsistencies across the biomarker dial set | **POLISH** | Mix of "Crp", "Alt", "Hdl", "Apob" vs expected all-caps abbreviations |

---

## 14. What Is Working Well

1. **Lead finding coherence:** Homocysteine elevation → methylation pathway → vascular risk is biologically accurate, well-governed, and clearly communicated.

2. **Lifestyle personalisation is real:** The alcohol bridge is working, visible, and correctly framed. This directly satisfies one of the planning paper's core Sprint 2 requirements.

3. **Hypothesis-level WHY:** Four distinct mechanistic hypotheses with evidence, limiting factors, and confirmatory tests. This is significantly above what most consumer blood-test products deliver.

4. **Missing-data honesty:** Glucose, insulin, and AST are all flagged in appropriate places. MMA is surfaced as a confirmatory test recommendation. Homocysteine repeat in 8–12 weeks is noted.

5. **Confidence language:** "moderate_by_default" framing with explicit strengthening and weakening conditions is clinically responsible and trust-building.

6. **Deterministic reproducibility infrastructure:** The replay manifest contains 30+ versioned hashes for every analytical engine component. This is robust.

7. **Trust strip:** "9/9 expected markers, quality checks passed" is a clear positive signal.

8. **Layer B → C for lead finding:** For the homocysteine pathway, the JSON truth translates cleanly to user-readable language without overstatement.

9. **Clinician report data quality section:** Panel completeness and lab range quality per primary metric are present and useful for clinical review.

10. **Knowledge Bus package structure:** `pkg_homocysteine_elevation_context` is a properly populated signal library with real peer-reviewed research backing.

---

## 15. What Needs Fixing Before External User Testing

Listed by priority:

**P0 — Must fix (blocks external user testing):**

1. **Gate or remove `insights[]` placeholder surface.** The planning paper explicitly required this. Three generic placeholder entries with empty biomarker lists must not be surfaced to users. At minimum, gate behind a feature flag. If any frontend surface currently renders this array, it must be confirmed off for the launch-core path.

2. **Fix blood sugar domain: suppress "early impaired sugar and lipid handling" narrative when no active signals exist.** With `active_signal_ids: []` and `primary_idl_record_id: null`, the contributor sentence is unsupported. Replace with an honest fallback: e.g., "HbA1c is within range on this panel. Glucose and insulin were not on this panel — a fuller glycaemic read would require these." Do not present a pattern label without a signal.

3. **Fix ApoA1 signal logic or interpretation framing.** Either: (a) reclassify the signal so elevated ApoA1 is explicitly described as a context signal rather than a risk driver, or (b) remove it from the "What's driving this" consumer surface for this panel. A medically literate user or clinician will notice immediately that elevated ApoA1 is being presented as a negative cardiovascular finding.

**P1 — Should fix before UAT begins:**

4. **Fix low ALT liver scoring.** ALT below the reference range minimum should not score at the same severity as ALT dangerously above the maximum. Either apply a floor-severity cap for below-minimum values, or suppress the liver score contribution from below-minimum ALT. The liver domain at 5/100 for a low-normal enzyme value is a trust-destroying false alarm.

5. **Reconcile "Systemic Inflammation signal fired" with CRP 1.1 mg/L being within the broad lab range.** Either: (a) clarify in the WHY text that the signal uses an hs-CRP cardiovascular threshold (typically 1.0–3.0 mg/L intermediate zone) rather than the broad lab range, or (b) remove the "signal fired" assertion if CRP is classified "normal" in the biomarker panel. The contradiction between status "normal" and "signal fired" copy is avoidable.

6. **Remove `deferred_kb_content: "lipid_dominant_cv_why_it_matters_gap_deferred_sprint"` from consumer JSON.** Internal sprint management strings must not leak into the consumer payload download.

**P2 — Quality / polish issues (address before broader rollout):**

7. Fix biomarker display label typo: "Photosphatase" → "Phosphatase".
8. Standardise capitalisation: CRP, HDL, ApoB, ApoA1, LDL, HbA1c — all lowercase in current display labels.
9. Investigate and resolve: `narrative_payload_v1_digest.payload_analysis_id` ≠ top-level `analysis_id`.
10. Investigate eGFR 84 mL/min/1.73m² being "low" in JSON but silent in the consumer report — confirm this is correct suppression policy, not an accidental omission.
11. Fix "Non Hdl Cholesterol Calculation (venous)" label: remove "Calculation"; fix capitalisation.

---

## 16. Recommended Next Work Package

**Recommended action:** Fix before further testing

**Proposed Work ID:** LC-S11A  
**Type:** BEHAVIOUR (signal logic) + CONTENT (narrative copy correction)  
**Purpose:** Eliminate the four BLOCKER/HIGH trust risks before any external human testing begins: gate `insights[]`, fix blood sugar domain narrative-without-evidence, correct ApoA1 signal direction, and fix liver/ALT low-value scoring.

This is not a polish sprint. These four issues directly contradict the planning paper's requirement that the output be *"coherent, credible, and not contradictory between surfaces."* An external user reviewing this report would correctly conclude that elevated ApoA1 is being penalised, low ALT constitutes a near-emergency, and the blood sugar section is making claims unsupported by the biomarkers on the panel.

A separate, smaller work package (**LC-S11B: Layer C payload structure**) should follow to implement the Sprint 3 governed payload shape — replacing the flat string blobs with structured fields — so the Layer B → Layer C contract can be enforced at field level.

---

## 17. Final Recommendation

The engine is real, the lead finding is governed, and the lifestyle bridge is working. This is genuinely above where most consumer health-data products sit analytically.

Do not proceed to external human testing yet.

Before external testing, run LC-S11A to:

1. Gate `insights[]`
2. Suppress the blood sugar domain contributor sentence when no active signals are present
3. Reclassify or remove ApoA1 from the consumer cardiovascular risk surface
4. Cap low-ALT liver scoring to prevent a non-finding from driving an alarming domain score

These are mechanical, bounded fixes. None require Knowledge Bus expansion or major architectural change. They do require careful testing to avoid regression on the lead finding pathway.

After LC-S11A passes a targeted re-audit (can be scoped narrowly to the four issues), external human testing can proceed. The homocysteine/methylation/vascular pathway is solid enough to withstand external scrutiny once these four trust-destroying artefacts are removed.

---

*Audit completed 2026-05-17. No code was modified in the course of this audit. All findings are based on live UI inspection, downloaded analysis JSON (`healthiq-analysis-2026-05-17.json`), Knowledge Bus asset inspection, and planning paper review.*
