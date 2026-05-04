# HealthIQ AI — Strategic Architectural Review
## Narrative Asset Inventory, UX Surfacing Strategy, and Target User Experience

**Date:** 2026-04-13
**Status:** Research-complete — strategy document only, no code changes
**Scope:** Full codebase review of explanation-bearing assets and UX surfacing architecture

---

## 1. Executive Summary

HealthIQ AI has a more sophisticated explanation engine than its current user experience reveals. The system contains a well-structured, deterministic-first explanation architecture spanning five distinct layers — from raw biomarker metadata through compiled clinical narratives to optional LLM-polished synthesis. The governance and contracts are sound. The deterministic reasoning is deeper than most health products achieve.

The problem is not the absence of explanatory material. The problem is a mismatch between what has been built and what the user actually experiences.

Key findings:
- **The ClinicianReportV1 is the richest deterministic explanation artifact** and is already surfaced to the frontend, but the frontend renders it in a way that does not communicate its reasoning depth to the user.
- **Root cause hypotheses are deterministic, structured, and evidence-backed** — but they are presented as a secondary block rather than a primary interpretive experience.
- **The signal library contains metadata only** — no mechanism, biological pathway, or interpretation fields exist at the SSOT level. This is a deliberate architectural choice (explanation lives in the compiler layer), but it means education and mechanism-level explanation must be assembled at compile time.
- **The retail educational explainers** (60+ biomarker blocks, system-level education) are rich, long-form, and largely invisible to users unless they actively expand a biomarker row.
- **Gemini/LLM is gated behind a double opt-in** and is off by default in production. The narrative layer is effectively inactive for all production users. The deterministic compilers are doing all the explanation work.
- **The InsightGraphV1 is a comprehensive analytical artifact** passed to the LLM when enabled, but it is not intelligently structured to extract the most consumer-valuable insights — it is a full audit object, not a curated narrative prompt.
- **The balanced systems surface is underexploited.** It exists as a contract and component, but the current implementation does not make it feel like a first-class "what is going well" experience.

The product has strong bones. The gap is in transformation, hierarchy, and presentation — not in the absence of data.

---

## 2. Problem Statement

After a successful upload → parse → review journey, the user arrives at a results page that fails to communicate the depth of analysis that has actually been performed. Specifically:

1. **The interpretation experience feels like a report, not reasoning.** Users see findings and scores but do not understand why the primary concern matters, how systems connect, or what is happening inside their body.

2. **Strong systems are invisible.** The product currently leads almost entirely with problems. Reassurance, context, and positive evidence — which are essential to trust and to the "wow" moment — are largely absent from the primary experience.

3. **Explanation depth is buried.** Rich content (root cause hypotheses, confirmatory test rationale, educational explainers) is present but placed in secondary positions that most users will not reach.

4. **The Gemini layer is inactive.** The LLM narrative synthesis that was intended to transform structured data into consumer-facing language is off by default. What the user sees is policy-driven text with character-count limits — clinically precise but not conversational.

5. **The signal library does not explain.** The SSOT registry contains metadata (roles, risks, modifiers) but no biological mechanism or pathway text. Explanation is only assembled at compile time, creating a hard dependency on compiler logic for all interpretation.

6. **Layer C features are underexploited.** The InsightGraphV1 contains rich derived features — metabolic age, heart resilience score, inflammation burden, fatigue root causes, detox capacity — that are computed deterministically but are not consistently surfaced in a first-class way.

---

## 3. Narrative / Explanation Asset Inventory

### 3.1 Signal Library — `backend/ssot/biomarkers.yaml`

**Type:** SSOT metadata registry (1,761 lines, 100+ signals)
**Generation:** Static governed YAML (no compiler, no LLM)
**Surfacing:** Not directly surfaced to users

**Fields per signal:**
| Field | Example | Richness | Consumer-safe? |
|-------|---------|----------|----------------|
| `description` | "Low-density lipoprotein cholesterol" | Shallow (single sentence) | Yes |
| `category` | "cardiovascular" | Taxonomy only | N/A |
| `system` | "cardiovascular" | Taxonomy only | N/A |
| `roles` | `["lipid_transport_marker"]` | Machine-readable codes | No |
| `key_risks_when_high` | `["cardiovascular_disease", "plaque_formation"]` | Risk codes | No |
| `key_risks_when_low` | — | Risk codes | No |
| `known_modifiers` | `["fasting_state", "training_load"]` | Modifier codes | No |
| `clinical_weight` | 0.8 | Float | N/A |

**Verdict:** The signal library is a lookup registry, not an explanation engine. It has no `mechanism`, `biological_pathway`, `interpretation`, or `implications` fields. This is an architectural gap at the SSOT level. All explanation must be assembled by compilers.

---

### 3.2 ReportV1 — `backend/core/contracts/report_v1.py`

**Type:** Intermediate deterministic compilation artifact
**Generation:** Fully deterministic compiler (`report_compiler_v1.py`)
**Surfacing:** NOT directly surfaced. Internal input to ClinicianReportV1.

**Explanation fields:**
| Field | Location | Max length | Richness |
|-------|----------|-----------|----------|
| `why_it_matters` | `top_findings[].why_it_matters` | 200 chars | Clinical statement |
| `summary_text` | `top_chains[].summary_text` | 200 chars | Interaction narrative |
| Policy-mode field | `primary_concern_mode` | Enum | Machine-readable |

**Verdict:** Rich enough to inform downstream compilation. Not consumer-facing on its own. The `why_it_matters` and chain `summary_text` fields are underused — they disappear into the ClinicianReportV1 compilation and the original formulations are not preserved for alternate rendering.

---

### 3.3 RootCauseV1 — `backend/core/contracts/root_cause_v1.py`

**Type:** Structured hypothesis contract — deterministic
**Generation:** Deterministic loader-based compiler (`root_cause_compiler_v1.py`), 37 registered signal targets
**Surfacing:** Embedded in ClinicianReportV1; rendered by `RootCauseEvidenceSummary.tsx`

**Explanation fields:**
| Field | Max length | Richness | Consumer-safe? |
|-------|-----------|----------|----------------|
| `hypothesis title` | Unbounded | Readable | Yes |
| `summary` | 200 chars | Clinical, concise | Yes |
| `evidence_for[].item` | 120 chars | Factual evidence | Yes |
| `evidence_against[].item` | 120 chars | Counterevidence | Yes |
| `missing_data[].reason` | 120 chars | Data gaps | Yes |
| `confirmatory_tests[].rationale` | 120 chars | Next-step reason | Yes |

**Verdict:** Genuinely underused. The hypothesis-ranked structure, with evidence-for and evidence-against, is a sophisticated clinical reasoning artifact. The current frontend presents it as a secondary block. It deserves primary billing as the "here is what the analysis found and why" section.

---

### 3.4 ClinicianReportV1 — `backend/core/contracts/clinician_report_v1.py`

**Type:** Consumer-facing deterministic clinical narrative — the primary explanation vehicle
**Generation:** Deterministic compiler (policy-driven, no LLM)
**Surfacing:** Fully exposed via `/analysis/result`; rendered by `ClinicianReportRenderer.tsx`

**All explanation fields:**
| Field | Max length | Richness | Notes |
|-------|-----------|----------|-------|
| `header.disclaimer_top` | 400 chars | Standard | Shown once |
| `data_quality.confidence_caveat` | 220 chars | Calibrated | Key trust signal |
| `sections.page1.primary_concern` | 160 chars | Lead statement | Most visible field |
| `sections.page1.key_findings[]` | 160 chars × 5 | Ranked findings | Core interpretation |
| `sections.page1.chains[]` | 200 chars × 2 | System interactions | Often ignored |
| `sections.page1.top_hypothesis_line` | 220 chars | Lead hypothesis | Underused |
| `sections.page1.confidence_and_missing_data` | 220 chars | Uncertainty | Underused |
| `sections.page1.runner_up_topic_line` | 220 chars | Secondary concern | Underused |
| `sections.page1.runner_up_why_not_lead_line` | 280 chars | Arbitration rationale | Almost never shown |
| `sections.confirmatory_tests[].rationale` | 120 chars | Test reason | Underused |
| `medication_supplement_interpretation_caveat` | 280 chars | Context flag | Conditional |

**Verdict:** This is the richest, most underexploited asset in the system. Many of its fields (`top_hypothesis_line`, `confidence_and_missing_data`, `runner_up_topic_line`, `runner_up_why_not_lead_line`) are either not rendered at all or buried in the clinician report block. The arbitration rationale (why the runner-up is not the lead) is one of the most useful reasoning explanations in the system and is almost certainly never seen by users.

---

### 3.5 ExplainabilityReportV1 — `backend/core/contracts/explainability_report_v1.py`

**Type:** Internal audit/debug artifact
**Generation:** Deterministic arbitration engines
**Surfacing:** Not exposed to frontend

**Contents:** Conflict detection, precedence decisions, dominance resolution graph, causal edges, arbitration trace, calibration impact audit, system burden validation.

**Verdict:** This is correctly classified as internal. It should never be surfaced to users directly. However, certain sanitised outputs (e.g., a human-readable arbitration rationale) could be compiled from it for the "how did we decide?" layer.

---

### 3.6 InsightGraphV1 — `backend/core/contracts/insight_graph_v1.py`

**Type:** Comprehensive analytical artifact; sole input to narrative/LLM layer
**Generation:** Deterministic assembly by `build_insight_graph_v1()` in orchestrator
**Surfacing:** Stored in `meta.insight_graph`; not surfaced to users as a complete object

**Key sub-assets within InsightGraphV1:**
| Asset | Content | Surfaced? |
|-------|---------|-----------|
| `biomarker_context` | Code-only explanatory context per marker | No (LLM input only) |
| `state_transitions` | Longitudinal biomarker changes | No |
| `system_states` | Multi-marker system state | No (used in balanced systems) |
| `layer_c_features.metabolic_age` | Computed metabolic age + severity | Partially |
| `layer_c_features.heart_feature` | Heart resilience score + ratios | Partially |
| `layer_c_features.inflammation_feature` | Inflammation burden + NLR | Partially |
| `layer_c_features.fatigue_feature` | Fatigue root causes + status | Partially |
| `layer_c_features.detox_feature` | Liver/kidney scores + eGFR | Partially |
| `system_capacity_scores` | Per-system integer scores | Used in visuals |
| `raw_system_burden_vector` | Pre-calibration system burden | Internal |
| `adjusted_system_burden_vector` | Post-calibration burden | Used in balanced systems |
| `precedence_output` | Ranking decisions | Internal |
| `arbitration_result` | Primary driver + supporting systems | Used in hero section |

**Verdict:** The Layer C features (metabolic age, heart resilience, inflammation burden, fatigue root causes, detox capacity) are deterministically computed, clinically meaningful, and underused. They are present in the contract but the frontend does not consistently present them as first-class "body-level insights." This is the highest-value untapped surface.

---

### 3.7 Layer3InsightsV1 — `backend/core/contracts/layer3_insights_v1.py`

**Type:** Insight cards — deterministic assembly with optional LLM `interpretation` field
**Generation:** Hybrid — deterministic structure, optional LLM-polished `interpretation`
**Surfacing:** Fully exposed as `insights[]` array; rendered by `InsightsPanel.tsx`

**Fields per insight card:**
| Field | Content | LLM? | Surfaced? |
|-------|---------|-------|---------|
| `insight_id` | Stable deterministic ID | No | No |
| `system_id` | Body system | No | Yes (grouping) |
| `title` | Card title | No | Yes |
| `severity` | action / watch / info | No | Yes |
| `confidence` | high / medium / low | No | Yes |
| `evidence.biomarkers[]` | Values, scores, ranges | No | Yes |
| `evidence.derived_markers[]` | Computed metrics | No | Yes |
| `interpretation` | Explanation text | Optional LLM | Yes |
| `next_steps[]` | Recommended actions | No | Yes |

**Verdict:** The insight card framework is well-designed. Because the LLM is off by default, the `interpretation` field in production currently comes from the deterministic mock synthesiser. Users are seeing mock interpretations, not the richest possible text. This is the primary place where enabling Gemini with the right InsightGraphV1 inputs would have the most visible UX impact.

---

### 3.8 RetailExplainerV1 — `backend/ssot/retail_explainer_v1/registry.yaml`

**Type:** Static educational content (non-personalised)
**Generation:** Governed YAML, no compiler, no LLM
**Surfacing:** Optional on API response; rendered conditionally by frontend

**Sub-types:**
| Class | Coverage | Max length | Richness | Consumer-safe? |
|-------|----------|-----------|----------|----------------|
| `biomarker_education` | 60+ biomarkers | 8,000 chars | Long-form educational | Yes |
| `system_education` | All body systems | 8,000 chars | System-level education | Yes |
| `contribution_context` | Cluster membership | 500 chars | Factual (non-speculative) | Yes |

**Verdict:** These are the richest long-form explanation assets in the system. They are almost completely invisible in the current UX. A user who does not expand a biomarker row will never see the 8,000-character educational block that explains what glucose does and why it matters. This content could power a significant "learn more" or "deep dive" layer in the product — it is already governed and safe.

---

### 3.9 BalancedSystemsV1 — compiled output

**Type:** Deterministic system-level context — positive and neutral system interpretation
**Generation:** Deterministic compiler; uses system burden, capacity scores, arbitration result
**Surfacing:** Exposed via `/analysis/result`; rendered by `BalancedSystemsSummary.tsx`

**Fields:** `intro_line`, `system_topic`, `evidence_line`, `capacity_note` per system

**Verdict:** This is correctly positioned as the "what is working well" counterbalance. However, the current component does not make this feel like a first-class product moment. It reads as supplementary context rather than a genuine reassurance layer. This is a presentation and positioning problem, not a data problem.

---

### 3.10 Gemini Client — `backend/core/llm/gemini_client.py`

**Type:** LLM integration layer (inactive in production by default)
**Model:** `models/gemini-flash-latest`
**Activation:** Requires `HEALTHIQ_NARRATIVE_LLM=1` AND `HEALTHIQ_ENABLE_LLM=1`
**Input:** InsightGraphV1 (full analytical artifact)
**Output:** Narrative text for `insights[].interpretation`

**Verdict:** The Gemini integration is well-governed (double opt-in, mock fallback, retry logic). The problem is the input — InsightGraphV1 is a comprehensive audit object, not a curated narrative prompt. When LLM is eventually enabled, the quality of its output will depend on whether the right structured inputs are extracted from InsightGraphV1 and presented in a form that guides genuinely insightful synthesis.

---

## 4. Current UX Surfacing Map

| UX Section | Data Source | Rendered? | Explanation Depth | Main Weakness |
|------------|-------------|-----------|------------------|---------------|
| Hero / Primary concern | `clinician_report.page1.primary_concern` | Yes | 160 chars, deterministic | Too brief; no supporting reasoning shown |
| Data quality / confidence | `data_quality.confidence_caveat` | Yes | 220 chars | Rarely noticed by users |
| Key findings list | `page1.key_findings[]` | Yes | 160 chars × 5 | Feels like a list, not a story |
| Lead hypothesis | `page1.top_hypothesis_line` | Likely buried | 220 chars | Unknown if rendered prominently |
| Arbitration rationale | `page1.runner_up_why_not_lead_line` | Likely not rendered | 280 chars | Almost certainly invisible |
| Root cause hypotheses | `sections.root_cause` via `RootCauseEvidenceSummary` | Yes | Evidence blocks | Secondary position; not the hero |
| Balanced systems | `balanced_systems_v1` via `BalancedSystemsSummary` | Yes | Deterministic | Feels supplementary, not primary |
| System groups | `clusters[]` + `system_educational_explainer` | Yes | Optional educational | Educational content rarely expanded |
| Biomarker detail | `biomarkers[]` + `biomarker_educational_explainer` | Yes | Score + optional education | Education buried in expand |
| Contribution context | `biomarkers[].contribution_context` | Yes | 500 chars | Factual but not explanatory |
| Insight cards | `insights[]` via `InsightsPanel` | Yes | Mock interpretation in prod | LLM off = deterministic mock text |
| Layer C features | Partially via meta | Partially | Metabolic age, heart score, etc. | Inconsistent; not first-class |
| Clinician report block | Full `ClinicianReportV1` | Yes | Most complete | Presented as a "report", not reasoning |

**Key observation:** The current frontend renders the right top-level fields but does not exploit the hierarchy and reasoning depth available in the contracts. The ClinicianReportV1 fields that explain *why* the lead finding is the lead, *why* the runner-up was not chosen, and *what the uncertainty means* are either not rendered or rendered without visual emphasis.

---

## 5. Gap Analysis

### 5.1 Surfacing gaps — "we already have the right data but do not use it"

- `page1.top_hypothesis_line` — a 220-char compiled hypothesis statement that belongs in the hero section and is likely not prominently displayed
- `page1.runner_up_topic_line` + `page1.runner_up_why_not_lead_line` — the arbitration rationale that explains why the secondary concern is secondary; almost certainly not surfaced
- `page1.confidence_and_missing_data` — a compiled uncertainty statement that should be a first-class trust signal
- `page1.chains[]` — signal interaction narratives that explain how findings connect; typically ignored
- `biomarker_educational_explainer.body` — up to 8,000 chars of governed educational text per biomarker; invisible unless expanded
- `system_educational_explainer.body` — same for system-level education
- Layer C features (metabolic age, heart resilience, inflammation burden, fatigue, detox) — computed but not consistently first-class

### 5.2 Contract gaps — "we lack the right intermediate contract"

- No mechanism/biological_pathway fields at the signal-library level. If the product wants to explain "why this biomarker works this way biologically," it must be compiled — there is no governed source field to draw from.
- No structured "body-level narrative" contract that aggregates across systems into a single coherent interpretation of the user's overall metabolic state. The ClinicianReportV1 focuses on findings; there is no "here is what your body looks like as a whole" compiled object.
- The InsightGraphV1 is too comprehensive to be a good LLM prompt. There is no curated "LLM narrative brief" contract that extracts the right signals in the right order for Gemini synthesis.

### 5.3 Compiler/report gaps — "we use the wrong layer"

- The retail educational explainers are static. They cannot personalise. A user with high LDL sees the same LDL education as a user with normal LDL. There is no "personalised educational note" layer that would say "because your LDL is elevated, this is why the biology matters for you specifically."
- The `interpretation` field in insight cards defaults to a deterministic mock in production. Users are not receiving LLM-polished narrative synthesis.

### 5.4 Runtime narrative gap — "the right system exists but is inactive"

- Gemini synthesis is off in production. All users see deterministic text or mock LLM output.
- The narrative runtime policy is correct in its caution, but the consequence is that the product's most differentiating explanation capability does not reach users.

### 5.5 Asset-governance gap — "the source material is too thin"

- Signal library has no mechanism, pathway, or interpretation fields — by design, but this means there is no governed source from which a biological mechanism explanation could be deterministically assembled. This must either be added to the SSOT or injected at compiler time from a knowledge bus package.
- The root cause hypothesis loaders cover 37 signals. Signals outside this set get no hypothesis layer.

### 5.6 Product-definition gap — "we do not yet have the right target experience definition"

- There is no designed "what this user should feel and know after viewing results" — which is why the current experience is a functional report rather than a transformative reasoning experience.
- The positive/reassuring layer (balanced systems) is not positioned as a product requirement — it is a component that happens to exist. It should be a first-class product moment.

---

## 6. Target User Experience Definition

After viewing a HealthIQ AI analysis, the user should walk away with the following:

### What they understand about their body overall

They should understand their body as a set of interconnected systems — not a list of markers — and have a clear sense of which systems are working well and which are under strain. They should be able to say, in their own words: "My metabolic system is showing signs of insulin resistance, but my cardiovascular system is actually in good shape — and here is how those two things connect."

### What they understand about their strongest systems

They should receive an explicit, evidence-backed statement that names which systems are performing well and why. This should feel like genuine reassurance grounded in data, not a consolation prize. "Your liver function markers are all within healthy range, and your detox capacity score is strong" — said directly, not buried.

### What they understand about their most strained systems

They should understand the primary concern at a meaningful level of depth. Not just "HbA1c is elevated" — but "your long-term glucose control marker suggests your cells are becoming less responsive to insulin, which is why your body is working harder to regulate blood sugar, and here is what that means over time." The root cause hypothesis structure already supports this; it needs to be the primary experience.

### What they understand about how markers connect

They should see at least one or two explicit connection narratives — not just a list of findings. "Elevated insulin is contributing to elevated triglycerides, which together increase strain on your cardiovascular system" is the kind of sentence that creates the "I understand my body" moment. The `chains[]` and `top_hypothesis_line` fields already contain this; they need to be surfaced.

### What they understand about uncertainty

They should know what is missing and why it matters. A statement like "your panel did not include a direct measure of insulin sensitivity, which limits confidence in the insulin resistance finding" is honest, trust-building, and already present in the `confidence_and_missing_data` and `missing_data[]` contract fields.

### What feels reassuring

The balanced systems section should feel like a genuine positive moment — not an afterthought. "Three of your five systems show no significant strain" should appear early in the experience, not at the bottom of the page.

### What feels important

The primary concern, delivered with its hypothesis, mechanism, and connection to other findings, should feel clinically serious without being alarming.

### What feels surprising

The Layer C features — metabolic age, heart resilience score, inflammation burden — are the surprise moments. "Your metabolic age is 6 years younger than your chronological age" is a statement that creates genuine engagement. These should be foregrounded.

### What feels educational

The educational explainers should be available on demand — not hidden. A well-designed "learn more" pattern that surfaces the governed educational content without cluttering the primary experience.

### What feels actionable

The confirmatory tests, next steps, and safety-class recommendations from the root cause layer should feel like a concrete, prioritised to-do — not a generic disclaimer.

### What creates the wow factor

The combination of: (1) a precise, evidence-backed primary finding with hypothesis and mechanism; (2) genuine reassurance about strong systems; (3) an explicit system connection narrative; (4) a surprising Layer C feature insight; (5) a clear "what to do next" — delivered in plain language, without jargon, with appropriate uncertainty — is the wow moment. None of these require new data. They require better transformation and presentation of what already exists.

**In summary:** After using HealthIQ AI, the user should feel that they understand their body in a deeper way than any GP visit or lab report has ever made possible — that the analysis saw them as a whole person with interconnected systems, told them honestly what is strong and what is strained, explained the reasoning behind each finding, and gave them a concrete next step.

---

## 7. Proposed Layered Explanation Architecture

### Layer A — Analytical Truth

**Role:** The governed deterministic reasoning engine. Signal evaluation, system burden computation, precedence arbitration, calibration.

**Feeds into:** InsightGraphV1 (the complete Layer A output artifact)

**Should contain:** Signal state, confidence, burden vectors, calibration items, precedence decisions, arbitration results, layer C feature scores.

**Should not contain:** Consumer language. No text generation at this layer.

**Current status:** Well-implemented. The analytical layer is sound and produces a rich InsightGraphV1 artifact.

---

### Layer B — Structured Explanation Contract

**Role:** Transforms Layer A analytical truth into structured, governed explanation objects. All deterministic. No LLM.

**Components:**
- ReportCompilerV1 → `ReportV1` (intermediate findings)
- RootCauseCompilerV1 → `RootCauseV1` (hypotheses + evidence)
- ClinicianReportCompilerV1 → `ClinicianReportV1` (primary consumer narrative)
- BalancedSystemsCompilerV1 → `BalancedSystemsV1` (positive/neutral context)
- RetailExplainerRegistry → `RetailExplainerV1` (static education)

**Should contain:** All character-limited narrative fields. Arbitration rationale. Hypothesis summaries. Chain narratives. Confidence statements. Mechanism context (currently missing — see gap 5.5).

**Should not contain:** Raw analytical scores (those stay in Layer A). LLM-generated text (that is Layer C).

**Current status:** Well-structured. The gap is that some Layer B output (particularly the arbitration rationale, chain narratives, and runner-up explanation) is not being consumed by the frontend.

**Required addition:** A "personalised mechanism brief" contract — a Layer B object that takes the signal SSOT roles/risks/modifiers and compiles them into a short personalised mechanism statement per primary finding. This bridges the gap between the signal library's machine-readable codes and the consumer-facing explanation.

---

### Layer C — Narrative Shaping

**Role:** Takes Layer B structured explanation objects and shapes them into fluent, consumer-grade language. This is where Gemini belongs — polishing and connecting, not reasoning.

**What should remain deterministic (not delegated to Gemini):**
- Primary concern statement
- Key findings list
- Confidence and uncertainty statement
- Data quality caveat
- Safety-class recommendations
- Confirmatory test rationale
- All root cause hypothesis structure

**What should be compiler-shaped (deterministic but template-driven):**
- Chain narratives ("X is contributing to Y because...")
- System connection descriptions
- Balanced system summaries
- Layer C feature plain-language summaries (metabolic age, heart resilience, etc.)

**What should be Gemini-polished using governed structured inputs:**
- The overall body-level narrative (a 3-4 sentence synthesis of all systems and their relationships — not generated from scratch but shaped from Layer B structured outputs)
- The insight card `interpretation` field (for cards where the deterministic text is technically correct but reads robotically)
- The "here is what this means for you" framing on the primary concern, once the deterministic structure has been established

**What should never be delegated to Gemini:**
- Hypothesis generation (that is Layer A/B's job)
- Confidence scores
- Risk classifications
- Confirmatory test selection
- Any output that will be consumed as clinical evidence

**Current status:** Gemini is inactive in production (correct given current state). The risk is not that Gemini is misused — it is that the product ships without any narrative shaping at all, making Layer B outputs feel clinical and terse.

---

### Layer D — UX Surfacing

The following sections should exist on the results page. This is the target surface architecture.

#### Section 1: Body Overview (Hero)
- **Purpose:** Give the user an immediate, whole-body orientation before diving into findings
- **Source authority:** `arbitration_result`, `system_capacity_scores`, `adjusted_system_burden_vector`
- **Expected tone:** Calm, orienting, authoritative
- **Contains:** A one-sentence body-level summary ("Across your five systems, metabolic function is the primary area of concern while cardiovascular and renal systems appear stable"); a visual system map showing which systems are strained, neutral, and strong; a single primary concern statement (`primary_concern` from ClinicianReportV1)
- **Does not contain:** Individual biomarker values. Jargon. Score numbers.

#### Section 2: What's Working (Balanced Systems)
- **Purpose:** Genuine reassurance — first-class, not buried
- **Source authority:** `balanced_systems_v1`, `system_capacity_scores`
- **Expected tone:** Genuinely positive, evidence-grounded
- **Contains:** Named systems that are performing well, with the evidence that supports that conclusion; capacity scores in plain language
- **Does not contain:** Hedging language that undermines the reassurance. Generic disclaimers.
- **Why it must be Section 2:** Trust is built when users know what is working before they are told what is not. Products that only report problems feel alarming rather than empowering.

#### Section 3: Primary Finding and Reasoning
- **Purpose:** Deliver the lead finding with its full explanatory chain
- **Source authority:** `page1.primary_concern`, `page1.top_hypothesis_line`, `page1.chains[]`, `root_cause` hypotheses
- **Expected tone:** Serious but not alarmist; educational; reasoned
- **Contains:** Primary concern statement; lead hypothesis in plain language; the top 1-2 chain narratives; evidence for and against the hypothesis; what data would change the conclusion
- **Does not contain:** Raw biomarker scores. All five key findings at once (that creates overwhelm).

#### Section 4: Body-Level Insight Features (Layer C)
- **Purpose:** The "wow" moments — derived insights that feel surprising and meaningful
- **Source authority:** `layer_c_features` (metabolic age, heart resilience, inflammation burden, fatigue, detox)
- **Expected tone:** Engaging, specific, surprising where warranted
- **Contains:** Metabolic age (if computed); heart resilience score with its basis; inflammation burden with contributing markers; fatigue root cause if identified; detox capacity score. Each presented as a discrete "feature insight" card.
- **Does not contain:** All features at once without prioritisation. Any feature that is not computed for this user's panel.

#### Section 5: Competing Findings and Uncertainty
- **Purpose:** Honest, confidence-building disclosure of what is uncertain and why
- **Source authority:** `page1.runner_up_topic_line`, `page1.runner_up_why_not_lead_line`, `page1.confidence_and_missing_data`, `data_quality.confidence_caveat`, `root_cause.missing_data[]`
- **Expected tone:** Honest, specific, not alarming
- **Contains:** Why the lead finding is the lead (and not another finding); what data is missing and what difference it would make; the confidence caveat
- **Does not contain:** Exhaustive arbitration traces. Technical scoring details.

#### Section 6: All Findings by System
- **Purpose:** Complete picture for users who want to go deeper
- **Source authority:** `clinician_report.page1.key_findings[]`, `clusters[]`, `system_educational_explainer`
- **Expected tone:** Structured, educational, thorough
- **Contains:** All significant findings grouped by system; optional system-level educational explainer; system capacity score
- **Does not contain:** Findings with no clinical significance.

#### Section 7: Biomarker Detail
- **Purpose:** Granular biomarker-level information for users who want to see the data
- **Source authority:** `biomarkers[]` with values, ranges, scores, `biomarker_educational_explainer`, `contribution_context`
- **Expected tone:** Informational, non-alarming, educational
- **Contains:** Biomarker value + reference range + score; cluster membership context; educational explainer on demand
- **Does not contain:** Raw clinical scores presented without context. Jargon without explanation.

#### Section 8: Next Steps and Confirmatory Tests
- **Purpose:** Concrete, prioritised action guidance
- **Source authority:** `root_cause.confirmatory_tests[]`, `actions.referrals`, `actions.monitoring`, `next_steps[]` from insight cards
- **Expected tone:** Practical, specific, prioritised
- **Contains:** Recommended tests with rationale; safety-class prioritisation (monitoring vs clinician referral vs lifestyle); next-step framing from insight cards
- **Does not contain:** Generic health advice not derived from the analysis.

#### Section 9: Clinician Summary (Exportable)
- **Purpose:** A complete, exportable summary for sharing with a clinician
- **Source authority:** Full `ClinicianReportV1`
- **Expected tone:** Clinical, precise
- **Contains:** All narrative fields from ClinicianReportV1 in their original form; disclaimer
- **Does not contain:** Layer C features (those are consumer, not clinical).

---

## 8. Deterministic vs Gemini Boundary

### Current state assessment

**Gemini is effectively inactive.** The double opt-in (`HEALTHIQ_NARRATIVE_LLM=1` AND `HEALTHIQ_ENABLE_LLM=1`) means no production user receives LLM-generated content. The `insights[].interpretation` field in production is populated by a deterministic mock synthesiser.

This is **not a failure of the governance model** — it is a deliberate, defensible choice during a period when the analytical engine was the primary focus. However, it has a significant UX consequence: the interpretation text users see is clipped, policy-driven, and reads as clinical output rather than consumer explanation.

### Recommended boundary

| Content | Recommended approach |
|---------|---------------------|
| Signal state, confidence, calibration | Fully deterministic (Layer A) — never Gemini |
| Hypothesis generation, evidence ranking | Fully deterministic (Layer B) — never Gemini |
| Confirmatory test selection | Fully deterministic — never Gemini |
| Safety-class classifications | Fully deterministic — never Gemini |
| Primary concern statement | Deterministic (Layer B compiler) — this is the clinical lead |
| Key findings list | Deterministic — character limits are appropriate here |
| Chain narratives | Compiler-shaped (template-driven deterministic) — could be Gemini-polished |
| Root cause hypothesis summaries | Deterministic — Gemini should not reinterpret these |
| Balanced system summaries | Compiler-shaped — Gemini-polished acceptable |
| Insight card `interpretation` | Gemini-polished using Layer B structured inputs — highest-value LLM use |
| Body-level narrative (Section 1 overview) | Gemini-shaped from Layer B structured inputs — best LLM opportunity |
| Layer C feature plain-language summaries | Compiler-shaped primarily; Gemini-polished acceptable |
| Educational explainer content | Deterministic static — never Gemini |

### Assessment of current Gemini usage

**Poorly aimed.** When enabled, Gemini receives the full InsightGraphV1 — a 250+ field analytical artifact that is comprehensive but not curated for narrative synthesis. A better approach is to build a "narrative brief" Layer B contract that extracts:
- The top 3 findings with their hypothesis summaries
- The chain narratives
- The balanced system evidence
- The Layer C features that are significant for this user
- The confidence and uncertainty statements

...and passes this curated brief to Gemini with a prompt that says: "You are synthesising these structured clinical findings into a consumer-facing interpretation. Do not add new claims. Do not generate new hypotheses. Shape the language, connect the findings, and make the uncertainty understandable."

**The Gemini layer is not fundamentally wrong — it is fed the wrong material and given the wrong brief.**

---

## 9. Balanced Narrative Strategy

### Current state

The `BalancedSystemsSummary` component exists and the `balanced_systems_v1` contract is populated. However, the product currently feels like it leads with problems. The positive narrative is treated as supplementary context rather than a product requirement.

### Recommended approach

**Make "what is working" a first-class section of every analysis**, positioned before the primary concern findings. This is not false reassurance — it is accurate interpretation. Most users will have some systems performing within normal parameters, and the analysis already computes this deterministically via system capacity scores and burden vectors.

**Why this matters for trust and the wow factor:**
- Users who are only told what is wrong feel alarmed and defensive.
- Users who are told "here is what is working well, and here is what needs attention" feel that the product has seen them as a whole person.
- Trust is built by demonstrating that the system can identify positives, not just negatives.

**How to avoid false reassurance:**
- Only surface a positive system statement if the system capacity score and burden vector genuinely support it. The compiler already enforces this — `balanced_systems_v1` is computed from deterministic analytical outputs.
- Never say a system is "healthy" — say it "shows no significant strain in the current panel" and include the qualifying evidence.
- Do not surface a balanced systems statement if the panel completeness for that system is below a threshold — the absence of findings is not the same as evidence of health.

**How stronger systems should contextualise weaker ones:**
- Where a strong system is adjacent to a strained system (e.g., a strong cardiovascular system co-existing with metabolic strain), the chain narrative should reference this: "Your cardiovascular system appears stable, which suggests the metabolic strain has not yet propagated to cardiovascular risk markers — this is an important window for early intervention."
- This context is only possible if the `chains[]` content from the ClinicianReportV1 is surfaced properly. Currently these connection narratives are underused.

---

## 10. Signal-Library Explanation Strategy

### Current state

The signal library (`biomarkers.yaml`) contains metadata only. There are no mechanism, biological pathway, interpretation, or implications fields. This was a deliberate architectural choice — explanation lives in the compiler and contract layer, not the registry.

### Assessment

This choice is defensible but has a cost: there is no governed source from which a biological mechanism explanation can be deterministically compiled. If the product wants to say "high LDL contributes to plaque formation by..." — that sentence must either be authored at compile time (in a hypothesis loader or knowledge bus package) or generated by Gemini.

### Recommended approach

**Do not add open-ended mechanism/pathway fields to `biomarkers.yaml`.** The registry is a lookup contract — adding free-text explanation fields would blur the boundary between the analytical SSOT and the explanation contract layer.

Instead, the right home for mechanism-level explanation is:
1. **In the retail educational explainer** (already exists at `retail_explainer_v1/registry.yaml`) — for generic, non-personalised mechanism education. The `body` field (8,000 chars) is the right place for "how this biomarker works biologically."
2. **In knowledge bus hypothesis loaders** (already exists for 37 signals) — for personalised, signal-state-specific mechanism context ("because your HbA1c is elevated, the relevant mechanism is..."). Extending this to more signals is the right approach.
3. **In a new `mechanism_brief` field in the ClinicianReportV1** — a short (200-char) compiler-generated mechanism statement for the primary concern, assembled from SSOT roles and knowledge bus content.

**Which signal-library fields are most valuable as compiler inputs:**
| Field | Value | Current use |
|-------|-------|-------------|
| `roles` | Defines what the marker measures (e.g., `insulin_sensitivity_marker`) | Used in signal evaluation; not surfaced |
| `key_risks_when_high/low` | Risk implications — could power mechanism briefs | Not surfaced |
| `known_modifiers` | Context qualifiers — critical for uncertainty statements | Partially used in calibration |
| `clinical_weight` | Drives burden vector | Used analytically; not surfaced |
| `system` | Body system mapping | Used in cluster grouping |

**Recommendation:** `roles` and `key_risks_when_high/low` are the two most underused fields. They are machine-readable codes today; a small compiler step that maps these codes to plain-language statements would produce personalised mechanism briefs without requiring new SSOT content.

---

## 11. Strategic Recommendation

### The core problem to solve

HealthIQ AI has built a sound analytical and explanation engine. The gap is not data — it is transformation, hierarchy, and presentation. The product needs to:

1. **Stop hiding its reasoning.** The most valuable explanation content (root cause hypotheses, chain narratives, arbitration rationale, uncertainty statements) is in the contracts but not in the primary user experience.
2. **Make balanced systems a first-class product moment**, not an afterthought.
3. **Activate or replace the Gemini layer** with a properly aimed, curated narrative brief.
4. **Promote Layer C features to first-class insight cards** — metabolic age, heart resilience, inflammation burden, fatigue root causes, and detox capacity are the "wow" moments the product needs.
5. **Redesign the results page hierarchy** to reflect the target user experience defined in Section 6.

### What the target explanatory UX should be

A nine-section results experience (as defined in Section 7) that:
- Opens with a whole-body orientation (what is strained, what is stable)
- Leads immediately with what is working well (Section 2 — balanced systems)
- Delivers the primary finding with its full reasoning chain (Section 3)
- Showcases the Layer C derived insights as the "wow" moment (Section 4)
- Honestly presents uncertainty and competing findings (Section 5)
- Provides depth on demand for all systems and biomarkers (Sections 6-7)
- Ends with concrete, prioritised next steps (Section 8)
- Offers a clean clinician-shareable export (Section 9)

### Which asset classes should power which layers

| Layer | Primary assets |
|-------|---------------|
| Body overview (hero) | `arbitration_result`, `system_capacity_scores`, `primary_concern` |
| Balanced systems | `balanced_systems_v1`, `system_capacity_scores`, `adjusted_system_burden_vector` |
| Primary finding + reasoning | `top_hypothesis_line`, `chains[]`, `root_cause` hypotheses, `evidence_for/against` |
| Layer C wow moments | `layer_c_features.*` from InsightGraphV1 |
| Uncertainty / competing findings | `runner_up_topic_line`, `runner_up_why_not_lead_line`, `confidence_and_missing_data`, `missing_data[]` |
| All findings by system | `key_findings[]`, `clusters[]`, `system_educational_explainer` |
| Biomarker detail | `biomarkers[]`, `biomarker_educational_explainer`, `contribution_context` |
| Next steps | `confirmatory_tests[]`, `actions.*`, `next_steps[]` |
| Clinician export | Full `ClinicianReportV1` |

### What should be surfaced first (quick wins)

1. `top_hypothesis_line` — a single 220-char field that is almost certainly not shown prominently; add it under the primary concern statement
2. `runner_up_why_not_lead_line` — a 280-char arbitration explanation that is almost certainly not surfaced; add it to the "competing findings" section
3. `chains[]` — two 200-char system connection narratives; add them to Section 3
4. Balanced systems — elevate from bottom-of-page to Section 2
5. Layer C features — present as discrete "insight feature" cards rather than metadata

### What should remain hidden/internal

- `ExplainabilityReportV1` — internal audit only
- Raw burden vector floats
- Arbitration trace details
- Precedence scores
- Calibration adjustment values
- InsightGraphV1 as a complete object

### What the recommended deterministic vs Gemini split is

See Section 8. Summary: deterministic for all clinical decisions; compiler-shaped for structured narratives; Gemini-polished for the body-level overview, insight card interpretation fields, and chain narrative fluency — but only when fed a curated Layer B narrative brief, not the raw InsightGraphV1.

---

## 12. Sequenced Roadmap / Priority Next Steps

### Phase 1 — Surface what already exists (no new assets required)

These changes require only frontend work against already-generated contract fields.

| Step | Action | Asset | Expected impact |
|------|--------|-------|----------------|
| 1.1 | Promote `top_hypothesis_line` to primary concern section | ClinicianReportV1 | Immediately deeper primary explanation |
| 1.2 | Surface `chains[]` as "how these connect" narrative in Section 3 | ClinicianReportV1 | Visible system connection story |
| 1.3 | Add `runner_up_topic_line` + `runner_up_why_not_lead_line` to competing findings section | ClinicianReportV1 | Honest arbitration transparency |
| 1.4 | Surface `confidence_and_missing_data` as a prominent trust signal | ClinicianReportV1 | Calibrated uncertainty shown to users |
| 1.5 | Elevate `balanced_systems_v1` to Section 2 position | BalancedSystemsV1 | First-class reassurance layer |
| 1.6 | Promote Layer C features to insight feature cards | InsightGraphV1 layer_c_features | Wow moment for each user |

### Phase 2 — Improve transformation of existing assets

These changes require backend compiler work or new compiler step, not new data.

| Step | Action | Asset | Expected impact |
|------|--------|-------|----------------|
| 2.1 | Build `mechanism_brief` compiler step: map `roles` + `key_risks_when_high/low` to plain-language statements | Signal library SSOT | Personalised mechanism explanation |
| 2.2 | Extend root cause hypothesis loaders from 37 to full signal coverage | Knowledge bus | Hypothesis layer for all elevated/low signals |
| 2.3 | Build curated LLM narrative brief contract (extract top 3 findings + chains + balanced systems + Layer C) | InsightGraphV1 | Proper Gemini input format |
| 2.4 | Add Layer C feature plain-language summaries in ClinicianReportV1 | ClinicianReportV1 | Consumer-safe Layer C narrative |

### Phase 3 — Activate and aim the Gemini layer

| Step | Action | Expected impact |
|------|--------|----------------|
| 3.1 | Build and govern the curated narrative brief contract (Phase 2.3) | Proper LLM input |
| 3.2 | Design and govern Gemini prompt for body-level overview synthesis | Coherent body narrative |
| 3.3 | Design and govern Gemini prompt for insight card interpretation shaping | Fluent insight text |
| 3.4 | Enable Gemini in production with double opt-in maintained | LLM narrative for all users |
| 3.5 | A/B test Gemini-polished vs deterministic for insight interpretations | Evidence-based LLM deployment |

### Phase 4 — Product experience redesign

| Step | Action | Expected impact |
|------|--------|----------------|
| 4.1 | Redesign results page to implement the nine-section architecture (Section 7 of this document) | Target UX delivered |
| 4.2 | Build "learn more" pattern for educational explainers (8,000-char biomarker + system education) | Deep education on demand |
| 4.3 | Build exportable clinician summary from ClinicianReportV1 | Clinician-sharing capability |
| 4.4 | Personalised educational note layer (Phase 2.1 mechanism briefs surfaced as biomarker education) | Personalised education |

---

**End of review.**

*This document is strategic only. It does not constitute a sprint prompt, implementation specification, or authorisation for code changes.*
