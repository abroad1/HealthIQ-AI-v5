# HealthIQ AI Strategic Vision v1.5 — Feedback and Hardening Review
*Reviewer: Claude Code (Sonnet 4.6) | Date: 2026-04-03 | Source: live codebase read + roadmap cross-reference*

---

## How to read this document

This is a direct, evidence-grounded review of `HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan_v1.5_draft_master_v3.md`.

It is structured in three parts:

1. **What the document gets right** — genuinely strong positions worth preserving verbatim
2. **Gaps and inaccuracies** — places where the document diverges from actual repo state
3. **Hardening suggestions** — concrete amendments to sharpen the document's truthfulness and governance utility

All findings are grounded in live codebase reads conducted 2026-04-03. Where specific file paths are cited, they reflect current repo state.

---

## Part 1 — What the document gets right

### 1.1 The A / B / C layered model is the platform's most important conceptual anchor

The three-layer model (Canonicalisation → Deterministic Engine → Narrative) is clear, correct, and essential. The enforcement that Layer C must never become the source of analytical reasoning is one of the strongest anti-drift controls in the document. This framing should never be softened in future versions.

**Codebase confirmation:** `backend/core/layer3/insight_assembler_v1.py` carries an explicit header — "No LLM. No timestamps. No UUIDs. Deterministic IDs and ordering only." This is exactly the Layer B / C separation the document prescribes. The principle is already operationalised.

### 1.2 "Breadth is not the same as completion" (§6.4) is the most strategically important statement in the document

This section directly guards against the most plausible drift mode for a platform at this stage. The signal estate has grown substantially (103 canonical biomarkers in SSOT, 187 knowledge bus packages, approximately 234 signals across packages as of 2026-04-03), but the 2026-03-20 Metabolic Pathway Coverage Audit confirms that approximately 30 of ~33 non-homocysteine signals have **no hypothesis asset**. The document's warning is real and warranted — it should be stronger, not softer.

### 1.3 The context-before-narrative sequencing (Wave 5 before Wave 6) is strategically correct

The document correctly refuses to allow narrative translation to precede context hardening. The `LifestyleModifierEngine` (`backend/core/analytics/lifestyle_modifier_engine.py`) is operational and deterministic (Sprint 19 implementation), but its coverage of subjective / behavioural inputs (smoking, stress, exercise) is bounded. Wave 5 represents the governance work needed to make this layer trustworthy for analytical use, not just present.

### 1.4 The anti-drift doctrine (§8) is comprehensive and well-ordered

All five drift modes are real threats and correctly named. "Narrative-first drift" and "disconnected signal-engine drift" are the most acute risks at the current platform maturity. The document articulates the failure modes with enough precision that a new team member could recognise them.

### 1.5 The medication / intervention boundary is appropriately cautious

§6.6's handling of medication context — class-level intervention-effects registry only, no silent threshold alteration, no invented medication-specific reasoning — is the right position. `backend/core/analytics/intervention_annotation_compiler_v1.py` and `backend/core/analytics/intervention_selector_v1.py` already implement this at code level.

### 1.6 The phase vision (engine → dataset → regulated moat) is the correct long-term frame

The three-phase company vision (§5) is coherent and matches the architectural decisions being made in Phase 1. The investment in governed deterministic truth now creates the longitudinal dataset moat later. This framing should be stable across all future document versions.

---

## Part 2 — Gaps and inaccuracies

### 2.1 CRITICAL — Sprint numbering divergence: the roadmap describes a future that is already partially history

**The most significant accuracy problem in v1.5.**

The roadmap describes KB-S45 through KB-S58 as the 12-month build plan, structured across Waves 1–4. But the live repo as of 2026-04-03 is at **KB-S61**. The sprint numbering has diverged:

| Roadmap says | Actual repo |
|---|---|
| KB-S58 = "Phenotype / Fixture / Regression Expansion" | KB-S58 = ingest CBC hematology Pass 3 batch into 22 packages (KBP-4796–4817) |
| KB-S56 = "Renal Research Promotion + Renal WHY Completion" | KB-S56 = Wave C tranche 1 packages (globulin, total_protein, zinc paths) |
| KB-S53 = "AB/VR Panel Formalisation + Acceptance Harness" | KB-S53 = classify Wave C blockers and define unblock tranches |

This is not a minor numbering detail. A reader using this document as a sprint planning guide would assign wrong meaning to KB sprint IDs. A GPT sprint author writing against this roadmap could create work packages with the wrong sprint number, wave position, or strategic context.

**Recommendation:** Either reframe the roadmap so it describes remaining work (removing completed sprints from the wave plan and updating to current baseline) or clearly annotate which sprint IDs are historical and which are upcoming. The current draft presents all KB-S45–S58 items as future planned work, which is materially misleading.

### 2.2 SIGNIFICANT — WHY depth gap is understated relative to what the March 2026 audit found

The document says "WHY / root-cause coverage remains too shallow relative to live signal breadth" (§6.3). This is correct but understated.

The 2026-03-20 Metabolic Pathway Coverage Audit (`docs/METABOLIC_PATHWAY_COVERAGE_AUDIT_2026-03-20.md`) documents:

- **~30 of ~33 non-homocysteine signals have no hypothesis asset**
- `signal_lipid_transport_dysfunction`, `signal_ldl_cholesterol_high`, `signal_hdl_cholesterol_low`, `signal_triglycerides_high` — all four lipid signals: **no hypothesis coverage**
- `signal_systemic_inflammation`, `signal_crp_high`, `signal_inflammation_crp_context`, `signal_neutrophils_high`, `signal_wbc_high` — all five inflammation signals: **no hypothesis coverage**
- All six iron / oxygen transport signals: **no hypothesis coverage**
- All four renal signals: **no hypothesis coverage**
- `root_cause_compiler_v1.py` currently registers loaders for only a handful of signals: ALT, HbA1c, Hcy, TSH, insulin resistance, and systemic inflammation (the last two described as added in KB-S46, status unconfirmed)

The document warns about the WHY gap. But the phrase "remains too shallow" significantly undersells what the audit found. "The majority of live signals produce no WHY reasoning at runtime" is more accurate and would create appropriate urgency.

**Recommendation:** Add a quantified WHY gap statement to §6.3. Something of the form: "As of the last pathway audit, the majority of live signals produce no root-cause hypothesis output at runtime — the WHY estate covers fewer than one in five active signals."

### 2.3 SIGNIFICANT — Renal status is understated: zero interaction edges is not merely a "weak point"

The document describes renal as "a gated structural weak point" (§6.3). The audit is more precise: the renal pathway has **zero active interaction map edges**. `ph_renal_stress_v1` exists as a phenotype fixture but its chain enforcement is marked pending because edges are missing.

This means:
- Renal signals fire at runtime
- No cross-signal interaction reasoning fires
- The phenotype fixture cannot be properly validated
- System-level burden scoring for renal is structurally incomplete

This is not a weakness in the ordinary sense — it is a structural gap that makes renal output unreliable. The document should label this more precisely.

**Recommendation:** Replace "renal remains a gated structural weak point" with something like "renal remains structurally incomplete: the interaction map has zero active edges for renal signals, and the phenotype fixture cannot be validated until this is resolved. Renal output at runtime is incomplete and should not be treated as governed truth."

### 2.4 SIGNIFICANT — Authentication is a non-functional stub, not merely a pending Wave 6 item

The document schedules FE-S3 "Customer Login and My Account Layer" in Wave 6 as the product shell completion sprint. This is the correct wave sequencing. However, the current state of authentication in the codebase is worth flagging explicitly:

`frontend/app/services/auth.ts` line 11:
```
const API_BASE_URL = 'about:blank';
```

The auth service was explicitly disabled ("Disabled: backend auth routes are not present"). The Supabase library is present (`frontend/app/lib/supabase.ts`) but has no active backend integration. The frontend app group contains `dashboard`, `analysis`, `reports`, `profile`, and `settings` routes — but none of these are behind a working auth gate.

This means the "customer-facing product experience" described as the Phase 1 launch deliverable is currently built on a fully broken auth foundation. The document should acknowledge this gap explicitly in §6.3 so the urgency of FE-S3 is appropriately communicated.

**Recommendation:** Add to §6.3: "Authentication is not yet functional — the auth service is currently a disabled stub. FE-S3 addresses a foundational gap, not an incremental enhancement."

### 2.5 MODERATE — Section 6.2 "materially advanced" breadth claims need quantification

§6.2 says the platform's signal breadth has "advanced materially beyond the original 'six batches / 56 additional biomarkers' framing" but provides no numbers.

Current measurable state as of 2026-04-03:
- 103 canonical biomarkers registered in `backend/ssot/biomarkers.yaml`
- 187 knowledge bus packages in `knowledge_bus/packages/`
- ~234 signals across packages
- Latest sprint: KB-S61 (transferrin pass 3, KBP-4829–4831)

Adding these numbers to §6.2 would make the document honest and usable as a planning reference for anyone picking it up cold.

### 2.6 MODERATE — The Wave 4 phenotype/fixture/regression sprint (described as KB-S58) has not run as described

The roadmap's Wave 4 places KB-S58 as "Phenotype / Fixture / Regression Expansion." The actual KB-S58 was CBC hematology Pass 3 ingestion. The phenotype, fixture, and regression expansion work described in Wave 4 is **still outstanding** — it has not been completed and simply carries the wrong sprint ID in the roadmap.

This matters because:
1. A reader might assume this work is done
2. It conflates ingestion completion with structural truth work, which the document itself describes as distinct

### 2.7 MODERATE — Wave 6 ordering: narrative before account management is a risk

Wave 6 sequences: BE-S1 (Narrative) → FE-S2 (Narrative Presentation) → FE-S3 (Login and Account) → OPS-S1 (Launch Readiness).

In practice, FE-S3 (auth) is a prerequisite for any customer-facing narrative to be usable. If BE-S1 and FE-S2 are built before auth is real, the result is a narrative layer sitting behind a broken door. While the wave numbering doesn't strictly imply sequential execution, the ordering could be read to deprioritise auth.

**Recommendation:** Either reorder Wave 6 to show auth as the first gating item, or add an explicit note that FE-S3 must be at minimum parallel to narrative work, not after.

### 2.8 LOW — The LLM layer already partially exists: Wave 6's BE-S1 is not starting from zero

The document treats BE-S1 (LLM Narrative Production Enablement) as a future Wave 6 creation. However, the following LLM infrastructure already exists in the codebase:

- `backend/core/llm/prompts.py`
- `backend/core/llm/schemas_v2.py`
- `backend/core/llm/validator_v2.py`
- `backend/core/insights/synthesis.py`
- `backend/core/insights/prompts.py`
- `docs/CLAUDE_TRANSLATION_SPEC_v1.md`
- `docs/HealthIQ AI v5_LLM Prompt.pdf`

BE-S1 should be framed as "govern and activate existing LLM infrastructure on top of governed structured output" rather than "build narrative production from scratch."

### 2.9 SIGNIFICANT — Age/sex scoring adjustments are defined but not applied at runtime

A deep codebase read reveals a concrete analytical correctness gap that the roadmap does not address:

`backend/core/scoring/rules.py` — age and sex scoring adjustments are defined but **not applied** in `calculate_biomarker_score()`. The logic exists; the call does not.

This matters strategically because:
- The questionnaire collects `date_of_birth` and `biological_sex` as required fields
- The platform's SSOT (`backend/ssot/questionnaire.json`) designates these as inputs that enable "sex-specific thresholds possible at runtime"
- The scoring policy and registry have age/sex modifiers available
- But at runtime, biomarker scores are computed without those modifiers

This is not a minor edge case. Age and sex materially change the interpretation of multiple high-frequency biomarkers (ferritin, haemoglobin, testosterone, TSH, creatinine). Producing scored output without applying these adjustments means the platform is currently outputting analytically weaker results than its own data model supports.

The document's Wave 5 (Context Hardening) should explicitly call out that context *collection* is largely in place, but context *application in analytical scoring* is incomplete. The scoring gap is within Layer B (not Layer A), which means it directly affects the deterministic engine's truthfulness.

**Recommendation:** Add this to §6.3 as a specific incomplete area: "Age and sex scoring adjustments are defined in the scoring policy but not currently applied in the scoring engine — this is a Layer B correctness gap that Wave 5 or an earlier sprint must explicitly address."

### 2.10 LOW — The docs directory contains a large number of unlisted planning artifacts

The `docs/` directory contains over 40 documents that are not referenced in the roadmap:
- Multiple sprint delivery reports (Sprint 2–9)
- Architecture review reports, deprecated architecture notices
- A v5.2 delivery sprint plan that predates this document
- Several "root cause analysis" documents on resolved bugs

The strategic roadmap should not be the document that inventories these, but it would benefit from explicitly noting that `docs/` carries historical artifacts and pointing readers to the governance hierarchy document (`docs/DOCUMENTATION_HIERARCHY.md`) to understand which documents are authoritative.

---

## Part 3 — Hardening suggestions

### 3.1 Add a "Current Baseline State" table to §6

Replace the prose descriptions with a factual snapshot table. This anchors the document to a specific date and forces future updates when it's refreshed:

| Metric | State as of 2026-04-03 |
|---|---|
| Latest completed sprint | KB-S61 (transferrin pass 3) |
| Canonical biomarkers in SSOT | 103 |
| Knowledge bus packages | 187 |
| Signals across packages | ~234 |
| Signals with hypothesis coverage | ~3–6 (of ~33+ non-trivial signals) |
| Pathways with zero interaction edges | 1 (renal) |
| Authentication status | Disabled stub — FE-S3 not started |
| Narrative / LLM layer | Infrastructure exists, not governed for production |

### 3.2 Add a "What has been completed" section before the wave plan

The 12-month wave plan in §10 reads as if everything from Wave 1 is pending. A brief completed-work section before the wave descriptions would stop the document from being misread as a greenfield plan. Something like:

> **As of v1.5 (April 2026), the following has materially advanced:**
> - Breadth ingestion through KB-S61 (exceeds original 6-batch plan)
> - Knowledge Bus governance and SOP alignment (v1.3.1)
> - Signal evaluator, scoring policy, and arbitration registry wiring
> - Layer 3 insight assembler (deterministic, no LLM)
> - Clinician report v1 contract and renderer path
> - Intervention-effects registry foundation
> - Lifestyle modifier engine (deterministic, bounded additive modifiers)
> - Cluster engine v2 (schema-driven)
>
> **What remains the primary build programme:**
> - WHY hypothesis coverage for the majority of live signals
> - Renal interaction map edges and chain enforcement
> - Phenotype and fixture expansion across the enlarged estate
> - Context hardening and governed analytical consumption
> - Auth, product shell, and launch readiness

### 3.3 The sprint ID range in Wave 1–4 needs replacing

Since the roadmap's KB-S45–S58 wave sprint IDs no longer match repo reality, consider replacing specific sprint ID references in §10 with logical sprint labels instead (e.g., "WHY-Expansion-Insulin-Resistance", "Renal-Unblock", "Phenotype-Fixture-Expansion"). This prevents the document from becoming inaccurate each time the sprint numbering advances.

Alternatively, the document could reference sprint IDs explicitly and commit to a versioned update process whenever sprint IDs are assigned.

### 3.4 Add a "Platform truth readiness" gate to §4

The Phase 1 success definition in §4 lists deployment readiness criteria. It could be strengthened by adding an explicit analytical truth gate before the product shell criteria:

> **Analytical truth gate (prerequisite for launch readiness):**
> - WHY hypothesis coverage for all six primary metabolic pathways
> - Renal interaction map edges promoted and chain-enforcement fixture validated
> - Phenotype fixtures pass regression for all governed pathways
> - Governed context inputs analytically consumed (not merely collected)
> - No known determinism violations in analytical pipeline

This makes §4 a checklist, not just a description — and guards against a scenario where product shell work (auth, narrative, frontend) is completed while analytical truth remains materially incomplete.

### 3.5 Address the longitudinal data model gap

Phase 2 ("Dataset moat") depends on repeat-panel journeys, intervention tracking, and longitudinal identity continuity. The document describes this vision clearly in §14. But Phase 1 makes no mention of the data persistence architecture required to support it.

`backend/core/models/database.py` exists, but there is no discussion in the roadmap of whether the current persistence model is capable of longitudinal linking. If Phase 2 requires a schema migration of Phase 1 data, that migration cost should be acknowledged in Phase 1 planning.

**Recommendation:** Add a brief note to §14 (or §6.3) that the longitudinal data model is a Phase 2 design concern that should not be left completely unexamined during Phase 1 system design.

### 3.6 OPS-S1 should explicitly include CI/CD pipeline hardening

`docs/CI_CD_PIPELINE.md` exists. The OPS-S1 sprint description says "privacy, security, and deployment-readiness foundations" — but does not mention CI/CD pipeline hardening, which is a standard launch-readiness requirement. If OPS-S1 is the last sprint before Phase 1 launch, it should explicitly cover the automated build and deployment pipeline.

### 3.7 The governance bus itself is a platform moat — name it as such in §1 or §2

The Automation Bus SOP v1.3.1, work package kernel, gate protocol, and prompt hardening discipline are genuinely unusual capabilities for an early-stage team. The document describes the platform's analytical moat clearly but nowhere acknowledges that the *governance infrastructure itself* is a defensible advantage — it means the platform can maintain deterministic truth at scale, something most competitors cannot claim.

Naming this in §1 or §2 (even briefly) would help future team members understand why the governance overhead exists and why it should not be traded away for speed.

---

## Part 4 — Summary verdict

The document is strategically sound and conceptually strong. The A/B/C model, breadth-depth braid discipline, context-before-narrative sequencing, and anti-drift doctrine are all correct positions. The document is genuinely useful as a strategic record.

Its primary weaknesses are accuracy gaps, not strategic errors:

| Priority | Issue |
|---|---|
| CRITICAL | Sprint ID numbering divergence — roadmap's KB-S45–S58 wave plan doesn't match what the repo has already executed |
| SIGNIFICANT | WHY depth gap understated — should cite the ~30/33 signal gap figure from the March 2026 audit |
| SIGNIFICANT | Renal described as "weak point" — should be described as structurally incomplete (zero interaction edges) |
| SIGNIFICANT | Auth is a disabled stub — the document should flag this explicitly rather than treating FE-S3 as a normal Wave 6 enhancement |
| MODERATE | §6.2 needs quantification — breadth claims need actual numbers |
| MODERATE | Wave 4 phenotype/regression sprint has not executed as described |
| MODERATE | Wave 6 ordering risk — auth should gate or parallel narrative work |
| SIGNIFICANT | Age/sex scoring adjustments defined but not applied in `scoring/rules.py` — Layer B correctness gap |
| LOW | BE-S1 narrative infrastructure partially exists |
| LOW | Longitudinal data model not addressed |
| LOW | CI/CD not listed in OPS-S1 scope |

The document is recommended for revision before use as a governance or sprint-planning reference. The sprint numbering discrepancy in particular must be resolved before this can serve as the authoritative planning record.

---

*End of feedback document. All file path references reflect live codebase state as of 2026-04-03.*
