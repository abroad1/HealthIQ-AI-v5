# HealthIQ AI — Launch-Grade Analytical Gap Map & Sequencing

**Date:** 2026-05-04
**Measuring stick:** `docs/audit-papers/LAUNCH_GRADE_ANALYTICAL_TARGET_STATE_2026-05.md` (the standard)
**Verified against:** repo state at HEAD, current-state pack, and Sprint Status register.
**Status:** Gap map only — not a sprint plan.

A material correction precedes the paper: the target-state document was written before reading post-R-8 code. Several weaknesses it described are partly out of date. Where verification changed the picture, this paper says so explicitly.

---

## 1. Executive summary

**The biggest launch-grade gaps are not where the target paper assumed.** Repo verification shows that:

- **WHY coverage breadth has expanded dramatically.** `_ROOT_CAUSE_TARGETS` in `backend/core/analytics/root_cause_compiler_v1.py` now wires **37 signals** to governed hypothesis pipelines (lipid panel + lipid-transport, full iron, expanded hepatic, full thyroid TSH/FT3/FT4/TgAB/TPO-Ab, renal creatinine/urea/urate, vitamin D, plus the original six). 37 hypothesis YAMLs exist on disk. The launch-floor seven domains (§4.1 of the standard) are **wired at registration**, not just "lipid + Vitamin D".
- **The two engine trust bugs are fixed at code level.** Asymmetric activation (`_evaluate_lab_range_activation_state` honours `enable_upper_bound`/`enable_lower_bound`) and one-sided bounds (`has_valid_numeric_lab_range` returns true for one-sided cases) are both materially addressed.
- **Hero runner-up surfacing exists at contract level.** `clinician_report_v1.sections.page1` carries `runner_up_topic_line` and `runner_up_why_not_lead_line` (BE-W2-RQ2); `InsightPanel.tsx` reads them.
- **IDL is on the result DTO.** `publish_interpretation_display_layer_v1` runs in the orchestrator; the bundle is attached as `interpretation_display_layer_v1` on `AnalysisDTO`; `InterpretationPatternsSection.tsx` consumes it.

**The real remaining launch-grade risk is therefore not "coverage breadth" but "verified depth and coherence on real panels."** None of the above tells leadership *what a UK commercial panel actually produces* end-to-end. The largest current-state gaps are:

1. **Verified depth on real commercial panels is unmeasured.** `_ROOT_CAUSE_TARGETS` lists 37 signals, but no document or test confirms that, on a realistic UK panel, the **lead finding** consistently produces **non-fallback** governed WHY in both the consumer hero and the clinician report.
2. **Coherence guards are placeholders, not active.** Sentinel Phase 1's `test_wave1_contradiction_status.py` and `test_persisted_result_replay_status.py` are explicitly status-reporting placeholders per the Sentinel report; the **cross-section contradiction-free** invariant in §3.1 of the standard is **not regression-protected**.
3. **Combination-case coherence is unverified.** Iron+inflammation and thyroid+lipid IDL records exist, but no test covers "do these produce one coherent joint card, not two contradictory cards" (§5.8 of the standard).
4. **Lifestyle/questionnaire visible payoff is still absent.** No frontend code path was found that surfaces lifestyle modifier effect to the user.
5. **Confidence band UX semantics are still undefined.** IDL contract leaves it optional and defaults to omission.
6. **Narrative runtime defaults to `deterministic_mock`** per `narrative_runtime_policy.py` gating; mock-mode honesty surfacing on the user-facing page is not verified.

**What the next phase must focus on:** *Verification, coherence guards, and surface honesty* — not new analytical breadth. The engine has overshot the target paper's launch-floor scope; the work that remains is proving and protecting it on real panels, closing the contradiction-free / coherence guarantees, and resolving small but launch-critical surface decisions (confidence band, lifestyle reflection, mock-mode framing, privacy disclosure).

---

## 2. Gap map against the target standard

Each row reports MET / PARTIALLY MET / NOT MET / UNCLEAR with concise repo-grounded justification.

### 2.1 §3 Launch-grade analytical standard

| Standard area | Status | Justification |
|---|---|---|
| §3.1 Coherence — no contradictory active signals on a single value | **MET** | `signal_evaluator.py:163–167` honours `enable_upper_bound`/`enable_lower_bound` (verified). |
| §3.1 Coherence — no contradiction between sections | **NOT MET (no guard)** | No regression test enforces that hero, system overview, and clinician section name the same lead. `test_wave1_contradiction_status.py` is a placeholder per Sentinel Phase 1 report. |
| §3.1 Coherence — single severity model | **UNCLEAR** | IDL severity is enum (`SeverityStateV1`), `clinician_report_v1` page1 carries its own framing, hero severity is rendered separately. No document confirms a single derivation path; no test enforces equality. |
| §3.2 Traceability — finding → signal → biomarker | **PARTIALLY MET** | Contracts carry `signal_id` and `supporting_markers`; there is no end-to-end UI assertion that every visible card cites them. |
| §3.2 Traceability — every WHY claim → governed YAML or labelled fallback | **PARTIALLY MET** | 37 hypothesis YAMLs wired; fallback string `"No hypothesis set available for this concern in v1."` exists in `report_compiler_v1.py:535`. **But no test confirms it always renders when applicable, nor that the consumer hero surfaces the fallback equivalently.** |
| §3.2 Traceability — replay integrity | **MET** | `replay_manifest` attached to `AnalysisDTO` (`orchestrator.py:2242`); enforced by existing replay tests. |
| §3.3 Depth — lead finding explained, not stated | **PARTIALLY MET** | Coverage breadth supports it; rendering depth on real UK panels unverified. |
| §3.3 Depth — runner-up named on hero when ambiguity exists | **MET (at contract level)** | `runner_up_topic_line` / `runner_up_why_not_lead_line` on page1; `InsightPanel.tsx:81–94` reads them and `showRunnerUp` no longer depends on `co_primary_signal_ids` alone. **Quality of the *content* on real panels is unverified.** |
| §3.4 Confidence — qualitative band stable | **NOT MET** | IDL `confidence_display` is optional and "default behaviour is to omit" per Design Lock §5. No governed band ladder exists in any document. |
| §3.4 Missing-data named | **PARTIALLY MET** | `confidence_and_missing_data` exists on page1 contract. No verification it always populates and renders. |
| §3.4 One-sided ranges scored honestly | **MET (code level)** | `has_valid_numeric_lab_range` (`primitives.py:87–93`) returns True for one-sided cases. **No regression test on a one-sided fixture is in `backend/tests/regression/`** — guard is implicit, not explicit. |
| §3.5 Personalisation visible to user | **NOT MET** | `LifestyleModifierEngine` runs only on `lifestyle_inputs`; no frontend surface was found that visibly reflects questionnaire/lifestyle effect. April 2026 review §2.9 finding stands. |
| §3.5 Lab origin acknowledgement on UI when non-standard | **UNCLEAR** | `lab_origin_metadata` carried on DTO; UI rendering of it under non-standard ranges not verified. |
| §3.6 Calm clinical register (style guide) | **PARTIALLY MET** | `docs/frontend/clinician_language_style_guide_v1.md` adopted for clinician report. **Not enforced on retail prose** in any tested way. |
| §3.7 One primary concern per analysis | **MET** | `_resolve_page1_concern_mode` produces `distinct_lead` / `near_tie_ambiguity` / `technical_tiebreak_lead`; one mode at a time. |
| §3.7 No raw IDs / slugs on retail surface | **MET** | Sentinel Phase 1 `test_slug_leakage_regression.py` (backend + Jest) is active; alias-canonical sweep is active. |

### 2.2 §4 Minimum launch analytical scope

| Domain | Status | Justification |
|---|---|---|
| Glycaemic / IR | **MET (registration)** | `signal_hba1c_high`, `signal_insulin_resistance` in `_ROOT_CAUSE_TARGETS`; IR phenotype is the lone `phenotype_allowed` IDL record. |
| Lipid panel (LDL, HDL, triglycerides, total cholesterol) | **MET (registration)** | All four signals + `signal_lipid_transport_dysfunction` registered. **Verification on a UK lipid-dominant panel still required** (§5.1 below). |
| Vitamin D | **MET (registration)** | `signal_vitamin_d_low` registered with `vitamin_d_low_hypotheses_v1.yaml`. |
| Hepatic (ALT-driven) | **MET (registration)** | `signal_hepatic_alt_context` + GGT, ALP high/low, bilirubin high, hyperbilirubinemia, hepatic metabolic stress all registered. |
| Thyroid (TSH-driven, basic) | **MET (registration)** | TSH context + TSH high/low + FT3/FT4 high/low + TgAB + TPO-Ab all registered. **Far beyond what the target paper required at floor.** |
| Systemic inflammation | **MET (registration)** | `signal_systemic_inflammation` registered. |
| Homocysteine / vascular-inflammation | **MET (registration)** | `signal_homocysteine_elevation_context` registered; "Vascular Inflammation Risk" IDL record present. |
| §4.2 Non-silence guarantee for non-floor signals | **PARTIALLY MET** | Fallback string exists in `report_compiler_v1.py`. **Not asserted in regression tests** that fallback always renders visibly on both consumer and clinician surfaces. |
| §4.4 LLM/narrative posture acceptable at launch | **PARTIALLY MET** | `narrative_runtime_policy.py` correctly defaults to `deterministic_mock` when env flags absent; `meta.narrative_runtime` provenance is attached. **User-facing acknowledgement that prose is deterministic (not personalised AI) is not verified.** |
| §4.5 IDL pattern layer (Section 5) at launch — IR phenotype + governed entities | **PARTIALLY MET** | `interpretation_display_layer_publish_v1.py` + `idl_records_v1.yaml` registry + DTO field + `InterpretationPatternsSection.tsx` all present. **Whether `enabled_for_frontend = true` for the IR phenotype and at least the established organ/syndrome states is not verified from the registry YAML in this pass.** |

### 2.3 §5 Edge-case handling standard

| Edge case | Status | Justification |
|---|---|---|
| §5.1 One-sided ranges | **MET (code) / NOT MET (regression guard)** | Code path verified above; **no test in `backend/tests/regression/` exercises a one-sided panel fixture**. |
| §5.2 Asymmetric activation | **MET (code) / NOT MET (regression guard)** | `_evaluate_lab_range_activation_state` fixed; **no `test_asymmetric_activation_regression.py` exists** in regression directory. |
| §5.3 Lead signal outside governed WHY | **PARTIALLY MET** | Fallback string exists. Whether the consumer hero surfaces it equivalently to the clinician section is unverified. |
| §5.4 Close-call ranked ambiguity | **MET (contract) / UNCLEAR (semantics)** | `near_tie_ambiguity` and `technical_tiebreak_lead` modes wired; runner-up surfacing wired. **Whether the governed delta that triggers ambiguity is calibrated for real panels is unclear** — no document defines the threshold. |
| §5.5 Incomplete panel | **PARTIALLY MET** | `confidence_and_missing_data` exists. No test confirms confidence degrades visibly on sparse fixtures. |
| §5.6 Aliased / canonical input | **MET** | Sentinel `test_alias_canonical_sweep.py`, `test_ggt_alias_regression.py`, `test_bilirubin_alias_regression.py` active. |
| §5.7 Lab-origin variability | **UNCLEAR** | DTO carries `lab_origin_metadata`; surfacing on retail UI not verified. |
| §5.8 Combination cases (iron+inflammation, thyroid+lipid) | **NOT MET (verification)** | IDL records exist for both. No test exists that asserts a fixture with both elevated CRP and low ferritin produces one joint card; same for thyroid+lipid. |
| §5.9 Persistence / version differences | **NOT MET (regression guard)** | `test_persisted_result_replay_status.py` is **explicitly a placeholder** per Sentinel Phase 1 report. Persisted DTOs vs live code drift is not actively guarded. |
| §5.10 Limited-confidence states | **UNCLEAR** | Compiler can produce mode classifications, but UI calibration on weak panels not verified. |

### 2.4 §6 WHY coverage standard

| Requirement | Status | Justification |
|---|---|---|
| §6.1 Floor seven domains produce governed `root_cause_v1` | **PARTIALLY MET** | Wired at registry level. Whether each fixture lead actually receives a non-null `sections.root_cause` is **not asserted in any test that names this contract on real panels** beyond the original homocysteine test. |
| §6.2 Fallback shape acceptable | **MET (string)** | "No hypothesis set available for this concern in v1." present in compiler. **Visibility on both consumer and clinician surfaces unverified.** |
| §6.3 No silent omission, no hero badge with no runner-up named, no `null` clinician root_cause hidden | **PARTIALLY MET** | Hero contract names runner-up (verified). The "clinician `null` root_cause hidden by UI" failure mode is not regression-protected. |
| §6.4 Deterministic fallback prose (same string every time) | **MET** | The compiler fallback is a literal constant. |

### 2.5 §7 User-facing interpretation standard

| Requirement | Status | Justification |
|---|---|---|
| §7.1.1 One primary concern named in human language | **MET** | Single mode resolution; retail labels governed by IDL contract. |
| §7.1.2 Governed WHY or labelled fallback for the primary | **PARTIALLY MET** | See §6.1 / §6.2 — registration done, end-to-end visibility unverified. |
| §7.1.3 Top driving signals (≤3) | **UNCLEAR** | `top_findings` and `key_findings` exist; whether the page caps to ≤3 is a frontend decision not verified in this pass. |
| §7.1.4 Runner-up named when ambiguous | **MET (contract)** | Verified above. |
| §7.1.5 Confidence framing | **NOT MET** | No governed band ladder. |
| §7.1.6 Missing-data line when material markers absent | **PARTIALLY MET** | Field exists; UI rendering not verified. |
| §7.1.7 Balanced view / "what's working well" | **PARTIALLY MET** | `compile_balanced_systems_v1` exists and is on the DTO; whether Section 2 of the Results Journey ("What's working well") is rendered prominently is not directly verified here. |
| §7.1.8 No contradiction across sections | **NOT MET (no guard)** | No regression test enforces this. |
| §7.1.9 No internal leakage | **MET** | Sentinel slug-leakage guard active. |
| §7.1.10 Non-diagnostic disclaimer | **UNCLEAR** | Style guide mandates it for clinician report; presence on every retail surface not verified. |

### 2.6 §G Testing protection (target paper §G — testing support)

| Requirement | Status | Justification |
|---|---|---|
| Alias / canonical regression | **MET** | Sentinel Phase 1, active. |
| Slug / internal-label leakage | **MET** | Sentinel Phase 1, backend + Jest, active. |
| Asymmetric-activation regression | **NOT MET** | Code fixed; no regression test in `backend/tests/regression/`. |
| One-sided-range regression | **NOT MET** | Code fixed; no regression test. |
| Wave 1 narrative coherence guard | **NOT MET** | `test_wave1_contradiction_status.py` is a placeholder per Sentinel report. |
| Persisted-result replay regression | **NOT MET** | `test_persisted_result_replay_status.py` is a placeholder per Sentinel report. |
| Combination-case coherence (iron+inflammation, thyroid+lipid) | **NOT MET** | No test exists. |
| Cross-section contradiction guard (hero vs clinician vs IDL) | **NOT MET** | No test exists. |
| Sentinel Phase 2 (Playwright orchestration, DTO schema comparison) | **NOT STARTED** | `SPRINT_STATUS.md` confirms. |

---

## 3. Launch-blocking gaps

These are gaps serious enough that the product **should not** claim launch-grade analytical credibility until closed. Each is repo-grounded and corresponds to a *specific* line in the standard.

### 3.1 Verified non-fallback WHY on a representative UK commercial panel
**Standard:** §3.3, §6.1, §6.3.
**Why blocking:** Coverage breadth is wired, but no document or test in the repo states: *"On a typical UK commercial AB-style panel, the lead finding produces a non-null `clinician_report_v1.sections.root_cause` AND the consumer hero shows governed WHY content"*. Without this, the moat claim is theoretical. This is the single most important open verification.

### 3.2 Cross-section coherence guarantee
**Standard:** §3.1, §7.1.8.
**Why blocking:** The "no contradiction between hero / system overview / clinician" invariant is not enforced. The April 2026 narrative-runtime investigation specifically showed the hero used to ignore the runner-up; the contract was fixed, but **no regression** prevents a future contract change from re-introducing the same class of drift. A hero that says one thing and a clinician section that says another would destroy the engine moat in a single screenshot.

### 3.3 Combination-case coherence (iron+inflammation, thyroid+lipid)
**Standard:** §5.8.
**Why blocking:** IDL Design Lock explicitly defined `Iron Deficiency (with inflammation)` and `Thyroid–Lipid Pattern` as syndrome/organ-pattern entities. If the runtime produces *both* a "low ferritin" card *and* a "high CRP" card with no joint reading, the user sees two contradictory frames. This is a launch-credibility issue, not a polish issue.

### 3.4 One-sided range and asymmetric activation regression guards
**Standard:** §5.1, §5.2.
**Why blocking:** Both bugs are *fixed in code*. Without explicit regression tests, the next signal-package authoring sprint can quietly reintroduce them. Given these were the headline R-1 trust bugs, allowing them to escape regression coverage is itself the gap.

### 3.5 Persistence / version drift guard
**Standard:** §5.9.
**Why blocking:** A paying user re-opens an analysis from history; the lead finding renders differently because of code drift since the snapshot. This is invisible until it happens. The placeholder test acknowledges the risk; closing it before commercial launch is non-negotiable for a product that sells reproducibility.

### 3.6 Confidence band semantics (decision, not implementation)
**Standard:** §3.4, §7.1.5.
**Why blocking on credibility, not on engineering:** Without a governed qualitative band, every surface that shows confidence-adjacent text invents its own framing. This is a *product decision* that must be made before the standard can be considered met — it is the lowest-engineering, highest-leverage open item.

### 3.7 Lifestyle/questionnaire visible payoff
**Standard:** §3.5.
**Why blocking:** A 59-question questionnaire that has no visible effect on the user-facing report is a trust gap on day one. The April review flagged it; it remains unaddressed in the surfaces inspected. The launch-grade bar in the standard explicitly requires *at least one* visible reflection.

### 3.8 Mock-mode honesty
**Standard:** §4.4.
**Why blocking:** If the default runtime is `deterministic_mock` (it is — verified in `narrative_runtime_policy.py`), the user must not be told they are receiving personalised AI prose. Whether the current frontend is honest about this is unverified and is a trust risk at first paying-user contact.

---

## 4. Deferrable gaps

These can safely remain Phase 2+ without invalidating launch credibility, **provided** §3 above is closed.

| Gap | Why deferrable |
|---|---|
| Renal interaction-map edges beyond zero | Renal hypotheses are wired (creatinine, urea, urate); interaction-map is research-promotion path. Standard §4.3 explicitly defers. |
| All 9 IDL entities `enabled_for_frontend = true` | Subset display is acceptable per IDL §6.4 and standard §4.5. |
| Outcome-calibration layer (v5.3 §3.4) | Post-launch defensibility, not launch-floor. |
| Longitudinal state-transition reasoning beyond delta tables | Sprint 6 already shipped delta view; deeper state transitions are v5.3. |
| Deterministic conflict-modelling layer as a first-class user surface | Conflict resolution exists internally; user-facing layer is later. |
| Live Gemini at full opt-in by default | Mock-mode acceptable; gate-flipping is a separate opt-in. |
| Real-time SSE pipeline progress | R-2A removal is the launch floor; richer progress is later. |
| Lifestyle inputs that *rewrite signal activation* | Visible modifier line satisfies the standard. Full reasoning-core integration is later. |
| Phenotype layer as primary runtime driver | IDL is the public contract; phenotype harness can remain test-only. |
| Sentinel Phase 2 (Playwright + full DTO comparison + Wave 1 narrative coherence at render-level) | Phase 1 backend regression is the launch floor; Phase 2 strengthens it. |
| B2B / clinician portal / EHR / Class II readiness | Phase 3 by design. |

---

## 5. Verification-required items

These cannot be safely judged from documentation or static reading alone. They must be checked.

### 5.1 Needs repo verification (read code/data files only)
- **`idl_records_v1.yaml` content** — confirm which records have `enabled_for_frontend = true`, and whether the IR phenotype + at least one organ-pattern + at least one syndrome-state are enabled (§4.5).
- **`top_findings` cap** — confirm whether `key_findings` on page1 is bounded to ≤3 in compiler, or whether the cap is a frontend decision (§7.1.3).
- **Frontend lab-origin rendering** — search `frontend/app/components/` for `lab_origin_metadata` consumption to confirm §3.5 / §5.7.

### 5.2 Needs runtime verification (run the pipeline)
- **Real-panel WHY depth** — run the orchestrator on `ab_full_panel_with_ranges.json` and `vr_full_panel_with_ranges.json` and inspect `clinician_report_v1.sections.root_cause` and the consumer hero. Confirm that for each typical lead the result is **non-fallback** governed content.
- **One-sided range fixture** — run a fixture with LDL max-only and HDL min-only; confirm "Not scored - insufficient numeric bounds" does not appear.
- **Asymmetric activation fixture** — run a fixture with a mid-range cholesterol value; confirm `signal_total_cholesterol_high` and `signal_total_cholesterol_low` do not both fire.
- **Combination-case fixture** — run a fixture with low ferritin + high CRP; confirm the IDL bundle yields a single coherent surface, not two contradictory cards.
- **`narrative_runtime.runtime_mode`** — confirm the production-default value (expected: `deterministic_mock`).

### 5.3 Needs UAT against specific panels
- **Hero behaviour on a "close call" panel** — confirm runner-up topic line and why-not-lead line are populated and human-readable, not empty fallback strings.
- **Clinician report on a panel whose lead is outside the original six but inside the 37** — confirm `sections.root_cause` is populated, not the fallback string.
- **Lifestyle reflection** — UAT a panel where a strong lifestyle modifier is supplied; confirm the user-facing report acknowledges it visibly somewhere.
- **Persisted analysis re-fetch** — fetch an analysis stored before a recent code change; confirm it still renders without error and without silent lead-finding change.

### 5.4 Needs product decision (not verification)
- **Confidence band ladder.** Three bands? Five? Words? Icons? Not exposed today by default.
- **Privacy disclosure copy and placement** for LLM upload parsing.
- **Mock-mode acknowledgement copy** on retail surfaces — what, exactly, do we say if Gemini is not active?
- **Threshold for "near-tie ambiguity" mode** — what governed delta triggers `near_tie_ambiguity`?
- **Whether the Wave 1 domain card layer (D-1…D-7) has now superseded any of the Results Journey v6 sections** in practice (the sprint status shows D-1 through D-7 complete; the journey paper is older).

---

## 6. Recommended sequencing

This sequencing is shaped by dependency, not preference.

### 6.1 First — verify before building
The **largest single risk** is that the work is already done and we do not know it. Before any new analytical work:

- Run the orchestrator on AB and VR fixtures and inspect WHY depth (§5.2 above).
- Audit `idl_records_v1.yaml` for `enabled_for_frontend` flags (§5.1).
- Inspect frontend rendering of fallback strings, runner-up content, lab origin, and missing-data lines.

This phase produces a **truth ledger** for whether §3 launch-blocking gaps are smaller than the documents suggest. It is *not* analytical work; it is a verification pass.

### 6.2 Second — close the coherence guard gap
Because §3.2 (cross-section coherence) and §5.8 (combination cases) are launch-blocking and *unprotected by tests*, the next workstream is **coherence regression coverage**:

- Cross-section contradiction guard.
- Combination-case coherence guard.
- Asymmetric activation regression test.
- One-sided range regression test.
- Persisted-result replay regression (graduate the placeholder).
- Wave 1 narrative coherence guard (graduate the placeholder).

This is **testing/protection work**, not new analytical depth. It depends only on the verification phase, not on new product decisions.

### 6.3 Third — close surface-honesty gaps
Once verification shows what exists end-to-end, close the small but launch-critical surface decisions:

- Confidence band ladder (decision + minimal carriage).
- Mock-mode framing on retail surfaces.
- Privacy disclosure on LLM upload.
- One visible lifestyle/questionnaire reflection on the report.

These do not depend on engine work. They depend on **product decisions** (5.4) and a small frontend pass.

### 6.4 Fourth — strengthen analytical depth where verification reveals real gaps
Only after 6.1–6.3 should the team author new analytical work, and only against verified shortfalls. Likely candidates if verification finds them:
- Hypothesis YAML quality polish where evidence/missing-data lines are too thin.
- Renal interaction-map edges beyond zero.
- IDL "Section 5" enablement of additional governed records if today's enabled set is too small.

This is **analytical depth work**, gated on verified need, not assumed need.

### 6.5 Fifth — Sentinel Phase 2 and longitudinal/outcome layers
Deferred per §4. Do not start until 6.1–6.3 are credible; otherwise these layers protect a base that is itself unmeasured.

### 6.6 What should not be tackled prematurely
- New signal/package additions beyond the 37 already wired. The breadth is sufficient or excessive for launch; depth verification must come first.
- New frontend layout work beyond the four surface-honesty items in 6.3. Results Journey v6 and Wave 1 domain cards are already deep enough; layout is not the gap.
- Outcome-calibration, longitudinal state transitions, conflict-modelling layer. All are post-launch.
- Live Gemini activation as default. Adds a large QA surface for no launch benefit.

---

## 7. Suggested workstream grouping

Without writing a sprint plan, the gap classes naturally group as follows.

| Workstream | What it contains | Approximate dependency |
|---|---|---|
| **W1 — Verification ledger** | Run AB/VR fixtures, inspect WHY depth on real leads, audit IDL registry flags, audit frontend fallback rendering, audit `narrative_runtime` defaults, audit lab-origin surfacing | None — can start immediately |
| **W2 — Coherence & regression hardening** | Cross-section contradiction guard, combination-case coherence guard, asymmetric activation regression, one-sided range regression, persisted-result replay regression (graduate from placeholder), Wave 1 narrative coherence guard (graduate from placeholder), one-sided + missing-data fixtures | Depends on W1 (so guards target real failure modes) |
| **W3 — Surface honesty & launch-decision items** | Confidence band ladder decision + minimal UI, mock-mode framing, privacy disclosure on upload, one lifestyle reflection on report | Depends on product decisions in §5.4; mostly orthogonal to W2 |
| **W4 — Targeted analytical depth (if W1 reveals shortfalls)** | Hypothesis polish, IDL `enabled_for_frontend` expansion, renal interaction-map edges if material | Gated on W1 findings |
| **W5 — Sentinel Phase 2** | Playwright orchestration, full DTO schema comparison, render-level Wave 1 coherence checks | After W2; protects a credible base |
| **W6 — Phase 2+ depth (deferred)** | Outcome calibration, longitudinal state-transitions, conflict-modelling user surface, live Gemini default, B2B surfaces | Post-launch |

This grouping is intentionally narrow. **Of the six workstreams, only W1–W3 sit on the launch-grade critical path.** W4 may turn out to be small or empty depending on what W1 finds.

---

## 8. Bottom-line readiness judgement

**Distance from launch-grade analytical standard:** *Smaller than the target-state paper assumed, but blocked by what is unverified rather than by what is unbuilt.*

The repo has overshot the target paper's launch-floor on coverage breadth (37 governed signals vs the seven required). The R-1 trust bugs are fixed at code level. The IDL is on the wire. The hero contract names runner-ups. The Sentinel Phase 1 protects alias and slug-leakage classes. **None of this is a small foundation.**

What stops a credible launch claim today is a much smaller, more specific list:

1. We have not measured WHY depth on real UK panels end-to-end.
2. The contradiction-free guarantee, the combination-case guarantee, and the persistence guarantee are not regression-protected.
3. Four product decisions (confidence band, mock-mode framing, privacy disclosure, lifestyle reflection) remain open and are launch-trust-critical.

**The smallest credible next move that actually matters** is **not** another sprint of analytical depth. It is **Workstream 1: verification** — a focused, code-and-runtime-grounded pass that runs the orchestrator on representative panels, inspects WHY depth, audits IDL enablement, audits frontend fallback rendering, and produces a one-page truth ledger.

That ledger is the only document that can tell leadership truthfully whether the engine *already* meets §3 of the standard, what subset of W2 / W3 / W4 must follow, and whether launch is six weeks away or six months. Any other "next move" risks shipping more code on top of an unmeasured base.
