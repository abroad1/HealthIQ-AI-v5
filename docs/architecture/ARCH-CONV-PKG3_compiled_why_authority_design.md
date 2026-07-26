# ARCH-CONV-PKG3 — Compiled WHY Authority Design

**Work ID:** `ARCH-CONV-PKG3`  
**Branch:** `feature/arch-conv-pkg3-why-authority-migration`  
**Baseline HEAD:** `d090747dac279f9983cb6a934f1a6e2128cd99c5`  
**STOP Gate B:** **PASS** (design only — no Phase 4 promotion in this kernel)

This design proves the migration architecture for the bounded pilot. It does **not** promote medical content and does **not** retire legacy authority until Gate C ratification and Phase 4–5 execute.

---

## 1. Current runtime paths (as-is)

| Path | Mechanism | Pilot coverage today |
|---|---|---|
| Compiled WHY | `RUNTIME_PROMOTED_COMPILED_SIGNAL_IDS` in `compiled_hypothesis.py`; selected in `root_cause_compiler_v1.py` via `is_runtime_promoted_compiled_signal` | **Only** `signal_vitamin_d_low` |
| Legacy WHY | `root_cause_registry_v1.ROOT_CAUSE_TARGET_SPECS` → YAML loaders under `knowledge_bus/root_cause/hypotheses/` | hcy, mcv, free_t3_low, tpo_ab_high (+ vitamin_d loader still present on disk) |
| Unit of medical frame | `activation_key = signal_id::source_spec_id` (Package 1) | All 10 pilot frames |

Observed dual-risk today: vitamin_d has compiled runtime promotion **and** legacy YAML still registered — retirement must remove runtime reachability of legacy without deleting history.

---

## 2. Governed authority states (per activation_key)

| State | Meaning |
|---|---|
| `LEGACY_ACTIVE` | Legacy YAML is the runtime WHY authority for the signal/frame path |
| `COMPILED_CANDIDATE` | Compiled artefact exists or is proposed; not medically approved |
| `MEDICALLY_APPROVED` | GPT recorded APPROVE_* for this activation_key |
| `HUMAN_RATIFIED` | Anthony explicitly ratified this activation_key |
| `COMPILED_ACTIVE` | Compiled artefact is the sole runtime WHY authority |
| `LEGACY_RETIRED` | Legacy YAML preserved on disk / VCS; **not** runtime-selectable |
| `REJECTED` | GPT/Anthony rejected; must stay inactive |
| `DEFERRED` | Explicit deferral; must stay inactive |
| `BLOCKED` | Missing evidence, identity, or ratification — fail closed |

Promotion requires ordered transitions:  
`LEGACY_ACTIVE` → (`COMPILED_CANDIDATE`) → `MEDICALLY_APPROVED` → `HUMAN_RATIFIED` → `COMPILED_ACTIVE` (+ peer `LEGACY_RETIRED` where applicable).

**No frame may skip Anthony ratification. No family-level inheritance.**

---

## 3. Canonical per-frame authority decision

For each pilot `activation_key`, exactly one of:

1. **Compiled sole authority** (`COMPILED_ACTIVE`) after Gate C APPROVE + Anthony ratification; or  
2. **Legacy sole authority** (`LEGACY_ACTIVE`) until ratified otherwise; or  
3. **Inactive** (`REJECTED` / `DEFERRED` / `BLOCKED`) with fail-closed selection.

Forbidden: simultaneous compiled + legacy runtime authority for the same `activation_key`.

Where legacy YAML is shared across frames (hcy / mcv / tpo), retirement must be designed so:

- family-level YAML cannot silently re-serve a retired frame; and  
- remaining non-promoted sibling frames either stay on an explicit legacy path or are deferred — **no bare `signal_id` collapse**.

---

## 4. Selection rules (to implement in Phase 4)

1. If frame state ∈ {REJECTED, DEFERRED, BLOCKED} → emit no WHY for that activation_key (fail closed).  
2. Else if state == `COMPILED_ACTIVE` and artefact present → compile from compiled artefact only.  
3. Else if state == `LEGACY_ACTIVE` → legacy registry path only.  
4. Else if compiled artefact present without `HUMAN_RATIFIED` → **do not** activate; fail closed (no silent candidate promotion).  
5. Never fall back from missing compiled asset to a `LEGACY_RETIRED` YAML.

Replay/audit must record: `activation_key`, authority state, artefact/YAML identity, review/ratification work ids.

---

## 5. Family presentation vs frame authority

Package 1 family-level presentation remains allowed only when:

- participating `activation_key`s are auditable; and  
- WHY authority decisions remain per-frame (no family approval).

---

## 6. Retirement model

| Requirement | Design |
|---|---|
| Reversible | Via VCS history + retirement register (work_id, date, replacement authority) — **not** dual runtime |
| Evidence preserved | Legacy YAML retained on disk when policy requires |
| Silent reactivation impossible | Runtime selectors must refuse `LEGACY_RETIRED`; no implicit fallback |
| Vitamin D pilot | Retirement confirmation only after GPT + Anthony; prove parity then mark legacy non-reachable |

Register path (Phase 5 deliverable after Gate C):  
`docs/architecture/ARCH-CONV-PKG3_legacy_retirement_and_authority_register.md`

---

## 7. STOP Gate B

| Trigger | Result |
|---|---|
| Retirement requires deleting evidence history | Not proposed |
| Authority cannot be selected per activation frame | Design requires per-frame state |
| Design depends on bare `signal_id` where frames differ | Forbidden; activation_key required |
| Legacy + compiled co-serving cannot be prevented | Prevention rules defined (§3–4) |
| New medical-priority policy required | Not required |
| Expansion into prose/PSI/Gemini/thresholds | Out of scope |

**PASS — architecture proof recorded. Phase 4 implementation blocked until Gate C.**

---

## 8. Out of scope for this design document

- Compiling new hypothesis artefacts for frames 2–10  
- Mutating `RUNTIME_PROMOTED_COMPILED_SIGNAL_IDS`  
- Retiring any legacy YAML at runtime  
- Any medical APPROVE/REJECT decision
