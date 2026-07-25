# ADR-RT-IDENTITY-PROV-001 — Activation Frame and Provenance Integrity

| Field | Value |
|-------|-------|
| **Status** | ACCEPTED for implementation under ARCH-RT-IDENTITY-PROV-1 |
| **Date** | 2026-07-25 |
| **Work package** | ARCH-RT-IDENTITY-PROV-1 |
| **Authority** | Implementation-extension ADR **subordinate to** ADR-RT-001, ADR-RT-002, ADR-RT-003, ADR-RT-004 |
| **Does not reopen** | Research-to-runtime authority; activation identity; registry keying; rejection of ONE_FRAME_PER_DIRECTION; compiled vs legacy hypothesis transition; compile-manifest authority; explicit provenance policy |

## Filename corrections (hardening C4)

Prompt citations resolved to actual accepted files:

| Prompt citation | Actual path |
|---|---|
| `ADR-RT-002_signal_identity_and_registry_architecture.md` | `docs/architecture/ADR-RT-002_signal_spec_identity_and_registry_policy.md` |
| `ADR-RT-003_hypothesis_and_root_cause_transition_architecture.md` | `docs/architecture/ADR-RT-003_hypothesis_artefact_and_root_cause_transition.md` |
| `ADR-RT-004_compile_manifest_and_provenance_policy.md` | `docs/architecture/ADR-RT-004_compile_manifest_and_package_provenance_policy.md` |

---

## A. Canonical runtime identity

Inherited from ADR-RT-002 without re-decision:

| Element | Role |
|---|---|
| `signal_id` | Signal-family identity |
| `source_spec_id` | Activation-frame / research-source identity |
| `activation_key` | Runtime frame identity = `signal_id::source_spec_id` |

**Legacy when explicit `source_spec_id` is absent on the package manifest:** runtime may continue to **infer** a frame id via `signal_activation_identity_v1.infer_source_spec_id` for activation-key construction (existing behaviour). That inference MUST be labelled provenance `LEGACY_INFERRED` or `SOURCE_DOCUMENT_DERIVED` — never `EXPLICIT_SPEC`.

**Collision behaviour:** duplicate `activation_key` remains a hard fail at registry load (existing).

**Ordering:** consumers MUST order multi-frame structures by `(signal_id, activation_key)` ascending unless a named ranking policy already governs presentation order.

**Replay:** new multi-frame records MUST round-trip `activation_key` / `source_spec_id`; old single-frame records remain valid when `activation_key` is present or reconstructible.

---

## B. Downstream preservation rule

Every downstream structure that can hold more than one frame for the same `signal_id` MUST:

1. Preserve `activation_key` on each frame-bearing row.
2. Avoid unqualified dictionaries keyed solely by `signal_id` for frame-bearing data.
3. Avoid first-match selection by `signal_id` where multiple frames exist.
4. Avoid cardinality reduction from list → single item unless an explicit named aggregation policy applies.
5. Expose family-level aggregation only as a named derived view.

**Shared helper (mandatory):** `backend/core/knowledge/signal_result_index_v1.py` provides:

- `index_by_activation_key`
- `group_by_signal_id`
- `require_activation_key`
- deterministic ordering helpers

All known collapse surfaces MUST use this helper rather than bespoke dicts.

---

## C. Clinician-report cardinality rule

**Decision (mechanical, additive):**

| Field | Behaviour |
|---|---|
| `sections.root_causes` | **New** `List[RootCauseFindingV1]` — all authorised findings, ordered deterministically |
| `sections.root_cause` | **Legacy** `Optional[RootCauseFindingV1]` — set **only** when `len(root_causes)==1`; otherwise `null` |

**Prohibited:** silent selection of `root_causes[0]` into `root_cause` when multiple findings exist.

**Frontend:** mirror additive contract in `frontend/app/types/analysis.ts`; remain render-only.

**Product note:** displaying multiple authorised findings is cardinality preservation, not clinical arbitration. No new medical ranking among root causes is introduced by this ADR.

Each `RootCauseFindingV1` MUST carry `activation_key` and `source_spec_id` when available.

---

## D. Root-cause authority rule

- Compiled frame-specific hypotheses match by `activation_key` / explicit frame identity when available.
- Legacy family-level hypotheses remain family-level; output MUST label `authority_scope: family_level` (or equivalent honest field) rather than inventing a frame.
- No first-match-by-`signal_id` when multiple frames share that family.
- Ambiguous multi-frame WHY without frame-specific compiled artefact → unresolved / family-level status; do **not** invent frame binding.
- No new medical WHY content.

---

## E. Provenance status model

Closed enum (runtime / DTO / inventory):

```text
EXPLICIT_SPEC
COMPILED_MANIFEST
SOURCE_DOCUMENT_DERIVED
LEGACY_INFERRED
UNRESOLVED
BLOCKED
```

| Status | Meaning |
|---|---|
| `EXPLICIT_SPEC` | `source_spec_id` present on package manifest and validated |
| `COMPILED_MANIFEST` | Compile-manifest-backed artefact authority (cards/hypotheses) |
| `SOURCE_DOCUMENT_DERIVED` | Deterministic derivation from `source_document` path without explicit manifest field |
| `LEGACY_INFERRED` | Inference from package_id / path heuristics without strong document evidence |
| `UNRESOLVED` | No defensible mapping |
| `BLOCKED` | Promotion/extraction blocked (e.g. batch-json pending) |

Inferred MUST never be presented as `EXPLICIT_SPEC`.

---

## F. Manifest schema migration

- Extend `knowledge_bus/schema/package_manifest_schema.yaml` **additively** with optional fields: `source_spec_id`, `activation_key`, `legacy_retained`, `compile_run_id`, `source_document_hash` (align ADR-RT-004).
- Keep schema status compatible for historical packages missing the new optional fields.
- Schema version → `1.1.0` (additive optional fields; historical packages remain valid).
- Document ARCH-RT gap: ADR-RT-004 required `source_spec_id` but prior ARCH-RT delivery left the locked schema without the field (continuity repair, not fabricated closure).
- Populate `source_spec_id` on the **bounded launch-critical cohort only** where `source_document` (or compile evidence) proves the mapping. Do not invent IDs.

---

## G. Compile-manifest naming authority

| Name | Role |
|---|---|
| `compile_manifest_ref` | **Canonical stable logical reference** on compiled artefacts / DTOs |
| `compile_manifest_path` | **Estate-index internal path field** resolving to the same manifest files |

They are **not** conflicting authorities. Do not blind-rename estate index fields in this sprint. Consumer-facing DTOs MUST expose `compile_manifest_ref` only (no filesystem path leakage beyond the governed relative repo path already used as the logical ref).

---

## H. Launch-critical enforcement policy

| Context | Policy |
|---|---|
| Runtime execution | Backward-compatible; identity collisions fail closed; multi-frame must not silently discard |
| Internal development | Same + gate reports unresolved items |
| Controlled beta eligibility | Launch-critical cohort must not claim false explicit lineage; unresolved/blocked items reported as beta-ineligible |
| Medical-content promotion | Out of scope (no Pass 3 / PSI) |

Do **not** make all 191 packages runtime-fatal.

---

## I. Migration boundary (launch-critical cohort)

**In cohort for this sprint:**

1. Runtime-active Knowledge Bus packages actually loaded by `SignalRegistry` for production evaluation (including the four `pkg_kb47_*` androgen packages verified by architecture gate).
2. Runtime-promoted compiled hypothesis `signal_vitamin_d_low`.
3. Estate-indexed compiled card evidence artefacts (compile-manifest-backed; provenance status `COMPILED_MANIFEST`).

**Out of cohort:** remaining `pkg_kb52c_*` / batch-blocked packages, PSI packs, MR-BATCH-001B, unused legacy packages.

Unresolved cohort members: mark `UNRESOLVED`/`BLOCKED`, keep runtime compatible, mark beta-ineligible.

---

## STOP Gate 1 assessment

| # | Applies? | Notes |
|---|---|---|
| 1–3 | NO | Extends ADR-RT-002/003/004; does not conflict |
| 4 | NO | No medical signal meaning change |
| 5–7 | NO | Inference retained with honest labels; no guessing for EXPLICIT |
| 8 | NO | Additive optional schema fields |
| 9 | NO | No mass fail-closed of legacy estate |
| 10 | NO | Additive `root_causes` + legacy `root_cause` when singleton |
| 11 | NO | Replay compatibility preserved |
| 12 | NO | Cohort bounded in §I |
| 13 | NO | Additive multi-finding is cardinality preservation, not product selection among conflicting clinical narratives |
| 14 | NO | ref vs path reconciled as logical vs estate-index internal |
| 15 | NO | Subordinate extension only |

**STOP_GATE_1: PASS**

---

## STOP Gate 2 note

Mechanical identity/cardinality and honest provenance labelling do not require medical review.  
Any future promotion of `BLOCKED`/`UNRESOLVED` → beta-eligible, or frame-specific binding of family-level WHY, **does** require STOP Gate 2 / medical review and is out of scope here.
