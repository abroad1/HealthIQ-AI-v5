# HealthIQ AI — Transformation Programme Brief

**Date:** 2026-05-05  
**Status:** LIVE — programme steering document  
**Audience:** Leadership, programme owners  
**Synthesised from:** CURRENT_STATE_PACK, AUTHORITY_MAP, SPRINT_STATUS, DECISION_REGISTER, PRODUCT_REVIEW_AND_STRATEGIC_RESET_2026-04, PRODUCT_REALITY_AND_DIRECTION_AUDIT, METABOLIC_PATHWAY_COVERAGE_AUDIT, Sentinel Phase 1 report, Results Journey Paper v6, IDL Design Lock, Questionnaire UX backgrounds, Strategy v1.5 FINAL ADOPTED

---

## 1. Executive Summary

### The real strategic problem now

HealthIQ has completed a significant and genuine stabilisation programme. The three engine correctness bugs that were destroying trust have been fixed. The product shell has moved from 2/10 to something substantially more complete. Domain cards, questionnaire UX, alias hardening, WHY Wave 1, and a quality layer are all done and merged. The documentation estate is no longer self-contradicting.

The risk of stalling on engine work while the product shell went empty has been avoided. That is a real achievement.

The problem that now presents itself is different: **the product has been assembled but not yet composed.**

The engine is strong on a bounded set of signals. The shell has the right structural bones. But the connective tissue — the user experiencing their own analysis as a coherent, credible, personalised story — is not yet there. And the questionnaire, which was always positioned as personalisation infrastructure, has been redesigned aesthetically but not yet strategically validated: it may be too wide, too weakly connected to visible output, and not well-scoped for what the launch product actually needs to demonstrate.

The risk now is the old pattern returning: fixing the next visible local issue, expanding WHY in every direction, patching questionnaire wiring, tweaking domain cards — without a governing view of what the bounded launch product actually is and which investments are load-bearing for that specific goal.

### What the product must avoid doing next

- Expanding WHY Wave 2 across all gap signals without deciding which signals are genuinely launch-core
- Treating the questionnaire as a local UX or wiring problem rather than a strategic scope decision
- Building Section 5 / IDL features without confirming they are required for the bounded launch product
- Adding Sentinel Phase 2 coverage before the launch surface itself is coherent
- Running multiple concurrent workstreams without a sequencing decision

### What the programme must now focus on

1. Deciding what the bounded launch product is — which surfaces are core, which are deferred
2. Strengthening only the surfaces that are core to that bounded product
3. Resolving the personalisation/questionnaire question as a strategic scope decision, not a wiring fix
4. Completing the minimum commercial and compliance requirements before first paying user

---

## 2. Current Product Reality

As of 2026-05-05, the following is the honest state of each product dimension.

### Engine

The deterministic engine is the genuine asset. The three trust-destroying correctness bugs from the April 2026 audit are fixed. Signal activation honours bound flags. One-sided lab ranges are scored correctly. WHY fallback is in place for lead signals without governed WHY. The engine's pipeline is real: 45+ sub-engines, 137 registered signals, 186 package directories, replay manifest, governed DTO contract.

WHY depth is the current limiting factor. Wave 1 (lipid panel, Vitamin D) is complete with governed root-cause hypothesis assets. Wave 2 (iron panel, inflammatory markers, renal, expanded thyroid) has not started. Approximately 131 of 137 signals still produce no governed structured WHY — they rely on signal-level explanation text and interaction chains only, not the full root_cause_v1 compilation. The renal pathway has zero interaction-map edges.

The engine is strong enough to launch on the signals it currently handles well. It is thin on signals that appear in real commercial panels but fall outside Wave 1.

### User-facing report

The results page has the right structural shape: primary finding, domain-level narrative, WHY section, next steps. Domain cards D-1 through D-7 are complete with headline coherence, consequence copy, driver meta, and next steps.

The IDL / Section 5 pattern layer (the most differentiated part of the results journey per the Results Journey Paper v6) has a design lock and a planned backend sprint (BE-IDL-1) but has not been built. Section 5 currently either renders nothing or a stub. The full 9-section guided reasoning journey described in the Results Journey Paper is not yet delivered.

The clinician summary report is structurally populated when the lead signal is one of the six WHY targets. When the lead signal is outside those six, root_cause section falls back to a placeholder. This is the most visible manifestation of WHY depth limits.

Biomarker dial section and cluster summary exist. The advanced/expandable depth story is present. What is thinner is the narrative coherence across the full journey from primary finding through to deep evidence.

### Personalisation / questionnaire

Q-1 (guided section-by-section flow) and Q-2 (premium visual layer) are both complete. The questionnaire UX is no longer a wall-of-text form. It now communicates purpose and precision.

The strategic problem is unchanged. The questionnaire feeds context, burden weighting, and insight synthesis input in the backend. It does not rewrite signal activation thresholds. The user completing 56 questions across 7 sections experiences the results as if they had not. No section of the results experience explicitly says "your sleep of 5 hours influenced this" or "your waist circumference was factored into your cardiovascular pattern." The analytical payoff is invisible.

This is not a wiring bug. It is a scope-and-integration gap that requires a strategic decision: either narrow the questionnaire to what genuinely and visibly drives output, or build the feedback loop that makes its influence explicit. The current Q-1/Q-2 work has solved the wrong part of the problem first.

### Testing / quality

Sentinel Phase 1 is live and all 32 regression tests pass. It covers alias/canonical sweep, escaped-defect regression (GGT, bilirubin, slug leakage), and produces structured JSON reports per run. This is real regression protection for the surfaces it covers.

Sentinel Phase 2 is not started. Wave 1 narrative coherence guard (requires Playwright), DTO schema comparison, and frontend mock sync check are all deferred. The quality layer is sound for what it covers but does not yet protect the full launch surface.

No release confidence gate exists. There is no formal definition of what must be true before the first paying user uses the product.

### Commercial / launch readiness

Stripe paywall is implemented (Sprint 7). Pricing model is implemented in code but the commercial decision (first free / subscription tier / per-analysis) is noted as pending leadership confirmation in the Decision Register.

PDF export is implemented (Sprint 4). Actions hub is implemented (Sprint 5). Trend view is implemented (Sprint 6). These were the major product-shell gaps from the April reset and they are closed.

The GDPR privacy disclosure on LLM parsing at upload is flagged as uncertain — whether copy exists in the current upload flow has not been confirmed closed.

---

## 3. Bounded Launch Product Definition

The bounded launch product should be:

**A deterministic metabolic interpretation service that takes a realistic commercial blood panel, produces a single-session guided reasoning journey for the user, explains the lead finding and why it matters, surfaces domain-level health patterns, and gives the user clear next steps — all backed by a clinically defensible governed engine.**

### What it should do well at launch

- Accept a realistic UK commercial blood panel and produce a trustworthy, non-contradictory result
- Lead with one primary finding and explain it with governed WHY reasoning (even if that WHY comes from a fallback for less-covered signals)
- Show domain-level metabolic interpretation (the Wave 1 domain card stack)
- Let the user explore biomarker evidence behind the interpretation
- Give the user 3–5 actionable next steps
- Export a shareable summary (PDF)
- Support longitudinal comparison across analyses
- Handle payment and account management
- Enable the user to optionally complete personalisation questions that visibly affect at least one part of the output

### What it does not need to do yet at launch

- Cover all 137 signals with full structured root_cause WHY (Wave 2 can follow launch)
- Surface Section 5 / IDL pattern layer (requires BE-IDL-1; can ship as Phase 1.1)
- Produce clinician-handoff-quality reports for signals outside the six WHY targets
- Support full phenotype retail naming on Section 5 cards (IDL governs this; not yet built)
- Deliver quantified personalisation across the full 56-question scope
- Achieve Sentinel Phase 2 coverage before launch (valuable, but not blocking)

The bounded launch product is defined by the results journey being coherent and trustworthy on the signals it does cover, not by being complete on all signals.

---

## 4. Core vs Weak / Over-Wide / Deferred

### Launch-core — these must work well before launch

| Area | Why core |
|---|---|
| Engine correctness on launch signals | The moat. Any trust-destroying bug on signals that appear in real UK commercial panels is a blocker. |
| Wave 1 domain card narrative | The primary user-facing analytical output. D-1 through D-7 complete. Must remain coherent under regression. |
| WHY reasoning for high-prevalence signals | The product's central differentiation claim. At minimum, lipid panel, Vitamin D, and the most common real-panel signals must have governed WHY or a clear, non-embarrassing fallback. |
| Primary finding → WHY → next steps journey | The core user experience chain. Must be coherent end-to-end. |
| PDF export | The first shareable artefact and the mechanism for clinician handoff. Complete. |
| Commercial surface (Stripe, account tiers) | Without this there is no commercial product. Complete in code; awaiting pricing decision. |
| GDPR disclosure on LLM parsing | A compliance requirement and a trust surface for a privacy-forward product. Currently uncertain. |

### Strategically important but not yet launch-ready

| Area | Gap | Why it is not yet launch-ready |
|---|---|---|
| Section 5 / IDL pattern layer | BE-IDL-1 not built | Design lock exists. Backend contract not yet created. Cannot ship Section 5 without it. |
| WHY Wave 2 (iron, inflammatory, renal, thyroid) | Not started | Real and important. But the launch product can be coherent without it if the fallback is credible. |
| Sentinel Phase 2 (Playwright, DTO schema) | Deferred | Important for confidence; not a blocker if Sentinel Phase 1 is clean and the surfaces are manually verified. |
| Release confidence gate | Not defined | Needed before launch. Should be authored as a document, not a sprint. |

### Over-wide relative to current maturity

**The questionnaire scope** is over-wide. 56 questions across 7 sections — demographics, medical history, symptoms, lifestyle, physical assessment, cognitive assessment, family history — is a broad intake. The backend consumes this for context and synthesis. But the visible output influence is not demonstrable per section, which means the breadth is not yet justified by the payoff. A narrowed questionnaire covering what genuinely and verifiably affects output would serve the launch product better than the current 7-section scope.

This is not a criticism of Q-1/Q-2 UX work (which is good). It is a strategic observation that the questionnaire scope was inherited from a vision-level ambition, not validated against what the current engine can actually demonstrate.

### Thin and needs strengthening before launch

**WHY coverage for lead-signal fallback cases.** The most visible gap: when the lead finding is outside the six WHY targets, the clinician summary section falls back to a placeholder. For a product whose central claim is "we explain why," this is the most credibility-damaging remaining gap. It does not require full Wave 2 to fix. It requires either expanding `_ROOT_CAUSE_TARGETS` to cover the most prevalent real-panel lead signals, or making the fallback experience more graceful and explicit.

**Frontend carriage of analytical truth.** The DTO contains governed interpretation that the frontend partially surfaces. Domain cards are good. But the narrative coherence across the full results journey — does the primary finding stated above the fold connect clearly to the WHY section, which connects to the domain cards, which connects to the next steps — has not been formally verified as a coherent user story. This is not a bug; it is a product quality gap.

### Better deferred than patched

**Section 5 / IDL.** Do not patch it. The IDL design lock defines the correct architecture. BE-IDL-1 is the correct sprint. Do not ship a Section 5 using cluster data without the IDL contract — it will drift on naming and classification and require rework.

**Renal pathway.** Zero interaction-map edges is a known gap. Do not patch it with partial coverage before Wave 2 is scoped. Either leave it absent and ensure the engine handles renal-primary panels gracefully, or address it properly in Wave 2.

**Sentinel Phase 2.** Do not build Playwright orchestration as a pre-launch blocker. It is valuable phase 1.1 work, not launch-gating.

---

## 5. Personalisation / Questionnaire in Programme Context

### What the problem actually is

The questionnaire problem is not a UX problem. Q-1 and Q-2 have solved the UX. The form is good.

The problem is that the questionnaire scope was authored top-down from a vision of what contextual intelligence should eventually do, not bottom-up from what the current engine can demonstrably return to the user in the results experience.

The result is a 56-question intake that the user completes with reasonable diligence, receives a results page that would look materially identical if they had skipped it, and has no reason to repeat the experience with any additional care.

This is a **trust gap**, not a wiring gap. The questionnaire implicitly promises that precision inputs produce precision output. If the user cannot see that promise fulfilled, the questionnaire actually undermines trust rather than building it.

### What the questionnaire should and should not influence at launch

At launch, the questionnaire should visibly influence at least:
- Age/sex-specific interpretation thresholds (directly derivable from demographics section alone)
- One or two explicitly flagged personalisation callouts in the results journey (e.g. "your sleep pattern was factored into your recovery and inflammation assessment")
- The framing of next steps (lifestyle factors already influence the actions hub in principle)

It should not, at launch, be expected to rewrite signal activation, produce sex-stratified phenotype assignments, or generate individual-pathway reasoning that differs materially from a non-questionnaire run. That is a Phase 2+ capability.

### Whether the current questionnaire is fit for purpose at launch

The current questionnaire scope is **too broad for what it can deliver at launch**. Seven sections with cognitive and family history questions imply a depth of personalisation that the current engine does not produce. Including them signals more than the product can currently fulfil.

A launch-bounded questionnaire would be narrower: demographics (age, sex — required), physical assessment (BMI-relevant inputs — required), and lifestyle (sleep, smoking, alcohol — genuinely influences output). The remaining sections can be presented as optional or staged post-results enrichment.

This is a product scope decision, not a sprint task. It requires a leadership decision before a sprint is authored.

### Why this must be handled as a strategic question

If the questionnaire scope is left at 56 questions with invisible payoff, the Q-1/Q-2 UX improvement will have made the problem more visible, not less. A well-designed form that promises personalisation and then produces no visible personalisation is worse than a form that never promised it.

The decision is: either build the visible payoff loop (the analytical feedback system that shows the user exactly which inputs mattered), or narrow the questionnaire scope to what can be honestly fulfilled at launch.

---

## 6. Recommended Next Programme Workstreams

Three workstreams, in the correct order.

---

### Workstream 1: Launch-Core Analytical Surface Hardening

**What it is trying to solve:** The engine has genuine analytical depth on a bounded set of signals, but the product's primary trust claim — "we explain why your leading concern matters" — fails silently when the lead signal falls outside the six WHY targets. This workstream hardens the launch-core signals so that the most common real-panel lead findings produce a credible, governed, non-placeholder experience.

**Why it comes first:** This is the engine's core differentiator. If the user's lead finding produces a placeholder WHY, everything else in the product — domain cards, next steps, clinician summary — is weakened. The product should launch with a strong, honest explanation surface on the signals it actually covers, not a broad but thin surface.

**What it covers:**
- Expand `_ROOT_CAUSE_TARGETS` to include the most prevalent real UK commercial panel lead signals (prioritised by actual panel prevalence: LDL high, HDL low, triglycerides high, ferritin low, CRP elevated, HbA1c borderline — these are the signals that will appear as lead findings in real panels)
- Author or verify governed WHY hypothesis YAML assets for those targets against the Knowledge Bus schema
- Ensure clinician summary `root_cause` section is populated for any signal that is a plausible lead in a real UK panel
- Audit the fallback experience: if WHY is still not governed for a lead signal, the fallback should say something honest and useful, not render a placeholder

**What it depends on:** Existing Knowledge Bus pipeline (KB SOP, Automation Bus). No new architecture required. WHY assets need KB authoring. Signal expansion needs Automation Bus.

**What it should deliberately avoid:**
- Attempting to cover all 137 signals (Wave 2 completionism is not the goal here)
- Touching the renal pathway as a patch (defer to proper Wave 2 scoping)
- Expanding beyond the signals that realistically appear as lead findings in UK commercial panels

---

### Workstream 2: Launch-Bounded Personalisation Redesign

**What it is trying to solve:** The questionnaire's analytical payoff is invisible to the user. This is a trust-destroying disconnect between the intake promise and the output experience. This workstream resolves it — not by patching the wiring but by making a product scope decision about what personalisation means at launch.

**Why it comes second:** The analytical surface must be strong first (Workstream 1) because the personalisation story is built on top of the analytical story. Personalisation that influences a thin WHY surface is not meaningful. Once the core signals are strong, the personalisation layer has something real to connect to.

**What it covers, as a two-part programme decision:**

*Part A — Leadership decision:* Should the launch questionnaire be narrowed to the sections the engine can demonstrably influence (demographics + physical + lifestyle core), or should it be kept broad with explicit staged disclosure ("Additional questions unlock deeper pattern matching — these will influence more of your analysis as we expand coverage")? This is not a sprint. It is a product scope decision that must be made before any sprint is authored.

*Part B — Feedback loop implementation:* Once the scope decision is made, build the visible personalisation feedback loop: one or more explicit callouts in the results journey that show the user which questionnaire inputs influenced their analysis. This does not require a new engine capability — it requires surfacing what the engine already computes (lifestyle modifier weights, context flags) back to the user in a readable form.

**What it depends on:** Leadership decision on questionnaire scope. Workstream 1 output (the lead signal WHY surface) must be strong enough to be worth personalising. Backend analytics context (already wired) needs a results DTO field or narrative callout mechanism.

**What it should deliberately avoid:**
- Treating this as a frontend wiring task (it starts with a product scope decision)
- Building deep lifestyle-to-signal rewiring (Phase 2+)
- Expanding the questionnaire scope further before the existing scope is demonstrated to the user

---

### Workstream 3: Commercial and Launch Readiness Gate

**What it is trying to solve:** Several independently small but collectively blocking items stand between the current state and a first paying user being onboarded with confidence. This workstream closes them in a single coordinated push.

**Why it comes third:** Items 1 and 2 are product-quality investments. This workstream is a launch-readiness checklist. Doing it before the product quality is right is premature. Doing it after wastes time.

**What it covers:**
- **Pricing model confirmation:** Leadership decision on the commercial model (first free / subscription / per-analysis). The code supports it; the business decision is pending.
- **GDPR / privacy disclosure:** Add the required one-sentence disclosure to the upload flow before Gemini parsing. This is a compliance requirement and a trust surface. It is small but currently uncertain whether it has been addressed.
- **Release confidence gate:** Author the formal document defining what must be true before first paying user. This is a leadership document, not a sprint. It should cover: engine correctness threshold, analytical coverage minimum, commercial surface readiness, compliance requirements, quality layer state.
- **Sentinel Phase 2 scoping:** Decide which Phase 2 checks are blocking for launch (DTO schema comparison is highest value) and which can follow launch. Do not build all of Phase 2 as a pre-launch requirement.
- **Frontend design system documentation:** Author a single page describing the design token source of truth, component library state, and styling rules. This removes a recurring contributor friction point.

**What it depends on:** Workstreams 1 and 2 reaching a settled state. Release confidence gate cannot be authored until the product surface is coherent.

**What it should deliberately avoid:**
- Treating this workstream as an opportunity to scope new features
- Over-specifying the release confidence gate (it should be narrow enough to be achievable)
- Running Sentinel Phase 2 in full before confirming it is blocking

---

## 7. Explicit Non-Goals

The following should **not** be done next, even if they appear tempting.

**WHY Wave 2 in full.** Iron panel, inflammatory markers, renal, expanded thyroid — all are real gaps. None of them are launch-blocking if Workstream 1 covers the most prevalent lead signals with governed WHY. Full Wave 2 is Phase 1.1 work, not launch-gate work.

**Section 5 / IDL pattern layer.** BE-IDL-1 is the correct sprint and the IDL design lock is the correct contract. But Section 5 is not on the critical path for the bounded launch product. It is the most strategically differentiated surface and it should ship correctly, not quickly. It belongs in Phase 1.1.

**Expanding the questionnaire scope.** The current 56-question scope is already too wide for what the engine can demonstrate. Adding more sections or more granular inputs before the payoff loop is visible is counterproductive.

**Sentinel Phase 2 as a pre-launch blocker.** Playwright orchestration and DTO schema comparison are valuable. They are not blocking the first paying user. They belong in Phase 1.1 quality work alongside Section 5.

**Orchestrator decomposition.** The 2,200-line orchestrator is a known maintainability risk. It is not a user-facing gap. This is Phase 2 technical debt work.

**Phenotype retail naming.** The IDL design lock defines the correct classification model. Phenotype retail naming on Section 5 cards cannot ship without the IDL. This is correctly gated.

**Any sprint that does not move Workstreams 1, 2, or 3 forward.** The period between now and launch should be deliberately sequenced. A sprint that adds depth to renal pathway WHY, improves the trend view UI, or expands the admin interface does not belong in the next programme window unless it is explicitly required by one of the three workstreams.

---

## 8. Open Uncertainties

These require either targeted verification or a leadership decision before they can be closed.

| Uncertainty | What is needed |
|---|---|
| Pricing model (first free / subscription / per-analysis) | Leadership commercial decision. Sprint 7 implemented the infrastructure; the business model is pending. |
| GDPR disclosure on LLM parsing | Targeted verification: read the current upload flow to confirm whether a disclosure exists. If absent, this is a compliance blocker. |
| Release confidence gate definition | Leadership document. No formal definition exists. Should be authored as part of Workstream 3 before first paying user. |
| Questionnaire scope for launch | Leadership product decision. Must be made before Workstream 2 Part B can be scoped. The decision is: narrow to demonstrated capabilities, or keep broad with staged disclosure framing. |
| Which signals appear as lead findings in real UK commercial panels | Targeted verification: run the golden runner against a representative sample of real-panel fixtures and determine the actual distribution of lead-signal types. This governs the WHY expansion priority list for Workstream 1. |
| Section 5 / BE-IDL-1 priority | Leadership decision: is Section 5 a launch requirement or a Phase 1.1 feature? If launch requirement, BE-IDL-1 enters the near-term workstream queue. If Phase 1.1, it stays deferred. |
| ADR-006 gap | No explanation for the absent ADR-006 in the registry. Not a launch blocker, but worth confirming whether it was intentionally omitted or represents a missing architectural decision. |

---

*This brief synthesises the programme state as of 2026-05-05. It is a steering document, not a sprint prompt. Sprint authoring, hardening, and gate work follow from programme decisions made against this brief — not from this brief itself.*
