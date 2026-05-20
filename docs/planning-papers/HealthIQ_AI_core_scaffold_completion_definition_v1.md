# HealthIQ AI — Core Scaffold Completion Definition v1

**Document ID:** `HealthIQ_AI_core_scaffold_completion_definition_v1`  
**Status:** DRAFT — pending Gate A approval  
**Controlling strategic plan:** `docs/planning-papers/HealthIQ_AI_Core_Scaffold_Completion_Sprint_Plan_FINAL.md`  
**Created by:** LC-S12B (Cursor, CONTENT sprint)  
**Date:** 2026-05-20  
**Audience:** GPT Head of Product Architecture, Claude Code audit, human product owner, future LC-S13–LC-S23B prompt authors

---

## 1. Executive statement

HealthIQ AI is **not** currently trying to launch, acquire paying users, or prove commercial readiness.

The next programme phase is **core scaffold completion**: finishing the platform machinery so future work becomes **governed intelligence ingestion** (KB-WAVE) rather than repeated scaffold repair.

The saved final roadmap (`HealthIQ_AI_Core_Scaffold_Completion_Sprint_Plan_FINAL.md`) is the controlling **strategic** plan. **This document** is the controlling **execution definition** for compressed scaffold sprints **LC-S13 through LC-S23B**. Automation Bus work packages for those sprints must cite this document alongside the strategic plan.

LC-S12A concluded the analytical engine is real and worth continuing; the gap is platform completeness (lifestyle surfacing, direction-aware scoring, KB/DTO contract, persisted replay, orchestrator maintainability, SSOT metadata), not a rebuild.

---

## 2. Definition of scaffold complete

**Scaffold complete** means HealthIQ AI has a stable, testable, governed platform that can absorb new medical intelligence safely and repeatedly.

At scaffold complete, the platform must provide:

| Capability | Meaning |
| -------- | ------- |
| Deterministic Layer B analytical engine | Scoring, signals, burden/capacity, clustering, and report assembly produce reproducible structured truth from the same inputs |
| Governed signal ingestion pathway | Signal libraries load, validate, and fire through `signal_evaluator` with lab-range and policy semantics |
| Governed root-cause / WHY ingestion pathway | Hypothesis YAML assets compile through a registration path that fails loudly on malformed metadata |
| Safe biomarker canonicalisation | Alias registry and normalisation without silent unit or identity drift |
| Governed unit handling | UK/SI and biomarker-specific conversion rules; no frontend conversion maths |
| Lab-derived reference range preservation | Scoring and signals use uploaded/lab ranges; no generic global clinical ranges as default |
| Direction-aware biomarker scoring | Policy-driven high/low/bidirectional/protective semantics — not per-biomarker hardcoded bypasses |
| Questionnaire / lifestyle propagation pathway | Structured inputs produce visible, explainable user-facing payoff where governed |
| Structured Layer B → Layer C DTO contract | Fields classified; consumer vs internal separation enforced |
| Coherent frontend surfacing of governed assets | Renderer consumes DTO truth; does not invent clinical interpretation |
| Persisted-result replay compatibility | Stored analyses remain renderable or are explicitly marked stale |
| Stale-result strategy | Policy for immutability vs regeneration and user-visible engine-version notice |
| Sentinel protection | Escaped defects and scaffold-defining behaviours promoted to deterministic guards |
| Scalable Knowledge Bus registration process | Lifecycle states, required files, coverage reporting, orphan detection (machine-enforced where specified) |
| Maintainable orchestration phases | Named phases with unchanged output fingerprints across decomposition |
| SSOT metadata completion for active signal biomarkers | Tier 1 biomarkers documented for future WHY authoring (metadata ≠ runtime interpretation unless wired) |
| Standing architecture and contributor documentation | Maps and guides reflect **actual** runtime behaviour |

Sprint acceptance is **not** this checklist alone; it requires gates, tests, audits, and evidence per sprint prompt.

---

## 3. What scaffold complete does not mean

Scaffold complete explicitly **does not** mean:

- Full WHY coverage for all signals or biomarkers
- All biomarkers fully interpreted on every panel
- All drug interactions, disease-context permutations, or medication overlays complete
- Final frontend product design or commercial UX polish
- Gemini / LLM narrative generation activated for consumer paths
- Commercial launch ready, first-user ready, or clinician-grade comprehensive coverage
- All KB-WAVE intelligence waves complete
- Medical application grade **A** (that requires KB-WAVE population on top of the scaffold)

After scaffold completion, most new work should be: **add / validate / govern intelligence assets**, not **repair machinery so assets can load**.

---

## 4. Defect classification model

Use this table before choosing sprint type or blaming “missing content.”

| Category | Meaning | Example | Correct response |
| -------- | ------- | ------- | ---------------- |
| **Scaffold defect** | Platform machinery fails or cannot carry governed intelligence | Lifestyle modifiers compute but never surface; DTO field exists but frontend never reads it | Architecture / scaffold sprint (LC-S13–LC-S23B) |
| **Missing knowledge asset** | Machinery works; governed content not yet authored | LDL signal fires but no governed WHY pack | KB-WAVE sprint |
| **Frontend presentation issue** | Governed content exists; ordering, hierarchy, or visual design poor | Lead WHY buried below generic domain card | Product/UI sprint **after** scaffold contract is stable |
| **Clinical content backlog** | Interpretation not yet authored in Knowledge Bus | Ferritin + CRP interaction pattern missing | Knowledge Bus / content sprint (KB-WAVE) |
| **Escaped defect** | Known failure reached UAT or audit without guard | ApoA1 elevated treated as cardio risk (LC-S11A) | Fix + regression + Sentinel metadata |
| **Governance gap** | Missing rule, approval, contract, or process | No persisted replay fixture strategy before render-level Sentinel | Scaffold governance sprint (e.g. LC-S20/22) |

**Rule:** Do not classify a scaffold defect as “copy fix” or a missing asset as “one-line code exception” without GPT/human authority.

---

## 5. Seven compressed scaffold sprints

Sequence (from controlling strategic plan §9):

```text
Sprint 1 — LC-S12B       — Core Scaffold Definition, Gates and Execution Governance
Sprint 2 — LC-S13        — Lifestyle Propagation, Coherence Guard and Narrative Language Audit [HIGH]
Sprint 3 — LC-S14        — Direction-Aware Scoring Framework [HIGH]
Sprint 4 — LC-S16/17/19  — Knowledge Asset Frontend Surface, KB Framework and Payload Contract [HIGH]
Sprint 5 — LC-S18        — Root Cause / WHY Registration Generalisation [HIGH]
Sprint 6 — LC-S20/22     — Persisted Replay, Stale-Result Strategy and Sentinel Phase 2 Scaffold
Sprint 7 — LC-S21/23/23B — Orchestrator Decomposition, Scaffold Documentation and SSOT Metadata [HIGH / MIXED]
```

### Sprint 1 — LC-S12B (this document)

| Field | Value |
| ----- | ----- |
| **Purpose** | Define scaffold complete, gates, risk model, and execution rules before implementation sprints |
| **Why it matters** | Prevents LC-S13+ from re-debating scope; establishes Gate A |
| **Risk** | STANDARD (CONTENT only) |
| **Key STOP conditions** | Runtime file required; duplicate final scaffold authority; primary plan missing |
| **Key output** | This document + `LC-S12B_core_scaffold_definition_notes.md` |
| **Sentinel / tests** | Not required (no behaviour change) |
| **Dependency** | `HealthIQ_AI_Core_Scaffold_Completion_Sprint_Plan_FINAL.md` |

### Sprint 2 — LC-S13

| Field | Value |
| ----- | ----- |
| **Purpose** | Prove questionnaire/lifestyle intelligence surfaces with coherence and honest narrative language |
| **Why it matters** | LC-S12A: lifestyle computes internally but user sees little payoff |
| **Risk** | **HIGH** — backend lifestyle/DTO/frontend/Sentinel expected |
| **Key STOP conditions** | Modifiers never compute non-zero output → split LC-S13A/B; Q-1/Q-2 questionnaire shape unstable |
| **Key output** | Wired lifestyle surfaces; coherence guards; narrative language audit |
| **Sentinel / tests** | Required: `lifestyle_visible_payoff_missing`, `domain_band_headline_polarity_contradiction`, `mock_mode_personalisation_overclaim`, etc. |
| **Dependency** | **Gate A** — LC-S12B approved |

### Sprint 3 — LC-S14

| Field | Value |
| ----- | ----- |
| **Purpose** | General direction-aware scoring policy (replace biomarker-specific bypasses) |
| **Why it matters** | LC-S11A ALT fix is targeted; asymmetric markers remain at risk |
| **Risk** | **HIGH** — `backend/core/scoring/`, policy/SSOT |
| **Key STOP conditions** | Requires global enzyme rescoring redesign without policy model; weakens high-ALT concern |
| **Key output** | Governed directionality in policy/SSOT; representative marker tests |
| **Sentinel / tests** | Required: `low_enzyme_false_alarm`, `protective_high_marker_penalised`, `hardcoded_biomarker_scoring_exception`, etc. |
| **Dependency** | Prior scaffold smoke pack green |

### Sprint 4 — LC-S16/17/19

| Field | Value |
| ----- | ----- |
| **Purpose** | Map visible UI to sources; formalise KB lifecycle; harden DTO contract without breaking consumers |
| **Why it matters** | Unknown fallback vs governed asset mix; internal field leakage; KB scale needs registration framework |
| **Risk** | **HIGH** — DTO, frontend consumers, KB surfacing |
| **Key STOP conditions** | **Gate B** — frontend-surface audit must complete before KB framework / DTO implementation; material rescoping → GPT/human |
| **Key output** | `LC-S16_knowledge_asset_frontend_surface_audit.md`; lifecycle rules; field classification |
| **Sentinel / tests** | Required: `consumer_payload_internal_field_leakage`, `generic_fallback_used_when_governed_asset_exists`, etc. |
| **Dependency** | Gate A; prior guards green |

### Sprint 5 — LC-S18

| Field | Value |
| ----- | ----- |
| **Purpose** | Metadata-driven WHY registration; reduce manual `_ROOT_CAUSE_TARGETS` wiring |
| **Why it matters** | Manual registration does not scale to hundreds of packages |
| **Risk** | **HIGH** — root-cause compiler behaviour |
| **Key STOP conditions** | GPT + Claude review before migration; silent skip forbidden; fingerprint mismatch after migration |
| **Key output** | Registration mechanism + identical output proof for all pre-existing targets |
| **Sentinel / tests** | Required: `why_asset_silent_skip`, `why_output_changed_after_registration_migration`, etc. |
| **Dependency** | Prior guards green |

### Sprint 6 — LC-S20/22

| Field | Value |
| ----- | ----- |
| **Purpose** | Real persisted replay; stale-result policy; Sentinel Phase 2 render/contract smoke |
| **Why it matters** | Placeholder replay; human UAT still catches page-level defects |
| **Risk** | **HIGH** if API/frontend/Sentinel/persisted DTO touched |
| **Key STOP conditions** | **Gate C** — fixture contract before finalising render-level Sentinel |
| **Key output** | Replay fixture strategy; stale marking; Sentinel Phase 2 pack entries |
| **Sentinel / tests** | Required: `persisted_result_render_failure`, `results_page_placeholder_text_visible`, etc. |
| **Dependency** | Gate A; prior guards green |

### Sprint 7 — LC-S21/23/23B

| Field | Value |
| ----- | ----- |
| **Purpose** | Orchestrator phase decomposition; standing contributor docs; Tier 1 SSOT metadata |
| **Why it matters** | 2,300+ line orchestrator; authors need maps; KB-WAVE needs biomarker metadata |
| **Risk** | **HIGH / MIXED** — pipeline decomposition is BEHAVIOUR; docs/metadata may be CONTENT |
| **Key STOP conditions** | Scope A blocked → GPT decides split for B/C; no output fingerprint drift without justification |
| **Key output** | Phase modules; architecture map; how-to guides; Tier 1 SSOT fields |
| **Sentinel / tests** | Required for decomposition: `orchestrator_phase_output_changed`; SSOT validators for Tier 1 |
| **Dependency** | Gate A; prior guards green |

This document is **not** the sprint-by-sprint Cursor prompt library. Each sprint requires its own Automation Bus work package.

---

## 6. Gate model

### Gate A — LC-S12B approval gate (mandatory)

**LC-S13 and all later scaffold sprints must not start** until this document (`HealthIQ_AI_core_scaffold_completion_definition_v1.md`) is:

1. Reviewed by GPT Head of Product Architecture  
2. Audited by Claude Code  
3. Approved by human product owner  

Approval status must be recorded (e.g. in `LC-S12B_core_scaffold_definition_notes.md` or programme ledger) before LC-S13 prompt authoring or kernel start.

### Gate B — Sprint 4 audit-before-implementation gate

Sprint 4 (LC-S16/17/19) must **complete and review** the Knowledge Asset Frontend-Surface Audit (`LC-S16_knowledge_asset_frontend_surface_audit.md`) **before** implementing or finalising Knowledge Bus framework and payload-contract hardening.

If the audit materially changes understanding of visible, governed, fallback-backed, or unsupported content → **STOP** → GPT/human amended scope.

### Gate C — Sprint 6 persisted replay fixture gate

Sprint 6 must establish a **concrete persisted replay fixture strategy** before finalising Sentinel Phase 2 render-level checks.

If no fixture contract can be established → Sentinel Phase 2 scope must be revised by GPT/human before implementation continues.

### Gate D — Cross-sprint guard gate

Every scaffold sprint after LC-S12B must begin by running the **current scaffold smoke / regression pack**.

If prior scaffold guards fail → **STOP** unless GPT explicitly classifies the failure as unrelated and authorises continuation.

---

## 7. Global STOP conditions

All scaffold sprints share these STOP triggers (non-exhaustive; sprint prompts may add specifics):

- Work package token missing or `work_id` / branch mismatch  
- Wrong branch or dirty branch ambiguity (unrelated uncommitted work)  
- Duplicate or competing “final” scaffold authority without resolution  
- Runtime / test / Sentinel / KB / control-plane change required in a **CONTENT-only** sprint  
- Risk level escalation needed (e.g. touching `backend/core/analytics/`, `pipeline/`, `scoring/`, `dto/`, `ssot/`, Sentinel, frontend results without HIGH controls)  
- Required source document missing  
- Frontend contract change discovered but not authorised in prompt  
- DTO field rename/removal required but not scoped with consumer update  
- Sentinel obligation identified but not implemented  
- Material rescoping required (Cursor must not self-rescope)  
- Prior scaffold regression failing (Gate D)  
- Scope drifts into launch, commercial readiness, or product redesign  

---

## 8. Cross-sprint regression policy

**Policy:** Run prior scaffold regression and Sentinel guards **before** new implementation in each sprint.

The smoke pack **grows** as sprints add protections. Initial minimum categories:

| Guard family | Source |
| ------------ | ------ |
| Unit / display fidelity | LC-S8F, LC-S8G |
| Launch-core slice protection | LC-S10B |
| Trust blockers | LC-S11A |
| Lifestyle / coherence | LC-S13 (once created) |
| Direction-aware scoring | LC-S14 (once created) |
| DTO / KB surfacing | LC-S16/17/19 (once created) |
| WHY registration | LC-S18 (once created) |
| Persisted replay / render | LC-S20/22 (once created) |
| Orchestrator / docs / SSOT | LC-S21/23/23B (once created) |

No sprint may silently break a prior guard. Failing guards block progress unless GPT documents an unrelated classification.

---

## 9. Sentinel / test-harness policy

Every scaffold sprint prompt must include a section:

```text
Sentinel / test harness obligations
```

It must state either:

```text
Sentinel update required
```

or:

```text
Sentinel update not required because...
```

**Sentinel is required** when a defect class is:

- User-facing  
- Previously escaped (UAT/audit)  
- Likely to recur or cross-layer  
- Clinically trust-sensitive  
- Unit / display / reference-range safety  
- Internal token or placeholder leakage  
- DTO compatibility or persisted replay  
- Knowledge Bus asset surfacing  

**Rule:** A known escaped-defect class must not be fixed without a regression test and, where applicable, Sentinel pack metadata pointing to that test.

Render-level checks may be deferred only with documented limitation and Gate C satisfaction for persisted fixtures.

---

## 10. Risk classification model

| Sprint | Default risk | Reason |
| ------ | ------------ | ------ |
| LC-S12B | STANDARD | CONTENT planning documents only |
| LC-S13 | HIGH | Lifestyle, DTO/frontend surfacing, Sentinel |
| LC-S14 | HIGH | Scoring policy / engine behaviour |
| LC-S16/17/19 | HIGH | DTO, frontend, KB contract |
| LC-S18 | HIGH | Root-cause registration mechanism |
| LC-S20/22 | HIGH when API/frontend/Sentinel/persisted DTO touched | Replay + render protection |
| LC-S21/23/23B | HIGH / MIXED | Pipeline decomposition (HIGH) plus docs/SSOT (CONTENT) |

**Escalation rule:** If a sprint touches `backend/core/analytics/`, `backend/core/pipeline/`, `backend/core/scoring/`, `backend/core/dto/`, `backend/ssot/`, Sentinel packs, or frontend result rendering, apply **Automation Bus SOP v1.3.1 HIGH-risk controls** unless GPT/human explicitly justifies otherwise in the hardened prompt.

MIXED sprints use **BEHAVIOUR** controls for the whole package unless explicitly split.

---

## 11. Knowledge Bus lifecycle expectations

Required lifecycle states (Sprint 4 must machine-enforce or backlog explicitly):

| State | Meaning |
| ----- | ------- |
| **draft** | Authoring in progress; not runtime-loaded |
| **validated** | Passes package validators |
| **runtime-loaded** | Signal library consumed by evaluator |
| **signal-only** | Fires signals; no WHY pack |
| **WHY-enabled** | Root-cause hypotheses present and registered |
| **frontend-surfaced** | Traceable to a visible frontend section via DTO |
| **Sentinel-protected** | Defect class guarded in Sentinel + regression |

Sprint 4 must classify each control as:

```text
machine-enforced now
documented now, machine-enforced later
advisory only
```

Minimum machine-enforced or validator-backlog targets:

- Orphaned package detection  
- Package lifecycle state validity  
- Required file presence for WHY-enabled packages  
- Signal library schema validity  
- Root-cause hypothesis metadata validity  
- Asset coverage reporting for active signals  

Documentation-only rules must be labelled and must not be treated as gates.

---

## 12. DTO / Layer B → Layer C contract principles

1. **Frontend is renderer, not analyst** — no clinical inference in UI code.  
2. **Layer B carries structured truth** — scores, signals, IDL selections, root cause, domain rows.  
3. **Layer C may polish presentation** — must not invent unsupported interpretation or pattern labels without active signals.  
4. **DTO field classification is governance work** — analytical truth vs display metadata vs internal-only vs legacy compatibility.  
5. **No casual rename/restructure/removal** of fields consumed by `frontend/`.  
6. **Any DTO shape change** requires: frontend consumer search, TypeScript update, runtime rendering check, regression test, stale-result compatibility assessment.  
7. **Internal sprint strings, raw `signal_*` ids, and debug slugs** must not appear in consumer JSON or user-visible prose.

---

## 13. Documentation standing obligation

Documentation produced during scaffold completion becomes **standing documentation**.

Every future **KB-WAVE** sprint must update documentation when it introduces or changes:

- Combination-case patterns  
- Modifier classes  
- Medication overlay patterns (post scaffold)  
- WHY registration patterns  
- DTO field categories  
- Sentinel requirements  
- Knowledge Bus lifecycle patterns  
- Frontend surfacing patterns  

Docs must track **actual runtime behaviour**, not historical scaffold snapshots.

---

## 14. Transition criteria into KB-WAVE phase

Systematic KB-WAVE intelligence expansion must not begin until:

| Criterion | Required state |
| --------- | -------------- |
| Gate A | LC-S12B approved (this document) |
| LC-S13 | Completed or split/closed with lifestyle payoff proven or explicitly deferred with mitigation |
| LC-S14 | Direction-aware scoring complete |
| LC-S16/17/19 | Frontend-surface audit + KB/DTO contract complete |
| LC-S18 | WHY registration generalisation complete or deferred with mitigation |
| LC-S20/22 | Persisted replay + Sentinel Phase 2 scaffold complete |
| LC-S21/23/23B | Complete or split/closed |
| SSOT | Tier 1 metadata complete for active signal biomarkers |
| Guards | Scaffold smoke pack green |
| Docs | Standing contributor guides available |

Then proceed to KB-WAVE-1+ (lipid, thyroid, iron/inflammation, renal, cortisol, CK, medication overlays, sex hormones, liver patterns, etc.) per strategic plan §8.

**Medication modifier pathway** remains **out of scaffold phase** until lifestyle propagation pattern is proven (KB-WAVE-7).

---

## 15. Expected grade after scaffold completion

```text
Scaffold architecture grade target: A−
Medical application grade target: B+
```

Clarifications:

- Grades are **strategic shorthand**, not Automation Bus pass/fail.  
- Sprint acceptance uses tests, gates, audits, and evidence.  
- Medical application grade **A** requires KB-WAVE population of governed intelligence on the completed scaffold.

**Phase model:**

```text
Phase 1: Build an A− scaffold.
Phase 2: Use that scaffold to build an A− medical intelligence platform (KB-WAVE).
```

---

## Document control

| Version | Date | Change |
| ------- | ---- | ------ |
| v1.0 | 2026-05-20 | Initial LC-S12B draft from FINAL compressed plan + LC-S12A audit |

**Supersedes:** No prior `core_scaffold_completion_definition` document.  
**Does not supersede:** `HealthIQ_AI_Core_Scaffold_Completion_Sprint_Plan_FINAL.md` (strategic plan remains co-authority).
