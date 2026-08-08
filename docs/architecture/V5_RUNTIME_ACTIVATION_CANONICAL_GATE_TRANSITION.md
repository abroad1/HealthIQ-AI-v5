# V5 Runtime Activation — Canonical Gate Transition (Stage 2 complete)

**Updated by:** `V5-CANONICAL-ACTIVATION-GATE-2`
**Supersedes:** Stage 1 temporary two-authority exception documentation.

## Estate-wide positive activation authority

**One positive runtime activation-grant authority now exists estate-wide:**

`knowledge_bus/governance/package_runtime_activation_register_v1.yaml`
via `canonical_runtime_activation_gate_v1.canonical_frame_activation_exclusion_reason`
consumed by `SignalRegistry._load` for **all** governed packages (non-launch and `pkg_kb47_*`).

A governed frame is runtime-reachable only when:

> canonical activation grant
> AND all applicable eligibility / provenance / safety constraints
> = runtime reachable

## What only constrains / vetoes

| Mechanism | Role |
|---|---|
| Launch-critical provenance/lineage (`package_runtime_eligibility_v1`) | **Prerequisite / veto only** for `pkg_kb47_*` — cannot independently grant activation |
| Package eligibility (non-launch branch) | Package-level mirror of register membership |
| Frame runtime authority (`REJECTED`) | Hard veto even if listed in the register |
| Explicit medical prohibitions | Load-time veto + write-path / day-one integrity |
| Non-governed harness libraries | Out-of-estate fixture bypass only |

## Temporary Stage 1 exception — RETIRED

Stage 1 documented a temporary second grant for launch-critical packages via lineage eligibility without register membership. That exception is **retired**.

The six previously lineage-granted Wave 1 frames are now canonical register members:

- `signal_egfr_low::inv_egfr_low_chronic_kidney_function_reduction`
- `signal_egfr_low::inv_egfr_low_hemodynamic_filtration_drop`
- `signal_free_t3_high::inv_free_t3_high_t3_predominant_thyrotoxicosis`
- `signal_free_t3_low::inv_free_t3_low_low_t3_syndrome`
- `signal_free_t4_high::inv_free_t4_high_thyrotoxicosis_context`
- `signal_free_t4_low::inv_free_t4_low_thyroid_hormone_deficiency`

Fourteen lineage-blocked `pkg_kb47_*` packages remain unreachable and were **not** added to the register.

## Write path

`activation_register_mutation_v1` accepts launch-critical mutations only when lineage eligibility already passes, and still fail-closes on medical prohibitions / identity / integrity failures.

## Further activation-gate convergence?

No further positive-authority consolidation sprint is required for the governed estate. Remaining optional hygiene (harness `governed=False` documentation) is non-blocking and not a second grant authority.
