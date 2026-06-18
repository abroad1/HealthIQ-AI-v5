---
work_id: LAYER-BOUNDARY-RECONCILIATION-1
branch: work/LAYER-BOUNDARY-RECONCILIATION-1-layer-boundary-reconciliation
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: DOCS
---

# LAYER-BOUNDARY-RECONCILIATION-1 — Canonical Layer Boundary ADR

## Objective

Create a short, authoritative architecture ADR that reconciles HealthIQ AI’s Layer A / Layer B / Layer C terminology and locks the canonical interpretation for all future roadmap and sprint planning.

This is a documentation-only sprint.

Do not change runtime code.
Do not change tests.
Do not change frontend behaviour.
Do not change backend compilers.
Do not implement Gemini.
Do not modify Layer B or Layer C runtime logic.
Do not create a new roadmap yet.

The purpose is to settle the vocabulary before the multi-sprint beta-readiness programme is written.

---

## Why this work is needed

Recent estate audits found that the product already has strong architecture and substantial documentation, but there is naming drift around “Layer C”.

Some documents use Layer C to mean LLM narrative translation.
Some documents use Layer C to include deterministic narrative compiler output.
ADR-005 uses A/B/C/D stage labels differently from ADR-002.
Strategic Vision v1.5 §2.3 confirms that Layer B owns signals, WHY, root-cause and clinician reporting, while Layer C is user-facing narrative translation / presentation only.

We need one concise ADR that reconciles these documents and prevents future sprints from accidentally moving Layer B responsibilities into Layer C.

---

## Required branch and state checks

Before making changes:

```powershell
git switch main
git pull
git status --short
git switch -c work/LAYER-BOUNDARY-RECONCILIATION-1-layer-boundary-reconciliation
```

Confirm the active work package/state file if required by the Automation Bus SOP.

Do not proceed if the working tree is dirty, except for known intentional files from this work package.

---

## Authoritative inputs

Read these before writing the ADR:

```text
docs/strategy/HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan_v1.5_FINAL_ADOPTED.md
docs/strategy/LAYER_ARCHITECTURE_AUTHORITY_INDEX_2026-06-17_r2.md
docs/strategy/LAYER_ARCHITECTURE_AUTHORITY_INDEX_2026-06-17.md
docs/strategy/eight_block_beta_readiness/EIGHT_BLOCK_BETA_READINESS_LATE_DOCUMENT_ADDENDUM_2026-06-17.md
docs/strategy/eight_block_beta_readiness/EIGHT_BLOCK_BETA_READINESS_ESTATE_AUDIT_CURSOR_2026-06-17.md
docs/strategy/eight_block_beta_readiness/EIGHT_BLOCK_BETA_READINESS_ESTATE_AUDIT_CLAUDE_2026-06-17.md
docs/architecture/ADR_WP2_layer_b_layer_c_contract_path_b.md
backend/core/contracts/narrative_payload_v1.py
architecture/ADR-002-deterministic-analysis-engine.md
architecture/ADR-005-disease-specific-signal-evaluation-v2.md
architecture/ADR-007-clinician-summary-report.md
docs/intelligence/PRIMARY_CONCERN_AND_RANKED_AMBIGUITY_POLICY_v1.md
docs/intelligence/DOMAIN_NARRATIVE_CONTRACT_WAVE1.md
docs/architecture/RETAIL_EXPLAINER_CONTENT_BOUNDARIES_v1.md
knowledge_bus/governance/day_one_launch_estate_gate_v1.yaml
docs/AUTHORITY_MAP.md
```

Supporting only, not authority:

```text
docs/archive/working-papers/download-arch/HealthIQ_FE_VISUALISATION_Surface_Policy_Proposal_v1_fresh.md
docs/frontend/CLAUDE_TRANSLATION_SPEC_v1.md
```

Important:

* `CLAUDE_TRANSLATION_SPEC_v1` is Knowledge Bus research translation, not runtime Layer C.
* The FE Visualisation Surface Policy is draft/supporting only unless AUTHORITY_MAP says otherwise.

---

## Required output file

Create:

```text
docs/architecture/ADR-LAYER-BOUNDARY-RECONCILIATION-1.md
```

If the existing ADR naming convention requires another location or filename, follow the repository convention and explain the deviation in the audit summary.

---

## Required ADR content

The ADR must be concise but authoritative.

Use this structure:

```text
# ADR-LAYER-BOUNDARY-RECONCILIATION-1 — Canonical Layer Boundary Vocabulary

## Status

Accepted / Proposed for acceptance

## Date

2026-06-17

## Context

Explain the naming drift:
- Strategic Vision v1.5 §2.3 defines the intended layer model.
- Pre-Sprint §3.9, ADR_WP2 and NarrativePayloadV1 define the Layer B → Layer C handoff.
- ADR-002 defines the constitutional deterministic engine separation.
- ADR-005 uses A/B/C/D labels differently in the signal pipeline.
- Some deterministic narrative compiler artefacts have historically been labelled Layer C.
- This has created ambiguity over where medical reasoning, WHY, surfacing and presentation belong.

## Decision

Lock the canonical product vocabulary:

### Layer A

Layer A owns ingestion, parsing, canonicalisation and factual normalisation.

Layer A may:
- parse source material
- canonicalise biomarkers
- preserve lab-provided reference ranges
- normalise units
- preserve raw factual inputs

Layer A must not:
- interpret medical meaning
- score biomarkers
- activate signals
- rank findings
- decide what to surface
- generate user-facing health conclusions

### Layer B

Layer B owns all deterministic medical intelligence and explanation.

Layer B owns:
- biomarker interpretation
- signal activation and suppression
- system and subsystem reasoning
- phenotype mapping
- WHY / root-cause reasoning
- evidence-for and evidence-against
- counter-evidence
- missing-marker handling
- confidence, completeness and reliability
- lead-finding hierarchy
- primary concern ranking
- what should be surfaced
- what should be suppressed
- clinician report output
- interpretation display records
- deterministic boilerplate/prose asset selection
- safety boundaries
- prohibited claims
- provenance and traceability for medical claims

Layer B must be the source of truth for:
- what matters
- why it matters
- how strongly it is supported
- what evidence complicates the interpretation
- what the user or clinician is allowed to see

Layer B may produce deterministic prose assets, report sections, explainer selections and structured narrative briefs.

Layer B must not delegate medical reasoning, finding selection, hierarchy, signal activation, WHY or surfacing decisions to Layer C, Gemini, frontend code or any presentation renderer.

### Layer C

Layer C owns presentation and translation of governed Layer B output.

Layer C may:
- present Layer B outputs in a clear user-facing format
- improve wording, flow, tone and readability
- arrange governed sections into a polished report experience
- use deterministic presentation templates
- use a constrained LLM such as Gemini only to translate or polish the governed brief
- render boilerplate modules selected by Layer B
- render clinician/user-facing sections according to the DTO contract

Layer C must not:
- decide findings
- rank findings
- activate or suppress signals
- infer medical meaning
- inspect raw biomarkers outside the governed Layer B brief
- add new medical claims
- change confidence or severity
- change what is surfaced
- create new evidence
- override Layer B
- read raw Pass 3 material or packages at runtime
- perform frontend medical inference

Gemini, if used, is not the analytical engine. It is an optional constrained presentation component inside Layer C.

## Canonical interpretation of existing naming drift

State how to interpret legacy references:

- References to deterministic narrative/report compilers as “Layer C” should be read as presentation/translation output only, not as authority for medical reasoning.
- `NarrativeReportV1` / deterministic narrative compiler output must not be treated as a place to introduce new medical logic.
- ADR-005 A/B/C/D stage labels are local signal-pipeline stages and must not override the product Layer A/B/C vocabulary.
- `NarrativePayloadV1` remains the governed handoff object from Layer B to Layer C.
- Strategic Vision v1.5 §2.3 is the strategic north star for layer responsibility.
- Pre-Sprint §3.9 and ADR_WP2 remain valid when interpreted through this reconciled vocabulary.

## Consequences

Future sprint prompts must:
- explicitly state which layer is being touched
- keep all medical reasoning and surfacing decisions in Layer B
- keep frontend and Layer C render-only / translate-only
- avoid using “Layer C” to mean analytical reasoning
- avoid using Gemini for medical decisioning
- cite this ADR when working on narrative, reports, Gemini, results page, domain cards, clinician reports or boilerplate prose
- stop if implementation would move Layer B responsibilities into Layer C

## Non-goals

This ADR does not:
- implement Gemini
- change runtime code
- change report compilers
- change DTOs
- change frontend behaviour
- alter existing medical logic
- change scoring
- create the beta roadmap
- decide system/domain completion sequencing

## Supporting documents

List and briefly describe:
- Strategic Vision v1.5 FINAL ADOPTED §2.3
- Layer Architecture Authority Index r2
- Late-document addendum
- Pre-Sprint §3.9
- ADR_WP2
- NarrativePayloadV1
- ADR-002
- ADR-005
- ADR-007
- Primary Concern and Ranked Ambiguity Policy
- DOMAIN_NARRATIVE_CONTRACT_WAVE1
- RETAIL_EXPLAINER_CONTENT_BOUNDARIES_v1
- day_one_launch_estate_gate_v1.yaml

## Decision record

State that this ADR is the governing reconciliation document for layer-boundary terminology in future roadmap and sprint planning.
```

---

## Optional authority map update

Inspect `docs/AUTHORITY_MAP.md`.

If it is clearly the repository mechanism for registering authoritative architecture documents, update it to include the new ADR.

Do not rewrite the authority map broadly.

If you update it, add only a minimal entry for:

```text
docs/architecture/ADR-LAYER-BOUNDARY-RECONCILIATION-1.md
```

Classify it consistently with other accepted ADRs.

If unsure, do not update `AUTHORITY_MAP.md`; instead state that the ADR should be added after human review.

---

## Validation requirements

Because this is documentation-only, validation is documentary.

Run:

```powershell
git diff --stat
git diff --name-only
```

Confirm only expected documentation files changed.

Expected changed files:

```text
docs/architecture/ADR-LAYER-BOUNDARY-RECONCILIATION-1.md
docs/AUTHORITY_MAP.md
```

`docs/AUTHORITY_MAP.md` is optional.

No code files may change.

No tests are required unless repository policy enforces documentation checks.

---

## Required final report

Return:

```text
- branch name
- files created/updated
- whether AUTHORITY_MAP was updated
- exact authority ranking used
- exact decision wording for Layer A
- exact decision wording for Layer B
- exact decision wording for Layer C
- how ADR-005 naming drift was handled
- how deterministic narrative compiler naming drift was handled
- confirmation no code files changed
- validation output
- git status --short
```

Do not merge until GPT architectural review and human approval.

---

## Acceptance criteria

This work is complete only if:

```text
1. The ADR clearly states Layer B owns WHY, hierarchy, surfacing, clinician report, boilerplate selection, safety and provenance.

2. The ADR clearly states Layer C is presentation / translation only.

3. The ADR clearly states Gemini is optional and constrained, not the analytical engine.

4. The ADR reconciles Strategic Vision v1.5, Pre-Sprint §3.9, ADR_WP2, NarrativePayloadV1, ADR-002 and ADR-005.

5. The ADR prevents future sprint prompts from assigning Layer B responsibilities to Layer C.

6. No runtime implementation changes are made.

7. No code files are changed.
```
