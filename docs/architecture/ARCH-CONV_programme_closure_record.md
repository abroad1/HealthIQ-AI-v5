# ARCH-CONV — Programme Closure Record

**Work ID:** `ARCH-CONV-RESIDUAL-AUDIT-1` (Part A — programme closure)  
**Date (UTC):** 2026-07-27  
**Governing decision gate:** Final v5 GO / NO-GO residual runtime audit  
**Runtime change:** NONE — documentation and decision-support only  

---

## 1. Programme status (authoritative)

```text
ARCH-CONV-CORRECT-1 CLOSED
MIGRATED COHORT SAFE
TARGET AUTHORITY MODEL PROVEN
ESTATE-WIDE DAY-ONE CONVERGENCE NOT YET PROVEN
FINAL V5 / V6 DECISION REMAINS OPEN
```

This record does **not** claim that the whole v5 estate now complies with the Day-One architecture.

---

## 2. What the merged convergence sequence established

The closed convergence sequence (`ARCH-CONV-GATE0` → `PKG1` → `PKG2` → `GATE2_5` → `PKG3` → `FINAL-AUDIT` → `CORRECT-1`) established:

```text
activation-frame identity and multi-frame safety
provenance and runtime reachability
compiled WHY authority for the reviewed cohort
structural inactivation of the rejected homocysteine frame
MCV co-service fail-closed policy
Layer B medical-authority enforcement
Layer C render/translation boundary correction
waist-circumference explicit-unit integrity
stale-session authentication resilience
automated regression verification
fresh human UAT and live-page review
```

### Scope of proof

| Claim | Status |
|---|---|
| Migrated 5-signal / 10-frame WHY pilot is safe under the target authority model | **Proven** |
| Target architecture pattern works end-to-end on the reviewed cohort | **Proven** |
| Whole active v5 runtime estate is Day-One converged | **Not proven** |
| Controlled-beta readiness | **Not assessed** |

---

## 3. Final live UAT analysis

```text
analysis_id:
20a99882-085c-475d-bb26-2ff28a13183a
```

### Live UAT outcomes recorded

| Check | Result |
|---|---|
| Rejected broad homocysteine metabolic frame absent | Confirmed |
| “methylation capacity” absent | Confirmed |
| Only permitted MCV morphology context served (causal WHY) | Confirmed |
| Competing MCV causal WHY did not co-surface | Confirmed |
| Consumer and clinician outputs aligned | Confirmed |
| Layer C did not reconstruct unsupported medical meaning | Confirmed |
| Explicit `90 cm` waist input remained `90 cm` | Confirmed |
| Valid-session `/api/auth/me` behaviour normal | Confirmed |
| CORRECT-1 and Package 1–3 protections passed | Confirmed |
| Original end-to-end scenario suite | **13/13** |

Supporting package evidence: `docs/audit-papers/ARCH-CONV-CORRECT-1_implementation_and_verification_report.md`.

---

## 4. Final merged commit reviewed

| Field | Value |
|---|---|
| Feature tip (CORRECT-1 merge tip) | `bfcb5fdb02c8a0c3ab492efa5d3acf7d89f9bc0c` |
| Published `main` tip at audit start | `2626d00bc12d773349bd2072a4f5fbe7261cd39f` |
| Branch | `main` (aligned with `origin/main` at programme publish) |
| Merge mode | Fast-forward of `feature/arch-conv-correct-1-e2e-authority-layerc` |

---

## 5. Separately retained follow-ups

These remain open and are **not** closed by CORRECT-1:

```text
pre-existing output-authority provenance regression involving
signal_homocysteine_high::inv_homocysteine_high

historic analysis impact from the former waist-unit defect

result-versioning policy advancement for regeneration after medical-authority changes
```

Evidence anchors:

- Provenance fixture/key: `backend/tests/regression/test_output_authority_provenance.py`
- Historic waist impact: `docs/audit-papers/WAIST_UNIT_LEGACY_IMPACT_AUDIT.md` (48 legacy bare rows; 12 used_incorrectly)
- Result versioning policy: `docs/architecture/LAUNCH-CORE-3_result_versioning_replay_and_regeneration_policy.md`

---

## 6. Programme decision boundary

- `ARCH-CONV-CORRECT-1` is **CLOSED** as a correction package.
- The migrated cohort is **SAFE** relative to the final-audit defect themes.
- Estate-wide Day-One convergence and the final **v5 retain / v6 freeze** decision are answered only by the residual runtime audit artefacts under `docs/architecture/ARCH-CONV_*`.
- No implementation, deletion, migration, registry change, or Knowledge Bus regeneration is authorised by this closure record.
