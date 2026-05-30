# LAUNCH-CORE-3 — Result Versioning, Replay and Regeneration Audit

**Generated:** 2026-05-30  
**Updated:** 2026-05-30 (documentation hardening — ReplayManifestV1 assessment + metadata gap table)  
**Work package:** `LAUNCH-CORE-3_result_versioning_replay_and_regeneration_policy`

## Final launch recommendation

**Proceed** with immutable-snapshot policy enforced in documentation and stale detection. Display **stale warning (behaviour B)**; plan **versioned regeneration (behaviour C)** without implementing regeneration job in this sprint.

## Current persistence paths

| Store | Location | Content |
|-------|----------|---------|
| Analysis session | `analyses` table | `raw_biomarkers`, `questionnaire_data`, `analysis_version`, `pipeline_version`, status |
| Client result snapshot | `analysis_results.processing_metadata['client_result_shape_v1']` | Full frontend DTO shape (immutable blob) |
| Replay | `analysis_results.replay_manifest` | ReplayManifestV1 JSON |
| In-process cache | `_analysis_results` dict | Same shape when DB unavailable |

Authority: `PersistenceService.save_live_analysis_after_run`, `AnalysisRepository`, `AnalysisResultRepository`.

## API retrieval paths

| Endpoint | Behaviour |
|----------|-----------|
| `GET /api/analysis/result` | Load snapshot → `build_analysis_result_dto` → attach `result_versioning` metadata |
| `POST /api/analysis/start` | New run; stamp policy meta; persist new snapshot |

## Are old results immutable today?

**Yes in practice** — no code path updates `client_result_shape_v1` in place after save. LAUNCH-CORE-3 makes this explicit and adds stale classification.

## Is raw source input available for regeneration?

**Yes** — `analyses.raw_biomarkers` and `questionnaire_data` are persisted on live runs. A future regeneration job can re-invoke the orchestrator without mutating the old snapshot.

## Is deterministic regeneration possible today?

| Mode | Feasible? |
|------|-----------|
| Re-render stored DTO only | Yes (current GET path) |
| Full pipeline replay from raw input | Yes (data present) |
| Same-analysis in-place refresh | **No** — forbidden by policy |

## ReplayManifestV1 `frozen=False` assessment

**Location:** `backend/core/contracts/replay_manifest_v1.py:21`

```python
model_config = ConfigDict(frozen=False, extra="forbid")
```

**Classification:** **Intentional assembly-time mutability** — not a launch-blocking contract defect. **Follow-up (low):** align class docstring with Pydantic semantics (see below).

### Why `frozen=False` is used today

| Factor | Assessment |
|--------|------------|
| Build path | `build_replay_manifest_v1()` constructs a `ReplayManifestV1` instance with many optional fields, then the orchestrator serialises once via `replay_manifest.model_dump(exclude_none=True)` (`orchestrator.py` ~2259). |
| Persisted shape | Stored value is **JSON** on `analysis_results.replay_manifest` and inside `client_result_shape_v1` — a plain `dict`, not a live Pydantic model. No production path rehydrates the manifest and mutates fields after save. |
| Mutable field types | `schema_hashes: Dict[str, str]` and `linked_snapshot_ids: List[str]` are populated during assembly; `frozen=True` would not prevent logical immutability but would complicate incremental population patterns without adding launch value. |
| Contract strictness | `extra="forbid"` **is** enforced — unknown manifest keys are rejected at validation time. |
| Docstring vs config | Class docstring describes the **persisted execution manifest** as immutable in the audit/replay sense (no timestamps, no env IDs, deterministic hashes). That refers to **stored snapshot semantics**, not `ConfigDict(frozen=...)`. |

### Why this is safe for LAUNCH-CORE-3

1. **Immutability policy applies to persisted client results**, not to transient builder objects. Once `model_dump` runs, the snapshot is written to `processing_metadata['client_result_shape_v1']` and `analysis_results.replay_manifest` without a subsequent in-place update path.
2. **GET /api/analysis/result** attaches read-only `result_versioning` metadata; it does not modify `replay_manifest` or re-instantiate `ReplayManifestV1` for mutation.
3. **Deterministic replay evidence** is carried by the serialised hash/version fields inside the dumped JSON (registry versions, `*_hash` fields, `burden_hash`, `lifestyle_input_hash`, `schema_hashes`), not by Pydantic instance freezing at runtime.

### Follow-up (non-launch)

| Item | Recommendation |
|------|----------------|
| Doc clarity | Amend `ReplayManifestV1` docstring to state “immutable **after serialisation**; model is mutable only during orchestrator assembly.” |
| Optional hardening | Consider `frozen=True` **after** builder returns if future code paths ever retain live instances on the request lifecycle (not required for Wave 1). |
| Estate-level hashes | `active_authority_manifest_hash` / `compiled_estate_index_hash` are **not** manifest fields today — track under metadata gap table below, not as `frozen=False` defect. |

**Conclusion:** `frozen=False` is **intentional** for assembly and one-shot serialisation. It does **not** weaken the LAUNCH-CORE-3 immutable persisted-result policy.

---

## Required metadata model — field-by-field gap table

Source requirement: LAUNCH-CORE-3 prompt “Required metadata model”. This table maps each prompt field to **current repository support** as of this audit (post-implementation). Classifications: **present**, **partial**, **gap**, **not applicable**.

| Required field | Status | Current support / location | Notes |
|----------------|--------|---------------------------|-------|
| `analysis_id` | **present** | `analyses.id` (UUID PK); DTO root `analysis_id`; FK `analysis_results.analysis_id` | Primary session key; one result row per analysis today. |
| `result_version_id` | **gap** | — | No distinct version-row identifier. Closest surrogate: `analysis_results.id` (result PK) is not exposed as `result_version_id` and does not support multiple versions per analysis. |
| `parent_analysis_id` / `source_analysis_id` | **partial** | `ReplayManifestV1.linked_snapshot_ids` (longitudinal prior analyses only) | List of prior `analysis_id` values for state-transition context — **not** regeneration parent linkage. No `parent_analysis_id` column. |
| `raw_input_hash` | **gap** | — | Upload/raw file bytes not hashed at persistence boundary. `analyses.raw_biomarkers` stores parsed JSON only. |
| `parsed_biomarker_payload_hash` | **gap** | — | No canonical SHA-256 of normalised biomarker panel persisted on analysis/result. |
| `questionnaire_hash` | **gap** | `analyses.questionnaire_data` (JSON, **present** as raw payload) | Content retained but **not** content-addressed; hash not stored. |
| `engine_version` | **partial** | `analyses.analysis_version` (semver string, default `1.0.0`) | Named `analysis_version` in schema — semantic overlap with “engine version” but not a separate `engine_version` field. |
| `pipeline_version` | **present** | `analyses.pipeline_version` (semver string, default `1.0.0`) | Persisted on analysis row at session create. |
| `result_schema_version` | **partial** | `analysis_results.result_version`; DTO `result_version`; `ReplayManifestV1.analysis_result_version` | Three related stamps — DTO/DB `result_version` and manifest `analysis_result_version` (default `1.0.0`). No separate `result_schema_version` column name. |
| `knowledge_estate_version` | **gap** | Repo SSOT: `knowledge_bus/compiled/estate_index_v1.yaml` (runtime/CI only) | Estate index not stamped onto persisted result metadata. Subsystem `source_trace` strings reference artefact IDs but are not a single estate version field. |
| `active_authority_manifest_hash` | **gap** | `docs/audit-papers/active_intelligence_authority_manifest.md` (governance doc, not hashed on result) | Validated in ARCH-RT guardrails; **not** persisted on analysis/result. |
| `compiled_estate_index_hash` | **gap** | — | Estate index has no content hash stored on `analyses` / `analysis_results` / `replay_manifest`. |
| `compile_manifest_hashes` | **partial** | Per-artefact `compile_manifest_ref` in KB compiled YAML; `ReplayManifestV1` registry `*_hash` fields (scoring, evidence, relationship, etc.) | Orchestrator stamps **component registry hashes** into replay manifest — not a bundle hash of all `knowledge_bus/compiled/manifests/*.yaml` entries. |
| `prompt_template_version` / `prompt_template_hash` | **partial** / **not applicable** | Runtime: insight synthesis / LLM paths may use template objects in-process | Narrative generation templates are **not** persisted on the client-result snapshot. Classify hash as **gap** for persisted audit; template versioning as **N/A** until LLM outputs are part of immutable replay contract. |
| `generated_at` | **present** | `analysis_results.created_at`; DTO `created_at` (ISO string from orchestrator) | Wall-clock timestamp on result row and DTO. Replay manifest explicitly excludes timestamps for determinism. |
| `result_payload_hash` | **gap** | — | No SHA-256 over canonical `client_result_shape_v1` JSON at save time. |
| `supersedes_result_version_id` | **gap** | — | No supersession lineage model. |
| `superseded_by_result_version_id` | **gap** | — | No supersession lineage model. |
| `regeneration_reason` | **gap** | — | Regeneration job not implemented; `result_versioning.regeneration_available` is `false`. |

### LAUNCH-CORE-3 policy stamps (prompt-adjacent, implemented)

| Field | Status | Location |
|-------|--------|----------|
| `meta.completeness_policy_id` | **present** (new runs) | Stamped via `stamp_current_policy_meta()` → `meta` on save; value `launch_core_1_subsystem_union_v1` |
| `meta.result_versioning_policy_id` | **present** (new runs) | Stamped via `stamp_current_policy_meta()`; value `launch_core_3_immutable_snapshot_v1` |
| `result_versioning` (API read model) | **present** | `build_result_versioning_metadata()` on GET only — not persisted inside snapshot |

### Where support concentrates today

| Mechanism | Fields covered |
|-----------|----------------|
| **`ReplayManifestV1`** (JSON column + DTO `replay_manifest`) | `manifest_version`, registry versions/hashes, `burden_hash`, `lifestyle_input_hash`, `schema_hashes`, `analysis_result_version`, `linked_snapshot_ids` |
| **`AnalysisResult.result_version`** | DTO/schema version gate (LC-S20 + LC-3 stale check) |
| **`analyses` row** | `raw_biomarkers`, `questionnaire_data`, `analysis_version`, `pipeline_version`, `created_at` |
| **`analysis_results.processing_metadata['client_result_shape_v1']`** | Full immutable frontend DTO blob |
| **Missing lineage layer** | `result_version_id`, parent/supersedes IDs, input/payload hashes, estate/authority hashes, `regeneration_reason` |

### Summary counts (prompt required fields)

| Classification | Count (19 prompt fields) |
|----------------|--------------------------|
| present | 4 (`analysis_id`, `pipeline_version`, `generated_at`, plus engine via partial row) |
| partial | 6 |
| gap | 11 |
| not applicable | 0 (prompt_template_hash counted under partial/N/A in row note) |

**Audit implication:** Implementation correctly scoped to **stale detection + policy stamps**; full metadata/lineage remains a **follow-on migration sprint**, consistent with architecture policy doc.

---

## Stale analysis examples (LAUNCH-CORE-2)

| Analysis ID | Classification | Reasons |
|-------------|----------------|---------|
| `18e14232-9f93-45e6-820c-004ab5a16235` | **stale** | Pre-LC-1 completeness (1/3 vs 2/4); policy meta missing |
| `bb695d3c-453e-4e49-abff-ae80587b4248` | **stale** | Legacy subsystem traces; `total_bilirubin` false-missing |
| `746f2b0a-b470-4d87-8ed8-e2c3d1e68c02` | **current** (post-LC-1 run) | Aligns with LC-1 presentation when policy stamped on future re-save N/A |

## Implementation performed

| Item | Path |
|------|------|
| Stale detection + metadata | `backend/core/dto/result_versioning_policy_v1.py` |
| API attachment | `backend/app/routes/analysis.py` |
| Policy stamp on new runs | `stamp_current_policy_meta` in start flow |
| Frontend banner | `frontend/app/components/results/StaleResultBanner.tsx` |
| Policy doc | `docs/architecture/LAUNCH-CORE-3_result_versioning_replay_and_regeneration_policy.md` |

**Not implemented:** regeneration job, DB lineage migration, destructive refresh.

## Tests run

```text
python -m pytest backend/tests/unit/test_launch_core3_result_versioning.py -q
python backend/scripts/validate_day_one_architecture.py
python -m pytest backend/tests/architecture/test_day_one_architecture_guardrails.py -q
cd frontend && npm test -- tests/components/StaleResultBanner.test.tsx
```

## Remaining risks

| Risk | Mitigation |
|------|------------|
| Heuristic false positive/negative on stale | Extend reasons; add analysis_id allowlist only for audit |
| Users confused by stale banner | Copy + future regenerate CTA |
| History lists stale analyses | Future filter or regen workflow |

## ARCH-RT-6

Guardrails **unchanged** — validator PASS; no clinical logic modified.

## Documentation hardening (Claude re-audit)

| Condition | Status |
|-----------|--------|
| ReplayManifestV1 `frozen=False` explicit assessment | **Addressed** (see section above) |
| Required metadata field-by-field gap table | **Addressed** (see section above) |
| Implementation / policy code changes for this patch | **None** (audit doc only) |

**Re-audit readiness:** Implementation unchanged; audit paper now satisfies both documentation-hardening conditions from the failed audit.
