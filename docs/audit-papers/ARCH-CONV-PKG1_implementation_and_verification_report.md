# ARCH-CONV-PKG1 — Implementation and Verification Report

**Work ID:** `ARCH-CONV-PKG1`  
**Branch:** `feature/arch-conv-pkg1-frame-identity-closure`  
**Baseline HEAD (kernel start):** `aacd52b10ffdd8d355cf778fdb45ad52d2188f99`  
**change_type:** BEHAVIOUR  
**runtime_change:** YES  
**STOP Gate 1:** PASS  
**Gate 1 recommendation:** **GO**

---

## 1. Outcome

Closed the five verified launch-path activation-frame collapse surfaces so distinct medical frames cannot silently merge after registry load. Interaction-map YAML remains family-level clinical policy; runtime aggregation is explicit and auditable.

---

## 2. Files changed (implementation)

| Path | Role |
|---|---|
| `docs/architecture/ARCH-CONV-PKG1_frame_identity_surface_design.md` | Phase 1 design + STOP Gate 1 |
| `backend/core/knowledge/signal_result_index_v1.py` | Per-family / collect helpers |
| `backend/core/analytics/interpretation_display_layer_publish_v1.py` | IDL frame-safe family aggregation |
| `backend/core/contracts/interpretation_display_layer_v1.py` | Additive participating_activation_keys |
| `backend/core/analytics/domain_score_assembler.py` | active_activation_keys companion |
| `backend/core/models/results.py` | ConsumerDomainScoreV1 additive field |
| `backend/core/analytics/narrative_report_compiler_v1.py` | Lead frame preservation on graph path |
| `backend/core/analytics/intervention_selector_v1.py` | activation_key_refs + dedup union |
| `backend/core/contracts/report_v1.py` | ReportInterventionV1.activation_key_refs (additive; required for report compile) |
| `backend/core/analytics/signal_interaction_builder.py` | Per-node/per-chain frame participation |
| `backend/scripts/validate_launch_path_frame_identity_gate.py` | Behavioural gate |
| `backend/scripts/run_architecture_validation_gate.py` | Wire new gate |
| `backend/tests/unit/test_arch_conv_pkg1_frame_identity.py` | Pressure-set coverage tests |
| `frontend/app/types/analysis.ts` | Additive DTO mirrors |
| `docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md` | Continuity entry |
| This report | Verification |

---

## 3. Per-surface before / after

| Surface | Before | After |
|---|---|---|
| IDL publish | Last-wins `states[sid]` / `by_id[sid]` | `family_fired_states` + `group_by_signal_id`; bundle `participating_activation_keys` + `aggregation_scope=signal_family` |
| Domain scores | `active_signal_ids` only | Same family list + `active_activation_keys` under identical predicates |
| Narrative lead | Graph path blanked `activation_key` | `_resolve_lead_frame` preserves row frame; meta records lead participating keys / authority scope |
| Interventions | Dedup dropped peer-frame refs | `activation_key_refs` emitted; dedup **unions** frame refs |
| Interaction builder | Panel-global keys only; map family-keyed | Map unchanged; `node_frame_participation` + per-chain keys; `aggregation_scope=signal_family` |

---

## 4. Pressure-set coverage

| Family | Frames exercised |
|---|---:|
| signal_homocysteine_high | 3 |
| signal_mcv_high | 3 |
| signal_iron_low | 2 |
| signal_tpo_ab_high | 2 |
| signal_egfr_low | 2 |
| signal_alt_high | 4 |
| signal_ferritin_high | 3 |
| signal_creatinine_high | 2 |
| **Total** | **21** |

Note: Gate 0 cohort text said “22”; verified arithmetic and live registry for these eight families = **21**.

---

## 5. Test commands and results

| Command | Exit |
|---|---:|
| `python -m pytest backend/tests/unit/test_arch_conv_pkg1_frame_identity.py -q` | 0 |
| `python backend/scripts/validate_launch_path_frame_identity_gate.py` | 0 |
| `python -m pytest backend/tests/unit/test_arch_rt_identity_prov_1.py backend/tests/unit/test_signal_interaction_builder.py -q` | 0 |
| `python -m pytest backend/tests/unit/test_narrative_report_compiler_v1.py backend/tests/unit/test_p3_layerb_intel_1.py -q` | 0 |
| `python -m pytest backend/tests/unit/test_intervention_selector_v1.py backend/tests/unit/test_domain_score_assembler_v1.py -q` | 0 |

Pre-existing unrelated failure observed (not introduced): `test_idl_design_lock_yaml_exists` — `docs/strategy/Interpretation_Display_Layer_Design_Lock.md` absent on tree.

Kernel finish / golden gate evidence captured by Automation Bus on finish.

---

## 6. Acceptance criteria

| Criterion | Status |
|---|---|
| All five surfaces assessed against live code | PASS |
| STOP Gate 1 passed or escalated | PASS |
| No frame-destructive bare-signal_id logic remains on five surfaces | PASS |
| Interaction node/confidence identity genuinely frame-safe (family map + frame audit) | PASS |
| Intentional family aggregation explicit/auditable | PASS |
| Narrative lead frame identity preserved | PASS |
| Domain scoring cannot silently collapse/double-count frames | PASS |
| Intervention selection cannot borrow across frames | PASS |
| Gate 0 pressure-set covered | PASS (8/21) |
| Determinism + single-frame compatibility proven | PASS |
| Architecture gates/tests pass (incl. new behavioural gate) | PASS (see §5; finish gate authoritative) |
| No provenance/WHY/prose/PSI/Gemini/threshold scope | PASS |
| No architecture-completion or beta-readiness claim | PASS |

---

## 7. STOP-condition assessment

| # | Result |
|---|---|
| 1 Medical frame-priority required | Not triggered |
| 2 Signal firing/thresholds change required | Not triggered |
| 3 Scope >25% growth | Not triggered |
| 4 >1 unplanned follow-on package | Not triggered |
| 5 Package 2 prerequisite | Not triggered |
| 6 Unexplained launch regression | Not triggered |
| 7 Estate-wide redesign required | Not triggered |
| 8 Unexplained gate failure | Not triggered |

---

## 8. Gate 1 recommendation

```text
GO
```

Package 1 obligation is closed. Proceed to Package 2 (provenance / reachability honesty). Do not merge without human authority.

---

## 9. Unresolved limitations

1. Interaction-map edges remain family-level by design; frame annotation is runtime metadata, not frame-specific clinical edges.
2. Narrative graph-path lead still selects the first fired lead-hint row deterministically for focus; multi-frame family peers are retained in `lead_participating_activation_keys`.
3. Gate 0 arithmetic typo (22 vs 21) corrected here; live registry confirms 21 for the eight families.
4. Pre-existing missing IDL design-lock markdown is out of scope.
5. No controlled-beta authorisation.
