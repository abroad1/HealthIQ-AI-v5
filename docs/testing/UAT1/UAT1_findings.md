# UAT Pass 1 Findings — HealthIQ AI

## Summary

### Core path status
- Register: PASS
- Login: PASS
- Upload: PASS WITH ISSUES
- Parse: PASS WITH ISSUES
- Marker review: PASS
- Questionnaire: PASS WITH ISSUES
- Analysis start: PASS WITH ISSUES
- Results: PASS WITH ISSUES
- Clinician report: PASS WITH ISSUES
- Logout/relogin: PASS
- History/reopen: PASS

### Overall assessment
The primary end-to-end journey is working. The current issues are concentrated in four areas:
- parsing fidelity and marker-editing control
- questionnaire UX, content quality, and repeat-use burden
- results/narrative quality and supporting-marker transparency
- a small SSE lifecycle/polish issue

There are no current core-path blockers in the latest manual run, but there are several pre-launch quality issues that would materially affect user trust and perceived product value.

---

## Living tracker — remediation waves

Authoritative grouped status. Full write-ups remain in **Detailed findings** below.

**Last updated:** 2026-04-11

### Recently completed
- **UAT-001** — **Completed** — HbA1c dual-unit governance fix merged; `mmol/mol` no longer blocks analysis start and only canonical `hba1c` now feeds Layer B analysis.

### Wave 1 — Upload fidelity and correction path
| ID | Status | Current status |
|----|--------|----------------|
| UAT-005 | Open | Open — awaiting grouped remediation wave |
| UAT-016 | Open | Open — investigated; fix not yet implemented |
| UAT-023 | Open | Open — umbrella finding; detail tracked in UAT-023a / UAT-023b |
| UAT-023a | Open | Open — investigated; fix not yet implemented |
| UAT-023b | Open | Open — investigated; fix not yet implemented |

### Wave 2 — Results quality and narrative contract
| ID | Status | Current status |
|----|--------|----------------|
| UAT-017 | Open | Open — awaiting grouped remediation wave |
| UAT-018 | Open | Open — awaiting grouped remediation wave |
| UAT-019 | Open | Open — awaiting grouped remediation wave |
| UAT-020 | Open | Open — awaiting grouped remediation wave |
| UAT-021 | Open | Open — awaiting grouped remediation wave |
| UAT-022 | Open | Open — awaiting grouped remediation wave |

### Wave 3 — Questionnaire usability and repeat-user context
| ID | Status | Current status |
|----|--------|----------------|
| UAT-006 | Open | Open — awaiting grouped remediation wave |
| UAT-007 | Open | Open — awaiting grouped remediation wave |
| UAT-008 | Open | Open — awaiting grouped remediation wave |
| UAT-009 | Open | Open — awaiting grouped remediation wave |
| UAT-010 | Open | Open — awaiting grouped remediation wave |
| UAT-011 | Open | Open — awaiting grouped remediation wave |
| UAT-012 | Open | Open — awaiting grouped remediation wave |
| UAT-013 | Open | Open — awaiting grouped remediation wave |
| UAT-014 | Open | Open — awaiting grouped remediation wave |

### Minor polish
| ID | Status | Current status |
|----|--------|----------------|
| UAT-015 | Open | Open — non-blocking polish |

### Auth / lifecycle (not assigned to a wave above)
| ID | Status | Current status |
|----|--------|----------------|
| UAT-002 | Open | Open — investigated; fix not yet implemented (intermittent; was masked as CORS) |
| UAT-003 | Open | Open — investigated; fix not yet implemented (expired JWT → 500) |
| UAT-004 | Open | Open — non-blocking polish (SSE closes with console error) |

---

## Detailed findings

### UAT-001
**Stage:** Analysis start  
**Title:** HbA1c unit conversion failure blocked analysis  
**Expected:** Analysis should accept HbA1c in mmol/mol and convert it correctly or otherwise support the reported unit.  
**Actual:** Analysis failed with: `No conversion from 'mmol/mol' to base unit '%' for biomarker 'hba1c'`.  
**Severity:** Critical  
**Type:** Functional bug / data-contract defect  
**Status:** Completed  
**Notes:** HbA1c dual-unit governance fix merged; `mmol/mol` no longer blocks analysis start and only canonical `hba1c` now feeds Layer B analysis.

### UAT-002
**Stage:** Questionnaire submit / analysis start  
**Title:** Backend 500 initially surfaced as CORS failure  
**Expected:** Questionnaire submit should start analysis successfully and wedge-event logging should not block user flow.  
**Actual:** Browser showed CORS-style errors, but backend was returning 500s.  
**Severity:** Critical  
**Type:** Functional bug / backend runtime error  
**Status:** Open  
**Current status:** Open — investigated; fix not yet implemented (intermittent; root cause included expired JWT handling during authenticated endpoint access).  
**Notes:** Re-run succeeded when session valid; no documented merge of a dedicated fix in this log.

### UAT-003
**Stage:** Questionnaire submit / analysis start  
**Title:** Expired JWT caused backend 500 on authenticated endpoints  
**Expected:** Expired session should return a clean auth error and prompt re-authentication.  
**Actual:** Backend threw 500 on `/api/analysis/start` and `/api/wedge-events` because Supabase rejected expired JWT.  
**Severity:** Critical  
**Type:** Functional bug / auth error-handling defect  
**Status:** Open  
**Current status:** Open — investigated; fix not yet implemented.  
**Notes:** Re-login unblocked the flow; no documented merge of auth-error mapping hardening in this log.

### UAT-004
**Stage:** Analysis progress / SSE  
**Title:** SSE stream logs error after successful completion  
**Expected:** After analysis completes, the progress stream should close cleanly without surfacing a console error.  
**Actual:** Analysis completed successfully, but frontend logged `SSE stream closed or errored` from `EventSource.onerror`.  
**Severity:** Low  
**Type:** UX / frontend lifecycle bug  
**Status:** Open  
**Current status:** Open — non-blocking polish.  
**Recommendation:** Review SSE completion contract and client cleanup logic so normal stream closure is not logged as an error.

### UAT-005
**Stage:** Upload / Parse  
**Title:** PDF parser collapses rich reference-range detail into a simplified single range  
**Expected:** Where the PDF contains complex sex/life-stage-specific ranges and unit notes, the parsed upload review should preserve that detail or clearly show that richer source detail exists.  
**Actual:** Prolactin is reduced to a single line and single range (`45–375 mIU/L`), losing female/non-pregnant, pregnant, postmenopausal distinctions and the “unit/range change” note.  
**Severity:** High  
**Type:** Data/logic concern  
**Status:** Open  
**Current status:** Open — awaiting grouped remediation wave (Wave 1).  
**Recommendation:** Verify whether rich reference-range extraction was intended and whether the parser/review DTO is discarding structured range detail.

### UAT-006
**Stage:** Questionnaire  
**Title:** Resting heart rate is missing  
**Expected:** A high-value cardiovascular context input like resting heart rate should be present if it is part of intended Phase 1 context capture.  
**Actual:** No resting heart rate question is present.  
**Severity:** Medium  
**Type:** UX / product-scope concern  
**Status:** Open  
**Current status:** Open — awaiting grouped remediation wave (Wave 3).  
**Recommendation:** Check whether this is intentionally excluded from current governed questionnaire or an omission from desired context set.

### UAT-007
**Stage:** Questionnaire  
**Title:** Energy-level dropdown options feel too limited  
**Expected:** Answer options should let users describe their daily energy meaningfully.  
**Actual:** The dropdown feels too constrained.  
**Severity:** Medium  
**Type:** UX friction / content  
**Status:** Open  
**Current status:** Open — awaiting grouped remediation wave (Wave 3).  
**Recommendation:** Review answer taxonomy for this question and expand or clarify options.

### UAT-008
**Stage:** Questionnaire  
**Title:** Diet-quality 1–10 scale lacks meaning anchors  
**Expected:** Numeric scales should explain what low, middle, and high mean.  
**Actual:** Users are given a number scale without clear interpretation.  
**Severity:** Medium  
**Type:** UX friction / content  
**Status:** Open  
**Current status:** Open — awaiting grouped remediation wave (Wave 3).  
**Recommendation:** Add scale descriptors or helper text.

### UAT-009
**Stage:** Questionnaire  
**Title:** “Unable to control important things” question is unclear  
**Expected:** Stress questions should be plainly worded and easy to understand.  
**Actual:** The intent of the question is unclear.  
**Severity:** Medium  
**Type:** Content/copy  
**Status:** Open  
**Current status:** Open — awaiting grouped remediation wave (Wave 3).  
**Recommendation:** Rewrite in plain language or add explanatory text.

### UAT-010
**Stage:** Questionnaire  
**Title:** “Major life stressors in the past 6 months” question is poor quality  
**Expected:** Stress/life-event questions should feel specific, purposeful, and credible.  
**Actual:** The question feels weak/useless.  
**Severity:** Medium  
**Type:** Content/copy  
**Status:** Open  
**Current status:** Open — awaiting grouped remediation wave (Wave 3).  
**Recommendation:** Reassess whether this question is needed at all; if retained, rewrite it substantially.

### UAT-011
**Stage:** Questionnaire  
**Title:** Excessive repeated “Next” clicks before completion  
**Expected:** Progression should feel efficient and predictable.  
**Actual:** User must click Next around 11 times before the CTA changes to “Complete assessment.”  
**Severity:** High  
**Type:** UX friction  
**Status:** Open  
**Current status:** Open — awaiting grouped remediation wave (Wave 3).  
**Recommendation:** Rework questionnaire flow into clearer grouped sections with fewer serial steps or a visible section-based progress model.

### UAT-012
**Stage:** Product / Repeat usage  
**Title:** Questionnaire answers are not reusable across later uploads  
**Expected:** Returning users should be able to reuse and reconfirm prior context rather than re-enter everything.  
**Actual:** Full questionnaire appears to be repeated.  
**Severity:** High  
**Type:** UX / product capability gap  
**Status:** Open  
**Current status:** Open — awaiting grouped remediation wave (Wave 3).  
**Recommendation:** Add saved baseline context + revalidation flow for repeat uploads.

### UAT-013
**Stage:** Questionnaire  
**Title:** Questionnaire lacks sectioning and feels overwhelming  
**Expected:** Long questionnaires should be grouped into clear sections.  
**Actual:** The experience feels overwhelming.  
**Severity:** High  
**Type:** UX friction  
**Status:** Open  
**Current status:** Open — awaiting grouped remediation wave (Wave 3).  
**Recommendation:** Introduce section structure, progress markers, and chunked completion.

### UAT-014
**Stage:** Questionnaire / Product scope  
**Title:** Unclear whether all questions are necessary for downstream analysis  
**Expected:** Every required question should feel justified by the analysis value it creates.  
**Actual:** Some questions appear superfluous.  
**Severity:** Medium  
**Type:** Product / analysis-scope concern  
**Status:** Open  
**Current status:** Open — awaiting grouped remediation wave (Wave 3).  
**Recommendation:** Audit each question against actual downstream usage and classify as required, optional, future, or removable.

### UAT-015
**Stage:** Upload  
**Title:** Drag-and-drop area lacks hover/highlight feedback  
**Expected:** Dropzone should visibly react when a file is dragged over it.  
**Actual:** File is accepted, but there is no reassuring drag-state highlight.  
**Severity:** Low  
**Type:** Visual polish / UX  
**Status:** Open  
**Current status:** Open — non-blocking polish.  
**Recommendation:** Add drag-over visual state.

### UAT-016
**Stage:** Marker review / Edit parsing results  
**Title:** Reference range cannot be edited manually  
**Expected:** Users correcting parsed results should be able to edit the reference range where needed.  
**Actual:** Range is not editable.  
**Severity:** High  
**Type:** Functional / UX  
**Status:** Open  
**Current status:** Open — investigated; fix not yet implemented (Wave 1).  
**Recommendation:** Decide whether range editing is intentionally locked. If not, enable bounded editing with validation.

### UAT-017
**Stage:** Results / Hero interpretation  
**Title:** Hero interpretation exposes internal governance language instead of meaningful health explanation  
**Expected:** Hero section should explain the main health story in plain English.  
**Actual:** It shows technical ranking/policy language and internal signal IDs.  
**Severity:** High  
**Type:** Content / UX / trust  
**Status:** Open  
**Current status:** Open — awaiting grouped remediation wave (Wave 2).  
**Recommendation:** Remove internal governance text from default user-facing hero layer.

### UAT-018
**Stage:** Results / System groups  
**Title:** System-group narrative is generic and not convincingly tied to actual marker pattern  
**Expected:** Group summary should explain this user’s actual biomarker pattern.  
**Actual:** Cardiovascular narrative is generic boilerplate and does not reconcile the real lipid picture.  
**Severity:** High  
**Type:** Analysis quality  
**Status:** Open  
**Current status:** Open — awaiting grouped remediation wave (Wave 2).  
**Recommendation:** Strengthen pattern-specific narrative and cross-marker interpretation.

### UAT-019
**Stage:** Results / Biomarker evidence  
**Title:** Marker evidence is data-heavy but insight-light  
**Expected:** Biomarker layer should explain meaning, contribution, and relationships.  
**Actual:** It mainly shows values, scores, and ranges with limited interpretive value.  
**Severity:** High  
**Type:** Analysis quality / UX  
**Status:** Open  
**Current status:** Open — awaiting grouped remediation wave (Wave 2).  
**Recommendation:** Add concise “why it matters” and “how it influences the interpretation” content.

### UAT-020
**Stage:** Results / Root-cause reasoning  
**Title:** Supporting and contradictory markers are not surfaced clearly enough  
**Expected:** Users should see which markers support, weaken, or complicate each hypothesis.  
**Actual:** Some reasoning is hinted at, but supporting-marker logic is too thin and opaque.  
**Severity:** High  
**Type:** Analysis quality  
**Status:** Open  
**Current status:** Open — awaiting grouped remediation wave (Wave 2).  
**Recommendation:** Surface supporting, opposing, and missing markers explicitly.

### UAT-021
**Stage:** Results / Advanced analysis  
**Title:** Clinician report is structurally present but low-depth and awkwardly formatted  
**Expected:** Clinician report should feel clinically literate, coherent, and useful.  
**Actual:** It is limited, repetitive, and includes ugly numeric/confidence formatting.  
**Severity:** High  
**Type:** Content / analysis quality  
**Status:** Open  
**Current status:** Open — awaiting grouped remediation wave (Wave 2).  
**Recommendation:** Improve report-generation quality, confidence formatting, and explanatory depth.

### UAT-022
**Stage:** Results / Narrative layer  
**Title:** Rich personalised Gemini narrative does not appear to be active  
**Expected:** User-facing output should show a richer, personalised explanatory layer.  
**Actual:** Output looks like structured backend content with light templating rather than real narrative synthesis.  
**Severity:** High  
**Type:** Functional / product-quality concern  
**Status:** Open  
**Current status:** Open — awaiting grouped remediation wave (Wave 2).  
**Recommendation:** Verify whether Gemini narrative generation is triggered and what input contract it receives.

### UAT-023
**Stage:** Results / Biomarker evidence
**Title:** Multiple biomarkers show “Not scored - no reference range available”
**Expected:** Biomarkers with valid lab ranges in the uploaded panel should retain enough range metadata to be scored where supported.
**Actual:** Some biomarkers, including Folate and free testosterone pct, show “Not scored - no reference range available.”
**Severity:** High
**Type:** Data/logic concern
**Status:** Open
**Current status:** Open — umbrella finding; detail tracked in UAT-023a / UAT-023b (Wave 1).
**Recommendation:** Investigate whether missing scores are caused by parser loss of reference-range detail, missing policy compatibility, or both.

#### UAT-023a

**Stage:** Parse / biomarker scoring  
**Title:** Some parsed biomarkers lose range data and cannot be scored  
**Expected:** Biomarkers with usable source ranges should carry enough range metadata into scoring.  
**Actual:** Some markers such as Folate and free testosterone pct show “Not scored - no reference range available.”  
**Severity:** High  
**Type:** Data/logic concern  
**Status:** Open  
**Current status:** Open — investigated; fix not yet implemented (Wave 1).

#### UAT-023b

**Stage:** Marker review / edit parsing results  
**Title:** Edit flow does not allow correction of missing range data  
**Expected:** If parsing misses or strips range data, users should be able to correct the range during marker review.  
**Actual:** Edit mode does not allow adding or amending range data.  
**Severity:** High  
**Type:** Functional / UX  
**Status:** Open  
**Current status:** Open — investigated; fix not yet implemented (Wave 1).

---

## Triage snapshot

Grouped remediation waves and per-ID status are maintained in **Living tracker — remediation waves** above. The following is a quick severity-oriented index (unchanged in intent from the original pass).

### Launch blockers
None currently confirmed in the latest successful end-to-end run.

### Pre-launch improvements
- UAT-005 — PDF rich reference-range loss
- UAT-011 — Excessive Next-click flow
- UAT-012 — Reusable questionnaire baseline
- UAT-013 — Questionnaire sectioning
- UAT-016 — Range not editable
- UAT-017 — Hero interpretation leaks governance language
- UAT-018 — System-group narrative is generic
- UAT-019 — Marker evidence lacks insight
- UAT-020 — Supporting-marker logic too opaque
- UAT-021 — Clinician report too thin
- UAT-022 — Gemini narrative may not be active

### Important but not blocking
- UAT-006 — Resting heart rate missing
- UAT-007 — Energy dropdown too limited
- UAT-008 — Diet scale lacks anchors
- UAT-009 — Stress question unclear
- UAT-010 — Life stressor question poor
- UAT-014 — Question necessity audit

### Polish
- UAT-004 — SSE stream logs error after completion
- UAT-015 — Drag-and-drop highlight missing

---

## Themes

### 1. Parsing fidelity and review control
- UAT-005
- UAT-016

### 2. Questionnaire UX and repeat-use burden
- UAT-006
- UAT-007
- UAT-008
- UAT-009
- UAT-010
- UAT-011
- UAT-012
- UAT-013
- UAT-014

### 3. Results, narrative, and explanation quality
- UAT-017
- UAT-018
- UAT-019
- UAT-020
- UAT-021
- UAT-022

### 4. Minor frontend polish and lifecycle issues
- UAT-004
- UAT-015

---

## Recommended next focus

If prioritising the next work pass, the highest-value investigations/fixes are:

1. Verify whether Gemini narrative generation is actually firing and what contract it receives (UAT-022)
2. Improve user-facing interpretation quality and remove internal governance/debug language (UAT-017, UAT-018, UAT-020, UAT-021)
3. Address parsing-review fidelity and editable range control (UAT-005, UAT-016)
4. Redesign questionnaire flow around sections, reuse, and necessity audit (UAT-011, UAT-012, UAT-013, UAT-014)
