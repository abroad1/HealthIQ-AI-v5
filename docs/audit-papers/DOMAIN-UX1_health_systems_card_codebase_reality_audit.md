# DOMAIN-UX1 — Health Systems Card Codebase Reality Audit

**Auditor:** Claude Code  
**Date:** 2026-05-25  
**Status:** COMPLETE — report only, no code modified  
**Reference design:** `docs/discussion documents/healthiq_health_systems_card_discussion_FINAL.md` (v0.3)  
**Architecture reference:** `docs/architecture/User Health to Systems Map_FINAL.md` (v0.4)  
**Prior audits consulted:** `DOMAIN-R1_launch_core_health_domain_readiness_audit.md`, `POST_MAP_R1A_world_class_results_experience_audit_3c4d2b1c.md`

---

## 1. Executive Verdict

**The agreed Health Systems Card can be substantially implemented from current repo assets for all three Wave 1 domains. It cannot be fully implemented as designed without one light backend assembly addition.**

| Question | Verdict |
|---|---|
| Can Wave 1 Health Systems Card be implemented from current assets? | **YES — with one DTO addition** |
| Is first implementation frontend-only? | **PARTIAL — collapsed card is frontend-only; full expanded reveal requires one backend DTO addition** |
| Is light backend assembly required? | **YES — evidence completeness numerator/denominator; subsystem structure is a larger ask** |
| Is deeper governed/backend work required? | **NO for Wave 1. YES for Wave 2 (Blood/Iron, Thyroid, Kidney)** |
| Cardiovascular health ready? | **YES** |
| Blood sugar control ready? | **YES** |
| Liver health ready? | **YES** |

**Recommended next sprint:** A BEHAVIOUR-class sprint to surface Wave 1 cards in the main journey (`results/page.tsx` layout change) and add two missing DTO fields (`plain_english_descriptor` and `evidence_completeness_numerator`/`denominator`) to the backend assembler. Work_id: `DOMAIN-UX1A`. Risk: STANDARD.

**Blocking fact for full design compliance:** The agreed expanded reveal requires per-subsystem sections (Lipid transport, Vascular strain, Homocysteine pathway) each with their own marker cards and status indicator. No structured subsystem breakdown exists in the current DTO. This is the one gap that cannot be frontend-invented without violating the governance rule. It requires a backend assembly sprint before the full expanded reveal can be built.

**Quick win available now:** The existing `Wave1DomainCards` component at `frontend/app/components/results/Wave1DomainCards.tsx` is fully functional and already renders all core DTO fields. It is hidden behind `defaultOpen={false}` in a `ResultsDisclosureSection`. Moving it into the main journey is a layout-only change with no data risk.

---

## 2. Agreed UX Requirements Checked Against Codebase

| Agreed UX requirement | Exists today? | Source path / field / component | Frontend-ready? | Gap | Recommendation |
|---|---|---|---|---|---|
| Health system name (`consumer_label`) | YES | `ConsumerDomainScoreV1.consumer_label` / `Wave1DomainCards.tsx:76` | YES | None | Surface in collapsed card header |
| Plain-English system descriptor (e.g., "Heart, arteries and circulation") | NO | Not in DTO. Not in `ConsumerDomainScoreV1` type | NO | Field absent from DTO and frontend type | Add to backend assembler as `plain_english_descriptor: str` — static per domain_id |
| Large score visual / dial / gauge | PARTIAL | Numeric `scorePct` rendered at `Wave1DomainCards.tsx:86` as `text-3xl`. No dial or gauge component exists. | PARTIAL | No dial/gauge component in codebase | Frontend design work — add radial/gauge component using existing score value |
| Band label (Strong / Stable / Watch / Needs attention) | YES | `ConsumerDomainScoreV1.band_label` / `bandLabelDisplay()` at `Wave1DomainCards.tsx:16` | YES | Minor: current label for `watch` is "Worth watching"; design doc uses "Watch". For `review`, current is "Needs review"; design doc uses "Needs attention". | Align label strings — frontend-only change |
| Score reliability | PARTIAL | `ConsumerDomainScoreV1.confidence_tier` ("high"/"medium"/"low") / `tierLabel()` at `Wave1DomainCards.tsx:26` | PARTIAL | Label mismatch: current renders "High confidence / Medium confidence / Limited confidence". Design doc uses "Good reliability / Moderate reliability / Limited reliability". Concept is right; wording differs. | Remap tier strings to reliability vocabulary — frontend-only change |
| Evidence completeness ("8 of 11 relevant markers included") | NO | `missing_marker_ids` list exists but no numerator/denominator count is emitted | NO | Backend does not emit `evidence_completeness_numerator` or `evidence_completeness_denominator`. Frontend cannot calculate expected marker set. | Add two integer fields to DTO and assembler: `evidence_completeness_numerator` + `evidence_completeness_denominator` |
| Short health-system read (one sentence) | YES | `ConsumerDomainScoreV1.headline_sentence` / `Wave1DomainCards.tsx:91` | YES | None. Already rendered. | Already present — verify copy is prose-light |
| Supporting biological systems preview (chips) | PARTIAL | `contributing_system_keys: string[]` exists (e.g., `["cardiovascular"]`). `supporting_systems_summary?: string` on IDL record type (`analysis.ts:252`). Neither surfaces subsystem chips. | NO | No structured subsystem list (e.g., "Lipid transport", "Vascular strain", "Homocysteine pathway") in DTO. `contributing_system_keys` is system-level, not subsystem-level. | Requires backend assembly — new `subsystems` array in DTO (see §7) |
| Expand / reveal action | YES | `Wave1DomainCards.tsx:92` — "More detail" / "Show less" button | YES | UX label differs ("More detail" vs design doc's "See what shaped this score"). | Relabel button — frontend-only |
| Per-subsystem section in reveal (with own status) | NO | Not in DTO. No structured subsystem objects emitted. | NO | Largest gap. No subsystem score, subsystem label, or per-subsystem marker list in backend output. | Backend assembly sprint required before full expanded reveal |
| Biomarker evidence cards (uploaded, active, colourised) | PARTIAL | `BiomarkerDials.tsx` renders full cards with value/unit/range/status. Cannot be directly reused in domain reveal without subsystem grouping data. | PARTIAL | Reuse is architecturally sound; component exists. Missing subsystem→biomarker mapping to know which markers belong to which subsystem. | Defer full reuse until subsystem structure added to DTO |
| Missing relevant biomarkers (greyed-out cards) | PARTIAL | `missing_marker_ids: string[]` emitted and rendered as bulleted text list in `Wave1DomainCards.tsx:126–138` | PARTIAL | Text list exists. Greyed-out card rendering with "Not uploaded" state not yet built. Component work required. | Frontend component work once subsystem structure available |
| Missing-marker explanation sentence | NO | No dedicated DTO field. Content required: "Markers marked Not uploaded were not included in your blood panel." | NO | No DTO field. Standard text can safely be frontend-static copy (not interpretation). | Frontend-safe static copy — no DTO field needed |
| Reliability explanation sentence | YES | `ConsumerDomainScoreV1.confidence_sentence` / `Wave1DomainCards.tsx:115–117` | YES | Already rendered in expanded section. | Already present |
| What this may mean over time | YES | `ConsumerDomainScoreV1.consequence_sentence` / `Wave1DomainCards.tsx:119–121` | YES | Already rendered. | Already present |
| What to do next | YES | `ConsumerDomainScoreV1.next_step_sentence` / `Wave1DomainCards.tsx:123–125` | YES | Already rendered. | Already present |
| Evidence anchor / traceability line | YES | `ConsumerDomainScoreV1.evidence_anchor_sentence` / `Wave1DomainCards.tsx:78–82` | YES | Rendered in collapsed card. | Already present |
| Caveat flags (consumer-safe caveats) | YES | `ConsumerDomainScoreV1.caveat_flags` / `Wave1DomainCards.tsx:140–143` | YES | Rendered with amber background in expanded section. | Already present |

---

## 3. Existing Assets That Support the Design

### DTO Fields (backend → frontend contract)

| Asset | Provides | Location | Currently visible | Can support Health Systems Card |
|---|---|---|---|---|
| `ConsumerDomainScoreV1.domain_id` | Domain identifier (e.g., `wave1_cardiovascular`) | `frontend/app/types/analysis.ts:331`, `backend/core/models/results.py` | Hidden | YES |
| `ConsumerDomainScoreV1.consumer_label` | "Cardiovascular health" display name | `analysis.ts:332` | Hidden | YES |
| `ConsumerDomainScoreV1.clinical_label` | "Cardiometabolic / Vascular Risk Status" — NOT for retail | `analysis.ts:333` | Hidden (correctly not surfaced to consumer) | Do not surface in retail card |
| `ConsumerDomainScoreV1.score` | 0–1 normalised domain score | `analysis.ts:334` | Hidden | YES — multiply by 100 for display |
| `ConsumerDomainScoreV1.band_label` | "strong" / "stable" / "watch" / "review" | `analysis.ts:335` | Hidden | YES — needs label remapping |
| `ConsumerDomainScoreV1.confidence_tier` | "high" / "medium" / "low" | `analysis.ts:336` | Hidden | YES — reliability label remapping needed |
| `ConsumerDomainScoreV1.missing_marker_ids` | List of canonical IDs for relevant but missing markers | `analysis.ts:339` | Hidden | YES — currently bulleted text; can evolve to greyed-out cards |
| `ConsumerDomainScoreV1.headline_sentence` | One-sentence system read | `analysis.ts:344` | Hidden | YES |
| `ConsumerDomainScoreV1.contributor_sentence` | "Why this score" explanation | `analysis.ts:345` | Hidden | YES |
| `ConsumerDomainScoreV1.confidence_sentence` | Explains reliability quality | `analysis.ts:346` | Hidden | YES |
| `ConsumerDomainScoreV1.consequence_sentence` | "What this may mean over time" | `analysis.ts:347` | Hidden | YES |
| `ConsumerDomainScoreV1.next_step_sentence` | Contextual next-step guidance | `analysis.ts:348` | Hidden | YES |
| `ConsumerDomainScoreV1.evidence_anchor_sentence` | "Based on: [IDL label]" traceability | `analysis.ts:349–350` | Hidden | YES |
| `ConsumerDomainScoreV1.caveat_flags` | Domain-specific consumer caveats | `analysis.ts:341` | Hidden | YES |
| `ConsumerDomainScoreV1.contributing_system_keys` | System-level keys (e.g., `["cardiovascular"]`) | `analysis.ts:342` | Hidden | LIMITED — system-level only, not subsystem |
| `ConsumerDomainScoreV1.active_signal_ids` | Signal IDs contributing to score | `analysis.ts:337` | Hidden | INDIRECT — backend-facing; not direct retail display |
| `ConsumerDomainScoreV1.primary_idl_record_id` | IDL phenotype record ID for cross-reference | `analysis.ts:338` | Hidden | INDIRECT |
| `AnalysisResult.consumer_domain_scores` | Array of all Wave 1 domain cards | `analysis.ts:379` | Hidden (behind disclosure) | YES |
| `InterpretationDisplayLayerBundleV1.supporting_systems_summary` | Optional string summary of supporting systems | `analysis.ts:252` | Hidden | PARTIAL — free-text string, not structured chips |

### Backend Assembler Outputs

| Asset | Provides | Location | Currently visible |
|---|---|---|---|
| `assemble_consumer_domain_scores_v1()` | Produces all three Wave 1 domain card objects | `backend/core/analytics/domain_score_assembler.py:364` | YES (runs in pipeline) |
| `cv_block()` | Cardiovascular domain card assembly | `domain_score_assembler.py:400–451` | YES |
| `met_block()` | Blood sugar domain card assembly | `domain_score_assembler.py:453–503` | YES |
| `liv_block()` | Liver health domain card assembly | `domain_score_assembler.py:505–581` | YES |
| `_cardiovascular_confidence_tier()` | Confidence tier for CV domain | `domain_score_assembler.py:243–270` | YES (in output) |
| `_metabolic_blood_sugar_confidence_tier()` | Confidence tier for blood sugar | `domain_score_assembler.py:273–290` | YES (in output) |
| `_liver_confidence_tier_domain()` | Confidence tier for liver | `domain_score_assembler.py:293–307` | YES (in output) |
| `_missing_for_rail()` | Missing marker IDs per scoring rail | `domain_score_assembler.py` | YES (in output) |
| Narrative factory functions | All sentence fields | `backend/core/analytics/domain_narrative_wave1.py` | YES (in output) |

### Confidence / Reliability Logic

| Asset | Provides | Location |
|---|---|---|
| `_cardiovascular_confidence_tier()` | High if full lipid panel + derived ratios; medium if core lipids; low otherwise | `domain_score_assembler.py:243–270` |
| `_metabolic_blood_sugar_confidence_tier()` | High if glucose + HbA1c + insulin/TG; medium if glucose + HbA1c; low otherwise | `domain_score_assembler.py:273–290` |
| `_liver_confidence_tier_domain()` | High if 4+ hepatic markers including ALT+AST+GGT; medium if ALT+AST; low otherwise. Requires ALT present. | `domain_score_assembler.py:293–307` |
| `_merge_tier_rail_and_domain()` | Takes minimum of rail-level and domain-level confidence (most conservative) | `domain_score_assembler.py` |

### Missing Marker Logic

| Asset | Provides | Location |
|---|---|---|
| `_CV_RAIL_BIOMARKERS` | Expected CV marker set (total_cholesterol, ldl, hdl, tg, tc_hdl_ratio, apob, apoa1, lipoprotein_a, homocysteine) | `domain_score_assembler.py:55–65` |
| `_MET_RAIL_BIOMARKERS` | Expected metabolic marker set | `domain_score_assembler.py` |
| `_LIV_RAIL_BIOMARKERS` | Expected liver marker set | `domain_score_assembler.py` |
| `_missing_for_rail()` | Computes missing IDs as set difference between rail and panel | `domain_score_assembler.py` |
| `wave1ConfidenceMarkerDisplayLabel()` | Converts canonical ID to user-friendly label | `frontend/app/lib/wave1ConfidenceMarkerLabels.ts` |

### Frontend Components

| Asset | Provides | Location | Currently visible |
|---|---|---|---|
| `Wave1DomainCards.tsx` | Complete domain card component (collapsed + expand toggle + all sentence fields + missing markers + caveats) | `frontend/app/components/results/Wave1DomainCards.tsx` | Hidden — `defaultOpen={false}` |
| `BiomarkerDials.tsx` | Full per-marker card with value/unit/range/status/educational explainer | `frontend/app/components/biomarkers/BiomarkerDials.tsx` | YES (section 7 of results) |
| `BiomarkerDialEntry` interface | Typed entry for a single biomarker card | `BiomarkerDials.tsx:15–35` | N/A |
| `ResultsDisclosureSection.tsx` | Accordion disclosure wrapper used to wrap domain cards | `frontend/app/components/results/ResultsDisclosureSection.tsx` | N/A |

### IDL / Knowledge Bus Assets

| Asset | Provides | Location |
|---|---|---|
| `idl_records_v1.yaml` | Phenotype records for Wave 1 patterns (ph_vascular_hcy_inflammation_v1, ph_lipid_residual_ldl_favourable_transport_v1, ph_hba1c_metabolic_stress_v1, ph_metabolic_early_ir_v1, ph_hepatic_alt_inflammatory_v1) | `knowledge_bus/interpretation_display_layer_v1/idl_records_v1.yaml` |
| `InterpretationDisplayLayerBundleV1` | Bundle of IDL records attached to analysis result | `frontend/app/types/analysis.ts:374–375`, `backend/core/contracts/interpretation_display_layer_v1.py` |
| `supporting_systems_summary` | Optional free-text string on IDL record (e.g., could contain "Lipid transport, Vascular strain") | `analysis.ts:252` |

---

## 4. Current Wave 1 Domain Card Reality

### Cardiovascular Health

| Attribute | Status |
|---|---|
| Domain ID | `wave1_cardiovascular` |
| DTO source | `ConsumerDomainScoreV1` assembled by `cv_block()` in `domain_score_assembler.py:400–451` |
| Frontend component | `Wave1DomainCards.tsx` |
| Fields rendered | `consumer_label`, `score` (as percentage), `band_label`, `confidence_tier`, `headline_sentence`, `evidence_anchor_sentence`, `contributor_sentence`, `confidence_sentence`, `consequence_sentence`, `next_step_sentence`, `missing_marker_ids` (bulleted), `caveat_flags` |
| Fields available but not rendered | `clinical_label` (correct — retail should not show), `contributing_system_keys`, `active_signal_ids`, `primary_idl_record_id`, `source_track`, `raw_evidence_refs`, `card_schema_version` |
| Fields not available | `plain_english_descriptor`, `evidence_completeness_numerator`, `evidence_completeness_denominator`, structured subsystem breakdown |
| Copy quality | Good. Headline sentence is best consumer-facing sentence in entire DTO (noted in POST_MAP_R1A audit). Minor prose issue: potential "on this panel" language in contributor_sentence. |
| Safe to surface? | YES — no data safety issues. Currently invisible to 100% of users. |
| Changes needed for design alignment | Add `plain_english_descriptor`; add evidence completeness fields; add score dial visual; relabel confidence_tier to reliability vocabulary; subsystem chips require backend work |

### Blood Sugar Control

| Attribute | Status |
|---|---|
| Domain ID | `wave1_blood_sugar` |
| DTO source | `ConsumerDomainScoreV1` assembled by `met_block()` in `domain_score_assembler.py:453–503` |
| Frontend component | `Wave1DomainCards.tsx` |
| Fields rendered | Same as CV above |
| Fields available but not rendered | Same as CV above |
| Fields not available | Same as CV above |
| Copy quality | Good. Fallback copy (`_MET_NO_ACTIVE_SIGNAL_CONTRIBUTOR`) correctly handles low-evidence cases. Caveat flags may fire if only HbA1c present. |
| Safe to surface? | YES |
| Changes needed | Same as CV above |

### Liver Health

| Attribute | Status |
|---|---|
| Domain ID | `wave1_liver` |
| DTO source | `ConsumerDomainScoreV1` assembled by `liv_block()` in `domain_score_assembler.py:505–581` |
| Frontend component | `Wave1DomainCards.tsx` |
| Fields rendered | Same as CV above. Caveat flags present and rendered in amber block. |
| Fields available but not rendered | Same as CV above |
| Fields not available | Same as CV above. Note: liver uses a blended score (min of liver rail score and hepatic capacity score) which is opaque to frontend — correctly so. |
| Copy quality | Good. Caveat flags are user-friendly and explain limited panel scope. |
| Safe to surface? | YES |
| Changes needed | Same as CV above. Verify `scoring_policy.yaml` key is `liver`, not `hepatic` (documented in assembler header — `domain_score_assembler.py:8–9`). |

---

## 5. Evidence Completeness Reality

| Question | Answer |
|---|---|
| Does the backend emit expected marker counts? | NO. `_CV_RAIL_BIOMARKERS` (and equivalent for met/liver) are defined as Python tuples in `domain_score_assembler.py:55–65`, but their length is not emitted in the DTO. |
| Does the backend emit included marker counts? | NO — not explicitly. Active marker count is derivable from `active_signal_ids.length` but this is not the same as "included from rail." |
| Does the backend emit missing relevant markers? | YES — `missing_marker_ids: string[]` is in the DTO and emitted correctly. |
| Are missing markers domain-level only or subsystem-grouped? | Domain-level only. No subsystem grouping. |
| Can evidence completeness be displayed now without frontend calculation? | NO. The numerator (included rail markers) and denominator (total expected rail markers) are not in the DTO. Frontend cannot safely derive these. |
| What exact backend assembly is needed? | Add two integer fields to `ConsumerDomainScoreV1`: `evidence_completeness_numerator: int` (how many rail markers were in the panel) and `evidence_completeness_denominator: int` (total markers in the domain's scoring rail). These are derivable from `_missing_for_rail()` logic already in `domain_score_assembler.py`. |

**Governance rule applies:** Frontend must not calculate expected marker sets or define what counts as a "relevant" marker. The evidence completeness display requires the backend to supply both integers.

**Effort:** Low. The rail biomarker constants already exist. Adding numerator/denominator to the DTO and assembler is a 1–2 hour backend task with STANDARD risk (DTO extension, not scoring logic change).

---

## 6. Score Reliability Reality

| Question | Answer |
|---|---|
| What field maps most closely to score reliability? | `ConsumerDomainScoreV1.confidence_tier: 'high' \| 'medium' \| 'low'` |
| Is `confidence_tier` sufficient? | YES for the concept. The label vocabulary needs updating. |
| Does it account for marker coverage, signal consistency, key missing markers? | YES — the three domain-specific confidence functions (`_cardiovascular_confidence_tier()`, `_metabolic_blood_sugar_confidence_tier()`, `_liver_confidence_tier_domain()`) evaluate marker coverage depth and require key markers (e.g., ALT must be present for liver). The merge rule takes the most conservative tier. |
| Does it account for contradictions between markers? | PARTIALLY — the underlying cluster_engine and confidence merge handle contradiction signals, but this is not explicitly surfaced as a separate concept. |
| Is the wording consumer-safe? | PARTIAL — current rendering "High confidence / Medium confidence / Limited confidence" is technically accurate but not aligned with the design doc's "Good reliability / Moderate reliability / Limited reliability" vocabulary. |
| Does it need backend refinement before surfacing? | NO — the concept is sound. Only frontend label remapping needed for vocabulary alignment. |
| Is `confidence_sentence` (explanatory text) consumer-safe? | YES — it explains WHY reliability is high/medium/low in plain English. Already rendered in expanded section. |

**Recommendation:** Remap `tierLabel()` in `Wave1DomainCards.tsx:26–30` to use "Good reliability" / "Moderate reliability" / "Limited reliability" vocabulary before surfacing. No backend change needed.

---

## 7. Supporting Biological Systems / Subsystem Reality

The agreed UX requires supporting biological systems as visual chips in the collapsed card and per-subsystem sections in the expanded reveal.

| Domain | Proposed supporting system | Existing source? | Markers available? | Missing markers available? | Score/status available? | Ready now? | Gap |
|---|---|---|---|---|---|---|---|
| Cardiovascular | Lipid transport | `contributing_system_keys` contains `"cardiovascular"` — system level only. `supporting_systems_summary` on IDL record is a free-text string, not structured. | YES (CV rail markers exist) | YES (missing_marker_ids) | NO — no subsystem-level score | NO | No structured subsystem object in DTO |
| Cardiovascular | Vascular strain | Not a separate DTO field. Inferrable from signal IDs but not structured. | PARTIAL (homocysteine, CRP if uploaded) | YES via missing_marker_ids | NO | NO | Same — no subsystem structure |
| Cardiovascular | Homocysteine pathway | IDL record `ph_vascular_hcy_inflammation_v1` maps to this concept. Not a separate subsystem object. | PARTIAL | YES | NO | NO | Same |
| Blood sugar | Glycaemic regulation | IDL records `ph_hba1c_metabolic_stress_v1`, `ph_metabolic_early_ir_v1`. No subsystem structure. | YES (metabolic rail markers) | YES | NO | NO | Same |
| Blood sugar | Lipid coupling / insulin action | Covered by TYG index logic in assembler. Not a structured subsystem. | PARTIAL | YES | NO | NO | Same |
| Liver | Liver strain / processing load | IDL record `ph_hepatic_alt_inflammatory_v1`. No subsystem structure. | YES (liver rail markers) | YES | NO | NO | Same |

**Key finding:** The proposed subsystem breakdown (Lipid transport, Vascular strain, Homocysteine pathway, etc.) does not exist as governed structured output anywhere in the codebase. The closest asset is `contributing_system_keys` (system-level, not subsystem-level) and `supporting_systems_summary` (free-text string on IDL record, not a structured array).

**What would be unsafe to invent in the frontend:** The frontend must not invent subsystem labels, decide which markers belong to which subsystem, assign subsystem scores or statuses, or determine which missing markers belong to which subsystem. All of these are interpretation decisions.

**What backend assembly is required:** A new `subsystems` array on `ConsumerDomainScoreV1`, where each element contains: `subsystem_id`, `subsystem_label`, `included_marker_ids`, `missing_marker_ids`, and optionally a `status_label`. This is a backend assembly task of STANDARD-to-HIGH risk (it modifies the DTO contract and requires governed subsystem definitions).

---

## 8. Biomarker Card Reuse Reality

| Question | Answer |
|---|---|
| Is there a canonical biomarker card component? | YES — `BiomarkerDials.tsx` with `BiomarkerDialEntry` interface. Renders value, unit, reference range, status, educational explainer, contribution context. |
| Can it be reused in compact form inside the Health Systems Card reveal? | ARCHITECTURALLY YES. The component accepts typed `BiomarkerDialEntry` objects. The same visual treatment is achievable. Subsystem grouping is the blocker, not component capability. |
| Can it show value, unit, reference range, score/status? | YES — all fields present in `BiomarkerDialEntry` interface (`BiomarkerDials.tsx:15–35`). |
| Can it show a missing / greyed-out state? | NO — there is no `missing` or `not_uploaded` state in the current `BiomarkerDialEntry` interface. A greyed-out card for missing markers would need either (a) a new prop on the component, or (b) a wrapper component that renders a styled placeholder using the canonical biomarker name. |
| Can it show a mini dial / range indicator? | YES — `referenceRange` is in the interface. The existing visual treatment includes the range bar. |
| What component work is required? | (1) Add a `missing?: boolean` prop to `BiomarkerDialEntry` or create a `MissingBiomarkerCard` wrapper. (2) Once subsystem structure is available from backend, map subsystem marker IDs to biomarker card data. (3) Create a compact/mini variant for use inside the domain card reveal if the full card is too large. |

---

## 9. What Can Be Implemented Immediately

### Frontend-only safe now

- **Surface Wave 1 domain cards in main journey**: Change `defaultOpen={false}` to `defaultOpen={true}` or reposition `Wave1DomainCards` earlier in `frontend/app/(app)/results/page.tsx` (lines 807–814). Zero data risk. Domain cards are already fully assembled by the backend.
- **Fix band label vocabulary**: Remap `review` → "Needs attention" in `bandLabelDisplay()` at `Wave1DomainCards.tsx:16`. Minor string change.
- **Fix reliability label vocabulary**: Remap confidence_tier to "Good reliability / Moderate reliability / Limited reliability" in `tierLabel()` at `Wave1DomainCards.tsx:26`. Minor string change.
- **Update expand button label**: Change "More detail" → "See what shaped this score" per design doc §3 item 9.
- **Add plain-English system descriptor (static)**: Map `domain_id` → descriptor string in frontend (e.g., `wave1_cardiovascular` → "Heart, arteries and circulation"). This is display copy, not interpretation. The three Wave 1 domain IDs are fixed. Can be implemented as a `DOMAIN_DESCRIPTOR` constant map in `Wave1DomainCards.tsx`. This is safe without a DTO field since there are only three fixed IDs and the mapping is purely presentational.
- **Add missing-marker explanation sentence**: Static string "Markers marked Not uploaded were not included in your blood panel, so they did not contribute to this score." — not interpretation; can be frontend-static copy.

### Frontend plus light backend assembly

- **Evidence completeness display** ("8 of 11 relevant markers included"): Requires adding `evidence_completeness_numerator: int` and `evidence_completeness_denominator: int` to `ConsumerDomainScoreV1` in `backend/core/models/results.py` and populating in `cv_block()`, `met_block()`, `liv_block()` in `domain_score_assembler.py`. Risk: STANDARD. Derivable from existing rail constants.
- **Score dial / gauge visual**: Frontend design component work. Requires no backend change. Should use existing `score` (0–1) value. Risk: LOW frontend component work.
- **Missing biomarker greyed-out card state**: Add `missing?: boolean` prop to `BiomarkerDialEntry` or create a thin wrapper component. No backend change. The missing marker IDs are already provided.

### Not safe without governed/backend work

- **Supporting biological systems chips in collapsed card**: Requires structured `subsystems[]` array in DTO. Cannot use frontend-hardcoded subsystem labels for non-static data — the set of contributing subsystems may vary by panel and phenotype.
- **Per-subsystem sections in expanded reveal**: Requires same `subsystems[]` array. Cannot safely group markers by subsystem in frontend without governed mapping.
- **Per-subsystem scores or status labels**: No subsystem-level scores exist anywhere in backend output. Would require new scoring rail design — HIGH risk.
- **Full biomarker card reuse inside reveal grouped by subsystem**: Requires subsystem structure from backend before safe frontend wiring.

---

## 10. Required Backend/DTO Additions

| Missing field / structure | Needed for | Likely source data | Likely file(s) | Risk | Notes |
|---|---|---|---|---|---|
| `evidence_completeness_numerator: int` | Evidence completeness display ("8 of 11 markers included") | Rail biomarker constants vs panel intersection | `backend/core/models/results.py` (Pydantic model), `backend/core/analytics/domain_score_assembler.py` (`cv_block`, `met_block`, `liv_block`) | STANDARD | Derivable from `_missing_for_rail()` and rail constant length. `denominator = len(_CV_RAIL_BIOMARKERS)`, `numerator = denominator - len(missing)` |
| `evidence_completeness_denominator: int` | Same | Same | Same | STANDARD | Same sprint as numerator |
| `plain_english_descriptor: str` | System descriptor ("Heart, arteries and circulation") | Static per domain_id — three fixed values | `backend/core/models/results.py`, `domain_score_assembler.py` | LOW | Could also be handled as frontend static map given only 3 fixed IDs. Backend field preferred for consistency. |
| `subsystems: List[SubsystemCardV1]` | Per-subsystem sections in expanded reveal | Governed subsystem-to-marker mapping (new) | New Pydantic model + assembly logic | HIGH | Largest new structure. Requires: (1) governed subsystem definitions per domain, (2) marker→subsystem mapping, (3) per-subsystem missing marker derivation. Do not implement without a full governance sprint. |
| `SubsystemCardV1.subsystem_id` | Subsystem identity | Governed definition | New model | HIGH | See above |
| `SubsystemCardV1.subsystem_label` | Consumer display label (e.g., "Lipid transport") | Governed definition | New model | HIGH | Cannot be frontend-invented |
| `SubsystemCardV1.included_marker_ids` | Which uploaded markers belong to this subsystem | Governed mapping | New assembly logic | HIGH | |
| `SubsystemCardV1.missing_marker_ids` | Which relevant markers are missing per subsystem | Governed mapping | New assembly logic | HIGH | |
| `SubsystemCardV1.status_label` | Optional mini status (Strong / Stable / Watch) | Scoring rail subset or heuristic | New scoring logic or rule | HIGH | May require separate scoring rail per subsystem |

---

## 11. Recommended Implementation Path

### Sprint 1 — DOMAIN-UX1A: Wave 1 Surface + Light DTO Hardening

**Proposed work_id:** `DOMAIN-UX1A`  
**Risk level:** STANDARD  
**Change type:** MIXED (frontend surface change + DTO extension)  
**Likely files:**
- `frontend/app/(app)/results/page.tsx` — reposition Wave1DomainCards into main journey
- `frontend/app/components/results/Wave1DomainCards.tsx` — label remapping, static descriptor map, button copy
- `backend/core/models/results.py` — add `evidence_completeness_numerator`, `evidence_completeness_denominator`, `plain_english_descriptor`
- `backend/core/analytics/domain_score_assembler.py` — populate new fields in `cv_block()`, `met_block()`, `liv_block()`
- `frontend/app/types/analysis.ts` — add new DTO fields to `ConsumerDomainScoreV1` interface

**Acceptance criteria:**
- Wave 1 domain cards are visible on page load without user action
- Collapsed card shows: name, plain-English descriptor, score, band, reliability label, evidence completeness ("X of Y markers"), health-system read, evidence anchor
- Expanded card shows: contributor sentence, confidence sentence, consequence sentence, next step sentence, missing marker text list, caveat flags
- Band label vocabulary matches design doc: Strong / Stable / Worth watching / Needs attention
- Reliability vocabulary matches: Good reliability / Moderate reliability / Limited reliability
- Evidence completeness numerator/denominator are backend-emitted integers, not frontend-calculated
- `clinical_label` is not displayed on the consumer-facing card

**What must not be included:**
- Subsystem chips or per-subsystem sections (backend structure not ready)
- Greyed-out biomarker cards (defer to Sprint 2)
- Score dial/gauge visual (defer to Sprint 2 or separate design sprint)
- Wave 2 domains (not ready)

---

### Sprint 2 — DOMAIN-UX1B: Visual Polish and Missing-Marker Card State

**After Sprint 1 is in production and UAT complete.**

- Score dial / gauge component for headline score visual
- Greyed-out missing biomarker card component (`MissingBiomarkerCard` or `missing` prop on `BiomarkerDialEntry`)
- Missing-marker explanation sentence in expanded reveal
- Compact biomarker card layout for reuse inside domain reveal

**Risk:** LOW (frontend component work, no DTO changes)

---

### Sprint 3 — DOMAIN-UX1C: Subsystem Structure (Backend Assembly)

**Requires full governance sprint — HIGH risk.**

- Design governed subsystem definitions per domain
- Add `SubsystemCardV1` model and `subsystems: List[SubsystemCardV1]` to `ConsumerDomainScoreV1`
- Add governed marker→subsystem mapping to assembler
- Add missing-marker derivation per subsystem
- Frontend: wire per-subsystem sections in expanded reveal using new DTO data

**Not safe to proceed without GPT architectural review and dual approval.**

---

## 12. STOP Conditions for Implementation

The following conditions must trigger a STOP before or during implementation:

| STOP condition | Rationale |
|---|---|
| Frontend calculates domain score | Score must come from backend. `ConsumerDomainScoreV1.score` exists — use it. |
| Frontend determines expected markers for a domain | Expected marker sets are governed by scoring rails in `backend/ssot/scoring_policy.yaml`. Frontend cannot define these. |
| Frontend determines missing relevant markers | `missing_marker_ids` must come from backend. If it is empty or absent, do not derive it in frontend. |
| Frontend invents subsystem labels | Subsystem names are clinical/semantic claims. They must be governed backend output. Hardcoding "Lipid transport" as a subsystem chip without a backend `subsystem_label` field is not permitted. |
| Frontend assigns biomarkers to subsystems without DTO mapping | Without a governed `subsystems[]` structure in the DTO, frontend cannot decide which biomarker belongs to which subsystem section. |
| `clinical_label` appears in consumer-facing card | `clinical_label` (e.g., "Cardiometabolic / Vascular Risk Status") must never appear in the retail view. Use `consumer_label` only. |
| Evidence completeness numerator/denominator is frontend-calculated | Frontend must not count panel markers or subtract missing markers to derive the completeness fraction. |
| Subsystem scores are invented | No subsystem-level scores exist in the backend. Do not render a subsystem score/dial without a governed `SubsystemCardV1.score` field. |
| Fake precision is introduced | If evidence completeness fields are absent from the DTO, do not show "8 of 11 markers" by guessing. Show nothing or show confidence_tier only. |
| Biomarker cards show interpretation not in DTO | All text in biomarker cards must come from DTO fields (`interpretation`, `educationalExplainer`, `contributionContext`). No frontend-generated copy. |

---

## 13. Final Recommendation

**Implement Sprint 1 (DOMAIN-UX1A) now. The Wave 1 infrastructure is complete and hiding it is costing the product.**

The three Wave 1 domain cards contain the best consumer-facing intelligence HealthIQ emits. The `headline_sentence` for cardiovascular is more useful and differentiated than most of the content currently visible on the results page. It is invisible to every user because of a single `defaultOpen={false}` flag.

Sprint 1 is low-risk, high-leverage, and does not require new analytical logic. The DTO extension (evidence completeness numerator/denominator) is a straightforward addition to existing assembler code. The frontend changes are label remapping and layout repositioning.

Do not wait for the subsystem structure before surfacing the cards. The agreed design in §13 of the discussion document explicitly scopes v1 to Wave 1 domains without requiring the full expanded subsystem reveal. The collapsed card plus prose-based expanded detail is a complete, governed, consumer-safe implementation of the core concept.

The subsystem reveal is the right second step but it requires a proper backend governance sprint. Do not attempt to approximate it with frontend-invented labels or hardcoded marker groupings.

**Fastest safe path:**
1. Sprint DOMAIN-UX1A: surface Wave 1 cards with evidence completeness fields → 1 sprint, STANDARD risk
2. Sprint DOMAIN-UX1B: add score dial and missing-marker card state → 1 sprint, LOW risk
3. Sprint DOMAIN-UX1C: governed subsystem structure → 1 sprint, HIGH risk, requires GPT review + dual approval
4. Once subsystem structure exists, the full expanded reveal per the discussion document is safe to implement

**Wave 2 (Blood/Iron/Oxygen, Thyroid, Kidney):** Not ready. Thyroid and Kidney require `scoring_policy.yaml` changes (HIGH risk). Blood/Iron requires new assembler block and IDL authoring. Do not include in Sprint 1 scope.
