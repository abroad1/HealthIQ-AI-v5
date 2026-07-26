# ARCH-CONV-FINAL — Frontend End-to-End UAT (Completed)

**Work ID:** `ARCH-CONV-FINAL-AUDIT`  
**Status:** **UAT EVIDENCE CAPTURED — programme decision issued**  
**Path convention:** `docs/testing/`  
**Analysis ID:** `e34aaedf-b09f-42f0-8cc8-4653a00b4c10`  
**URL:** `http://localhost:3000/results?analysis_id=e34aaedf-b09f-42f0-8cc8-4653a00b4c10`  
**Environment:** local frontend `:3000` + backend `:8000`  
**Commit SHA (audit branch HEAD at inspection):** `4cbb7f5` (resume) / baseline audit start `5228734`  
**Inspector:** Cursor (browser automation + authenticated API fetch)  
**Account:** local test account supplied by Anthony (identity not recorded here)

Credentials were used only for live login and were **not** written into this artefact, commits, or evidence extracts.

---

## Case summary

| Case ID | Intent | Mapping to this analysis | Result |
|---|---|---|---|
| UAT-2 | Pilot multi-frame panel | Homocysteine B-vitamin + MCV mega/nonmega/anchor + eGFR frames fired | **PARTIAL PASS** (pilot compiled WHY present) with **FAIL** leak findings |
| UAT-3 | Negative leakage | Rejected metabolic must not surface | **FAIL** — rejected metabolic activation still present in API/top_findings/interventions |
| UAT-4 | Rejected metabolic inertness | No methylation-capacity / broad metabolic WHY | **FAIL** — “methylation capacity” visible in clinician synthesis; metabolic signal interpretation uses that phrase |
| UAT-1 | Normal panel | Not this analysis | N/A |

**Anthony overall UAT decision (human):** successful real frontend exercise completed (analysis reachable and reviewable).  
**Audit overall UAT decision (independent inspection):** **FAIL to close programme PASS** — active medical-content / rejected-frame leakage found.

---

## Panel facts observed (rendered)

| Marker | Rendered value | Notes |
|---|---|---|
| Homocysteine | 16.2 µmol/L · Above range | Lead pattern |
| MCV | 99.5 fL · Above range (ref 80–96) | Macrocytosis context |
| Folate | 7.7 ug/L | Supporting B-vitamin context |
| Vitamin B12 | 336 pg/ml | Supporting |
| Active B12 | 139.2 pmol/L | Supporting |
| eGFR | 84 mL/min/1.73m² · Below range | Renal signals also fired |
| Free T3 / Free T4 / TSH | Within displayed ranges | No low-T3/TPO lead |

Lifestyle: moderate alcohol context mentioned in body overview.

---

## Traceability table (visible / API medical statements)

| page section | rendered text (abbrev.) | supporting API field | signal_id | activation_key | source_spec_id | WHY authority | hypothesis ID | expected | actual | PASS/FAIL |
|---|---|---|---|---|---|---|---|---|---|---|
| PRIMARY FINDING | Raised homocysteine pattern… | narrative / IDL retail | `signal_homocysteine_elevation_context` | `…::inv_elevation_context` | `inv_elevation_context` | legacy family lead | n/a (lead card) | Lead from elevation context allowed | Matches lead routing | PASS |
| Patterns across body | Methylation pathway pattern | IDL pattern record | family hcy/mcv | participating keys include pilot frames | mixed | IDL aggregate | n/a | Must not imply rejected metabolic catch-all | Consumer pattern title “Methylation pathway” | FAIL (wording risk) |
| Clinician summary | Top ranked hypothesis… reduced B12-related **methylation capacity** | `clinician_report_v1` / synthesis from elevation-context hyps | `signal_homocysteine_elevation_context` | `…::inv_elevation_context` | `inv_elevation_context` | LEGACY family WHY | `hcy_b12_pattern_v1` | No “methylation capacity” claim per PKG3 reject rule spirit | Phrase present in clinician UX | **FAIL** |
| API signal row (not shown as raw key on page) | interpretation: “Reflects **methylation capacity** and B-vitamin status.” | `meta.insight_graph.signal_results[]` | `signal_homocysteine_high` | `…::inv_homocysteine_high_metabolic` | `inv_homocysteine_high_metabolic` | REJECTED (WHY) but signal still active | n/a | Rejected frame inactive end-to-end | Signal fires; interpretation uses forbidden phrase | **FAIL** |
| API top_findings | metabolic frame ranked | `report_v1.top_findings` | `signal_homocysteine_high` | `…::inv_homocysteine_high_metabolic` | `inv_homocysteine_high_metabolic` | should not be user-facing authority | n/a | Rejected frame not in rankings | Present in top_findings | **FAIL** |
| Interventions | vascular clinician referral / lifestyle | `activation_key_refs` | `signal_homocysteine_high` | includes `…metabolic` | `inv_homocysteine_high_metabolic` | rejected | n/a | Rejected key not cited | Cited on 2 interventions | **FAIL** |
| Compiled WHY (B-vitamin) | Folate/B12 associated wording | `root_cause_v1.findings` | `signal_homocysteine_high` | `…b_vitamin…` | `inv_homocysteine_high_b_vitamin…` | COMPILED_ACTIVE | `hyp_folate…`, `hyp_b12…` | Ratified hyps only | Matches pack | **PASS** |
| Compiled WHY (MCV anchor) | Morphology only | root_cause | `signal_mcv_high` | `…macrocytosis` | `inv_mcv_high_macrocytosis` | COMPILED_ACTIVE | `mcv_high_anchor_pattern_v1` | Anchor only | Present | PASS |
| Compiled WHY (MCV mega) | vitamin-related macrocytosis | root_cause | `signal_mcv_high` | `…megaloblastic…` | `inv_mcv_high_megaloblastic…` | COMPILED_ACTIVE | `hyp_megaloblastic…` | Ratified | Present | PASS |
| Compiled WHY (MCV nonmega) | non-vitamin differential | root_cause | `signal_mcv_high` | `…nonmegaloblastic…` | `inv_mcv_high_nonmegaloblastic…` | COMPILED_ACTIVE | `hyp_alcohol_or_hepatic…` | Ratified; no alcohol DX asserted on consumer card alone | Present alongside mega+anchor | FAIL vs Frame 5 “no duplicate causal” intent |
| Provenance-blocked kb47 | — | production registry | — | — | — | — | — | No blocked pkg in fired set | No DHEA/etc. in fired | PASS |
| Rejected metabolic WHY finding | — | root_cause findings | metabolic | — | — | REJECTED skip | — | No WHY finding for metabolic | No metabolic root finding | PASS (WHY path only) |

---

## Anthony questions (answered from this inspection)

1. Medical/business sense? Partially — lead hcy story is coherent, but rejected/legacy wording leaks undermine trust.  
2. WHY match inputs? B-vitamin compiled WHY fits; legacy elevation-context “methylation capacity” overclaims.  
3. Cause without support? MCV nonmega alcohol/hepatic differential appears without strong hepatic/alcohol lab proof (GGT in range).  
4. Old/duplicated/contradictory? Yes — legacy elevation-context hyps + compiled B-vitamin hyps + metabolic signal interpretation coexist.  
5. Rejected/blocked/retired visible? Rejected metabolic **not** shown as raw activation key on consumer page, but **is** in API, rankings, interventions, and related wording reaches clinician summary.  
6. Consumer/clinician same story? Same lead family; clinician exposes “methylation capacity” more explicitly.  
7. Activation frame traceable? Yes in API; consumer lead is elevation-context, not B-vitamin compiled key.  
8. Layer C alteration? Prior BOUNDARY_LEAKs remain in FE code; this page also shows FE-assembled pattern titles.  
9. Surprising? **Yes** — PKG3 rejection did not remove metabolic frame from runtime signal/ranking/intervention surfaces.

---

## Evidence preserved

- Authenticated `GET /api/analysis/result?analysis_id=e34aaedf-…` inspected in-browser (token not stored).  
- Browser screenshots captured locally during session (not committed; contain account chrome).  
- Structured findings recorded in this file and `docs/architecture/ARCH-CONV-FINAL_end_to_end_pipeline_and_leakage_report.md`.

---

## Resume / decision

Final programme decision: **CORRECT** (see verification report).  
Do not claim PASS.

---

## ARCH-CONV-CORRECT-1 post-correction re-test (added by the correction package)

**Work ID:** `ARCH-CONV-CORRECT-1` · **Branch:** `feature/arch-conv-correct-1-e2e-authority-layerc`
**Method:** deterministic replay of this analysis's recorded panel through Layer B and report
assembly (`backend/scripts/replay_arch_conv_correct1_uat_case.py`), plus frontend component
render tests. No credentials, no account data and no network access were used.

### Traceability re-test (rows that previously failed)

| page section | rendered text after correction | supporting API field | activation_key | WHY authority | hypothesis ID | expected | actual | PASS/FAIL |
|---|---|---|---|---|---|---|---|---|
| Patterns across body | "One-carbon pathway pattern" | IDL `retail_display_label` | family hcy/mcv | IDL aggregate | n/a | No methylation-capacity framing | Governed one-carbon label | **PASS** |
| Clinician summary | "Homocysteine is elevated and may be associated with reduced availability of vitamin B12, particularly if that marker is also low or borderline. Other factors can also raise homocysteine." | `root_cause_v1.findings[].hypotheses[].summary` | `signal_homocysteine_elevation_context::inv_elevation_context` | LEGACY family WHY | `hcy_b12_pattern_v1` | No "methylation capacity" claim | Ratified B-vitamin wording only | **PASS** |
| API signal row | — (row absent) | `meta.insight_graph.signal_results[]` | `…::inv_homocysteine_high_metabolic` | REJECTED → not runtime-eligible | n/a | Rejected frame inactive end-to-end | Absent from fired set | **PASS** |
| API top_findings | — (row absent) | `report_v1.top_findings` | `…::inv_homocysteine_high_metabolic` | REJECTED | n/a | Not in rankings | 7 rows, none rejected | **PASS** |
| Interventions | vascular referral / lifestyle now cite the elevation-context key only | `activation_key_refs` | `…::inv_homocysteine_high_metabolic` | REJECTED | n/a | Rejected key not cited | 0 citations (was 2) | **PASS** |
| Compiled WHY (MCV family) | Morphology context only on this panel | `root_cause_v1.findings[].why_role` | `…::inv_mcv_high_macrocytosis` | COMPILED_ACTIVE | `mcv_high_anchor_pattern_v1` | No duplicate causal WHY | Anchor `morphology_context`; both specific frames suppressed (GGT/ALT and hematinics in range) | **PASS** |
| Layer C boundary | Driver, colour, confidence, order all backend-supplied | `meta.insight_graph.primary_driver_v1` etc. | n/a | Layer B ranking policy | n/a | No FE medical decision | 12/12 inventory leaks closed | **PASS** |

Rows that already passed (compiled B-vitamin WHY, provenance-blocked packages, rejected-frame
WHY silence) were re-verified unchanged.

### Anthony's original questions — re-answered after correction

1. Rejected/legacy wording no longer leaks into API, rankings, interventions or clinician text.
2. Cause without support: the MCV alcohol/hepatic differential no longer serves as causal WHY
   while GGT and ALT are in range.
3. Duplicate/contradictory explanations: MCV siblings can no longer co-emit causal WHY.
4. Layer C no longer alters a Layer B medical decision.

### Outstanding UAT obligation

This re-test is deterministic-replay plus component-render evidence. A **fresh human UAT of the
live page** for this analysis is still required before any programme PASS, and no controlled-beta
readiness claim is made here.
