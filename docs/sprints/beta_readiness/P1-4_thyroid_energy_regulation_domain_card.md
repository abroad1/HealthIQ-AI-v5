# P1-4 — Thyroid / Energy Regulation Domain Card

## 1. Summary

**Phase 1: STOPPED — implementation did not proceed.**

Authority reconciliation found unresolved FT3-low register conflict, an inert hormonal scoring rail, and inactive TSH runtime packages. A bounded launch-core thyroid domain card cannot be emitted safely without improvising scoring policy, activating deferred/context-dependent signals, or presenting a misleading partial thyroid view.

**Implemented:** Phase 1 authority reconciliation only (this note + register update).

**Out of scope (blocked):** Domain assembler wiring, compiled card, subsystem evidence, scoring-policy changes, runtime signal allowlist, tests for domain output.

## 2. Phase 1 authority reconciliation

### Authority documents and files reviewed

| Source | Finding |
|---|---|
| `docs/sprints/beta_readiness/P1-1_launch_core_domain_build_materials_map.md` §6 | Thyroid partial readiness; FT3 register drift documented; kb52c TSH and kb59 antibodies inactive |
| `backend/ssot/biomarkers.yaml` | tsh, free_t3, free_t4, tpo_ab, tgab present; all `system: thyroid` |
| `backend/ssot/scoring_policy.yaml:31-34` | **hormonal system inert** — `system_weight: 0.0`, `biomarkers: []`, no thyroid bands |
| `batch2_thyroid_gate_execution_register_v1.yaml:65-73` | `signal_free_t3_low` **deferred**, `activated: false` |
| `batch2_full_coverage_activation_execution_register_v1.yaml:12-15` | Same signal listed **ACTIVATE_WITH_GATES**, `runtime_active_canonical` |
| `batch2_context_clearance_register_v1.yaml:217-246` | FT3 low **inactive**, `activation_eligibility: false`, `DEFERRED_NON_LAUNCH_CRITICAL` |
| `medical_frame_identity_index_v1.yaml:1368-1393` | Frame shows `runtime_active_canonical` / `active` but notes say **"Not runtime-active"** and **"FT3 low formally deferred"** |
| `root_cause_authority_register_v1.yaml:33-37` | `signal_free_t3_low` → `ROOT_CAUSE_REQUIRES_FUTURE_MAPPING` |
| `package_estate_KB-S49_v1.yaml` (via P1-1) | kb52c TSH patterns **not runtime-loaded**; kb59 antibodies **inactive** |
| P1-2 / P1-3 implementation notes | Pattern requires active scoring rail or bounded card evidence; P1-3 used empty signal allowlist + existing cbc rail |

### Marker scope (governed estate)

| Marker | SSOT | Scoring rail | Runtime package |
|---|---|---|---|
| TSH | Yes | **None** (hormonal empty) | kb52c/s24 packages **not launch-loaded** |
| free_t4 | Yes | **None** | kb47 FT4 high/low **runtime_active_canonical** (TSH-gated) |
| free_t3 | Yes | **None** | kb47 FT3 high **runtime_active_canonical**; FT3 low **conflicted** |
| tpo_ab / tgab | Yes | **None** | kb59 **inactive** |

### Signal status

| Signal | Status | Notes |
|---|---|---|
| `signal_free_t3_high` | runtime_active_canonical | TSH-suppressed gate required |
| `signal_free_t4_high` | runtime_active_canonical | TSH-suppressed gate required |
| `signal_free_t4_low` | runtime_active_canonical | TSH-present gate required |
| `signal_free_t3_low` | **Unresolved / context-dependent** | Contradictory across registers; deferred in gate register; inactive in clearance register |
| kb52c TSH high/low | **Inactive** | Not runtime-loaded |
| kb59 antibody signals | **Inactive** | Not runtime-loaded |
| Legacy s24 TSH | runtime_loaded, not launch-visible | Pass 3 revalidation required |

### FT3 low status

**Unresolved — context-dependent with contradictory authority.**

- `batch2_thyroid_gate_execution_register_v1.yaml` lists FT3 low under `deferred_thyroid_packages` with `activated: false`.
- `batch2_full_coverage_activation_execution_register_v1.yaml` lists the same package as activated `runtime_active_canonical`.
- `batch2_context_clearance_register_v1.yaml` records `activation_eligibility: false` and `current_runtime_authority_status: inactive`.
- `medical_frame_identity_index_v1.yaml` contains conflicting fields (`promotion_state: runtime_active_canonical` vs notes stating formal deferral).
- `root_cause_authority_register_v1.yaml` blocks root-cause mapping.

**Decision:** FT3 low must **not** be included in any domain signal allowlist and must **not** be treated as safely launch-visible until registers are reconciled under a dedicated governance sprint.

### Authority conflicts / ambiguities

1. **FT3 low register drift** — three governance registers disagree on activation status (STOP condition 1).
2. **Hormonal scoring rail absent** — unlike P1-2 (kidney) and P1-3 (cbc), no existing scoring rail supports a scored thyroid domain row without new bands (STOP condition: scoring-policy ambiguity).
3. **TSH runtime gap** — primary thyroid-axis marker has no launch-visible runtime signal; a domain card led by FT3/FT4 only would omit TSH (STOP condition: misleading domain per prompt signal-routing rules).
4. **Medical frame index self-contradiction** — FT3 low frame metadata conflicts with its own deferral notes.

### Implementation decision

**STOP before Phase 2.** Do not modify runtime code, scoring policy, compiled cards, or domain assembler.

Rationale: P1-4 prompt Phase 1 STOP conditions triggered at items 1, 5, 7, and signal-routing misleading-domain check. Cursor cannot reconcile register drift or invent hormonal scoring bands within this sprint scope.

## 3. P1-1 evidence used

- P1-1 §6 rated thyroid partial readiness and **not recommended first** among missing domains
- P1-1 §6.3 documented FT3 low register drift and kb47 vs kb52c/kb59 split
- P1-1 §6.7 carry-forward: reconcile FT3 register drift before thyroid implementation
- P1-1 §11 sequencing: P1-4 thyroid after FT3 register reconciliation

## 4. Runtime changes

**Not applicable — stopped at authority gate.**

No changes to `domain_score_assembler.py`, `wave1_subsystem_evidence.py`, `domain_narrative_wave1.py`, `health_system_card_evidence.py`, `scoring_policy.yaml`, or `knowledge_bus/compiled/`.

## 5. Safety boundaries

- No runtime output emitted; no diagnostic thyroid disease language introduced
- No blocked/context-dependent signals activated
- No scoring-policy or global reference-range changes
- No Gemini, frontend inference, or fallback parser logic

## 6. Tests and validation

**Tests added/updated:** None (blocked sprint — documentation only).

**Commands run:**
```powershell
git diff --stat
git status --short
```

**Result:** No runtime tests run; Phase 1 gate stop documented honestly.

## 7. Carry-forwards

- **P3 governance:** Reconcile FT3 low across `batch2_thyroid_gate_execution_register_v1.yaml`, `batch2_full_coverage_activation_execution_register_v1.yaml`, `batch2_context_clearance_register_v1.yaml`, and `medical_frame_identity_index_v1.yaml`; resolve `ROOT_CAUSE_REQUIRES_FUTURE_MAPPING` for `signal_free_t3_low`
- **Scoring:** Define bounded hormonal scoring rail (TSH/FT4 minimum) with governed bands before domain-card sprint retry — or explicitly authorise unscored card-only domain pattern
- **Signals:** kb52c TSH and kb59 antibody promotion/adjudication plan before launch-visible thyroid domain
- **P2 prose:** FT3, FT4, antibody retail explainers; thyroid pathway explainer
- **P5 UX:** Defer fifth launch-core consumer row until Layer B thyroid output is stable

**Recommended next sprint:** P3-FT3-REGISTER-RECONCILIATION (governance-only) or retry P1-4 only after reconciliation artefact exists on main.
