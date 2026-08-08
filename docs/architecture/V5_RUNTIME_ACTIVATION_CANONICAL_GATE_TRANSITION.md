# V5 Runtime Activation — Canonical Gate Transition (updated)

**Supersedes:** the implementation-map section of the `V5-RUNTIME-AUTHORITY-INTEGRITY-1` transition note for current architecture status.
**Updated by:** `V5-CANONICAL-ACTIVATION-GATE-1`
**Claim boundary:** non-launch-critical cohort only. **Not** estate-wide single-authority convergence.

## What now grants activation

| Cohort | Grant authority | Status |
|---|---|---|
| Non-launch-critical governed frames | `package_runtime_activation_register_v1.yaml` via `canonical_runtime_activation_gate_v1.non_launch_frame_activation_exclusion_reason` (consumed by `SignalRegistry._load`) | **Canonical for this cohort** |
| Launch-critical `pkg_kb47_*` | `package_runtime_eligibility_v1` lineage (`EXPLICIT_SPEC` / `COMPILED_MANIFEST`) | **Temporary ratified exception** — Stage 2 fold-in required |

## What only constrains / vetoes

| Mechanism | Role |
|---|---|
| Package eligibility (non-launch branch) | Package-level mirror/precondition of register membership — not an independent grant |
| Provenance status | Lineage honesty / launch-critical safety input |
| Frame runtime authority (`REJECTED`) | Hard veto even if a key were listed |
| Explicit medical prohibitions | Load-time veto inside the canonical gate + write-path / day-one integrity validation |
| Non-governed harness libraries | Out-of-estate fixture bypass; not production grant authority |

## Legacy grant path demoted

- Non-launch frames no longer obtain activation through ad hoc peer mechanisms; loader grant for that cohort is solely the canonical gate wrapper over the activation register (+ explicit-prohibition veto).
- Independent bootstrap-by-snapshot without integrity checks is retired as an acceptable write process; programmatic mutations must use `activation_register_mutation_v1` / `mutate_runtime_activation_register.py`, which fail closed on prohibition + basic package preconditions.

## Remaining carry-forward (genuinely required)

**Stage 2 package (immediate follow-on):** fold `pkg_kb47_*` into the canonical activation register so those frames also require register membership, while **preserving** provenance/lineage safety constraints as vetoes/preconditions (not as a second grant authority).

Until Stage 2 completes, V5 retains **two** activation-grant authorities by deliberate temporary exception — one canonical (non-launch), one legacy cohort-specific (launch-critical). Do not describe the estate as fully converged.

## Further consolidation?

After Stage 2 fold-in: evaluate whether harness `governed=False` bypass semantics need tighter documentation or test-only guards. No full `SignalRegistry` rewrite is required for activation-gate integrity.
