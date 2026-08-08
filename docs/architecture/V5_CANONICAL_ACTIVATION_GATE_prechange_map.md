# V5 Canonical Activation Gate — Pre-change Topology Map

**Work ID:** `V5-CANONICAL-ACTIVATION-GATE-1`  
**Branch:** `refactor/v5-canonical-activation-gate-1`  
**Scope decision:** canonicalise the **non-launch-critical** cohort only. Do not claim estate-wide single-authority convergence in this sprint.  
**Launch-critical carry-forward:** `pkg_kb47_*` remains a temporary ratified exception for the immediately following Stage 2 package.

## Baseline measurements (pre-change)

| Cohort | Loaded frames | Grant authority used |
|---|---:|---|
| Non-launch-critical | 172 | `package_runtime_activation_register_v1.yaml` (all 172 keys ⊆ register) |
| Launch-critical `pkg_kb47_*` | 6 | Lineage eligibility (`EXPLICIT_SPEC` / `COMPILED_MANIFEST`); register **not** consulted |
| Total `SignalRegistry` load | 178 | mixed |

## Mechanism map (live code)

| Mechanism | Location | Role pre-change | Classification |
|---|---|---|---|
| Package activation register | `package_activation_register_v1.py` ← `package_runtime_activation_register_v1.yaml` | Per-`activation_key` allow-list for non-launch frames (`signal_evaluator.py` former L139–149) | **GRANTS_ACTIVATION** (non-launch) — intended canonical grant |
| Package runtime eligibility | `package_runtime_eligibility_v1.py` L89–100 | Non-launch: package reachable iff any register membership (`is_package_runtime_activated`). Launch-critical: lineage grant without register | Non-launch: **CONSTRAINT / mirror** of register. Launch-critical: **GRANTS_ACTIVATION** (temporary exception) |
| Launch-critical cohort split | `is_launch_critical_package_id` (`package_runtime_eligibility_v1.py` L39–41); skip register in `signal_evaluator.py` L89, L139 | Routes `pkg_kb47_*` away from register gate | **LAUNCH_CRITICAL_TEMPORARY_EXCEPTION** |
| Provenance status | `provenance_status_v1.py` via eligibility L84–87 / loader L118 | Lineage honesty; feeds launch-critical grant and audit labels | **PROVENANCE / SAFETY CONSTRAINT** |
| Frame runtime authority | `frame_runtime_authority_v1.py`; loader L129–138 | Excludes WHY `authority_state == REJECTED` | **VETO / SAFETY CONSTRAINT** (not a grant) |
| Medical prohibition integrity | `runtime_medical_authority_integrity_v1.py`; day-one validator | Cross-checks register vs explicit `NOT_AUTHORISED*` / `blocked_targets` | **WRITE/CI VETO** (not yet load-time before this sprint) |
| Non-governed harness path | `signal_evaluator.py` L80–82 (`governed=False`) | Fixture libraries outside `knowledge_bus/packages/` skip register | **HARNESS BYPASS** (non-production estate) |

## Why Stage 1B is not a no-op

Two independent grant paths exist on current `main`:

1. Non-launch: key ∈ activation register ∧ not WHY-REJECTED  
2. Launch-critical: lineage-eligible `pkg_kb47_*` ∧ not WHY-REJECTED (register skipped)

Hardening STOP-2 candidate is resolved by **explicit disjoint-cohort framing**: this sprint canonicalises (1) only; (2) is documented as temporary and deferred to Stage 2 fold-in.

## Write / bootstrap paths

- No Python mutator existed for `package_runtime_activation_register_v1.yaml` before this sprint.
- Historical bootstrap: ARCH-CONV-E commit `a260c53` (snapshot); later E2/E3 manual YAML appends.
- Integrity validator was read-only post-hoc — no write-path guard.

## Intended post-change topology (this sprint)

| Cohort | Grants activation | Constrains / vetoes |
|---|---|---|
| Non-launch governed | **Only** canonical register gate (`canonical_runtime_activation_gate_v1`) | Eligibility mirror; provenance labels; WHY REJECTED; explicit prohibition (load-time + write-path); harness still out of estate |
| Launch-critical `pkg_kb47_*` | Unchanged lineage eligibility (**temporary exception**) | WHY REJECTED; provenance lineage quality — Stage 2 must fold into register |
