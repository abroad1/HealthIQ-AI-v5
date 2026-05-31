# PROGRAMME-STATUS-1 — HealthIQ Launch Workstream Consolidation Audit

**work_id:** `PROGRAMME-STATUS-1_healthiq_launch_workstream_consolidation_audit`  
**Authored by:** Claude (claude-sonnet-4-6) — repo-grounded read-only investigation  
**Generated:** 2026-05-31  
**Mode:** Audit only — no production code, schema, test, package, or medical content modified.

---

## 1. Executive Summary

### What is complete

- **Day-one architecture guardrail stream (ARCH-RT-6)** — closed and accepted for Wave 1 launch. `validate_day_one_architecture.py` + `sentinel/packs/day_one_architecture_guardrails_v1.json` enforce card evidence routing, hypothesis promotion rules, signal identity, provenance classification, PSI runtime isolation, and no raw Pass 3 reads. All 7 Wave 1 subsystems consume compiled artefacts; legacy hard-code fallback is empty (`estate_index_v1.yaml` line 47: `subsystem_ids: []`).
- **Wave 1 compiled card estate (ARCH-RT-5)** — 7 compiled health-system cards + 1 compiled hypothesis (`signal_vitamin_d_low`) delivered, classified, and manifested. 186 packages classified (provenance tier documented).
- **Launch-core proving slice (LC-S1–S9, LAUNCH-CORE-0/1/1B/5)** — card coherence/consumer copy validated, post-fix UAT passed, results journey restructuring complete. LAUNCH-CORE-5 (2026-05-30) resolved the 4 P0 UX problems from the LAUNCH-CORE-4 audit: primary finding now before Health Systems Cards, stale/incompatible banner corrected, marker numeric scores hidden by default, consumer labels retail-ready.
- **Layer B → Layer C boundary** — formally decided in pre-sprint1 pack §3.9. `NarrativePayloadV1`, `NarrativeSectionIntentV1`, and ADR WP2 Path B exist as the typed handoff scaffold. Layer C correctly defaults to `deterministic_mock`; Gemini path guarded by `validate_llm_output_v2`.
- **Result immutability policy (LAUNCH-CORE-3)** — documented; stale/incompatible detection metadata present on GET response.
- **Bounded launch product definition** — `TRANSFORMATION_PROGRAMME_BRIEF_2026-05.md` §3–4 clearly scopes what must work at launch vs what is deferred. Alignment is real and actionable.

### What is partially complete

- **Day-one architecture programme as a whole** — launch slice accepted; §H completion criteria in `healthiq_day_one_architecture_rework_sprint_plan_FINAL_updated.md` still lists explicit provenance, activation-compile authority, multi-frame root-cause, PSI decision-or-wire, and estate-wide research→runtime traceability as unresolved or classified-deferred.
- **Pass 3 / package medical intelligence utilisation** — signal activation uses governed packages; but hypotheses, contradiction markers, `relationship_kind`, per-marker role/rationale, and `explanation.*` prose are largely not consumed by Health Systems Cards, subsystem evidence, IDL, or the report compiler. Rich Pass 3 content exists in repo but is offline at the product surface (`PASS3_research_asset_utilisation_investigation_cursor.md` verdict: "only partially using Pass 3").
- **Health systems / subsystem medical model alignment** — 7 compiled subsystems with marker roles exist and are guarded. However the medical review target (`healthiq_wave1_health_systems_subsystem_medical_review.md`) is not yet reflected in compiled artefacts or assembler logic: homocysteine pathway is `scored_subsystem` but medical review recommends hide/defer; vascular strain is `contextual_evidence` (visible) but medical review recommends hide/defer; both liver subsystems are scored but medical review recommends a flat unscored evidence group. `visibility_tier` field exists on compiled YAML and DTO but is not filtered in `domain_score_assembler.py` or frontend.
- **Layer B narrative brief richness** — `NarrativePayloadV1` provides schema scaffolding and default section intents; per-section governed intent at the §3.9 groups 4–5 depth (section-specific wording boundaries, hypothesis set constraints per section, personalisation-driven narrative branching) is not yet implemented in the payload builder.
- **Results-page narrative quality** — structural journey correct (post LC-5); score-family competition, hero/body-overview duplicate framing, and partial-data score confusion remain. These are upstream-driven issues, not layout problems.

### What is still immature

- **Full medical intelligence on user-facing cards** — subsystem rows are marker checklists only; Pass 3 hypothesis ranking, contradiction logic, mechanism prose (`explanation.*`), and marker relationship semantics are stranded in packages and Pass 3 JSON, not surfaced on cards or reports.
- **Thin subsystem trust model** — CRP-only vascular strain, homocysteine-only pathway, insulin-resistance context with triglycerides-only: all flagged as trust risks in the medical review. Still scored and visible.
- **LLM narrative translation** — production defaults to `deterministic_mock`. Gemini path exists but is not launch-ready as a governed translation layer. Blocked on Layer B brief maturity and subsystem model stability.
- **Regeneration / versioned results** — policy locked (LAUNCH-CORE-3); content hashes, `result_version_id`, and estate stamps are largely absent from live DTOs per LAUNCH-CORE-3 metadata table.
- **Cross-section narrative coherence guards** — `LAUNCH_GRADE_ANALYTICAL_GAP_MAP_2026-05.md` Gap 2 (coherence guarantee) and Gap 3 (combination-case coherence: iron+inflammation, thyroid+lipid) have no regression guards.

### What is blocked

- **Estate-wide explicit `source_spec_id`** — classified deferred; no explicit manifest field on any of 186 packages (`ARCH-RT-5D_unresolved_provenance_register.md` item RT5D-EXP-001).
- **142 batch JSON packages (kb52c + other cohorts)** — `batch_json_blocked_pending_spec_extraction`; frame IDs buried in JSON; no compiler yet. Not launch-blocking for current Wave 1 slice.
- **PSI runtime wiring** — explicitly `deferred_non_launch_blocker` (ARCH-RT-5E); loader exists for validation only.
- **Multi-frame root-cause promotion** — blocked pending frame-selection policy (ARCH-RT-5C, ARCH-RT-6).
- **LLM narrative design (F)** — blocked on Layer B brief maturity and subsystem model stability.

### What should be worked on next

**Primary: C — health systems/subsystems medical review completion.**
The governed medical target exists in `healthiq_wave1_health_systems_subsystem_medical_review.md` but is not yet reflected in compiled artefacts, assembler logic, or frontend surfacing. Thin subsystems erode product credibility. This is the highest trust-per-effort lever before launch.

**Immediately after C: B — research intelligence utilisation audit/fix**, scoped to compiling Pass 3 richness (roles, rationales, mechanism prose) into governed card/subsystem DTO fields — not raw runtime reads.

---

## 2. Programme Completion Matrix

### Programme 1 — Day-One Re-Architecture Programme

| Field | Assessment |
|-------|------------|
| **Original intended purpose** | Move from fragmented research/runtime architecture to a governed research → compile → runtime → DTO → frontend path before launch. Authority: `HealthIQ_As-Is_to_Day-One_Architecture_Transition_Plan_v3.md`, `healthiq_day_one_architecture_rework_sprint_plan_FINAL_updated.md`. |
| **Key sprint/work IDs found** | ARCH-RT-0 through ARCH-RT-6; ARCH-RT-5B/5C/5D/5E; LAUNCH-CORE-3; WAVE1-EQUIV1; DOMAIN-UX1A–1D. |
| **Key artefacts found** | `docs/audit-papers/ARCH-RT-6_day_one_architecture_acceptance_audit.md`, `docs/audit-papers/active_intelligence_authority_manifest.md`, `knowledge_bus/compiled/estate_index_v1.yaml`, `backend/scripts/validate_day_one_architecture.py`, `sentinel/packs/day_one_architecture_guardrails_v1.json`, ADR-RT-001–003, ARCH-RT-5* audit series, `docs/audit-papers/ARCH-RT-5D_unresolved_provenance_register.md`. |
| **Implementation status** | Launch slice complete: 7 compiled card artefacts, 1 compiled hypothesis, classified package provenance (186 packages), programmatic validator, Sentinel pack. Carry-forward items (activation-compile authority, estate-wide explicit provenance, multi-frame root-cause, PSI) remain open or deferred with documented rationale. |
| **Guardrail status** | **Strong for Wave 1 launch slice.** 6 rule groups enforced by `validate_day_one_architecture.py` (lines 69–200) + architecture regression tests + Sentinel JSON. Checks cover: card estate routing, compile manifest integrity, compiled hypothesis promotion, provenance classification, PSI isolation, runtime research-read prohibition. |
| **Open risks** | Dual authority paths (legacy root-cause YAML ~40 signals vs compiled hypothesis); 5 card markers with inferred-only provenance (RT5D-CARD-001–005); 142 batch JSON packages unextracted; CRP still via legacy `pkg_s24_crp_high_inflammation`. |
| **Launch impact** | **Non-blocking** for bounded Wave 1 pilot with deferred register accepted. **Blocking** for "day-one fully delivered" or estate-wide regeneration claims. |
| **Completion rating** | **Mostly complete** (launch slice) / **Partially complete** (§H programme completion criteria) |
| **Evidence** | ARCH-RT-6 verdict: `accepted_for_wave1_launch`. `estate_index_v1.yaml` subsystem_ids: `[]`. Carry-forward register §A–H still lists 9 criteria, not all satisfied. |
| **Recommended next action** | Dedicated **legacy architecture cleanup / classification sprint (A)** after medical model (C) — retire or reclassify dual-path modules, close RT5D register items tied to launch-critical claims. |

---

### Programme 2 — Full Medical Intelligence Utilisation (Pass 3 / Packages)

| Field | Assessment |
|-------|------------|
| **Original intended purpose** | Ensure governed research assets (Pass 3 investigation specs → packages → runtime) deliver full medical intelligence to product surfaces, not just signal activation thresholds. |
| **Key sprint/work IDs found** | KB-S52* ingest tranche; PASS3 investigation (`PASS3_research_asset_utilisation_investigation_cursor.md`); proposed `KB-S63`; ARCH-R1 review; ARCH-RT-5B card evidence. |
| **Key artefacts found** | 9 `*_Pass_3.json` files (153 specs total); 186 packages in `knowledge_bus/packages/`; `promoted_signal_intelligence.yaml` (KB47 subset, unused at runtime); `PASS3_research_asset_utilisation_investigation_cursor.md`; `ARCH-R1_research_asset_to_runtime_intelligence_architecture_review_cursor.md`. |
| **Implementation status** | **Pass 3 → packages:** moderate for signal logic (~132 of 186 cite Pass 3 lineage; `supporting_metrics[]` role/rationale preserved in 2.0.0 packages). **Lost in standard package path:** hypotheses[], contradiction_markers, hypothesis_ranking, relationship_kind, missing-data policies, confirmatory test rationales. **Packages → runtime:** partial — evaluator uses activation/overrides/confidence; `explanation.*` stored in insight graph but not consumed by Health Systems Cards, subsystem evidence, or report compiler. `SubsystemEvidenceV1.evidence_role` is always null. PSI not consumed. CRP still from legacy `pkg_s24_crp_high_inflammation`, not dedicated Pass 3 specs. |
| **Guardrail status** | Package schema validation and day-one validator prevent raw Pass 3 runtime reads. **No guard** enforcing that card surfaces consume available package richness. |
| **Open risks** | Duplicate `signal_id` last-wins policy in evaluator; 44 legacy 1.0.0 packages (flat string lists, no structured roles/rationale); CRP signal bypasses newer Pass 3 frames entirely; `relationship_kind` exists in KB47 PSI but is runtime-dead. |
| **Launch impact** | Product under-delivers on research investment at card surfaces. Trust risk when UI implies clinical specificity that the surfaced evidence does not support. Not a runtime safety blocker if signals fire correctly. |
| **Completion rating** | **Partially complete** |
| **Evidence** | PASS3 audit §1 verdict: "only partially using Pass 3." Runtime table (PASS3 audit §4): `explanation.*` stored-only; `evidence_role` always null; `relationship_kind` dead. CRP signal still from legacy s24 package. |
| **Recommended next action** | **B — research intelligence utilisation sprint:** extend governed compile artefact (card evidence v2 or subsystem compile) to carry Pass 3 / 2.0.0 `explanation.*`, marker roles, and visibility policy into DTO fields; wire consumption in Layer B assemblers — not frontend. Do not read raw JSON in orchestrator. |

---

### Programme 3 — Wave 1 Health Systems / Subsystem Medical Review

| Field | Assessment |
|-------|------------|
| **Original intended purpose** | Define medically safe v1 subsystem visibility — which subsystems may be scored vs contextual vs hidden; establish marker role taxonomy; specify liver flat card; rename lipid subsystem. Authority: `healthiq_wave1_health_systems_subsystem_medical_review.md`. |
| **Key sprint/work IDs found** | DOMAIN-UX1A, 1A-PATCH, 1B, 1C, 1D; ARCH-RT-3/5B; WAVE1_subsystem investigations; MAP-R1A bilirubin fix. |
| **Key artefacts found** | `docs/audit-papers/healthiq_wave1_health_systems_subsystem_medical_review.md`, compiled cards under `knowledge_bus/compiled/health_system_cards/` (7 YAML files), `backend/core/knowledge/health_system_card_evidence.py`, `backend/core/analytics/wave1_subsystem_evidence.py`, `docs/audit-papers/WAVE1_subsystem_coverage_and_marker_role_codebase_investigation_cursor.md`. |
| **Implementation status** | **Implemented in code** — 7 compiled subsystems with marker lists. **Not aligned with medical review:** homocysteine pathway remains `scored_subsystem` (medical review: hide/defer); vascular strain is `contextual_evidence` but still visible (medical review: hide/defer); both liver subsystems are scored (medical review: single flat unscored evidence group); lipid subsystem label still "Lipid transport" (medical review: rename to "Atherogenic lipid pattern"); insulin-resistance context scored (medical review: hide unless richer markers). `visibility_tier` exists on compiled YAML and DTO but is **not consumed** in `domain_score_assembler.py` or any frontend component. |
| **Guardrail status** | DOMAIN-UX1A–1D Sentinel guards prevent frontend-invented roles; day-one validator requires compiled routing. **No guard** enforcing medical review visibility policy for `visibility_tier`. |
| **Open risks** | Over-trust in thin subsystems (CRP-only, homocysteine-only, TG-only); liver biology oversimplified across two scored subsystems; domain completeness score vs visible subsystem marker count mismatch; `total_bilirubin` false-missing fix protected by ARCH-RT-6 validator but underlying alias equivalence not surfaced to users as a clear explanation. |
| **Launch impact** | **High trust risk.** UI implies clinical specificity beyond marker support for vascular strain, homocysteine pathway, and liver subsystems. LAUNCH-CORE-1B passed card coherence but noted IDL "Vascular Inflammation Risk" label persists in IDL layer. |
| **Completion rating** | **Partially complete** (engineering) / **Immature** (medical alignment with review recommendations) |
| **Evidence** | Medical review §6–9 vs compiled YAML: `wave1_cv_homocysteine_pathway.yaml` scored; `wave1_cv_vascular_strain.yaml` visible contextual_evidence; both liver YAML files scored. Grep confirms no `visibility_tier` filtering in `domain_score_assembler.py` or results page components. `SubsystemEvidenceV1.evidence_role` always null (WAVE1 investigation §9). |
| **Recommended next action** | **C — medical review completion sprint:** recompile card artefacts to medical v1 visibility model; enforce `visibility_tier` filtering in Layer B assembler; rename consumer labels; collapse liver to flat card with evidence groups only. |

---

### Programme 4 — Frontend Results Ordering and Narrative

| Field | Assessment |
|-------|------------|
| **Original intended purpose** | Deliver a coherent guided reasoning journey: primary finding → why → confidence → systems → evidence → next steps; govern score hierarchy; prepare for optional LLM translation without Layer C reasoning. Authority: `HealthIQ_Final_Results_Journey_Recommendation_Paper_v6`, pre-sprint1 pack §3.9. |
| **Key sprint/work IDs found** | LC-S3 (Layer C payload), LC-S4–S7, LAUNCH-CORE-0/1/1B/4/5; FE-R0–R6A; DOMAIN-UX1*. |
| **Key artefacts found** | `frontend/app/(app)/results/page.tsx`, `LAUNCH-CORE-4_results_page_narrative_hierarchy_and_score_rationalisation_audit.md`, `LAUNCH-CORE-5` (just closed 2026-05-30), `LAUNCH_GRADE_ANALYTICAL_GAP_MAP_2026-05.md`, `docs/intelligence/DOMAIN_NARRATIVE_CONTRACT_WAVE1.md`. |
| **Implementation status** | **Current journey order (post LAUNCH-CORE-5):** Hero+body-overview → Primary finding → Working well → Health Systems Cards → Confidence/trust strip → Patterns → Marker evidence → Next steps. Major FE-R1 backend prose fixes merged. Layer C consumer labels retail-ready. Stale/incompatible banner corrected. Marker scores hidden by default. **Remaining:** score-family competition (6+ score families visible), hero/body-overview duplicate framing (P2 carry-forward from LC-5), partial-data 100/100 blood sugar tension, IDL pattern layer not wired (deferred; BE-IDL-1 not built). |
| **Guardrail status** | FE-R1 Sentinel classes; LC-S11A trust blockers; slug leakage regression. ARCH-RT-6 validator passes post LC-5. **Weak** on cross-section coherence and score precedence. LAUNCH_GRADE_ANALYTICAL_GAP_MAP gaps 2–3 have no regression guards. |
| **Open risks** | Continuing to polish layout before subsystem medical model is stable risks encoding the wrong subsystem story (e.g., scored homocysteine) that must be reworked after C. Deterministic prose still depends on IDL labels that backend has not fully retail-normalised. |
| **Launch impact** | **Non-blocking for pilot** with known reservations; **blocking for premium consumer credibility** at scale without further upstream model work. |
| **Completion rating** | **Partially complete** — journey structure correct; content and hierarchy policy still upstream-limited |
| **Evidence** | LAUNCH-CORE-5 gate: PASS (2026-05-30). LAUNCH-CORE-4: "PASS WITH RESERVATIONS." `page.tsx` L701–732 confirms new order. LAUNCH_GRADE_ANALYTICAL_GAP_MAP gaps 2–3 open. |
| **Recommended next action** | **E — results-page UX redesign** only **after C + partial B + score rationalisation spec**. Limited FE copy/order tweaks safe now; full redesign is downstream of upstream model stability. |

---

## 3. Dependency Map

```
A [Day-one architecture guardrails] ──► B [Pass 3 / package utilisation]
                                              │
                                              ▼
                                        C [Medical subsystem model]
                                              │
                                    ┌─────────┴──────────┐
                                    ▼                    ▼
                              D [Layer B                E [Results page
                               narrative brief]          UX hierarchy]
                                    │
                                    ▼
                              F [LLM narrative
                               translation design]

A ──► H [Legacy pathway retirement]
H ──► B (safer to retire after medical model locked)

G [Regeneration/versioned flow] depends on: A (stable) + E (stable hierarchy)
```

### Cross-Cutting Dependency Answers

| Question | Answer |
|----------|--------|
| **Can results-page narrative work continue safely before full research intelligence utilisation is confirmed?** | **Limited yes, full no.** Order/scrub/deduplication (FE-R*, LAUNCH-CORE-4/5) can proceed without full Pass 3 utilisation. But subsystem/card narrative quality is capped until research richness is compiled into DTOs (B). Risk: a UX sprint that encodes the wrong subsystem story (e.g., scored homocysteine) will need rework after C/B. |
| **Can UX polish continue before subsystem medical review / core-support model is confirmed?** | **No for card/subsystem surfaces.** Polishing hero and journey order is safe; changing card prominence, labels, or subsystem expansion should wait for C. Medical review §10 explicitly prescribes architecture-first sequence. |
| **Can LLM narrative translation be designed before Layer B narrative brief maturity is confirmed?** | **No.** §3.9 groups 4–5 (per-section intent, wording boundaries, personalisation branching) are prerequisites. `NarrativePayloadV1` is a scaffold, not a mature brief. F is **blocked** until D completes. |
| **Are old architecture pathways sufficiently retired/guarded?** | **Partially.** Day-one validator blocks new drift and raw Pass 3 reads; legacy root-cause YAML (~40 signals), dual loader paths, 142 batch packages, and legacy s24 signals for CRP remain **reachable but classified**. Unguarded product risk is medical over-surfacing of thin subsystems, not silent wrong signal firing. A dedicated cleanup sprint (A) is warranted but not as urgent as C. |

---

## 4. Research Intelligence Utilisation Assessment

| Question | Answer |
|----------|--------|
| **Are the rich Pass 3 research files used by runtime artefacts?** | **No directly.** Pass 3 JSON is ingest/audit source only. Runtime loads `signal_library.yaml` / packages and compiled card YAML — never `*_Pass_3.json`. |
| **Are package files using the full research richness or only a subset?** | **Subset.** Activation thresholds, supporting metric lists, research_brief citations, and merged `explanation.*` are preserved in 2.0.0 packages. **Lost in standard package path:** hypotheses[], contradiction_markers, hypothesis ranking, relationship_kind, missing-data policies, confirmatory tests. Legacy 1.0.0 packages (44 of 186) have flat string lists only — no per-marker role or rationale. |
| **Is the package/compiled artefact pipeline now authoritative?** | **Yes for Wave 1 launch slice.** `estate_index_v1.yaml` and `active_intelligence_authority_manifest.md` declare compiled card evidence and one compiled hypothesis as launch authority; validator enforces. **Not authoritative for full 153-spec estate** — 142 batch JSON packages blocked; legacy s24 CRP path remains active. |
| **What richness is stranded in source research files?** | Ranked hypotheses, contradiction logic, relationship_kind semantics, missing-data policies, confirmatory test rationales, mechanism/pathway/implications prose (`explanation.*`), PSI overlay (20 KB47 packages, runtime-dead), per-marker role tags (`evidence_role` always null at runtime). |
| **What must be done before claiming full medical intelligence utilisation?** | (1) Governed compile from Pass 3 / 2.0.0 packages → card/subsystem DTO with roles, rationales, visibility tiers. (2) Resolve duplicate `signal_id` last-wins policy. (3) Migrate legacy s24 CRP signal to dedicated Pass 3 specs. (4) Wire `explanation.*` consumption in Layer B assemblers — not frontend. (5) PSI join only if launch-critical and provenance-safe. |

**Evidence anchors:** `PASS3_research_asset_utilisation_investigation_cursor.md` §1–4; `ARCH-R1_research_asset_to_runtime_intelligence_architecture_review_cursor.md`; `active_intelligence_authority_manifest.md` PSI table.

---

## 5. Health Systems / Subsystems Medical Review Assessment

| Question | Answer |
|----------|--------|
| **Are core and support systems medically reviewed?** | **Yes** — comprehensive review in `healthiq_wave1_health_systems_subsystem_medical_review.md`. |
| **Are they implemented in code?** | **Partially** — 7 compiled subsystems with marker lists exist; implementation **diverges** from visibility tier recommendations. |
| **Are they surfaced correctly to users?** | **No.** Medical review recommends only **one scored CV subsystem** (atherogenic lipid), one scored glycaemic subsystem, and a **flat liver card**. Current UI surfaces three CV + two metabolic + two liver subsystems with visible scores or evidence rows. |
| **Are support systems being over-surfaced?** | **Yes** — homocysteine pathway scored; vascular strain contextual but visible; insulin/metabolic context with TG-only; liver processing context scored. |
| **Are any user-facing body system cards medically immature?** | **Yes** — CRP-only vascular strain, homocysteine-only pathway, TG-only insulin-resistance context, liver processing context (mixed biology), blood sugar with 2 of 4 expected markers showing 100/100 score tension. |
| **Does the results page expose system/subsystem logic before clinical/narrative maturity?** | **Yes** — Health Systems Cards are in the main journey with expandable subsystem evidence before medical model alignment is complete. |

### Medical Review vs Compiled Artefact Gap Table

| Subsystem | Medical review recommendation | Current compiled state | Alignment |
|-----------|-------------------------------|------------------------|-----------|
| CV — Lipid transport | Scored; rename to "Atherogenic lipid pattern" | `scored_subsystem`; label still "Lipid transport" | **Label gap only** |
| CV — Homocysteine pathway | Hide/defer; contextual only | `scored_subsystem` | **Misaligned** |
| CV — Vascular strain | Hide/defer; contextual only | `contextual_evidence` (still visible) | **Misaligned** |
| Blood sugar — Glycaemic control | Scored with caveats | Scored | **Aligned** |
| Blood sugar — Insulin/metabolic | Hide unless richer markers | `scored_subsystem` (TG-only) | **Misaligned** |
| Liver — Enzyme pattern | Evidence group, not scored | `scored_subsystem` | **Misaligned** |
| Liver — Processing context | Merge/hide; not scored | `scored_subsystem` | **Misaligned** |

**`visibility_tier` enforcement status:** Field exists in compiled YAML and `SubsystemEvidenceV1` DTO type. **Not filtered or consumed** in `domain_score_assembler.py` or any frontend component (confirmed by grep). All subsystems reach the UI regardless of tier.

---

## 6. Results-Page Narrative Assessment

*Does not repeat the LAUNCH-CORE-4/5 UX audit. Focuses on upstream dependency drivers.*

### Primary Drivers of Poor Narrative (Ranked by Root Cause)

| Driver | Weight | Evidence |
|--------|--------|----------|
| **Incomplete system/subsystem medical review (C)** | **High** | Cards interrupt story with medically thin scored subsystems; contributor copy repeats vascular/homocysteine themes for single-marker signals. |
| **Incomplete medical intelligence utilisation (B)** | **High** | Subsystem sections show marker chips with no mechanism, contradiction context, or hypothesis rationale — all of which exist in Pass 3/packages but are offline at the card surface. |
| **Layer B narrative assembly duplication** | **Medium–High** | Multiple surfaces emit the same lead pattern (hero, body overview, primary finding, IDL patterns); backend duplication partially addressed by FE-R1 but not fully resolved at source. |
| **Too many analytical surfaces exposed at once** | **Medium** | System scores, domain scores, marker scores, severity badges, completeness metrics, IDL patterns — score inventory from LAUNCH-CORE-4 is still largely valid despite LC-5 improvements. |
| **Missing narrative brief contract depth (D)** | **Medium** | `NarrativePayloadV1` provides intent enum and claim boundary scaffold but not per-section governed intent or wording constraint at §3.9 groups 4–5 richness. |
| **Deterministic hard-coded prose limitations** | **Medium** | IDL retail labels and narrative compiler templates still produce internal-adjacent copy; frontend scrub masks rather than eliminates. |
| **Frontend layout** | **Lower** | FE-R2/LC-5 fixed major ordering bug; remaining issues are content, hierarchy policy, and upstream model — not component absence. |

### Summary Verdict

Poor narrative is **not primarily a frontend layout problem**. Section order is now correct (post LC-5). The remaining weakness is the **upstream truth model** — thin subsystem scores creating false clinical specificity, analytical surfaces competing rather than converging, and deterministic prose limited by an incomplete medical intelligence compile. Frontend scrub is a temporary shield, not a fix.

---

## 7. Legacy Architecture Cleanup Assessment

### Classification Register

| Category | Items | Notes |
|----------|-------|-------|
| **Deleted** | None confirmed at scale in this audit pass | Programme approach: classify-over-delete |
| **Retained but unreachable at runtime** | Raw Pass 3 JSON (blocked by validator); PSI loader in production orchestrator (not imported on live paths) | **Guarded** |
| **Retained and explicitly classified** | 186 packages (ARCH-RT-5D register); deferred PSI; 142 batch JSON packages; legacy root-cause YAML (~40 signals); compiled hypothesis (1 promoted) | `ARCH-RT-5D_unresolved_provenance_register.md`, `active_intelligence_authority_manifest.md` |
| **Guarded by validator/Sentinel** | Card evidence routing, no raw Pass 3 reads, compile manifest refs, frontend subsystem isolation (DOMAIN-UX1D), day-one architecture pack | **Strong for Wave 1 launch slice** |
| **Still reachable** | Legacy `load_root_cause_hypotheses.py` YAML path (~40 signals); CRP signal still via legacy `pkg_s24_crp_high_inflammation`; duplicate `signal_id` last-wins in evaluator; 5 card markers with inferred-only provenance (RT5D-CARD-001–005) | **Classified but active** |
| **Unguarded risk** | `visibility_tier` not enforced downstream; thin subsystem medical over-surfacing; hero/body-overview duplicate framing (P2 carry-forward); `incompatible` result flow not fully regression-guarded | **Product/trust risk — not silent engine corruption** |

### Dedicated Cleanup Sprint Needed?

**Yes — audit-first, then targeted implementation (A), sequenced after C.** ARCH-RT-6 prevents new drift but does not retire dual authority paths. Recommended scope: inventory all reachable legacy paths → classify retire/defer with rationale → remove CRP s24 legacy once dedicated Pass 3 spec is authored → close RT5D batch extraction programme or permanently defer with a user-facing scope statement → retire `wave1_subsystem_evidence.py` fallback once visibility tier enforcement is in place.

---

## 8. Layer Architecture Readiness

| Layer | Intended role | Readiness | Evidence |
|-------|---------------|-----------|----------|
| **Layer A — Governed medical intelligence inputs** | SSOT, packages, Pass 3 compile, canonical biomarkers | **Mostly ready for Wave 1 launch slice** | 186 packages classified; 7 compiled card artefacts; 1 compiled hypothesis; unit governance LC-S8*; provenance tiered |
| **Layer B — Interpretation, prioritisation, narrative planning, DTO shaping** | AnalysisDTO, narrative payload, root cause, domain scores, clinician report | **Partially ready** | Rich DTO exists; `NarrativePayloadV1` scaffold present; subsystem/medical model not final; `visibility_tier` not consumed; narrative brief groups 4–5 incomplete |
| **Layer C — Presentation/rendering only** | Frontend render, deterministic narrative compiler, optional LLM translation | **Mostly compliant for deterministic path** | FE-R1/R2/LC-5 complete; AGENTS.md frontend-shell rules in place; mock-mode disclosure present; Layer C correctly does not perform LLM reasoning in production default |

### LLM Narrative Readiness

| Question | Answer |
|----------|--------|
| **Is Layer B producing a sufficiently governed narrative brief?** | **Not yet.** `NarrativePayloadV1` provides intent enum and claim boundary model; per-section rich governed intent (wording constraints, hypothesis-set linkage, personalisation branching) is not yet implemented in the payload builder. |
| **Is the LLM role defined in existing docs?** | **Yes** — pre-sprint1 pack §3.9, strategy v1.5, ADR WP2 Path B: translation-only; `validate_llm_output_v2` guard; production defaults to `deterministic_mock`. |
| **What must exist before LLM translation is wired?** | Mature Layer B brief (§3.9 groups 1–5 complete); subsystem medical model stable; validator extended for ranking/hypothesis/wording preservation; explicit product decision to enable Gemini path; regeneration/version stamps for safe replay. |
| **Layer C must not perform LLM reasoning** | **Confirmed as current policy.** Production path uses deterministic compilers + frontend scrub. Risk is a future sprint bypassing the payload contract — guard via D + validator review before any Gemini enablement. |

---

## 9. Recommended Prioritised Roadmap

| Order | work_id suggestion | Purpose | Why next | Dependencies | Risk | Type |
|-------|--------------------|---------|----------|--------------|------|------|
| **1** | `MED-REV-1_wave1_subsystem_visibility_and_label_alignment` | Implement medical review v1: enforce `visibility_tier` in Layer B; collapse/hide thin subsystems; rename labels; collapse liver to flat card | Stops trust erosion from thin scored subsystems; unblocks honest card UX; highest trust-per-effort lever | Medical review doc; compiled card YAML; `domain_score_assembler.py` | STANDARD | Implementation |
| **2** | `KB-UTIL-1_pass3_card_evidence_compile_and_consume` | Compile Pass 3 / pkg richness (roles, rationales, mechanism prose) into governed card DTO; consume in Layer B assemblers | Delivers research ROI on cards; depends on stable visibility model from 1 | MED-REV-1; PASS3 audit; 2.0.0 packages | STANDARD | Implementation |
| **3** | `LAYER-B-1_narrative_brief_maturity` | Complete §3.9 groups 4–5 in `NarrativePayloadV1` builders; wire into narrative compiler; extend `validate_llm_output_v2` | Prerequisite for LLM; reduces duplicate prose surfaces; enables coherence guards | KB-UTIL-1 partial; clinician report stable | STANDARD | Implementation |
| **4** | `ARCH-LEGACY-1_pathway_retirement_audit` | Classify and retire dual paths: legacy root-cause YAML migration plan; CRP s24 legacy; batch JSON scope closure | Reduces long-term drift; safe after medical model locked | ARCH-RT-6 baseline; MED-REV-1 complete | STANDARD | Audit then implementation |
| **5** | `LAUNCH-UX-2_results_hierarchy_and_score_rationalisation` | Score precedence policy; deduplicate metrics; hero/body-overview duplicate fix; full stale/incompatible regression suite | Symptom fix **after** upstream model stable; completes LAUNCH-CORE-4 backlog | MED-REV-1; LAYER-B-1 partial | STANDARD | Implementation |
| **6** | `LLM-NAR-0_translation_design_audit` | Design-only: Gemini envelope, validator contract extension, rollout gates | Must not be implemented before 3 | LAYER-B-1 | LOW | Audit-only |
| **7** | `LAUNCH-CORE-6_versioned_regeneration_implementation` | Behaviour C from LAUNCH-CORE-3: regen job, version rows, estate stamps | After analytical surfaces stable; avoid regenerating bad UX | LAUNCH-UX-2; content hash policy | STANDARD | Implementation |

**Sequencing principle:** Do not run **E (full UX redesign)** or **F (LLM design/wire)** before **C → B → D**. Do not run **G (regeneration)** before the user-visible hierarchy stabilises. Do not run **A (legacy cleanup)** before the medical model is locked — retiring dual paths while medical model is in flux risks removing the wrong authority.

---

## 10. Key Decision: Recommended Next Sprint

### Recommended: **C — Health Systems/Subsystems Medical Review Completion**

| Option | Recommendation | Rationale |
|--------|----------------|-----------|
| **A. Legacy architecture cleanup** | **4th** — after C completes | Guardrails exist; cleanup important but not the highest trust lever; sequencing before C risks retiring assets still needed |
| **B. Full research intelligence utilisation** | **2nd** — immediately after C | Cannot safely compile Pass 3 richness onto a misaligned subsystem visibility model |
| **C. Medical review completion** | **NEXT — do this first** | Governed target exists; implementation diverges; thin subsystems erode credibility on every user session; blocks B, constrains E |
| **D. Layer B narrative brief** | **3rd** | Prerequisite for LLM; reduces prose duplication; safely deferred until subsystem truth is stable |
| **E. Results-page UX redesign** | **5th — limited polish only until C/B/D progress** | LAUNCH-CORE-4/5 issues are mostly upstream-driven; full redesign before model stability is wasted effort |
| **F. LLM narrative translation design** | **6th — audit-only first** | Blocked on D; policy is clear, implementation is premature |
| **G. Regeneration/versioned result flow** | **7th** | Policy done (LAUNCH-CORE-3); implementation should not preserve a hierarchy that will be redesigned after C/B/D |

---

## 11. Key Repo Artefacts Index

### Day-one / Architecture
- `docs/planning-papers/HealthIQ_As-Is_to_Day-One_Architecture_Transition_Plan_v3.md`
- `docs/sprints/healthiq_day_one_architecture_rework_sprint_plan_FINAL_updated.md`
- `docs/audit-papers/day_one_architecture_launch_readiness_audit.md`
- `docs/audit-papers/ARCH-RT-6_day_one_architecture_acceptance_audit.md`
- `docs/audit-papers/active_intelligence_authority_manifest.md`
- `docs/architecture/ADR-RT-001_research_to_runtime_day_one_architecture.md`
- `backend/scripts/validate_day_one_architecture.py`
- `sentinel/packs/day_one_architecture_guardrails_v1.json`

### Pass 3 / Packages / Intelligence
- `docs/audit-papers/PASS3_research_asset_utilisation_investigation_cursor.md`
- `docs/architecture/ARCH-R1_research_asset_to_runtime_intelligence_architecture_review_cursor.md`
- `knowledge_bus/research/investigation_specs/multi_llm_research/*_Pass_3.json` (153 specs across 9 files)
- `knowledge_bus/packages/**` (186 packages)
- `knowledge_bus/compiled/estate_index_v1.yaml`
- `knowledge_bus/compiled/health_system_cards/*.yaml` (7 files)

### Medical Review / Subsystems
- `docs/audit-papers/healthiq_wave1_health_systems_subsystem_medical_review.md`
- `docs/audit-papers/WAVE1_subsystem_coverage_and_marker_role_codebase_investigation_cursor.md`
- `docs/audit-papers/DOMAIN-UX1A_wave1_health_systems_card_scaffold_notes.md` through `DOMAIN-UX1D_*`
- `backend/core/knowledge/health_system_card_evidence.py`
- `backend/core/analytics/wave1_subsystem_evidence.py`
- `backend/core/analytics/domain_score_assembler.py`

### Results Narrative / Frontend
- `docs/audit-papers/FE_R0_results_page_prose_source_trace_audit.md`
- `docs/audit-papers/LAUNCH-CORE-4_results_page_narrative_hierarchy_and_score_rationalisation_audit.md`
- `docs/audit-papers/LAUNCH-CORE-5_results_page_narrative_hierarchy_and_score_rationalisation_audit.md`
- `docs/audit-papers/LAUNCH_GRADE_ANALYTICAL_GAP_MAP_2026-05.md`
- `frontend/app/(app)/results/page.tsx`
- `docs/intelligence/DOMAIN_NARRATIVE_CONTRACT_WAVE1.md`

### Layer B/C / LLM
- `docs/planning-papers/healthiq_pre_sprint1_decision_pack_FINAL.md` §3.9
- `docs/planning-papers/healthiq_pre_sprint3_closure_pack_FINAL.md` §4
- `docs/architecture/ADR_WP2_layer_b_layer_c_contract_path_b.md`
- `backend/core/contracts/narrative_payload_v1.py`
- `backend/core/analytics/narrative_payload_builder_v1.py`
- `backend/core/llm/validator_v2.py`

### Legacy / Provenance / Versioning
- `docs/audit-papers/ARCH-RT-5D_unresolved_provenance_register.md`
- `docs/audit-papers/LAUNCH-CORE-3_result_versioning_replay_and_regeneration_audit.md`
- `docs/audit-papers/LAUNCH_GRADE_ANALYTICAL_GAP_MAP_2026-05.md`
- `sentinel/packs/day_one_architecture_guardrails_v1.json`

### Programme Steering
- `docs/audit-papers/TRANSFORMATION_PROGRAMME_BRIEF_2026-05.md`
- `docs/planning-papers/healthiq_launch_core_transformation_plan_FINAL.md`

---

## 12. Success Criteria Checklist

| Criterion | Met |
|-----------|-----|
| 1. All four named programmes assessed | **Yes** — §2 |
| 2. Key repo artefacts identified with file citations | **Yes** — §11 + throughout |
| 3. Completion status clearly classified per programme | **Yes** — §2 completion ratings |
| 4. Dependencies mapped | **Yes** — §3 |
| 5. Unresolved legacy architecture risk classified | **Yes** — §7 |
| 6. Research intelligence utilisation status clear | **Yes** — §4 |
| 7. Subsystem medical review status clear | **Yes** — §5 |
| 8. Next sprint priority recommended with rationale | **Yes** — §10 (C first) |
| 9. No implementation changes made | **Yes** — audit-only |

---

*End of PROGRAMME-STATUS-1 consolidation audit.*
