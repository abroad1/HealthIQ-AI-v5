# FE-R4 — Patterns Layer Gate and Implementation Decision

**work_id:** FE-R4  
**branch:** `frontend/fe-r4-patterns-layer-gate`  
**change_type:** CONTENT (audit/specification only — no runtime changes)  
**date:** 2026-05-24

---

## 1. Executive verdict

**GO WITH CONDITIONS**

A governed pattern-display layer **exists** (`interpretation_display_layer_v1` / BE-IDL-1) and a frontend renderer **already exists** (`InterpretationPatternsSection.tsx`), but Section 5 is **not** implementation-ready as a full retail-journey sprint using `clusters[]` or domain cards. The next work must be a **limited frontend surfacing sprint (FE-R5A)** using IDL-only fields, plus a **contract/content hardening sprint (PATTERN-C1)** before claiming a complete phenotype/pattern taxonomy layer across panels.

---

## 2. Preflight and guard results

| Check | Result |
|-------|--------|
| `git branch` at audit start | `main` → `frontend/fe-r4-patterns-layer-gate` |
| `git stash list` | **Empty** (no stashes) |
| Dirty before kernel start | `automation_bus/latest_cursor_prompt.md`, `latest_prompt_hardening.json` — committed as `chore(bus): FE-R4 work package prompt and hardening` |
| Kernel start | Success — token `work_id=FE-R4`, branch `frontend/fe-r4-patterns-layer-gate` |
| Cross-sprint guards | **All pass** (see commands below) |

```powershell
python -m pytest backend/tests/regression/test_fe_r1_consumer_prose_cleanup.py -q
python -m pytest backend/tests/regression/test_fe_r2_results_journey_restructure.py -q
python -m pytest backend/tests/regression/test_fe_r3_evidence_depth_ux_quality.py -q
python -m pytest backend/tests/regression/test_lc_s16_17_19_kb_surface_payload_contract.py -q
python -m pytest backend/tests/regression/test_lc_s18_root_cause_why_registration.py -q
python -m pytest backend/tests/regression/test_lc_s20_22_persisted_replay_sentinel_phase2.py -q
```

**Output:** 86 passed, 0 failed (single run, 2026-05-24).

---

## 3. FE-R1/2/3 merge confirmation

| Evidence | Status |
|----------|--------|
| `test_fe_r1_consumer_prose_cleanup.py` on `main` | Present — passes |
| `test_fe_r2_results_journey_restructure.py` on `main` | Present — passes |
| `test_fe_r3_evidence_depth_ux_quality.py` on `main` | Present — passes (merged at `fb20990`) |
| `FE-R1_consumer_prose_cleanup_narrative_safety_notes.md` | Present |
| `FE-R2_results_journey_restructure_notes.md` | Present |
| `FE-R3_evidence_depth_ux_quality_pass_notes.md` | Present |
| Main ancestry | `fb20990` includes FE-R3; FE-R1/R2 commits on ancestry |

**Conclusion:** FE-R1, FE-R2, and FE-R3 are merged to `main`. Audit may proceed.

---

## 4. Current pattern-surface implementation

### 4.1 Retail journey (FE-R2 Phase 1)

The v6 Section 5 slot in the **retail** journey is **not** populated. `frontend/app/(app)/results/page.tsx` implements seven FE-R2 sections (body overview → working well → primary finding → uncertainty → marker evidence → next steps → clinician summary). **No** “Patterns across your body” block appears in that ordered list.

### 4.2 Existing pattern UI (collapsed / supplementary)

| Surface | Location | Data source | Journey role |
|---------|----------|-------------|--------------|
| `InterpretationPatternsSection` | Disclosure **“Pattern cards and health domains”** (`defaultOpen={false}`) | `interpretation_display_layer_v1` | Closest to v6 Section 5; **not** in retail order |
| `Wave1DomainCards` | Same disclosure block | `consumer_domain_scores[]` | Commercial domain scores (3 wave-1 domains) — **not** the pattern layer |
| `ClusterSummary` | **Advanced analysis** disclosure only | `clusters[]` via `clusterSummaries` | Technical cluster view — **unsafe** for retail pattern naming |
| `SystemUnderstandingSection` | “Additional interpretation context” disclosure | `clusters[]` + IDL label | Educational prose; uses cluster names in copy |
| `InterpretationPatternsSection` header | Renders **“Patterns across your body”** | IDL only | Correct heading; buried |

Component comment references “FE-R8” — implementation was started ahead of this gate; FE-R4 confirms it must not be promoted without the conditions below.

### 4.3 Field wiring summary

| Question | Answer |
|----------|--------|
| Uses `interpretation_display_layer_v1`? | **Yes** — sole feed for `InterpretationPatternsSection` |
| Uses `clusters[]` for pattern cards? | **No** in IDL section; **yes** in advanced/educational surfaces |
| Uses `consumer_domain_scores`? | **Yes** — adjacent domain cards, not interchangeable with pattern layer |
| Uses `root_cause_v1`? | **No** in pattern section (clinician report / primary finding only) |
| Raw internal IDs in pattern UI? | IDL `internal_id` used as React `key` only — **not** shown to user |
| Display names reliable? | **Yes** for enabled IDL rows (`retail_display_label` after `sanitize_retail_display_label`) |
| Subtitles / why-it-matters? | **Yes** when IDL row enabled |
| Supporting markers? | **Yes** — `supporting_biomarkers_summary` (dynamic at publish) |
| Severity/status? | **Yes** — `severity_state` chip (enum labels formatted in frontend) |
| Scientific classification in UI? | **No** — `scientific_class` in DTO but **not rendered** |

---

## 5. Current DTO/API field inventory

### 5.1 `interpretation_display_layer_v1` (primary — governed)

**Contract:** `backend/core/contracts/interpretation_display_layer_v1.py`  
**Static authority:** `knowledge_bus/interpretation_display_layer_v1/idl_records_v1.yaml`  
**Publish:** `backend/core/analytics/interpretation_display_layer_publish_v1.py` → orchestrator attaches to analysis result  
**Frontend types:** `frontend/app/types/analysis.ts` (`InterpretationDisplayRecordV1`)

Per-record fields available to frontend:

- `internal_id` (governed; display-suppressed)
- `scientific_class` — `phenotype | risk_construct | organ_pattern | syndrome_state`
- `clinical_display_label`, `retail_display_label`, `subtitle`, `why_it_matters`
- `severity_state` — `not_observed | watch | attention | strong_signal`
- `supporting_biomarkers_summary` (runtime-derived from insight_graph signals)
- `frontend_allowed_term` — `phenotype_allowed | clinical_only`
- `enabled_for_frontend` (static ∧ severity ≠ `not_observed`)
- Optional: `supporting_systems_summary`, `user_safe_description`, `display_caveat`

**Enablement rule:** `enabled_for_frontend = static_enabled AND severity_state != "not_observed"`. On AB/homocysteine fixture (`lc_s20_ab_launch_core_v1.json`), **one** record is typically enabled (`ph_vascular_hcy_inflammation_v1` or methylation family depending on signal fire); most registry rows ship with `enabled_for_frontend: false` at runtime.

### 5.2 `clusters[]` (secondary — not pattern-contract safe)

Cluster objects (`Cluster` in `analysis.ts`) expose `name`, `description`, `summary`, `biomarkers`, `severity`, `recommendations`, `system_educational_explainer`. Names are often **engine labels** (e.g. “Cardiovascular 4 Biomarkers”, “Cardiovascular Health Pattern”) — documented as consumer-unsafe in FE-R0. **Not** a substitute for Section 5.

### 5.3 `consumer_domain_scores[]` (adjacent layer)

Wave-1 domain cards (`wave1_cardiovascular`, `wave1_blood_sugar`, `wave1_liver`) with `consumer_label`, `headline_sentence`, `contributor_sentence`, `evidence_anchor_sentence`. Useful commercially but **overlap** narratively with IDL/domain compilers; `evidence_anchor_sentence` can leak internal cluster/signal names (FE-R0).

### 5.4 `root_cause_v1` / clinician report

Hypothesis and evidence live under `clinician_report_v1.sections` — appropriate for Section 3–4, **not** Section 5 pattern cards.

---

## 6. v6 pattern contract readiness matrix

| Required field | Present? | Source | Governed? | Consumer-safe? | Stable across panels? | Notes |
|---|---|---|---|---|---|---|
| Clinical display name | **Present** | `retail_display_label` (+ `clinical_display_label` in DTO) | Yes — IDL YAML + sanitize | Yes when enabled | **Partial** — only enabled rows; registry ~11 phenotypes | Do not use `clusters[].name` |
| Plain-English subtitle | **Present** | `subtitle` | Yes — IDL YAML | Yes | Partial — same enablement gate | |
| Why-it-matters explainer | **Present** | `why_it_matters` | Yes — IDL YAML | Yes | Partial | Duplicated in narrative/hero if not deduped when promoted |
| Supporting markers/signals | **Present** | `supporting_biomarkers_summary` | Yes — publish-time from insight_graph | Mostly | Partial | Generic fallback: “Key pattern signals for this interpretation.” when no metrics |
| Severity/status | **Present** | `severity_state` | Yes — derived from signal fire | Yes (enum chips) | Partial | `not_observed` → row disabled |
| Scientific classification (4-class taxonomy) | **Partial** | `scientific_class` in DTO | Yes — IDL YAML | Yes if shown as label | Partial | **Not surfaced in UI today** — contract exists, presentation missing |
| Unified pattern card UX | **Partial** | `InterpretationPatternsSection` | Yes — IDL-only | Yes | Partial | Exists but **not** in retail journey; taxonomy chip absent |
| Phase 2 “full phenotype layer” | **Partial** | IDL registry | Yes | Yes for registered IDs | **No** — coverage limited to registry; not all panels fire all `ph_*` rows | Expand registry + signal mapping in PATTERN-C1 |

---

## 7. Taxonomy/classification assessment

- **Governed taxonomy exists** in backend/DTO as `scientific_class` with four v6-aligned values.
- **Frontend does not display** scientific class — users cannot distinguish phenotype vs risk construct vs organ-pattern vs syndrome-state.
- **`frontend_allowed_term`** gates phenotype marketing language (`phenotype_allowed` vs `clinical_only`) but is **not** shown in UI; only used implicitly via IDL filter (`clinical_only` rows still render if enabled).
- **Recommendation:** PATTERN-C1 should require a consumer-safe class chip (e.g. “Risk pattern”, “Organ pattern”) mapped from enum — no frontend invention.

---

## 8. Naming quality assessment

| Name / label | Source | Current use | Classification | Verdict | Recommendation |
|---|---|---|---|---|---|
| Methylation pathway pattern | IDL `ph_one_carbon_homocysteine_macrocytosis_v1` | IDL pattern card (when enabled) | Consumer-safe | **Keep** | Primary Section 5 exemplar on homocysteine panels |
| Vascular Inflammation Risk | IDL `ph_vascular_hcy_inflammation_v1` | IDL card; also leaked in hero/domain anchors (FE-R0) | Consumer-safe label; **overused** | **Keep label; dedupe surfacing** | PATTERN-C1: stop reuse as hero anchor name |
| Insulin Resistance Phenotype | IDL registry | IDL card when IR signals fire | Consumer-safe | Keep | |
| Blood Sugar Stress State | IDL registry | IDL when enabled | Consumer-safe | Keep | |
| Liver / Kidney / Thyroid *Pattern* | IDL registry | IDL when enabled | Consumer-safe | Keep | |
| Cardiovascular Health Pattern | `clusters[].name` | SystemUnderstanding, cluster summaries | Internal/technical | **Hide from pattern layer** | Do not use for Section 5 cards |
| Cardiovascular 4 Biomarkers | Compiler/cluster id phrasing | Body overview, cluster context | Internal/technical | **Hide** | Backend rewrite (PATTERN-C1) |
| Functional read — one-carbon pathway… | Narrative/compiler thread labels | Body overview themes | Internal/technical | **Hide** | Omit from retail (FE-R1 partial fix) |
| Homocysteine Elevation Context / Homocysteine High | Signal/thread labels | Why lead won, hero | Internal/technical | **Hide in retail** | Already FE-R1 concern; not pattern cards |
| Your health domains (Wave-1) | `consumer_domain_scores` | Adjacent disclosure | Consumer-safe framing | **Keep separate** | Not Section 5 — do not merge with pattern cards |

---

## 9. Assets safe to use now

- `interpretation_display_layer_v1.records[]` filtered by `enabled_for_frontend === true` and `frontend_allowed_term !== 'clinical_only'` (current component filter).
- Fields: `retail_display_label`, `subtitle`, `why_it_matters`, `supporting_biomarkers_summary`, `severity_state`, optional `user_safe_description`, `display_caveat`.
- Existing `InterpretationPatternsSection` component logic (no cluster inference).
- FE-R2 retail journey **position 5** (after uncertainty, before marker evidence) as target placement — per v6 order; requires FE-R5A page reorder only.

---

## 10. Assets not safe to use yet

- `clusters[]` names/descriptions as pattern card titles (internal labels).
- `consumer_domain_scores` as pattern cards (different product layer; anchor sentence leaks).
- `root_cause_v1` hypothesis titles as pattern names.
- Raw `insight_graph` signal labels in consumer pattern copy.
- Full registry rows when `severity_state === not_observed` (correctly suppressed — do not force-show).
- Pretending scientific taxonomy is complete without UI surfacing of `scientific_class`.

---

## 11. Risks of premature implementation

1. **Promoting cluster cards** to Section 5 would reintroduce FE-R0 naming failures (“Cardiovascular 4 Biomarkers”).
2. **Promoting IDL without journey placement** leaves value buried in collapsed disclosure (current state).
3. **Promoting IDL without deduplication** repeats methylation/vascular copy across hero, retail summary, and pattern cards (FE-R0 § duplicate blocks).
4. **Showing all registry rows** regardless of `enabled_for_frontend` would display “empty” patterns with generic supporting text — misleading.
5. **Frontend-invented taxonomy or pattern names** would violate governance (Intelligence Core boundary).
6. **Merging domain cards + pattern cards** in one section blurs commercial domains vs interpretation patterns.

---

## 12. Recommended next sprint

### Path C — Limited interim + contract hardening (selected)

#### FE-R5A — Limited IDL Pattern Surface (frontend surfacing sprint)

**Scope:**

- Move `InterpretationPatternsSection` into FE-R2 retail journey at Section 5 (between uncertainty and marker evidence).
- Keep `Wave1DomainCards` and `ClusterSummary` in supplementary/advanced disclosures only.
- Add consumer-safe **classification chip** from `scientific_class` (display map only — no new clinical logic).
- Add regression tests: journey order, IDL-only rendering, no `clusters[].name` in pattern section, no internal-id visible copy, empty state when no enabled IDL rows.
- Sentinel: `patterns_section_missing_from_retail_journey`, `pattern_card_uses_cluster_name`, `pattern_scientific_class_not_shown`, `pattern_internal_id_visible`.

**Fields to use:** IDL fields listed in §9.  
**Fields to avoid:** `clusters[].name`, `cluster_id`, signal thread labels, raw confidence numbers.

**Fallback:** If `selectVisibleIdlRecords(bundle).length === 0`, omit Section 5 entirely (component already returns `null`) — do not fall back to clusters.

#### PATTERN-C1 — Governed Pattern Display Contract (backend/content sprint)

**Scope:**

- Expand IDL registry coverage and signal→`ph_*` mapping for panels beyond homocysteine/methylation exemplar.
- Governance for `supporting_biomarkers_summary` generic fallback copy.
- Stop internal names in `consumer_domain_scores.evidence_anchor_sentence` and hero alignment (coordinate with domain narrative compiler).
- Optional: expose `scientific_class` display labels in SSOT for frontend map.
- Tests: publish enablement across ≥2 fixture panels; Sentinel on placeholder supporting summary when signals missing.

**Not in FE-R5A:** Knowledge Bus bulk expansion, scoring changes, compiler rewrites, Gemini.

---

## 13. Acceptance criteria for next sprint

### FE-R5A (frontend)

- [ ] “Patterns across your body” appears in retail journey order (test id between uncertainty and marker evidence).
- [ ] Section renders only from `interpretation_display_layer_v1` enabled records.
- [ ] Each card shows: retail label, subtitle, why-it-matters, supporting markers summary, severity chip, scientific-class chip.
- [ ] No cluster name strings in pattern section DOM (static regression).
- [ ] Section omitted when zero enabled IDL rows.
- [ ] FE-R1/R2/R3 guards remain green.

### PATTERN-C1 (contract/content)

- [ ] Documented mapping: insight_graph signals → enabled `ph_*` rows for AB + at least one non-HCY panel fixture.
- [ ] `evidence_anchor_sentence` / hero no longer surfaces raw cluster/signal names on audited fixture.
- [ ] IDL registry entries reviewed for `frontend_allowed_term` and subtitle quality.
- [ ] Sentinel guards for generic supporting-marker placeholder abuse.

---

## 14. Final decision

| Question | Answer |
|----------|--------|
| Is Section 5 a **frontend-only** sprint today? | **No** — limited frontend (FE-R5A) is viable, but taxonomy presentation and cross-panel stability need PATTERN-C1. |
| Is a governed pattern-display layer present? | **Yes** — BE-IDL-1 + KB YAML + publish pipeline. |
| Can we implement v6 Section 5 on `clusters[]`? | **No** — naming unsafe. |
| Verdict | **GO WITH CONDITIONS** |
| Authorised next step | **FE-R5A** (IDL retail surfacing) in parallel planning with **PATTERN-C1** (contract/content); do **not** start FE-R5 until FE-R4 audit is merged and human approves. |

**Explicit non-decisions (FE-R4):**

- No frontend, backend, KB, or Sentinel code changes in this sprint.
- No merge to `main` performed by Cursor.
- No FE-R5 implementation authorisation — audit output only.

---

*Cursor produces audit/specification only. Cursor does not self-certify pattern-layer readiness, merge readiness, or permission to begin FE-R5.*
