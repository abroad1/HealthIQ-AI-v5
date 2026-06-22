# ADR-FERRITIN-HIGH-SIGNAL-AUTHORITY-RECONCILIATION-1 — Ferritin-High Signal Authority

## Status

Accepted — implemented P1-21.

## Date

2026-06-22

## Context

`pkg_s24_ferritin_high_overload` is legacy Knowledge Bus authority for `signal_ferritin_high`. It defines the signal only through `signal_library.yaml` (`library.package_id: KBP-2404`), uses a validator-compatibility placeholder threshold (`9999.0`), and has no `promoted_signal_intelligence.yaml`. Two distinct Pass 3 ferritin-high PSI contexts are validated and activation-ready:

- `inv_ferritin_high_inflammatory_hyperferritinemia`
- `inv_ferritin_high_iron_overload_context`

P1-19 blocked host creation at Gate 3B due to `signal_id` collision with `pkg_s24`.

## Evidence

| Claim | Citation |
|-------|----------|
| Legacy `signal_ferritin_high` in pkg_s24 | `knowledge_bus/packages/pkg_s24_ferritin_high_overload/signal_library.yaml:8` |
| Placeholder threshold 9999.0 | `signal_library.yaml:32-35` |
| No production PSI | No `promoted_signal_intelligence.yaml` in pkg_s24 directory |
| Multi-package same `signal_id` precedent | `pkg_kb61_transferrin_low_*` pair sharing `signal_transferrin_high` |
| Ferritin production naming family | `pkg_kb52c_ferritin_low_iron_store_depletion` active production host |

## Decision — Option A (selected)

1. Retire `pkg_s24_ferritin_high_overload` from **active** authority via in-place manifest deprecation (`deprecated: true`, `deprecated_by: [...]`).
2. Do **not** move or delete the pkg_s24 directory (non-regression tests load it).
3. Do **not** modify pkg_s24 `signal_library.yaml`.
4. Promote two modern `pkg_kb52c_*` production packages with byte-copied Pass 3 PSI.
5. Retain `signal_id: signal_ferritin_high` for both packages — no new signal IDs.
6. No runtime evaluator or scoring policy changes in P1-21.

## Rejected options

- **Option B** — distinct signal IDs per clinical context: unnecessary evaluator surface risk.
- **Option C** — attach PSIs to pkg_s24: incoherent mixed legacy/modern host.

## Consequences

- Active ferritin-high intelligence authority migrates to Pass 3 PSI under `pkg_kb52c_ferritin_high_inflammatory_hyperferritinemia` and `pkg_kb52c_ferritin_high_iron_overload_context`.
- pkg_s24 remains on disk for test compatibility but is marked deprecated.
- No medical content invented; PSI files are byte-copies from staged compile artefacts.
