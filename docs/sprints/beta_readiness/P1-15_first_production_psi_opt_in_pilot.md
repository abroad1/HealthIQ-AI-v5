# P1-15 — First Production PSI Opt-In Pilot with Contract STOP Gate

## 1. Contract verification evidence

| Authority question | Answer | Evidence |
|---|---|---|
| Production package store | `knowledge_bus/packages/` | Package manifests and artefacts under per-package directories |
| Package manifest schema | `knowledge_bus/schema/package_manifest_schema.yaml` | Optional `promoted_signal_intelligence` field triggers PSI validation only |
| PSI schema | `knowledge_bus/schema/promoted_signal_intelligence_schema_v1.yaml` | KB-S47d contract |
| Package validator | `backend/scripts/validate_knowledge_package.py` | Orchestrates manifest, research, signal, PSI validators |
| PSI validator | `backend/scripts/validate_promoted_signal_intelligence.py` | Structural PSI compliance |
| Runtime loader consumes production PSI? | **No on launch-critical path** | `backend/tests/unit/test_arch_rt5e_psi_runtime_wiring_decision.py` — launch-critical modules do **not** import `load_promoted_signal_intelligence` |
| Effect of opt-in today | **Validation / lifecycle inventory only** | `behavioural_impact: NONE` on opted-in packages |
| Duplicate authority | **No cross-ID placements after remediation** | Staged pilot copies remain under `generated_pilot/`; 18 ID-matched production copies only |

**STOP gate 1 — Runtime boundary:** **PASS.**

## 2. Existing production opt-in overlap findings

| Metric | Value |
|---|---|
| Pre-existing production PSI opt-ins | 20 (`pkg_kb47_*`) |
| Overlap with P1-14 activation-ready candidates | **None** |

**STOP gate 2 — Existing opt-in conflict:** **PASS.**

## 3. Candidate mapping summary (post-remediation)

Mapping artefact: `P1-15_production_psi_opt_in_mapping.yaml`

| Classification | Count |
|---|---|
| Production PSI opt-ins completed (ID-matched) | **18** |
| `BLOCKED_AMBIGUOUS_PACKAGE_MAPPING` | **4** |
| Cross-ID opt-ins remaining | **0** |

**18 clean opt-ins:** staged `package_id` matches production directory name exactly.

**4 deferred candidates:** staged `pkg_kb52c_rbc_*` / `pkg_kb52c_rdw_cv_*` artefacts have no matching `pkg_kb52c_*` production package. An initial P1-15 attempt mapped them to `pkg_kb58_*` by `source_spec_id`; GPT architectural review (Option B) rejected cross-ID production PSI placement because staged PSI internal `package_id` remains `pkg_kb52c_*`. Those four cross-ID production opt-ins were **reverted** in remediation.

## 4. Final opted-in cohort

**18/22** activation-ready candidates retain governed production PSI opt-in:

- Byte-identical PSI copied from staged pilot to ID-matched production package
- `promoted_signal_intelligence: promoted_signal_intelligence.yaml` on each of 18 manifests
- `behavioural_impact: NONE` preserved
- No changes to `research_brief.yaml` or `signal_library.yaml`

**4 deferred** pending package identity/provenance adjudication (see section 5).

Representative opted-in packages: `pkg_kb60_total_cholesterol_high_atherogenic_hypercholesterolemia`, `pkg_kb52c_alt_high_hepatocellular_injury_pattern`, `pkg_kb52c_ferritin_low_iron_store_depletion`.

## 5. Blocked / deferred candidates

| Staged package | Classification | Reason |
|---|---|---|
| `pkg_kb52c_rbc_high_erythrocytosis_pattern` | `BLOCKED_AMBIGUOUS_PACKAGE_MAPPING` | No `pkg_kb52c_*` production home; cross-ID `pkg_kb58_*` opt-in reverted |
| `pkg_kb52c_rbc_low_iron_restricted_anemia_pattern` | `BLOCKED_AMBIGUOUS_PACKAGE_MAPPING` | Same |
| `pkg_kb52c_rdw_cv_high_iron_deficiency_anisocytosis` | `BLOCKED_AMBIGUOUS_PACKAGE_MAPPING` | Same |
| `pkg_kb52c_rdw_cv_high_mixed_red_cell_population_pattern` | `BLOCKED_AMBIGUOUS_PACKAGE_MAPPING` | Same |

P1-14 blocked cohorts (9 biomarker, 7 derived, 3 medical-review) were **not** opted in.

## 6. Remediation (GPT Option B)

Reverted only:

- `pkg_kb58_rbc_high_erythrocytosis_pattern`
- `pkg_kb58_rbc_low_iron_restricted_anemia_pattern`
- `pkg_kb58_rdw_cv_high_iron_deficiency_anisocytosis`
- `pkg_kb58_rdw_cv_high_mixed_red_cell_population_pattern`

Actions: removed `promoted_signal_intelligence:` from each manifest; deleted copied PSI files. No staged PSI content changed. No medical content changed.

## 7. Validation commands and outputs (post-remediation)

```powershell
python backend/scripts/validate_knowledge_package.py --package-dir knowledge_bus/packages/<pkg>
python backend/scripts/validate_promoted_signal_intelligence.py --model knowledge_bus/packages/<pkg>/promoted_signal_intelligence.yaml
python backend/scripts/validate_staged_psi_activation_readiness.py
```

- Remaining 18 opted-in packages: **18/18 PASS** (package + PSI validation)
- Staged activation-readiness validator: 18 ID-matched staged packages report production opt-in (`NOT_ELIGIBLE_FOR_ACTIVATION`); 4 deferred candidates may remain `ACTIVATION_READY` on staged audit because matching `pkg_kb52c_*` production packages do not exist — acceptable because mapping now classifies them as `BLOCKED_AMBIGUOUS_PACKAGE_MAPPING`

## 8. Runtime / user-facing activation confirmation

- No runtime or user-facing behaviour introduced
- No staged PSI or staged compile manifest edits
- No medical content or biomarker ID changes
- No cross-ID `pkg_kb52c_* → pkg_kb58_*` opt-ins remain

## 9. Recommended next work

1. **Package identity/provenance adjudication** for the 4 deferred `pkg_kb52c_rbc_*` / `pkg_kb52c_rdw_cv_*` candidates before any production opt-in
2. **P1-16** — SSOT biomarker identity adjudication for biomarker-blocked staged cohort

## 10. Business value

Establishes an 18-package ID-matched production PSI opt-in pilot under validation-only contract boundaries, with explicit rejection and reversion of cross-ID placements that would create package identity mismatch.
