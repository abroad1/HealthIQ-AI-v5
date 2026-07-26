# ARCH-CONV-FINAL — Frontend End-to-End UAT Plan (Awaiting Anthony)

**Work ID:** `ARCH-CONV-FINAL-AUDIT`  
**Status:** **MANDATORY STOP — awaiting Anthony**  
**Path convention:** `docs/testing/` (repo precedent; prompt’s `docs/uat/` does not exist)  
**Commit SHA to test against:** `522873428882d9f47093e283a3ab31dc16fcd684` (or later published main SHA after merge)  
**Environment:** local / staging as Anthony selects — record exact URL and build

This document is the human UAT handoff. Automated Layer B audit is complete. **Do not issue programme PASS until this UAT pack is completed and attached.**

---

## Minimum cases (required)

| Case ID | Intent | Suggested panel pattern | PASS criteria (Anthony) |
|---|---|---|---|
| UAT-1 | Normal / mostly normal panel | Values mostly in range; minimal lifestyle flags | Usable flow; **no false WHY / no invented causes** |
| UAT-2 | Pilot multi-frame panel | Exercise ≥1 of: hcy B-vitamin, hcy renal, MCV mega/nonmega, TPO hypo/euthyroid, low FT3 | Displayed WHY matches input pattern; frame traceable; consumer/clinician coherent |
| UAT-3 | Negative leakage panel | e.g. raised hcy **without** renal impairment **or** high MCV **without** B12/folate support | Unsupported cause **does not** appear; no rejected metabolic catch-all |
| UAT-4 (optional but recommended) | Rejected metabolic inertness | If product can activate only metabolic-like broad hcy without B-vit/renal support | No methylation-capacity / broad metabolic WHY |

---

## Evidence checklist (per case)

Preserve:

- [ ] case ID, date/time, environment, commit SHA
- [ ] exact blood inputs (values, units, reference ranges)
- [ ] lifestyle / questionnaire answers
- [ ] screenshots: input completion
- [ ] screenshots: consumer results
- [ ] screenshots: clinician results (if available)
- [ ] consumer report/export
- [ ] clinician report/export
- [ ] API payload or replay artefact (if available)
- [ ] Anthony observations
- [ ] PASS / FAIL

---

## Anthony’s questions (answer per case)

1. Does the displayed interpretation make medical and business sense?
2. Does the displayed WHY match the actual input pattern?
3. Is any cause asserted without supporting evidence?
4. Is any wording visibly old, duplicated, contradictory or out of context?
5. Is rejected, blocked or retired content visible?
6. Do consumer and clinician views tell the same underlying medical story?
7. Is the correct activation frame traceable?
8. Does the result appear to have been inferred or altered in Layer C?
9. Is anything surprising enough to require medical or architecture review?

---

## Known automated Layer C risks to watch during UAT

Confirm whether these FE behaviours are visible in real UX:

- Primary driver / hero emphasis that disagrees with clinician lead
- Confidence values that look “always high” when backend confidence is missing
- Dial colours that look clinical without matching backend status
- Layer C insight cards inventing explanations beyond DTO prose

---

## Results section (Anthony completes)

| Case ID | Date | SHA | PASS/FAIL | Key observations | Attachments |
|---|---|---|---|---|---|
| UAT-1 | | | | | |
| UAT-2 | | | | | |
| UAT-3 | | | | | |
| UAT-4 | | | | | |

**Anthony overall UAT decision:** `OPEN`  
**Date:** _(pending)_

---

## Resume instruction

After evidence is filled, resume `ARCH-CONV-FINAL-AUDIT` on the same work ID / branch (or successor continuation) to issue the final programme decision (`PASS` / `CORRECT` / `STOP` / `V6`).
