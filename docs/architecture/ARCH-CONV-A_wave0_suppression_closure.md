# ARCH-CONV-A — Wave 0 Closure (Suppression Disposition)

**Work ID:** `ARCH-CONV-A`  
**Wave:** 0 — Homocysteine elevation-context  
**Date (UTC):** 2026-07-27  
**Gate status:** Closed as **suppression disposition** (not a compile wave)

---

## Ratified disposition

```text
disposition: FOLD_SUPPRESS
independent frame count: 0
```

| Field | Value |
|---|---|
| signal_id | `signal_homocysteine_elevation_context` |
| Independent WHY frame | **Not created** |
| activation_key / frame_id | **None** |
| Compile eligibility | **None** |
| Finding context retention | Governed **non-causal** signal / card / presentation surfaces only |
| Shared legacy source | `knowledge_bus/root_cause/hypotheses/hcy_hypotheses_v1.yaml` — **still connected** |
| Package B hand-offs | Shared selector / exclusivity mechanics; final physical retirement of shared YAML |

---

## Explicit non-actions

- No investigation_spec authored for elevation-context  
- No compiled WHY artefact  
- No runtime WHY activation change for elevation-context beyond existing dual-serve state  
- No disconnect / delete / archive of `hcy_hypotheses_v1.yaml`  
- No medical decision on inflammation-only legacy hyp (`hcy_inflammation_context_v1`) beyond fold into Package B scope  

---

## Relationship to pilot compiled frames

Existing `signal_homocysteine_high` frames remain the governed causal WHY path:

| activation_key | state |
|---|---|
| `signal_homocysteine_high::inv_homocysteine_high_b_vitamin_related_methylation_impairment` | COMPILED_ACTIVE |
| `signal_homocysteine_high::inv_homocysteine_high_renal_clearance_reduction` | COMPILED_ACTIVE |
| `signal_homocysteine_high::inv_homocysteine_high_metabolic` | REJECTED |

Wave 0 does **not** reopen these frames.

---

## Closure statement

Wave 0 is **documentation-closed** under STOP A ratification. It does not submit frames to STOP B and does not require Gate 1 medical review for a new WHY frame.
