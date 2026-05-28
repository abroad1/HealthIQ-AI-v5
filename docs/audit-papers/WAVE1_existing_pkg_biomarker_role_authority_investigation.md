# Wave 1 Existing Package Biomarker Role Authority Investigation

## 1. Executive verdict
Existing package role authority is **partially sufficient but not directly consumable as-is** for Health Systems Card marker roles.

- There is a governed role model in package signal assets (`supporting_metrics[].role`) with enforced vocab.
- But Wave 1 subsystem evidence currently does not consume package roles at all; it uses manual expected marker maps.
- Package role authority mainly describes **signal-supporting marker semantics**, while the card needs **domain/subsystem UI semantics** (score vs confidence vs context vs missing-for-confidence).
- `total_bilirubin` has no package-role coverage (canonical package usage is `bilirubin`), so subsystem equivalence still needs governed handling.

Verdict: **Option B** (backend-governed translation layer from existing package roles to card roles) is the best architecture, with selective package-role extension only where truly missing.

## 2. Package role authority inventory

| File | Package/domain | Role field | Role values | Runtime-used? | Authoritative? |
|---|---|---|---|---|---|
| `knowledge_bus/packages/*/signal_library.yaml` | Knowledge Bus package signal libraries | `signals[].supporting_metrics[].role` | `mechanism_marker`, `severity_marker`, `contextual_marker`, `corroborator`, `differential_marker` | Loaded in runtime via `SignalRegistry` (`signal_evaluator.py`), but role value itself is not consumed by scoring flow today | Yes (package-governed) |
| `knowledge_bus/schema/signal_library_schema.yaml` | Schema authority for signal library | `supporting_metric_object_field_rules.role` | Same 5-value enum above | Used in validator pipeline (`validate_signal_library.py`) | Yes (contract authority) |
| `backend/scripts/validate_signal_library.py` | Signal library contract enforcement | `_SUPPORTING_ROLES` | Same 5-value enum above | Yes (validation gate) | Yes (enforcement authority) |
| `knowledge_bus/packages/*/promoted_signal_intelligence.yaml` | Promoted signal intelligence package assets | `signals[].supporting_markers[].role` | Above 5 + `exclusion_marker` | Validation/fixture usage present; no evidence of production scoring orchestration consumption path | Governed, but runtime usage currently limited |
| `knowledge_bus/schema/promoted_signal_intelligence_schema_v1.yaml` | Promoted signal schema authority | `role_allowed` | Above 5 + `exclusion_marker` | Used by `validate_promoted_signal_intelligence.py` | Yes (contract authority) |
| `backend/scripts/validate_promoted_signal_intelligence.py` | Promoted signal validator | `_ROLES` | Above 5 + `exclusion_marker` | Yes (validation gate) | Yes (enforcement authority) |
| `backend/ssot/biomarkers.yaml` | SSOT biomarker metadata | `roles` | Present but mostly empty (`[]`) | No active runtime consumers found | Weak/latent authority (not currently operational) |

## 3. Existing role vocabulary
Exact role vocabulary as implemented in governed package contracts:

From `signal_library` contract/runtime validators:
- `mechanism_marker`
- `severity_marker`
- `contextual_marker`
- `corroborator`
- `differential_marker`

From `promoted_signal_intelligence` contract/runtime validators:
- `mechanism_marker`
- `severity_marker`
- `contextual_marker`
- `corroborator`
- `differential_marker`
- `exclusion_marker`

Important implementation nuance:
- `signal_library` has explicit role only for **supporting metrics**.
- `primary_metric` has no explicit role field; it is an implied anchor/primary signal driver.

## 4. Wave 1 marker role coverage matrix

| Marker | Current subsystem | Existing package role | Source file | Directly usable? | Notes |
|---|---|---|---|---|---|
| `total_cholesterol` | CV lipid transport | Yes (supporting: `corroborator`/`differential_marker`; primary in TC packages) | `pkg_kb60_tc_hdl_ratio_*`, `pkg_kb60_total_cholesterol_*` signal libraries | Partial | Role exists in signal context, not card/subsystem context |
| `ldl_cholesterol` | CV lipid transport | Yes (primary + supporting `corroborator`/`differential_marker`/`mechanism_marker`) | `pkg_kb52c_ldl_high_*`, `pkg_s24_ldl_high_*` | Partial | Strong coverage |
| `hdl_cholesterol` | CV lipid transport | Yes (primary + supporting `corroborator`) | `pkg_kb52c_hdl_low_*`, `pkg_s24_hdl_*` | Partial | Strong coverage |
| `triglycerides` | CV lipid transport; Blood sugar insulin/met context | Yes (primary + supporting `corroborator`/`mechanism_marker`/`differential_marker`) | `pkg_kb52c_triglycerides_high_*`, multiple KB lipid/metabolic packages | Partial | Supports cross-context semantics; requires translation for domain-specific UI role |
| `tc_hdl_ratio` | CV lipid transport | Yes (primary + supporting `corroborator`/`differential_marker`) | `pkg_kb60_tc_hdl_ratio_*`, `pkg_kb60_total_cholesterol_*` | Partial | Strong coverage |
| `homocysteine` | CV homocysteine pathway | Yes (primary + supporting mostly `mechanism_marker`) | `pkg_kb52c_homocysteine_high_*`, `pkg_s24_homocysteine_high_*` | Partial | Coverage exists but not wired to subsystem model |
| `crp` | CV vascular strain context | Yes (primary in inflammatory package; supporting in others with `contextual_marker`/`severity_marker`/`mechanism_marker`/`differential_marker`) | `pkg_s24_crp_high_inflammation`, several KB packages | Partial | Package authority treats CRP as inflammatory; card currently rehomes under CV subsystem |
| `glucose` | Blood sugar glycaemic control | Yes (supporting `corroborator` in HbA1c package; primary in other metabolic packages) | `pkg_kb52c_hba1c_high_*` and other KB packages | Partial | Good evidence for confidence/corroboration |
| `hba1c` | Blood sugar glycaemic control | Yes (primary in multiple packages) | `pkg_kb52c_hba1c_high_*`, `pkg_s24_hba1c_high_*` | Partial | Primary metric role implied, not explicit role field |
| `insulin` | Blood sugar insulin/met context | No package role found in current KB signal libraries | N/A | No | Major coverage gap for current subsystem marker set |
| `alt` | Liver enzyme pattern | Yes (primary + supporting `corroborator`/`differential_marker`/`mechanism_marker`) | `pkg_kb52c_alt_high_*`, `pkg_s24_alt_high_*` | Partial | Strong package coverage |
| `ast` | Liver enzyme pattern | Yes (supporting `corroborator`) | `pkg_kb52c_alt_high_*` | Partial | Supporting-role coverage |
| `ggt` | Liver enzyme pattern | Yes (primary + supporting `differential_marker`) | `pkg_kb52c_ggt_high_*`, `pkg_s24_ggt_high_*` | Partial | Strong package coverage |
| `alp` | Liver processing context | Yes (primary + supporting `corroborator`/`differential_marker`/`mechanism_marker`) | `pkg_kb52c_alp_high_*`, `pkg_s24_alp_high_*` | Partial | Strong package coverage |
| `albumin` | Liver processing context | Yes (primary + supporting `corroborator`/`differential_marker`/`mechanism_marker`) | `pkg_kb52c_albumin_low_*`, `pkg_s24_albumin_low_*` | Partial | Strong package coverage |
| `bilirubin` | Liver processing context | Yes (primary + supporting `corroborator`/`differential_marker`/`mechanism_marker`) | `pkg_kb52c_bilirubin_high_*`, `pkg_kb45_bilirubin_high_*` | Partial | Canonical package marker coverage is on `bilirubin` |
| `total_bilirubin` | Liver processing context | No | N/A | No | Not present in package role definitions; canonical package model uses `bilirubin` |

## 5. Role alignment analysis
Current Wave 1 subsystem evidence **flattens and bypasses** existing package role authority:

- `wave1_subsystem_evidence.py` uses manual expected marker sets and emits included/missing only.
- `SubsystemEvidenceV1.evidence_role` exists but is always `null`.
- UI (`Wave1SubsystemEvidenceSection.tsx`) renders all included markers as equivalent evidence chips.

Alignment/conflict highlights:

- **CRP in CV context**: package authority mostly frames CRP in inflammatory signal context; current card presents it as a cardiovascular subsystem marker (`Vascular strain context`) without role differentiation.
- **Homocysteine in CV**: package role data can support contextual/mechanistic interpretation, but card currently treats it as generic included marker.
- **Triglycerides in CV + blood sugar**: package model supports multi-role behavior across different signals; current subsystem model duplicates marker without clarifying role per context.
- **Liver markers (GGT/ALP/albumin/bilirubin)**: package roles can express corroborator/differential/mechanism; current card surfaces them as undifferentiated included markers.
- **`total_bilirubin`**: package authority does not include it, reinforcing that current subsystem expectation key is outside package role authority.

## 6. Translation-layer assessment
Yes, a backend/governed translation layer is needed.

Why direct surfacing is insufficient:
- Package roles are signal-level and technical.
- Health Systems Card needs simplified, user-safe, domain/subsystem-semantic roles.
- `primary_metric` has no explicit role field, so card-facing “score contributor” requires governed derivation, not raw passthrough.

Recommended governed mapping pattern:

`package role + primary/supporting context + signal/domain mapping`  
-> `card marker role`

Example mapping candidate:
- primary metric -> score contributor
- corroborator / severity_marker -> confidence support
- contextual_marker / mechanism_marker -> context marker (or confidence support depending on domain rule)
- differential_marker / exclusion_marker -> context/differential marker

This must remain backend-side/governed, not frontend-derived.

## 7. DTO implications
`SubsystemEvidenceV1` should emit per-marker role fields (not just subsystem-level `evidence_role`).

Current shape limitation:
- only `included_marker_ids` / `missing_marker_ids` + display labels
- cannot communicate marker role semantics

Recommended shape direction (conceptual, not implementation):
- extend marker rows (included/missing) with a role field
- include optional provenance source (e.g., package/signal trace id) for auditability

This can be introduced without changing scoring logic if treated as **presentation metadata** only.

## 8. Medical-review concern check
Existing package roles can address most medical-review concerns if translated properly:

- **CRP as full subsystem vs context**: yes, role translation can downgrade to context/confidence support.
- **Homocysteine as advanced/context evidence**: yes, package semantics support contextual framing.
- **Triglycerides dual-use (CV score vs blood sugar context)**: yes, translation can represent different roles by subsystem/domain context.
- **Liver marker differentiation (GGT/ALP/albumin/bilirubin)**: yes, package role types can separate corroborative/context/differential semantics from core scoring markers.
- **Optional markers shown as required missing**: partially; package availability (`common/specialist/optional`) helps, but subsystem expected-marker policy still requires governed rules to avoid false-required presentation.

Unresolved edge:
- `total_bilirubin` is not represented in package role authority, so package roles alone cannot solve that mismatch.

## 9. Gaps and risks

- Gap: `insulin` was not found in current KB signal-library role definitions, despite being in Wave 1 blood-sugar subsystem expected markers.
- Gap: `primary_metric` role is implicit, not explicit role field.
- Gap: `total_bilirubin` absent from package role authority.
- Risk: introducing card roles independently of package authority would create a second competing role model.
- Risk: frontend-side role mapping would violate authority boundaries.
- Risk: role translation could accidentally alter scoring behavior if mixed into evaluator logic instead of metadata-only assembly.

## 10. Recommended next work package

- **work_id:** `WAVE1-SUBSYS-R3_pkg_role_to_card_role_translation`
- **risk level:** HIGH (MIXED)
- **files likely touched:**
  - `backend/core/analytics/wave1_subsystem_evidence.py`
  - `backend/core/models/results.py`
  - `backend/core/analytics/domain_score_assembler.py` (if metadata pass-through needed)
  - `backend/core/analytics/signal_evaluator.py` or KB adapter layer (read-only role extraction path only)
  - `frontend/app/types/analysis.ts`
  - `frontend/app/components/results/Wave1SubsystemEvidenceSection.tsx`
  - `backend/tests/regression/test_domain_ux1c_governed_subsystem_evidence.py`
- **exact implementation principle:**
  - Reuse existing package role authority first.
  - Add a governed backend translation layer from package role vocabulary to card display roles.
  - Emit role metadata in subsystem DTO without changing score calculations or subsystem expected marker maps in the same work package unless explicitly approved.
- **what must not change:**
  - scoring policy/weights/thresholds
  - unit normalization
  - reference ranges
  - KB clinical content meanings
  - IDL/roots-cause logic
  - frontend-derived role inference

