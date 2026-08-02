# ARCH-CONV-PKGC-2 — Identity Contract Map

**Work ID:** `ARCH-CONV-PKGC-2`  
**Date:** 2026-08-02  
**Risk:** STANDARD — CONTRACT_ADJACENT

## Canonical grammar

```text
activation_key = signal_id + "::" + source_spec_id
```

| Authority | Path |
|---|---|
| ADR | `docs/architecture/ADR-RT-IDENTITY-PROV-001_activation_frame_and_provenance_integrity.md` |
| Producer | `backend/core/knowledge/signal_activation_identity_v1.py` (`build_activation_key`, `resolve_activation_identity`) |
| Consumer / reconstruct | `backend/core/knowledge/signal_result_index_v1.py` (`require_activation_key`, `activation_key_or_empty`) |

One grammar. Producer builds at package/registry load; consumer requires or reconstructs on result rows. No alternate delimiter or production form.

## Live emitters of activation keys

| Emitter | Path | Notes |
|---|---|---|
| Signal evaluator / registry load | `signal_evaluator.py` via `resolve_activation_identity` | All evaluated rows carry canonical keys |
| Report compiler top findings | `report_compiler_v1.py` | Copies `activation_key` from signal rows |
| Root-cause compiler | `root_cause_compiler_v1.py` | Frame-bearing findings carry keys |
| Provenance builder | `output_authority_provenance_builder_v1.py` | Labels only; must not invent keys |

## Malformed / non-frame examples

| Example | Class | Live? |
|---|---|---|
| `signal_homocysteine_high::inv_homocysteine_high` | Truncated / non-frame synthetic | Test fixture only (pre-fix) |
| `signal_homocysteine_high` | Bare signal-only (no `::`) | Must fail closed |
| `signal_x::` / `::inv_y` / `a::b::c` | Empty / multi-separator malformed | Must fail closed |
| `signal_homocysteine_high::inv_homocysteine_high_b_vitamin_related_methylation_impairment` | Live COMPILED_ACTIVE | Must pass |
| `signal_homocysteine_high::inv_homocysteine_high_renal_clearance_reduction` | Live COMPILED_ACTIVE | Must pass |
| `signal_homocysteine_high::inv_homocysteine_high_metabolic` | REJECTED frame key (register) | Not a provenance positive fixture; not invented by this sprint |

## Validation boundary (Phase 1)

```text
require_activation_key(row)
  → if activation_key present: parse as signal_id::source_spec_id (fail closed)
  → else reconstruct from signal_id + source_spec_id (fail closed if incomplete)
```

Provenance builder must call this shared helper for claimed activation identities and must not fall back from a malformed key to bare `signal_id`.

## Quarantine filter (out of this sprint’s mutation set)

| Name | Location | Relationship to builder |
|---|---|---|
| Compiler quarantine filter | `report_compiler_v1._normalise_root_cause_finding` + `is_governed_hypothesis` | Distinct clinician-path id filter; does not consume provenance bundle |

## Carry-forward

`CF-ARCH-CONV-PROV-1` closes only when synthetic non-frame fixture is removed/converted to negative test, guard is live, and all current live canonical keys pass.
