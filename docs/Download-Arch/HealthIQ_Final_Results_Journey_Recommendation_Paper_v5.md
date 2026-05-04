
# HealthIQ AI — Final Recommendation Paper v5
## Recommended world-class results journey, educational framing, and asset-to-UX mapping

**Status:** Final recommendation for delivery-team review  
**Purpose:** To define the recommended user journey for the HealthIQ AI results experience, grounded in the governed assets already present in the codebase, refined for delivery realism, and explicit about where content or contract dependencies still exist.

---

## 1. Executive summary

HealthIQ AI should not behave like a better lab report.

Most users will already have seen a conventional blood report, often with at least a reasonable marker-by-marker explanation. That means the product must achieve two things at once:

1. **Point of parity**  
   It must still let users inspect individual biomarkers, understand what each marker means, and feel that the system respects the familiar “show me my actual results” expectation.

2. **Point of differentiation**  
   It must go far beyond that by showing the body as an interconnected system, surfacing the lead pattern, making the reasoning visible, balancing strain with reassurance, and teaching the user something deeper about how their biology works.

That means the results experience must be organised as a **guided reasoning journey** rather than a report surface.

The strongest direction is not to add novelty for novelty’s sake. It is to use the exceptional deterministic assets already present in the system and present them in a clearer, tighter, more emotionally intelligent sequence.

The recommended final journey is:

1. Your body overview *(with a short “how to read this page” framing block)*  
2. What’s working well  
3. Primary finding and why  
4. Why this lead won / uncertainty  
5. Patterns across your body  
6. Marker-level evidence  
7. Key body-level insights *(optional, only when robust and explainable)*  
8. What to do next  
9. Clinician summary  

This sequence is recommended because it:
- shows the user their story quickly
- reassures before alarming
- explains before drowning them in evidence
- preserves biomarkers as a credible evidence layer
- keeps the “wow” factor grounded in governed truth, not visual gimmicks
- separates retail understanding from clinician handoff cleanly

The key recommendation is:

**Use deterministic assets as the narrative spine, preserve biomarkers as a high-quality evidence layer, and use richer explanation only where it genuinely improves understanding.**

However, two delivery realities must be stated clearly:

- the proposed **pattern layer** (Section 5) is partly grounded in the current cluster/system implementation, but a fully governed phenotype-display layer with strong retail naming is not yet proven as an existing implementation-ready asset and must be treated as Phase 2, gated behind an explicit existence check before any sprint work begins
- rich **mechanism/pathway explanation text** exists only where authored knowledge-bus packages currently provide it; it is not universally available across all biomarkers and must never be assumed at scale

Those constraints do **not** invalidate the journey. They simply mean some parts of it are buildable immediately, while others require content or contract verification before speccing begins.

---

## 2. Why this recommendation is the right one

The current strategic challenge is not whether HealthIQ can analyse a panel. It clearly can.

The real question is:

**How should a world-class metabolic reasoning engine reveal its intelligence to the user?**

In arriving at this recommendation, the governing principles were:

### 2.1 Users need orientation before detail
Users are not opening the page to browse cards. They are trying to understand what their body is telling them overall. That means the page should start with orientation, not evidence.

### 2.2 Reassurance must come early
A product that only reports concerns feels alarming and narrow. A system that can say what appears stable, resilient, or well-regulated feels more trustworthy and more intelligent.

### 2.3 The lead finding must be explained, not merely stated
The main value of HealthIQ is not that it can identify a concern, but that it can explain:
- why that concern matters
- why it won over other possibilities
- how the markers connect
- what would change the conclusion

### 2.4 Biomarkers still matter commercially and experientially
Many users will expect to see individual biomarker results because that is what traditional blood reports provide. That is the point of parity.

So biomarker evidence should not be marginalised or weakened. It should be presented later in the journey, but when the user gets there, it should still feel premium and unusually rich.

That means:
- clear values and ranges
- contribution context
- strong educational expansion
- explicit relevance to the wider patterns

### 2.5 “Wow” must be earned
The strongest “wow” moment is not an abstract futuristic visual. It is the moment a user feels:
- “this system sees my body as a whole”
- “it can explain what is strong as well as weak”
- “it can justify why it chose this lead”
- “it can teach me how my biomarkers connect to meaningful patterns”

That is why this recommendation prioritises explanation hierarchy over decorative novelty.

---

## 3. The most important strategic design choice

The single most important design choice is this:

**The product should not begin with biomarker data, but it must eventually deliver a biomarker experience that is richer than conventional blood-report UX.**

That means biomarkers are:
- **not the opening layer**
- **not the main narrative engine**
- **but absolutely still a high-value experience layer**

This is critical because it reconciles:
- the product’s systems-level differentiation
- with the user’s existing expectation of marker-by-marker inspection

The result is a journey where:
- the body story comes first
- the evidence comes later
- and the biomarker expansion experience itself becomes a second-tier “wow” layer through explanation depth

---

## 4. Recommended final results journey

---

### Section 1 — Your body overview

**Purpose:**  
Provide a calm, whole-body orientation that helps the user feel seen as more than a set of abnormal markers.

**Opening framing rule:**  
This section should begin with a very short “aha” framing block, not a long educational preamble. The user has come for results, so we should not delay the interpretation journey with a tutorial. However, because HealthIQ is showing the body through systems and patterns rather than through a flat list of markers, a compact framing note is strategically valuable.

That note should explain in 2–3 sentences that:
- individual markers are clues, not the whole story
- HealthIQ groups markers into body systems and patterns to show how the body is functioning as a whole
- this helps cut through the noise of many isolated results and makes it clearer what looks strong, what needs attention, and why

This framing should be embedded inside Section 1 rather than introduced as a separate standalone section.

**What this section must answer:**  
- what the body looks like overall at a whole-system level
- which systems appear stable or resilient
- where the main area of emerging or meaningful strain sits within that wider picture
- whether the lead concern was clear or closely contested
- how HealthIQ is reading the body as a connected system

**Why this comes first:**  
Users need a balanced body-level frame before they can interpret any detailed content.
This section should not feel like “bad news first.” It should feel like a whole-body read in which strengths, stability, and strain are all placed in context.

**Recommended UX character:**  
Calm, concise, orienting, confidence-building, balanced and holistic.

**Primary assets:**  
- `arbitration_result`
- `system_capacity_scores`
- primary concern fields from `clinician_report_v1.sections.page1`
- selected top-level report metadata

**What belongs here:**  
- a short whole-body summary
- a balanced statement that acknowledges both stability and strain
- the lead concern placed in context, not presented in isolation
- one-sentence framing that HealthIQ reads the body as interacting systems, not isolated markers
- a light overview visual if it clarifies the system picture

**What does not belong here:**  
- biomarker grids
- long evidence blocks
- deep uncertainty copy
- clinician-style prose
- an alarm-first framing that foregrounds strain before context

---

### Section 2 — What’s working well

**Purpose:**  
Anchor the user in strengths and resilience before discussing what needs attention.

**What this section must answer:**  
- which systems appear stable or resilient
- what evidence supports that
- why this matters

**Why this comes second:**  
This is one of the strongest trust-building layers in the entire product. It proves the engine is not merely scanning for problems.

**Recommended UX character:**  
Grounded, reassuring, evidence-based, not sentimental.

**Primary assets:**  
- `balanced_systems_v1`
- selected burden/capacity evidence
- low-strain deterministic system facts
- optional system explainers where useful

**What belongs here:**  
- named stable systems
- brief evidence lines
- short capacity notes
- plain-language reassurance

**What does not belong here:**  
- false reassurance
- generic “all good” language
- anything unsupported by deterministic evidence

---

### Section 3 — Primary finding and why

**Purpose:**  
Deliver the lead interpretation with real explanatory depth.

**What this section must answer:**  
- what the lead pattern is
- what it means
- why it matters
- what supports it
- what complicates it

**Why this comes here:**  
Once the user is oriented and reassured where possible, the experience should move directly into the core reasoning moment.

**Recommended UX character:**  
Serious, educational, reasoned, non-alarmist.

**Primary assets:**  
- `clinician_report_v1.sections.page1.primary_concern`
- `top_hypothesis_line`
- `chains[]`
- `root_cause_v1`
- evidence-for / evidence-against / missing-data / confirmatory-tests
- compiler-mediated signal explanation snippets where available *(sourced from KB `signal_library.yaml` packages where knowledge-bus coverage exists for the relevant signal — see Section 7 for scope and fallback rules)*

**What belongs here:**  
- lead pattern statement
- top hypothesis line
- 1–2 chain narratives
- strongest evidence for
- strongest evidence against or complicating factor
- concise “why this matters” framing

**What does not belong here:**  
- full biomarker vault
- all findings at once
- raw explainability traces
- generic lifestyle content

**Important delivery qualification:**  
This section is highly buildable where root-cause and hypothesis coverage exists. Where the primary finding falls outside current root-cause coverage (currently 37 registered signals), the UX must gracefully fall back to:
- primary concern
- top findings
- chain narrative if available
- confidence/missing-data explanation

without pretending a full hypothesis layer exists.

**Content quality note:**  
This section will succeed or fail not only on wiring, but on the clarity and quality of:
- `top_hypothesis_line`
- `chains[]`
- root-cause summaries

So Sprint R-2 must explicitly include **content QA**, not just FE wiring and DTO verification.

---

### Section 4 — Why this lead won / uncertainty

**Purpose:**  
Build trust through transparency immediately after the lead finding.

**What this section must answer:**  
- what nearly became the lead
- why it did not
- how certain the engine is
- what data is missing
- what would change the conclusion

**Why this comes fourth rather than later:**  
Once the user sees the lead finding, their next natural question is: “How sure are you?”  
This is the right moment to answer it.

**Recommended UX character:**  
Intellectually honest, precise, calm, non-defensive.

**Primary assets:**  
- `runner_up_topic_line`
- `runner_up_why_not_lead_line`
- `confidence_and_missing_data`
- `data_quality.confidence_caveat`
- missing-data fields from root cause and report structures

**What belongs here:**  
- confidence statement
- runner-up explanation
- missing-data note
- rationale for why the lead won

**What does not belong here:**  
- raw engine trace
- debug language
- scoring internals
- opaque technical wording

**Important delivery note on explainability outputs:**  
The `ExplainabilityReportV1` contract exists in the codebase and contains rich arbitration trace data. However, it is currently classified as an internal audit artifact and has no compiler step that extracts consumer-safe content from it. The primary assets for this section — `runner_up_topic_line`, `runner_up_why_not_lead_line`, and `confidence_and_missing_data` — are already present in `ClinicianReportV1` and are sufficient to build this section without touching the internal explainability contract. A future compiler step could extract additional arbitration context from `ExplainabilityReportV1`, but this is not a Phase 1 dependency and should not be treated as one.

**Content quality note:**  
As with Section 3, this section depends heavily on the readability and specificity of the existing compiler text. Sprint R-3 should include **content QA** for:
- runner-up wording
- confidence language
- missing-data phrasing

not just field surfacing.

---

### Section 5 — Patterns across your body

**Purpose:**  
Show the structured interpretation layer that sits beneath the lead finding and above the biomarker evidence.

**What this section must answer:**  
- what the main patterns across the body are
- how they are named
- what each means in plain language
- what evidence family supports each

**Why this is the middle layer:**  
This is the bridge between body-level reasoning and marker-level truth.

**Recommended UX character:**  
Structured, medically meaningful, readable, high-value.

**Primary assets:**  
- current cluster/system outputs
- system explainers
- supporting biomarker summaries
- any governed phenotype-display layer where it is confirmed to exist

**Phase classification: Phase 2 — gated behind existence check**

This section must not be specced or sprinted concurrently with the Phase 1 sections. Before any sprint work begins on Section 5, a dedicated existence check must confirm:

- what the current system/cluster layer actually provides
- whether a governed phenotype-display layer with consistent naming fields already exists or needs to be built
- what naming fields are available versus requiring new contract work

**What appears real now (Phase 1 floor — buildable without gate):**
- cluster/system grouping
- system summaries
- supporting marker groupings
- system educational explainers where wired

**What is not yet confirmed as a current implementation-ready asset:**
- a mature, governed phenotype-display layer with consistent:
  - clinical display name
  - plain-English subtitle
  - why-it-matters line

The Phase 1 floor is buildable using the current system/cluster layer with improved naming where possible. The full three-layer phenotype naming model is the Phase 2 target, subject to the existence check.

**Required naming model where contract support is confirmed:**  
Each pattern should ideally use:
1. Clinical display name  
2. Plain-English subtitle  
3. Why-it-matters explainer  

**What belongs here:**  
- strong pattern names where available
- brief plain-English description
- why-it-matters line where contract support is confirmed
- severity/status
- top supporting markers or signals
- optional system education on demand

**What does not belong here:**  
- generic health buckets
- weak labels like “Organ Health”
- raw internal ids
- undifferentiated cards with no explanation

**Naming quality note:**  
If Section 5 is ever implemented, naming quality will be as important as technical wiring. Weak naming will collapse the value of the middle layer even if the contract exists.

---

### Section 6 — Marker-level evidence

**Purpose:**  
Deliver the familiar blood-report layer, but make it significantly richer than a conventional report.

**What this section must answer:**  
- what the biomarker is
- how the result sits relative to the range
- how it contributes to the wider pattern
- how the user can learn more
- why this biomarker matters in the context of the body story

**Why this comes after the reasoning journey:**  
The evidence is more meaningful once the user already understands the body frame and the main patterns.

**Recommended UX character:**  
Clear, premium, evidence-focused, educational on demand.

**Primary assets:**  
- `biomarkers[]`
- `contribution_context`
- `biomarker_educational_explainer`
- reference range data
- scores / interpretations

**Important strategic note:**  
This section is the point of parity with conventional blood-report experiences, but it should still become a point of differentiation through:
- better contribution-context surfacing
- stronger educational expansion
- clearer relationship to the identified pattern(s)

**Biomarker expansion should wow the user too.**  
A user who opens a biomarker should feel:
- this system knows what the marker is
- it can explain what the marker does
- it can explain why it matters for this user
- it can connect that marker to the wider pattern, not just define it generically

**What belongs here:**  
- current result
- reference range
- status
- short interpretation
- contribution context
- strong educational explainer expansion
- pattern relevance

**Technical definition — pattern relevance:**  
“Pattern relevance” is not a standalone contract field. It should be derived for each biomarker by combining:
- `contribution_context` (the factual cluster-membership statement already in the contract)
- the biomarker's cluster membership (from `clusters[]`) cross-referenced against the identified primary pattern/system from Section 3

This tells the user: “this marker contributed to the [pattern name] finding” — grounding the biomarker in the wider reasoning rather than presenting it in isolation. No new contract field is required for Phase 1; it is a rendering-layer derivation.

**What does not belong here:**  
- biomarker grid as the main emotional centre of the page
- educational content without relevance framing
- generic explanation without linkage to the wider body story

---

### Section 7 — Key body-level insights

**Purpose:**  
Deliver the selective higher-order “wow” layer once the core story is already understood.

**Hard display rule:**  
This section is optional by user and by panel. It should only appear when there are robust, explainable, genuinely worthwhile body-level features to show. If the available Layer C feature set is thin, weakly supported, or not clearly interpretable for this user, the section should collapse cleanly rather than appear as a thin or gimmicky layer.

**What this section must answer:**  
- what broader derived insights the engine has found
- what those mean in a body-level sense
- why they are noteworthy

**Why this comes late rather than early:**  
These insights should feel earned and credible, not flashy or over-promoted.

**Recommended UX character:**  
High-value, surprising where warranted, tightly controlled.

**Primary assets:**  
- `layer_c_features`
- selected deterministic higher-order feature summaries
- only those robust enough for user-facing display

**Important runtime qualification:**  
This section is **not** dependent on Gemini if it is built from deterministic Layer C features (`layer_c_features.*` from `InsightGraphV1`). The following features are computed deterministically and do not require LLM activation:
- metabolic age (`MetabolicAgeFeatureV1`)
- heart resilience score (`HeartFeatureV1`)
- inflammation burden (`InflammationFeatureV1`)
- fatigue root causes (`FatigueFeatureV1`)
- detox capacity (`DetoxFeatureV1`)

However, if the delivery team expects richer **insight-card interpretation prose** in the `insights[]` array, they must assume one of two tracks:
- enable and govern Gemini for narrative synthesis
- or improve the deterministic synthesiser independently

The current production default is deterministic mock synthesis. This section can be built and shipped without resolving that question, provided it draws from Layer C features directly rather than from insight-card interpretation prose.

**Readiness caution:**  
Before promising this as a broad multi-card section, the team should perform a **feature robustness check** across real panels:
- which Layer C features are most consistently populated
- which are clinically defensible enough for first-wave surfacing
- which should remain hidden until stronger coverage exists

This is not a strategic objection. It is a delivery realism check. If the check does not support confident surfacing, the section should not render.

**What belongs here:**  
- only robust, explainable features
- concise explanation
- clear relevance to the wider journey

**What does not belong here:**  
- gimmicky visuals
- unsupported composite scores
- too many feature cards
- “future-feeling” ideas that are not actually defendable

---

### Section 8 — What to do next

**Purpose:**  
Move the user from understanding to action.

**What this section must answer:**  
- what confirmatory tests could help
- what should be discussed with a clinician
- what monitoring or follow-up matters
- what the priority order is

**Recommended UX character:**  
Practical, prioritised, specific, non-generic.

**Primary assets:**  
- `confirmatory_tests[]` with rationale fields
- `actions` (referrals, monitoring)
- `next_steps[]` from insight cards
- `safety_class` values for priority ordering (`clinician_referral` > `monitoring` > `lifestyle`)

**What belongs here:**  
- prioritised roadmap ordered by safety class
- confirmatory test rationale
- follow-up logic
- clinician discussion cues

**What does not belong here:**  
- vague lifestyle advice
- generic wellness filler
- unprioritised lists

---

### Section 9 — Clinician summary

**Purpose:**  
Provide a professional handoff without contaminating the retail journey.

**Why this remains separate:**  
The retail user journey and the clinician handoff solve different problems. They should remain related, but distinct.

**Primary assets:**  
- full `ClinicianReportV1`

**Recommended UX character:**  
Structured, professional, exportable, separate from the core retail flow.

**What belongs here:**  
- full clinician summary
- clean lower-page or exportable section
- professional handoff logic

**What does not belong here:**  
- live mode-switch transformation of the whole page
- clinician detail injected throughout the retail flow

---

## 5. Recommended asset-to-UX mapping

| UX section | Main purpose | Primary text assets | Supporting assets | Delivery note |
|---|---|---|---|---|
| Your body overview | orientation | `primary_concern`, selected page1 summary fields | `arbitration_result`, `system_capacity_scores` | buildable now |
| What’s working well | reassurance | `balanced_systems_v1` | low-burden evidence, capacity notes | buildable now |
| Primary finding and why | explain the lead | `top_hypothesis_line`, `chains[]`, `root_cause_v1` | KB signal explanation where package exists; fallback required for signals outside root-cause coverage | buildable with fallback |
| Why this lead won / uncertainty | trust | `runner_up_topic_line`, `runner_up_why_not_lead_line`, `confidence_and_missing_data` | `data_quality.confidence_caveat`, missing-data fields — use ClinicianReportV1 fields only; ExplainabilityReportV1 is internal and has no consumer compiler step | buildable now from ClinicianReportV1 |
| Patterns across your body | structured interpretation | current system/cluster naming; phenotype display layer where available | system explainers, supporting marker summaries | **Phase 2 — existence check gate required before speccing** |
| Marker-level evidence | evidence depth + parity | `biomarkers[]`, `contribution_context`, short interpretations | `biomarker_educational_explainer`, reference ranges; pattern relevance derived from `contribution_context` + cluster membership (rendering-layer derivation, no new contract field) | buildable now |
| Key body-level insights | selective wow | deterministic `layer_c_features` summaries | selected derived metrics | buildable from Layer C features without Gemini; insight-card prose requires Gemini track or improved synthesiser |
| What to do next | action | `confirmatory_tests[]` with rationale, `actions`, `next_steps[]` | `safety_class` for priority ordering | buildable now |
| Clinician summary | handoff | full `ClinicianReportV1` | optional export metadata | buildable now |

---

## 6. How biomarkers should deliver both parity and differentiation

This deserves explicit treatment.

### 6.1 Point of parity
Users expect:
- to find their marker
- to see the value
- to understand range position
- to understand whether it looks normal, low, or high

HealthIQ must meet that expectation cleanly.

### 6.2 Point of differentiation
HealthIQ should then go further by using the assets already available to say:
- what that biomarker actually does biologically
- how it contributes to the user’s identified pattern
- why it matters in this wider body context
- how it connects to related markers or systems

### 6.3 Biomarker expansion rule
Every biomarker expansion should be structured as:

1. **What this result means now**
   Short interpretation tied to this user’s actual result

2. **Why this marker matters**
   Educational explainer content

3. **How it connects to your wider pattern**
   Contribution context and pattern relevance (derived from `contribution_context` + cluster membership cross-referenced against the primary pattern — see Section 6 technical definition)

This is where the biomarker layer becomes a second-order wow experience rather than just a technical appendix.

### 6.4 Fallback rule
If richer educational or pattern-linking content is absent:
- still show value, range, status, and short interpretation
- omit missing deeper layers cleanly
- do not fabricate a richer explanation than the data supports

---

## 7. How signal-library explanation assets should be used

The signal packages in:
- `knowledge_bus/packages/**/signal_library.yaml`

contain some of the richest explanation-bearing assets in the system, including where authored:
- `explanation.mechanism`
- `explanation.biological_pathway`
- `explanation.interpretation`
- `explanation.implications`
- structured supporting metric roles / rationales

### Critical qualification
These fields are **not universally available across all biomarkers or all systems**.

They exist only where richer **knowledge-bus packages** have been authored. They do **not** exist generally in the core `biomarkers.yaml` SSOT, which contains metadata only (description, roles, risk codes, modifiers) — not mechanism or pathway text.

So the correct delivery assumption is:

- use them where governed package coverage exists
- never assume universal availability
- always support a fallback compiler path when package-level explanation fields are absent

These should **not** be surfaced raw.

They should instead be used as governed source material for **compiler-mediated copy** that can support:
- pattern-level “why this matters” statements
- lead-finding significance framing
- system-group explanation snippets
- richer evidence summaries
- biomarker relevance framing

This approach protects:
- tone consistency
- length discipline
- version control
- user comprehension

---

## 8. Deterministic vs Gemini recommendation

The recommendation remains clear:

### Deterministic assets should form the narrative spine
The primary journey should be powered by:
- `clinician_report_v1`
- `root_cause_v1`
- `balanced_systems_v1`
- current system/cluster outputs
- explainability-derived rationales (via ClinicianReportV1 compiled fields only — not raw ExplainabilityReportV1)
- deterministic educational explainers
- compiler-mediated signal explanation excerpts where KB package coverage exists

### Gemini should remain supplementary
Gemini can later help with:
- smoothing section summaries
- improving connective tissue
- optional polished summary layers

But Gemini should not be the authority for:
- clinical reasoning
- lead interpretation
- confidence
- prioritisation
- confirmatory tests
- core body story

### Current production reality
The delivery team should assume:
- production Gemini is not currently the default narrative spine
- sections depending on deterministic assets remain buildable and shippable without Gemini
- richer prose in optional insight cards may remain thin unless Gemini is enabled or the deterministic synthesiser is improved
- this is not a blocker for Phase 1 delivery

The wow factor should come from governed truth, not prose styling.

---

## 9. Design rules that should now be treated as locked

1. The page is a guided reasoning journey, not a report surface.
2. Biomarkers do not lead the experience.
3. Balanced systems are first-class, not supplementary.
4. The lead finding must be explained, not merely stated.
5. Uncertainty must be visible and user-readable.
6. Section 1 should begin with a very short “how to read this page” framing block embedded inside the body overview — not a separate educational preamble.
7. Pattern naming must be strong and three-layered where contract support is confirmed — not assumed universally.
8. Biomarker expansion should be rich enough to wow the user too.
9. Signal-library explanation assets should be compiler-mediated, not pasted raw.
10. Rich KB explanation fields must be treated as selective, not universal — always support a fallback path.
11. Gemini is optional polish, not the product spine.
12. Clinician handoff remains separate from the retail journey.
13. ExplainabilityReportV1 is an internal audit artifact — do not treat it as a consumer content source without a dedicated compiler step.
14. Section 5 (patterns layer) is Phase 2 — it must not be specced or sprinted without completing the existence check gate first.
15. Section 7 (key body-level insights) is optional — it should only render when robust and explainable features are genuinely available.
16. The body overview must frame strain within overall balance; it must not read as a “bad news first” section.

---

## 10. Content coverage and fallback rules

This section is included specifically to keep delivery honest.

### 10.1 If root-cause coverage is absent
Use:
- primary concern
- top findings
- chain narratives where available
- confidence/missing-data explanation

Do not pretend a full hypothesis layer exists.

### 10.2 If system explainer is absent
Keep the system/pattern card interpretive only.
Do not insert generic education filler.

### 10.3 If richer KB explanation text is absent
Use compiler-safe summary text only.
Do not imply that mechanism/pathway detail exists when it does not.

### 10.4 If Gemini remains off
The core journey remains valid.
Do not block delivery of the main sections.
Only optional polished narrative layers become thinner.

### 10.5 If Layer C feature support is uneven
Show only robust, explainable features.
Omit the rest cleanly.

### 10.6 If the phenotype-display layer existence check fails
Implement Section 5 using the current system/cluster layer with improved naming only.
Do not build toward a phenotype contract that does not yet exist.
Scope the additional contract work and treat it as a separate content/backend sprint before the frontend work can proceed.

---

## 11. Delivery dependencies and minimum viable scope

### Buildable now from current deterministic assets
- Your body overview
- What’s working well
- Primary finding and why (with fallback where root-cause coverage absent)
- Why this lead won / uncertainty (from ClinicianReportV1 fields — no ExplainabilityReportV1 consumer compiler required)
- Marker-level evidence
- What to do next
- Clinician summary

### Requires explicit existence/content check before speccing begins — Phase 2
- full phenotype-display pattern layer
- universal three-layer pattern naming
- richer mechanism/pathway text at scale
- any section assuming broad KB explanation coverage

### Independent of Gemini being on
- overview
- reassurance
- primary finding
- uncertainty
- biomarkers
- next steps
- clinician summary
- deterministic Layer C features where computation is confirmed robust

### Becomes richer if Gemini is later enabled or deterministic synthesiser improved
- connective prose
- optional insight-card interpretation language
- smoother summary transitions

---

## 12. Immediate practical recommendation to the delivery team

The next step is **not** more abstract ideation.

The next step is to turn this recommendation into a concrete section-by-section specification covering:

### A. Results page section specification
For each section:
- purpose
- key user question
- intro message
- show layer
- summary layer
- exact data assets
- expanded / hidden content
- fallback condition if richer content absent

### B. Pattern existence and naming check — must complete before Section 5 sprint
Before speccing Section 5, verify:
- what current system/cluster layer already exists
- whether a governed phenotype-display layer exists with consistent naming fields
- what naming fields are already available versus needing new contract work
- output of this check gates whether Section 5 is a surfacing sprint or a content/contract sprint first

### C. Deterministic narrative spine specification
Define exactly which existing assets drive:
- body overview
- reassurance layer
- lead interpretation
- why / uncertainty
- pattern layer (post existence check)
- biomarker evidence
- action layer

### D. Biomarker expansion specification
Define exactly how each biomarker card uses:
- short interpretation
- educational explainer
- contribution context
- pattern relevance (derived from contribution_context + cluster membership)
- fallback if deeper layers absent

That is now the most practical way to move from discussion into delivery.

---

## 13. Sprint delivery plan

This section sequences the recommended journey into concrete successive delivery sprints. Each sprint is scoped to be independently shippable. Backend dependencies are called out explicitly. The sequence respects the phase classification established in Section 11.

---

### Sprint R-1 — Page architecture and body overview

**Objective:** Restructure the results page into the nine-section hierarchy and implement the body overview.

**What this sprint does:**
- Restructures the results page component hierarchy to the nine-section model
- Implements Section 1 (Your body overview) as the new page entry point
- Adds the short embedded “how to read this page” framing block at the top of Section 1
- Surfaces `primary_concern`, `system_capacity_scores`, and `arbitration_result` in the hero position
- Adds a light system-map visual showing which systems are strained, neutral, and stable (using `system_capacity_scores`)
- Moves `balanced_systems_v1` to the Section 2 position immediately below the hero — this is a repositioning sprint; the content does not change

**Frontend work:**
- New page layout scaffold with nine named sections
- Hero component consuming `clinician_report_v1.sections.page1.primary_concern` and `arbitration_result`
- Micro-orientation framing block explaining why markers are grouped into systems and patterns
- System overview visual component using `system_capacity_scores`
- Reposition existing `BalancedSystemsSummary` component to Section 2

**Backend work:**
- None. All required assets (`clinician_report_v1`, `balanced_systems_v1`, `system_capacity_scores`, `arbitration_result`) are already present in the `/analysis/result` API response.

**Success criterion:**
- User landing on results sees a whole-body frame immediately
- Balanced systems appears before any strain findings
- Existing clinician report content is still accessible further down the page

**Fallback handling:** None required — all assets are available.

---

### Sprint R-2 — Primary finding with full reasoning depth

**Objective:** Implement Section 3 as the core reasoning moment — not a summary card but a full explanatory experience.

**What this sprint does:**
- Implements Section 3 (Primary finding and why)
- Surfaces `top_hypothesis_line` prominently as the lead interpretive statement
- Surfaces `chains[]` as explicit system-connection narratives (“here is how these findings connect”)
- Elevates `root_cause_v1` from a secondary block to the primary evidence layer for the lead finding
- Implements the evidence-for / evidence-against structure from `RootCauseHypothesisV1`
- Implements graceful fallback for findings outside current root-cause coverage (37 signals)

**Frontend work:**
- Section 3 component with hypothesis headline, chain narratives, evidence blocks
- Evidence-for / evidence-against sub-component
- Fallback renderer: if `root_cause_v1` is absent for the primary signal, fall back to `primary_concern` + `top_findings` + `chains[]` only
- Missing-data sub-component showing gaps in the evidence

**Backend work:**
- Verify `top_hypothesis_line` and `chains[]` are present and populated in the DTO. If not surfaced in the current DTO builder output, add them — both are fields of `ClinicianReportV1.sections.page1` and should already be included.
- Verify `root_cause_v1` finding for the primary signal is accessible in the response.

**Content QA requirement:**
- Review `top_hypothesis_line` quality across a representative panel set
- Review `chains[]` readability and duplication risk
- Review evidence-for / evidence-against balance for clarity and brevity

**Success criterion:**
- User sees the lead hypothesis stated in plain language
- At least one system-connection narrative is visible
- Evidence-for is present where root-cause coverage exists
- Fallback renders correctly and honestly where it does not

---

### Sprint R-3 — Uncertainty and arbitration transparency

**Objective:** Implement Section 4 — making the reasoning process visible to the user immediately after the primary finding.

**What this sprint does:**
- Implements Section 4 (Why this lead won / uncertainty)
- Surfaces `runner_up_topic_line` (what nearly became the lead)
- Surfaces `runner_up_why_not_lead_line` (why it did not)
- Surfaces `confidence_and_missing_data` as a prominent statement
- Surfaces `data_quality.confidence_caveat` as a trust signal

**Frontend work:**
- Section 4 component with runner-up card, confidence statement, missing-data note
- “How sure are we?” framing component
- The ExplainabilityReportV1 contract must not be used here — all required fields are already in ClinicianReportV1 and this sprint must not create a dependency on that internal artifact

**Backend work:**
- Verify `runner_up_topic_line`, `runner_up_why_not_lead_line`, and `confidence_and_missing_data` are populated in the DTO response. These are ClinicianReportV1 fields and should be present; if they are not in the current DTO output, surface them without adding new computation — they are already compiled.

**Content QA requirement:**
- Review runner-up wording for clarity and non-defensiveness
- Review confidence language for calmness and precision
- Review missing-data phrasing for user readability

**Success criterion:**
- User can see what the runner-up finding was and why it did not lead
- Confidence caveat is visible and readable without being alarming
- Missing-data note is honest and specific

---

### Sprint R-4 — Biomarker expansion depth

**Objective:** Implement the three-layer biomarker expansion rule so that the marker-level experience becomes a second-order differentiator, not a conventional blood-report appendix.

**What this sprint does:**
- Implements the full biomarker expansion model (Section 6.3)
- Layer 1: short interpretation tied to this user’s actual result
- Layer 2: `biomarker_educational_explainer` surfaced in expansion
- Layer 3: pattern relevance — derived from `contribution_context` + cluster membership cross-referenced against the primary pattern (rendering-layer derivation; no new contract field required)
- Implements fallback rule: where richer layers are absent, show value/range/status/short interpretation only

**Frontend work:**
- Expanded biomarker card component with three-layer structure
- Pattern relevance derivation: map biomarker’s cluster membership against primary pattern identified in Section 3; render as “this marker contributed to [pattern name]”
- Conditional rendering for each layer — omit cleanly if absent
- Ensure `contribution_context` is surfaced as part of expansion, not just in hover/tooltip

**Backend work:**
- Minor: ensure `contribution_context` and `biomarker_educational_explainer` are consistently present in the `biomarkers[]` array in the DTO. Both are already governed assets; this sprint should only require confirming they are wired through to the response.

**Success criterion:**
- User expanding a biomarker sees at minimum: result, range, status, short interpretation
- Where educational explainer exists, it appears in expansion
- Where contribution context exists, it links the marker to the identified pattern
- No biomarker card fabricates a richer explanation than its data supports

---

### Sprint R-5 — Action layer structure

**Objective:** Implement Section 8 (What to do next) as a prioritised, clinically ordered action summary — not a generic checklist.

**What this sprint does:**
- Implements Section 8 using `confirmatory_tests[]`, `actions`, and `next_steps[]`
- Orders actions by `safety_class`: `clinician_referral` first, then `monitoring`, then `lifestyle`
- Surfaces `confirmatory_tests[].rationale` for each test
- Surfaces `actions.referrals` and `actions.monitoring` from `ReportV1`

**Frontend work:**
- Section 8 component with safety-class priority ordering
- Confirmatory test card with test name and rationale
- Referral and monitoring sub-sections

**Backend work:**
- Verify `confirmatory_tests[]` with rationale fields and `actions` are accessible in the DTO. Both exist in the current contracts and should already be surfaced.

**Success criterion:**
- User sees a prioritised list of next steps ordered by clinical urgency
- Each confirmatory test has an explanatory rationale
- Generic filler is absent — every item is grounded in the analysis

---

### Sprint R-6 — Layer C insight features

**Objective:** Implement Section 7 (Key body-level insights) using deterministic Layer C features — independently of Gemini.

**What this sprint does:**
- Implements Section 7 as a set of discrete “body insight” feature cards
- Sources each card from `layer_c_features.*` in `InsightGraphV1`
- Only surfaces features that are robustly computed for this user’s panel
- Handles uneven feature availability cleanly — omits cards where feature computation is not available rather than showing empty or partial cards
- Features in scope: metabolic age, heart resilience score, inflammation burden, fatigue root causes, detox capacity

**Frontend work:**
- Section 7 feature card components (one per Layer C feature type)
- Robustness check gate: each feature card should only render if the underlying feature is populated and valid for this user’s panel
- Plain-language summary for each feature (content to be drafted as compiler-mediated copy — deterministic, not LLM)

**Backend work:**
- Verify each `layer_c_features.*` sub-feature is accessible in the DTO response. If `InsightGraphV1.layer_c_features` is stored in `meta` but not extracted into the top-level DTO, add extraction for the relevant feature fields.
- For each feature: define the robustness condition (e.g., metabolic age requires certain insulin-related markers; do not display if prerequisite markers are absent).

**Readiness gate requirement:**
Before sprint execution begins, produce a short validation artifact showing:
- which Layer C features are most consistently populated in real results
- which are suitable for first-wave surfacing
- which should remain hidden pending stronger coverage

**Success criterion:**
- At least the most universally computed Layer C feature is live for all qualifying analysis results
- No feature card renders without valid data
- Section does not appear at all if no robust features are available for this user
- Weak or thin Layer C output is omitted rather than shown for novelty

---

### Sprint R-7 — Pattern existence check and Phase 2 gate (not an implementation sprint)

**Objective:** Complete the gate that unlocks Section 5 (Patterns across your body). This is a research and specification sprint, not a frontend implementation sprint.

**What this sprint does:**
- Conducts a formal existence check of the current system/cluster/phenotype layer
- Determines what naming fields currently exist in the cluster/system contract
- Determines whether a governed phenotype-display layer with consistent clinical display name, plain-English subtitle, and why-it-matters line exists or needs to be built
- Produces a written output: either a sprint specification for implementing Section 5 using existing assets, or a scoping document for the contract/content work required before implementation can proceed

**Participants:** Backend lead, product, and the team member responsible for the cluster/system contracts.

**Outputs:**
- Written determination: is Section 5 a surfacing sprint or a content/contract sprint first?
- If surfacing: sprint specification for R-8 (Section 5 frontend, using current cluster/system layer with improved naming)
- If contract work required: scope document for the backend contract sprint that must precede the frontend sprint

**Success criterion:**
- A decision is made in writing
- No implementation work begins on Section 5 before this sprint produces its output

---

### Sprint R-8 — Patterns layer (conditional on R-7 outcome)

**Objective:** Implement Section 5 (Patterns across your body) using the confirmed available assets.

**Scope depends on Sprint R-7 output:**

**If the existence check confirms the current cluster/system layer is sufficient:**
- Implement Section 5 using the current cluster/system layer with improved naming
- Apply three-layer naming (clinical display name, plain-English subtitle, why-it-matters) where contract fields support it
- Surface system educational explainers on demand
- Surface supporting marker summaries per pattern

**If the existence check reveals a contract gap:**
- Sprint R-8 becomes a backend content/contract sprint: author the phenotype-display contract and governed naming fields
- A subsequent sprint R-9 implements the frontend against the new contract

**Frontend work (if surfacing path):**
- Section 5 component with pattern cards
- Three-layer naming component where available
- System education on-demand expand
- Supporting marker summary per pattern

**Backend work (if surfacing path):**
- Wire system/cluster naming fields through to DTO if not already present

**Naming QA requirement:**
- Review proposed pattern names for clarity, distinctiveness, and non-generic wording
- Reject labels that collapse into generic health buckets
- Treat naming quality as a first-class review criterion, not a cosmetic pass

**Success criterion (surfacing path):**
- User sees a named, described pattern layer between the primary finding and the biomarker detail
- Each pattern card communicates what the pattern is and why it matters
- No raw internal IDs or generic health bucket labels appear

---

### Sprint R-9 — Gemini narrative brief (conditional, future phase)

**Objective:** Enable Gemini for production narrative synthesis using a properly aimed, curated narrative brief — not the raw InsightGraphV1.

**Preconditions before this sprint is authorised:**
- Phase 1 (Sprints R-1 through R-6) is complete and stable in production
- A curated narrative brief contract has been designed that extracts the right inputs from Layer B (top 3 findings, chain narratives, balanced system evidence, Layer C features relevant to this user, confidence and uncertainty statements)
- A governed Gemini prompt has been designed and reviewed for clinical safety
- The production double opt-in (`HEALTHIQ_NARRATIVE_LLM=1` and `HEALTHIQ_ENABLE_LLM=1`) remains the activation model

**What this sprint does:**
- Authors the curated narrative brief contract (Layer B extraction)
- Designs and governs the Gemini prompt for body-level overview synthesis (Section 1 polish) and insight-card interpretation shaping (Section 7)
- Implements production enablement with audit trail
- Defines A/B test or staged rollout for Gemini vs deterministic synthesis

**Success criterion:**
- Gemini receives a curated brief, not the full InsightGraphV1
- Gemini output is not the authority for any clinical decision
- Deterministic fallback is preserved if Gemini is unavailable or returns an error
- Rollout is staged and measurable

---

### Sprint R-10 — KB coverage expansion (content, future phase)

**Objective:** Extend knowledge-bus package coverage to increase the depth of mechanism/pathway explanation available across more signals.

**What this sprint does:**
- Extends the root-cause hypothesis loader registry beyond the current 37 signals
- Authors additional knowledge-bus packages for high-priority signals not yet covered
- Feeds mechanism/pathway fields into compiler-mediated surfacing at scale

**Priority signals for extension:**
- Determined by which primary findings most frequently fall outside current root-cause coverage in production analysis data

**Success criterion:**
- Root-cause hypothesis coverage increased measurably
- No new surfacing work required — the frontend fallback-to-primary-concern logic from Sprint R-2 automatically upgrades when new hypothesis coverage arrives

---

### Sprint delivery summary

| Sprint | Section | Type | Gemini dependency | Backend dependency |
|--------|---------|------|------------------|--------------------|
| R-1 | Sections 1 + 2 restructure | Frontend restructure | None | None |
| R-2 | Section 3 — primary finding | Frontend + minor backend check | None | Verify top_hypothesis_line, chains[] in DTO; include content QA |
| R-3 | Section 4 — uncertainty | Frontend + minor backend check | None | Verify runner_up fields in DTO; include content QA |
| R-4 | Section 6 — biomarker expansion | Frontend + minor backend check | None | Verify contribution_context, educational_explainer in DTO |
| R-5 | Section 8 — next steps | Frontend + minor backend check | None | Verify confirmatory_tests, actions in DTO |
| R-6 | Section 7 — Layer C insights | Frontend + backend feature extraction | None | Extract layer_c_features from meta into DTO; complete readiness gate |
| R-7 | Section 5 gate | Research + specification only | None | None (decision sprint) |
| R-8 | Section 5 — patterns layer | Frontend (or backend contract first) | None | Conditional on R-7 outcome; naming QA mandatory |
| R-9 | Gemini narrative brief | Backend + frontend | Required | Narrative brief contract design |
| R-10 | KB coverage expansion | Backend content | None | KB package authoring |

**Phase 1 (buildable now, no Gemini):** R-1 through R-6  
**Phase 2 (gated):** R-7, R-8  
**Phase 3 (future, conditional):** R-9, R-10

---

## 14. Final recommendation

HealthIQ should now move decisively from “results interface” thinking to **guided reasoning journey** thinking.

The strongest version of the product is one that:
- teaches the user how to understand their body without feeling tutorial-heavy
- reassures before alarming
- explains before overloading with evidence
- preserves biomarkers as a premium evidence layer
- uses deterministic assets more boldly
- links marker-level truth back to system-level understanding
- reserves clinician content for a distinct lower section
- treats the best existing assets as a disciplined narrative system rather than as scattered text

If this is executed well, the user should leave the results page feeling:

- I understand my body at a whole-system level
- I know what appears strong and what needs attention
- I understand why the engine concluded this
- I can inspect my biomarker evidence without losing the bigger picture
- I learned something genuinely new about how my biology works

That is the standard the front end should now be built to meet.
