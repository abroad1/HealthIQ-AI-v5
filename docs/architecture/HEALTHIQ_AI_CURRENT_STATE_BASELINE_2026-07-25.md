# HealthIQ AI — Current State Baseline (2026-07-25)

**Status:** AUTHORITATIVE maturity baseline for future Stage 0 planning until superseded by a later approved baseline.  
**Work package:** ARCH-GOV-BASELINE-1  
**Nature:** Verified current reality — not historical aspiration. No unsupported completion percentages.

---

## 1. Repository baseline

| Field | Value |
|---|---|
| Audit date | 2026-07-25 |
| Branch at independent audit | `main` |
| HEAD used for independent audit verification | `2a8fa64ed791cabc8ae478113b96cefdf25145a1` |
| Sprint branch (this baseline published on) | `feature/arch-gov-baseline-1-programme-baseline-governance-reset` |
| Source audits | `docs/audit-papers/CURSOR_sprint_governance_and_codebase_maturity_audit.md`; `docs/audit-papers/CLAUDE_CODE_sprint_governance_and_codebase_maturity_audit.md`; `docs/audit-papers/CURSOR_executable_codebase_and_runtime_reality_audit.md`; `docs/audit-papers/CLAUDE_CODE_independent_executable_architecture_assurance_audit.md` |

---

## 2. Authoritative governance stack

| Document | Classification |
|---|---|
| `docs/governance/AUTOMATION_BUS_SOP_v1.3.1.md` | AUTHORITATIVE (LOCKED) |
| `docs/governance/KNOWLEDGE_BUS_SOP_v1.3.1.md` | AUTHORITATIVE (LOCKED) |
| `docs/governance/KNOWLEDGE_BUS_PASS3_PROMOTION_PROTOCOL_v1.1.md` | SUPPORTING (DRAFT) — operative companion pending governance ratification; not silently APPROVED |
| `docs/governance/healthiq_pre_sop_prompt_scoping_workflow_v0_6.2.md` | AUTHORITATIVE pre-SOP workflow |
| `AGENTS.md` | AUTHORITATIVE agent operating map |
| `docs/AUTHORITY_MAP.md` | AUTHORITATIVE document-authority index (reconciled 2026-07-25) |

Legacy / superseded (do not use as current authority): Knowledge Bus SOP v1.3 on disk; missing pre-SOP v0_4 path previously cited in AUTHORITY_MAP; `docs/SPRINT_STATUS.md` (historical only).

---

## 3. Current programme continuity stack

| Document | Role |
|---|---|
| `docs/architecture/HEALTHIQ_AI_CURRENT_STATE_BASELINE_2026-07-25.md` | This document — maturity baseline |
| `docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md` | Lightweight continuity log only |
| `docs/sprints/healthiq_day_one_architecture_rework_sprint_plan_FINAL_updated.md` | Current day-one carry-forward plan |
| `docs/sprints/healthiq_day_one_architecture_rework_sprint_plan_FINAL.md` | SUPERSEDED earlier FINAL variant |
| `docs/strategy/beta_readiness/HEALTHIQ_AI_BETA_READINESS_DEFINITIVE_STRATEGY_FINAL_2026-06-20.md` | Programme strategy baseline (aspirational claims superseded where this baseline conflicts) |
| Four 2026-07-25 audit papers under `docs/audit-papers/` | Evidence only — not ongoing authority |

---

## 4. Current production authorities (verified)

- **Compiled card evidence** is active Wave 1 subsystem authority (`knowledge_bus/compiled/estate_index_v1.yaml`; empty legacy hard-coded subsystem lists).
- **Hard-coded card evidence is not active.**
- **Activation-key identity** (`signal_id::source_spec_id`) is active at signal registry load.
- **Gemini narrative** is deny-default / non-authoritative for analytical reasoning.
- **PSI** (`load_promoted_signal_intelligence`) is built but intentionally **not** on the launch analysis path.
- **WHY authority is dual:** one compiled hypothesis (`signal_vitamin_d_low`) plus legacy root-cause YAML targets.

---

## 5. Maturity by eight beta-readiness blocks

Summary labels are qualitative, evidence-backed, and **not** percentage scores.

| Block | Current posture | Notes |
|---|---|---|
| 1 Core health systems model | Materially advanced | Six Wave 1 domains backend-assembled and DTO-exposed; only three are frontend-rendered to consumers (see §14) |
| 2 Subsystems and depth | Materially advanced | 10 estate-indexed compiled cards |
| 3 Layer B intelligence/prose | Partial | Production prose/registries exist; frame routing and modifier binding not delivered |
| 4 Layer C / Gemini | Gated | Gemini non-authoritative; deny-default narrative |
| 5 Provenance / research-to-runtime | Partial | Compile manifests exist; **zero** explicit `source_spec_id` across scanned package estate at audit baseline |
| 6 PSI | Built-not-wired | Intentionally unwired from launch path |
| 7 Governance / Automation Bus | Operative with gaps | SOP stack live; stale continuity docs reconciled by ARCH-GOV-BASELINE-1 |
| 8 Controlled beta readiness | **Not authorised** | Remaining blockers listed in §10 |

---

## 6. Verified delivered capabilities

- Six Wave 1 domains backend-assembled and DTO-exposed: `wave1_cardiovascular`, `wave1_blood_sugar`, `wave1_liver`, `wave1_kidney`, `wave1_blood_iron_oxygen`, `wave1_thyroid`. Frontend rendering is confirmed for only the first three; `wave1_kidney`, `wave1_blood_iron_oxygen`, and `wave1_thyroid` do not appear in `Wave1DomainCards.tsx` or any other frontend component — see §14 for the full backend/DTO/consumer-visibility distinction and the verified thyroid firing defect.
- Compiled card evidence active; hard-coded card evidence inactive.
- Activation-key identity active at registry load.
- Day-one architecture / launch-estate / architecture-validation gates PASS on pre-change baseline (ARCH-GOV-BASELINE-1 Phase 1).
- Retail explainer SSOT registry present for production biomarkers.
- Deterministic golden / NO-LLM enforcement paths exist (local golden runner + `golden_gate.yml`).

---

## 7. Documented-but-undelivered capabilities

- End-to-end multi-frame preservation across consumers (interaction builder, root-cause, report maps still collapse or first-match on `signal_id` in places).
- Frame routing and modifier binding for prose depth (P3 deferred).
- Formal Pass 3 promotion protocol ratification (still DRAFT).
- Controlled beta authorisation.

---

## 8. Built-but-unwired capabilities

- Promoted Signal Intelligence (PSI) packages and loaders — intentionally unwired from launch analysis.
- Gemini narrative synthesis — present but deny-default / non-authoritative for analytical output.

---

## 9. Test-only and candidate-only assets

- **MR-BATCH-001B:** 69-asset CANDIDATE pack under sprint docs; loaded only via `candidate_test_mode=True` test support; **benchmark/test-only**; **not** medically approved; **not** promotable; **not** for production runtime.
- Candidate prose assets must not proceed to medical review as a promotion route; useful only as Round 1 benchmark evidence for future Round 2 pipeline design.

---

## 10. Active blockers before controlled beta

- Authority/continuity hygiene was stale prior to ARCH-GOV-BASELINE-1 (addressed in this sprint for map/status/MR-BATCH docs).
- Package provenance: zero explicit `source_spec_id` on scanned manifests at audit baseline.
- Multi-frame consumer completeness incomplete.
- PSI intentionally unwired; activation requires separate governed work.
- Pass 3 protocol remains DRAFT pending human governance ratification.
- Controlled beta is **not** yet authorised.

---

## 11. Explicit supersession notes

| Prior claim | Supersession |
|---|---|
| Strategy (2026-06-20) implying three launch-core domains still missing | Superseded: six Wave 1 domains are built and wired |
| `docs/SPRINT_STATUS.md` as LIVE source of truth | Superseded by BUILD register + this baseline |
| AUTHORITY_MAP KB SOP v1.3 / pre-SOP v0_4 | Superseded by KB SOP v1.3.1 and pre-SOP v0.6.2 |
| MR-BATCH-001B completion/output “medical review then promote” recommendations | Superseded: benchmark/test-only; no medical-review promotion route |
| Stale RT-5D inventory expectations (186 packages / 7 cards) | Superseded by live estate: 191 provenance rows / 10 cards (refreshed in ARCH-GOV-BASELINE-1 tests) |
| This baseline's §5/§6 "six Wave 1 domains built and wired" | Qualified 2026-08-06 (§14): "wired" meant backend/DTO only — three domains are not frontend-rendered. See `docs/audit-papers/HEALTHIQ_MAIN_SYSTEM_SUBSYSTEM_COMPLETION_AUDIT.md`. |

---

## 12. Planning directive

**This document is the authoritative maturity baseline for future Stage 0 planning until superseded by a later approved baseline.**  
Do not invent completion percentages. Do not select or author the next implementation sprint from this document alone without a governed Stage 0 / pre-SOP workflow.

**Controlled beta is not yet authorised.**
---

## 13. Estate snapshot (audit / sprint verification)

| Metric | Value at verification |
|---|---|
| Provenance scan rows | 191 |
| Explicit `source_spec_id` on package manifests | 0 |
| Estate card evidence artefacts | 10 |
| Compiled hypotheses | 1 (`signal_vitamin_d_low`) |
| `pkg_kb52c_*` packages (batch-blocked class) | 72 |
| `knowledge_bus/current/latest_knowledge_status.json` | Absent |

---

## 14. 2026-08-06 Verification Update — main-system backend/DTO/consumer-visibility distinction

Source: `docs/audit-papers/HEALTHIQ_MAIN_SYSTEM_SUBSYSTEM_COMPLETION_AUDIT.md` (repository-grounded, includes direct code inspection and test execution).

| System | Backend-assembled | DTO-exposed | Consumer-visible | Status |
|---|---|---|---|---|
| Cardiovascular health | Yes | Yes | Yes | 1 of 3 compiled subsystems visible (MED-REV-1 deliberately hides 2) |
| Blood sugar control | Yes | Yes | Yes | 1 of 2 compiled subsystems visible (MED-REV-1 deliberately hides 1) |
| Liver health | Yes | Yes | Yes | 0 of 2 compiled subsystems visible — flat evidence only, by design |
| Kidney function | Yes | Yes | **No** | Not in `Wave1DomainCards.tsx`; no other frontend path found |
| Blood / iron / oxygen | Yes | Yes | **No** | Same; also no primary IDL narrative selected |
| Thyroid / energy regulation | Yes | Yes | **No** | Same; also has an active firing defect (below) |
| Silent inflammation (second-wave) | No | No | No | Deliberately deferred; research-present, domain-unmapped |
| Hormone balance / gonadal axis (second-wave) | No | No | No | Deliberately deferred; research-present, domain-unmapped |

**Known active defect (recorded, not diagnosed or corrected by this update):** `backend/tests/unit/test_p1_22_thyroid_activation_pack.py::test_ft3_high_requires_tsh_suppressed_companion_gate` fails on the current repository state — `signal_free_t3_high` does not fire when expected (FT3=7.0, TSH=0.2 suppressed). This is a genuine runtime-firing correctness defect in the thyroid domain, independent of and not to be conflated with the MED-REV-1 visibility decisions above.

This section qualifies, and takes precedence over, the "six Wave 1 domains built and wired" phrasing in §5 and §6 above for any reader relying on consumer-facing completeness.
