# ARCH-CONV-PKGC-2 — Hardening Pack

**Work ID:** `ARCH-CONV-PKGC-2`  
**Branch:** `feature/arch-conv-pkgc-2-provenance-identity-closure`  
**Date:** 2026-08-02  
**Hardening recommendation (Claude):** provisional STANDARD  
**Cursor Stage 1A authoritative classification:** below

---

## RISK_CLASSIFICATION: STANDARD — CONTRACT_ADJACENT

Stage 1A independently confirms the provisional hardening recommendation.

### 1. Provenance builder is additive / descriptive only

File: `backend/core/analytics/output_authority_provenance_builder_v1.py`

| Question | Finding |
|---|---|
| Mutates `report.top_findings`? | **No** — reads findings; does not rewrite them |
| Mutates `root_cause.findings`? | **No** |
| Selects / ranks hypotheses? | **No** |
| Changes signal / frame authority registers? | **No** — read-only classification via `compiled_output_authority_v1` |
| Changes medical narrative? | **No** |
| Changes report inclusion? | **No** — inclusion already decided before builder runs |
| Role | Serialises already-decided authority labels into additive `ReportV1.output_authority_provenance_v1` |

Call chain (post-hoc attach):

```text
compile_report_v1
  → compile_root_cause_v1 (...)
  → build_report_output_authority_provenance_v1(signal_results, report_draft, root_cause)
  → ReportV1(..., output_authority_provenance_v1=bundle)
```

Authority: ARCH-COMPLETION-2 audit paper — “Runtime provenance metadata is attached ADDITIVELY”.

### 2. Canonical activation-key grammar — one grammar, two roles

| Module | Role | Grammar |
|---|---|---|
| `signal_activation_identity_v1.py` | **Producer** at package load (`build_activation_key`, `resolve_activation_identity`) | `signal_id::source_spec_id` |
| `signal_result_index_v1.py` | **Consumer / reconstruct** (`require_activation_key`, `activation_key_or_empty`) | same `signal_id::source_spec_id` |

Authoritative ADR: `docs/architecture/ADR-RT-IDENTITY-PROV-001_activation_frame_and_provenance_integrity.md`  
Shared helper mandate: `signal_result_index_v1.py`.

No competing parser or alternate production grammar found.  
`ACTIVATION_KEY_SEP = "::"` in the identity module; result-index reconstructs with the same literal separator.

### 3. Compiler quarantine filter — distinct from provenance builder

ARCH-COMPLETION-2 revert list item “compiler quarantine filter” resolves to:

| Item | Location |
|---|---|
| Filter | `backend/core/analytics/report_compiler_v1.py` → `_normalise_root_cause_finding` |
| Line | ~449: `if not is_governed_hypothesis(hypothesis_id): continue` |
| Mechanism | Skips hypothesis id `why_engine_fallback_v1` from clinician-facing hypothesis normalisation |
| Helper home | `is_governed_hypothesis()` is **co-located** in `output_authority_provenance_builder_v1.py` for packaging convenience |
| Uses provenance bundle? | **No** — pure id equality vs `WHY_ENGINE_FALLBACK_HYPOTHESIS_ID` |
| Uses `build_report_output_authority_provenance_v1`? | **No** |
| Timing | Runs in clinician normalisation path; provenance builder runs later as additive attach |

`is_quarantined_root_cause_signal()` (bundle reader) has **no production callers** outside its defining module.

Therefore the quarantine filter does **not** make the provenance builder an Intelligence Core decision surface. The builder remains contract-adjacent labelling; the clinician filter is a separate, pre-existing fail-closed id gate.

### Classification decision

Does **not** meet SOP Intelligence Core tests (interpretation, ranking, authority mutation, narrative, inclusion).  
Proceed under STANDARD — CONTRACT_ADJACENT. No Gate 1 / Gate 2 required.

---

## Stage 1B — Reality check (current main tip `e286a48` / branch base)

| Premise | Status |
|---|---|
| Synthetic bare key still in provenance test | TRUE — `test_output_authority_provenance.py` fixture |
| Not a live evaluated authority row | TRUE |
| Builder lacks defensive canonical-key form validation | TRUE — accepts any non-empty `activation_key`; falls back to `signal_id` |
| Malformed key absent from live governance registers | TRUE — live HCY keys are frame-suffixed (`…_b_vitamin…`, `…_renal…`, REJECTED metabolic) |
| No live emitter produces truncated `…::inv_homocysteine_high` | TRUE — evaluator uses `resolve_activation_identity` |
| `CF-ARCH-CONV-PROV-1` Open | TRUE |
| Sprint not already complete | TRUE |

---

## Phase 1 plan (authorised under STANDARD)

1. **Reuse** `require_activation_key()` — extend with form parse (`signal_id::source_spec_id`, both non-empty, exactly one `::` separator group).
2. **Guard** provenance emission: refuse malformed / bare keys fail-closed (`ValueError`); do not silently rewrite to `signal_id`.
3. **Replace** synthetic fixture in `test_report_includes_output_authority_provenance` with a real evaluated canonical row (existing package evaluation path).
4. **Retain** truncated/malformed key only as explicit negative tests.
5. **Close** `CF-ARCH-CONV-PROV-1` only after live canonical keys pass and negatives fail closed.

### Validation boundary

- Primary: `signal_result_index_v1.require_activation_key` (shared constructor).
- Provenance builder calls through that helper rather than inventing a second grammar.
- Registry membership of investigation IDs is **not** required by the existing shared contract for this sprint (structural + reconstructable identity only). Wrong-investigation registry checks remain out of scope unless a live key fails.

### Expected failure contract

`ValueError` with clear message when activation identity is missing or non-canonical. No silent coercion.

### Exclusions

Waist / PKGC-1, result-versioning, regeneration, compiled-WHY authority-state changes, signal activation changes, narrative/ranking/inclusion changes, frontend medical logic, general identity-registry redesign.

### Rollback

Revert the shared form validation + provenance fail-closed call + test changes. No schema migration.
