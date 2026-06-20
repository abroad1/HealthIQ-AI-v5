# P1-5 — FT3 / Thyroid Authority Reconciliation

## 1. Summary

- **Why required:** P1-4 stopped before thyroid domain implementation because FT3 low carried contradictory authority across governance registers, the hormonal scoring rail is inert, TSH kb52c packages are not launch-loaded, and kb59 antibodies are inactive.
- **Reconciliation outcome:** **Partially reconciled.** FT3 low register drift was corrected conservatively across three governance files. Remaining thyroid launch blockers (hormonal scoring rail, TSH package promotion, antibody inactivity) are documented but not resolved in this sprint.
- **Governance files changed:** Yes — three YAML registers (see §8). `root_cause_authority_register_v1.yaml` left unchanged (runtime-consumed; already conservative).
- **P1-4 retry:** **Permitted only after named preconditions** (see §7). FT3 low reconciliation alone does not unblock domain-card implementation.

## 2. Authority files inspected

| File | Path | Purpose | Changed? |
|---|---|---|---|
| Thyroid gate execution register | `knowledge_bus/governance/batch2_thyroid_gate_execution_register_v1.yaml` | Authoritative thyroid activation/deferral gates | No — already deferred FT3 low |
| Full-coverage activation execution register | `knowledge_bus/governance/batch2_full_coverage_activation_execution_register_v1.yaml` | Batch 2 activation audit trail | **Yes** — FT3 low moved to kept_inactive |
| Full-coverage activation readiness register | `knowledge_bus/governance/batch2_full_coverage_activation_readiness_register_v1.yaml` | Readiness metadata per package | **Yes** — FT3 low deferred status |
| Context clearance register | `knowledge_bus/governance/batch2_context_clearance_register_v1.yaml` | Launch clearance / eligibility | No — already inactive/deferred for FT3 low |
| Medical frame identity index | `knowledge_bus/governance/medical_frame_identity_index_v1.yaml` | Frame promotion and runtime authority | **Yes** — FT3 low frame inactive |
| Root-cause authority register | `knowledge_bus/governance/root_cause_authority_register_v1.yaml` | Runtime root-cause mapping | No — `ROOT_CAUSE_REQUIRES_FUTURE_MAPPING` retained |
| Scoring policy | `backend/ssot/scoring_policy.yaml` | Domain scoring rails | No |
| Package estate | `knowledge_bus/governance/package_estate_KB-S49_v1.yaml` | Runtime package load status | No |
| P1-4 blocker report | `docs/sprints/beta_readiness/P1-4_thyroid_energy_regulation_domain_card.md` | Trigger authority | No |
| P1-1 build materials map | `docs/sprints/beta_readiness/P1-1_launch_core_domain_build_materials_map.md` | Domain readiness context | No |

## 3. Thyroid marker and signal status table

| Marker / pattern | File/register | Current status before P1-5 | Conflict? | P1-5 reconciled position | File changed? | Notes |
|---|---|---|---|---|---|---|
| FT3 low | thyroid_gate / full_coverage / clearance / frame_index / root_cause | Deferred vs runtime_active_canonical vs inactive vs active frame | **Yes** | **Deferred / not launch-visible / inactive** | Yes (3 files) | Supersedes permissive full-coverage claim |
| FT3 high | thyroid_gate execution register | `runtime_active_canonical`, TSH-suppressed gate | No | **Runtime active with TSH-suppressed gate** | No | Launch-visible only with gate satisfied |
| FT4 high | thyroid_gate execution register | `runtime_active_canonical`, TSH-suppressed gate | No | **Runtime active with TSH-suppressed gate** | No | Same gating model as FT3 high |
| FT4 low | thyroid_gate execution register | `runtime_active_canonical`, TSH-present gate | No | **Runtime active with TSH-present gate** | No | Requires TSH companion evidence |
| TSH high | package_estate kb52c | Package exists; `runtime_loaded: false` | Partial | **Not launch-active** | No | s24 legacy may load but not launch-visible |
| TSH low | package_estate kb52c | Package exists; `runtime_loaded: false` | Partial | **Not launch-active** | No | Domain card without TSH is misleading |
| Thyroid antibodies (TPO/TgAb) | package_estate kb59 | `runtime_loaded: false` | No | **Inactive / not launch-visible** | No | Excluded from launch domain scope |

## 4. FT3 low reconciliation

### Positions found (pre-P1-5)

1. **`batch2_thyroid_gate_execution_register_v1.yaml`** — `deferred_thyroid_packages`: `activated: false`, reason requires TSH + FT4 + illness/medication context.
2. **`batch2_full_coverage_activation_execution_register_v1.yaml`** — Listed in `activated_packages` as `runtime_active_canonical` / `ACTIVATE_WITH_GATES_THIS_SPRINT`.
3. **`batch2_context_clearance_register_v1.yaml`** — `activation_eligibility: false`, `DEFERRED_NON_LAUNCH_CRITICAL`, inactive runtime authority.
4. **`medical_frame_identity_index_v1.yaml`** — Frame showed `runtime_active_canonical` / `active` while notes stated "Not runtime-active" and "FT3 low formally deferred".
5. **`root_cause_authority_register_v1.yaml`** — `ROOT_CAUSE_REQUIRES_FUTURE_MAPPING` (conservative; unchanged).

### Contradiction analysis

The permissive interpretation (full-coverage activation + active frame index) conflicted with three independent conservative sources: thyroid gate deferral, context clearance ineligibility, and frame-index notes. Per SOP, the **conservative deferred/inactive position** is authoritative.

### Final authority position

**FT3 low is deferred, inactive, and not launch-visible.** It must not appear in launch-core domain allowlists or be treated as runtime-active canonical for beta readiness until a dedicated activation-control sprint resolves TSH + FT4 + illness/medication context gates with unified register alignment.

### Corrections applied

| File | Correction |
|---|---|
| `medical_frame_identity_index_v1.yaml` | `promotion_state: compiled_not_promoted`, `runtime_authority_status: inactive`, P1-5 supersession note |
| `batch2_full_coverage_activation_execution_register_v1.yaml` | Removed from `activated_packages`; added to `kept_inactive_packages`; counts 5→4 activated, 4→5 inactive |
| `batch2_full_coverage_activation_readiness_register_v1.yaml` | `governance_deferred_inactive`, `DEFERRED_PENDING_CONTEXT_GATES`, superseded by P1-5 |

## 5. Other thyroid authority findings

- **FT3 high / FT4 high / FT4 low:** No register conflict. Thyroid gate register is authoritative; TSH companion gates apply. No changes made.
- **TSH high/low:** kb52c packages not runtime-loaded for launch. Legacy s24 TSH material may exist in estate but is not launch-visible. TSH absence blocks a complete thyroid domain card.
- **Thyroid antibodies:** kb59 packages inactive (`runtime_loaded: false`). Out of launch scope.
- **Root-cause mapping:** FT3 low remains `ROOT_CAUSE_REQUIRES_FUTURE_MAPPING`. No change (runtime-consumed register; effect uncertain if edited).

## 6. Hormonal scoring rail assessment

- **Current status:** Inert — `backend/ssot/scoring_policy.yaml` hormonal system has `system_weight: 0.0` and empty `biomarkers: []`.
- **Changed?** No. Scoring policy changes require a separate scoring sprint.
- **Preconditions for future thyroid scoring:** Named biomarker bands for tsh, free_t3, free_t4 (and optionally antibodies) with medical authority sign-off; must not be improvised during domain-card sprints.

## 7. P1-4 retry decision

**P1-4 retry permitted only after named preconditions:**

1. **Hormonal scoring rail populated** — separate scoring-policy sprint with governed bands for thyroid markers.
2. **TSH launch authority resolved** — kb52c promotion or explicit documented acceptance of a bounded FT3/FT4-only card with clinical disclaimer (not recommended).
3. **FT3 low remains deferred** — must not be added to launch domain signal allowlist (unchanged by this sprint).
4. **Register alignment maintained** — no reintroduction of permissive FT3 low activation without thyroid-gate + medical review.

FT3 low reconciliation **does not alone** permit P1-4 retry.

## 8. Files changed

| File | Status correction |
|---|---|
| `knowledge_bus/governance/medical_frame_identity_index_v1.yaml` | FT3 low frame: active → inactive/deferred |
| `knowledge_bus/governance/batch2_full_coverage_activation_execution_register_v1.yaml` | FT3 low: activated → kept_inactive (superseded) |
| `knowledge_bus/governance/batch2_full_coverage_activation_readiness_register_v1.yaml` | FT3 low: RUNTIME_ACTIVE → DEFERRED_PENDING_CONTEXT_GATES |
| `docs/architecture/ADR-THYROID-FT3-AUTHORITY-RECONCILIATION-1.md` | New ADR |
| `docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md` | P1-5 register entry |
| `backend/tests/governance/test_batch2_context_clearance_register.py` | FT3 removed from activated set expectation |
| `backend/tests/governance/test_active_signal_context_gate_reachability_governance.py` | Activated count 5 → 4 |
| `backend/tests/regression/test_batch2_thyroid_tsh_gating.py` | Frame index expects inactive/deferred |

## 9. Safety and architecture boundaries

Confirmed:

- No runtime core code changed
- No scoring policy changed
- No signal newly activated
- No package promoted
- No Knowledge Bus source packages changed
- No Pass 3 artefacts changed
- No Gemini / frontend / fallback parser introduced

## 10. Recommended next sprint

1. **P1-SCORING-HORMONAL** (or equivalent) — populate hormonal scoring rail for thyroid markers.
2. **P1-TSH-PROMOTION** (or governance sprint) — resolve kb52c TSH launch authority.
3. **P1-4 retry** — only after preconditions 1–2 are met.
