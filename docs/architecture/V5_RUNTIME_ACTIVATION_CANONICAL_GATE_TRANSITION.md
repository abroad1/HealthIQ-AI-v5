# V5 Runtime Activation — Canonical Gate Transition

**Work ID:** `V5-RUNTIME-AUTHORITY-INTEGRITY-1`  
**Based on:** current `SignalRegistry._load` inspection (`backend/core/analytics/signal_evaluator.py`)

## Five current mechanisms (loader order / roles)

| # | Mechanism | Module | Role today |
|---|---|---|---|
| 1 | Package runtime eligibility | `package_runtime_eligibility_v1` | Launch-critical lineage gate; for non-launch-critical, requires package to appear in activation register |
| 2 | Launch-critical cohort split | `is_launch_critical_package_id` | Routes `pkg_kb47_*` away from the non-launch activation register |
| 3 | Provenance status | `provenance_status_v1` | Classifies lineage honesty; feeds eligibility / audit surfaces |
| 4 | Frame runtime authority | `frame_runtime_authority_v1` | Excludes frames with WHY `authority_state == REJECTED` |
| 5 | Package activation register | `package_activation_register_v1` ← `package_runtime_activation_register_v1.yaml` | Per-`activation_key` allow-list for non-launch-critical production reachability |

This sprint adds a **validation invariant** (not a sixth loader gate): `runtime_medical_authority_integrity_v1` reconciles explicit medical activation prohibitions with mechanism 5.

## Canonical future gate

**Canonical activation authority:** mechanism 5 — the governed `package_runtime_activation_register_v1.yaml` / `package_activation_register_v1` allow-list.

Rationale: it is already the only artefact that answers “is this non-launch-critical frame allowed to load?” as an explicit promotion decision. Medical prohibition artefacts must constrain what may be written into that register; they should not become a parallel runtime allow-list.

## Supporting constraints (not independent activation authorities)

- **Eligibility + launch-critical split + provenance** — cohort and lineage constraints around the allow-list; demote toward helpers of the canonical gate.
- **Frame runtime authority (`REJECTED`)** — hard medical exclusion that must remain enforceable even if a key were mistakenly listed; keep as a fail-closed safety constraint, not a second activation SSOT.
- **Medical decision `blocked_targets` / `NOT_AUTHORISED*`** — upstream authority that must prevent register membership (enforced by the new validator / future write-path guard).

## Minimum safe transition sequence

1. **Done in this package:** fail-closed validator between explicit prohibitions and the activation register; correct known lipid drift; regression coverage.
2. **Next bounded package:** enforce the same invariant on any script/process that mutates `activated_frames` (write-path guard), without collapsing loader branches.
3. **Later:** fold package-level eligibility checks so non-launch reachability is expressed only as “key ∈ activation register ∧ not REJECTED”, with provenance retained as metadata.
4. **Later:** retire ad hoc bypass semantics; keep launch-critical as an explicit cohort policy documented beside the register rather than a silent alternate path.

## Retirement / demotion targets

| Target | Disposition |
|---|---|
| Independent bootstrap-by-snapshot of activation register | Retire; all additions require prohibition cross-check |
| Treating WHY `LEGACY_RETIRED` / `SUPERSEDED_*` as deactivation | Never promote; wrong semantic |
| Five peer “activation authorities” | Demote 1–4 to constraints; keep 5 canonical |
| Full `SignalRegistry` rewrite | Not required for integrity; optional later consolidation package |

## Is a later implementation package required?

**Yes, but narrowly.** This sprint restores integrity without collapsing the five mechanisms. A follow-on package is warranted to (a) write-path enforce the invariant and (b) simplify loader branching toward the single canonical allow-list. That work is an in-place V5 consolidation, not a V6 rewrite, provided the prohibition↔register invariant remains mandatory.
