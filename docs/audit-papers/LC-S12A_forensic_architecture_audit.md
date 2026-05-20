# LC-S12A — Forensic Architecture Audit
**Date:** 2026-05-20
**Auditor:** Claude Code (forensic architecture mode)
**Repo:** C:\Users\abroa\HealthIQ-AI-v5

---

## 1. Executive verdict

**Grade: C+**

HealthIQ AI v5 has a genuine analytical engine that is architecturally more serious than most consumer health-tech products and substantially more serious than the codebase appeared to be one year ago. The product is worth continuing on the current codebase. It does not require a full rebuild. It does not require a major partial rebuild of the engine. It does require targeted restructuring in two specific areas that currently prevent commercial launch.

The core analytical engine — signal evaluation, root cause compiler, WHY hypothesis YAML assets, IDL bundle, arbitration engine, replay manifest — is a real foundation. The governance machinery — Automation Bus, Sentinel Phase 1, Knowledge Bus pipeline, three-layer architecture — is functioning and appropriate for the product's risk profile.

The product is blocked from commercial launch by two structural gaps, not engine gaps:

1. The questionnaire / lifestyle modifier layer computes correctly internally but produces near-zero visible user payoff. A paying user cannot detect that they filled in any questionnaire. This is not a wiring bug. It is a missing connection between internal computation and output surfaces.

2. The scoring engine's bio_stats_engine uses a symmetric z-score formula that treats clinical deviations below the reference range with identical weight to those above. This produces clinically wrong severity in one confirmed case (low ALT driving a "Needs review" liver card) and is structurally unresolved — the LC-S11A fix is a targeted `biomarker_name == "alt"` bypass in `rules.py:309-311`, not a direction-aware mechanism. Every enzyme-class biomarker where low values are benign is at risk of the same class of false alarm.

Everything else is manageable product debt that does not require architectural intervention.

---

## 2. Sources inspected

**Planning and audit documents:**
- `docs/planning-papers/healthiq_launch_core_transformation_plan_FINAL.md`
- `docs/audit-papers/LAUNCH_GRADE_ANALYTICAL_GAP_MAP_2026-05.md`
- `docs/audit-papers/LAUNCH_GRADE_ANALYTICAL_TARGET_STATE_2026-05.md`
- `docs/audit-papers/LAUNCH_GRADE_VERIFICATION_LEDGER_2026-05.md`
- `docs/audit-papers/TRANSFORMATION_PROGRAMME_BRIEF_2026-05.md`
- `automation_bus/latest_audit_summary.md` (LC-S11A audit)
- `automation_bus/latest_cursor_prompt.md` (LC-S11A sprint prompt)
- `automation_bus/latest_cursor_status.json`

**Layer B artifacts (runtime verification):**
- `docs/audit-papers/verification-2026-05-04/artifacts/AB_full_panel_with_profiles__P3_stressed/analysis_result.json`
- `docs/audit-papers/verification-2026-05-04/artifacts/AB_full_panel_with_profiles__P3_stressed/narrative.txt`
- `docs/audit-papers/verification-2026-05-04/artifacts/AB_full_panel_with_profiles__P3_stressed/layer3_insights.json`

**Backend core:**
- `backend/core/pipeline/orchestrator.py` (2,319 lines)
- `backend/core/analytics/signal_evaluator.py`
- `backend/core/analytics/root_cause_compiler_v1.py`
- `backend/core/analytics/domain_narrative_wave1.py`
- `backend/core/analytics/domain_score_assembler.py`
- `backend/core/analytics/bio_stats_engine.py`
- `backend/core/scoring/rules.py`
- `backend/core/scoring/engine.py`
- `backend/core/units/registry.py`
- `backend/core/dto/builders.py`
- `backend/ssot/biomarkers.yaml` (103 entries observed)
- `backend/ssot/lifestyle_registry.yaml`
- `backend/ssot/scoring_policy.yaml`
- `backend/scripts/run_work_package.py`
- `backend/scripts/golden_gate_local.py`
- `backend/app/routes/analysis.py`

**Frontend:**
- `frontend/app/(app)/results/page.tsx`
- `frontend/app/components/results/PrimaryFindingAndWhy.tsx`
- `frontend/app/components/insights/InsightPanel.tsx`
- `frontend/app/lib/legacyInsightsVisibility.ts`
- Directory listings: `frontend/app/components/results/`, `frontend/app/components/`, `frontend/tests/`

**Knowledge Bus:**
- `knowledge_bus/packages/pkg_homocysteine_elevation_context/signal_library.yaml`
- `knowledge_bus/root_cause/hypotheses/` (40 files listed)
- Package count: 187 directories under `knowledge_bus/packages/`

**Sentinel:**
- `sentinel/sentinel_runner.py`
- `sentinel/packs/escaped_defects_v1.json`

**Tests:**
- `backend/tests/regression/test_persisted_result_replay_status.py`
- `backend/tests/regression/test_lc_s5_proving_checks.py`
- Directory listing of all 219 backend test files and 44 frontend test files

---

## 3. Architecture map

### Ingestion / parsing
User uploads a blood panel. `backend/app/routes/analysis.py` receives the request. `BiomarkerNormalizer` and `normalize_panel` resolve aliases to canonical keys via `backend/core/canonical/`. A `CanonicalCollisionError` is raised on duplicates. HbA1c unit arbitration runs separately via `arbitrate_hba1c_layer_b_input`. Unit normalisation follows via `apply_unit_normalisation` from `backend/core/units/registry.py`, which uses YAML-defined conversion factors. Unmapped units are rejected by default (env flag `UNIT_ALLOW_UNMAPPED` required to pass them through).

### Questionnaire / context mapping
The user's questionnaire submission is mapped by `QuestionnaireMapper` into a `MappedLifestyleFactors` struct. This feeds `LifestyleModifierEngine` (which reads `lifestyle_registry.yaml` for system caps, thresholds, and modifier rules) and `compute_lifestyle_interpretation_bridges_v1` (which probes bridge conditions such as alcohol-methylation coherence). The modifier output is attached to the DTO as `lifestyle.system_modifiers` and `meta.lifestyle_interpretation_bridges_v1`. Critically, this output does NOT propagate to any user-facing field (`consumer_domain_scores`, `clinician_report_v1.sections.page1`, `narrative_report_v1.retail_summary`, `actions.interventions`). The computation is correct; the wire from computed modifiers to user-visible surfaces is absent.

### Layer B — analytical engine (orchestrator)
`AnalysisOrchestrator.run` in `orchestrator.py` (2,319 lines) orchestrates 45+ sub-engines in a fixed sequence. The architecture is a long procedural pipeline, not a pluggable DAG. The core flow is:

1. Canonicalisation and unit normalisation (complete)
2. `ScoringEngine.score` — scores each biomarker using lab-supplied reference ranges; scoring policy YAML is only used for derived ratios (correct design)
3. `SignalRegistry._load` — scans all `knowledge_bus/packages/*/signal_library.yaml` files and loads signal definitions; `SignalEvaluator` applies them
4. `build_insight_graph_v1` — constructs the InsightGraph with signal results, ranked top findings, confidence, chains, and arbitration output
5. `root_cause_compiler_v1` — for signals in `_ROOT_CAUSE_TARGETS` (37 entries), loads governed hypothesis YAML assets from `knowledge_bus/root_cause/hypotheses/` and compiles structured `root_cause_v1` blocks with `evidence_for`, `evidence_against`, `missing_data`, `confirmatory_tests`
6. `publish_interpretation_display_layer_v1` — publishes the IDL bundle from `idl_records_v1.yaml`
7. `compile_narrative_report_v1` — compiles the narrative report (deterministic mock path by default; Gemini-gated behind env flags)
8. `assemble_consumer_domain_scores_v1` — assembles Wave 1 domain cards with band labels, headlines, consequence sentences, next-step sentences
9. `build_replay_manifest_v1` — stamps the engine versions, registry hashes, and signal registry version for audit trail
10. `build_analysis_result_dto` — serialises to the frontend payload contract

The scoring engine (`rules.py`) uses `position_in_range` / `position_in_one_sided_lab_range` from `primitives.py` against lab-supplied reference ranges for standard biomarkers. Derived ratios use explicit policy-defined bounds from `scoring_policy.yaml`. The "SSOT/global range fallback" path is explicitly blocked for lab-provided markers (`rules.py:323-325`). This is architecturally correct.

`bio_stats_engine.py` computes z-scores for system burden: `z = (value - mid) / half_range`. This is symmetric — z is equally positive whether the value is above or below the range. No directional weighting exists in this module.

### Knowledge Bus
187 package directories exist under `knowledge_bus/packages/`. `SignalRegistry._load` globs all `*/signal_library.yaml` files at runtime — the packages are consumed at startup, not via an import list. 40 governed hypothesis YAML files exist under `knowledge_bus/root_cause/hypotheses/`. The runtime compiler loads whichever of the 37 `_ROOT_CAUSE_TARGETS` matches the active lead signal. Packages that are not in `_ROOT_CAUSE_TARGETS` contribute signal definitions only (signal library YAML), not governed WHY.

### Layer B → Layer C contract
`build_analysis_result_dto` in `backend/core/dto/builders.py` (392 lines) assembles the payload passed to the frontend. The payload includes: `analysis_id`, `biomarkers` (with scores, lab ranges, educational explainers, display fields), `consumer_domain_scores`, `clinician_report_v1`, `narrative_report_v1`, `interpretation_display_layer_v1`, `actions.interventions`, `actions.clinician_referrals`, `meta` (including replay manifest, missing markers, system confidence, lifestyle bridges, narrative runtime provenance). The `insights[]` array is still serialised (now empty after LC-S11A) but remains in the contract. `layer3_insights.json` was a separate structured surface from the P3 artifact containing lifestyle-aware insight structs — this is distinct from the empty `narrative.txt` placeholder.

### Frontend / Layer C
`frontend/app/(app)/results/page.tsx` (large file) renders a multi-section results journey consuming: `ClinicianReportV1` (the primary analytical payload consumed by `InsightPanel`, `PrimaryFindingAndWhy`, `WhyThisLeadWonSection`), `Wave1DomainCards`, `InterpretationPatternsSection` (IDL), `DeterministicNarrativeSurface`, `BalancedSystemsSummary`, `BiomarkerDials`, `ClinicianReportRenderer`. The `legacyInsightsVisibility.ts` gate filters `manifest_id: legacy_v1` entries from the `insights[]` array; this is correctly gated off consumer paths by default. The frontend does NOT perform analytical reasoning — it renders governed structured fields. This is architecturally correct Layer C behaviour.

### Tests / Sentinel
219 backend test files total. 14 active regression tests under `backend/tests/regression/`. Sentinel Phase 1 runner (`sentinel/sentinel_runner.py`) maps defect classes to regression test files and executes them; it does not write to governance artefacts. 44 frontend test files covering Jest unit tests and 4 Playwright e2e specs. One Sentinel entry (`persisted_result_replay`) is explicitly `status: "PLACEHOLDER"` with no real assertion.

### Automation Bus
`run_work_package.py` enforces branch/work_id alignment, writes/reads the execution authority token in `automation_bus/state/work_package_active.json`. `golden_gate_local.py` runs the gate tests. The audit chain (GPT → Claude → Cursor → Gate) is operationally enforced. LC-S11A completed cleanly with two residual escalation items noted in the audit.

---

## 4. Category scores

| Category                   | Score /10 | Rationale |
| -------------------------- | --------: | --------- |
| Overall architecture       |         7 | Three layers are real and mostly respected. Orchestrator monolith is debt but not a rebuild-level problem. No LLM in Layer B. |
| Medical governance         |         6 | Lab-range-only scoring for standard biomarkers is correct. Unit registry is real. Alias handling is guarded. Symmetric z-score in bio_stats_engine is a clinical governance gap for direction-sensitive biomarkers. SSOT `key_risks_when_high: []` is empty for 55/103 biomarkers — not used in scoring path, but incomplete registry. |
| Layer B analytical core    |         7 | Signal evaluation with bound-aware activation is correct. Root cause compiler with 37 targets and governed hypothesis YAMLs is a real differentiator. Arbitration, replay manifest, confidence builder, IDL publisher are all real. Weakness: lifestyle modifier modifies internal numbers but does not propagate to user-visible fields. |
| Knowledge Bus              |         6 | 187 packages and 40 hypothesis YAMLs are real assets loaded at runtime. Signal library YAML → evaluator wiring is clean. However: 37 `_ROOT_CAUSE_TARGETS` out of 137 signals means 73% of signals produce no governed WHY; packages not in `_ROOT_CAUSE_TARGETS` contribute signal shape only. Runtime consumption is real; scalability is real; depth is uneven. |
| Layer B → Layer C contract |         6 | Structured payload is real and rich (clinician_report_v1, consumer_domain_scores, IDL bundle, replay manifest). Flat narrative.txt is the mock-mode output, not the primary consumer surface. Layer C does not reinterpret Layer B. Weakness: the consumer domain scores and narrative surfaces carry lifestyle-invariant content despite the lifestyle modifier running. The contract is complete structurally; its propagation is incomplete functionally. |
| Frontend architecture      |         7 | No analytical reasoning in the frontend. Structured field consumption is correct. Layer C insert points (`InsightPanel`, `PrimaryFindingAndWhy`, `Wave1DomainCards`, `InterpretationPatternsSection`) map to correct contract fields. Legacy insights gated correctly post-LC-S11A. Some complexity in `results/page.tsx` (very large file). |
| Product/user experience    |         5 | Analytical depth on the lead finding is genuinely strong. Runner-up disclosure language is unusually honest. Questionnaire produces no visible payoff — the product asks for 56 questions and the user cannot detect any effect. Cardiovascular card `band: stable` + headline "not a simple all-clear" is a coherence contradiction that is reproducible and unguarded. Mock-mode prose ("your measured homocysteine") reads as personalised output. |
| Testing/Sentinel           |         5 | 14 active regression tests are real and protect specific defect classes. One key test (`test_lc_s5_proving_checks.py`) has a pre-existing Unicode failure (urate unit mismatch). `persisted_result_replay` is an explicit placeholder with no real assertion. No cross-section coherence guard (hero vs clinician agreement) exists. No combination-case tests (iron+inflammation, thyroid+lipid). Lifestyle-invariant output is not regression-protected. Frontend e2e coverage is thin (4 Playwright specs). |
| Maintainability            |         5 | Orchestrator is 2,319 lines — acknowledged technical debt. Analytics directory has 55 files; navigation requires familiarity. The three-layer architecture and Automation Bus discipline create a navigable structure for a small team but would require significant on-boarding for new developers. `biomarkers.yaml` has 55/103 entries with empty `key_risks_when_high` fields — the SSOT is incomplete as documentation. |
| Scalability                |         6 | New signals can be added via Knowledge Bus packages without changing orchestrator code. New hypothesis YAMLs can be added by adding a loader and a `_ROOT_CAUSE_TARGETS` entry. Lifestyle registry is YAML-driven and extensible. Weakness: adding a new direction-sensitive biomarker (like ALT) currently requires a hardcoded bypass in `rules.py`. The `_ROOT_CAUSE_TARGETS` list is a maintained registration table — manageable but not auto-discovered. |
| Commercial readiness       |         4 | The engine is commercially credible on the homocysteine/methylation finding. The questionnaire gap destroys the personalisation promise at first user contact. The legacy `insights[]` placeholder was removed from computation (LC-S11A) but the `insights` key remains in the DTO as an empty array — not user-facing now, but structurally ugly. Mock-mode prose reads as AI output. No formal release confidence gate document exists. GDPR LLM upload disclosure status is uncertain. |

**Overall architecture grade: C**

Grading standard applied:
- A = enterprise-grade foundation, needs normal product hardening
- B = strong foundation with some architectural debt
- C = viable but uneven; needs targeted restructuring
- D = prototype with serious architectural debt
- E = fragile demo system; major rebuild likely
- F = not worth continuing without rebuild

The C grade reflects a product that has a genuine and serious analytical foundation, passes evidence inspection in its core claim (governed WHY for the lead finding), and has real governance infrastructure — but has not yet composed its pieces into a coherent, commercially trustworthy user experience. The architecture is sound enough to launch from; the product is not yet ready to charge for.

---

## 5. What is genuinely strong

**Root cause compiler and hypothesis YAMLs are real.**
`root_cause_compiler_v1.py:76-118` registers 37 signal→loader pairs. 40 hypothesis YAML files exist under `knowledge_bus/root_cause/hypotheses/`. The verification ledger (2026-05-04) confirmed that on both AB and VR fixtures, the lead signal produced 4 governed hypotheses with `evidence_for`, `evidence_against`, `missing_data`, `confirmatory_tests`, and `hypothesis_confidence` — zero fallback strings across 12 runs. This is the product's moat claim and it holds.

**Signal activation boundary enforcement is architecturally correct.**
`signal_evaluator.py:155-175` reads `enable_upper_bound` and `enable_lower_bound` from each signal's `activation_config` before applying the check. The fix for the R-1 asymmetric activation bug is baked into the evaluation loop, not a patch on top. LC-S11A's fix for ApoA1 (`pkg_kb45_apoa1_low_cardio_risk/signal_library.yaml` line 43: `enable_upper_bound: false`) follows the same mechanism correctly.

**Lab-range-only scoring for standard biomarkers is a correct governance choice.**
`rules.py:323-325` explicitly blocks SSOT/global fallback for lab-provided markers. Derived ratios use explicit policy bounds (`scoring_policy.yaml`). This prevents the product from silently using hardcoded reference ranges when the lab provides its own — a common failure mode in competitor products.

**Replay manifest and auditability infrastructure are real.**
Each analysis run produces a `replay_manifest` with engine versions, registry hashes, and signal registry version. The verification ledger confirmed this was stamped per run. This is a genuine enterprise-grade traceability mechanism that most consumer health products lack entirely.

**Runner-up disclosure language when it fires is unusually honest.**
On the VR panel, `runner_up_why_not_lead_line` produced: "Homocysteine Elevation Context and Homocysteine High are similarly strong on this panel (0.90 vs 0.90); the headline shows one pattern first so the discussion has a single starting point." This is the kind of explicit clinical honesty that most products actively suppress in favour of false confidence.

**Unit registry and alias handling are production-grade.**
`units/registry.py` covers 19 distinct unit enums with deterministic conversion dispatch by biomarker group. Sentinel guards alias/canonical sweep, GGT alias, and bilirubin venous alias separately. The LC-S8 sprint series built a genuinely robust unit governance layer.

**Three-layer architecture is respected in practice.**
No LLM calls were found in `backend/core/analytics/` or `backend/core/scoring/`. Gemini is confined to `backend/core/llm/` and double-gated behind env flags. The frontend does not perform analytical reasoning. The layer boundary is enforced in practice, not just in architecture documents.

---

## 6. What is weak, brittle, or dangerous

**The bio_stats_engine symmetric z-score is a clinical governance failure for direction-sensitive markers.**
`bio_stats_engine.py:24-60` uses `z = (value - mid) / half_range` symmetrically. For ALT at 7 U/L against a 10–49 U/L range, this computed a z-score of -1.17 (below) equivalent in magnitude to ALT at 52 U/L (above), driving a 5/100 liver score. The LC-S11A fix hardcodes `if biomarker_name == "alt" and value < float(min_val):` at `rules.py:309-311`. This is confirmed as non-systematic by the LC-S11A audit itself (residual item R1, escalated to GPT). GGT, AST, ALP, and any other enzyme where low values are benign carry the same uncorrected risk. The fix is a one-biomarker bypass on top of a structurally wrong formula.

**The questionnaire has zero visible user payoff.**
The verification ledger (LAUNCH_GRADE_VERIFICATION_LEDGER_2026-05.md §4.4) confirmed across 12 runs with four contrasting lifestyle profiles (including a stressed profile with BMI 32.4, BP 158/96, current smoker, 35 alcohol units/week, 5h sleep) that `overall_score`, `top_findings` ordering, `consumer_domain_scores` (all fields), `narrative_report_v1.retail_summary`, `narrative_report_v1.next_steps_narrative`, `actions.interventions`, and all clinician page1 fields are identical to seven decimal places. The only visible effect is a 124-character technical bridge sentence in `lead_narrative` when the alcohol bridge fires, using the raw internal rationale code verbatim ("Lifestyle bridge - one-carbon / alcohol context: active (alcohol_intake_moderate_or_higher_with_one_carbon_lab_coherence)."). No user can read this as personalisation. `lifestyle.confidence_adjustments` is uniformly 0.0 in all runs — the path exists but produces no output.

**The orchestrator is a 2,319-line procedural monolith.**
`backend/core/pipeline/orchestrator.py` at 2,319 lines is acknowledged as technical debt in the Transformation Programme Brief. It imports from 45+ sub-modules. Adding or reordering analytical steps requires modifying this file. It is navigable by a single developer who built it; it is not multi-developer-safe without significant decomposition.

**Cross-section coherence is unguarded and one contradiction is reproducible.**
The verification ledger (§5) confirmed that the cardiovascular consumer card simultaneously shows `band_label: "stable"`, `confidence_tier: "high"`, and `headline_sentence: "Your cardiovascular read on this panel is not a simple all-clear"`. These are in direct tension. No Sentinel test or regression test asserts that hero bands and headline sentences are polarity-coherent. The gap map documented this as "NOT MET (no guard)."

**Persisted result replay protection is a placeholder.**
`backend/tests/regression/test_persisted_result_replay_status.py` is documented as a placeholder with the comment "Full persisted-result replay (loading a golden run JSON through the current pipeline validator and asserting schema compatibility + correct frontend rendering) is deferred to Phase 2+." The escaped_defects pack confirms: `"guard_type": "status_reporting"`. A paying user who re-opens a historical analysis after a code change may receive a different or broken result, and no deterministic guard will catch this.

**37 of 137 signals have governed WHY; the remaining 100 fall back silently or use the fallback string.**
The verification ledger confirmed that on the AB panel, `signal_homocysteine_high` (rank 2), `signal_mcv_high` (rank 3), `signal_apoa1_cardio_risk` (rank 5), and `signal_ldl_high` (rank 7) are all active but carry no governed `root_cause_v1` block. When these appear as lead findings on other panels they will use the fallback string, which the product explicitly claims is unacceptable for §4.1 signals. `signal_ldl_high` appearing as lead without governed WHY is a credibility failure because LDL is one of the most prevalent UK commercial panel findings.

**SSOT biomarkers.yaml has 55/103 entries with empty `key_risks_when_high` and `known_modifiers` fields.**
While these fields are not currently used in the scoring path, their emptiness signals that the canonical biomarker registry was created structurally but not populated substantively. A future team reading `biomarkers.yaml` to understand the clinical model would find it opaque. This is a documentation and maintainability debt.

**Mock-mode prose uses first-person possessive language without disclosure.**
Narrative strings like "your measured homocysteine is the main lab anchor" and "your cardiovascular read on this panel" are in the deterministic mock output (`narrative_runtime.runtime_mode = "deterministic_mock"`). A paying user can reasonably read this as AI-personalised output. The mock-mode flag is buried inside `meta.narrative_runtime` and not surfaced anywhere on the user-facing results page.

---

## 7. Medical-governance assessment

**Reference range handling is correct by design.**
The scoring rules explicitly block SSOT global range fallback for lab-provided biomarkers (`rules.py:323-325`). Derived ratios use explicit policy bounds. This is the right clinical governance choice and it is enforced at code level with test coverage.

**Unit safety is production-grade.**
The unit registry covers 19 unit types with deterministic conversion dispatch. Biomarker-group-specific dispatch (cholesterol group, thyroid group, etc.) prevents silent unit mismatches. `UNIT_ALLOW_UNMAPPED` defaults to false. The LC-S8 sprint series is responsible for this and it is genuine.

**Signal traceability is adequate but incomplete at the user-facing surface.**
Every signal carries `signal_id` and `supporting_markers`. The replay manifest is stamped per run. The frontend renders `PrimaryFindingAndWhy` from governed `clinician_report_v1` fields. However, no end-to-end UI test asserts that every visible card cites its signal ID, and there is no guard preventing a card appearing with an un-governed confidence statement.

**Direction-sensitive biomarker handling has a structural gap.**
The bio_stats_engine symmetric z-score (`bio_stats_engine.py:51`) is the core clinical governance failure. For any biomarker where "below range" is clinically distinct from "above range" in severity (ALT, GGT, ALP for low values; HDL where high is protective), the system currently overweights below-range deviations in the system burden calculation. The ALT bypass in `rules.py:309-311` patches the downstream scoring effect but does not fix the z-score computation. The system burden vector used by domain card assembly still reflects the wrong directional weighting.

**Fallback governance is present but not regression-protected for all cases.**
The fallback string "No hypothesis set available for this concern in v1" is a constant in `report_compiler_v1.py:535` (confirmed by gap map). This is deterministic. However, no regression test confirms that it renders on both consumer and clinician surfaces when triggered. The LC-S11A defect 2 fix (`domain_narrative_wave1.py`: early return for no active signals) adds a more specific honest fallback for the blood sugar case — this is the right approach but has not been generalised.

**The confidence_adjustments path is broken.**
`lifestyle.confidence_adjustments` is uniformly 0.0 in all four profiles tested in the verification ledger. The path exists in the registry (`lifestyle_registry.yaml:209-221`) with rules for `missing_input_confidence_penalty` by system. Either the penalty computation is gated by a condition that was never triggered, or the integration path is broken. Either way, the confidence layer does not degrade as expected when core lifestyle inputs are missing.

---

## 8. Layer B analytical-core assessment

**What works:**
- Signal evaluation with bound-aware activation, override rules, and confidence scoring is correct and governed
- Root cause compiler produces structured multi-hypothesis WHY with evidence_for/against for 37 registered signal targets — verified at runtime, not just claimed
- Arbitration engine (dominance edges, near-tie detection, `distinct_lead`/`near_tie_ambiguity`/`technical_tiebreak_lead`) is sophisticated and produces honest output
- InsightGraph construction with ranked top findings and signal chains is real
- IDL publisher produces an enabled record set with severity, frontend terms, and supporting biomarker summaries
- Replay manifest is stamped correctly per run
- Intervention annotation compiler selects interventions from the registry and formats them into the actions block

**What is weak:**
- Orchestrator at 2,319 lines is difficult to extend safely without introduction of regression risk
- Lifestyle modifier outputs do not reach any user-visible surface — the internal computation is correct but disconnected
- `lifestyle.confidence_adjustments` uniformly 0.0 indicates a broken or dormant path
- 100 signals (73% of the estate) produce no governed WHY — the signal estate outgrew the hypothesis estate
- bio_stats_engine symmetric z-score produces clinically wrong system burden for direction-sensitive biomarkers, affecting domain card severity downstream
- No combination-case reasoning (iron+inflammation, thyroid+lipid) is implemented at the rendering level — IDL records exist for these but no runtime fixture confirms they produce a coherent joint card

**Determinism verdict:** The engine is deterministic. Same inputs produce identical outputs across 12 runs with varying profiles (the lifestyle invariance that is the product gap is also, from a determinism standpoint, a confirmation that the engine is not drifting). The replay manifest mechanism makes determinism auditable.

---

## 9. Knowledge Bus assessment

**Real infrastructure, uneven depth.**

The Knowledge Bus pipeline is genuinely operational. `SignalRegistry._load()` in `signal_evaluator.py:41-70` globs `knowledge_bus/packages/*/signal_library.yaml` at startup and loads all signal definitions deterministically. 187 package directories exist. The packages are consumed at runtime, not as documentation.

40 hypothesis YAML files under `knowledge_bus/root_cause/hypotheses/` are loaded by function-specific loaders registered in `_ROOT_CAUSE_TARGETS`. The 37-entry registration table in `root_cause_compiler_v1.py:76-118` is the runtime consumption point.

**The gap:** 187 packages but 37 hypothesis YAML coverage points means that 150 packages contribute signal definitions only. Their `research_brief.yaml` and `signal_library.yaml` are loaded at runtime; their hypotheses are not — because they are not in `_ROOT_CAUSE_TARGETS`. This is not a pipeline failure; it is a prioritisation reality that has been documented in the gap map. The bottleneck is not the Knowledge Bus pipeline; it is the rate at which governed WHY assets can be authored and integrated.

**Scalability is real but requires a maintained registration table.** Adding a new signal to `_ROOT_CAUSE_TARGETS` requires: authoring a hypothesis YAML, writing a loader function, and adding the `(signal_id, loader)` pair to the list. This is manageable for one or two developers but is not auto-discoverable — a new contributor will not know that `_ROOT_CAUSE_TARGETS` is the runtime integration point without documentation.

**The `pkg_example` package is explicitly excluded** (`signal_evaluator.py:33`) from the glob — this is correct governance.

---

## 10. Layer B → Layer C contract assessment

**The contract is structured and real.** The DTO includes `clinician_report_v1` (the primary analytical payload), `consumer_domain_scores` (Wave 1 domain cards), `interpretation_display_layer_v1` (IDL bundle), `narrative_report_v1` (narrative sections), `actions` (interventions and clinician referrals), and `meta` (system confidence, missing markers, replay manifest, lifestyle bridges, narrative runtime provenance). This is a rich, structured payload — not flat strings.

**Layer C does not reinterpret Layer B.** The frontend renders governed fields from the DTO. `PrimaryFindingAndWhy.tsx` renders `clinician_report_v1.sections.page1.primary_concern` and `root_cause` without augmentation. `InsightPanel.tsx` renders `page1.key_findings[0]`, `confidence_and_missing_data`, `runner_up_topic_line`, `runner_up_why_not_lead_line` — all governed Layer B fields. This is architecturally correct.

**The lifestyle computation outputs are not in the contract.** `lifestyle.system_modifiers` is in the DTO but is not consumed by any user-facing component. The `meta.lifestyle_interpretation_bridges_v1` block contains the active bridge data but `meta` is not rendered to users. The contract between lifestyle computation and user-visible surfaces is the missing link, not the contract between Layer B and Layer C.

**LLM readiness:** The `narrative_runtime` field on `meta` carries the runtime mode, policy reason, and master switch status. This is the governed handoff point if Gemini is ever activated. The double-opt-in gate is correctly implemented. The contract supports LLM activation without architectural change.

**Flat strings vs structured payload:** The `narrative.txt` artifact (the mock output surface) is template-generated flat text. But the primary consumer surfaces — `consumer_domain_scores`, `clinician_report_v1`, `IDL records` — are structured. The `narrative.txt` surface is the mock-mode narrative layer, not the product's primary output surface.

---

## 11. Frontend/product assessment

**Architecture:**
The frontend is a correctly positioned Layer C. No analytical reasoning, no hardcoded clinical thresholds, no signal evaluation. Renders structured DTO fields only. The legacy `insights[]` gate (`legacyInsightsVisibility.ts`) correctly suppresses `manifest_id: legacy_v1` entries from consumer paths behind an env flag. The `scrubConsumerRetailNarrative` call in `PrimaryFindingAndWhy.tsx` confirms that there is at least some LLM boundary enforcement at the presentation layer.

The results page (`frontend/app/(app)/results/page.tsx`) is a complex file importing from 40+ modules and managing significant local state. It is not architecturally wrong, but it is reaching the size where decomposition into sub-page components would improve maintainability.

**Product quality gaps:**
- The cardiovascular domain card shows `band_label: "stable"`, `confidence_tier: "high"`, and headline "not a simple all-clear" simultaneously. A user reading this cannot understand whether their cardiovascular health is stable or not.
- The questionnaire produces no visible personalisation. The most visible effect of answering 56 questions with extreme lifestyle inputs is a 124-character internal code string in the narrative.
- Mock-mode prose uses "your measured homocysteine" and "your cardiovascular read on this panel" in a template-generated context. A new user who expects personalised AI output and then notices the questionnaire changed nothing will correctly suspect the product is not using their data.
- Wave 1 domain cards (D-1 through D-7) are described as complete. These are the primary user-facing analytical output and they appear to be structurally in place.

---

## 12. Testing/Sentinel assessment

**What is real:**
- 14 named regression tests in `backend/tests/regression/` protect specific defect classes (alias resolution, slug leakage, unit governance, statin isolation, narrative WHY surface, payload assembly, proving checks)
- Sentinel runner maps these to defect classes and executes them
- LC-S11A added 11 new regression tests covering its four trust blockers
- Frontend has 44 test files and 4 Playwright e2e specs
- The `test_lc_s5_proving_checks.py` conservative contradiction check (band vs consequence polarity) is a real guard, not a status placeholder

**What is placeholder or missing:**
- `test_persisted_result_replay_status.py` is explicitly a status-reporting placeholder: "Full persisted-result replay ... is deferred to Phase 2+." It checks only that the golden runs corpus exists and has `analysis_id` fields. It does not assert schema compatibility or correct rendering.
- No cross-section coherence test: no test asserts that hero `primary_concern`, retail `retail_summary`, and IDL lead record all agree on the same signal
- No combination-case fixture: no test runs a fixture with low ferritin + high CRP and asserts a coherent joint IDL card
- No lifestyle-invariance guard: no test asserts that swapping lifestyle profiles changes at least one user-visible field (which would currently fail)
- `test_lc_s5_proving_checks.py` has a pre-existing failure on the `test_check2_alcohol_bridge_language_when_moderate_threshold_met` test due to a urate Unicode normalisation mismatch (Greek mu vs micro sign) — this is pre-existing and noted in the LC-S11A audit
- Sentinel Phase 2 (Playwright coherence checks, DTO schema comparison) is NOT STARTED

**Testing quality vs. quantity problem:**
219 backend test files but the regression coverage of the critical path is 14 tests. The unit test count is high; the regression integration count is low. The unit tests verify individual components; the regression tests verify the user-visible pipeline. The balance favours unit tests over the tests that would catch the questionnaire-invisible-payoff class of failure.

---

## 13. Automation/workflow assessment

**The Automation Bus is functioning as intended.** LC-S11A completed cleanly: kernel started, Cursor implemented, gate passed, Claude audited, escalation items noted. The branch discipline is enforced. The hardening JSON has mandatory evidence checklist. The `latest_cursor_status.json` confirms the COMPLETE status.

**The workflow is appropriate for the risk profile.** A product that claims clinical interpretive authority needs governance that prevents unreviewed changes to the analytical engine. The GPT→Claude→Cursor→Gate chain is that governance. It has costs (slower delivery) that are real and justified.

**The workflow does not hide weak architecture; it governs real architecture.** The LC-S11A sprint fixed four genuine trust blockers, each with a traceable evidence chain from audit finding to code change to regression test. This is the workflow working as intended, not as bureaucratic cover for weak output.

**One structural tension exists.** The Transformation Programme Brief notes that "no release confidence gate document exists" and that "no formal definition of what must be true before the first paying user uses the product" has been authored. The Automation Bus governs per-sprint execution but does not enforce a launch-readiness threshold. This is a programme management gap, not an Automation Bus failure.

---

## 14. Maintainability and scalability

**For the current team:** The codebase is navigable. The three-layer architecture, Automation Bus discipline, and Knowledge Bus pipeline create clear responsibility boundaries. A developer who understands the sprint history can find their way.

**For a new developer:** Challenging. The orchestrator is 2,319 lines with no internal decomposition into named phases. The analytics directory has 55 Python files with no documented dependency order. `_ROOT_CAUSE_TARGETS` in `root_cause_compiler_v1.py` is not documented as the runtime integration point for new hypothesis assets. The `biomarkers.yaml` SSOT has 55/103 biomarker entries with empty metadata fields that do not signal what those fields mean or where they are used.

**Scalability of the signal estate:** Adding a new signal requires a Knowledge Bus package (signal_library.yaml), potentially a hypothesis YAML if WHY is needed, a loader function, and a `_ROOT_CAUSE_TARGETS` entry. This is reproducible but not self-documenting. The fact that 187 packages exist with only 37 in `_ROOT_CAUSE_TARGETS` is a potential onboarding confusion: "why are there 187 packages if only 37 matter for WHY?"

**Scalability of the scoring engine:** The current `biomarker_name == "alt"` bypass in `rules.py:309-311` is the first of what could become a growing list of direction-specific special cases. Without a systematic direction-aware mechanism, each new enzyme that has clinically asymmetric severity will need its own bypass. This is maintainability debt with clinical risk.

**Multi-developer readiness:** Currently single-developer (or very small team). The Automation Bus governance framework is capable of supporting multiple developers with appropriate lane discipline. The codebase itself needs onboarding documentation, orchestrator decomposition, and a generalised direction-aware scoring mechanism before it is safe for multi-developer expansion.

---

## 15. Commercial readiness

**To a consumer:** The analytical depth on the lead finding is genuinely impressive — 4 governed hypotheses with structured evidence, transparent runner-up disclosure, honest confidence framing. But the questionnaire is a broken promise. The user fills in 56 questions and the product visibly does nothing with the answers. In a paid product, this destroys the trust the analytical depth built. The cardiovascular card polarity contradiction (stable + "not a simple all-clear") will be noticed by any medically literate user.

**To a clinician:** The governed WHY with evidence_for/evidence_against, the ranked hypothesis confidence, the confirmatory tests list, and the clinician summary report are credible. The fallback string appears for signals outside the 37 `_ROOT_CAUSE_TARGETS` — a clinician encountering this for a cortisol or creatine kinase lead finding will correctly judge it as an incomplete product. The replay manifest and audit trail are appropriate for a clinical handoff tool.

**To an investor:** The architecture is investable — three real layers, governed engine, audit trail, 187 KB packages. The questionnaire gap is a product gap, not an architectural gap. An investor who runs the product themselves will encounter the personalisation failure within minutes of completing the questionnaire. This is the most important commercial risk: the gap between the strategic narrative ("personalised contextual intelligence") and the runtime reality ("questionnaire has no visible effect") is large enough to undermine the funding story.

**To a technical due-diligence team:** The codebase would pass a basic architecture review — three layers are real, no LLM in the analytical core, SSOT enforcement, audit trail. Due diligence would flag the orchestrator monolith, the symmetric z-score clinical governance gap, the empty SSOT metadata fields, and the placeholder persistence test. None of these would be deal-breakers individually; together they form a picture of "early-stage but architecturally serious."

---

## 16. Rebuild judgement

**Continue on current codebase — with two targeted interventions.**

A full or major rebuild is not justified. The analytical engine core is sound, the three-layer separation is real, and the Knowledge Bus pipeline is operational. Rebuilding these would discard genuine value.

A targeted partial rebuild of the orchestrator (decomposition into phases) is warranted as a Phase 1.1 maintainability sprint — it is not launch-blocking.

Two targeted interventions are required before commercial launch:

1. **Lifestyle → surface propagation.** The lifestyle modifier engine and bridge engine are computing correct outputs that are not reaching any user-visible surface. This is not a rebuild; it is a wire connection. The target surfaces are `consumer_domain_scores`, `clinician_report_v1.sections.page1`, and `actions.interventions`. The mechanism exists; the propagation is missing.

2. **Direction-aware scoring for asymmetric biomarkers.** The `bio_stats_engine.py` symmetric z-score needs a directional weighting mechanism that can be configured per biomarker. This is a scoring engine change, not an architectural change. It requires generalising the `biomarker_name == "alt"` pattern into a policy-driven asymmetry table. Without this, every new direction-sensitive enzyme biomarker is a false alarm risk.

---

## 17. Top risks

### Top five architectural risks

**Risk 1: Symmetric scoring engine produces false alarms for direction-sensitive biomarkers.**
`bio_stats_engine.py:51` z-score formula is symmetric. The ALT bypass in `rules.py:309-311` is a patch. GGT, AST, ALP, and any enzyme where low is benign are unprotected. Each will produce a false alarm (disproportionate domain severity) until bypassed individually. This is a patient-safety-adjacent risk if clinicians use the clinician report.

**Risk 2: Questionnaire visible-payoff gap destroys commercial trust at first contact.**
12 verified runs confirmed the lifestyle modifier produces no user-visible effect. This is not speculative — it is measured. If the product launches with this gap, the first user cohort will notice and the trust recovery cost will be higher than the fix cost.

**Risk 3: Orchestrator monolith becoming progressively more fragile.**
At 2,319 lines and growing, `orchestrator.py` is one analytical step away from becoming unmaintainable. Each new sub-engine added in a sprint adds another import and another block to an already long pipeline. Phase 1 sprints are individually safe; the accumulation is not.

**Risk 4: 100 signals with no governed WHY create a long tail of credibility failures.**
If a user's panel produces a lead finding outside the 37 `_ROOT_CAUSE_TARGETS` — which is statistically likely for any panel where cortisol, creatine kinase, DHEA, or eGFR leads — the product's central claim fails silently. The fallback string exists but is a product quality failure compared to the governed WHY the product can produce for homocysteine.

**Risk 5: Persisted result replay has no real test.**
The `test_persisted_result_replay_status.py` placeholder does not assert anything about rendering correctness. Schema drift between persisted analyses and live code is a silent failure mode that will surface in production when a returning user loads a historical analysis.

### Top five product risks

**Risk 1: Questionnaire produces no visible payoff.**
Already detailed. This is the single highest-priority commercial risk.

**Risk 2: Mock-mode narrative prose reads as personalised AI output.**
Paying users may believe they are receiving AI-personalised interpretation. When they notice the questionnaire had no effect, they will correctly conclude the product misrepresented its capability. Regulatory risk in markets where AI health product claims are scrutinised.

**Risk 3: Cardiovascular card polarity contradiction.**
`band_label: "stable"` + `headline_sentence: "not a simple all-clear"` is reproducible and unguarded. A medically literate user or clinician reading this will lose confidence in the product's analytical coherence.

**Risk 4: Active findings without WHY create a thin results experience for real panels.**
4-5 active suboptimal findings per real panel currently have no governed WHY. On a panel where LDL is elevated but not the lead, the user sees an active LDL finding with no explanation. This is the most common commercial panel marker.

**Risk 5: No formal release confidence gate.**
The Transformation Programme Brief confirms "no formal definition of what must be true before the first paying user uses the product" exists. This means launch is a judgement call rather than a governed threshold. Given the questionnaire gap and the symmetric scoring issue, a launch decision made without a formal gate is a commercial risk.

---

## 18. Recommended next three sprints

### Sprint 1: LC-S13 — Lifestyle Surface Connection

**Work ID:** LC-S13
**Purpose:** Connect the lifestyle modifier engine and bridge engine outputs to user-visible surfaces in `consumer_domain_scores`, `clinician_report_v1.sections.page1`, and `actions.interventions`. Make the questionnaire produce at least one detectable user-visible effect on a contrasting lifestyle comparison.

**Why it matters:** This is the single highest-priority gap between the product's strategic claim ("personalised contextual intelligence") and runtime reality (questionnaire has no visible effect). It is commercially blocking. The analytics are computed correctly; the propagation is missing.

**What NOT to do:** Do not redesign the questionnaire. Do not attempt to make lifestyle rewrite signal activation (that is Phase 2+). Do not build a new lifestyle narrative engine. The goal is to propagate already-computed modifier values and bridge activations to fields the user can see — at minimum, the alcohol bridge rationale in human-readable language in the narrative, and lifestyle-conditional next-step recommendations.

**Acceptance bar:** Two contrasting lifestyle profiles on the same AB panel produce at least one different user-visible field in `consumer_domain_scores` or `narrative_report_v1.retail_summary`, expressed in human-readable language. The alcohol-methylation bridge sentence appears in language a paying user can read (not raw rationale code).

### Sprint 2: LC-S14 — Direction-Aware Scoring Mechanism

**Work ID:** LC-S14
**Purpose:** Replace the `biomarker_name == "alt"` hardcoded bypass in `rules.py:309-311` with a policy-driven direction-awareness table. Identify all biomarkers where below-range deviation is clinically distinct in severity from above-range deviation and encode their directional asymmetry in the scoring policy YAML.

**Why it matters:** The current bypass is the residual item R1 from the LC-S11A audit, escalated to GPT for architectural review. Without a systematic fix, each new enzyme biomarker where low values are benign requires its own hardcoded bypass. This is a clinical governance gap that scales poorly and creates false alarm risk for every new direction-sensitive biomarker added.

**What NOT to do:** Do not change `bio_stats_engine.py`'s z-score formula for the system burden path without understanding the downstream effects on all domain card band computations. The fix should be in the scoring rules layer, not in the z-score computation, to avoid unintended domain-level drift. Do not expand the scope to redesign the full scoring engine.

**Acceptance bar:** A panel where ALT is below range does not produce a critical liver score or "Needs review" card. The fix mechanism is a policy table, not a biomarker name comparison. GPT architectural review is completed before implementation begins (residual from LC-S11A).

### Sprint 3: LC-S15 — Coherence Guard and Persisted Replay Minimum

**Work ID:** LC-S15
**Purpose:** (A) Add a regression guard for band-headline polarity coherence on consumer domain cards. (B) Graduate the `test_persisted_result_replay_status.py` placeholder to a real schema compatibility check that asserts a stored DTO loads without error against the current DTO contract.

**Why it matters:** (A) The cardiovascular card contradiction (`band: stable` + headline "not a simple all-clear") is reproducible, unguarded, and will be noticed by any medically literate user or due-diligence reviewer. (B) Returning users loading historical analyses from before a code change have no protection against silent schema drift. Both gaps were identified in the verification ledger and gap map as launch-blocking.

**What NOT to do:** Do not attempt to build full Playwright-based Sentinel Phase 2 in this sprint. The target for part B is a backend schema compatibility assertion only — not render-level testing. Do not conflate this sprint with combination-case coherence (iron+inflammation, thyroid+lipid) — that is a separate workstream.

**Acceptance bar:** (A) A Sentinel regression test asserts that `band_label: "stable"` or `band_label: "optimal"` domain cards do not carry `headline_sentence` text containing emergency or high-urgency language. (B) A stored AB panel DTO from the current git history loads through the current DTO validation layer without schema error and with `analysis_id` present.

---

## 19. Final recommendation

The product owner should proceed on the current codebase but must resolve two specific gaps before charging a paying user:

**The questionnaire must produce at least one user-visible effect.** If this is not fixed before launch, the product will be judged dishonest by any user who fills in 56 questions and then notices the results are identical to a user who answered none. The analytical engine is genuinely impressive; this gap makes it invisible behind a broken promise.

**The scoring engine's direction-sensitive failure must be addressed systematically.** The LC-S11A ALT bypass is a minimum fix for one biomarker. It is not a solution. The architectural review escalated to GPT in the LC-S11A audit must be resolved and the direction-awareness table implemented before the product encounters panels with other direction-sensitive enzyme lead findings.

Do not expand the signal estate before both of these are fixed. Adding Wave 2 signals on top of a questionnaire that has no visible payoff and a scoring engine with a known directional failure is investment in the wrong order.

Do not launch without a formal release confidence gate document. The programme has been running without one. Author it before LC-S13 is scoped. It should answer: what test must pass, what coverage must exist, what product decisions must be made, and who signs off. The Automation Bus governs per-sprint execution; the release gate governs launch. Both are necessary.

The architecture is sound enough to build a commercial product from. The product is not yet ready to charge for. The distance between these two statements is smaller than it appears — the required interventions are bounded and specific, not architectural rescues.
