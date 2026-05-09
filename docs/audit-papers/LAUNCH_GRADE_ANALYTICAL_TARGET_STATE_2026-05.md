# HealthIQ AI — Launch-Grade Analytical Target-State

**Date:** 2026-05-04
**Audience:** Leadership / Product / Intelligence Core
**Status:** Target standard, not a sprint plan
**Anchored against:**
`docs/strategy/PRODUCT_REVIEW_AND_STRATEGIC_RESET_2026-04.md`,
`docs/intelligence/PRODUCT_REALITY_AND_DIRECTION_AUDIT.md`,
`docs/METABOLIC_PATHWAY_COVERAGE_AUDIT_2026-03-20.md`,
`docs/strategy/RESET_SPRINT_PLAN_2026-04.md`,
`docs/HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan_v1.5_FINAL_ADOPTED.md`,
`docs/STATE_OF_TRUTH_REVIEW_2026-05.md`, `docs/SPRINT_STATUS.md`,
`docs/testing/healthiq_sentinel_phase1_implementation_report.md`,
`docs/frontend/HealthIQ_Final_Results_Journey_Recommendation_Paper_v6.md`,
`docs/frontend/Interpretation_Display_Layer_Design_Lock.md`,
`docs/intelligence/PRIMARY_CONCERN_AND_RANKED_AMBIGUITY_POLICY_v1.md`,
`docs/frontend/clinician_language_style_guide_v1.md`,
`docs/intelligence/2026-04-12_results_why_narrative_runtime_investigation.md`.

---

## 1. Executive summary

**The problem.** HealthIQ AI has a deterministic engine that already exceeds most consumer-blood startups in machinery: 103 canonical biomarkers, 137 signals, 187 Knowledge Bus packages, governed clustering, a structured `report_v1`/`clinician_report_v1` pair, and a Replay Manifest. Yet at user-experience level the engine still appears as a long results page whose **lead finding can be unexplained**, whose **runner-up hypothesis is structurally invisible to the hero**, and whose **WHY coverage was, until R-8, six signals out of 137**. Reset Sprints R-1, R-1B, R-2A and R-8 closed the worst correctness and Wave 1 WHY gaps, but launch-grade depth is **not yet present**: WHY Wave 2 is **not started**, the IDL pattern layer is gated, narrative runtime defaults to `deterministic_mock`, and renal has zero interaction-map edges.

**What the target standard solves.** It defines the **minimum analytical bar** below which a HealthIQ result should not ship to a paying consumer. It is calibrated for a **UK-first, B2C, post-test interpretation product** whose moat claim is "deterministic, explainable, governed reasoning." If we cannot meet this bar on a typical UK commercial blood panel, we should not be charging for the engine moat — we should still be building it.

The standard is intentionally **narrower than the strategic vision** in `v1.5_FINAL_ADOPTED.md` and **stricter than the v5.2 PRD's feature checklist**. It is the floor, not the ceiling.

---

## 2. Current-state analytical weakness

### 2.1 Coverage breadth has outrun coverage depth

`SignalRegistry` loads **137 unique signals** across **187 packages** (`docs/intelligence/PRODUCT_REALITY_AND_DIRECTION_AUDIT.md` §Q2). Until reset Sprint 8 (R-8 — `feature/why-coverage-expansion-wave-1`), the **`_ROOT_CAUSE_TARGETS`** list in `backend/core/analytics/root_cause_compiler_v1.py` carried exactly **six** governed hypothesis pipelines (`hcy`, `hba1c_high`, `hepatic_alt_context`, `thyroid_tsh_context`, `insulin_resistance`, `systemic_inflammation`). After R-8, lipid and Vitamin D are governed (per `RESET_SPRINT_PLAN_2026-04.md` Sprint 8 mandatory targets and `SPRINT_STATUS.md` "COMPLETE"), but **iron, inflammatory beyond `systemic_inflammation`, renal, and expanded thyroid (FT3/FT4) remain in Wave 2 — `NOT STARTED`** in `SPRINT_STATUS.md` "Active / Upcoming Work".

The asymmetry is the problem: a user can have a fired signal that is **prominently displayed** with no governed reasoning behind it, because the **package estate grew faster than the reasoning estate**.

### 2.2 The hero does not see its own runner-up

`docs/intelligence/2026-04-12_results_why_narrative_runtime_investigation.md` is unambiguous: `meta.insight_graph.report_v1.top_findings` carries the full ranked list, but the **hero (`InsightPanel`) reads only `clinician_report_v1.sections.page1`**. `co_primary_signal_ids` is populated only when the tie-bucket has ≥2 IDs; otherwise the "Close call between top findings" badge can show with **no "Also closely reviewed" row**. This means a panel where two signals are nearly tied can present a confident lead **without the second hypothesis ever being named to the user**, even though it exists in the DTO.

This is not a UX bug. It is an **analytical contract** problem: the hero contract does not formalise runner-up surfacing, and the policy in `docs/intelligence/PRIMARY_CONCERN_AND_RANKED_AMBIGUITY_POLICY_v1.md` is **adopted but not yet reflected in runtime contracts** ("describes what should be aimed for", not what runs today, §3).

### 2.3 The clinician summary can fall back silently

`compile_clinician_report_v1` selects `primary = top_findings[0]`, then resolves `primary_root` only if its `signal_id` matches a row in `root_cause_v1.findings`. If `top_findings[0]` is e.g. `signal_alp_low`, the clinician section's `root_cause` is `null` and hypothesis lines fall back to **"No hypothesis set available for this concern in v1."** (`docs/intelligence/PRODUCT_REALITY_AND_DIRECTION_AUDIT.md` §Q5). R-1 Bug 3 introduced a graceful fallback so this is **visible rather than invisible**, but the underlying truth — *the engine does not have a WHY for the lead it chose* — is still operative on the long tail.

### 2.4 Interpretation/phenotype layer is harness-only at runtime

Phenotype expectations live in `backend/tests/fixtures/panels/phenotypes/phenotype_expectations_v1.yaml` and `knowledge_bus/phenotypes/phenotype_map_v1.yaml`, exercised by `test_phenotype_suite_v1.py`. They are **not** the primary runtime driver of the production `AnalysisOrchestrator` (`docs/intelligence/PRODUCT_REALITY_AND_DIRECTION_AUDIT.md` §Q6). The IDL Design Lock (`docs/frontend/Interpretation_Display_Layer_Design_Lock.md`) defines a 9-entity, governed pattern layer with strict scientific classes — but it is a **design lock**, gated behind `BE-IDL-1` (backend) and `FE-R8` (frontend). Section 5 ("Patterns across your body") of the Results Journey is therefore **not present at retail level**.

### 2.5 Narrative runtime is typically a mock

`meta.narrative_runtime.runtime_mode` is `deterministic_mock` unless **all** of `HEALTHIQ_NARRATIVE_LLM`, `HEALTHIQ_ENABLE_LLM`, `LLM_ENABLED`, and policy mode allow Gemini (`docs/intelligence/2026-04-12_results_why_narrative_runtime_investigation.md` §3). The default user therefore receives **deterministic mock summaries** in `insights[]`, which by construction have **similar depth across categories**. Strategy positioning ("LLM is governed Layer C polish") is correctly encoded, but practically the user-facing prose is template-shaped.

### 2.6 Lifestyle / questionnaire input does not change reasoning

`QuestionnaireMapper` maps to `lifestyle_factors` and `medical_history` and is passed to insight synthesis. `LifestyleModifierEngine` runs only when `lifestyle_inputs` is supplied (`docs/intelligence/PRODUCT_REALITY_AND_DIRECTION_AUDIT.md` §Q4). There is **no evidence that lifestyle fields rewrite signal activation** at the reasoning core. A user who answers 59 questions experiences the analysis as if they had not.

### 2.7 Pathway gaps already documented and unchanged in their core form

`docs/METABOLIC_PATHWAY_COVERAGE_AUDIT_2026-03-20.md` shows every pathway as **PARTIAL or MISSING**; renal is **MISSING with zero active interaction-map edges**. Even after R-8, the pathway-by-pathway status table remains directionally correct: lipid and Vitamin D moved to "governed WHY"; **iron, full thyroid, expanded inflammatory, and renal did not**.

---

## 3. Launch-grade analytical standard

A HealthIQ result, on a typical UK commercial blood panel, should meet **all** of the following at launch.

### 3.1 Coherence
- **No contradictory active signals on a single panel value.** Already enforced post-R-1; must remain a regression-guarded invariant for any new signal definition. The "asymmetric activation" case is a configuration error, not a runtime result (`RESET_SPRINT_PLAN_2026-04.md` Sprint 1 acceptance).
- **No contradiction between sections.** The hero, the system overview, and the clinician section must not name different lead findings, different severities, or different evidence.
- **Severity is one model, not three.** Hero severity, IDL `severity_state`, and clinician page1 framing are derived from a single governed scoring path; UI never re-derives severity.

### 3.2 Traceability
- **Every visible finding traces to specific biomarkers and at least one governed signal ID.** No retail card, no clinician hypothesis, no "What's driving this" line should exist without a deterministic chain `biomarker(s) → signal_id → finding`.
- **Every WHY claim traces to a governed hypothesis YAML or to a labelled fallback.** Silent omission is unacceptable; "*No hypothesis available for this concern*" is acceptable provided it is surfaced visibly (R-1 Bug 3 contract).
- **Replay integrity.** Every result rendered to a paying user must be reproducible from `replay_manifest`. This already exists; launch-grade requires it remain unbroken when new signals/packages are added.

### 3.3 Depth where it claims depth
- **The lead finding is explained, not just stated.** The user must read, in plain English, *what* was found, *why it matters*, *which markers drove it*, and *what would change confidence*.
- **The runner-up exists at hero level when it materially exists.** When the deterministic top-finding ranking puts two signals close enough to be a "tie" or "close call", the runner-up signal **must be named**, not implied by a badge. This formalises §3 of `PRIMARY_CONCERN_AND_RANKED_AMBIGUITY_POLICY_v1.md` into a runtime contract.

### 3.4 Confidence and missing-data honesty
- **Confidence is qualitative and stable.** Numeric engine confidence does not appear on retail surfaces (per IDL Design Lock §5 `confidence_display`: "default behaviour is to omit"). A coarse band (e.g. *"Strong / Mixed / Limited"*) is acceptable.
- **Missing data is named.** When the lead pattern is held back by absent markers, the report says which markers would raise confidence (the existing `confidence_and_missing_data` block on `clinician_report_v1.sections.page1` is the governed source).
- **One-sided ranges are scored honestly.** Post-R-1 fix is the floor; "insufficient numeric bounds" must never appear for a panel that supplies a one-sided range.

### 3.5 Personalisation that the user can detect
- **At least one questionnaire/lifestyle input must be visibly reflected in the rendered output**, even if as a contextual modifier line ("read in the context of self-reported low sleep"). Otherwise the questionnaire is a tax with no payoff (§2.6).
- **Lab origin is acknowledged when ranges are non-standard.** `lab_origin_metadata` already exists; the user-facing surface should not silently use an unusual reference range without saying so.

### 3.6 Calm, clinical-style register
- **Adopt the clinician language style guide** (`docs/frontend/clinician_language_style_guide_v1.md`) for *all* governed prose, not only the clinician report: approved verbs (*suggests / consistent with / cannot exclude*), no diagnosis claims, no motivational/coaching tone.
- **Mock-mode prose is acceptable** if it meets the style guide and never claims to be more than it is. If we rely on Gemini at launch, that is a separate gate (§4.4).

### 3.7 Editorial discipline
- **One primary concern per analysis** unless ranked ambiguity is explicit (`PRIMARY_CONCERN_AND_RANKED_AMBIGUITY_POLICY_v1.md` §4.2). No "10 things that are wrong with you" hero.
- **No raw IDs, no internal slugs, no `ph_*_v*`, no `unmapped_*` strings on retail surfaces** — already guarded by Sentinel Phase 1 slug-leakage tests; launch-grade keeps this guard green.

---

## 4. Minimum launch analytical scope

Launch credibility does not require "everything in the strategic plan." It requires a **bounded, defensible set** strong enough that a UK B2C blood-panel user finds value in the majority of real uploads.

### 4.1 Domains that must be strong at launch ("launch-grade depth")

| Domain | Floor | Source / rationale |
|---|---|---|
| **Glycaemic / insulin resistance** | Governed signals + governed WHY (HbA1c, IR, fasting glucose where present); IR phenotype display label (`ph_metabolic_early_ir_v1`) live | Already governed; flagship phenotype per IDL §4 |
| **Lipid panel** (LDL, HDL, triglycerides, total cholesterol) | Governed signals + **governed WHY (R-8 Wave 1 mandatory)** + one-sided range scoring | `RESET_SPRINT_PLAN_2026-04.md` Sprint 8 mandatory; `SPRINT_STATUS.md` shows R-8 COMPLETE |
| **Vitamin D** | Governed signals + **governed WHY (R-8 Wave 1 mandatory)** | Same; among the most common single-marker findings in UK panels |
| **Hepatic (ALT-driven)** | Governed signal + governed WHY for `hepatic_alt_context`; correct mapping for trace aliases (GGT/bilirubin) | `_ROOT_CAUSE_TARGETS`; alias regression now Sentinel-guarded |
| **Thyroid (TSH-driven, basic)** | Governed signal + governed WHY for `thyroid_tsh_context`; thyroid-axis pattern entity at IDL level | `_ROOT_CAUSE_TARGETS`; IDL §4 "Thyroid Axis Pattern" |
| **Systemic inflammation (CRP-driven)** | Governed signal + governed WHY for `systemic_inflammation` | `_ROOT_CAUSE_TARGETS` |
| **Homocysteine / vascular-inflammation context** | Governed signal + governed WHY; "Vascular Inflammation Risk" entity at IDL level | `_ROOT_CAUSE_TARGETS`; IDL §4 |

These seven domains are the **launch floor**. They cover the most prevalent UK commercial findings and align to what the engine already governs. A panel dominated by any of these must produce a **non-fallback WHY**.

### 4.2 Domains that must at minimum produce a **safe finding** at launch

For panels where the lead signal sits **outside** §4.1, the system must:
- still rank the finding correctly (deterministic ordering),
- still display value, range, and a state classification,
- emit the **R-1 Bug 3 fallback** ("Deeper hypothesis analysis is not yet available for this marker") **visibly** in both the consumer hero and the clinician report,
- never produce a hero card with no WHY content at all.

This is the **non-silence guarantee**.

### 4.3 Domains that may remain Phase 2 / later

The following may ship at launch with **no governed WHY** provided they meet §4.2:
- **Iron panel** (ferritin, transferrin saturation) — Wave 2, NOT STARTED in `SPRINT_STATUS.md`.
- **Expanded inflammatory** (WBC sub-lines, neutrophils) beyond `systemic_inflammation`.
- **Renal** (creatinine, eGFR, urea, urate) — flagged at zero interaction-map edges.
- **Expanded thyroid** (FT3, FT4) beyond TSH.

These remain **Wave 2** per the reset plan. They are recognised analytically (signals fire) but are not required to carry governed WHY at launch. They must, however, fall under §4.2 (no silent omission).

### 4.4 LLM/narrative posture at launch
- **Acceptable launch posture:** `deterministic_mock` runtime, with deterministic prose that meets the clinician style guide. No false claim that text is AI-personalised.
- **Required if Gemini is enabled at launch:** `narrative_runtime` is logged on every result, prose is governance-bounded (no raw biomarker leakage — already enforced by `LLM boundary` enforcement tests), and a structured failure path exists (`deterministic_mock` fallback) when the LLM call fails. The double-opt-in gate already documented in the April review must remain.
- **Not acceptable at launch:** silent toggling of LLM with no provenance metadata, or LLM prose that contradicts deterministic structured fields.

### 4.5 IDL pattern layer (Section 5) at launch
- **Required at launch:** IDL contract published on the result payload (BE-IDL-1) for **at least the IR phenotype** (`ph_metabolic_early_ir_v1`) plus the syndrome/organ-pattern entities the engine already supports (per IDL §4 mapping table).
- **Not required at launch:** all 9 entities `enabled_for_frontend = true`. Section 5 may render with **a subset** as long as the section render-gate behaviour is honest (omit cleanly when no record qualifies — IDL §6.4).

---

## 5. Edge-case handling standard

These are **classes** of edge case that must be handled deterministically, not a defect list.

### 5.1 Asymmetric / one-sided lab ranges
- A range with only `min` or only `max` is valid input.
- Scoring must produce a real status, not "insufficient numeric bounds".
- Floor confirmed by R-1 Bug 2 fix; launch-grade requires this is a **regression-guarded invariant** for any future scoring change.

### 5.2 Asymmetric activation (high vs low cannot both fire)
- A signal definition with `enable_upper_bound: false` must not fire on `value > upper`, and vice versa.
- The engine treats simultaneous fire as a **configuration error**, not a runtime output (R-1 Bug 1 fix).

### 5.3 Lead signal outside governed WHY set
- Behaviour: structured fallback, visible, named — never silent.
- The clinician report must null-guard `top_findings[0]`; the hero must show *something* honest.

### 5.4 Close-call / ranked ambiguity
- When `top_findings[0]` and `top_findings[1]` are within a governed delta, the hero must surface both, with explicit "close call" framing (per `PRIMARY_CONCERN_AND_RANKED_AMBIGUITY_POLICY_v1.md` §4 and §6).
- Tie-break by deterministic ID order is permitted **only when labelled as such** in implementation; it must not appear to the user as clinical primacy.

### 5.5 Incomplete panel
- The engine produces a result with **explicit acknowledgement of which biomarker classes are absent**.
- Confidence band degrades accordingly; primary concern remains acceptable to surface only if at least the canonical drivers for that finding are present.
- "Limited by missing data" is the approved register (clinician style guide); retail surfaces use plain-English equivalents.

### 5.6 Present-but-non-canonical / aliased input
- Trace-style keys (e.g. `Gamma-GlutamilTransferase GGT (Venous)`, `bilirubin_total_(venous)`) must resolve to the canonical biomarker.
- Sentinel Phase 1 alias-canonical sweep is the regression floor; launch-grade requires it remains green.

### 5.7 Lab-origin variability
- Non-standard or non-UK reference ranges must not silently change interpretation; lab origin is captured on the DTO (`lab_origin_metadata`) and acknowledged on the user-facing surface where it materially affects status.

### 5.8 Marker combinations that shift meaning
- Iron + inflammation: ferritin must be read jointly with CRP/inflammation context (per IDL `Iron Deficiency (with inflammation)` syndrome state).
- Thyroid + lipid: thyroid-axis context must modulate lipid interpretation (per IDL `Thyroid–Lipid Pattern`).
- Launch-grade requires **at minimum these two** combination cases produce coherent joint interpretation, not two contradictory cards.

### 5.9 Persistence / version differences
- A re-fetched analysis must render identically to its originally rendered form for a given `replay_manifest` version.
- Schema/DTO drift between persisted snapshots and live code is the failure mode Sentinel Phase 2 will guard; **at launch**, the floor is: persisted analyses do not crash and do not silently change their lead finding.

### 5.10 Limited-confidence states
- An analysis whose lead finding is "weak" (low confidence, sparse markers) must still produce a result, but its hero framing must be calibrated — e.g. "Mixed signals; limited by panel scope" — not a confident lead.

---

## 6. WHY coverage standard

### 6.1 Must be explainable at launch (no fallback acceptable)
- Every signal in §4.1 must produce a **governed `root_cause_v1` block** with: hypothesis name, summary, `evidence_for`, `evidence_against`, `missing_data`, `ranking_rationale` — the structure already produced by `root_cause_compiler_v1` for the original six.
- The clinician report's `sections.root_cause` must be non-null when the lead is in §4.1.

### 6.2 Acceptable governed fallback
- For signals outside §4.1 but inside the runtime registry, the fallback must:
  - name the signal in plain English,
  - state its activation state and lab status,
  - explicitly say "deeper hypothesis analysis is not yet available for this marker",
  - not pretend to be a hypothesis,
  - render in both retail and clinician surfaces.

### 6.3 Unacceptable
- A lead finding rendered with **no WHY content** of any kind (silent omission).
- A hero "Close call" badge with **no runner-up named**.
- A clinician summary `primary_concern` line whose corresponding `root_cause` is `null` and whose UI hides the absence.
- Hypothesis prose that contradicts the deterministic `evidence_for` / `evidence_against` lists (which would mean Layer C is overruling Layer B — banned by ADR-001 / ADR-002).

### 6.4 Behaviour when WHY depth is missing
- The product **degrades visibly** (says so) rather than degrading silently.
- The fallback is the **same prose** every time for a given signal (deterministic), so users do not infer false personalisation.

---

## 7. User-facing interpretation standard

This is the analytical contract the frontend must carry — **not** the layout spec.

### 7.1 What every result must analytically deliver
1. **One primary concern**, named in human language, with severity.
2. **A governed WHY for that primary concern**, OR a labelled fallback (per §6).
3. **Top driving signals** (≥1, ≤3) with biomarker name, value, range status, one-sentence interpretation. Each signal traces to specific markers.
4. **A runner-up acknowledgement** when the deterministic ranking flags ambiguity — named, not implied.
5. **A confidence framing** (qualitative band, not a number).
6. **A missing-data line** when material markers are absent.
7. **A balanced view** — at least one calm "what looks well-regulated" framing, per Results Journey v6 Section 2 ("What's working well").
8. **No contradiction** between hero, system overview, and clinician section.
9. **No raw IDs / slugs / internal labels** on retail surface — Sentinel-guarded.
10. **A non-diagnostic disclaimer** present on every analytical surface.

### 7.2 Section-by-section minimum (mapped to Results Journey v6)

| Journey section | Analytical floor at launch |
|---|---|
| Body overview | Whole-system framing line + balanced systems summary; comes from governed structured fields, not free LLM prose |
| What's working well | At least one well-regulated system named, governed by deterministic state |
| Primary finding & WHY | §6.1 or §6.2 — non-silent in all cases |
| Why this lead won | At minimum: ranking rationale string from `root_cause_v1` or governed fallback explaining tie-break |
| Patterns across your body (IDL Section 5) | At minimum: IR phenotype if active, plus organ/syndrome entities the engine supports — per §4.5; section omits cleanly if no record qualifies |
| Marker-level evidence | Every marker shown with value, range, lab origin, and status — one-sided ranges supported |
| Body-level insights | Optional at launch; if shown, governed-only |
| What to do next | Sourced from existing intervention annotation; cards must cite source signal; no medical claim language |
| Clinician summary | Style-guide-compliant; null-guarded; never empty when retail surface is non-empty |

### 7.3 What the report must **not** do
- Lead with a number.
- Show a confident hero on a panel whose drivers are absent.
- Surface contradictory states for the same analyte.
- Silently use a non-standard lab range.
- Display engine internals (`ph_*`, `unmapped_*`, `internal_id:`).
- Imply LLM personalisation when running in `deterministic_mock`.

---

## 8. Explicit out-of-scope boundary

Launch credibility does **not** require any of the following. These are deferrable without weakening the standard above.

### 8.1 Out of scope for launch — analytical depth
- **Wave 2 governed WHY** for iron, expanded inflammatory, renal, FT3/FT4 (`SPRINT_STATUS.md` "Active / Upcoming Work").
- **Renal interaction-map edges** beyond zero (research-promotion path).
- **All 9 IDL entities `enabled_for_frontend = true`.** Subset display is acceptable per IDL §6.4.
- **Outcome-calibration layer** (v5.3 §3.4 of `MASTER_ROADMAP_v5.2_to_v5.3.md`).
- **Longitudinal state-transition reasoning** beyond delta tables (v5.3 §3.3).
- **Deterministic conflict-modelling layer** as a first-class user surface (v5.3 §3.2).

### 8.2 Out of scope for launch — runtime polish
- **Live Gemini at full opt-in by default.** Mock-mode prose is acceptable provided §4.4 holds.
- **Real-time SSE pipeline progress.** R-2A (backend SSE removal) is the floor; honest polling is acceptable.
- **Lifestyle inputs that rewrite signal activation.** A *visible modifier line* satisfies §3.5; full reasoning-core integration is later phase.
- **Phenotype layer as primary runtime driver** (currently harness-only; remains acceptable).

### 8.3 Out of scope for launch — product / commercial / governance
- **Class II readiness, full clinical validation, full regulatory packaging** — explicitly Phase 3 in `v1.5_FINAL_ADOPTED.md`.
- **B2B/B2B2C deployment surfaces, clinician portals, EHR integration** — Phase 1 is B2C-primary per `HealthIQ_Phase1_Launch_Posture.md`.
- **Sentinel Phase 2 (Wave 1 narrative coherence guard, Playwright orchestration, DTO schema comparison)** — `SPRINT_STATUS.md` "NOT STARTED — Deferred". Phase 1 Sentinel coverage is the launch floor.

These exclusions are a feature of the standard. They prevent the target from becoming infinite.

---

## 9. Open risks

These items could not be confidently resolved from the repo and remain genuine uncertainties.

### 9.1 R-8 actual depth vs Sprint 8 minimum
`SPRINT_STATUS.md` marks **R-8 "WHY Coverage Wave 1" COMPLETE**. `RESET_SPRINT_PLAN_2026-04.md` Sprint 8 lists Lipid + Vitamin D as **mandatory** and "at minimum 1 additional Wave 2 group if capacity allows" as success criteria. Whether R-8 actually delivered the optional Wave 2 group, and whether *all four* lipid signals received governed hypotheses (not just `signal_total_cholesterol_high` etc.), is **not verifiable from documentation alone** — it requires reading `_ROOT_CAUSE_TARGETS` post-merge. **Launch-grade depends on this being true** for §4.1.

### 9.2 IDL contract status
The `Interpretation_Display_Layer_Design_Lock.md` is approved; **BE-IDL-1 (backend contract) and FE-R8 (Section 5 frontend) status is not in `SPRINT_STATUS.md`**. If the IDL is not yet on the result payload at runtime, §4.5 / §7.2 require either acceleration or further deferral.

### 9.3 Runner-up surfacing in hero contract
The April 2026 narrative-runtime investigation showed the hero ignores `top_findings[1]`. Whether reset Sprint 3 (Results Page Restructure, marked COMPLETE) addressed this, or only restructured layout, is **not verifiable from documentation alone**. §3.3 / §6.3 are floor requirements that may need a separate small workstream.

### 9.4 Lifestyle/questionnaire visible payoff
`PRODUCT_REVIEW_AND_STRATEGIC_RESET_2026-04.md` §2.9 flagged the questionnaire has "no visible payoff". Reset Sprints did not directly address this. §3.5 elevates it to a launch-grade requirement; whether existing structured fields can satisfy it without engine work, or whether a small surface-only enhancement is needed, is open.

### 9.5 Privacy disclosure on LLM upload parsing
`SPRINT_STATUS.md` lists this as **UNCERTAIN**; it is a GDPR-adjacent gap flagged in the April review. It is not analytical depth, but at launch it is part of the trust posture and must be resolved before commercial sale (it sits on the boundary of Phase 1 launch posture, not the analytical standard, but is worth flagging).

### 9.6 Confidence band semantics
Engine confidence is numeric. The IDL Design Lock defaults to **not exposing confidence bands**. Whether launch-grade means "no confidence band visible" or "coarse band visible" is a **product decision pending**. The standard above keeps it qualitative and stable, but the exact band ladder is not yet defined anywhere governed.

### 9.7 Mock-mode honesty
If `deterministic_mock` ships at launch, the user must not be told they are reading personalised AI prose. Where this is currently surfaced (or not) on the frontend was not verifiable in this review — it is part of launch trust posture, not just analytical content.

### 9.8 Combination-case coherence
§5.8 requires iron+inflammation and thyroid+lipid to produce coherent joint interpretation. The IDL Design Lock defines these entities; **whether the runtime currently produces a single joint card vs two contradictory ones** for these cases was not directly verified.

---

**Bottom line.** The engine is genuinely strong. The launch-grade standard above is intentionally **floor-level, not aspirational** — it codifies what the April 2026 audits and the reset plan have already implicitly demanded, and pulls in the policy decisions made in the IDL Design Lock and the Primary Concern policy. Meeting it is achievable from the current state. **Falling short of it would mean charging users for a moat we have built but not yet delivered.**
