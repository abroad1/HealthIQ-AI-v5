# HealthIQ AI — Sprint Governance Discovery and Codebase Maturity Audit

**Repository:** C:\Users\abroa\HealthIQ-AI-v5
**Branch:** main
**HEAD SHA:** 2a8fa64ed791cabc8ae478113b96cefdf25145a1
**Audit date:** 2026-07-25
**Auditor:** Claude Code (independent governance and architecture assurance auditor)

---

## 1. Executive verdict

The repository has a mature, largely self-consistent Automation Bus lifecycle for early-to-mid programme sprints, and one clean example of correctly-isolated research candidate content (MR-BATCH-001B). However, three material issues undermine confidence in "current state" claims:

1. **The canonical Automation Bus artefact set (`automation_bus/latest_*`) is frozen at sprint P3-PROSE-DEPTH-1 (closed 2026-06-29).** Six later commits — covering P3-PROSE-DEPTH-1A and all of MR-BATCH-001B — carry no matching `chore(bus): <work_id> kernel IN_PROGRESS/COMPLETE` commit pair, no hardening artefact, and no audit summary. This is a real gap between documented lifecycle process and what actually ran for the most recent work.
2. **`docs/AUTHORITY_MAP.md` is stale in its governance/control-plane section**: it names `KNOWLEDGE_BUS_SOP_v1.3.md` (superseded) as authoritative, omits `KNOWLEDGE_BUS_SOP_v1.3.1.md` and both Pass-3 promotion protocol versions entirely, and cites a pre-SOP scoping document (`v0_4.md`) that does not exist anywhere in the repository — a stale reference that is also embedded inside the LOCKED `AUTOMATION_BUS_SOP_v1.3.1.md` itself.
3. **The last ~13 register entries (P1-13 through MR-BATCH-001B) have no independent `docs/audit-papers/` closure document**, breaking the pattern set by earlier sprints (which did receive dedicated ARCH-COMPLETION/BATCH2/DHEA-style audit papers). All "Complete" status for this stretch rests on self-authored register/completion-doc entries only.

Against this, MR-BATCH-001B itself is verified clean: it is fully isolated to `docs/sprints/` and `backend/tests/`, gated behind an explicit `candidate_test_mode=True` runtime guard, tagged `review_status: CANDIDATE` throughout, and referenced nowhere in production backend code. The Knowledge Bus SOP v1.3.1 is unusually candid about its own enforcement gaps (self-declares several validation categories as "Required (Not Yet Implemented)"), which is a governance strength (honest self-disclosure) even though it is also a maturity weakness (the gaps are real).

The Automation Bus gate (`golden_gate_local.py`) is genuinely narrow — three checks (architecture validation, baseline tests, three-layer pipeline verification) — and Sentinel is explicitly report-only and not wired into any CI workflow. One correction to an initial research finding: `run_architecture_validation_gate.py` (one of the three golden_gate_local.py checks) **is** independently invoked by `.github/workflows/architecture-gate.yml` on every push/PR to `main`/`develop`, so architecture validation specifically is CI-enforced even though the full local gate script, Sentinel, and prose/content-specific checks are not.

## 2. Audit scope and method

This audit was performed by direct repository inspection: `git log`/`git show`, `Read` of governance documents, prompt-hardening/audit-summary/status JSON, backend source files (signal registry, root-cause compiler, card evidence, orchestrator, Gemini client), frontend results components, CI workflow YAML, and test/fixture files. Four parallel research passes (governance/control-plane; day-one architecture/Layer B/Gemini boundary; beta-readiness programme blocks/recent-sprint verification; MR-BATCH-001B) were run and their findings cross-checked and, where feasible, independently re-verified by the lead auditor (e.g. CI workflow content, register tail, audit-papers inventory) rather than accepted at face value. No repository file other than this report was modified. No sprint was selected, no implementation prompt was written.

Where a prior audit paper's claim was reused, it was only after checking whether the cited file still exists at current HEAD and, where practical, cross-reading the current source directly (see §11 for specific re-verifications).

## 3. Repository and branch state

- Branch: `main`
- HEAD: `2a8fa64ed791cabc8ae478113b96cefdf25145a1` — "Update MR-BATCH-001B benchmark carry-forward status"
- Working tree: clean at audit start
- Most recent 10 commits (oldest→newest of the tail): `78e3aaf` (P3-PROSE-DEPTH-1A schema rules) → `df56a35`/`4b106f3` (P3-PROSE-DEPTH-1 close) → `9be3835`, `6c8ef49`, `b7f2256`, `8744b09`, `4b6d59b` (MR-BATCH-001B work) → `6b5d2c8` (register update) → `c465de2` (merge) → `2a8fa64` (HEAD, register carry-forward update)
- `automation_bus/state/work_package_active.json` does not exist at HEAD — no live kernel token, consistent with a clean lifecycle close (last confirmed kernel close: P3-PROSE-DEPTH-1).

## 4. Authoritative governance document map

| Document | Status header | Classification | Confidence |
|---|---|---|---|
| `docs/governance/AUTOMATION_BUS_SOP_v1.3.1.md` | LOCKED | AUTHORITATIVE_CURRENT | HIGH |
| `docs/governance/KNOWLEDGE_BUS_SOP_v1.3.1.md` | APPROVED FOR USE (WITH KNOWN CONSTRAINTS — §§5,10,14,15) | AUTHORITATIVE_CURRENT (self-flagged constrained) | HIGH |
| `docs/governance/KNOWLEDGE_BUS_PASS3_PROMOTION_PROTOCOL_v1.1.md` | DRAFT FOR GOVERNANCE REVIEW | CURRENT_BUT_LIGHTWEIGHT_CONTINUITY_ONLY — companion doc, never formally locked despite being CLAUDE.md-cited as a key authority file | HIGH |
| `docs/governance/healthiq_pre_sop_prompt_scoping_workflow_v0_6.2.md` | current (cited directly by CLAUDE.md §14) | AUTHORITATIVE_CURRENT | HIGH |
| `docs/AUTHORITY_MAP.md` | self-dated "Last updated 2026-06-20", "LIVE" | UNKNOWN_REQUIRES_REVIEW / effectively stale in its governance section (see §5) | HIGH (that it is stale) |
| `docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md` | self-declared "lightweight continuity log... not a substitute for formal audits, ADRs, closure papers, test evidence, or merge records" (lines 5–16) | CURRENT_BUT_LIGHTWEIGHT_CONTINUITY_ONLY | HIGH |
| `automation_bus/latest_cursor_prompt.md` / `latest_prompt_hardening.json` / `latest_cursor_status.json` / `latest_audit_summary.md` | all pinned to work_id P3-PROSE-DEPTH-1, closed 2026-06-29 | FORMAL_AUDIT_OR_CLOSURE_EVIDENCE — but only for P3-PROSE-DEPTH-1; not current for anything after 2026-06-29 | HIGH |
| `sentinel/sentinel_runner.py` / `sentinel/packs/escaped_defects_v1.json` | header: "Phase 1 Sentinel — report-only quality runner... Never modifies product code or governed assets" | AUTHORITATIVE_CURRENT as a mechanism, narrow scope (report-only, not CI-wired) | HIGH |
| `backend/scripts/golden_gate_local.py` | active | AUTHORITATIVE_CURRENT mechanism; runs exactly 3 subprocess checks (architecture validation, baseline tests, three-layer pipeline verification) at lines 166–182; not itself invoked by CI | HIGH |

Documents whose classification is negative (superseded/legacy) are in §5.

## 5. Legacy, superseded and unresolved documents

- **`docs/governance/KNOWLEDGE_BUS_SOP_v1.3.md`** (non-`.1`) — LEGACY_OR_SUPERSEDED, confidence MEDIUM. Header aligns itself to "Automation Bus SOP v1.3" (not v1.3.1) and "Supersedes: v1.2." CLAUDE.md cites only the `.1` file as authoritative. The `.1` file does not explicitly say "supersedes v1.3" (only v1.2), which is a minor internal gap in the newer document's own provenance chain, but version numbering and CLAUDE.md's exclusive citation make v1.3 non-authoritative in practice.
- **`docs/governance/KNOWLEDGE_BUS_PASS3_PROMOTION_PROTOCOL_v1.0.md`** — LEGACY_OR_SUPERSEDED, confidence HIGH. Declares itself companion to the non-`.1` KB SOP, confirming it predates the current stack; v1.1 adds a transition-state section (§10) not present in v1.0.
- **`docs/discussion documents/*`** (v0_1, v0_2 proposal, review_claude, review_claude_v0_2, v0_3) — SPRINT_SPECIFIC_CONTEXT / LEGACY_OR_SUPERSEDED. These are early drafts of the pre-SOP scoping workflow; the authoritative versions (v0.6.1/v0.6.2) now live under `docs/governance/`, not this folder. **`v0_4.md` does not exist anywhere in the repository** (confirmed via directory listing), yet is cited by `docs/AUTHORITY_MAP.md` as authoritative, and the same stale path is also referenced inside `AUTOMATION_BUS_SOP_v1.3.1.md` §10 for pipeline-advisory workflow definition. This is a dangling reference inside a LOCKED document.
- **`docs/AUTHORITY_MAP.md` (governance/control-plane section specifically)** — UNKNOWN_REQUIRES_REVIEW, effectively stale: names the superseded KB SOP as authoritative, omits both Pass-3 protocol versions and the v0.6.x pre-SOP workflow entirely, and cites a non-existent `v0_4.md`. **This is an unresolved authority conflict that should go to Head of Architecture adjudication** — the rest of AUTHORITY_MAP.md (non-governance sections) was out of this audit's direct verification scope and should not be assumed accurate by extension.
- **`docs/audit-papers/*` inventory**: 169 markdown files exist. Dedicated closure papers exist for early/mid-programme sprints (BATCH2-*, ARCH-COMPLETION-1/2/3, ARCH-RT-5*, DHEA-*, CONTEXT-*, WAVE1-*, PROSE-INVENTORY-1 dated 2026-06-29, CTRL-01 dated 2026-06-22). **No dedicated audit-papers/ entry exists for P1-13 through P1-26, P2-1, P2-2+P2-3, P2-4, P3-PROSE-DEPTH-1, P3-PROSE-DEPTH-1A, or MR-BATCH-001B** (confirmed via targeted grep across the audit-papers filename list — zero matches for these work_ids). This is a real evidentiary gap for roughly the last third of the programme's sprint history — see §6 and §13.

## 6. Current sprint-state and closure evidence

- Last kernel-confirmed lifecycle close: **P3-PROSE-DEPTH-1**, 2026-06-29T19:09:11Z, gate_status PASS, 22/22 acceptance criteria (`automation_bus/latest_audit_summary.md`; `automation_bus/latest_cursor_status.json`, note: this status file's `bus_version` field reads `"1.2"` even though the operative SOP is v1.3.1 — a minor, unexplained field drift, UNKNOWN_REQUIRES_REVIEW).
- `automation_bus/latest_audit_summary.md` for P3-PROSE-DEPTH-1 sets `pipeline_advisory_trigger: true` and recommends MR-BATCH-001B candidate prose generation as next — consistent with what actually happened next in git history.
- **P3-PROSE-DEPTH-1A and MR-BATCH-001B have no corresponding `automation_bus/latest_*` artefacts.** No hardening JSON, no cursor status, no audit summary exists for either work_id at HEAD. Git log confirms neither shows the `chore(bus): <work_id> kernel IN_PROGRESS/COMPLETE status` commit pair that every other properly-lifecycled sprint (P2-4, P2-2+P2-3, P3-PROSE-DEPTH-1 itself) exhibits. VERIFIED_FACT: MR-BATCH-001B's own commits and files touched are confined to `docs/sprints/beta_readiness/` and `backend/tests/` (never `backend/core`, `backend/ssot`, or `knowledge_bus/packages/`), so the *practical* risk of this gap is low for this specific case — but it does mean this work was not run through the documented Stage 0–5 kernel process, and the SOP's own Docs-Only Bypass (defined for `/docs/` changes) would not, on a strict reading, extend to the `backend/tests/` files also touched. This should be treated as an open governance question, not a resolved one.
- Build register's own final entries (`docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md:770-808`) explicitly recommend `SPRINT-BUILD-PLAN-AUDIT-1` — i.e., an audit exactly like this one — as the next sprint, and flag "Risk that future agents misread MR-BATCH-001B as promotion-ready unless benchmark-only status is explicit" (line 793) as a live concern.

## 7. Current maturity by programme block

| Block | Claimed status (register) | Repository evidence | Verdict |
|---|---|---|---|
| Core systems (P1-x) | Complete (with P1-4 marked Blocked) | Early sprints have dedicated audit-papers/ closure; P1-4 explicitly still Blocked in the register | BUILT_AND_MERGED for most P1 items; P1-4 = BLOCKED (register's own label, not contradicted) |
| Subsystems | Complete | WAVE1-* audit papers exist and are substantive (subsystem visibility, marker role investigations) | BUILT_AND_MERGED + audited |
| Layer B intelligence/prose/clinician report | Complete through P3-PROSE-DEPTH-1; P3-PROSE-DEPTH-1A/MR-BATCH-001B "Complete" (register only) | Root-cause compiler is a hybrid of legacy YAML (majority) + one compiled-hypothesis exception (`signal_vitamin_d_low.yaml`); card evidence is schema-validated, not hardcoded; prose manifest explicitly flags `candidate_only_status: true`, `medical_content_promoted_to_approved: false` | BUILT_AND_MERGED + RUNTIME_WIRED for root-cause/card-evidence machinery; CANDIDATE_ONLY for MR-BATCH-001B prose specifically; no independent audit paper for the last 3 entries in this block |
| Layer C presentation and Gemini | P4-1 "CEO-gated" per register carry-forward note | `orchestrator.py` builds `InsightGraph` deterministically before any Gemini call; `GeminiClient` is a thin translation wrapper with no scoring/ranking logic | RUNTIME_WIRED as translation-only, confirms Layer B/C separation holds in code |
| UX and results page | Complete | ~19 real components under `frontend/app/components/results/` plus `frontend/app/(app)/results/page.tsx`; substantive, non-trivial | BUILT_AND_MERGED + RUNTIME_WIRED |
| Safety and provenance | Claimed addressed in various P1/P2 entries | Only `source_spec_id`/`activation_key` provenance mechanics were directly verified in code; no single "safety/provenance module" was located in the time available | PARTIAL — UNKNOWN_REQUIRES_REVIEW for a dedicated provenance subsystem beyond activation identity |
| Auditability and replay | Claimed via golden-run artefacts | `replay_manifest.json` artefacts exist under `backend/artifacts/arbitration_runs/sprint10_*/...` and are also produced/verified by CI (`ci-golden-160` job checks for `replay_manifest.json` among required golden snapshot files) | RUNTIME_WIRED for golden-run replay artefacts specifically; broader "auditability" claims beyond this were not independently traced |
| Phenotype and beta-validation test estate | Complete | Real test files confirmed: `backend/tests/unit/test_phenotype_suite_v1.py`, `test_validate_phenotype_map.py`, fixtures at `backend/tests/fixtures/panels/phenotypes/phenotype_expectations_v1.yaml`; 309 total files under `backend/tests/` | BUILT_AND_MERGED + TEST_ONLY (by definition of a test estate) |

## 8. Day-one architecture verification

- **Explicit provenance at the call site (VERIFIED_FACT):** `backend/core/analytics/signal_evaluator.py:57-59` — `SignalRegistry._load()` calls `resolve_activation_identity(...)`, returning `(activation_key, source_spec_id, package_id)` explicitly per signal; attached at line 70. Deeper internals of `resolve_activation_identity` (in `backend/core/knowledge/signal_activation_identity_v1.py`) were not read line-by-line — whether resolution itself ever falls back to inference is UNKNOWN_REQUIRES_REVIEW.
- **Fail-closed activation_key collision (VERIFIED_FACT):** `signal_evaluator.py:61-66` raises `ValueError("Duplicate activation_key collision: ...")` at load time on collision — real, not just test-asserted behaviour.
- **Multi-frame activation (REASONABLE_INFERENCE, design-only):** `docs/architecture/MED-FRAME-1_signal_family_contextual_frame_architecture.md` defines `activation_key = signal_id::research_spec_id` and requires 1:1 frame-to-research_spec_id mapping "unless an explicit multi-frame package split is approved" (line 112). No runtime code implementing multi-frame *selection/collapse* logic (beyond the uniqueness check above) was located. Treat as architecturally scoped but not demonstrated as runtime-exercised.
- **PSI (Promoted Signal Intelligence) — deferred, not runtime-wired (VERIFIED_FACT, independently re-checked):** `docs/audit-papers/ARCH-RT-5E...` (and companion `ARCH-RT-5_M4_psi_runtime_wiring_audit.md`) claim PSI is a non-launch-blocker with no Intelligence Core consumer. Independently re-verified against current HEAD: `grep "promoted_signal_intelligence|load_promoted_signal" backend/core/pipeline/orchestrator.py` returns no matches. The prior audit's claim still holds against current code — this was not simply inherited.
- **Root-cause authority — hybrid, legacy-dominant (VERIFIED_FACT):** `backend/core/knowledge/root_cause_registry_v1.py:14,27-60` — comment states registry "Preserves legacy registration order and loaders"; ~15+ `RootCauseTargetSpec` entries point at legacy `*_hypotheses_v1.yaml` loaders. Only one compiled-hypothesis artefact exists (`knowledge_bus/compiled/hypotheses/signal_vitamin_d_low.yaml`). `root_cause_compiler_v1.py:32-45` imports both the legacy registry and the compiled-hypothesis path — runtime root-cause reasoning is genuinely a hybrid, legacy-majority system, not a fully-compiled one. This reconfirms (rather than merely repeats) the prior ARCH-RT-5E/M3 characterization against current source.
- **Card evidence — schema-validated, not hardcoded (VERIFIED_FACT):** `backend/core/knowledge/health_system_card_evidence.py` — `validate_card_evidence_payload()` (line 145) is fail-closed against `health_system_card_evidence_schema_v1`; `load_card_evidence_artefact()` (line 293) validates compiled YAML before parsing (lines 298-299). No hardcoded card content found in this file.
- **Frontend render-only boundary — PARTIALLY VERIFIED:** grep of `frontend/app/components/results/` for threshold/scoring keywords surfaced 6 files (`PrimaryFindingAndWhy.tsx`, `ResultsHeroBlocks.tsx`, `ClinicianReportRenderer.tsx`, `SystemUnderstandingSection.tsx`, `LayerCInsightSection.tsx`, `RootCauseEvidenceSummary.tsx`). Their content was **not** read to confirm the matches are display formatting rather than clinical logic — flagged as UNKNOWN_REQUIRES_REVIEW, a good candidate for a targeted follow-up check before any beta go-live sign-off.
- **Compile manifests:** not independently re-verified against current file paths in this pass beyond the PSI and root-cause checks above; the prior ARCH-RT-5D compile-manifest-refresh claims should be re-checked directly if a decision depends on them (UNKNOWN_REQUIRES_REVIEW for manifest-path resolution specifically).

## 9. Layer B, prose and reasoning maturity

- **Prose candidate/approved status gate (VERIFIED_FACT):** `docs/sprints/beta_readiness/P3-PROSE-DEPTH-1_manifest.yaml:31-32` — explicit fields `medical_content_promoted_to_approved: false`, `candidate_only_status: true`. This is a real, machine-readable status gate, not just prose in a document.
- **MR-BATCH-001B candidate assets carry the same discipline (VERIFIED_FACT):** `docs/sprints/beta_readiness/MR-BATCH-001B_candidate_prose_assets.yaml` header declares `review_status_all: CANDIDATE`, `authored_by_all: MR_LLM_CANDIDATE`, `candidate_only: true` across all 69 assets (3270 lines); none are `APPROVED`.
- **Modifier binding / frame routing — deferred (per register), not independently traced to selection code** in this pass. The register itself states (MR-BATCH-001B carry-forwards): "Modifier binding and frame routing deferred; P4-1 Gemini remains CEO-gated." This self-reported deferral is consistent with the absence of any production consumer of the candidate pack (see §12), but the *general* (non-MR-BATCH) prose-selection routing code was not independently read in this pass — UNKNOWN_REQUIRES_REVIEW for whether currently-approved prose selection is frame-bound versus looser marker/family-bound.
- **No contradiction found** between MR-BATCH-001B's claimed non-authoritative status and its actual code/asset treatment (see §12 for full detail).

## 10. Layer C, Gemini and frontend boundary

- **Gemini is strictly downstream of deterministic Layer B output (VERIFIED_FACT):** `backend/core/pipeline/orchestrator.py:794-819` — `insight_graph` is built via deterministic `build_insight_graph_v1(...)` *before* `self.insight_synthesizer.synthesize_insights(context=context, insight_graph=insight_graph, ...)` is called. Gemini receives an already-fully-structured `InsightGraph`; it does not participate in building it.
- **`GeminiClient` has no scoring/ranking logic (VERIFIED_FACT):** `backend/core/insights/gemini_client.py:1,31-47` — thin `google.generativeai` wrapper exposing `generate()`; `backend/core/insights/synthesis.py:19,413-418` falls back to `MockLLMClient` when Gemini isn't configured, confirming the pipeline does not require Gemini to produce a complete deterministic result.
- **CI explicitly asserts NO-LLM behaviour on golden runs (VERIFIED_FACT, independently found):** `.github/workflows/ci.yml` "Golden Gate" job sets `HEALTHIQ_ENABLE_LLM: "0"` and has a dedicated "Enforce NO-LLM logs" step that fails the build if `"Creating GeminiClient"` appears in the golden runner log — a real, mechanically-enforced guard that Layer B's golden-panel path runs deterministically without Gemini.
- **Frontend inference risk — unresolved:** as noted in §8, six results-page components matched threshold/scoring greps but were not read for actual logic content. This is the single most actionable follow-up item before any claim of a fully clean render-only frontend boundary can be made with HIGH confidence.

## 11. Recent sprint verification

| Work_id | Hardening artefact | Audit-papers/ closure | Kernel commit pair (`chore(bus):...`) | Code/asset evidence | Still active at HEAD |
|---|---|---|---|---|---|
| P2-2+P2-3 | Yes (`ee13717`) | Not found | Yes | `feat(P2-2+P2-3)` commit present | Presumed yes (no evidence of reversal) |
| P2-4 | Yes (`f150b09`) | Not found | Yes | `feat(P2-4)` NarrativePayloadV1 commit present | Presumed yes |
| P3-PROSE-DEPTH-1 | Yes (`7fd2ddf`) — this is the current `automation_bus/latest_prompt_hardening.json` | Yes — `docs/audit-papers/PROSE-INVENTORY-1...` dated 2026-06-29 (title suggests related, not confirmed identical scope) | Yes | Prose schema/coverage-matrix commit present | Yes — this is the pinned "latest" state |
| P3-PROSE-DEPTH-1A | Not found | Not found | **No** — no kernel commit pair located | `78e3aaf` schema-rules commit exists | UNKNOWN — code exists, governance trail does not |
| MR-BATCH-001B | Not found | Not found | **No** | Full commit + asset trail present (§12) | Yes, but explicitly non-authoritative by design |

**Contradiction check:** the register claims all of the above as "Complete." For P2-x and P3-PROSE-DEPTH-1, hardening artefacts and kernel commit pairs corroborate this. For P3-PROSE-DEPTH-1A and MR-BATCH-001B, "Complete" rests solely on the register's own self-entry plus (for MR-BATCH-001B) a separate self-authored completion doc (`docs/sprints/beta_readiness/MR-BATCH-001B_test_import_completion.md`) — no independent audit trail exists for either. This is not evidence that the work is wrong (MR-BATCH-001B's own isolation evidence is strong, see §12), but it is a process gap: the documented Stage 0–5 lifecycle was not demonstrably followed for the two most recent work items.

## 12. MR-BATCH-001B classification

**VERIFIED_FACT — repository evidence fully supports the claimed classification**: Round 1 benchmark/test fixture only; not medically approved; not promoted; not production-wired.

- **File inventory (exhaustive):** `docs/sprints/beta_readiness/MR-BATCH-001B_candidate_prose_assets.yaml` (3270 lines, 69 assets), `docs/sprints/beta_readiness/MR-BATCH-001B_candidate_prose_test_output.md`, `docs/sprints/beta_readiness/MR-BATCH-001B_test_import_completion.md`, `backend/tests/support/mr_candidate_prose_test_v1.py`, `backend/tests/unit/test_mr_batch_001b_candidate_prose_test_import.py`, and the register entry itself. `git log --name-only` across all five MR-BATCH-001B commits (9be3835, 6c8ef49, b7f2256, 8744b09, 4b6d59b) plus the HEAD carry-forward commit (2a8fa64) touches only `docs/sprints/beta_readiness/` and `backend/tests/` — never `backend/core`, `backend/ssot`, or `knowledge_bus/packages/`.
- **Runtime guard (VERIFIED_FACT, file:line):** `backend/tests/support/mr_candidate_prose_test_v1.py:1-8` docstring: "Loads candidate prose assets... for test/demo composition. Must NOT be imported from production runtime paths." Lines 54-59: `_require_candidate_test_mode()` raises `RuntimeError` unless `candidate_test_mode=True` is explicitly passed. Lines 300-317: `validate_pack_governance()` fails any asset whose `review_status != "CANDIDATE"`.
- **Isolation test, not integration test (VERIFIED_FACT):** `backend/tests/unit/test_mr_batch_001b_candidate_prose_test_import.py:10-12` imports `retail_explainer_assembly_v1`, `orchestrator`, and `narrative_runtime_policy` only to assert they do **not** consume the candidate pack — the opposite of wiring it in.
- **No promotion evidence exists:** no `knowledge_bus/packages/*mr*batch*` directory; no `backend/core/**` reference to the candidate loader or any `MrBatch001b*` symbol (zero matches).
- **Register carry-forward language (`BUILD_DELIVERABLE_REGISTER.md:770-796`)** explicitly states the intended classification, including the self-aware risk: "Risk that future agents misread MR-BATCH-001B as promotion-ready unless benchmark-only status is explicit."
- **Note on skill file location:** the skill governing this work lives at `.cursor/skills/mr-batch-research/SKILL.md`, not `.claude/skills/mr-batch-research/SKILL.md` as recorded in the auditor's own standing memory file — that memory reference is stale and should be corrected.
- **The one open item is process, not content:** as noted in §6/§11, this work did not go through the documented Automation Bus kernel lifecycle (no hardening JSON, no audit summary, no kernel commit pair), even though its content-level isolation is exemplary. This should be flagged, not waived, given the SOP's own Docs-Only Bypass would not obviously cover the `backend/tests/` files also touched.

## 13. Documentation-versus-code mismatches

1. `docs/AUTHORITY_MAP.md` names a superseded KB SOP version and cites a non-existent pre-SOP scoping document (`v0_4.md`) — see §5.
2. `AUTOMATION_BUS_SOP_v1.3.1.md` §10 itself references the same non-existent `v0_4.md` path — a stale reference inside a LOCKED document.
3. `automation_bus/latest_cursor_status.json` reports `bus_version: "1.2"` while the operative SOP is v1.3.1 — unexplained field drift (UNKNOWN_REQUIRES_REVIEW, likely a copy-paste artefact rather than a real version mismatch, but not confirmed).
4. P3-PROSE-DEPTH-1A and MR-BATCH-001B are marked "Complete" in the register with no corresponding kernel lifecycle artefacts — a documented-process-versus-actual-process mismatch (§6, §11).
5. The last ~13 register entries have no independent `docs/audit-papers/` closure document, despite earlier programme sprints consistently receiving one — a coverage mismatch, not a content-accuracy problem per se (§5, §6).
6. `golden_gate_local.py`'s three checks are not run in full by any CI workflow; only one of the three (`run_architecture_validation_gate.py`) is independently wired into `.github/workflows/architecture-gate.yml`. Anyone assuming "the gate runs in CI" would be partially wrong — the full local gate is a manual/local tool.

## 14. Stale or superseded build-register recommendations

- No build-register recommendation was found to be already superseded by later work, other than the general observation that the register's own most recent recommendation (`SPRINT-BUILD-PLAN-AUDIT-1`) is what this audit itself now discharges.
- The Knowledge Bus Pass-3 Promotion Protocol remains in DRAFT status despite being listed in CLAUDE.md as a "key authority file" — this is not stale, but it is a document whose authority level does not match how it is referenced elsewhere, and should be resolved (either lock it or stop citing it as authoritative).

## 15. Active blockers before controlled beta

1. **Governance-trail gap for P3-PROSE-DEPTH-1A and MR-BATCH-001B** — no hardening/audit evidence exists; should be closed retroactively or explicitly waived by Head of Architecture before further work builds on top of this baseline.
2. **AUTHORITY_MAP.md governance-section staleness** — must be corrected before it is relied upon for any future sprint's document-authority lookups.
3. **Frontend render-only boundary not fully confirmed** — six components flagged by keyword grep were not read for actual logic; this should be closed before any beta go-live claim of "frontend has no medical inference."
4. **Knowledge Bus SOP v1.3.1 self-declared gaps** (package lifecycle controller non-authoritative for `pkg_*` IDs; behavioural validation categories "Required (Not Yet Implemented)"; Automation Bus does not enforce Knowledge Bus readiness) remain open per the SOP's own text — these are not new findings, but they are still live blockers, not resolved history.
5. **P1-4 remains Blocked** per the register's own label — not independently re-investigated in this pass; carried forward as-is.
6. **Multi-frame activation and prose frame-routing** are architecturally specified but not demonstrated as runtime-exercised/enforced in this pass — worth a dedicated verification sprint if multi-frame content is planned before beta.

## 16. Candidate next work packages

These are plausible candidates only. No selection is made here.

- **Governance-trail backfill for P3-PROSE-DEPTH-1A / MR-BATCH-001B.** Problem: no hardening/audit artefacts exist for the two most recent work items (§6, §11). Why it matters: sets precedent for whether Automation Bus lifecycle is optional for test/doc-only work. Dependencies: Head of Architecture ruling on whether Docs-Only Bypass should be read to cover `backend/tests/`. Risk class: LOW (no production code involved) but governance-significant. Medical review: not required. Blocked by unresolved authority decision: yes (bypass-scope interpretation).
- **AUTHORITY_MAP.md correction pass.** Problem: stale governance-section references (§5, §13). Why it matters: AUTHORITY_MAP.md is meant to be the canonical index; its staleness risks propagating wrong citations into future sprint prompts. Dependencies: none beyond confirming the rest of the document's other sections for similar drift. Risk class: LOW (docs-only). Medical review: not required. Blocked: no.
- **Frontend results-component logic audit.** Problem: 6 files flagged by keyword grep, unread (§8, §10, §15). Why it matters: a genuine render-only boundary is a stated architectural non-negotiable (CLAUDE.md §3). Dependencies: none. Risk class: STANDARD if any logic needs to move server-side. Medical review: possibly, if clinical thresholds are found client-side. Blocked: no.
- **Knowledge Bus SOP §5/§10/§14/§15 gap closure** (package lifecycle controller reconciliation for `pkg_*`, behavioural validation implementation, cross-bus enforcement). Problem: self-declared in the locked SOP itself. Why it matters: currently the validator is "the only trusted promotion gate" per the SOP's own words — a single point of enforcement. Dependencies: likely HIGH risk / Intelligence Core adjacent depending on scope. Risk class: potentially HIGH. Medical review: possibly for behavioural validation categories (contradictory signal detection etc.). Blocked: no, but scoping needed first.
- **Round 2 medical prose pipeline design**, explicitly flagged by the register itself as needing "a new primary research pipeline and a different primary research LLM" before any MR-BATCH successor is attempted. Why it matters: MR-BATCH-001B's own carry-forwards state Claude Code / current LLM research execution "is not trusted as a scalable medical research pipeline" (encoding corruption, oversized run, salvage requirement). Dependencies: LLM/tooling decision outside this audit's scope. Risk class: HIGH (medical content). Medical review: required. Blocked: yes, by an unresolved tooling/process decision.

## 17. Recommended immediate next action

Convene a Head of Architecture adjudication on two specific, narrow items before any further sprint planning: (1) whether the P3-PROSE-DEPTH-1A / MR-BATCH-001B governance-trail gap requires retroactive hardening/audit artefacts or an explicit documented waiver, and (2) correction of `docs/AUTHORITY_MAP.md`'s governance/control-plane section (wrong KB SOP version cited, missing Pass-3 protocol entries, dangling `v0_4.md` reference — the latter also needs fixing inside the locked Automation Bus SOP itself). Both are small, bounded, non-implementation actions that remove live authority ambiguity before the next real work package is selected. This is not an implementation prompt and does not select the next sprint.

## 18. Evidence index

- `docs/governance/AUTOMATION_BUS_SOP_v1.3.1.md`, `KNOWLEDGE_BUS_SOP_v1.3.1.md` (and superseded `v1.3.md`), `KNOWLEDGE_BUS_PASS3_PROMOTION_PROTOCOL_v1.1.md` (and superseded `v1.0.md`), `healthiq_pre_sop_prompt_scoping_workflow_v0_6.1.md`/`v0_6.2.md`
- `docs/AUTHORITY_MAP.md`
- `docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md` (lines 5-16, 760-833)
- `docs/sprints/beta_readiness/P3-PROSE-DEPTH-1_manifest.yaml:31-32`
- `docs/sprints/beta_readiness/MR-BATCH-001B_candidate_prose_assets.yaml`, `MR-BATCH-001B_test_import_completion.md`, `MR-BATCH-001B_candidate_prose_test_output.md`
- `automation_bus/latest_cursor_prompt.md`, `latest_prompt_hardening.json`, `latest_cursor_status.json`, `latest_audit_summary.md`
- `automation_bus/state/work_package_active.json` (absent)
- `backend/scripts/golden_gate_local.py:166-182`, `run_work_package.py`
- `sentinel/sentinel_runner.py`, `sentinel/packs/escaped_defects_v1.json`
- `.github/workflows/architecture-gate.yml`, `ci.yml` (Golden Gate job, NO-LLM enforcement step), `golden_gate.yml`, `validate.yml`
- `backend/core/analytics/signal_evaluator.py:57-70`
- `backend/core/knowledge/root_cause_registry_v1.py:14,27-60`, `root_cause_compiler_v1.py:32-45`
- `backend/core/knowledge/health_system_card_evidence.py:145,293-299`
- `backend/core/pipeline/orchestrator.py:794-819`
- `backend/core/insights/synthesis.py:19,413-418`, `gemini_client.py:1,31-47`
- `backend/tests/support/mr_candidate_prose_test_v1.py:1-8,54-59,300-317`
- `backend/tests/unit/test_mr_batch_001b_candidate_prose_test_import.py:10-12`
- `.cursor/skills/mr-batch-research/SKILL.md`
- `docs/architecture/MED-FRAME-1_signal_family_contextual_frame_architecture.md:112`
- `docs/audit-papers/ARCH-RT-5E_psi_runtime_wiring_decision_audit.md`, `ARCH-RT-5_M4_psi_runtime_wiring_audit.md` (claims independently re-checked against current orchestrator.py, not inherited)
- `docs/audit-papers/*` inventory (169 files; gap for P1-13→MR-BATCH-001B noted)

## Appendix A — Governance document classification table

See §4 and §5 tables above (combined here for completeness):

| Path | Classification | Confidence |
|---|---|---|
| `AUTOMATION_BUS_SOP_v1.3.1.md` | AUTHORITATIVE_CURRENT | HIGH |
| `KNOWLEDGE_BUS_SOP_v1.3.1.md` | AUTHORITATIVE_CURRENT (constrained) | HIGH |
| `KNOWLEDGE_BUS_SOP_v1.3.md` | LEGACY_OR_SUPERSEDED | MEDIUM |
| `KNOWLEDGE_BUS_PASS3_PROMOTION_PROTOCOL_v1.1.md` | CURRENT_BUT_LIGHTWEIGHT_CONTINUITY_ONLY (DRAFT) | HIGH |
| `KNOWLEDGE_BUS_PASS3_PROMOTION_PROTOCOL_v1.0.md` | LEGACY_OR_SUPERSEDED | HIGH |
| `docs/AUTHORITY_MAP.md` (governance section) | UNKNOWN_REQUIRES_REVIEW / stale | HIGH |
| `docs/discussion documents/*` (pre-SOP drafts) | LEGACY_OR_SUPERSEDED | HIGH |
| `BUILD_DELIVERABLE_REGISTER.md` | CURRENT_BUT_LIGHTWEIGHT_CONTINUITY_ONLY | HIGH |
| `automation_bus/latest_*` (four files) | FORMAL_AUDIT_OR_CLOSURE_EVIDENCE for P3-PROSE-DEPTH-1 only | HIGH |
| `sentinel/*` | AUTHORITATIVE_CURRENT, narrow/report-only | HIGH |
| `golden_gate_local.py` | AUTHORITATIVE_CURRENT mechanism, not CI-invoked in full | HIGH |

## Appendix B — Capability maturity matrix

| Capability | State(s) |
|---|---|
| Signal activation identity / activation_key uniqueness | BUILT_AND_MERGED + RUNTIME_WIRED |
| Multi-frame activation | DOCS_ONLY (design spec) — not shown RUNTIME_WIRED |
| PSI (Promoted Signal Intelligence) | BUILT (compiled artefact exists) + BLOCKED/CANDIDATE_ONLY — deferred, no Intelligence Core consumer |
| Card evidence generation/validation | BUILT_AND_MERGED + RUNTIME_WIRED |
| Root-cause compiler | BUILT_AND_MERGED + RUNTIME_WIRED, but hybrid: legacy YAML majority + 1 compiled exception |
| Gemini / Layer C translation | BUILT_AND_MERGED + RUNTIME_WIRED + PRODUCTION_ACTIVE (optional/downstream, NO-LLM CI-enforced on golden path) |
| Frontend results UI | BUILT_AND_MERGED + RUNTIME_WIRED |
| Frontend render-only boundary (no client-side clinical logic) | UNKNOWN_REQUIRES_REVIEW — not confirmed for 6 flagged files |
| MR-BATCH-001B candidate prose | CANDIDATE_ONLY + TEST_ONLY, explicitly not RUNTIME_WIRED, not PRODUCTION_ACTIVE (by design, verified) |
| P3-PROSE-DEPTH-1 prose schema/depth work | BUILT_AND_MERGED, hardened, audited (kernel-confirmed) |
| P3-PROSE-DEPTH-1A | BUILT (code exists) but governance-trail STALE/absent |
| Automation Bus kernel gate (golden_gate_local.py full 3-check set) | BUILT_AND_MERGED, not CI-invoked as a whole (only 1 of 3 checks independently CI-wired) |
| Sentinel | BUILT_AND_MERGED, report-only, NOT CI-wired |
| Knowledge Bus package lifecycle controller (`pkg_*` support) | BUILT but SOP self-declares it non-authoritative for current naming convention; validator is the real gate |
| Knowledge Bus behavioural validation (contradiction/cascade/dominance detection) | NOT_FOUND / DOCS_ONLY — SOP itself states "Required (Not Yet Implemented)" |

## Appendix C — Recent sprint verification table

See §11 table above.

## Appendix D — Commands and searches executed

Representative commands (full detail distributed across four parallel research passes plus lead-auditor spot checks):
- `git log --oneline -30`, `git status`, `git branch -a`, `git rev-parse HEAD`
- `git show --stat` on 9be3835, 6c8ef49, b7f2256, 4b6d59b, 2a8fa64
- `git log --name-only` across MR-BATCH-001B commits
- Glob: `docs/governance/*.md`, `docs/audit-papers/*.md`, `docs/sprints/**`, `knowledge_bus/**`
- Grep: `activation_key`, `source_spec_id`, `promoted_signal_intelligence|load_promoted_signal`, `MR-BATCH-001B|MR_BATCH_001B|mr_candidate_prose_test_v1|candidate_test_mode`, `sentinel|golden_gate_local|run_baseline_tests|verify_three_layer_pipeline` (against `.github/workflows/*.yml`), threshold/scoring keywords against `frontend/app/components/results/`
- Direct Read of: SOPs, Pass-3 protocols, AUTHORITY_MAP.md, BUILD_DELIVERABLE_REGISTER.md (targeted ranges), `automation_bus/latest_*`, `automation_bus/state/work_package_active.json` (confirmed absent), `golden_gate_local.py`, `sentinel_runner.py`, `signal_evaluator.py`, `root_cause_registry_v1.py`, `root_cause_compiler_v1.py`, `health_system_card_evidence.py`, `orchestrator.py`, `synthesis.py`, `gemini_client.py`, `mr_candidate_prose_test_v1.py`, `test_mr_batch_001b_candidate_prose_test_import.py`, `.cursor/skills/mr-batch-research/SKILL.md`, `.github/workflows/architecture-gate.yml`, `ci.yml`, `golden_gate.yml`, `validate.yml`
