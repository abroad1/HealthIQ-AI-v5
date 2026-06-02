# PASS3-FRAME-INDEX-2 — High-Risk Signal Family Index Expansion Report

**Work ID:** `PASS3-FRAME-INDEX-2_high_risk_signal_family_index_expansion`  
**Date:** 2026-06-02  
**SOP:** AUTOMATION_BUS_SOP_v1.3.1

---

## Executive verdict

**PASS (governance only).** Medical frame identity index expanded for **3 high-risk families beyond creatinine**: `signal_alt_high` (6 frames), `signal_crp_high` (5 frames), `signal_ferritin_high` (3 frames). **14 new frame entries** added; validator passes; no duplicate active activation keys. Unadjudicated legacy frames remain `blocked_pending_medical_review`. No runtime behaviour changes.

---

## Ranked high-risk family shortlist (audit-derived)

Ranking used PASS3-FRAME-COVERAGE-1 criteria (edge_case_loss_risk, promotion_safety_status, Pass_3 frame count, legacy overrides, worked examples).

| Rank | signal_family_id | primary_biomarker | edge_risk | promotion_safety | pass3_frames | legacy_overrides | Selected |
|------|------------------|-------------------|-----------|------------------|--------------|------------------|----------|
| 1 | signal_creatinine_high | creatinine | high | enrichment | 2+ | 2 (eGFR, K+) | Already indexed |
| 2 | signal_alt_high | alt | high | frame adjudication | 3 | 3 | **Yes** |
| 3 | signal_crp_high | crp | high | frame adjudication | 2 | 3 | **Yes** |
| 4 | signal_ferritin_high | ferritin | high | frame adjudication | 3 | 1 | **Yes** |
| 5 | signal_ferritin_low | ferritin | medium | enrichment | 3 | 3 | No (this sprint) |
| 6 | signal_apob_atherogenic | apob | high | frame adjudication | 3 | 1 | No (this sprint) |
| 7 | signal_systemic_inflammation | crp | high | frame adjudication | 2 | 0 | No (ROUTE_G separate sprint) |

---

## Selected families and rationale

### 1. signal_alt_high

- **Evidence:** PASS3-FRAME-COVERAGE-1 worked example; priority 2 in expansion candidates; 3 kb52c Pass_3 packages + s24 with Hy's Law / cholestatic overrides.
- **Packages:** `pkg_kb52c_alt_high_*` (3), `pkg_s24_alt_high_hepatocellular_injury`.
- **Frames added:** 6 (3 Pass_3 canonical active; 3 legacy override frames, 1 active + 2 inactive on shared legacy key).

### 2. signal_crp_high

- **Evidence:** priority 3; CF-CRPPASS3-001; dual Pass_3 specs not compiled; s24 retains 3 override rules.
- **Packages:** `pkg_s24_crp_high_inflammation` (runtime); Pass_3 packages deferred.
- **Frames added:** 5 (2 Pass_3 deferred; 3 legacy override frames on s24).

### 3. signal_ferritin_high

- **Evidence:** priority 4; 3 Pass_3 inflammatory vs overload vs depletion specs; s24 extreme-elevation override.
- **Packages:** `pkg_s24_ferritin_high_overload` (runtime); Pass_3 high frames deferred.
- **Frames added:** 3 (2 Pass_3 deferred; 1 legacy active).

---

## Frame entries added (summary)

| Family | New frames | Active runtime authorities |
|--------|------------|----------------------------|
| signal_alt_high | 6 | 3 kb52c Pass_3 + 1 legacy Hy's Law (s24) |
| signal_crp_high | 5 | 1 legacy acute-infection (s24) |
| signal_ferritin_high | 3 | 1 legacy extreme elevation (s24) |

**Collision checks:** Shared legacy activation keys use **one active** frame per key (creatinine pattern). Three distinct kb52c ALT activation keys all active (non-colliding).

---

## Context modifier relevance

Not wired. Future binding via CONTEXT-MOD-2. Relevant modifiers exist for inflammatory (CRP), hepatic (ALT), and iron (ferritin) in `context_modifier_catalogue_draft_v1.yaml`.

---

## Governance helper script disposition

| Script | Location | Classification |
|--------|----------|----------------|
| `build_pass3_frame_coverage_audit.py` | `backend/scripts/` | `read_only_governance_helper_non_runtime` (PASS3-FRAME-COVERAGE-1) |

**CF-GOVHELPER-001:** Resolved in this sprint by policy statement: future governance helpers **preferred** under `knowledge_bus/tools/`; existing `backend/scripts/` helper retained (validator convention). No runtime imports; no package mutation.

---

## Carry-forward updates

| ID | Status |
|----|--------|
| CF-PASS3FRAME-001 | **Resolved** — ALT, CRP, ferritin_high indexed |
| CF-PASS3FRAME-002 | **Open** — Pass_3 enrichment not done |
| CF-PASS3FRAME-003 | **Open** — promotion pause list unchanged |
| CF-GOVHELPER-001 | **Resolved** — policy documented in this report |
| CF-CRPPASS3-001 | **Open** — CRP Pass_3 frames indexed as deferred |
| CF-CREATININE-001 | **Open** |

---

## Recommended next sprint

**CRP-PASS3-COMPILE-1** or **FERritin-PASS3-ENRICH-1** — compile/enrich Pass_3 packages for deferred frames before promotion.

---

## Validation output (actual)

```
validation_status: PASS
errors: 0
index_path: C:\Users\abroa\HealthIQ-AI-v5\knowledge_bus\governance\medical_frame_identity_index_v1.yaml

validation_status: PASS
errors: 0
catalogue_path: C:\Users\abroa\HealthIQ-AI-v5\knowledge_bus\governance\context_modifier_catalogue_draft_v1.yaml

day_one_architecture_validation: PASS

....                                                                     [100%]
...........                                                              [100%]
..........                                                               [100%]
```

---

## Runtime boundary confirmation

No changes to `knowledge_bus/packages/*`, evaluators, frontend, or SSOT.
