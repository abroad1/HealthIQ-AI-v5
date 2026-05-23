# LC-S16/17/19 — Combined Implementation Notes

**Work package:** LC-S16-17-19  
**Branch:** `scaffold/lc-s16-17-19-kb-surface-payload-contract`  
**Date:** 2026-05-23

## 1. Preflight results

| Check | Result |
|-------|--------|
| Branch (before start) | `main` → created `scaffold/lc-s16-17-19-kb-surface-payload-contract` |
| Stash | Empty — no triage required |
| Working tree | `automation_bus/latest_cursor_prompt.md`, `latest_prompt_hardening.json` modified on main |
| Controlling docs | `HealthIQ_AI_core_scaffold_completion_definition_v1.md` — present |
| Sprint plan | `HealthIQ_AI_Core_Scaffold_Completion_Sprint_Plan_FINAL.md` — present |
| Kernel start | `python backend/scripts/run_work_package.py start` — exit 0 |
| Active token | `automation_bus/state/work_package_active.json` — `LC-S16-17-19` |

**Bus commit:** `chore(bus): LC-S16-17-19 work package prompt and hardening` (required clean porcelain for kernel).

## 2. Prior scaffold guard results

All passed (single run):

```
pytest backend/tests/regression/test_lc_s8f_phase_b_true_conversions.py -q
pytest backend/tests/regression/test_lc_s8g_uploaded_unit_display_fidelity.py -q
pytest backend/tests/regression/test_lc_s8d_unit_governance_sentinel.py -q
pytest backend/tests/regression/test_lc_s10b_launch_core_protection.py -q
pytest backend/tests/regression/test_lc_s11a_trust_blocker_correction.py -q
pytest backend/tests/regression/test_lc_s13_lifestyle_coherence_narrative.py -q
pytest backend/tests/regression/test_lc_s14_direction_aware_scoring.py -q
pytest backend/tests/unit/test_scoring_rules.py -q
```

## 3. Frontend-surface audit summary

See `LC-S16_knowledge_asset_frontend_surface_audit.md`. Verdict: **PASS WITH GAPS**. Retail journey maps to governed DTO/IDL/narrative fields; hero assembly and `meta.insight_graph` exposure are the main gaps.

## 4. STOP / rescope gate

**Not triggered.** Proceeding to LC-S17/LC-S19 implementation was authorised by audit.

## 5. Knowledge Bus lifecycle decisions

- Seven lifecycle states defined (see LC-S17).
- Runtime continues to load all valid packages (no gating change this sprint).
- Orphan reporter documents inventory drift vs KB-S49 estate.

## 6. Machine-enforced vs documentation-only controls

| Control | Status |
|---------|--------|
| Lifecycle enum | Machine-enforced |
| Standard / WHY package files | Machine-enforced (sample + PSI subset) |
| Orphan reporting | Machine-enforced (reporter + test) |
| DTO root key contract | Machine-enforced |
| Inventory refresh | Documentation-only / LC-S18 backlog |
| Runtime lifecycle gating | Documentation-only |

## 7. DTO field classification summary

See `LC-S19_payload_contract_hardening_notes.md`. No serialisation shape changes.

## 8. Frontend consumer impact assessment

**None breaking.** No frontend file edits. TypeScript contract already declares consumed roots. Future work may filter `meta.insight_graph` for retail-only API.

## 9. Files changed

| File | Purpose |
|------|---------|
| `docs/audit-papers/LC-S16_knowledge_asset_frontend_surface_audit.md` | LC-S16 audit |
| `docs/audit-papers/LC-S17_knowledge_bus_lifecycle_framework.md` | LC-S17 framework |
| `docs/audit-papers/LC-S19_payload_contract_hardening_notes.md` | LC-S19 contract |
| `docs/audit-papers/LC-S16_17_19_kb_surface_payload_contract_notes.md` | This note |
| `backend/core/dto/frontend_contract_v1.py` | Root key contract |
| `backend/core/knowledge/kb_lifecycle_contract_v1.py` | Lifecycle constants + orphan detect |
| `backend/scripts/validate_kb_package_estate_orphans_v1.py` | Orphan CLI reporter |
| `backend/tests/regression/test_lc_s16_17_19_kb_surface_payload_contract.py` | Regression guards |
| `sentinel/packs/escaped_defects_v1.json` | New defect classes |

## 10. Tests added/updated

- `backend/tests/regression/test_lc_s16_17_19_kb_surface_payload_contract.py` (new)

## 11. Sentinel updates

Added to `escaped_defects_v1.json`:

- `frontend_section_not_backed_by_governed_source`
- `knowledge_asset_not_surfaced_when_available`
- `generic_fallback_used_when_governed_asset_exists`
- `consumer_payload_internal_field_leakage`
- `dto_frontend_contract_breakage`
- `raw_signal_or_internal_id_visible`
- `kb_lifecycle_required_file_missing`
- `kb_orphan_package_unreported`

## 12. Residual risks

- `package_estate_KB-S49_v1.yaml` stale vs 109+ on-disk packages.
- `meta.insight_graph` still on consumer payload.
- Hero/body fallback chains remain frontend-derived.
- Browser UAT not run this sprint (orchestrator/static audit only).

## 13. Recommendation for LC-S18

1. Regenerate package estate inventory and close orphan drift.
2. Build surfacing matrix: signal_id → IDL / narrative / domain / frontend section.
3. Optional retail-safe API projection stripping internal meta paths.
4. Playwright results journey snapshot tests tied to LC-S16 section map.
