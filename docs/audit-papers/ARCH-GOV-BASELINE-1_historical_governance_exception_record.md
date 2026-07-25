# ARCH-GOV-BASELINE-1 — Historical Governance Exception Record

**Date:** 2026-07-25  
**Work package:** ARCH-GOV-BASELINE-1  
**Purpose:** Record missing historical Automation Bus lifecycle evidence honestly.  
**Non-precedential:** Future work must not cite this document as authority to bypass Automation Bus or Knowledge Bus governance.

---

## Scope

This record covers two recent workstreams that remain accepted as historical repository state:

1. **P3-PROSE-DEPTH-1A** — directional marker-state prose schema rules  
2. **MR-BATCH-001B** — candidate prose test import / fixture pathway  

No retrospective hardening is claimed. No retrospective kernel start/finish is fabricated.

---

## Findings

### P3-PROSE-DEPTH-1A

- Lacks a demonstrated full Automation Bus lifecycle trail for the 1A follow-on work (prompt → HARDENED → kernel start → implementation → kernel finish → audit) as a distinct work package.
- Parent **P3-PROSE-DEPTH-1** does have bus artefacts historically associated with its lifecycle; that does not substitute for a complete demonstrated trail for 1A.
- Content-level risk was limited by scope (schema/docs/test-adjacent prose rules) and by isolation from changing production medical inference pathways beyond the authorised schema work.

### MR-BATCH-001B

- Lacks a demonstrated full Automation Bus lifecycle trail (no complete HARDENED → start → finish → audit chain attributable to MR-BATCH-001B as a governed work_id).
- Touched `backend/tests/` (test support loader + unit tests). Therefore the Automation Bus **docs-only bypass** (`/docs/` only) does **not** clearly apply.
- Content-level risk was limited by isolation from production paths:
  - Candidate assets live under sprint docs.
  - Loader requires `candidate_test_mode=True`.
  - Production orchestrator / retail assembly do not import the candidate loader.
  - Assets remain `review_status: CANDIDATE`; none APPROVED.
- Classification confirmed by BUILD register and current-state baseline: Round 1 benchmark / test fixture only; not medically approved; not for promotion; not for production runtime.

---

## Acceptance posture

| Item | Posture |
|---|---|
| Historical repository state | Accepted unless a specific defect is found |
| Retrospective hardening | **Not** claimed |
| Precedent for future bypass | **Explicitly rejected** |
| Required future behaviour | Full Automation Bus SOP for any Intelligence Core, analytical, or non-docs-only work |

---

## Explicit non-precedent clause

This exception record documents a **historical gap**. It does **not**:

- authorise skipping Claude hardening;
- authorise skipping kernel start/finish;
- authorise docs-only bypass when tests or runtime paths are touched;
- authorise medical review or promotion of MR-BATCH-001B;
- convert DRAFT governance documents into APPROVED status.

Any future attempt to use this record as a bypass rationale must be rejected and escalated.
