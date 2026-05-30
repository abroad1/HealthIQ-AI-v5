# Compiled Hypothesis Contract

**Status:** DRAFT (ARCH-RT-4 pilot)  
**Authority:** ADR-RT-003, ADR-RT-008

## Purpose

Define governed compiled hypothesis artefacts as the future WHY authority, while legacy `knowledge_bus/root_cause/hypotheses/*.yaml` (`schema_version: "v1"`) remains runtime authority during pilot.

## Investigation specs

- Investigation specs do **not** currently expose a formal `hypotheses` block.
- Pilot artefacts are **manual translations** from `evidence.*`, `narrative.*`, and `supporting_markers` content.
- Runtime must **not** read raw investigation specs to build WHY output.
- A future activation/hypothesis compiler may automate translation; that is out of scope for ARCH-RT-4.

## PSI

- PSI remains signal-layer semantics only (ADR-008).
- Hypothesis graphs must **not** be placed into PSI.
- Compiled hypothesis loader does not consume PSI artefacts.

## Legacy root-cause YAML

- Legacy files use `schema_version: "v1"` (string), validated by `load_root_cause_hypotheses._load_hypotheses_asset`.
- Compiled artefacts use semver `1.0.0`, validated by `compiled_hypothesis.validate_compiled_hypothesis_payload`.
- Cross-loading fails closed (legacy loader rejects `1.0.0`; compiled loader rejects `v1`).
- Legacy YAML must not be deleted or rewritten during pilot.

## root_cause_registry

- Production registry: `ROOT_CAUSE_TARGET_SPECS` in `root_cause_registry_v1.py` (41 manual entries).
- Pilot shadow registry: `COMPILED_HYPOTHESIS_PILOT_SPECS` in `compiled_hypothesis_registry_v1.py` — **separate module**, never merged into `get_root_cause_targets()`.
- Import-time validation of all 41 legacy assets must remain unchanged.

## Confirmatory test registry

- When `confirmatory_tests` is non-empty on a compiled hypothesis row, each `test_id` must exist in `confirmatory_tests_v1`.
- Vitamin D pilot uses empty confirmatory tests (same as legacy YAML); mapping mechanism is documented for future pilots.

## Multi-frame signal identity (ADR-RT-002)

- `activation_key` is required on compiled artefacts.
- `signal_id` remains signal-family identity.
- Root-cause compiler still selects targets by **`signal_id` first match only** — not `activation_key`.
- Pilot `signal_vitamin_d_low` is single-frame; no silent frame selection.
- Multi-frame pilots require explicit frame-selection policy before runtime promotion.

## Provenance fields

| Value | Meaning |
|-------|---------|
| `explicit` | Canonical `source_spec_id` from governed compile manifest |
| `source_document_derived` | Derived from `source_document` path / spec filename |
| `package_id_inferred` | Inferred from package manifest |
| `manual_pilot` | Hand-authored pilot only |

## Divergence handling

- Every pilot requires `ARCH-RT-4_root_cause_divergence_report.md` (or generated comparison via `root_cause_divergence_v1`).
- Material unresolved divergence **blocks** runtime registry promotion.
- Shadow loading may proceed when recommendation is `acceptable` or `acceptable_with_carry_forward`.

## Estate migration prerequisites

- Explicit vs inferred `source_spec_id` resolution
- Multi-frame root-cause compiler policy
- Real `compile_manifest_ref` (not pilot manual string)
- Clinical adjudication of divergence for each signal family
