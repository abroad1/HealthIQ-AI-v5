# HealthIQ AI — Sprint Governance Discovery and Codebase Maturity Audit

| Field | Value |
|---|---|
| **Audit date** | 2026-07-25 |
| **Auditor identity** | Cursor — independent repository reality and runtime wiring auditor |
| **Repository root** | `C:\Users\abroa\HealthIQ-AI-v5` |
| **Branch** | `main` |
| **HEAD SHA** | `2a8fa64ed791cabc8ae478113b96cefdf25145a1` |
| **Working tree** | CLEAN (no staged/unstaged/untracked porcelain at audit time) |
| **HEAD subject** | `Update MR-BATCH-001B benchmark carry-forward status` |
| **Mode** | Read-only inspection; this report is the only intended write |

Evidence labels used below:

- **VERIFIED_FACT** — observed in repository files, imports, indexes, tests, or git state during this audit
- **REASONABLE_INFERENCE** — supported by multiple artefacts but not exhaustively proven end-to-end
- **UNVERIFIED_CLAIM** — stated in documents without confirming code/runtime evidence in this audit
- **UNKNOWN_REQUIRES_REVIEW** — evidence insufficient or conflicting

---

## 1. Executive verdict

HealthIQ AI has a **usable governance stack** and a **materially advanced day-one / Wave 1 runtime path**, but **document authority is not clean**, and **controlled beta is not yet justified**.

**VERIFIED_FACT:** Six Wave 1 consumer domains (`wave1_cardiovascular`, `wave1_blood_sugar`, `wave1_liver`, `wave1_kidney`, `wave1_blood_iron_oxygen`, `wave1_thyroid`) are assembled from compiled card evidence with empty legacy hard-coded subsystem lists (`knowledge_bus/compiled/estate_index_v1.yaml`; `backend/core/analytics/wave1_subsystem_evidence.py`). This **supersedes** the 2026-06-20 strategy claim that three launch-core domains were still missing.

**VERIFIED_FACT:** PSI (`load_promoted_signal_intelligence`) is intentionally **not** on the launch analysis path; production imports are forbidden by day-one validators/tests. Root-cause WHY remains a **dual path**: one compiled hypothesis (`signal_vitamin_d_low`) plus ~40 legacy YAML targets. Deterministic Layer B narrative exists with Gemini narrative **deny-default**. Retail explainers cover **40** biomarkers in SSOT registry.

**VERIFIED_FACT:** MR-BATCH-001B is present as a **69-asset CANDIDATE pack** under sprint docs, loaded only by a test support module requiring `candidate_test_mode=True`, with tests asserting non-import by orchestrator/retail assembly. **No APPROVED assets.** Classification as Round 1 benchmark / test fixture / not-for-promotion is **supported by current code and the latest BUILD register entry**, with one important documentation contradiction (older completion/output docs still recommend medical review).

**Highest-priority governance finding:** unresolved **authority conflicts** require Head of Architecture adjudication before the next implementation sprint is selected — especially Knowledge Bus SOP `v1.3` vs `v1.3.1`, stale `docs/AUTHORITY_MAP.md` / `docs/SPRINT_STATUS.md`, Pass 3 protocol still marked DRAFT while used as companion, and MR-BATCH medical-review guidance conflict between completion artefacts and the updated BUILD register.

**Immediate next action (governance, not implementation):** adjudicate and refresh the authoritative document stack, then treat `SPRINT-BUILD-PLAN-AUDIT-1` (already recommended by the BUILD register) as the planning gate — not as a code sprint.

---

## 2. Audit scope and method

### In scope

- Governance, planning, sprint-state, audit, closure, and continuity documents
- Automation Bus / Knowledge Bus operational state and mechanical enforcement gaps
- Day-one research-to-runtime architecture wiring
- Eight-block beta-readiness maturity vs repository evidence
- Layer B prose / reasoning and Layer C / Gemini / frontend boundary
- Recent sprint verification and MR-BATCH-001B classification
- Dead artefacts, stale recommendations, and doc-vs-code mismatches

### Out of scope (per assignment)

- Choosing the next sprint
- Writing an implementation prompt
- Modifying runtime code, schemas, tests, packages, governance files, or sprint state
- Merging, committing, or changing branches
- Inferring completion from titles/status labels alone

### Method

1. Branch / HEAD / working-tree inspection
2. Governance document discovery and classification (Phase 1 completed before Phase 2 maturity claims)
3. Import/loader/consumer tracing for runtime wiring
4. Estate index / manifest path resolution checks
5. Test and fixture location checks (especially MR-BATCH-001B)
6. Cross-check of strategy/build-register claims against code

This audit did **not** execute the full golden gate or full pytest suite; gate evidence cited is from existing artefacts and static wiring inspection.

---

## 3. Repository and branch state

| Item | Evidence | Label |
|---|---|---|
| Branch | `main` | VERIFIED_FACT |
| HEAD | `2a8fa64ed791cabc8ae478113b96cefdf25145a1` | VERIFIED_FACT |
| Working tree | `git status --porcelain` empty | VERIFIED_FACT |
| Recent merges | MR-BATCH-001B test import merge `8744b09`; build-register session update `c465de2`; P3-PROSE-DEPTH-1 merge `df56a35`; P2-4 merge `8aea163` | VERIFIED_FACT |
| Active WP token | `automation_bus/state/` empty; no `work_package_active.json` | VERIFIED_FACT |
| Local Cursor status | `automation_bus/latest_cursor_status.json` shows `P3-PROSE-DEPTH-1` COMPLETE on branch `feature/p3-prose-depth-1-...`, `bus_version: "1.2"`, older SHA | VERIFIED_FACT — **stale vs HEAD** |
| Knowledge status path | `knowledge_bus/current/latest_knowledge_status.json` **absent** | VERIFIED_FACT |
| `automation_bus/` | Present locally; listed in `.gitignore` as operational cache | VERIFIED_FACT |
| Package count | 192 package directories under `knowledge_bus/packages/` | VERIFIED_FACT |
| Compiled cards | 10 estate-indexed cards; 11 YAML files on disk under `health_system_cards/` | VERIFIED_FACT |
| Compiled hypotheses | 1 (`signal_vitamin_d_low`) | VERIFIED_FACT |
| PSI YAML on disk | 57 `promoted_signal_intelligence.yaml` under packages | VERIFIED_FACT — presence ≠ runtime consumption |
| Local `.env` / `old.env(copy)` | Exist on disk; **not** git-tracked; `.env` gitignored | VERIFIED_FACT — history purge / secret rotation **UNKNOWN_REQUIRES_REVIEW** |

---

## 4. Authoritative governance document map

### 4.1 Authoritative current governance stack (auditor recommendation)

These are the documents that **should** govern future sprint planning **after** conflict adjudication. Classification reflects current operational use plus stated headers, not title optimism.

| Document | Path | Stated status | Classification | Govern future planning? | Confidence |
|---|---|---|---|---|---|
| Agent operating map | `AGENTS.md` | Operating roles | AUTHORITATIVE_CURRENT | Yes (agent scope) | HIGH |
| Permanent ops context | `.claude/CLAUDE.md` | Permanent context | AUTHORITATIVE_CURRENT | Yes | HIGH |
| Automation Bus SOP | `docs/governance/AUTOMATION_BUS_SOP_v1.3.1.md` | LOCKED; supersedes v1.3 | AUTHORITATIVE_CURRENT | Yes | HIGH |
| Knowledge Bus SOP | `docs/governance/KNOWLEDGE_BUS_SOP_v1.3.1.md` | APPROVED FOR USE (WITH KNOWN CONSTRAINTS) | AUTHORITATIVE_CURRENT | Yes | HIGH |
| Pass 3 promotion protocol | `docs/governance/KNOWLEDGE_BUS_PASS3_PROMOTION_PROTOCOL_v1.1.md` | DRAFT FOR GOVERNANCE REVIEW | AUTHORITATIVE_CURRENT *(operative companion; draft status unresolved)* | Yes, with caveat | MEDIUM |
| Pre-SOP scoping workflow | `docs/governance/healthiq_pre_sop_prompt_scoping_workflow_v0_6.2.md` | ACTIVE | AUTHORITATIVE_CURRENT | Yes (Stage 0) | HIGH |
| Cursor operating policy | `docs/governance/CURSOR_OPERATING_POLICY.md` | Policy | AUTHORITATIVE_CURRENT | Yes | HIGH |
| Document authority map | `docs/AUTHORITY_MAP.md` | LIVE 2026-06-20 | AUTHORITATIVE_CURRENT *(map itself is stale in places)* | Yes after refresh | MEDIUM |
| Layer boundary ADR | `docs/architecture/ADR-LAYER-BOUNDARY-RECONCILIATION-1.md` | AUTHORITATIVE per map | AUTHORITATIVE_CURRENT | Yes | HIGH |
| ADR-RT-001..004 | `docs/architecture/ADR-RT-00*.md` | ACCEPTED 2026-05-28 | AUTHORITATIVE_CURRENT | Yes (day-one architecture) | HIGH |
| Classic ADRs 001–003,005,007–009 | `architecture/ADR-*.md` | Indexed / authoritative | AUTHORITATIVE_CURRENT | Yes | HIGH |

### 4.2 Current planning and build-register stack

| Document | Path | Classification | Govern future planning? | Confidence |
|---|---|---|---|---|
| Beta strategy FINAL | `docs/strategy/beta_readiness/HEALTHIQ_AI_BETA_READINESS_DEFINITIVE_STRATEGY_FINAL_2026-06-20.md` | AUTHORITATIVE_CURRENT for programme structure; **maturity snapshot partially STALE** | Yes for blocks/rules; **not** for Block 1 “missing domains” claim | HIGH structure / MEDIUM currency |
| Build deliverable register | `docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md` | CURRENT_BUT_LIGHTWEIGHT_CONTINUITY_ONLY | Yes for continuity; not substitute for audits/ADRs | HIGH |
| Day-one plan (updated) | `docs/sprints/healthiq_day_one_architecture_rework_sprint_plan_FINAL_updated.md` | AUTHORITATIVE_CURRENT for day-one carry-forward | Yes for architecture CF | MEDIUM |
| Local automation_bus latest_* | `automation_bus/latest_*.json|md|txt` | CURRENT_BUT_LIGHTWEIGHT_CONTINUITY_ONLY (gitignored ops cache) | Context only; stale relative to HEAD | MEDIUM |

### 4.3 What currently references the stack

- `.claude/CLAUDE.md` and `.cursor/rules/healthiq-knowledge-bus-medical-intelligence.mdc` → KB SOP **v1.3.1** + Pass3 **v1.1**
- `docs/AUTHORITY_MAP.md` → KB SOP **v1.3** (conflict) and pre-SOP **v0.4** (stale citation)
- `AGENTS.md` → Full Automation Bus SOP for core/KB work
- BUILD register → latest recommended next: `SPRINT-BUILD-PLAN-AUDIT-1`

---

## 5. Legacy, superseded and unresolved documents

### 5.1 Legacy / superseded (must not drive new sprint decisions)

| Item | Path | Notes |
|---|---|---|
| Automation Bus SOP older | `docs/archive/superseded/AUTOMATION_BUS_SOP_v1.3.md`, `v1.2.md`; `docs/archive/working-papers/download-arch/AUTOMATION_BUS_SOP_*` | Archive / drafts |
| Knowledge Bus SOP v1.2 | `docs/archive/superseded/KNOWLEDGE_BUS_SOP_v1.2.md` | Banner path stale |
| Pass3 protocol v1.0 | `docs/governance/KNOWLEDGE_BUS_PASS3_PROMOTION_PROTOCOL_v1.0.md` | Superseded by presence of v1.1 |
| Pre-SOP ≤ v0.6.1 / discussion drafts | `docs/governance/...v0_6.1.md`; `docs/discussion documents/healthiq_pre_sop_*` | Superseded / discussion |
| Day-one plan without `_updated` | `docs/sprints/healthiq_day_one_architecture_rework_sprint_plan_FINAL.md` | Prefer `_updated` |
| Sprint status register | `docs/SPRINT_STATUS.md` (2026-05-04) | Claims LIVE; **stale** vs beta programme |
| `docs/README.md` | Still points readers toward old sprint-status era | Partially stale navigation |
| Strategy working papers / eight-block pre-FINAL | `docs/strategy/beta_readiness/working_papers/`; `docs/strategy/eight_block_beta_readiness/` | Archaeology |
| Transition plans v1–v3 | `docs/planning-papers/HealthIQ_As-Is_to_Day-One_*` | Supporting history |

### 5.2 Unresolved authority conflicts (Head of Architecture adjudication required)

| Conflict ID | Description | Evidence |
|---|---|---|
| AUTH-01 | KB SOP: CLAUDE/rules cite **v1.3.1**; AUTHORITY_MAP lists **v1.3** as AUTHORITATIVE; both files live under `docs/governance/` | Dual files + map |
| AUTH-02 | Pass 3 protocol **v1.1** is companion to live SOP but header remains **DRAFT FOR GOVERNANCE REVIEW**; companion line still cites KB SOP v1.3 | Protocol header |
| AUTH-03 | Pre-SOP: live **v0.6.2** vs AUTHORITY_MAP citing discussion **v0.4** | Map vs governance tree |
| AUTH-04 | Sprint continuity: BUILD register vs `docs/SPRINT_STATUS.md` both behaving as “current” in docs navigation | Dates 2026-06-30 vs 2026-05-04 |
| AUTH-05 | Day-one FINAL vs FINAL_updated | Parallel FINAL artefacts |
| AUTH-06 | MR-BATCH medical review: BUILD register (HEAD) says **must not** proceed to medical review/promotion; `MR-BATCH-001B_test_import_completion.md` §11 and `MR-BATCH-001B_candidate_prose_test_output.md` still recommend medical review | Doc conflict |
| AUTH-07 | Strategy Block 1 maturity still says three domains missing; code + estate index show six domains wired | Strategy §8.1 vs `wave1_subsystem_evidence.py` / estate index |
| AUTH-08 | `architecture/ARCHITECTURE_INDEX.md` incomplete vs ADR-RT-* and later ADRs (per discovery) | Index lag — UNKNOWN_REQUIRES_REVIEW for full ADR coverage |

---

## 6. Current sprint-state and closure evidence

### 6.1 Continuity (not ongoing specification authority)

| Artefact | State | Classification |
|---|---|---|
| `BUILD_DELIVERABLE_REGISTER.md` | Latest closed entry **MR-BATCH-001B** (2026-06-30); next recommended `SPRINT-BUILD-PLAN-AUDIT-1` | CURRENT_BUT_LIGHTWEIGHT_CONTINUITY_ONLY |
| `automation_bus/latest_cursor_status.json` | COMPLETE P3-PROSE-DEPTH-1; **does not reflect** later MR-BATCH-001B / register commits on `main` | STALE operational cache |
| `automation_bus/latest_gate_evidence.json` / `latest_gate_output.txt` | P3-PROSE-DEPTH-1 PASS (local, gitignored) | FORMAL_AUDIT_OR_CLOSURE_EVIDENCE (local) |
| `automation_bus/latest_audit_summary.md` | P3-PROSE-DEPTH-1 MERGE | FORMAL_AUDIT_OR_CLOSURE_EVIDENCE (local) |
| `automation_bus/latest_pipeline_advisory.md` | Dated around P2-era advisory; partially stale vs P2-4/P3/MR-BATCH | CURRENT_BUT_LIGHTWEIGHT_CONTINUITY_ONLY / STALE |
| Active work package | None | VERIFIED_FACT |

### 6.2 Formal audit / closure evidence (proves past outcomes only)

Representative high-signal papers under `docs/audit-papers/` (175+ files). These are **not** ongoing governance specs:

- Day-one: `ARCH-RT-6_day_one_architecture_acceptance_audit.md`, `DAY-ONE-ARCHITECTURE-CLOSURE-REVIEW.md`, `day_one_architecture_launch_readiness_audit.md`
- Launch/beta gates: `WAVE1-LAUNCH-READINESS-1_...`, `BETA-READINESS-RECHECK-1_...`, `BETA-READINESS-SPRINT-2_...`
- Architecture completion: `ARCH-COMPLETION-1/2/3_...`
- Programme consolidation: `PROGRAMME-STATUS-1_...` (2026-05-31 — partially superseded by later P1 domain work)
- Prose inventory: `PROSE-INVENTORY-1_...`
- Pass3 / Batch2 / Context series: numerous `PASS3-*`, `BATCH2-*`, `CONTEXT-*` papers

### 6.3 Sprint-specific context packs

Under `docs/sprints/beta_readiness/`: P1-1..P1-26 packs/manifests/carry-forwards; P2-1..P2-4; P3-PROSE-DEPTH-1*; MR-BATCH-001B*. Classification: **SPRINT_SPECIFIC_CONTEXT** / closure evidence for those work IDs.

---

## 7. Current maturity by programme block

Baseline claims from strategy FINAL §8–9 (2026-06-20) compared to repository evidence on 2026-07-25.

### Block 1 — Core systems

| Aspect | Detail |
|---|---|
| Claimed (strategy) | Medium; three of six launch-core domains missing |
| Actual evidence | Six domains in `WAVE1_DOMAIN_IDS`; kidney / blood-iron-oxygen / thyroid assemblers in `domain_score_assembler.py`; compiled cards for renal, bio-oxygen, thyroid in estate index |
| Maturity verdict | **BUILT_AND_MERGED + RUNTIME_WIRED** for domain card surfaces; depth/scoring completeness still uneven (thyroid history of scoring-rail constraints; antibody deferrals) |
| Gaps | Domain **presence** ≠ equal clinical depth; strategy snapshot **STALE** |
| Beta blockers | Not the “three missing domains” claim anymore; remaining depth/scoring/activation hygiene |
| Stale recommendations | Strategy §8.1 “map and complete missing domains” as primary Block 1 action |

### Block 2 — Subsystems

| Aspect | Detail |
|---|---|
| Claimed | Low–Medium / Medium; uneven depth |
| Evidence | 10 compiled subsystem cards; `wave1_subsystems_legacy_hard_coded: []`; assembler “no hard-coded fallback” |
| Verdict | **RUNTIME_WIRED** compiled-card path; medical visibility-tier policy enforcement still weak historically (PROGRAMME-STATUS-1); PSI richness **not** consumed |
| Gaps | Pass 3 hypothesis/contradiction richness stranded; thin subsystems may still over-present |
| Beta blockers | Medical model vs card presentation alignment |

### Block 3 — Layer B intelligence / prose / clinician report

| Aspect | Detail |
|---|---|
| Claimed | Medium; prose incomplete |
| Evidence | Clinician report compile path via `report_compiler_v1` → `compile_root_cause_v1`; IDL publish; narrative compilers; pathway/functional packs; retail SSOT 40 biomarkers; P3 schema/templates **docs-only**; MR-BATCH **candidate/test-only** |
| Verdict | **RUNTIME_WIRED** for clinician/IDL/narrative substrate; prose depth **CANDIDATE_ONLY / DOCS_ONLY** for P3/MR assets; retail coverage partial |
| Gaps | Modifier binding deferred; frame routing deferred; candidate→approved promotion route absent |
| Beta blockers | Content depth + frame routing + retail coverage decision (79/79 vs subset) |

### Block 4 — Layer C / Gemini

| Aspect | Detail |
|---|---|
| Claimed | Low; Gemini inactive |
| Evidence | `resolve_narrative_llm_allow_llm` deny-default; P2-4 NarrativePayload hardening; CEO gate in carry-forwards; Gemini used on upload parse path when enabled (`llm_parser.py`) — separate from narrative authority |
| Verdict | Narrative Gemini **NOT_PRODUCTION_ACTIVE**; Layer C brief contract **BUILT_AND_MERGED**; parse-path LLM **RUNTIME_WIRED when configured** but non-analytical for report story |
| Gaps | Activation design (P4-1) CEO-gated; tests for constrained translation underdeveloped historically |
| Beta blockers | Must not activate narrative Gemini as analytical authority |

### Block 5 — UX / results page

| Aspect | Detail |
|---|---|
| Claimed | Medium; residual trust issues |
| Evidence | Results journey paper v6 authoritative per map; FE consumers of clinician_report / IDL / domains; sanitize helpers; presentation selection helpers exist |
| Verdict | **RUNTIME_WIRED** render path; trust/IA polish **PARTIAL**; frontend UAT blocked in P3 carry-forward on content/frame/modifier/Gemini/journey |
| Gaps | Journey v6 IA work; hierarchy/trust residual issues (historical audits) |
| Beta blockers | Content completeness + UX trust after Layer B stabilises |

### Block 6 — Safety / provenance

| Aspect | Detail |
|---|---|
| Claimed | Medium–High |
| Evidence | Day-one validators; launch estate gate YAML; collision resolver; provenance builders; Pass3 protocol (draft); package provenance classification exists; inferred vs explicit `source_spec_id` still mixed |
| Verdict | **GOVERNANCE + RUNTIME_WIRED** for many gates; estate-wide explicit provenance **not** complete; Pass3 DRAFT status weakens claimed maturity |
| Gaps | Explicit provenance coverage; secrets history review; draft promotion protocol |
| Beta blockers | Secrets history/rotation verification; provenance honesty on inferred fields |

### Block 7 — Auditability / replay

| Aspect | Detail |
|---|---|
| Claimed | Medium |
| Evidence | Replay contracts include six Wave 1 domains; result versioning / stale banners historically present; Sentinel packs exist; broader beta gate artefact still not a single executed controlled-beta gate |
| Verdict | **PARTIAL RUNTIME_WIRED**; not production-grade regulatory completeness |
| Gaps | Broader replay/Sentinel; single beta-readiness gate execution |
| Beta blockers | Incomplete end-to-end replay estate |

### Block 8 — Phenotype / beta validation

| Aspect | Detail |
|---|---|
| Claimed | Low–Medium |
| Evidence | Phenotype map + IDL consumers; fixtures/Sentinel exist; MR-BATCH is **not** a phenotype validation estate |
| Verdict | **PARTIAL**; insufficient for controlled beta claim |
| Gaps | Edge cases, incomplete panels, suppression/counter-evidence breadth |
| Beta blockers | Validation estate breadth + human approval gate |

**Overall programme maturity (auditor):** architecturally coherent Wave 1 slice with expanded domains; **not** controlled-beta ready. Strategy “not beta-ready” conclusion still holds; several strategy **gap descriptions** are outdated.

---

## 8. Day-one architecture verification

| Topic | Maturity | Evidence | Does not prove |
|---|---|---|---|
| Canonical research authority | GOVERNANCE_PARTIAL | Pass3 protocol + research specs; packages cite research | Protocol still DRAFT |
| Research → governed artefact traceability | PARTIAL | Compile manifests + estate index resolve (0 missing paths in sampled estate refs) | Estate-wide explicit `source_spec_id` for all packages |
| Package provenance | CLASSIFIED / MIXED | launch estate / provenance scanners exist | All packages explicit |
| `source_spec_id` explicit vs inferred | RUNTIME_WIRED mixed | `signal_activation_identity_v1.resolve_activation_identity` | Explicit-only estate |
| Compile manifests | RUNTIME_WIRED (artefact refs) + GOVERNANCE validators | `knowledge_bus/compiled/manifests/`; estate index; validators | Live Pass3→card compile on request path |
| Activation compile path | PARTIAL / DEFERRED historically | Day-one carry-forward historically listed activation compile | Full activation-compile authority closed |
| `activation_key` | RUNTIME_WIRED | `build_activation_key`; evaluator registry | — |
| Multi-frame activation | RUNTIME_WIRED | Same `signal_id` allowed across frames when keys differ (validators) | Multi-frame **compiled root-cause** sets |
| Duplicate `activation_key` fail-closed | RUNTIME_WIRED | `signal_evaluator.py` raises on collision | — |
| Family-vs-frame assumptions | PARTIAL | Collision model / frame indexes exist | Uniform downstream policy everywhere |
| Interaction / phenotype maps | RUNTIME_WIRED | map YAML + builders/publishers | Full phenotype beta estate |
| PSI generation | EXISTS (compiler/pilot) | `compile_pass3_pilot_artifacts.py`; package PSI files | Runtime analysis consumption |
| PSI manifest opt-in | EXISTS on packages | `promoted_signal_intelligence:` in manifests | Activation |
| PSI loader | EXISTS / DEAD on launch path | `load_promoted_signal_intelligence.py`; only unit tests import | Launch wiring |
| PSI runtime consumption | CANDIDATE_ONLY / deferred | Validators forbid launch imports | Future activation readiness |
| Card evidence | RUNTIME_WIRED compiled | `get_card_evidence_artefact`; estate cards | Pass3 richness fully expressed on cards |
| Hard-coded card evidence | NONE remaining per estate | `wave1_subsystems_legacy_hard_coded: []` | Older audits claiming hard-coded fallbacks are **STALE** |
| Compiled hypotheses | RUNTIME_WIRED pilot | vitamin D only | Estate-wide compiled WHY |
| Root-cause / WHY | RUNTIME_WIRED dual path | `compile_root_cause_v1` + legacy registry (~40 YAML) | Compiled-only authority |
| Legacy root-cause YAML | RUNTIME_WIRED for non–vitamin-D | `knowledge_bus/root_cause/hypotheses/` | Retirement complete |
| Multi-frame root-cause policy | BLOCKED / PARTIAL | Tests block multi-frame compiled promotion | Policy sprint closed |
| Frontend render-only | MOSTLY | Card copy maps enums; domain IDs fixed; sanitize | Zero presentation selection logic (some ranking helpers exist) |
| Gemini non-authoritative for analysis | YES for narrative default | deny-default policy | Upload parse path never uses Gemini |

---

## 9. Layer B, prose and reasoning maturity

| Topic | Verdict | Evidence |
|---|---|---|
| Prose library authority | No named `prose_library/` runtime package; live packs are pathway/functional/entity YAML + retail SSOT | VERIFIED_FACT |
| Approved production prose | Retail registry 40 biomarkers; pathway explainers pack | RUNTIME_WIRED |
| Candidate prose | MR-BATCH-001B 69 assets all `CANDIDATE` | CANDIDATE_ONLY |
| Modifier binding | Templates in P3 docs; carry-forward `future_work`; catalogue often inactive | DOCS_ONLY / NOT_RUNTIME_WIRED |
| Frame routing | Deferred (`P2-FRAME-ROUTING-ARCHITECTURE-1`) | NOT_FOUND as production router |
| Signal frames ↔ prose selection | Production selection uses existing registries/hints; MR candidate composition is **test-side only** | VERIFIED_FACT |
| Contradiction handling | Interaction map / insight graph exist; Pass3 contradiction richness historically under-consumed | PARTIAL |
| Confirmatory-test handling | UNKNOWN_REQUIRES_REVIEW for full estate behaviour in this audit | — |
| Clinician report | `compile_clinician_report_v1` path + FE Section consumers | RUNTIME_WIRED |
| Retail-safe wording | Registry boilerplate + FE sanitize + consumer safety helpers | PARTIAL / RUNTIME_WIRED |
| IDL safety | `publish_interpretation_display_layer_v1` + IDL records | RUNTIME_WIRED |
| Deterministic Layer B independent of Gemini | Yes by default | VERIFIED_FACT |

---

## 10. Layer C, Gemini and frontend boundary

| Topic | Verdict | Evidence |
|---|---|---|
| Narrative Gemini | Deny-default; CEO gate for activation | `narrative_runtime_policy`; P2-4 / P3 carry-forwards |
| NarrativePayload B→C brief | Hardened contract present | P2-4 completion + tests (per register/merge) |
| Frontend DTO wiring | Types/store/results page consume clinician report, IDL, domains, provenance fields | `frontend/app/types/analysis.ts` and results components |
| Medical inference in FE | No scoring/diagnosis engine found; display shaping + sanitize | REASONABLE_INFERENCE from module survey |
| Borderline FE logic | Presentation alignment helpers (e.g. hero/driver picks from backend scores) | Not analytical authority, but not “zero logic” |
| Gemini as analytical authority | **Not** for narrative story path under defaults | VERIFIED_FACT |

---

## 11. Recent sprint verification

| Sprint / work | Spec / pack | Hardening / gate | Implementation | Tests | Merge evidence | Active today? | Carry-forward / contradictions |
|---|---|---|---|---|---|---|---|
| P2-4 NarrativePayload | beta_readiness P2-4 docs | bus COMPLETE + gate artefacts (local) | NarrativePayload contract hardening | Contract tests cited in register | Merge `8aea163` | Yes (contract) | Gemini CEO-gated; frame routing deferred |
| P3-PROSE-DEPTH-1 | schema/matrix/templates | `latest_prompt_hardening.json`; gate PASS local | Docs/schema only | Foundations | Merge `df56a35` | Schema docs active; not runtime | Modifier/frame deferred; older CF still points to MR medical review |
| P3-PROSE-DEPTH-1A | schema directional rules | Docs | Schema/docs | — | Commit `78e3aaf` lineage | Docs active | No production promotion |
| MR-BATCH-001B | assets YAML + completion | Unit tests; no bus WP token for this work on main status file | Test loader + output md | `test_mr_batch_001b_*` | Merge `8744b09`; HEAD register update `2a8fa64` | **Test fixture only** | Register forbids medical review; completion §11 still recommends it |
| P1-25 thyroid MR v2 | completion + manifests | Pass3 CF | Allowlist/activation updates | Governance/regression expected | On main (domain cards present) | Thyroid domain RUNTIME_WIRED with deferrals | Antibodies partially deferred |
| P1-26 iron/homocysteine | manifests/cards | Pass3 CF | Cards in estate index | — | On main | RUNTIME_WIRED cards | — |
| ARCH-RT / day-one series | ADR-RT + audits | validators + Sentinel packs | Compiled estate | architecture tests | Historical merges | Launch slice active; programme CF open | PSI deferred; dual WHY path |
| BETA-READINESS-RECHECK-1 | audit paper 2026-06-14 | — | — | — | Snapshot at `f6054d4` | Secrets **not currently tracked**; history/rotation UNKNOWN | Do not treat as current secrets status without re-verify |

---

## 12. MR-BATCH-001B classification

### Intended classification (assignment)

1. Retained as Round 1 benchmark / test fixture  
2. Not medically approved  
3. Not for promotion  
4. Not for production runtime  
5. Useful only as benchmark for future Round 2 prose pipeline design  

### Repository verification

| Check | Result | Evidence |
|---|---|---|
| Asset location | Sprint docs only | `docs/sprints/beta_readiness/MR-BATCH-001B_candidate_prose_assets.yaml` |
| Asset count / status | 69 assets; statuses `{CANDIDATE}` only; 0 APPROVED | Python parse this audit |
| Production loader | **None** | Orchestrator / retail assembly contain no `MR-BATCH-001B` / `mr_candidate_prose` strings |
| Test loader | Exists; requires `candidate_test_mode=True` | `backend/tests/support/mr_candidate_prose_test_v1.py` |
| Isolation tests | Assert non-import by production modules; Gemini inactive | `backend/tests/unit/test_mr_batch_001b_candidate_prose_test_import.py` |
| Knowledge Bus / manifests | No 001B promotion records under `knowledge_bus/` found | Search |
| BUILD register (HEAD) | Explicit ROUND_1_BENCHMARK / TEST FIXTURE; **must not** medical review or promotion | Register § MR-BATCH-001B |
| Completion / output docs | Still recommend medical review then promotion design | **Documentation contradiction** — not runtime contradiction |

### Classification verdict

**SUPPORTED** for runtime/safety classification: retained as Round 1 benchmark / test fixture; not medically approved; not for production runtime; not promoted into Knowledge Bus production packs.

**Blocker (documentation authority, not runtime):** AUTH-06 — older completion/output artefacts still instruct medical review/promotion. Until those are superseded or annotated, future agents may mis-route work. This is a **governance blocker**, not evidence of runtime promotion.

**No runtime promotion blocker found** that contradicts “not for production runtime.”

---

## 13. Documentation-versus-code mismatches

| Mismatch | Docs claim | Code / repo reality | Label |
|---|---|---|---|
| Missing three launch-core domains | Strategy §8.1 | Six domains wired + compiled cards | STALE doc |
| Hard-coded card evidence remaining | Older programme audits | Estate `legacy_hard_coded: []`; assembler no hard-coded fallback | STALE doc |
| KB SOP authoritative version | AUTHORITY_MAP → v1.3 | Ops/rules → v1.3.1; both files present | AUTHORITY CONFLICT |
| Pre-SOP version | AUTHORITY_MAP → v0.4 | Live v0.6.2 | STALE map |
| Current sprint status | `SPRINT_STATUS.md` LIVE 2026-05-04 | Beta register through 2026-06-30 | STALE |
| Cursor status = latest work | P3 COMPLETE | HEAD includes MR-BATCH + register updates | STALE ops cache |
| Pass3 protocol readiness | Used as companion everywhere | Status DRAFT | GOVERNANCE GAP |
| MR-BATCH next step | Completion recommends medical review | Register forbids it | CONFLICT |
| `latest_knowledge_status.json` | Expected by bus tooling | Missing under `knowledge_bus/current/` | GAP |
| Named prose library runtime | Inventory/docs language | No `prose_library` package; packs elsewhere | NAMING MISMATCH |
| PSI “promoted” language | Package filenames / manifests | Not consumed on launch path | SEMANTIC TRAP |
| Secrets beta blocker | RECHECK-1 committed secrets on main | Files not git-tracked now; local copies exist | PARTIALLY SUPERSEDED / UNKNOWN history |

---

## 14. Stale or superseded build-register recommendations

Treat each entry’s “Recommended next sprint” as **historical recommendation at closure**, not current mandate — except the **latest** entry.

| Historical recommendation pattern | Status now |
|---|---|
| P1-1 → P1-2 kidney, etc. | Delivered / superseded by later P1 sequence |
| P1-4 thyroid domain while blocked | Later thyroid sprints progressed; still partial depth |
| Medical review of MR-BATCH-001B (P3 / 1A entries) | **Superseded** by MR-BATCH-001B register entry forbidding medical review |
| P4-1 Gemini activation design | Still CEO-gated; not invalidated, but not next continuity recommendation |
| Latest: `SPRINT-BUILD-PLAN-AUDIT-1` | Current continuity recommendation (this audit is aligned in purpose) |

---

## 15. Active blockers before controlled beta

Ordered by evidence strength (not a sprint selection):

1. **Authority stack adjudication** (AUTH-01..08) — planning risk if agents follow wrong docs  
2. **MR-BATCH documentation conflict** — risk of incorrect medical-review sprint  
3. **Prose / frame / modifier incompleteness** — Layer B depth insufficient for trustworthy consumer explanation at beta  
4. **Retail explainer coverage decision unresolved** (40 wired vs larger biomarker estate; 79/79 question open)  
5. **PSI deliberately unwired** — research richness stranded; acceptable only if beta scope excludes PSI claims  
6. **Dual root-cause authority** (compiled vitamin D + legacy YAML) — regeneration/traceability complexity  
7. **Pass 3 protocol still DRAFT** while used as operational companion  
8. **Phenotype / edge-case validation estate insufficient** for external exposure claims  
9. **Secrets history / rotation verification** still UNKNOWN despite non-tracking of `.env`  
10. **No active mechanical knowledge-status ready gate file** at expected path  
11. **Narrative Gemini must remain non-authoritative** until CEO-gated design — not a feature gap, a safety constraint  

---

## 16. Candidate next work packages

Plausible candidates only. **None selected as the next sprint.**

### CWP-1 — Document authority reconciliation

- **Problem evidenced:** AUTH-01..08; stale AUTHORITY_MAP / SPRINT_STATUS; dual KB SOP; MR-BATCH review conflict  
- **Why it matters:** Wrong authority → wrong sprint selection and unsafe promotion attempts  
- **Dependencies:** Head of Architecture decisions  
- **Risk class:** Governance / process (HIGH organisational risk if skipped)  
- **Medical review required?** No  
- **Blocked by unresolved authority decision?** It *is* that decision  

### CWP-2 — SPRINT-BUILD-PLAN-AUDIT-1 (programme vs codebase reconciliation)

- **Problem evidenced:** Strategy maturity tables outdated; register recommends this; this Cursor audit is a sibling input  
- **Why it matters:** Prevents reinventing delivered Block 1 work or reopening closed PSI decisions casually  
- **Dependencies:** Prefer after CWP-1  
- **Risk class:** Planning  
- **Medical review?** No  
- **Blocked by authority decision?** Partially (AUTH conflicts)  

### CWP-3 — Round 2 prose research pipeline design (explicitly excluding MR-BATCH-001B promotion)

- **Problem evidenced:** Candidate depth needed; Round 1 pipeline not trusted per register  
- **Why it matters:** Layer B consumer explanation is a beta differentiator  
- **Dependencies:** Authority lock on MR-BATCH benchmark-only; schema from P3  
- **Risk class:** Medical content process  
- **Medical review?** Yes for outputs of Round 2 — not for promoting 001B  
- **Blocked?** Yes if AUTH-06 unresolved  

### CWP-4 — Frame-routing architecture (P2-FRAME-ROUTING-ARCHITECTURE-1)

- **Problem evidenced:** Deferred in P3 carry-forward; multi-frame activation exists without prose binding  
- **Why it matters:** Wrong-frame prose is a clinical trust risk  
- **Dependencies:** Stable activation_key model (exists); prose selection design  
- **Risk class:** Architecture / clinical presentation  
- **Medical review?** Likely for policy outcomes  
- **Blocked?** Not by AUTH map, but by sequencing after Layer B design choices  

### CWP-5 — Retail coverage subset decision + governed fill

- **Problem evidenced:** 40/registry biomarkers; open 79/79 question  
- **Why it matters:** Incomplete explainers undermine beta UX  
- **Dependencies:** Coverage decision; Round 2 pipeline if new content  
- **Risk class:** Content / product  
- **Medical review?** Yes for new medical prose  
- **Blocked?** By coverage decision (product/clinical)  

### CWP-6 — Root-cause compiled authority expansion / legacy retirement plan

- **Problem evidenced:** Only vitamin D compiled; 40 legacy YAML still live  
- **Why it matters:** Traceability and dual-path complexity  
- **Dependencies:** Multi-frame root-cause policy  
- **Risk class:** Core intelligence  
- **Medical review?** Yes for clinical WHY content  
- **Blocked?** Multi-frame policy historically blocked  

### CWP-7 — Secrets history and environment hygiene verification

- **Problem evidenced:** RECHECK-1 blocker; local env files still present; not currently tracked  
- **Why it matters:** Hard beta blocker class if secrets remain in history or live systems  
- **Dependencies:** Ops access to history/rotation evidence  
- **Risk class:** Security  
- **Medical review?** No  
- **Blocked?** UNKNOWN pending verification  

### CWP-8 — Pass 3 protocol ratification (DRAFT → APPROVED)

- **Problem evidenced:** Operative companion still DRAFT; cites older KB SOP line  
- **Why it matters:** Promotion governance ambiguity  
- **Dependencies:** AUTH-01/02  
- **Risk class:** Governance  
- **Medical review?** No (protocol), medical for promotions using it  
- **Blocked?** By HoA ratification  

### CWP-9 — Phenotype / incomplete-panel beta validation estate expansion

- **Problem evidenced:** Block 8 low–medium; strategy still correct on validation thinness  
- **Why it matters:** External beta without panels is optimism  
- **Dependencies:** Stable domain/Layer B scope  
- **Risk class:** QA / clinical validation  
- **Medical review?** Panel design may need clinical input  
- **Blocked?** Not by AUTH, by programme sequencing  

### CWP-10 — PSI staged activation readiness (report-only → optional wire)

- **Problem evidenced:** 57 PSI files; loader dead on launch path by design  
- **Why it matters:** Unlocks stranded research intelligence — or confirms continued deferral  
- **Dependencies:** Explicit activation decision; day-one isolation tests  
- **Risk class:** Core intelligence / HIGH if wired casually  
- **Medical review?** Yes before activation  
- **Blocked?** By explicit architecture decision (ARCH-RT-5E deferral)  

---

## 17. Recommended immediate next action

**Head of Architecture adjudication + document authority cleanup**, using this audit and the BUILD register’s `SPRINT-BUILD-PLAN-AUDIT-1` intent as inputs.

Concrete governance actions (not an implementation prompt):

1. Resolve AUTH-01 (KB SOP v1.3 vs v1.3.1) and refresh `docs/AUTHORITY_MAP.md`.  
2. Ratify or formally keep-as-draft Pass 3 protocol v1.1; align companion citations.  
3. Mark `docs/SPRINT_STATUS.md` STALE/ARCHIVE; point navigation to BUILD register + AUTHORITY_MAP.  
4. Annotate or supersede MR-BATCH completion/output sections that still recommend medical review, so they cannot override the HEAD register classification.  
5. Refresh strategy Block 1 maturity note (six domains present; depth remaining) without rewriting the whole strategy.  
6. Decide whether local `automation_bus/latest_*` should be regenerated or explicitly labelled non-authoritative after merges outside the kernel.  
7. Only after the above, select an implementation sprint from candidates in §16.

Do **not** treat this section as authorisation to implement runtime changes.

---

## 18. Evidence index

| ID | Path / symbol | Proves | Does not prove |
|---|---|---|---|
| E01 | `git rev-parse HEAD` → `2a8fa64…` on `main` | Audit baseline | Future merges |
| E02 | `docs/governance/AUTOMATION_BUS_SOP_v1.3.1.md` LOCKED | Active Automation Bus SOP | Perfect mechanical enforcement of every clause |
| E03 | `docs/governance/KNOWLEDGE_BUS_SOP_v1.3.1.md` | Live KB SOP used by rules | AUTHORITY_MAP already updated |
| E04 | `docs/governance/KNOWLEDGE_BUS_SOP_v1.3.md` coexistence | Dual file conflict | Which file git history intended |
| E05 | Pass3 protocol v1.1 DRAFT header | Operative-but-draft | Formal ratification |
| E06 | `BUILD_DELIVERABLE_REGISTER.md` MR-BATCH entry | Continuity classification benchmark-only | Medical correctness of candidates |
| E07 | `wave1_subsystem_evidence.py` six domains | Domain wiring | Equal clinical depth |
| E08 | `estate_index_v1.yaml` 10 cards; legacy hard-coded `[]` | Compiled card estate; no legacy hard-coded list | Estate index `updated_at` currency |
| E09 | Estate path resolve 0 missing | Indexed refs exist on disk | All manifests semantically correct |
| E10 | `signal_evaluator.py` duplicate activation_key raise | Fail-closed collisions | No multi-frame product bugs |
| E11 | PSI loader imports only in tests/validators | Not launch-wired | PSI files invalid |
| E12 | `compile_root_cause_v1` + vitamin D gate | Dual WHY path | Legacy YAML medically complete |
| E13 | Retail registry 40 biomarkers | Partial retail coverage | Exact beta-blocking threshold |
| E14 | MR pack 69 CANDIDATE; test isolation | Benchmark/fixture classification | Future agent compliance |
| E15 | No orchestrator/retail MR strings | Not production imported | Dynamic import tricks (none found) |
| E16 | `automation_bus/latest_cursor_status.json` P3 + bus_version 1.2 | Stale ops status vs HEAD | Kernel broken |
| E17 | Missing `knowledge_bus/current/latest_knowledge_status.json` | Expected status file absent | Entire KB non-functional |
| E18 | `.env` not tracked + gitignored | RECHECK-1 “committed on main” not current index state | History purged; keys rotated |

---

## Appendix A — Governance document classification table

| Path | Title / role | Stated version/status | Classification | Evidence for classification | Referenced by | Conflict / successor | Govern planning? | Confidence |
|---|---|---|---|---|---|---|---|---|
| `AGENTS.md` | Agent Operating Map | Current | AUTHORITATIVE_CURRENT | Repo root operating map | Agents | — | Yes | HIGH |
| `.claude/CLAUDE.md` | Permanent context | Current | AUTHORITATIVE_CURRENT | Cites live SOPs + register | Claude/Cursor | Prefer over stale map entries | Yes | HIGH |
| `docs/governance/AUTOMATION_BUS_SOP_v1.3.1.md` | Automation Bus SOP | LOCKED; supersedes v1.3 | AUTHORITATIVE_CURRENT | Header + citations | CLAUDE, map, AGENTS | Older archive copies | Yes | HIGH |
| `docs/governance/KNOWLEDGE_BUS_SOP_v1.3.1.md` | Knowledge Bus SOP | APPROVED WITH CONSTRAINTS | AUTHORITATIVE_CURRENT | Header + cursor rule | CLAUDE, rules | Conflicts with map→v1.3 | Yes | HIGH |
| `docs/governance/KNOWLEDGE_BUS_SOP_v1.3.md` | Knowledge Bus SOP | APPROVED | LEGACY_OR_SUPERSEDED *(or UNKNOWN if HoA keeps)* | Sibling of v1.3.1; map still cites | AUTHORITY_MAP | Successor v1.3.1 | No pending adjudication | MEDIUM |
| `docs/governance/KNOWLEDGE_BUS_PASS3_PROMOTION_PROTOCOL_v1.1.md` | Pass3 protocol | DRAFT | AUTHORITATIVE_CURRENT *(draft caveat)* | Companion citations | SOP, rules, sprints | v1.0 superseded | Yes with caveat | MEDIUM |
| `docs/governance/KNOWLEDGE_BUS_PASS3_PROMOTION_PROTOCOL_v1.0.md` | Pass3 protocol | DRAFT | LEGACY_OR_SUPERSEDED | Older sibling | Historical | v1.1 | No | HIGH |
| `docs/governance/healthiq_pre_sop_prompt_scoping_workflow_v0_6.2.md` | Pre-SOP workflow | ACTIVE | AUTHORITATIVE_CURRENT | Header supersedes 0.6.1 | CTRL-01 notes | Map cites v0.4 | Yes | HIGH |
| `docs/governance/healthiq_pre_sop_prompt_scoping_workflow_v0_6.1.md` | Pre-SOP | Amended | LEGACY_OR_SUPERSEDED | Superseded by 0.6.2 | — | 0.6.2 | No | HIGH |
| `docs/discussion documents/healthiq_pre_sop_*` | Discussion drafts | Various | LEGACY_OR_SUPERSEDED | Discussion folder | Stale map | 0.6.2 | No | HIGH |
| `docs/governance/CURSOR_OPERATING_POLICY.md` | Cursor policy | Policy | AUTHORITATIVE_CURRENT | Map | Agents | — | Yes | HIGH |
| `docs/AUTHORITY_MAP.md` | Authority map | LIVE 2026-06-20 | AUTHORITATIVE_CURRENT *(needs refresh)* | Purpose statement | Navigation | Internal stale rows | Yes after update | MEDIUM |
| `docs/strategy/beta_readiness/HEALTHIQ_AI_BETA_READINESS_DEFINITIVE_STRATEGY_FINAL_2026-06-20.md` | Beta strategy | FINAL v1.0 | AUTHORITATIVE_CURRENT structure / STALE maturity rows | Header + map | Register, programme | Block 1 claims outdated | Yes (structure) | HIGH/MEDIUM |
| `docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md` | Build register | Continuity log | CURRENT_BUT_LIGHTWEIGHT_CONTINUITY_ONLY | Self-declared | CLAUDE, advisory skill | Not audit substitute | Continuity yes | HIGH |
| `docs/sprints/healthiq_day_one_architecture_rework_sprint_plan_FINAL_updated.md` | Day-one plan | FINAL updated | AUTHORITATIVE_CURRENT (CF) | Updated variant | Audits | Non-updated FINAL | Architecture CF | MEDIUM |
| `docs/sprints/healthiq_day_one_architecture_rework_sprint_plan_FINAL.md` | Day-one plan | FINAL | LEGACY_OR_SUPERSEDED | Parallel FINAL | — | `_updated` | No | MEDIUM |
| `docs/architecture/ADR-RT-001`…`004` | Research-to-runtime ADRs | ACCEPTED | AUTHORITATIVE_CURRENT | Headers | Day-one programme | — | Yes | HIGH |
| `architecture/ADR-001`…`009` (excl. 004) | Classic ADRs | Various | AUTHORITATIVE_CURRENT | Map + index | Core | ADR-004 superseded | Yes | HIGH |
| `docs/SPRINT_STATUS.md` | Sprint status | LIVE 2026-05-04 | LEGACY_OR_SUPERSEDED | Date + content era | docs README | BUILD register | No | HIGH |
| `docs/audit-papers/*` (series) | Audits/closures | Various verdicts | FORMAL_AUDIT_OR_CLOSURE_EVIDENCE | Folder purpose | Planning refs | May be stale vs later code | No (evidence only) | HIGH |
| `automation_bus/latest_*` | Ops cache | Local | CURRENT_BUT_LIGHTWEIGHT_CONTINUITY_ONLY / STALE | Gitignored; P3 status | Kernel scripts | HEAD newer | Context only | MEDIUM |
| `docs/sprints/beta_readiness/P*_*.md|yaml` | Sprint packs | Sprint-local | SPRINT_SPECIFIC_CONTEXT | Paths | Register | Later sprints | Historical | HIGH |
| `docs/archive/**` | Archive | Superseded banners | LEGACY_OR_SUPERSEDED | Archive tree | — | Live docs | No | HIGH |
| `docs/planning-papers/**` | Planning | Various | LEGACY_OR_SUPERSEDED / continuity | Planning folder | History | Strategy/ADRs | Rarely | MEDIUM |
| This report | Cursor maturity audit | 2026-07-25 | FORMAL_AUDIT_OR_CLOSURE_EVIDENCE | Assignment output | Future planning | Does not replace SOPs | Evidence for planning | HIGH |

---

## Appendix B — Capability maturity matrix

| Capability | Applicable states | Notes |
|---|---|---|
| Automation Bus SOP + kernel scripts | BUILT_AND_MERGED + RUNTIME_WIRED (ops) | Status cache stale; no active WP |
| Knowledge Bus SOP | BUILT_AND_MERGED (docs) | Dual version conflict |
| Pass 3 promotion protocol | DOCS_ONLY / DRAFT | Used as companion |
| Pass 3 compile → generated_pilot | BUILT_AND_MERGED + CANDIDATE_ONLY | Not auto-activate |
| PSI loader | BUILT_AND_MERGED + NOT_RUNTIME_WIRED + CANDIDATE_ONLY | Deferred by tests |
| Compile manifests + estate index | RUNTIME_WIRED (refs) + GOVERNANCE | Paths resolve |
| Activation key / multi-frame / duplicate fail-closed | RUNTIME_WIRED | Evaluator + validators |
| Compiled card evidence → Wave1 domains | BUILT_AND_MERGED + RUNTIME_WIRED + PRODUCTION_ACTIVE (Wave1 path) | Six domains |
| Hard-coded card evidence | SUPERSEDED / NONE | Estate empty list |
| Compiled hypothesis WHY | RUNTIME_WIRED + CANDIDATE_ONLY (pilot vitamin D) | Dual with legacy |
| Legacy root-cause YAML | RUNTIME_WIRED | ~40 targets |
| Interaction / phenotype / IDL | RUNTIME_WIRED | — |
| Deterministic narrative Layer B | RUNTIME_WIRED | Gemini off by default |
| Retail explainers | RUNTIME_WIRED + PARTIAL coverage | 40 biomarkers |
| P3 prose schema/templates | DOCS_ONLY + CANDIDATE_ONLY | No runtime binder |
| MR-BATCH-001B | TEST_ONLY + CANDIDATE_ONLY + NOT_PRODUCTION_ACTIVE | Benchmark |
| Narrative Gemini | BUILT (client exists) + NOT_PRODUCTION_ACTIVE | CEO gate |
| Upload Gemini parse | RUNTIME_WIRED when configured | Non-narrative authority |
| Frontend render path | RUNTIME_WIRED | Mostly render-only |
| Day-one validators / CI architecture gate | RUNTIME_WIRED (CI/scripts) | — |
| Controlled beta readiness claim | BLOCKED | Multiple open gaps |

---

## Appendix C — Recent sprint verification table

| Work ID | Spec present | Code present | Tests present | Gate/audit present | Merged to main | Still active? | Contradictions |
|---|---|---|---|---|---|---|---|
| P2-4 | Yes | Yes | Yes (per register/merge) | Local bus gate for WP | Yes | Contract active | — |
| P3-PROSE-DEPTH-1 | Yes | Docs/schema | Foundations | Local bus PASS | Yes | Docs active | CF medical-review vs later register |
| P3-PROSE-DEPTH-1A | Yes | Docs/schema | — | Docs | Yes | Docs active | — |
| MR-BATCH-001B | Yes | Test support only | Yes | Completion md; unit tests | Yes | Fixture only | Completion vs register on medical review |
| P1-25 / P1-26 | Yes | Cards/assemblers | Governance tests exist in estate | Completion packs | Yes | Domain cards active | Strategy still says domains missing |
| ARCH-RT-5/6 | Yes | Validators + compiled estate | Architecture/Sentinel | Audit papers | Yes | Launch slice active | Programme CF open |
| BETA-READINESS-RECHECK-1 | Audit only | N/A | N/A | Paper | Snapshot | Secrets claim outdated vs index | Needs security re-verify |

---

## Appendix D — Commands and searches executed

Representative commands and searches used in this audit (not exhaustive of every Read/Grep):

```text
git rev-parse --abbrev-ref HEAD
git rev-parse HEAD
git status --short --branch
git status --porcelain
git log --oneline -20
git ls-files --error-unmatch .env
git check-ignore -v .env

Get-ChildItem docs/audit-papers
Get-ChildItem docs/governance
Test-Path knowledge_bus/current/latest_knowledge_status.json
Test-Path automation_bus/state/work_package_active.json
Get-Content automation_bus/latest_cursor_status.json

rg / Grep: MR-BATCH-001B, mr_candidate_prose, load_promoted_signal_intelligence,
  activation_key, compile_manifest, wave1_kidney|blood_iron|thyroid, gemini,
  hard-coded, Pass3, prose_library

python: parse retail registry count; MR asset statuses; estate_index path resolution

Glob: **/*SOP*, docs/**/*.{md,yml,yaml}, governance/authority/gate artefacts
```

Parallel explore agents were used for broad discovery; claims in this report were corroborated with direct file reads, greps, and local counts on `main` @ `2a8fa64…`.

---

*End of audit report. No runtime code, schemas, tests, packages, or governance files were modified by this auditor other than creating this file.*
