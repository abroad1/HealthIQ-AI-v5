---
work_id: CLIN-PRIORITY-IMPLEMENTATION-RESET-1
branch: docs/clin-priority-implementation-reset-1
risk_level: HIGH
execution_model: SINGLE_PHASE
change_type: CONTENT
---

# Cross-Domain Clinical Findings and Prioritisation — Stage 0 Repository Inspection

## 1. Verdict

`READY_TO_AUTHOR_AUTOMATION_BUS_CORE_IMPLEMENTATION_PROMPT`

The ratified clinical package (contract v0.6.3, ruleset v0.5, adjudication register v0.4, closure report v0.4), the approved acceptance-scenario estate (v1.2, 109 scenarios), the product-ratified clinician-first model, and the approved architecture-hardening report together supply enough authority and architecture to define one bounded core implementation package without inventing clinical or product policy. The repository contains reusable primitives (signal registry, longitudinal delta calculation, prior-snapshot linking, InsightGraph assembly) but **no existing component implements the contract's consolidated-clinical-finding, tier, urgency, or no-forced-lead model** — this is confirmed green-field work at the finding-construction layer, not an extension of an existing but incomplete finding layer.

## 2. Documents and repository paths inspected

**Governing clinical/product/architecture authority (full read, this and prior sessions in this engagement):** contract v0.6.3; cross-domain ruleset v0.5; HMR adjudication register v0.4; six-domain closure report v0.4; six domain rulesets; acceptance-scenario medical adjudication v0.1; acceptance-scenario approval pack v1.2; product ratification (clinician-first) v1.0; `CLIN-PRIORITY-ARCH-HARDEN-1` architecture-hardening report; day-one architecture rework sprint plan FINAL; ADR-RT-001 through ADR-RT-004.

**Runtime, DTO, orchestration, trend and frontend paths (inspected this task):**
- `backend/core/pipeline/orchestrator.py` — `AnalysisOrchestrator`, the single coordination point for the entire analysis pipeline (lines 1-120 read; import graph confirms every engine named below is wired through it)
- `backend/core/models/insight.py` — `Insight` model (LLM/narrative-facing, not the contract's finding unit)
- `backend/core/contracts/insight_graph_v1.py`, `backend/core/analytics/insight_graph_builder.py` — sole InsightGraph assembler
- `backend/core/analytics/signal_evaluator.py` — `SignalRegistry`, activation-key-keyed, multi-frame preserving (confirmed in prior architecture-hardening pass, `signal_evaluator.py:26-202`)
- `backend/core/models/results.py` — `AnalysisDTO`, `InsightResult`, `ConsumerDomainScoreV1`, `SubsystemEvidenceV1` and related response classes (`results.py:20-403`)
- `backend/core/contracts/report_v1.py` — `ReportV1`, `ReportTopFindingV1`, `ReportTopChainV1` (signal-derived "top finding," not a consolidated clinical finding)
- `backend/core/contracts/clinician_report_v1.py` — `ClinicianReportV1`, `Page1SummaryBlockV1` (`clinician_report_v1.py:88-101`), `RootCauseFindingV1`
- `backend/core/analytics/longitudinal_numeric_v1.py` — `comparable_lab_delta()`, a bounded numeric-delta primitive, explicitly documented as carrying no clinical interpretation (`longitudinal_numeric_v1.py:1-45`)
- `backend/core/analytics/snapshot_linker.py` — `link_prior_snapshot_insight_graphs`, builds deterministic prior-InsightGraph slices from persisted `Analysis`/`AnalysisResult` rows (`snapshot_linker.py:1-30`)
- `backend/core/analytics/state_transition_engine.py` — `build_state_transition_v1`, biomarker-level better/worse/volatile band-transition detection (`state_transition_engine.py:1-90`)
- `backend/core/analytics/state_engine.py` — system-level state aggregation, consumed by precedence
- `backend/core/analytics/precedence_engine.py` — `build_precedence_v1`, cluster/system-level conflict and dominance arbitration, including `conflict_trend_opposition` detection (`precedence_engine.py:55-72`)
- `frontend/app/components/results/WhyThisLeadWonSection.tsx`, `PrimaryFindingAndWhy.tsx` — frontend lead-presentation components consuming `ClinicianReportV1`
- `backend/tests/unit/test_arbitration_scenario_runner.py`, `backend/tests/fixtures/arbitration_scenarios_v2.json`, `backend/tools/run_arbitration_scenarios.py` — an existing, reusable **scenario-runner test-harness pattern**: JSON-fixture scenarios, each producing `insight_graph.json`, `arbitration_report.json`, `explainability_report.json`, `replay_manifest.json`, `summary.txt`, asserted against an `expected` block per scenario (`test_arbitration_scenario_runner.py:19-79`)
- `Glob` for `backend/tests/**/*concern*` and `**/*prioriti*` — zero matches, confirmed again this task (no existing test estate for clinical-concern consolidation or prioritisation)
- `Grep` for `fib.?4|cardiovascular_risk|qrisk|framingham` across `backend/core` — six files matched, none confirmed (without deeper inspection) to expose a live consumer-facing CV-risk score or FIB-4 calculation; flagged for verification, not resolved, in §9

## 3. Current-state inspection, separated by evidence class

### 3.1 Clinical finding construction

`REPOSITORY_VERIFIED_CURRENT_STATE`: no component in the repository constructs a "consolidated clinical finding" as contract §3.1 defines it (a governed unit carrying urgency, severity, tier, role, provenance, missing-data state). The closest existing constructs are:
- `Insight` (`insight.py`) — narrative/LLM-facing, free-text `severity` field, no tier/urgency separation.
- `ReportTopFindingV1`/`RootCauseFindingV1` (`report_v1.py`, `clinician_report_v1.py`) — signal- and root-cause-derived, no Tier 0-3, no urgency time-band, no missing-data/indeterminate-severity state machine.
- `primary_driver_v1` on `InsightGraphV1` — operates on **cluster/system identity**, not on individual clinical findings (confirmed in the approved architecture-hardening report §6).

`PROVISIONAL_INFERENCE`: this confirms, a second time and via a different code path than the architecture-hardening pass used, that the canonical `ClinicalFinding` model decided in that report (§6) remains unbuilt and is genuine new-build work, not a relabelling exercise.

### 3.2 Signal/frame consolidation

`REPOSITORY_VERIFIED_CURRENT_STATE`: `SignalRegistry` (`signal_evaluator.py:26-202`) already implements activation-key-keyed, deterministic, multi-frame-preserving signal storage — this is ADR-RT-002's target architecture, already live, not a pending pilot (re-confirmed from the architecture-hardening pass). This is the correct upstream input for a new concern-construction layer; it does not itself consolidate signals into clinical findings.

### 3.3 Same-domain and cross-domain duplicate handling

`REPOSITORY_VERIFIED_CURRENT_STATE`: `precedence_engine.py` and `state_engine.py` perform **conflict and dominance resolution between systems/clusters** (e.g. `conflict_trend_opposition`, `conflict_abnormal_vs_improving`, `precedence_engine.py:55-72`) — this is duplicate/conflict handling at the wrong grain for the ratified contract, which requires consolidation at the finding level (same-analyte frame consolidation, contract §9.1; cross-domain combination register, ruleset §8) before any system-level arbitration occurs. No code path consolidates two same-domain frames of one analyte, or a cross-domain finding pair, into one finding object.

### 3.4 Urgency and severity representation

`REPOSITORY_VERIFIED_CURRENT_STATE`: no field on any existing model separates urgency (time-to-action band) from severity (domain-specific magnitude) as two independent axes per contract §4.1-§4.2. `Insight.severity` is a single free-text field (`info|warning|critical`).

### 3.5 Lead, co-lead, secondary, supporting and contextual roles; no-forced-lead behaviour

`REPOSITORY_VERIFIED_CURRENT_STATE`: `Page1SummaryBlockV1.primary_concern_mode` (`clinician_report_v1.py:96-99`) is a `Literal["distinct_lead", "near_tie_ambiguity", "technical_tiebreak_lead"]`. **`technical_tiebreak_lead` is a live, named mode in which the current system forces a lead by technical tiebreak even in a tied case.** This directly conflicts with the ratified no-forced-lead product decision (`XD-AS-32`, product ratification §6: "co-lead status must not be used merely to avoid making a difficult prioritisation decision," and the newly-proposed rule that a governed tie with no clinical distinguisher must not be forced). `co_primary_signal_ids` (max length 4) is the existing co-lead mechanism, keyed to signal IDs, not consolidated findings.

`ARCHITECTURE RECOMMENDATION` (carried from the approved hardening report, re-confirmed here): the new concern-construction service must **not** reuse `primary_concern_mode`'s tiebreak logic for clinical-finding lead selection. It may reuse the presentation *shape* (a mode enum, a co-primary list) if convenient, but the underlying selection algorithm must implement contract §7 and the approved no-forced-lead rule from first principles against `ClinicalFinding` objects, not adapt the existing signal-level tiebreak.

### 3.6 Missing-data and indeterminate states

`REPOSITORY_VERIFIED_CURRENT_STATE`: `MissingDataItem` exists in `clinician_report_v1.py` at the narrative-presentation layer. No code implements the contract §8.1 two-consequence-class distinction (insufficient data vs indeterminate severity) as a governed state machine upstream of presentation.

### 3.7 Current-result prioritisation

`REPOSITORY_VERIFIED_CURRENT_STATE`: prioritisation today happens via `precedence_engine`/`arbitration_engine` at cluster/system granularity, using criticality-bucket scoring (`_criticality_bucket`, `precedence_engine.py:26-41`) — a confidence/score-derived bucket, not the contract's urgency-then-severity tier algebra (contract §6.1). No governed-tier assignment exists.

### 3.8 Longitudinal trend calculation and provenance

`REPOSITORY_VERIFIED_CURRENT_STATE`: substantial reusable trend infrastructure already exists:
- `comparable_lab_delta()` (`longitudinal_numeric_v1.py`) — deterministic prior/current numeric delta with unit-match enforcement, explicitly documented as carrying no clinical interpretation.
- `link_prior_snapshot_insight_graphs` (`snapshot_linker.py`) — persists and retrieves up to `DEFAULT_LINKED_PRIOR_SNAPSHOTS = 3` prior InsightGraph slices per analysis, with optional `lab_value`/`lab_unit` for exact numeric replay.
- `build_state_transition_v1` (`state_transition_engine.py`) — per-biomarker band-transition detection (`better`/`worse`/volatile-flagging across ≥2 priors), driven by score bands (`<40 low_band`, `40-70 mid_band`, `>70 high_band`), not by the domain-specific change-defined criteria the ratified rulesets specify (e.g. NICE AKI 48h/50%-7d windows, potassium 6-12h rate-of-change, CKD 3-month chronicity).

`PROVISIONAL_INFERENCE`: this is real, working, deterministic longitudinal machinery, but it implements a **generic band-crossing signal**, not the **domain-specific governed trend rules** the ratified package actually specifies (contract §12; renal ruleset §7 baseline windows; hepatic ruleset §9; haematology ruleset §7; thyroid ruleset §7; cardiometabolic ruleset §7). It is a correct low-level building block for the trend work that **is** governed (§8, trend boundary below), not a substitute for it.

### 3.9 Whether trend currently affects prominence or ranking

`REPOSITORY_VERIFIED_CURRENT_STATE`: trend feeds `precedence_engine`'s **conflict detection** between systems (`conflict_trend_opposition`, `conflict_abnormal_vs_improving`) — i.e. it currently affects cluster-level arbitration outcomes, not clinical-finding tier or lead selection as the contract defines them. No code path implements contract §7.2 point 5 (persistence/worsening trend as a within-tier ordering criterion) or §12.2 (trend may adjust within-tier ordering or fire a governed override, never lower a finding below its urgency/severity floor).

### 3.10 Structured DTO support

`REPOSITORY_VERIFIED_CURRENT_STATE`: `AnalysisDTO` (`results.py:403+`) and `InsightGraphV1` are both extensible, versioned Pydantic models already carrying multiple additive stamped sub-objects (confidence, cluster summary, relationship registry, precedence output, arbitration result, calibration items) — this is a proven, precedented pattern for adding one more additive field (a `clinical_concern_set`) without breaking existing consumers, consistent with the architecture-hardening report §6 recommendation.

### 3.11 Frontend ordering and render-only behaviour

`REPOSITORY_VERIFIED_CURRENT_STATE`: `WhyThisLeadWonSection.tsx` and `PrimaryFindingAndWhy.tsx` render fields already computed server-side (`report.sections.page1.primary_concern_mode`, `co_primary_signal_ids`, `runner_up_why_not_lead_line`) — the frontend does not itself compute lead/tiebreak logic, it renders it. This is consistent with, and does not require architectural correction for, the render-only boundary required by contract and product ratification. It does mean the frontend currently has UI copy and conditional logic (`isCloseCallMode`, `shouldRenderWhyThisLeadWonSection`) built around the **existing** `technical_tiebreak_lead` concept, which will need updating once the concern-construction service supplies a `no_forced_lead` state instead — a bounded, identified frontend change, not an open design question.

### 3.12 Active quarantines

`REPOSITORY_VERIFIED_CURRENT_STATE`: `Grep` for FIB-4/CV-risk-calculation terms across `backend/core` returned six files (`orchestrator.py`, `ratio_registry.py`, `questionnaire_mapper.py`, `medication_caveat_assembler_v1.py`, `clustering/rules.py`, `prompt_builder/v2.py`). None was opened in this pass to confirm whether a live, consumer-facing risk-score or FIB-4 output exists. **This is a verification gap, not a resolved fact** — carried into §9 STOP-adjacent risk and into the core package's exclusion boundary (§4 of the package definition) as a mandatory Phase 0 check.

### 3.13 Existing scenario and regression harnesses

`REPOSITORY_VERIFIED_CURRENT_STATE`: `backend/tools/run_arbitration_scenarios.py` plus `backend/tests/unit/test_arbitration_scenario_runner*.py` and `backend/tests/fixtures/arbitration_scenarios_v2.json` constitute a **directly reusable pattern** for the 109-scenario acceptance strategy (§7): JSON-defined scenarios, each run end-to-end and asserted against an `expected` block, with a manifest and per-scenario artefact bundle. No equivalent harness exists yet for clinical-concern scenarios; building one **as an adaptation of this existing pattern** (not a new pattern) is in scope for the core package.

### 3.14 Research-to-runtime identity and provenance dependencies

`REPOSITORY_VERIFIED_CURRENT_STATE`: unchanged from the architecture-hardening report — `activation_key` (ADR-RT-002) is the correct identity primitive to carry into `ClinicalFinding` provenance; ADR-RT-004's compile-manifest fields are the correct provenance shape for any new compiled prioritisation artefact.

## 4. Gap analysis

| Capability | Exists? | Grain | Reusable as-is? |
|---|---|---|---|
| Signal identity/registry | Yes | Signal/activation-key | Yes — direct input |
| Cross-domain conflict/dominance arbitration | Yes | Cluster/system | No — wrong grain; do not repurpose |
| Lead/co-lead selection | Yes | Signal, with forced-tiebreak mode | No — conflicts with ratified no-forced-lead policy; replace |
| Numeric trend delta | Yes | Biomarker value pair | Yes — direct input |
| Prior-snapshot persistence | Yes | InsightGraph slice | Yes — direct input |
| Band-transition detection | Yes | Biomarker score band | Partially — informs but does not implement governed domain trend rules |
| Consolidated clinical finding | No | — | N/A — new build |
| Tier 0-3 / urgency / severity separation | No | — | N/A — new build |
| Missing-data / indeterminate-severity state machine | No | — | N/A — new build |
| Cross-domain finding consolidation (pre-arbitration) | No | — | N/A — new build |
| Governed trend-to-tier / trend-to-ordering effect | No | — | N/A — new build, bounded by §8 |
| Scenario acceptance harness | Analogous pattern exists (arbitration scenarios) | — | Yes — adapt pattern |
| Structured DTO extension point | Yes | `InsightGraphV1`, `AnalysisDTO` | Yes — additive field |
| Frontend render-only boundary | Already respected | — | Yes — extend, not redesign |

## 5. Minimum required architecture

Unchanged from the approved architecture-hardening report §6-§11, restated here as confirmed still current:

1. New `ClinicalFinding` / `ConsolidatedConcernSet` models (additive, not replacing `Insight`/`InsightGraphV1`).
2. New concern-construction service between `SignalEvaluator.evaluate_all()` and `build_insight_graph_v1()`.
3. Identity/provenance extending `activation_key` and ADR-RT-004's compile-manifest fields.
4. Tier 0 fail-closed at output assembly (not evaluation), mirroring `filter_runtime_eligible_rows()`'s existing evaluate-then-gate pattern (confirmed live in `insight_graph_builder.py:239`).
5. Questionnaire context consumed via the existing disclosure-state pattern (`runtime_context_evaluator.py`), no new interface invented.
6. One additive `clinical_concern_set` field on `InsightGraphV1`/`AnalysisDTO`.

## 6. Reuse versus new-build decisions

| Component | Decision |
|---|---|
| `SignalRegistry` / `activation_key` | Reuse as upstream input, unmodified |
| `comparable_lab_delta`, `link_prior_snapshot_insight_graphs` | Reuse as trend-data primitives |
| `state_transition_engine` band logic | Reuse only as a supporting signal for governed domain trend rules where those rules reduce to a band-crossing test (e.g. improving/worsening framing); do not treat its output as itself a governed clinical trend determination |
| `precedence_engine` / `arbitration_engine` / cluster-level primary driver | Do not reuse for clinical-finding lead selection; leave in place for its existing cluster/system purpose, unmodified |
| `ClinicianReportV1.primary_concern_mode` / `technical_tiebreak_lead` | Do not reuse the forced-tiebreak algorithm; may reuse the presentation shape once its logic is replaced |
| `run_arbitration_scenarios.py` harness pattern | Reuse as the structural template for a new clinical-concern scenario runner |
| `InsightGraphV1` / `AnalysisDTO` | Extend additively; do not fork or replace |

## 7. Trend integration position

Per the trend boundary in the governing prompt: existing clinical authority is sufficient to implement, without inventing new policy:

- The change-defined vs change-modified distinction (contract §12.1-§12.2).
- The domain-specific change-defined criteria and their baseline-validity windows already recorded in the ratified domain rulesets (NICE AKI 48h/7d; CKD 3-month chronicity; potassium 6-12h rate-of-change; statin-monitoring 3-month window; FIB-4 3-year recalculation cadence), including the windows explicitly labelled `[J]` (HealthIQ judgement, not a sourced UK guideline) — these are still governed, adjudicated positions within the ratified authoring framework, not open questions, and are implementable as recorded.
- "Absent baseline is never evidence of stability" (contract §12.2, §18.9) as a hard invariant.
- Persistence/worsening trend as a **within-tier ordering criterion only** (contract §7.2 point 5) — implementable now.

**Not implementable without new medical/product adjudication, and not invented here:**
- **Trend-triggered tier promotion via a governed override.** Contract §12.2 permits trend to "act through a governed override subject to §13," but no override register entry in any of the six domain rulesets or the cross-domain ruleset actually enumerates a trend-triggered promotion rule. This is a genuine, real gap — not a documentation oversight — and is recorded as a follow-on item (§14 of the sprint plan; `TREND-TIER-PROMOTION-1` candidate), not implemented speculatively.

## 8. Quarantine boundaries

Preserved unmodified, per the governing prompt's exclusion list and the ratified package's own quarantine register: comprehensive Tier 0 operational pathway (R1); FIB-4 activation (R3); cardiovascular-risk calculation activation (R2); consumer-facing disease-name output (R4); specialist pregnancy interpretation; broad questionnaire redesign; laboratory-provider integrations; final regulatory release approval. The core package implements the **fail-closed representation** of Tier 0 and the quarantine-consistent representation of FIB-4/CV-risk findings (contract §8, hepatic `HEP-AS-10`, cross-domain `XD-AS-17`/`-18`/`-36`), not their activation.

## 9. Test and acceptance strategy

See package definition §7 for the full scenario-classification table. Summary: the 109-scenario estate from the approved approval pack v1.2 is the governing specification; a new scenario-runner harness, structurally modelled on `run_arbitration_scenarios.py`, executes each scenario end-to-end against the new concern-construction service and asserts the full governed field set (finding, urgency, severity, tier, role, missing-data state, override, action class, prohibited-behaviour negative assertions, dependency/quarantine state) recorded in approval pack v1.2 §7-§9.

## 10. Implementation risks

1. **Frontend coupling to `technical_tiebreak_lead`.** Existing UI logic (`isCloseCallMode`, `shouldRenderWhyThisLeadWonSection`) is built around a concept the ratified policy now supersedes. Bounded, but must be scoped explicitly, not discovered mid-implementation.
2. **Unverified FIB-4/CV-risk code paths.** Six files matched a keyword search; none were opened to confirm whether a live, user-facing computation exists that would need active quarantining rather than simple non-construction. Must be resolved in Phase 0 of the core package, not assumed.
3. **`[J]`-labelled trend windows carry lower evidence grade.** Implementing them is consistent with how every other `[J]`-labelled item in the ratified package has been treated throughout this engagement (as closed, adjudicated authority), but the lower evidence grade should be visible in provenance, not silently equal-weighted with `[E]`-graded rules.
4. **Six domain rulesets remain individually unreconciled to v0.5 text** (per the architecture-hardening report §3, non-blocking). The core package's compiler must apply the source-precedence rule from that report (§8): ratified package governs, domain-ruleset detail compiles only where incorporated.

## 11. STOP conditions

None triggered. All required authority exists at the ratified-package level; no clinical, product, or architecture decision needed to be invented to complete this inspection.

## 12. Repository evidence summary

All file:line citations in §2-§3 above are drawn from direct reads performed in this task (orchestrator.py, insight.py, insight_graph_v1.py, insight_graph_builder.py, signal_evaluator.py [prior pass], results.py, report_v1.py, clinician_report_v1.py, longitudinal_numeric_v1.py, snapshot_linker.py, state_transition_engine.py, precedence_engine.py, WhyThisLeadWonSection.tsx, test_arbitration_scenario_runner.py) plus targeted `Grep`/`Glob` searches whose results are quoted verbatim above. No claim in this report is inherited from a prior task without either a fresh read this session or explicit citation to the architecture-hardening report where it was independently established.
