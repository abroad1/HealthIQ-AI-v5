# ARCH-CONV-PKGC-1 — Phase 0 Hardening Pack (Data-Governance STOP)

**Work ID:** `ARCH-CONV-PKGC-1`  
**Branch:** `feature/arch-conv-pkgc-1-waist-unit-remediation`  
**Risk:** STANDARD (re-confirmed below)  
**Change type:** MIXED  
**Execution model:** TWO_PHASE_START_FINISH  
**Implementation owner:** Core Engine agent  
**Status:** Phase 1 mechanism implemented under `APPROVED_WITH_CONDITIONS`. Live DB write **outstanding** — WP remains `IN_PROGRESS`.

**Hardening clearance:** `automation_bus/latest_prompt_hardening.json` — `ARCH-CONV-PKGC-1` / `HARDENED`.

---

## 0. Baseline (repository-grounded)

| Check | Result |
|---|---|
| Feature branch tip at Phase 0 | `9ae8a9e` (bus stage commit) |
| `main == origin/main` at branch creation | **YES** — `a433f9f6b846a82317f928048c316bc1d8a78b0c` |
| Stash | Empty (governed) |
| Active WP after start | `ARCH-CONV-PKGC-1` / `IN_PROGRESS` |
| Carry-forward | `CF-ARCH-CONV-WAIST-1` — **Open** (`launch_core_carry_forward_register.md:99`) |
| Live DB probe | **FAILED** — `DATABASE_URL` present (`postgresql`) but localhost:5433 connection refused |
| Stage 1B no-op check | **Not a no-op** — waist-unit stale rule absent; historic disposition not executed |

---

## 1. Stage 1A classification check (Intelligence Core)

| Question | Answer | Evidence |
|---|---|---|
| Does `detect_launch_core_stale_reasons()` alter medical reasoning, ranking, interpretation or output construction? | **No** | `backend/core/dto/result_versioning_policy_v1.py:63-102` — read-only heuristic over persisted DTO shape; returns reason strings only. Module docstring (`:1-4`) states “Does not mutate stored results.” |
| Is it Intelligence Core under Automation Bus SOP §3? | **No** | SOP §3 covers root-cause compilers, signal evaluators, InsightGraph construction, ranking/filtering, governed-content loaders that affect emitted reasoning. This function performs presentation/staleness metadata assessment under `backend/core/dto/`, consumed by `build_result_versioning_metadata` (`analysis.py` API metadata). |
| Does this sprint remain STANDARD? | **YES — STANDARD** | Behaviour change is one new stale-reason string + governed historic-row disposition metadata. No medical content / compiled-WHY / ranking change. |

**Reclassification to HIGH is not required on current evidence.**

---

## 2. Affected code surface

| Path | Role |
|---|---|
| `backend/core/dto/result_versioning_policy_v1.py` | Six existing stale rules; proposed home for waist-unit rule |
| `backend/core/dto/persisted_replay_contract_v1.py` | Base compatibility / version stale reasons (must remain unchanged) |
| `backend/core/dto/analysis_regeneration_v1.py` | Read-only regen availability; **must not** invoke a regen job |
| `backend/app/routes/analysis.py:439` | Calls `build_result_versioning_metadata` on read |
| `backend/core/pipeline/waist_circumference_v1.py` | Forward-path unit contract; legacy unitless detector (`is_legacy_unitless_waist_questionnaire`) — reference for rule evidence, not clinical rewrite |
| `backend/core/models/database.py` | `Analysis.questionnaire_data` / `raw_biomarkers`; `AnalysisResult.result_version` / `processing_metadata` — audit-trail capacity |

**Excluded (PKGC-2 / medical):** `output_authority_provenance_builder_v1.py`, compiled-WHY / root-cause / package / PSI / SSOT / frontend medical logic.

---

## 3. Existing stale-reason rules (must preserve)

From `detect_launch_core_stale_reasons()` (`result_versioning_policy_v1.py:63-102`):

1. `completeness_policy_mismatch:{policy}`
2. `completeness_policy_missing`
3. `card_subsystem_completeness_mismatch:{domain_id}`
4. `legacy_hard_coded_subsystem_trace:{subsystem_id}`
5. `legacy_total_bilirubin_false_missing`
6. (dedupe via `dict.fromkeys`)

Base contract (`persisted_replay_contract_v1.py`) separately contributes version/manifest reasons merged in `assess_result_versioning`.

**Waist-unit rule:** **absent** (grep `waist` across versioning/replay/regen modules: zero matches).

### Proposed stale-reason identifier (for Anthony ratification)

```text
legacy_waist_unit_defect:used_incorrectly
```

**Semantics (proposed):** persisted analysis is among the audit-governed `used_incorrectly` set **or** carries equivalent deterministic lineage evidence of the former inches×2.54 mishandling on a bare unitless waist. Must not fire on:

- valid explicit-cm dict waists;
- valid explicit-inches dict waists with correct conversion;
- bare values without sufficient proof of the legacy defect.

Exact detection predicate for Phase 1 must be derived from audit + live row evidence after Anthony approval — not invented here as implementation.

---

## 4. Affected data surface — 12 `used_incorrectly` IDs

Source: `docs/audit-papers/WAIST_UNIT_LEGACY_IMPACT_AUDIT.md` (48 bare rows; 12 used_incorrectly; 36 dropped_as_implausible).

| analysis_id | created_at (audit) | original_value | incorrect_mapped_cm_if_inches | audit class |
|---|---|---:|---:|---|
| `e5cfbc62-93fa-4bac-8894-dcb69117ac4c` | 2026-04-25 21:23:55 | 77 | 195.58 | used_incorrectly |
| `02df9062-eba8-4df1-8072-8d2182aca35d` | 2026-04-27 17:38:36 | 77 | 195.58 | used_incorrectly |
| `7fc35b86-15c2-4d76-843a-e964263be0b7` | 2026-04-28 15:47:57 | 77 | 195.58 | used_incorrectly |
| `a3244490-dd74-4922-a1c6-49a25c1f6604` | 2026-04-28 16:55:54 | 60 | 152.4 | used_incorrectly |
| `7f780514-d288-4331-8020-8866744b70ae` | 2026-04-28 17:42:57 | 67 | 170.18 | used_incorrectly |
| `ad721d67-f2e8-4942-8450-8598b8e35343` | 2026-05-02 08:27:35 | 75 | 190.5 | used_incorrectly |
| `7cc8b2d5-c8f0-4138-ba18-8540eece06a1` | 2026-05-17 10:04:35 | 78 | 198.12 | used_incorrectly |
| `91046b62-114f-44a3-a2ab-2b885ea5782b` | 2026-05-17 11:18:39 | 78 | 198.12 | used_incorrectly |
| `7b8c58b5-191f-41e7-8fe4-a66938bb0a98` | 2026-05-17 11:48:34 | 78 | 198.12 | used_incorrectly |
| `e3a1ee79-963e-46a1-afee-58657d1ffb55` | 2026-05-17 17:04:26 | 78 | 198.12 | used_incorrectly |
| `7aacc734-95cf-4ea5-a19c-0d03d98dd2e9` | 2026-05-24 06:55:24 | 76 | 193.04 | used_incorrectly |
| `d7417288-7e11-48da-8716-d0f63f77c491` | 2026-05-26 17:23:37 | 22 | 55.88 | used_incorrectly |

### Live DB verification status

```text
probe: CONNECTION_REFUSED localhost:5433
current_persisted_value: UNKNOWN (pending live DB)
current_unit_provenance: UNKNOWN (pending live DB)
current_result_version / stale state: UNKNOWN (pending live DB)
already_remediated / deleted / superseded: UNKNOWN (pending live DB)
```

**Stage 1B partial gap:** existence of all 12 rows could not be re-confirmed live. Phase 0 register therefore carries `live_verification: PENDING` and does **not** authorise write mode. Anthony may still approve dispositions conditional on Phase 1 dry-run fail-closed precondition checks.

---

## 5. Schema / audit-trail capacity

Without new columns, remediation metadata can live in existing JSON:

- `analyses.questionnaire_data` / `raw_biomarkers` — preserve original waist payload
- `analyses.processing_metadata` and/or `analysis_results.processing_metadata` — remediation action, reason, timestamp, actor/work_id, reversibility pointer
- `analysis_results.result_version` — unchanged unless policy requires (this sprint prefers **no** version redesign)

Alembic migrations exist if a dedicated lineage column is later required; Phase 0 proposes **no** DB schema migration if Anthony accepts metadata-in-JSON for `MARK_STALE_NO_REWRITE`.

---

## 6. Proposed row dispositions (pending Anthony)

**Architectural recommendation (not yet authorised):** for all 12 rows prefer **`MARK_STALE_NO_REWRITE`**.

Rationale:

1. Audit recommendation #1 is mark stale / incompatible when a waist-unit policy id is introduced.
2. `GOVERNED_REMAP` that corrects clinical scores would require regeneration — explicitly out of scope / unbuilt.
3. Remapping questionnaire unit alone without regenerating scores would leave incorrect derived outputs while claiming repair — unsafe.
4. `MARK_STALE_NO_REWRITE` preserves originals, needs no inferred corrected value, and pairs with the new stale-detection rule.

Optional note: `d7417288` (`original_value=22`) is outside the audit’s ~75–93 UK-cm cluster. Still classified `used_incorrectly` by the audit. Proposed disposition remains `MARK_STALE_NO_REWRITE` (no rewrite). Anthony may elevate this row to `BLOCKED_AMBIGUOUS` if desired.

`GOVERNED_REMAP` is **not** proposed for any row in this Phase 0 pack.

---

## 7. Rollback / idempotency design (proposed)

| Concern | Design |
|---|---|
| Rollback | Stale mark + remediation metadata are additive; removing the metadata / reason reverses display classification without inventing clinical values |
| Idempotency | Re-running remediation must detect existing remediation metadata for work_id `ARCH-CONV-PKGC-1` and no-op |
| Dry-run | Must list exact 12 IDs and planned actions before write |
| Fail-closed write | Refuse if row missing, precondition mismatch, unexpected set size, unknown ID, or audit persistence failure |

---

## 8. Acceptance-test matrix (Phase 1 after approval)

Cover prompt tests 1–23: new reason on governed shapes; no false positives on valid cm/inches; six existing rules unchanged; dry-run exact set; no unapproved mutations; idempotent re-run; fail-closed precondition; no regen/provenance/compiled-WHY drift; architecture + baseline + three-layer green.

---

## 9. Explicit exclusion proof

| Exclusion | Proof |
|---|---|
| PKGC-2 provenance identity | No edits to `output_authority_provenance_builder_v1.py` / provenance tests |
| Full result-versioning advancement | No change to `CURRENT_RESULT_VERSION` / replay redesign |
| Regeneration job | `analysis_regeneration_v1.py` remains read-only assessor |
| Compiled-WHY / medical content | Out of allowed file scope |
| CF-MEDREV2-002 | Not touched |

---

## 10. Data-governance STOP

Anthony must approve the complete row-by-row register in:

- `docs/architecture/ARCH-CONV-PKGC-1_data_remediation_register.yaml`
- `docs/architecture/ARCH-CONV-PKGC-1_DATA_GOVERNANCE_decision.md`

Until `implementation_authorised: true` is recorded:

- Do **not** add the stale-detection rule
- Do **not** mutate historic rows
- Do **not** run remediation write mode
- Do **not** build/invoke regeneration
- Do **not** touch provenance-identity code

Work package remains `IN_PROGRESS`.
