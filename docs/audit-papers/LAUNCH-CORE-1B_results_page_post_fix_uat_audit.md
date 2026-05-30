# LAUNCH-CORE-1B — Post-Fix Results Page Human UAT Audit

**Analysis:** `746f2b0a-b470-4d87-8ed8-e2c3d1e68c02`  
**URL:** `http://localhost:3000/results?analysis_id=746f2b0a-b470-4d87-8ed8-e2c3d1e68c02`  
**Account:** `test-user3@example.com`  
**Repo:** `main` @ `48b078b` (post LAUNCH-CORE-1 merge)  
**Prior baseline:** `docs/audit-papers/LAUNCH-CORE-0_results_page_human_uat_investigation.md`  
**Fix reference:** `docs/audit-papers/LAUNCH-CORE-1_results_page_card_coherence_and_consumer_copy_report.md`  
**Date:** 2026-05-30  
**Mode:** Investigation only — no code or artefact changes made.

---

## 1. Executive verdict

### **PASS WITH RESERVATIONS**

LAUNCH-CORE-1 fixes are **visible and working** on the target analysis for all six primary acceptance checks. The blood-sugar completeness mismatch that blocked LAUNCH-CORE-0 is **resolved** (`2 of 4` summary matches expanded subsystem chips). Cardiovascular and liver completeness also align with subsystem unions.

Reservations are **non-blocking copy/presentation polish**, not structural regressions:

- IDL construct label **“Vascular Inflammation Risk”** still surfaces as the cardiovascular evidence anchor (pre-existing, not LAUNCH-CORE-1 scope).
- Persisted API narrative still contains raw compiler strings and mojibake; **frontend scrub hides them at render time** — durable fix would be backend recompile.
- Blood sugar **100/100** with qualification line is clearer than before but may still read oddly alongside **Limited reliability** and **2 of 4** markers.

**Launch recommendation:** Safe to proceed for Wave 1 card journey; schedule follow-up for backend narrative compiler retail labels (not display-only scrub).

---

## 2. Investigation method

1. Browser login + full page load of target URL.
2. Expanded all three Health Systems Cards; captured hero and card screenshots.
3. DOM text scan for forbidden internal tokens and LAUNCH-CORE-0 defect strings.
4. Authenticated API fetch → `automation_bus/_launch_core1b_746f2b0a.json`.
5. Cross-checked DTO completeness vs subsystem included/missing unions for all three domains.
6. Ran `python backend/scripts/validate_day_one_architecture.py` (ARCH-RT-6 guardrails).

---

## 3. Screenshots

| File | Description |
|------|-------------|
| `docs/audit-papers/assets/lc1b-hero.png` | Page header / journey intro |
| `docs/audit-papers/assets/lc1b-health-systems-expanded.png` | Cardiovascular card with **7 of 7** completeness |

*(Blood sugar and liver expanded states verified via accessibility snapshot — see section 5.)*

---

## 4. Console and network

### Console

- **No JavaScript errors or warnings** observed after load and card expansion.
- DOM scan for raw internal tokens (`score contributor`, `Homocysteine Elevation Context`, `signal_*`, `pkg_*`, `compile_manifest`, etc.) returned **zero matches**.

### Network

| Request | Result |
|---------|--------|
| `POST /api/auth/login` | 200 |
| `GET /api/auth/me` | 200 |
| `GET /api/analysis/result?analysis_id=746f2b0a-b470-4d87-8ed8-e2c3d1e68c02` | 200 (~256 ms) |
| `POST /api/wedge-events` | 200 |

---

## 5. LAUNCH-CORE-1 fix verification

| Check | LAUNCH-CORE-0 (pre-fix) | Observed post-fix | Status |
|-------|-------------------------|-------------------|--------|
| Blood sugar completeness vs subsystems | Summary **1 of 3** vs detail **2 included + 2 missing** | Summary **2 of 4**; detail **HbA1c + Triglycerides** included, **Glucose + Insulin** missing | **PASS** |
| Role chips | `score contributor`, `confidence contributor` | `Used in this score`, `Supports confidence`, `Context marker` | **PASS** |
| “Homocysteine Elevation Context” in UI | Visible in hero/narrative | **Not visible**; scrubbed to **“Raised homocysteine pattern”** | **PASS** |
| MCV marker ref | `Mcv` | **MCV** in Primary finding section | **PASS** |
| Mojibake (`â` etc.) in visible UI | Present in persisted narrative | **Not visible** in rendered body text (`hasMojibake: false`) | **PASS** |
| Score qualification when limited | 100/100 with no qualification | **“Score based on available markers only”** (CV 86) / **“Score based on available markers”** (BS 100, Liver 73) | **PASS** |

---

## 6. Health Systems Cards — completeness and subsystem detail

### 6.1 Summary table (API + browser)

| Domain | Score | Confidence | Completeness (summary) | Subsystem union (included / total) | Summary ↔ detail match |
|--------|-------|------------|------------------------|-------------------------------------|-------------------------|
| Cardiovascular | 86/100 | high | **7 / 7** | 7 / 7 | **Yes** |
| Blood sugar | 100/100 | low | **2 / 4** | 2 / 4 | **Yes** |
| Liver | 73/100 | low | **5 / 6** | 5 / 6 | **Yes** |

Backend field source: `consumer_domain_scores[].evidence_completeness_numerator/denominator` from `_evidence_completeness_from_subsystems()` (LAUNCH-CORE-1).

### 6.2 Cardiovascular (`wave1_cardiovascular`) — **7 / 7**

| Subsystem | Included | Missing |
|-----------|----------|---------|
| Lipid transport | `hdl_cholesterol`, `ldl_cholesterol`, `tc_hdl_ratio`, `total_cholesterol`, `triglycerides` | — |
| Homocysteine pathway | `homocysteine` | — |
| Vascular strain | `crp` | — |

**Browser chips:** e.g. “LDL cholesterol **Used in this score**”, “TC/HDL ratio **Supports confidence**”, “CRP **Context marker**”.

**False missing check:** None — all seven expected markers present in `biomarkers[]`.

### 6.3 Blood sugar (`wave1_blood_sugar`) — **2 / 4**

| Subsystem | Included | Missing |
|-----------|----------|---------|
| Glycaemic control | `hba1c` | `glucose` |
| Insulin and metabolic context | `triglycerides` | `insulin` |

**Browser:** Summary **“2 of 4 expected markers included”**; expanded section shows **2 green + 2 grey** chips — **consistent**.

**False missing check:** `glucose` and `insulin` genuinely absent from panel (79 biomarkers); `hba1c` and `triglycerides` present.

### 6.4 Liver (`wave1_liver`) — **5 / 6**

| Subsystem | Included | Missing |
|-----------|----------|---------|
| Liver enzyme pattern | `alt`, `ggt` | `ast` |
| Liver processing context | `albumin`, `alp`, `bilirubin` | — |

**Browser:** Summary **“5 of 6 expected markers included”**; expanded **5 green + 1 grey (AST Not uploaded)** — **consistent**.

**False missing check:** `ast` genuinely absent; `bilirubin` included (no `total_bilirubin` false-missing — ARCH-RT canonical artefact).

---

## 7. Compiled card evidence (all 7 subsystems)

All subsystem rows carry compiled-artefact `source_trace` prefix `health_system_card_evidence_v1:` and non-null `compile_manifest_ref` in API (not rendered in UI):

| Subsystem ID | Manifest ref (truncated) |
|--------------|--------------------------|
| `wave1_cv_lipid_transport` | `arch_rt5b_lipid_transport_card_evidence.yaml` |
| `wave1_cv_homocysteine_pathway` | `arch_rt5b_homocysteine_pathway_card_evidence.yaml` |
| `wave1_cv_vascular_strain` | `arch_rt5b_vascular_strain_card_evidence.yaml` |
| `wave1_met_glycaemic_control` | `arch_rt3_glycaemic_card_evidence.yaml` |
| `wave1_met_insulin_metabolic` | `arch_rt5b_insulin_metabolic_card_evidence.yaml` |
| `wave1_liv_enzyme_pattern` | `arch_rt5b_enzyme_pattern_card_evidence.yaml` |
| `wave1_liv_processing_context` | `arch_rt5b_processing_context_card_evidence.yaml` |

---

## 8. Internal field visibility

| Field / pattern | In API payload | Visible in browser |
|-----------------|----------------|-------------------|
| `source_trace` (internal path form) | Yes | **No** — filtered by `isConsumerSafeSourceTrace()` |
| `compile_manifest_ref` | Yes | **No** |
| `artefact_id` / `source_spec_ids` | In compiled YAML only | **No** |
| `signal_*` / `pkg_*` / `wave1_*` IDs | In meta/insights | **No** in consumer surfaces |
| Raw `marker_role` enum text | In DTO | **No** — mapped via `consumerMarkerRoleLabel()` |

---

## 9. ARCH-RT-6 guardrails

```
python backend/scripts/validate_day_one_architecture.py
→ day_one_architecture_validation: PASS
```

No regression detected in day-one architecture validation after LAUNCH-CORE-1.

---

## 10. Remaining defects (post-fix)

| ID | Observation | Visible? | Root cause class | Blocks launch? |
|----|-------------|----------|------------------|----------------|
| R1 | **“Vascular Inflammation Risk”** as cardiovascular evidence anchor | Yes | DTO mapping / IDL `retail_display_label` | No |
| R2 | **“Strong Signal”** severity chip on IDL pattern cards | Yes | Frontend rendering (`formatSeverityLabel`) | No |
| R3 | Raw **“Homocysteine Elevation Context”** still in persisted `narrative_report_v1` / `clinician_report_v1` API fields | API only | Backend assembly (compiler); FE scrub masks UI | No for UI; yes for API/export hygiene |
| R4 | Mojibake in persisted `body_overview` / `lead_narrative` API text | API only; **not in rendered body** | Backend persist encoding | No for UI |
| R5 | Blood sugar **100/100** with **Limited reliability** + **2/4** markers | Yes | Backend scoring semantics + FE qualification (partially mitigated) | No — improved vs LC-0 |
| R6 | HbA1c upload-fidelity note vs scored chip both present | Yes | Copy-only / dual surface alignment | No |

---

## 11. API payload fields involved

| Field | Role in audit |
|-------|---------------|
| `consumer_domain_scores[].evidence_completeness_numerator/denominator` | LAUNCH-CORE-1 subsystem-union completeness |
| `consumer_domain_scores[].subsystems[]` | Included/missing + `marker_evidence[].marker_role` |
| `consumer_domain_scores[].score`, `confidence_tier` | Score qualification gating |
| `narrative_report_v1.*` | Raw compiler prose (scrubbed at FE) |
| `clinician_report_v1.sections.page1.primary_concern` | Hero lead (scrubbed at FE) |
| `clinician_report_v1.sections.root_cause.hypotheses[].evidence_for[].marker_refs` | MCV display |
| `biomarkers[].biomarker_name` | Ground truth for false-missing audit |

**Saved payload:** `automation_bus/_launch_core1b_746f2b0a.json`

---

## 12. Frontend components verified

| Component | LAUNCH-CORE-1 role |
|-----------|-------------------|
| `Wave1DomainCards.tsx` | Renders DTO completeness; `wave1ScoreQualificationLine()` |
| `Wave1SubsystemEvidenceSection.tsx` | `consumerMarkerRoleLabel()` role chips |
| `Wave1HealthSystemScoreVisual.tsx` | Limited-coverage visual styling |
| `cardEvidenceConsumerCopy.ts` | Role map + `scrubKnownInternalPatternNames()` |
| `retailNarrativeSanitize.ts` | Mojibake + pattern name scrub pipeline |
| `PrimaryFindingAndWhy.tsx` | `formatBiomarkerDisplayName()` for marker refs |
| `ResultsHeroBlocks.tsx` / `DeterministicNarrativeSurface.tsx` / `ResultsBodyOverview.tsx` | Scrubbed narrative surfaces |

---

## 13. Recommended follow-up (not implemented)

| Fix | Layer | Risk | Sprint |
|-----|-------|------|--------|
| Emit consumer-safe lead pattern label from narrative compiler (stop relying on FE scrub) | Backend assembly | Medium | Post-launch hygiene |
| Re-encode or recompile persisted narratives to remove mojibake at source | Backend persist / compiler | Low | Post-launch hygiene |
| Plain-language IDL anchor for cardiovascular card (alternative to “Vascular Inflammation Risk”) | DTO / copy deck | Low | Optional polish |
| Consider score cap or band downgrade when completeness &lt; 50% and confidence low | Backend + FE | Medium | Product decision — separate from LC-1 |

---

## 14. Before / after — blood sugar card (primary LC-0 defect)

| Surface | LAUNCH-CORE-0 (`18e14232`) | LAUNCH-CORE-1B (`746f2b0a`) |
|---------|---------------------------|----------------------------|
| Evidence completeness | **1 of 3** | **2 of 4** |
| Expanded included | HbA1c, Triglycerides | Same |
| Expanded missing | Glucose, Insulin | Same |
| Summary ↔ detail | **Mismatch** | **Aligned** |
| Role chips | `score contributor` | `Used in this score` |
| Score note | None | **Score based on available markers** |

---

## 15. Stop conditions respected

- No production code, compiled artefacts, backend logic, or frontend components modified.
- Investigation artefacts: this document, API JSON, screenshots under `docs/audit-papers/assets/`.
