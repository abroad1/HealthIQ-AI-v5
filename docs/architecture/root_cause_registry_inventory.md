# Root Cause Registry Inventory

**Work package:** ARCH-RT-0  
**Generated:** 2026-05-28

## Hypothesis YAML corpus

| Metric | Value |
|--------|------:|
| Location | `knowledge_bus/root_cause/hypotheses/` |
| File count (`*.yaml`) | 40 |
| Example files | `alt_hypotheses_v1.yaml`, `hcy_hypotheses_v1.yaml`, `hba1c_hypotheses_v1.yaml` |

## Registry implementation

| Component | Path |
|-----------|------|
| Registry | `backend/core/knowledge/root_cause_registry_v1.py` |
| Hypothesis loaders | `backend/core/knowledge/load_root_cause_hypotheses.py` |
| Runtime consumer | `backend/core/analytics/root_cause_compiler_v1.py` |
| Confirmatory tests registry | `knowledge_bus/registries/confirmatory_tests_v1.yaml` |
| Confirmatory loader | `backend/core/knowledge/load_confirmatory_tests_registry.py` |

## Registered targets

| Metric | Count |
|--------|------:|
| `ROOT_CAUSE_TARGET_SPECS` entries | 41 |
| Distinct hypothesis YAML files referenced | 40 (one YAML shared by two signal targets) |

## Shared YAML usage (duplicate target)

| `signal_id` (registry key) | Hypothesis asset |
|----------------------------|------------------|
| `signal_homocysteine_elevation_context` | `hcy_hypotheses_v1.yaml` |
| `signal_homocysteine_high` | `hcy_hypotheses_v1.yaml` |

## Provenance gaps

| Issue | Status |
|-------|--------|
| `source_spec_id` on hypothesis YAML | **UNKNOWN** — not verified field-by-field in this sprint |
| Link from investigation spec → hypothesis YAML | **MISSING** for most packages; manual tuple in registry |
| Pass 3 `hypotheses` block in investigation spec | **Not compiled** to YAML automatically (see activation compile gap) |

## Proposed transition direction

**Phase 1 (ARCH-RT-1..2):** Retain **manual tuple** in `root_cause_registry_v1.py` for launch parity; add **provenance fields** on registry rows (`source_spec_id`, `hypothesis_asset_hash`).

**Phase 2 (ARCH-RT-3+):** **Compiled hypothesis artefact** emitted from investigation spec compile; registry becomes **manifest-backed index** pointing at compiled assets (not hand-maintained parallel YAML).

**Phase 3:** Optional **generated registry** from compile manifest estate index; deprecate hand-edited tuples when parity gates pass.

**Rejected for day-one:** Direct consumption of raw investigation spec at runtime.

See `ADR-RT-003_hypothesis_artefact_and_root_cause_transition.md`.
