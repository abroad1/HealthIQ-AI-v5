---
work_id: CLIN-PRIORITY-ARCH-HARDEN-1
branch: docs/clin-priority-arch-harden-1
risk_level: HIGH
execution_model: SINGLE_PHASE
change_type: CONTENT
---

# Cross-Domain Clinical Prioritisation — Architecture Hardening Report

## 1. HARDENING VERDICT

`HARDENED_READY_FOR_ANTHONY_ARCHITECTURE_APPROVAL`

**Correction note (this revision — second correction).** The prior version of this report incorrectly treated matters already closed by the ratified clinical package — the literal BSG hepatic Tier 1 floor, the hypokalaemia/hypernatraemia/hypocalcaemia bands, and general domain-ruleset reconciliation — as open architecture blockers. They are not. The governing authority hierarchy is: contract v0.6.3, cross-domain ruleset v0.5, HMR adjudication register v0.4 and six-domain closure report v0.4 are the current ratified clinical authority. The six individual domain rulesets and the supplemental electrolyte evidence document are subordinate historical/evidentiary inputs; where their draft content conflicts with or has been superseded by the later ratified package, the ratified package governs and the domain draft's unresolved register is not carried forward as a live blocker. See §5 for the corrected gap classification.

All seven required architecture decisions (§6-§12) are explicit and repository-grounded. The remaining gaps are classified `IMPLEMENTATION DELIVERABLE`, `RELEASE-ONLY DEPENDENCY`, `OPEN PRODUCT / REGULATORY / LEGAL AUTHORITY`, or `NON-BLOCKING REPOSITORY OBSERVATION` (§5) — none is an unresolved architecture decision. **This verdict certifies architecture-hardening completeness only.** It does not, by itself, make a Cursor implementation prompt eligible to be authored — that is a separate gate governed by contract §23.6, corrected in §3 and §19 below.

**Six distinct readiness states — do not collapse these into one:**

| State | Status after this correction |
|---|---|
| **Architecture approval** (this report, Anthony) | Ready to seek — verdict above |
| **Cursor prompt authoring** (contract §23.6) | **Prohibited** — four of eight §23.6 conditions remain open regardless of architecture approval (§19) |
| **Implementation execution** (Cursor building Package A) | Cannot begin until Cursor prompt authoring is eligible |
| **Tier 0 activation** (contract §17) | Blocked — R1 open; architecture keeps it unreachable by design (§10) |
| **Runtime reliance on questionnaire context** | Blocked — `CF-QUESTIONNAIRE-CONTEXT-1/2` open (§11.3) |
| **Release approval** | Blocked — R1, R5, R6 and questionnaire remediation all open (§17) |

## 2. Documents and repository paths read

**Mandatory closed list (25/25 read in full):**
`AUTOMATION_BUS_SOP_v1.3.1.md`; `KNOWLEDGE_BUS_SOP_v1.3.1.md`; `KNOWLEDGE_BUS_PASS3_PROMOTION_PROTOCOL_v1.1.md`; `docs/governance/healthiq_pre_sop_prompt_scoping_workflow_v0_6.2.md`; `docs/sprints/healthiq_day_one_architecture_rework_sprint_plan_FINAL.md`; `docs/architecture/ADR-RT-001_research_to_runtime_day_one_architecture.md`; `ADR-RT-002_signal_spec_identity_and_registry_policy.md`; `ADR-RT-003_hypothesis_artefact_and_root_cause_transition.md`; `ADR-RT-004_compile_manifest_and_package_provenance_policy.md`; `docs/discussion documents/HEALTHIQ_CLINICAL_FINDING_PRIORITISATION_CONTRACT_v0_6_3.md`; `HEALTHIQ_CROSS_DOMAIN_CLINICAL_PRIORITISATION_RULESET_v0_5.md`; `HEALTHIQ_CROSS_DOMAIN_HMR_ADJUDICATION_REGISTER_v0_4.md`; `HEALTHIQ_SIX_DOMAIN_CLINICAL_CLOSURE_REPORT_v0_4.md`; `docs/audit-papers/HEALTHIQ_UPLOAD_QUESTIONNAIRE_CONTEXT_AUDIT_v0.1.md`; `HEALTHIQ_ELECTROLYTE_SUPPLEMENTAL_EVIDENCE_v0_1.md`; `HEALTHIQ_HMR_SIX_DOMAIN_RECONCILIATION_v0.1.md`; the six domain rulesets (haematology v0.1, hepatic v0.2, renal/electrolyte v0.1, iron/inflammatory v0.1, thyroid/endocrine v0.1, cardiometabolic/nutritional v0.1); `docs/sprints/launch_core_carry_forward_register.md`; `backend/ssot/questionnaire.json`; `knowledge_bus/governance/active_signal_context_gate_reachability_policy_v1.yaml`.

**Bounded discovery (5/5 searches, 4 additional files read, within the 10-file allowance):**
1. Canonical finding/DTO search → `backend/core/models/insight.py`.
2. Concern-construction/assembly search → `backend/core/analytics/insight_graph_builder.py`, `backend/core/contracts/insight_graph_v1.py`.
3. Compile/promotion path search → `backend/scripts/compile_pass3_pilot_artifacts.py`.
4. Loader/registry search → `backend/core/analytics/signal_evaluator.py` (`SignalRegistry`, targeted grep on activation-key logic).
5. Test-estate search → `Glob` for `backend/tests/**/*concern*` and `**/*prioriti*` — **zero matches** for either pattern.

## 3. Documented clinical authority

`DOCUMENTED FACT` — governing authority and supersession hierarchy:

1. **Ratified package (current governing authority):** contract v0.6.3, cross-domain ruleset v0.5, HMR adjudication register v0.4, six-domain closure report v0.4. All four are status `CLINICALLY_RATIFIED_FOR_ARCHITECTURE_HARDENING`, `implementation_status: NOT_AUTHORISED`. **No clinical adjudication from this package remains open** — the adjudication register §3 "Open clinical-item register" is explicitly empty, and the closure report §5 states "No clinical adjudication from this package remains open" without qualification.
2. **Closed within the ratified package, not open:**
   - The hepatic Tier 1 floor is `CLINICALLY_ADJUDICATED — CLOSED` (adjudication register §2, B1; ruleset §2, `XD-HEP-FLOOR-1`): "Adopt the BSG position literally... No magnitude-gated alternative is retained." This closes what the hepatic domain ruleset's own `HEP-U1` posed as an open question. **HEP-U1 is superseded and is not a live blocker** — it is exactly the kind of "domain draft conflicts with the later cross-domain package" case the ratified package's own supersession language anticipates (ruleset §16, "settled positions preserved unchanged").
   - Hypokalaemia, hypernatraemia and hypocalcaemia bands are incorporated and adjudicated in the ratified package: ruleset §3 "Fixed adjudications" table cites the potassium/sodium/calcium same-day and band positions directly, and the electrolyte supplemental evidence document's findings were folded into the ratified ruleset's front matter (`incorporates: HEALTHIQ-ELECTROLYTE-SUPPLEMENTAL-EVIDENCE-001 v0.1`) and adjudication register (A1-A4). The renal/electrolyte domain ruleset's own `REQUIRES_ADDITIONAL_DOMAIN_RESEARCH` verdict and its `RE-U2/U3/U4` unresolved-band items are **superseded** by this incorporation — they describe the state before the cross-domain package closed the gap, not the current state. The supplemental evidence document's own `DRAFT_FOR_HMR_REVIEW` status does not require a further, separate ratification step for this architecture task: its content is carried forward and adjudicated by the ratified ruleset and register, which are the governing documents.
3. **Six individual domain rulesets — subordinate evidentiary status.** Each domain ruleset (haematology, hepatic, renal/electrolyte, iron/inflammatory, thyroid/endocrine, cardiometabolic/nutritional) remains valuable as detailed clinical evidence, taxonomy, urgency/severity tables, combination registers and acceptance scenarios — this report continues to rely on that content directly (§6-§13 below). What must not be inherited from them is their own self-declared draft status, their "must be re-checked against v0.5" notes, or their individually-unresolved-question registers (`HEP-U1`, `RE-U2/U3/U4`, etc.) as if those were still live blockers against the later, ratified cross-domain package. **Where an individual domain ruleset conflicts with the ratified cross-domain package, the ratified package governs**, per the ruleset's own supersession instruction (ruleset front matter: "incorporates" the adjudication register and supplemental evidence; §0 "Changes from v0.4"). General reconciliation of all six domain rulesets against v0.5 is not a precondition for architecture or implementation planning to proceed — it is ordinary, expected authoring hygiene that does not block a decision already closed at the cross-domain level.

Contract §23.6 states: "No Cursor implementation prompt may be issued until: (1) independent medical validation is complete; (2) Head of Medical Research reconciliation is complete; (3) Anthony has ratified the product decisions; (4) the regulatory workstream has established any constraints material to design; (5) architecture hardening is complete; (6) the hepatic pilot has a clinically governed specification; (7) acceptance scenarios are approved; (8) the Tier 0 operational pathway is defined if Tier 0 is in implementation scope."

This is a conjunctive gate on **issuing a Cursor implementation prompt**, not a gate limited to release or activation. It contains no carve-out for bounded, fail-closed or specification-only implementation work. **This hardening pass satisfies condition (5) only, once Anthony approves this report.** Conditions (3), (4), (7) and (8) are independently open per repository and register evidence (§19) and are not resolved by architecture approval. Correcting the prior version of this report: those conditions are not merely "release/authorisation dependencies external to architecture" in the sense of not mattering to this task — §23.6 makes them literal prerequisites to Cursor prompt authoring specifically, and this report must not imply otherwise. See §19 for the full condition-by-condition status and the corrected Cursor authoring gate.

## 4. Repository-verified current state

`REPOSITORY-VERIFIED CURRENT STATE`:

- **No canonical clinical finding model exists.** `backend/core/models/insight.py` defines `Insight` (id, category, summary, evidence, confidence, severity as a free string `info|warning|critical`, recommendations, biomarkers_involved). It has no urgency/severity/tier/lead/contextual-role/provenance fields as the contract defines them, and `severity` is a narrative label, not the contract's multi-dimensional model (§4 of the contract).
- **`InsightGraphV1`** (`backend/core/contracts/insight_graph_v1.py`) is the actual sole Layer B→Layer C assembly contract (`insight_graph_builder.py:4`: "Sole assembler of InsightGraph_v1"). It carries `biomarker_nodes`, `cluster_summary`, `relationship_registry`, `precedence_output` (an `ArbitrationNode`/`PrecedenceOutput` pair), and `primary_driver_v1` — described in-code (line 282-284) as "governed lead projected onto cluster identity so Layer C renders the Layer B ranked lead instead of arbitrating its own primary driver." This is architecturally the closest existing analogue to "lead selection," but it operates on **clusters/systems**, not on the contract's **consolidated clinical finding** unit, and has no tier (0-3), no urgency time-band, no Tier 0 safety gate, and no marker-modifier/insufficient-data/indeterminate-severity states.
- **`SignalRegistry`** (`backend/core/analytics/signal_evaluator.py:26-202`) already keys signals by `activation_key` (`_signals_by_activation_key`, line 30), calls `resolve_activation_identity()` per signal (line 125), sorts deterministically (line 178, 705), and preserves multi-frame results — this is ADR-RT-002's `MULTI_FRAME_PER_DIRECTION` / `activation_key` decision **already implemented**, materially ahead of where the day-one sprint plan's "ARCH-RT-2 identity runtime pilot" framing (sprint plan §Sprint 3) suggested it stood. This is a positive repository fact the sprint plan's Sprint 3 framing should be checked against before further pipeline sequencing decisions are made — it is out of scope for this hardening pass to resolve that discrepancy, but it is material to §16 below.
- **A Pass3→package compiler exists** (`backend/scripts/compile_pass3_pilot_artifacts.py`) — explicitly non-runtime output (`knowledge_bus/generated_pilot/kb_util_2_pilot/`), emits SHA-256 source/output hashes and canonical YAML, consistent with ADR-RT-004's compile-manifest fields. It compiles individual biomarker packages, not cross-domain prioritisation rules — no compiler for consolidated findings, tiering or lead selection exists anywhere in the repository.
- **No test estate exists for clinical-concern consolidation or prioritisation.** `Glob` for `backend/tests/**/*concern*` and `**/*prioriti*` returned zero files. This is consistent with `implementation_status: NOT_AUTHORISED` — there is nothing to regress against, and nothing to accidentally break either.
- **Questionnaire gap is exactly as the audit states** (`docs/audit-papers/HEALTHIQ_UPLOAD_QUESTIONNAIRE_CONTEXT_AUDIT_v0.1.md`, confirmed by direct read of `backend/ssot/questionnaire.json`): no `pregnancy_status` question exists in the 34-question schema (confirmed — searched the full file, no pregnancy field of any kind); `biological_sex` is `required: true` in schema but the audit's cited backend behaviour (`context_factory.py` silent `Sex.OTHER` default) was not independently re-read in this pass — it is inherited from the audit as `ARTEFACT-BACKED`, not independently re-verified, because `context_factory.py` was outside the bounded discovery allowance. The governance policy file `active_signal_context_gate_reachability_policy_v1.yaml` independently confirms (lines 21-28) that `pregnancy_status` is registered as an "absent context key" with `safe_missing_states: [not_answered, not_applicable]` and `suppressive_states: [answered_yes]` — i.e. the current architecture-gate policy is fail-open on unanswered pregnancy, exactly as ratified contract §26.3 describes as the *interim defensive* state, not a target state.

`ARCHITECTURE RECOMMENDATION`: for compile purposes (§8 below), the medical authority is contract v0.6.3 + ruleset v0.5 + adjudication register v0.4 + closure report v0.4. The six domain rulesets supply detailed taxonomy, urgency/severity tables, combination registers and acceptance scenarios that the ratified package incorporates by reference and does not restate line-by-line — a compiler must therefore read the domain rulesets for that structural and evidentiary detail, while treating the ratified package as authoritative wherever the two sources differ (per §3 above). This is not a reconciliation prerequisite; it is the compiler's own source-precedence rule, analogous to how ADR-RT-001 already establishes canonical research as authoritative over package files without requiring package files to be independently "reconciled" first.

## 5. Gaps and conflicts — reclassified

Every item is classified as exactly one of: `ARCHITECTURE DECISION BLOCKER`, `IMPLEMENTATION DELIVERABLE`, `RELEASE-ONLY DEPENDENCY`, `OPEN PRODUCT / REGULATORY / LEGAL AUTHORITY`, `NON-BLOCKING REPOSITORY OBSERVATION`.

| # | Item | Classification | Basis |
|---|---|---|---|
| 1 | No canonical `ClinicalFinding` model exists yet | `IMPLEMENTATION DELIVERABLE` | The architecture decision (§6) is made and repository-grounded; building the model is ordinary implementation work that follows from an approved decision, not an open design question. |
| 2 | No concern-construction service exists yet | `IMPLEMENTATION DELIVERABLE` | Same reasoning — service boundary decided (§9), not built. |
| 3 | No Tier 0 fail-closed gate exists yet | `IMPLEMENTATION DELIVERABLE` | Mechanism decided (§10), not built. |
| 4 | No compiled prioritisation artefact/compiler/loader exists yet | `IMPLEMENTATION DELIVERABLE` | Compile/promotion design decided (§8), not built. |
| 5 | No prioritisation test estate exists (confirmed zero matches, §2 item 5) | `IMPLEMENTATION DELIVERABLE` | Validation strategy specified (§13); tests are a deliverable of implementation, not a precondition for approving the architecture that the tests will validate. |
| 6 | HEP-U1 (hepatic Tier 1 floor: literal vs magnitude-gated) | **Not a gap.** Closed by the ratified package (§3, item 2). Removed from all blocker/prerequisite lists. | Adjudication register §2 (B1), ruleset §2 (`XD-HEP-FLOOR-1`). |
| 7 | Hepatic ruleset reconciliation against v0.5/v0.6.3 text | `NON-BLOCKING REPOSITORY OBSERVATION` | Ordinary authoring hygiene (§3, item 3); the ratified package already governs any conflict, so this is not a precondition for architecture or implementation planning. |
| 8 | Supplemental electrolyte evidence still `DRAFT_FOR_HMR_REVIEW` | `NON-BLOCKING REPOSITORY OBSERVATION` | Its content is already incorporated and adjudicated in the ratified ruleset/register (§3, item 2); no further ratification step is required for this architecture task. |
| 9 | General six-domain-ruleset reconciliation to v0.5 | `NON-BLOCKING REPOSITORY OBSERVATION` | Same reasoning as #7, generalised across all six domains. Not a prerequisite to implementation planning. |
| 10 | `SignalRegistry`'s activation-key maturity is ahead of the day-one sprint plan's ARCH-RT-2 framing | `NON-BLOCKING REPOSITORY OBSERVATION` | Repository fact that may affect future pipeline sequencing; does not reopen ADR-RT-002 and does not block this architecture. |
| 11 | Tier 0 operational pathway content (R1) not defined | `OPEN PRODUCT / REGULATORY / LEGAL AUTHORITY` | Contract §17; joint clinical/product/regulatory/legal decision, architecture must remain ready to receive it (§10), not resolve it. |
| 12 | Questionnaire — no `pregnancy_status` question; no server-side enforcement | `RELEASE-ONLY DEPENDENCY` | Blocks release and runtime reliance on questionnaire context (carry-forward register `CF-QUESTIONNAIRE-CONTEXT-1/2`); does not block architecture (§11 revised below). |
| 13 | P1, P3, P4, P5, P6 (presentation/communication/sequencing) | `OPEN PRODUCT / REGULATORY / LEGAL AUTHORITY` | Ratified as open and non-blocking to clinical ruleset ratification (adjudication register §5); remain open to product/architecture until Anthony decides them, but do not block this architecture. |
| 14 | R2, R3 (CVD risk calculation, FIB-4) | `OPEN PRODUCT / REGULATORY / LEGAL AUTHORITY` | Blocking only their specific quarantined capabilities (adjudication register §7), not the wider architecture. |
| 15 | R4 (disease-name outputs) | `OPEN PRODUCT / REGULATORY / LEGAL AUTHORITY` | Open, not architecture-blocking. |
| 16 | R5, R6 (population exclusions/intended-purpose wording; renal/electrolyte release with Tier 0 suppressed) | `RELEASE-ONLY DEPENDENCY` | Explicitly blocking for release (adjudication register §7); architecture must support Tier 0 suppression cleanly (§10) but is not itself blocked. |

No item in this table is an unresolved architecture decision. Only genuine architecture-decision blockers would justify `HARDENED_WITH_BLOCKING_REPOSITORY_GAPS`; none exists here.

## 6. Target architecture — 1. Canonical clinical finding model

**ARCHITECTURE RECOMMENDATION**: introduce a new, dedicated `ClinicalFinding` Pydantic model (immutable, `frozen=True` per the repository's existing convention in `insight.py`/`insight_graph_v1.py`) and a new `ConsolidatedConcernSet` container, both under `backend/core/models/` or a new `backend/core/models/clinical_finding.py`, populated by a new **concern-construction service** (§8) that runs downstream of `SignalEvaluator` and upstream of `InsightGraphBuilder`.

**Options considered:**
- *Extend `Insight`* — rejected. `Insight` is LLM/narrative-facing (fields like `tokens_used`, `latency_ms`, free-text `severity`), not a governed clinical-priority object, and contract §3.1 explicitly prohibits reducing a finding to "a narrative section."
- *Extend `InsightGraphV1`/`primary_driver_v1`* — rejected. `primary_driver_v1` operates on **cluster/system identity** ("primary_driver_system_id", "supporting_systems"), which is exactly one of the units contract §3.1 prohibits ("a phenotype label," "a system-level" construct standing in for a finding). Contract §14 requires phenotype/system outputs to *map onto* the same tier framework as direct findings, not to *be* the findings.
- *New dedicated model* — accepted. Only this avoids collapsing the finding unit into an existing structure that already has a different, narrower job.

**Consequences**: `InsightGraphV1` will need a new field (e.g. `clinical_concern_set: Optional[ConsolidatedConcernSet]`) once implementation is authorised, additive and optional so existing consumers are unaffected until the feature is wired in.

**Unresolved dependency**: none clinical — this is a structural/ownership decision, not a threshold decision.

**ADR required**: **Yes** — a new `ADR-RT-005` (or `ADR-CLIN-001`) is needed to make this the recorded authority boundary, analogous to how ADR-RT-001 fixed the canonical research authority.

## 7. Identity and provenance design

**ARCHITECTURE RECOMMENDATION**: extend, do not replace, the ADR-RT-002/ADR-RT-004 identity chain.

- Stable semantic identity: `finding_id` = deterministic hash or composed key over `(domain, finding_type, sorted constituent activation_keys)` — never over raw values, so identical clinical facts always produce the same `finding_id` across regeneration (contract requires deterministic finding identity, §3 of this report's required-decision list).
- Build/provenance identity: `compile_run_id`, `source_document`, `source_hash`, `compiler_version` per ADR-RT-004 §Decision 1 — reused verbatim, not reinvented.
- Runtime-instance identity: `runtime_execution_id` (already implied by existing `signal_registry_hash`/`signal_registry_version` stamping pattern visible in `InsightGraphV1`, lines 197-199) extended to the new concern-set object.
- Constituent lineage: every `ClinicalFinding` carries a `constituent_activation_keys: List[str]` (per ADR-RT-002's `activation_key` as primary registry key) plus `clinical_rule_id`, `adjudication_id` (nullable), `contract_version`, `ruleset_version` fields sourced directly from the front matter of the ratified documents read in §2 above.
- `[E]`/`[C]`/`[J]` evidence labels: carried as a `evidence_label: Optional[str]` field on the finding **and** independently on each cited rule inside a `rule_citations: List[RuleCitation]` sub-structure, so a consolidated finding built from rules of different evidence grades does not lose the distinction (this matters concretely — e.g. XD-VITD-1's `<25 nmol/L` band is `[E]`, the 25-50 band is HealthIQ policy).

**Rejected alternative**: reusing `package_id` as primary identity — ADR-RT-002 already rejected this for signals ("not stable across regeneration") and the same reasoning applies unchanged to findings built from those signals.

**ADR required**: extend ADR-RT-002/004, or fold into the new ADR-RT-005 from §6.

## 8. Compile and promotion design

**ARCHITECTURE RECOMMENDATION**: cross-domain prioritisation rules (tier thresholds, urgency bands, consolidation triggers, override register entries) should compile into a **new governed artefact class** — e.g. `compiled_prioritisation_rules.yaml` — under the existing Pass3 Promotion Protocol's "Compiled WHY / Root-Cause Target" pattern (§6.3 of that protocol), not into `signal_library.yaml`/`package_manifest.yaml`, because prioritisation rules operate **across** packages (cross-domain combination register, XD-C1–XD-C15) and are not properties of a single signal's activation logic.

**Authority for compile purposes.** The current medical authority is exclusively: contract v0.6.3, cross-domain ruleset v0.5, HMR adjudication register v0.4, and six-domain closure report v0.4. The six domain rulesets are subordinate detailed source material, not independent authority. They may supply canonical finding taxonomy, detailed rule identifiers, marker combinations, urgency and severity mechanics, acceptance scenarios and evidence annotations to the compiler **only** where that content is explicitly incorporated, preserved, adjudicated or left unchanged by the later ratified package (per §3). A domain ruleset's own draft status, its "must be re-checked against v0.5" note, or its individually-unresolved-question register (e.g. `HEP-U1`, `RE-U2/U3/U4`) is never itself compilable authority — those are closed or superseded at the cross-domain level (§3, §5) and must not re-enter the system through the compiler's input path.

**Compiler source-precedence rule (mandatory, fail-closed):**
1. The ratified cross-domain package governs. Any domain-ruleset clause it incorporates, adjudicates, preserves unchanged, or does not conflict with may compile.
2. Any domain-ruleset clause that conflicts with, has been withdrawn by, or is superseded by the ratified package must be **rejected at compile-authoring time**, not silently overridden or silently dropped — the rejection itself must be a recorded, auditable event (consistent with the "no duplicate authority" and "no silent invention" principles in the Pass3 Promotion Protocol §7.3).
3. A domain draft's unresolved-question register (open `[U]` items, `HEP-U1`-style adjudication placeholders) must never be treated as active authority or compiled as if it were a settled rule.
4. Compile manifest fields follow ADR-RT-004 §Decision 1 exactly, plus a `contract_version`/`ruleset_version`/`adjudication_register_version` triple, so a compile run is invalid if any of the four ratified documents' versions have moved since the last compile.
5. Runtime consumption: a new thin loader analogous to `SignalRegistry`, but keyed on `clinical_rule_id`, feeding the concern-construction service (§9) — never raw Markdown reads (Pass3 protocol §7.4).
6. Tier 0 rules compile into a **separate quarantined namespace** within the same artefact (see §10) rather than a separate file, so a single manifest always shows the complete rule set with explicit release-gating metadata per rule, auditable in one place.

**Rejected alternative**: folding prioritisation rules into `signal_library.yaml` per-package — rejected because it would fragment cross-domain rules across dozens of package files, defeating auditability and reintroducing exactly the "duplicate/competing authority" risk ADR-RT-001 was written to prevent.

**Implementation deliverable (not an unresolved dependency, not a gate on Package A or Cursor authoring):** produce the governed machine-readable prioritisation source/artefact from the ratified package and only those subordinate domain provisions demonstrably incorporated or preserved by it. The compiler or authoring validator must fail closed on conflicts, unresolved draft clauses, withdrawn rules and missing authority lineage. This is ordinary implementation and Knowledge Bus authoring work carried out *inside* Package A (§15) against the hepatic domain first — it is not a separate clinical reconciliation gate, and general reconciliation or re-ratification of all six domain rulesets is not a prerequisite for Package A or for Cursor prompt authoring.

**ADR required**: Yes — this is new Knowledge Bus scope not covered by ADR-RT-001 through 004. The ADR must record the source-precedence rule above.

## 9. Runtime concern-construction ownership decision

**ARCHITECTURE RECOMMENDATION**: one new backend service module (e.g. `backend/core/analytics/concern_constructor.py`), invoked between `SignalEvaluator.evaluate_all()` and `build_insight_graph_v1()`, owning all thirteen responsibilities listed in the governing prompt (finding construction through phenotype/IDL coordination) as **internal functions under one canonical entry point**, not thirteen separately-owned services — this matches the existing repository pattern where `insight_graph_builder.py` itself orchestrates many sub-builders (`confidence_builder`, `biomarker_context_builder`, `signal_interaction_builder`, etc.) under one canonical assembler, and avoids the ownership fragmentation the anti-micro-sprint rule warns against at the architecture level too.

- The frontend remains render-only. `REPOSITORY-VERIFIED CURRENT STATE`: nothing in the bounded discovery touched frontend code (out of the 25+4 files read, zero are under `frontend/`), so no current frontend violation of this boundary was verified either way in this pass — this must be checked explicitly during Stage D hardening of any future implementation prompt, not assumed clean here.
- `InsightGraphBuilder` gains one new call to the concern-constructor and stores its output in the new `clinical_concern_set` field (§6) — it does not absorb the concern-constructor's logic itself, preserving `insight_graph_builder.py`'s own stated boundary ("Layer B computes; builder translates").

**Rejected alternative**: distributing consolidation logic per-domain (a haematology consolidator, a hepatic consolidator, etc.) — rejected because cross-domain combination rules (contract §9.5, ruleset §8 shared-marker table) require a single arbiter that can see all domains' candidate findings simultaneously; per-domain services would need a second cross-domain layer anyway, which is just this same service with extra steps.

**ADR required**: Yes, as part of ADR-RT-005.

## 10. Tier 0 fail-closed architecture decision

**ARCHITECTURE RECOMMENDATION**: every Tier 0 rule carries a `release_gate_status: SPECIFICATION_ONLY | RELEASE_AUTHORISED` field, set at **compile time** from a single governed manifest field (not per-environment config, not a runtime flag), defaulting to `SPECIFICATION_ONLY`. The concern-constructor's Tier 0 evaluation path always runs (so validation/audit fixtures can prove non-reachability), but the **output-assembly** step (not the evaluation step) strips or withholds any finding whose triggering rule has `release_gate_status: SPECIFICATION_ONLY`, replacing it with the auditable withheld-statement contract §17 requires. This mirrors the existing `filter_runtime_eligible_rows()` pattern already used in `insight_graph_builder.py:239` for a different governed-exclusion purpose (governed-REJECTED frames) — the repository already has a precedent for "evaluate everything, gate at assembly" rather than "gate at evaluation," which is the safer of the two because it keeps the audit trail (a withheld Tier 0 finding is provably *evaluated and blocked*, not silently never computed).

- Activation requires a **second, independent** manifest field change (e.g. `tier0_capability_activated_by: <named authority + date>`) that cannot be set by the same compile process that emits ordinary rule updates — this must require a distinct, higher-friction promotion step so an ordinary content sprint cannot accidentally flip it.
- Partial package promotion cannot activate Tier 0: the gate field lives at the rule level inside the single compiled prioritisation artefact (§8), not at the package level, so promoting an unrelated package can never touch it.
- Validation: an acceptance fixture per Tier 0 rule proving `release_gate_status: SPECIFICATION_ONLY → withheld, auditable, not demoted` is a **mandatory** test-suite requirement before any implementation of this design is accepted (§14).

**Rejected alternative**: an environment variable or feature flag — rejected explicitly by the governing prompt and by contract §17's own language ("impossible to activate through ordinary configuration drift").

**Unresolved dependency**: contract §17's operational pathway (the actual action/timeframe/escalation content) is a joint clinical/product/regulatory/legal decision (R1) that this architecture must remain permanently ready to receive, but must not anticipate the content of.

## 11. Questionnaire dependency isolation decision — corrected, three-state framing

This section is corrected to distinguish what architecture may safely do now from what runtime may safely claim now, per the required three-state framing. The questionnaire defect is not irrelevant to runtime implementation — it is architecturally isolable, but pregnancy-sensitive behaviour cannot be treated as operationally proven until remediation lands.

### 11.1 Architecture may be built now

**ARCHITECTURE RECOMMENDATION**: the concern-constructor consumes questionnaire-derived context through the same `AnalysisContext`/`runtime_context_evaluator.py` disclosure-state pattern already in use, extended to represent every state the ratified contract requires:

- `pregnant` and `may_be_pregnant` — treated identically per contract §26.2/ruleset `XD-PREG-1` (no rule may distinguish between them);
- `not_pregnant`;
- unknown/unanswered status;
- visible, auditable out-of-scope handling for the known/possibly-known states (contract §26.2 — "silent suppression is prohibited," the withheld interpretation must be visible as withheld);
- provenance-preserving context states, so the original disclosure answer and any derived flag (e.g. a future `pregnancy_sensitive_interpretation_required` boolean) remain distinguishable in the record, consistent with §7's identity/provenance design.

This data model and branching logic can be fully designed and implemented today, independent of the questionnaire fix, because the disclosure-state values already exist end-to-end in `runtime_context_evaluator.py` and the governance policy YAML read in this pass.

### 11.2 Current runtime must not rely on pregnancy context as complete or enforced

`REPOSITORY-VERIFIED CURRENT STATE`: no canonical `pregnancy_status` question exists in `backend/ssot/questionnaire.json` (confirmed by direct read); backend questionnaire enforcement is absent (`AnalysisStartRequest.questionnaire_data` is optional; `validate_requirements` exists but is never invoked, per the questionnaire audit); the active governance policy (`active_signal_context_gate_reachability_policy_v1.yaml`, lines 21-28) treats unanswered pregnancy as `safe_missing`, i.e. unanswered pregnancy currently passes the existing signal-gate policy; and because no question exists, `answered_yes` can never actually be produced today — **the known-pregnancy path in §11.1's architecture is not operationally reachable through the canonical questionnaire.** The architecture must be built to handle `answered_yes` correctly, but no implementation or test may claim that path is exercised by real users until the question exists.

### 11.3 Release remains blocked pending questionnaire remediation

This is a `RELEASE-ONLY DEPENDENCY` (§5, item 12), not an architecture blocker. Any release decision, and any runtime reliance on pregnancy or sex context for clinically consequential behaviour, remains blocked by `CF-QUESTIONNAIRE-CONTEXT-1` and `CF-QUESTIONNAIRE-CONTEXT-2` in the carry-forward register until: the pregnancy question is added; server-side enforcement is wired in; and the interim `not_answered`-safe governance policy is revisited in light of the newly-reachable `answered_yes` path. Architecture approval of §11.1 does not authorise release, and must not be cited as evidence that pregnancy-sensitive behaviour is operationally proven.

**No fail-open behaviour is embedded as permanent policy** by this design: the `not_answered → proceed with stated assumption` behaviour is contract policy (§26.3), not an architecture-invented shortcut, and it is explicitly labelled in the contract itself as "interim... not a standing expectation."

## 12. Migration and versioning decision

**ARCHITECTURE RECOMMENDATION**: given no live users (per the governing prompt and consistent with the day-one sprint plan's stated posture of "controlled replacement, not backward-compatibility preservation"), no dual-authority coexistence period is needed. A single `clinical_prioritisation_contract_version` stamp (mirroring the existing `signal_registry_version`/`relationship_registry_version` stamping pattern already on `InsightGraphV1`) is written onto every `ConsolidatedConcernSet`. Any regeneration request against an analysis whose stored concern-set version predates the currently active compiled prioritisation artefact must re-run the concern-constructor fresh rather than reinterpret the stored result — this is a straightforward extension of the existing version-stamp pattern, not new architecture.

**Rejected alternative**: presenting old and new prioritisation outputs side-by-side during a transition window — rejected as unnecessary complexity given the "no live users" premise and the existing precedent of clean regeneration in the repository (e.g. `CF-ARCH-CONV-VERSION-1` in the carry-forward register already flags exactly this class of problem as open work for compiled/legacy authority changes generally — this hardening pass's recommendation is consistent with, not a departure from, that existing open item).

## 13. Validation strategy

Required validators/tests before any implementation is accepted, all currently absent (confirmed zero matches in bounded discovery §2 item 5):

1. Schema validation for the new compiled prioritisation artefact (extends `validate_knowledge_package.py` pattern).
2. Finding-identity determinism (identical input → identical `finding_id`).
3. Duplicate-identity rejection at compile time (mirrors `activation_key` collision detection already implemented in `signal_evaluator.py`).
4. Provenance completeness (every `ClinicalFinding` traces to `spec_id`/`activation_key`/`clinical_rule_id`/versions).
5. Same-analyte and cross-domain consolidation fixtures per acceptance scenario (ruleset §13 table — 30 scenarios already specified as governing fixtures).
6. Urgency/tier invariants (contract §18 prohibited-behaviours list — each of the 36 items needs a corresponding negative test).
7. Excluded-input invariants (confidence, frame count, supporting-marker count, panel completeness, analytical reliability must not affect tier).
8. Tier 0 non-reachability — one fixture per Tier 0 rule proving withheld-not-demoted behaviour (§10 above).
9. Questionnaire fail-closed boundary fixtures (pregnancy `answered_yes`/`not_answered` paths; malformed/missing-sex fallback).
10. Regeneration/version-isolation fixtures (§12 above).
11. Full-estate regression once any real domain content compiles.

## 14. Required ADRs

- **New ADR-RT-005** (or `ADR-CLIN-001`): canonical finding model, identity/provenance extension, concern-construction service boundary, Tier 0 fail-closed mechanism — the four decisions in §6, §7, §9, §10 belong together in one ADR because they are mutually dependent (you cannot specify identity without the model; you cannot specify the Tier 0 gate without the service boundary).
- **New ADR** for the compiled prioritisation artefact class and its Knowledge Bus promotion path (§8) — this is new Knowledge Bus scope, cleanly separable from the runtime ADR above.

## 15. Minimum safe implementation sequence — recalculated under corrected authority

**Product outcomes required**: (a) a governed, auditable place for consolidated clinical findings to exist with full provenance; (b) deterministic tiering/urgency/lead selection that matches the ratified contract; (c) Tier 0 content fully specified but provably unreachable; (d) a working hepatic pilot proving the architecture end-to-end (contract §23.6 requires "the hepatic pilot has a clinically governed specification" and "acceptance scenarios are approved" before any Cursor prompt — the hepatic Tier 1 floor is closed per §3 above, so this specification already exists at the cross-domain level and does not require a separate adjudication step).

**Anti-micro-sprint test applied**: an ADR-only, schema-only, validator-only or registry-only package is invalid per the pre-SOP workflow's anti-micro-sprint rule. No package below is split on a reopened clinical decision — HEP-U1 and domain-ruleset reconciliation are removed as split justifications per §5.

**Recommended minimum package structure (two packages):**

**Package A — Prioritisation Runtime Foundation + Hepatic Pilot** (`HIGH`/`MIXED`/`TWO_PHASE_START_FINISH`)
- *Product outcome*: a working, auditable, deterministic concern-construction pipeline proven against one real domain (hepatic), per contract §23.6.
- *Hard boundary*: none required beyond the natural one — architecture cannot be validated without at least one domain's rules running through it, and hepatic is the domain the ratified package already specifies as pilot with its Tier 1 floor closed (§3) and its own regression fixture defined (contract §19).
- *Implementation deliverables*: canonical `ClinicalFinding` model and identity (§6-§7); concern-construction service (§9); Tier 0 fail-closed gate (§10); questionnaire dependency interface per §11.1; compiled-artefact schema/compiler/loader for the hepatic domain (§8); full validator suite from §13 built against hepatic rules; hepatic acceptance scenarios from the domain ruleset §14 and contract §19.
- *Release dependencies*: none block this package's implementation; R1/R5/R6 and questionnaire remediation (§5) block *release* of any Tier 0 or pregnancy/sex-dependent behaviour this package produces, not its construction.
- *STOP gate*: Anthony's architecture approval of this report **and** satisfaction of the remaining contract §23.6 conditions (§19) — architecture approval alone does not clear this gate. No hepatic-specific clinical adjudication STOP gate applies — HEP-U1 is closed and is not one of the open §23.6 conditions.
- *Cursor authoring eligibility*: **not eligible on architecture approval alone.** Per §23.6 and §19, Cursor prompt authoring for Package A remains prohibited until conditions (3) Anthony product ratification, (4) regulatory workstream constraints, (7) approved acceptance scenarios and (8) the Tier 0 operational pathway (or an explicit scope decision excluding Tier 0 from Package A) are also closed.

**Package B — Estate-Wide Domain Rollout**
- *Product outcome*: extend the proven Package A architecture to haematology, renal/electrolyte, iron/inflammatory, thyroid/endocrine, cardiometabolic/nutritional.
- *Hard boundary (sequencing dependency, not a reopened clinical decision)*: Package B cannot start meaningfully until Package A's architecture is built and proven — this is an ordinary implementation sequencing dependency (one of the pre-SOP workflow's valid split reasons), not a wait on any domain ruleset being "reconciled" as a precondition.
- *Implementation deliverables*: compiled-artefact extensions for the remaining five domains; corresponding acceptance-scenario fixtures per domain ruleset §13/§14 tables (already available as evidentiary detail per §3, item 3).
- *Release dependencies*: same as Package A, plus R2/R3 for the specific cardiometabolic capabilities they gate (cardiovascular risk calculation, FIB-4).
- *STOP gate*: successful completion and audit of Package A, plus the same §23.6 conditions as Package A (§19) — Package B does not get a lighter gate than Package A.
- *Cursor authoring eligibility*: not eligible until Package A is complete and audited and the §23.6 conditions are closed — no domain-ruleset reconciliation gate applies, but the §23.6 gate does.

**Do not provide a sprint count beyond these two.** A separate "questionnaire fix" sprint remains explicitly out of scope (§11.3) — it is independent release-dependency carry-forward work (`CF-QUESTIONNAIRE-CONTEXT-1/2`) that neither package depends on for construction and must not be bundled in.

## 16. STOP gates encountered during this hardening pass

None triggered a full `REJECT_AND_RETURN` for this pass — all 25 mandatory files existed and were readable after the one path correction applied earlier in this engagement (the questionnaire audit file was corrected from `docs/discussion documents/` to its actual location `docs/audit-papers/`). One material discrepancy was found and is flagged for GPT/Anthony attention rather than resolved here: the day-one sprint plan (Sprint 3, "ARCH-RT-2 identity runtime pilot") describes multi-frame `activation_key` registry behaviour as a pending pilot, but `SignalRegistry` in the current repository already implements activation-key keying, deterministic multi-frame preservation and duplicate-key detection (§4 above). This does not block this hardening pass's conclusions, but it should be checked before any future pipeline-sequencing decision treats ARCH-RT-2 as not-yet-started.

## 17. Unresolved decisions (explicitly not closed here)

All eleven items from the governing prompt's "Regulatory and product boundaries" section (P1, P3, P4, P5, P6, R1, R2, R3, R4, R5, R6) remain open, classified `OPEN PRODUCT / REGULATORY / LEGAL AUTHORITY` or `RELEASE-ONLY DEPENDENCY` per §5, and are not touched by this report. Questionnaire remediation (`CF-QUESTIONNAIRE-CONTEXT-1/2`) likewise remains open as a release-only dependency per §11.3. **HEP-U1 and general domain-ruleset reconciliation are not unresolved decisions** — they are closed or non-blocking per §3 and §5, and are not carried forward here as prerequisites. **Note the distinction from §19**: several of these same open items (P1-P6 via condition 3, R1/R4/R5/R6 via condition 4, plus conditions 7 and 8) are not only release-blocking — they are also, independently, prerequisites to Cursor prompt authoring under contract §23.6, which this report's prior version incorrectly elided.

## 18. Exact next action

GPT should route this hardening report to Anthony for **architecture approval** per the verdict in §1. Architecture approval is a necessary but not sufficient step toward Cursor prompt authoring: per §19, four of the eight contract §23.6 conditions remain open independently of this report. GPT/Anthony should treat closing those four conditions as the next action after architecture approval, before any Cursor implementation prompt for Package A (§15) is authored.

## 19. Contract §23.6 condition status — Cursor prompt authoring gate

| # | §23.6 condition | Status | Evidence |
|---|---|---|---|
| 1 | Independent medical validation complete | **Satisfied** | Contract §25: "no further independent medical review is required after the v0.5 clause corrections... the core clinical model is validated." |
| 2 | HMR reconciliation complete | **Satisfied** (for the ratified package) | Closure report §5: "No clinical adjudication from this package remains open." Distinct from, and not blocked by, unreconciled domain-ruleset text (§3, §5). |
| 3 | Anthony has ratified the product decisions | **Open** | Adjudication register §5 / ruleset §11.2: P1, P3, P4, P5, P6 all listed `OPEN`. Contract §23.3's enumerated ratification items (lead-plus-tiered model, co-lead cap, tier visibility, etc.) have no recorded sign-off in any document read. |
| 4 | Regulatory workstream constraints established | **Open** | Adjudication register §7: R1, R2, R3, R4, R5, R6 all `REG_LEGAL_PENDING`. |
| 5 | Architecture hardening complete | **Pending this report's approval** | This report, once approved by Anthony. |
| 6 | Hepatic pilot has a clinically governed specification | **Satisfied at the ratified-package level** | Hepatic Tier 1 floor closed literally (§3); contract §19 regression fixture defined. Weaker than conditions 1-2 because the hepatic domain ruleset text itself remains unreconciled to v0.5 — treated here as satisfied per §3's supersession rule, but flagged as the least certain of the "satisfied" items. |
| 7 | Acceptance scenarios approved | **Open** | Ruleset §15 and domain-ruleset sign-off tables contain only unchecked (`☐`) items; no recorded approval of the acceptance-scenario matrices (ruleset §13, hepatic ruleset §14) was found in any document read. |
| 8 | Tier 0 operational pathway defined, if Tier 0 is in implementation scope | **Open** | Contract §17 pathway undefined (condition 4/R1). Tier 0 hepatic rules (e.g. Hy's law, ALT/AST ≥10× ULN) fall within Package A's hepatic-pilot representation scope (§10, §15) even though the architecture keeps them unreachable — this places Tier 0 "in implementation scope" for the purpose of this condition. |

**Four of eight conditions are open (3, 4, 7, 8), independent of architecture approval.** Per contract §23.6's literal, conjunctive wording, this prohibits Cursor prompt authoring now, regardless of Anthony approving this report's architecture verdict.

---

## CURSOR PROMPT AUTHORING GATE

```text
CURSOR PROMPT AUTHORING: PROHIBITED
Reason: architecture hardening is complete, but contract §23.6 governance prerequisites for implementation-prompt authoring remain open.
```

Remaining conditions to close before this gate can change (§19): (3) Anthony's ratification of the product decisions (P1-P6 and the contract §23.3 items); (4) regulatory workstream constraints (R1-R6, at minimum R1/R5/R6 for anything touching Tier 0 or release scope); (7) formal approval of the acceptance-scenario matrices; (8) either the contract §17 Tier 0 operational pathway, or an explicit, recorded scope decision excluding Tier 0 representation from Package A's initial implementation prompt.

Claude Code has not written, and will not write, a Cursor prompt as part of this task.
