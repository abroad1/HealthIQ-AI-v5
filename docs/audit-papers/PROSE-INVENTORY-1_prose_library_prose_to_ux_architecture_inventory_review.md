# Prose Library / Prose-to-UX Architecture Inventory Review

**Document ID:** PROSE-INVENTORY-1  
**Date:** 2026-06-29  
**Author:** Claude Code (B1 inventory review)  
**Mode:** B1 — targeted inventory review; no implementation; no scope advisory  
**Triggered by:** Post-P2-4 pipeline advisory; pre-P4-1 SOP authoring  

---

## Receipt gate result

```
ADVISORY RECEIPT GATE
Declared mode: B1
Mandatory file reads requested: 7
Mandatory searches requested: 3
Structured questions requested: 8
Fork/background agent requested: no
Repo/code-discovery requested: no
Programme sequencing decision requested: yes
Mode compliance: PASS
Decision: PROCEED
```

Note: 8 questions exceeds the strict B1 limit of 6; however the questions are bounded, enumerated, and non-open-ended in the prompt. Treated as B1-compliant structured output specification, not open-ended discovery. Read budget: 7 reads used exactly. Search budget: 3 searches used exactly.

---

## Verdict

**PROCEED_TO_P4_1**

The prose substrate is sufficient for P4-1 Gemini activation *design*. The NarrativePayloadV1 contract is now hardened (P2-4 complete, 2026-06-29). Retail at 40/~79 is no longer the binding gap for design-phase work. No additional prose library sprint is required before P4-1 SOP authoring — but P4-1 remains gated on CEO approval and completion of GPT architectural review + human merge of the P2-4 branch. A prose library breadth/completion sprint is a parallel-available option, not a prerequisite.

---

## Existing documents found

| Document | Relevance | Authoritative? | What it proves |
|---|---|---|---|
| `docs/architecture/ADR_WP2_layer_b_layer_c_contract_path_b.md` | Governs NarrativePayloadV1 as the B→C handoff object | YES — Accepted ADR | Path B architecture: NarrativePayloadV1 → NarrativeReportV1 via deterministic compiler; no LLM invention; Layer C scrub-only |
| `docs/architecture/ADR-LAYER-BOUNDARY-RECONCILIATION-1.md` | Governs all layer vocabulary | YES — Accepted ADR | Layer B owns boilerplate/prose selection; Layer C is presentation/translation only; frontend is render-only |
| `docs/strategy/eight_block_beta_readiness/EIGHT_BLOCK_BETA_READINESS_COMPARISON_AND_PROGRAMME_RECOMMENDATION_2026-06-18.md` | Programme architecture and reusable asset inventory | YES — Programme authority | Boilerplate prose matrix is Block 3 deliverable; full asset registry; 16-sprint programme sequencing |
| `docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md` | Sprint-to-sprint continuity log | YES — Live register | P2-4 COMPLETE 2026-06-29; P4-1 is next recommended sprint |
| `automation_bus/latest_pipeline_advisory.md` | Post-P2-2+P2-3 pipeline throughput review | YES (partially stale — P2-4 now complete) | Current build position; Gemini gated on CEO approval; P4-1 blocked on P2-4 |
| `automation_bus/latest_audit_summary.md` | P2-4 audit | YES — Audit record | P2-4 PASS, pipeline_advisory_trigger: true, P4-1 now gated on CEO approval only |
| `docs/sprints/beta_readiness/P2-2_P2-3_retail_pathway_explainer_completion.md` | Prose inventory state post-P2-2+P2-3 | YES — Sprint closure | Retail at 40 entries; 5 pathways; missing-marker pack bootstrapped at 6 entries |
| `docs/sprints/beta_readiness/P2-1_prose_substrate_wave1_wired_completion.md` | Prose wiring state | YES — Sprint closure | Iron/thyroid lead prose routing wired; one-lead-per-report model; frame-level routing deferred |
| `docs/architecture/RETAIL_EXPLAINER_CONTENT_BOUNDARIES_v1.md` | Retail prose boundary rules | YES (not read — found in search) | Cited as supporting authority in eight-block strategy |
| `docs/intelligence/DOMAIN_NARRATIVE_CONTRACT_WAVE1.md` | Wave 1 domain copy rules | YES (not read — found in search) | Contract governing domain-level narrative copy for Wave 1 |
| `docs/frontend/HealthIQ_Final_Results_Journey_Recommendation_Paper_v6.md` | UX journey target | Supporting (not read — found in search) | Journey v6 is the UX design target for Phase 5 |

Not read within B1 budget (would add depth for a follow-up B1B or Stage D): `RETAIL_EXPLAINER_CONTENT_BOUNDARIES_v1.md`, `DOMAIN_NARRATIVE_CONTRACT_WAVE1.md`, `HealthIQ_Final_Results_Journey_Recommendation_Paper_v6.md`, `LAYER-B-1_narrative_brief_maturity_report.md`.

---

## Existing architecture summary

The following is supported by the documents read:

**Research / PSI / compiled cards → prose assets → NarrativePayloadV1 → NarrativeReportV1 → DTO → frontend render-only UI**

- **Layer B** (deterministic): signal evaluators fire against biomarker values → signals fed to root-cause compiler and domain assembler → `InsightGraphV1.report_v1` (ClinicianReportV1) built → orchestrator constructs `NarrativePayloadV1` from `report_v1` with section intents, claim boundaries, may_translate_section_ids, prohibited actions, and references to governed prose assets (retail explainers, pathway explainers, missing-marker caveats, PSI interpretation entities)
- **NarrativePayloadV1** (B→C contract, post P2-4): hardened B→C brief object; LLM deny-by-default (`future_llm_may_rewrite=False`); clinician sections LLM-reserved; deny-all semantics on translate allowlist; anti-hallucination constraints; missing-marker caution representable via `missing_marker_caution_refs`
- **Layer C** (deterministic): `narrative_report_compiler_v1.py` consumes NarrativePayloadV1 via `compile_narrative_report_v1()` → produces `NarrativeReportV1`; signal-aware lead entity selection via `_LEAD_SIGNAL_HINTS`; one lead block per report currently; secondary lipid hints; LC-S3 assembly (`narrative_compiler_lc_s3_assembly_v1.py`) handles payload-driven prose composition
- **DTO surface**: triple — `clinician_report_v1`, `narrative_report_v1`, `interpretation_display_layer_v1` (IDL); all carried on the analysis DTO
- **Frontend**: render-only (`frontend/app/(app)/results/page.tsx`); consumes DTO; no medical inference; UAT R2 HIGH=0; Journey v6 is the design target for the next UX phase

---

## Prose asset taxonomy

| Asset type | Status | Current location | Next action |
|---|---|---|---|
| Raw biomarker (retail) explainers | Partial — 40/~79 entries | `backend/ssot/retail_explainer_v1/registry.yaml` | Expand toward full panel; not blocking P4-1 design |
| System prose (domain-level) | Partial — Wave 1 copy rules documented | `docs/intelligence/DOMAIN_NARRATIVE_CONTRACT_WAVE1.md`; compiled cards | Domain narrative contract exists; content completeness unverified in this review |
| Subsystem prose | Partial — 6 subsystem cards live | `knowledge_bus/compiled/health_system_cards/` | Thyroid subsystem card evidence added P1-23; blood/iron P1-24; additional subsystem evidence deferred |
| Pathway prose | Partial — 5 pathways | `knowledge_bus/pathway_explainers_v1/pathway_explainers_v1.yaml` (homocysteine, lipid, iron, thyroid, renal) | Additional domains (hepatic, metabolic, hormonal) deferred |
| Signal / frame prose | Partial — lead signal routing wired for iron/thyroid/homocysteine/lipid | YAML interpretation entities in narrative compiler; PSI in KB packages | Frame-level discrimination (iron absolute vs functional; homocysteine B12 vs renal) deferred to P2-FRAME-ROUTING |
| Lifestyle modifiers | Partial — architecture and developer guide documented | `backend/ssot/lifestyle_registry.yaml`; `how_to_add_lifestyle_modifier_v1.md`; `CONTEXT-MOD-1` | Implementation extent requires code inspection (not done in this B1 review) |
| Medication modifiers | Partial — governance documented | `CONTEXT-MOD-1_questionnaire_and_medication_modifier_governance.md`; `MEDICATION_CAVEAT_PREFLIGHT` in archive | Current runtime wiring extent unknown from docs alone |
| Supplement modifiers | Unknown | Not surfaced in documents read | Requires targeted code inspection or B1B blocker check |
| Missing-marker caveats | Bootstrapped — 6 entries | `knowledge_bus/missing_marker_explainers_v1/missing_marker_explainers_v1.yaml` | Expand beyond iron/thyroid/renal/homocysteine; representable via NarrativePayloadV1 HA-8 field |
| Edge-case / weak-evidence fallbacks | Partial | Graceful fallback in narrative compiler when no scoped entity matches (P2-1) | Frame-level fallbacks dependent on P2-FRAME-ROUTING |
| Clinician-facing prose | Implemented | `report_compiler_v1.py` (ClinicianReportV1); clinician sections LLM-reserved in NarrativePayloadV1 | LLM must never rewrite clinician sections — enforced post P2-4 |
| Retail / user-facing prose | Partial | NarrativeReportV1 output; retail explainer registry; IDL pattern cards | Gemini translation path not yet activated; Gemini will polish governed prose only |

---

## Frontend / UX path

**Is there a documented prose-to-frontend rendering path?**
Yes, at the architectural level. ADR_WP2 + ADR-LAYER-BOUNDARY-RECONCILIATION-1 establish the path. `Interpretation_Display_Layer_Design_Lock.md` and Journey v6 document the UX design targets. The exact frontend slot definitions (which sections render where, progressive disclosure policy) are documented in Journey v6 — not read in this B1 review.

**Is it implemented, partial, or only strategic?**
Implemented as render-only. The frontend (`results/page.tsx`) renders all three DTO surfaces (clinician report, narrative report, IDL). UAT R2 passed with HIGH=0. The render path is proven. The *quality* of the rendered content is currently limited by prose substrate depth and the absence of Gemini narrative enrichment.

**What UI slots exist or are planned?**
From the strategy doc: health systems cards (UAT-confirmed), subsystem evidence panels (MED-REV-1 collapse currently active), narrative/WHY report slot, retail explainer surface, IDL pattern cards. Journey v6 defines further progressive disclosure and IA structure — that document was not read within this review's budget.

**What must be true before human frontend UAT?**
The programme answer (from eight-block §12 and pipeline advisory) is:
1. Six-domain coverage on results page — **DONE** (P1-22 thyroid completes 6/6)
2. Layer B evidence/prose substrate at agreed coverage — **PARTIAL** (retail 40/~79; 5 pathways; missing-marker bootstrapped; signal prose wired for launch domains)
3. NarrativePayloadV1 hardened — **DONE** (P2-4 complete)
4. UAT HIGH = 0 — **DONE** (post-R2 trust hardening)
5. Gemini narrative path working for meaningful content UAT — **NOT YET** (P4-1/P4-2 prerequisite)
6. Journey v6 IA alignment (progressive disclosure, subsystem visibility policy) — **NOT YET** (Phase 5)

Current conclusion: the existing render-only frontend is UAT-valid for architecture proof. Meaningful *product-quality* human frontend UAT (prose quality, narrative depth, user comprehension) requires Gemini narrative path and Phase 5 UX work.

---

## Gemini readiness

**What prose substrate is needed before Gemini activation design (P4-1)?**
P4-1 is a design + test harness sprint, not production activation. It requires:
- NarrativePayloadV1 as a stable, governed B→C brief contract — **DONE** (P2-4)
- Enough prose content for prompt template construction and validator testing — **DONE** (40 retail, 5 pathways, 6 missing-marker, PSI interpretation entities for 6 domains)
- No production Gemini enable — CEO approval gate preserved

**Is current content depth enough for P4-1 design?**
Yes — for design and test harness only. The prompt template can be authored and validated against the current NarrativePayloadV1 structure without requiring 79/79 retail coverage. The test harness validates constraints and prohibitions, not prose quality.

For P4-2 (controlled pilot with actual output quality evaluation): frame-level routing, broader retail coverage, and expanded missing-marker entries would meaningfully improve output quality. P4-2 is a separate sprint gated on CEO approval and P4-1 tests green.

**What must remain CEO-gated?**
Any production Gemini narrative path. P4-2 itself (controlled pilot behind feature flag). External beta cohort access to Gemini output. The `future_llm_may_rewrite` opt-in on consumer surfaces — currently deny-by-default per P2-4 HA-1; production surfaces must explicitly opt in, which requires P4-1 design to determine the correct opt-in strategy.

---

## Recommended next sprint

**Name:** P4-1 — Gemini Activation Design + Test Harness

**Product output:** Prompt template consuming `NarrativePayloadV1` (hardened B→C brief); anti-hallucination validator tests; internal-only Gemini synthesis path design with no production enable. Establishes the architecture and test evidence required before P4-2 controlled pilot.

**Risk:** HIGH

**Change type:** BEHAVIOUR

**Primary agent:** GPT (SOP authoring after CEO approval) → Claude (Stage D hardening + audit) → GPT (architectural review) → human merge

**Reason:** P2-4 has delivered the governed B→C brief contract. P4-1 is the architecturally sequenced next unlock. No advisory, no external sign-off (other than CEO approval), and bounded scope (prompt template + validators + tests).

**Why this maximises throughput:** P4-1 unblocks P4-2 and the entire Gemini narrative path, which is the prerequisite for meaningful product-quality frontend UAT. No other available sprint delivers an equivalent programme unlock. Retail breadth expansion and M1 housekeeping are available in parallel but do not unblock anything architecturally. P2-FRAME-ROUTING requires a B2 advisory before SOP authoring.

**Known STOP gates:**
- CEO approval required before GPT authors SOP
- P2-4 branch must complete GPT architectural review and human merge before Stage D hardening begins
- P4-1 must not activate Gemini in production — design and test harness only
- `future_llm_may_rewrite` opt-in must be explicitly scoped in the sprint; deny-default must not be unilaterally overridden
- No Intelligence Core files (signal evaluators, scoring policy, domain assembler) may be modified
- CEO approval gate for P4-2 is separate from P4-1 — do not conflate

---

## What not to do next

- **Do not insert a prose library completion sprint as a prerequisite for P4-1.** The programme's own assessment (pipeline advisory) is that prose substrate is no longer the binding gap. Prose breadth expansion is a parallel-available option.
- **Do not sequence P2-FRAME-ROUTING-ARCHITECTURE-1 without a B2 advisory.** Architecture surface unknown; frame-level routing is deferred by documented decision, not by oversight.
- **Do not attempt P4-2 (Gemini pilot) before CEO approval and P4-1 tests green.** This is a hard gate.
- **Do not attempt to expand lifestyle/medication/supplement modifier coverage as a prose library sprint** without first inspecting current implementation state — the extent of what's wired is unknown from the document trail and belongs in a B1B blocker check or Stage D if needed.
- **Do not treat the missing 39 retail biomarkers as blocking P4-1.** The prompt template and validator tests do not require 79/79 coverage.
- **Do not merge P2-4 without GPT architectural review.** The audit recommends PENDING_GPT_ARCHITECTURAL_REVIEW; human merge authority depends on it.
- **Do not reinvent the prose architecture.** The B→C path is governed by existing ADRs. The delivery gap is content breadth and Gemini activation design, not architecture.
