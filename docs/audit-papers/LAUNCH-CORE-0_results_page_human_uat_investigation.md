# LAUNCH-CORE-0 — Results Page Human UAT Investigation

**Analysis:** `18e14232-9f93-45e6-820c-004ab5a16235`  
**URL:** `http://localhost:3000/results?analysis_id=18e14232-9f93-45e6-820c-004ab5a16235`  
**Account:** `test-user3@example.com`  
**Repo:** `main` @ `8be6959` (post ARCH-RT programme)  
**Date:** 2026-05-30  
**Mode:** Investigation only — no production code, compiled artefact, or logic changes made.

---

## 1. Executive summary

The results page is **materially improved** after ARCH-RT (compiled card evidence, governed subsystem rows, IDL pattern guards). For this analysis, **subsystem marker presence is backend-correct**: every “Missing / Not uploaded” chip corresponds to a marker genuinely absent from the scored `biomarkers[]` payload. The prior **`total_bilirubin` false-missing defect is resolved** on this analysis via compiled artefact canonicalisation (`bilirubin` only).

Remaining human UAT defects fall into three buckets:

| # | Theme | Verdict | Primary layer |
|---|--------|---------|---------------|
| A | Internal / generated names in consumer prose | **Confirmed** | Backend narrative assembly + incomplete frontend scrub |
| B | Health Systems Card marker presence wrong | **Not reproduced on this analysis** | True missings only; perceived error likely from score/coverage dissonance |
| C | Interpretation / display defects | **Confirmed** | Mixed: backend scoring semantics + frontend role-chip rendering |

**Overall UAT posture:** PASS WITH RESERVATIONS — safe to ship structurally, but consumer prose and marker-role chips still leak engineering vocabulary.

---

## 2. Investigation method

1. Browser login via API token injection + full page load of target URL.
2. Screenshots of hero, health-system cards (all three expanded), and full-page scroll capture.
3. Accessibility snapshot + DOM text scan for forbidden internal tokens (`ph_`, `signal_`, `pkg_`, `score_contributor`, etc.).
4. Authenticated API fetch: `GET /api/analysis/result?analysis_id=18e14232-9f93-45e6-820c-004ab5a16235` → saved to `automation_bus/_launch_core0_18e14232.json` (~951 KB).
5. Code trace of DTO assembly (`health_system_card_evidence.py`, `wave1_subsystem_evidence.py`, `domain_score_assembler.py`) and frontend renderers (`Wave1DomainCards.tsx`, `Wave1SubsystemEvidenceSection.tsx`, `DeterministicNarrativeSurface.tsx`, `ResultsHeroBlocks.tsx`, `InterpretationPatternsSection.tsx`, `PrimaryFindingAndWhy.tsx`).
6. Cross-check against prior Wave 1 equivalence audit (`WAVE1_subsystem_marker_equivalence_investigation.md`, analysis `bb695d3c`).

---

## 3. Screenshots

| File | Description |
|------|-------------|
| `docs/audit-papers/assets/launch-core0-hero-patterns.png` | Page header + journey intro |
| `docs/audit-papers/assets/launch-core0-health-systems-expanded.png` | Cardiovascular card expanded (86/100, 5/5 markers) |
| `docs/audit-papers/assets/launch-core0-results-full.png` | Lower journey (blood sugar + liver cards visible) |

**Browser-visible highlights (expanded cards):**

- Cardiovascular: included markers show chips like **“LDL cholesterol score contributor”**, **“TC/HDL ratio confidence contributor”**.
- Blood sugar: **100/100** gauge with **“Limited reliability”** and **“1 of 3 expected markers included”**; Glycaemic control shows **HbA1c** included, **Glucose Not uploaded**; Insulin subsystem shows **Insulin Not uploaded**, Triglycerides included.
- Liver: **73/100**, **“Limited marker coverage”**, enzyme pattern shows **AST Not uploaded** (ALT + GGT included); processing context shows ALP, Albumin, Bilirubin all included.

---

## 4. Console and network

### Console

- **No JavaScript errors or warnings** observed after page load and card expansion.
- Post-hoc console hook returned empty `errors` / `warnings` arrays.

### Network

| Request | Status | Notes |
|---------|--------|-------|
| `GET /api/auth/me` | 200 | Session established |
| `GET /api/analysis/result?analysis_id=18e14232-…` | 200 | ~256 ms; sole results payload |
| `POST /api/wedge-events` | 200 | Analytics beacon |

Frontend data path: `useAnalysisResult` → `AnalysisService` → renders `consumer_domain_scores`, `narrative_report_v1`, `interpretation_display_layer_v1`, `clinician_report_v1` from single result DTO. **No local subsystem re-computation on the frontend.**

---

## 5. DTO fields rendered on the results page

### Health Systems Cards (`consumer_domain_scores[]`)

| Field | Backend source | Frontend component | User-visible? |
|-------|----------------|-------------------|---------------|
| `consumer_label` | `domain_score_assembler` | `Wave1DomainCards` → `CardTitle` | Yes |
| `plain_english_descriptor` | `_WAVE1_PLAIN_DESCRIPTOR` map | Card subtitle | Yes |
| `evidence_anchor_sentence` | Domain assembler + IDL linkage | Card border-left note | Yes (“Based mainly on: Vascular Inflammation Risk”) |
| `score`, `band_label` | Rail scoring | `Wave1HealthSystemScoreVisual` | Yes |
| `confidence_tier` | Merged rail + domain tiers | `wave1ScoreReliabilityLabel()` | Yes (“Limited reliability”) |
| `evidence_completeness_numerator/denominator` | `_evidence_completeness_for_rail()` | `wave1EvidenceCompletenessLine()` | Yes |
| `headline_sentence`, `contributor_sentence`, etc. | Domain assembler copy | Expanded card prose | Yes |
| `subsystems[]` | `assemble_wave1_subsystem_evidence()` | `Wave1SubsystemEvidenceSection` | Yes (expanded) |

### Subsystem row (`subsystems[]` / `SubsystemEvidenceV1`)

| Field | Backend source | Frontend usage | User-visible? |
|-------|----------------|----------------|---------------|
| `subsystem_label` | Compiled YAML `subsystem_label` or legacy def | `<h4>` | Yes |
| `mechanism_line` | Compiled YAML | Paragraph | Yes |
| `included_marker_ids` | `_partition_markers()` exact ID match | Filter key for chips | No (IDs hidden when `marker_evidence` present) |
| `missing_marker_ids` | `_partition_markers()` | Drives missing list | No |
| `included_markers[]` / `missing_markers[]` | `_labels_for_marker_ids()` SSOT display names | Fallback chip labels | Yes (when no `marker_evidence`) |
| `marker_evidence[]` | Compiled YAML per-marker defs | Primary chip source | Yes — **`display_label` + `marker_role` chip** |
| `source_trace` | `health_system_card_evidence_v1:{artefact_id}:{compile_manifest_ref}` | Shown only if `isConsumerSafeSourceTrace()` | **No** (underscore/path filtered out) |
| `compile_manifest_ref` | Compiled YAML | Not rendered | **No** |
| `source_spec_ids` | Compiled YAML | Not rendered | **No** |
| `card_evidence_schema_version`, `visibility_tier` | Compiled YAML | Not rendered | **No** |

### Narrative / hero / patterns

| Field | Frontend component | Sanitised? |
|-------|-------------------|------------|
| `narrative_report_v1.retail_summary` | `NarrativeRetailSummaryCard` | Partial (`scrubConsumerRetailNarrative`) |
| `narrative_report_v1.body_overview` | `ResultsBodyOverview` | Partial |
| `clinician_report_v1.sections.page1.primary_concern` | `ResultsPrimaryHero` via `resolveHeroPrimaryStory()` | Partial |
| `interpretation_display_layer_v1.records[].retail_display_label` | Hero fallback / IDL cards | Guarded by `selectSafeIdlPatternRecords()` |
| `interpretation_display_layer_v1.records[].severity_state` | Severity badge | Frontend splits on `_` → “Strong Signal” |

---

## 6. Issue A — Internal / generated names surfacing to users

### A1. Lead pattern uses package signal library name (HIGH visibility)

**Observed in browser hero:**

> **Homocysteine Elevation Context: warrants attention on this panel**

**API source:** `clinician_report_v1.sections.page1.primary_concern` and echoed in `narrative_report_v1.retail_summary` / `body_overview` as “homocysteine elevation context”.

**Origin:** `knowledge_bus/packages/pkg_homocysteine_elevation_context/signal_library.yaml` — signal display name **“Homocysteine Elevation Context”** flows through narrative compiler into persisted result DTO.

**Frontend path:** `resolveHeroPrimaryStory()` prefers `extractPage1ConcernLeadSentence()` over IDL retail label → `ResultsPrimaryHero.phenotypeLabel`.

**Scrub gap:** `scrubConsumerRetailNarrative()` replaces `signal_homocysteine_elevation_context` slug only — **not** the humanised Title Case form already emitted by backend compiler.

| Classification | Layer |
|----------------|-------|
| Root cause | **Backend assembly** (narrative / clinician report compiler) |
| Contributing | **Frontend rendering** — scrub incomplete for compiler-emitted display names |

---

### A2. Marker role chips expose enum tokens (MEDIUM visibility)

**Observed:** “LDL cholesterol **score contributor**”, “TC/HDL ratio **confidence contributor**”, “CRP **contextual marker**” (inference from lipid transport YAML roles).

**API source:** `marker_evidence[].marker_role` from compiled card YAML (`score_contributor`, `confidence_contributor`, `contextual_marker`).

**Frontend path:** `Wave1SubsystemEvidenceSection.markerRoleChipLabel()` — replaces `_` with space, uppercases nothing → renders raw enum vocabulary.

| Classification | Layer |
|----------------|-------|
| Root cause | **Frontend rendering** |
| Contributing | **Compiled artefact content** — roles are engineering taxonomy, not consumer copy |

---

### A3. Clinician evidence marker refs use naive title-case (LOW visibility)

**Observed:** “related markers: **Mcv**” (should be **MCV**).

**API source:** `clinician_report_v1` → `evidence_for[].marker_refs: ["mcv"]`.

**Frontend path:** `PrimaryFindingAndWhy.formatMarkerRef()` — generic underscore split; **does not use** `LC_S7_BIOMARKER_LABELS` map available in `resultsPageLayout.ts`.

| Classification | Layer |
|----------------|-------|
| Root cause | **Frontend rendering** |

---

### A4. Severity state chips (LOW — acceptable but mechanical)

**Observed:** “**Strong Signal**” badge on IDL pattern cards.

**Source:** `severity_state: "strong_signal"` → `formatSeverityLabel()` splits on `_`.

| Classification | Layer |
|----------------|-------|
| Root cause | **Frontend rendering** (acceptable trade-off unless copy deck specifies different labels) |

---

### A5. Internal IDs **not** visible to user (PASS)

DOM scan found **zero** visible instances of: `ph_*`, `signal_*`, `pkg_*`, `wave1_*`, `compile_manifest`, `health_system_card_evidence_v1`, `score_contributor` as raw snake_case tokens.

`source_trace` values like `health_system_card_evidence_v1:wave1_cv_lipid_transport_v1:knowledge_bus/compiled/manifests/...` are correctly **suppressed** by `isConsumerSafeSourceTrace()`.

---

## 7. Issue B — Health Systems Card marker presence

### 7.1 Full subsystem audit (this analysis)

Panel: **79 scored biomarkers**. Subsystem partition uses **exact canonical ID match** on `panel_biomarker_ids ∪ scored_on_rail`.

| Domain | Subsystem | Expected | Included (API) | Missing (API) | Truly absent from panel? | False missing? |
|--------|-----------|----------|----------------|---------------|--------------------------|----------------|
| CV | Lipid transport | 5 lipid IDs | All 5 | — | — | No |
| CV | Homocysteine pathway | homocysteine | homocysteine | — | — | No |
| CV | Vascular strain | crp | crp | — | — | No |
| Blood sugar | Glycaemic control | glucose, hba1c | hba1c | glucose | glucose absent | **No** |
| Blood sugar | Insulin metabolic | insulin, triglycerides | triglycerides | insulin | insulin absent | **No** |
| Liver | Enzyme pattern | alt, ast, ggt | alt, ggt | ast | ast absent | **No** |
| Liver | Processing context | alp, albumin, bilirubin | all 3 | — | — | No |

**Automated cross-check:** No marker appears in `missing_marker_ids` while present in `biomarkers[].biomarker_name`.

### 7.2 Alias / canonicalisation check

| Pair | Panel state | Subsystem outcome | Notes |
|------|-------------|-------------------|-------|
| `bilirubin` / `total_bilirubin` | `bilirubin` present; `total_bilirubin` absent | Bilirubin **included**; no `total_bilirubin` expected | **Fixed** vs `bb695d3c` — compiled artefact uses canonical `bilirubin` only (`wave1_liv_processing_context.yaml` notes `total_bilirubin` forbidden) |
| `hba1c` / `glucose` | hba1c present; glucose absent | HbA1c included; glucose missing | Correct — no alias equivalence |
| `total_cholesterol` / `cholesterol` | `total_cholesterol` present | Included | N/A |
| HDL / LDL / triglycerides | All present under canonical IDs | Included | N/A |

### 7.3 Why human UAT may still report “wrong missing”

1. **True missing vs user expectation:** Panel has HbA1c but no fasting glucose — glycaemic subsystem correctly flags glucose missing; users may expect HbA1c alone to satisfy “glycaemic control”.
2. **Score / coverage dissonance (see Issue C):** Blood sugar shows **100/100** while UI also states **1 of 3 markers** and lists glucose + insulin missing — reads as contradictory even when presence logic is correct.
3. **Upload fidelity section:** HbA1c row shows “Uploaded representation of HbA1c — not scored separately” while health card treats HbA1c as scored contributor — parallel surfaces disagree on scoring status (not a subsystem partition bug).
4. **Regression elsewhere:** Bilirubin false-missing **was** real on pre-ARCH-RT / pre-compiled artefact analyses (`bb695d3c`); fixed here but worth regression-testing older persisted replays.

| Classification | Layer |
|----------------|-------|
| Marker presence on `18e14232` | **Backend assembly** — working as designed |
| Prior bilirubin false missing | **Alias/canonicalisation** + legacy expected-marker set — **fixed in compiled artefacts** |
| Perceived “wrong missing” | **Styling/prose issue** + user mental model, not partition bug on this ID |

---

## 8. Issue C — Interpretation / display defects

### C1. Blood sugar 100/100 with low confidence and 1/3 evidence (HIGH)

| Field | Value |
|-------|-------|
| `consumer_domain_scores[wave1_blood_sugar].score` | `1.0` → **100/100** |
| `confidence_tier` | `low` |
| `evidence_completeness` | **1 / 3** |
| `missing_marker_ids` (domain level) | `glucose`, `insulin` |
| Active signals | Includes `signal_homocysteine_high` (cross-domain bleed) |

**Root cause:** Domain score derives from rail `biomarker_scores` (HbA1c scored 100) while completeness denominator counts rail scored + domain missing list. Frontend faithfully renders both — **no cap ties score display to evidence completeness**.

| Classification | Layer |
|----------------|-------|
| Root cause | **Backend assembly** (scoring vs completeness semantics) + **frontend rendering** (no gating of perfect score UI when `limitedCoverage`) |

---

### C2. Cardiovascular evidence anchor uses IDL construct name (MEDIUM)

**Observed:** “Based mainly on: **Vascular Inflammation Risk**”

**Source:** `evidence_anchor_sentence` built from top IDL record (`retail_display_label`). Technically consumer-safe but reads like an internal risk construct rather than plain biomarker language.

| Classification | Layer |
|----------------|-------|
| Root cause | **Backend assembly** / **DTO mapping** |

---

### C3. Narrative encoding artefact (LOW)

API `lead_narrative` contains mojibake sequences (`â` replacement characters) for em-dashes / quotes — suggests UTF-8 text passed through a Latin-1 hop during compile or persist.

| Classification | Layer |
|----------------|-------|
| Root cause | **Backend assembly** / persistence encoding |

---

## 9. Compiled card evidence artefact usage (Wave 1)

All **7** Wave 1 subsystems route through `assemble_subsystem_from_compiled_card_evidence()` (`PILOT_COMPILED_SUBSYSTEM_IDS == WAVE1_COMPILED_SUBSYSTEM_IDS`).

| Subsystem ID | Artefact | `source_trace` prefix | `compile_manifest_ref` |
|--------------|----------|----------------------|-------------------------|
| `wave1_cv_lipid_transport` | `wave1_cv_lipid_transport.yaml` | `health_system_card_evidence_v1:wave1_cv_lipid_transport_v1:…` | `arch_rt5b_lipid_transport_card_evidence.yaml` |
| `wave1_cv_homocysteine_pathway` | ✓ | ✓ | `arch_rt5b_homocysteine_pathway_card_evidence.yaml` |
| `wave1_cv_vascular_strain` | ✓ | ✓ | `arch_rt5b_vascular_strain_card_evidence.yaml` |
| `wave1_met_glycaemic_control` | ✓ | ✓ | `arch_rt3_glycaemic_card_evidence.yaml` |
| `wave1_met_insulin_metabolic` | ✓ | ✓ | `arch_rt5b_insulin_metabolic_card_evidence.yaml` |
| `wave1_liv_enzyme_pattern` | ✓ | ✓ | `arch_rt5b_enzyme_pattern_card_evidence.yaml` |
| `wave1_liv_processing_context` | ✓ | ✓ | `arch_rt5b_processing_context_card_evidence.yaml` |

Legacy `_Wave1SubsystemDef` partition path in `wave1_subsystem_evidence.py` is **dead code for Wave 1** at runtime (always hits compiled branch first).

---

## 10. Frontend vs backend rendering responsibility

| Surface | Backend-only | Frontend adds interpretation? |
|---------|--------------|--------------------------------|
| Domain scores & sentences | Yes | No — passthrough |
| Subsystem included/missing IDs | Yes | No |
| Subsystem marker chip labels | Backend `marker_evidence.display_label` | **Yes** — role chip from raw `marker_role` enum |
| Subsystem marker fallback labels | Backend `included_markers` / SSOT | **Yes** — `defensiveFallbackLabel()` if arrays empty |
| `source_trace` | Backend emits internal trace | **Yes** — consumer-safe filter hides it |
| Hero title | Backend `primary_concern` | **Yes** — chooses concern over IDL label; partial scrub |
| IDL pattern cards | Backend records | **Yes** — filter unsafe labels; format severity/class chips |
| Narrative blocks | Backend compiler text | **Yes** — `scrubConsumerRetailNarrative()` pipeline |

**Conclusion:** Marker **presence** is backend-authoritative and correctly wired. Most remaining defects are **consumer copy** (backend compiler strings + frontend chip/label formatting).

---

## 11. Root cause classification matrix

| ID | Defect | Root cause class | Primary owner |
|----|--------|------------------|---------------|
| A1 | “Homocysteine Elevation Context” hero + narrative | Backend assembly | Narrative / signal display-name compiler |
| A2 | “score contributor” / “confidence contributor” chips | Frontend rendering + compiled artefact content | FE subsystem section + card evidence copy deck |
| A3 | “Mcv” marker ref | Frontend rendering | `PrimaryFindingAndWhy` |
| A4 | “Strong Signal” badge | Frontend rendering | Acceptable unless copy review says otherwise |
| B1 | Marker false-missing on `18e14232` | **Not found** | N/A |
| B2 | Historical bilirubin / total_bilirubin | Alias/canonicalisation | **Fixed** in ARCH-RT compiled artefacts |
| C1 | Blood sugar 100/100 vs 1/3 evidence | Backend assembly + frontend rendering | Domain scorer + card visual gating |
| C2 | “Vascular Inflammation Risk” anchor | DTO mapping | Domain assembler / IDL linkage |
| C3 | Narrative mojibake | Backend assembly | Compiler / persist encoding |

---

## 12. Recommended fixes (not implemented)

| Fix | Description | Risk | Sprint split |
|-----|-------------|------|--------------|
| **R1** | Add governed `consumer_role_label` (or map) in compiled card YAML / DTO; stop rendering raw `marker_role` enums | Low | **Same sprint** (FE + small DTO/artefact field) |
| **R2** | Narrative compiler: emit `consumer_lead_pattern_label` distinct from `signal_library.name`; migrate “Homocysteine Elevation Context” → clinician-safe retail string | Medium | **Own sprint** (touches narrative compiler + replay) |
| **R3** | Extend `scrubConsumerRetailNarrative()` with governed replacements for known compiler display names (interim guardrail) | Low | **Same sprint** as R2 interim |
| **R4** | Cap or annotate perfect domain score when `evidence_completeness_denominator - numerator >= 2` or `confidence_tier === 'low'` | Medium | **Same sprint** (backend rule + FE visual) |
| **R5** | Reuse `formatBiomarkerDisplayName()` / `LC_S7_BIOMARKER_LABELS` in `PrimaryFindingAndWhy.formatMarkerRef()` | Low | **Same sprint** (FE-only) |
| **R6** | Align upload-fidelity “not scored separately” copy with rail scoring reality for hba1c | Low | **Same sprint** (FE copy or backend fidelity flag) |
| **R7** | Fix narrative UTF-8 mojibake at compile/persist boundary | Low | **Same sprint** (backend hygiene) |
| **R8** | Persisted replay regression suite for bilirubin / total_bilirubin on pre-ARCH-RT analysis IDs | Low | **Same sprint** (QA harness) |

---

## 13. Frontend components involved

| Component | Role in defects |
|-----------|-----------------|
| `frontend/app/(app)/results/page.tsx` | Orchestrates all sections; passes DTO slices |
| `frontend/app/components/results/ResultsHeroBlocks.tsx` | Hero title from `primary_concern` |
| `frontend/app/components/results/DeterministicNarrativeSurface.tsx` | Retail / lead narrative prose |
| `frontend/app/components/results/ResultsBodyOverview.tsx` | Body overview with “homocysteine elevation context” |
| `frontend/app/components/results/Wave1DomainCards.tsx` | Health system cards, score vs completeness |
| `frontend/app/components/results/Wave1SubsystemEvidenceSection.tsx` | **Role chips**, missing/included markers |
| `frontend/app/components/results/InterpretationPatternsSection.tsx` | IDL pattern cards |
| `frontend/app/components/results/PrimaryFindingAndWhy.tsx` | **Mcv** marker ref formatting |
| `frontend/app/lib/retailNarrativeSanitize.ts` | Incomplete scrub for compiler display names |
| `frontend/app/lib/resultsPageLayout.ts` | Hero story resolution; biomarker label map (not shared with PrimaryFinding) |
| `frontend/app/lib/wave1HealthSystemCardDisplay.ts` | Reliability / completeness strings |

---

## 14. Backend / API payload fields involved

| Module / field | Purpose |
|----------------|---------|
| `backend/core/knowledge/health_system_card_evidence.py` | Compiled artefact load; `assemble_subsystem_from_compiled_card_evidence()` |
| `backend/core/analytics/wave1_subsystem_evidence.py` | Subsystem dispatch (compiled-first) |
| `backend/core/analytics/domain_score_assembler.py` | `_evidence_completeness_for_rail()`, domain copy, `subsystems` attachment |
| `consumer_domain_scores[].subsystems[]` | Full subsystem DTO |
| `marker_evidence[].{marker_id, display_label, marker_role, relationship_kind, presence_policy}` | Per-marker governed evidence |
| `narrative_report_v1.{retail_summary, body_overview, lead_narrative}` | Consumer prose |
| `clinician_report_v1.sections.page1.primary_concern` | Hero lead pattern |
| `interpretation_display_layer_v1.records[]` | Pattern cards + cardiovascular anchor |
| `biomarkers[].biomarker_name` | Ground truth for presence audit |
| `knowledge_bus/packages/pkg_homocysteine_elevation_context/signal_library.yaml` | Source of lead pattern display name |

**Saved payload:** `automation_bus/_launch_core0_18e14232.json`

---

## 15. Comparison to prior UAT (`bb695d3c`)

| Topic | `bb695d3c` (pre/full ARCH-RT) | `18e14232` (this run) |
|-------|-------------------------------|------------------------|
| Bilirubin missing false-positive | Yes (`total_bilirubin` expected) | **No** — artefact uses `bilirubin` only |
| Compiled card path | Partial / rolling | **All 7** subsystems |
| Blood sugar score vs coverage | 100/100, 1/3 markers | Same pattern |
| Lead pattern internal name | Homocysteine Elevation Context | Same — narrative compiler unchanged |
| Role chips | N/A or legacy | **score contributor** visible |

---

## 16. Stop conditions respected

- No production code modified.
- No compiled artefacts modified.
- No backend logic modified.
- No frontend components modified.
- Investigation artefact: this document + API JSON + screenshots under `docs/audit-papers/assets/`.

---

## 17. Suggested next sprint ordering

1. **Quick wins (one sprint):** R1, R3 (interim), R5, R6, R7  
2. **Follow-on sprint:** R2 (compiler-level retail display names), R4 (score/evidence coupling policy)  
3. **QA:** R8 replay regression across `bb695d3c`, `18e14232`, and one fresh upload
