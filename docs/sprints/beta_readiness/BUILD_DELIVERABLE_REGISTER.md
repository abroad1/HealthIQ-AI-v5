# HealthIQ AI — Beta Readiness Build Deliverable Register

Purpose:

To track what has been delivered against the eight-block beta-readiness build programme, what remains open, and what should happen next.

This register is a lightweight continuity log for the HealthIQ AI beta-readiness programme. It is not a substitute for formal audits, ADRs, closure papers, test evidence, or merge records.

Entries should record only:
- what was delivered / ticked off from the programme;
- carry-forwards;
- material blockers or risks;
- recommended next sprint.

Entries should not list every file touched or every non-change.

---

## BETA-BASELINE-REGISTER-1 — Final strategy baseline and build register

**Status:** Complete  
**Date closed:** 2026-06-20  
**Programme block(s):** Phase 0 — Governance and evidence consolidation  

### Delivered / ticked off
- Final definitive beta-readiness strategy baseline adopted as the first authority document for the eight-block build programme.
- Lightweight build deliverable register created for sprint-to-sprint continuity.
- Register path established at `docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md`.

### Carry-forwards
- P1-1 must use the final strategy baseline as its first authority document.
- Future sprint closures must append a short register entry using this format.

### Blockers / risks
- None from this baseline/register sprint, unless repository authority registration remains unresolved.

### Recommended next sprint
- P1-1 — Launch-core domain build-materials map.

---

## P1-1 — Launch-core domain build-materials map

**Status:** Complete  
**Date closed:** 2026-06-20  
**Programme block(s):** Block 1 Core health systems model; Block 2 Subsystems and depth model; Block 3 Layer B intelligence/prose substrate  

### Delivered / ticked off
- Evidence-backed build-materials map for all three missing launch-core domains (blood/iron/oxygen, thyroid/energy regulation, kidney function).
- Knowledge Bus package count verified at 187 (matches strategy 186–187 range).
- P1-2 first-domain recommendation recorded: kidney function (safest bounded implementation path).

### Carry-forwards
- All three domains lack compiled cards and Wave 1 domain assembler wiring.
- Thyroid FT3 low register drift must be reconciled before thyroid domain implementation.
- Blood/iron TIBC/UIBC and urea frame-index gaps remain open.

### Blockers / risks
- No domain is fully implementation-ready without P1-2+ domain-card and subsystem wiring work.
- Thyroid domain carries highest clinical gating risk if sequenced before register hygiene.

### Recommended next sprint
- P1-2 — Kidney function launch-core domain card and subsystem wiring.

---

## P1-2 — Kidney function domain card

**Status:** Complete  
**Date closed:** 2026-06-20  
**Programme block(s):** Block 1 Core health systems model; Block 2 Subsystems and depth model; Block 3 Layer B intelligence/prose substrate  

### Delivered / ticked off
- First missing launch-core domain implemented as `wave1_kidney` with compiled filtration subsystem evidence.
- Domain assembler, subsystem routing, kidney domain card implementation, and targeted tests added. eGFR scoring-policy inclusion deferred post-audit.

### Carry-forwards
- Urea signal launch visibility deferred pending frame-index adjudication.
- ACR/UACR standalone package still absent.
- Frontend render-only integration and P2 kidney prose substrate remain open.

### Blockers / risks
- Fourth domain increases replay/DTO surface area; frontend must remain render-only.
- Collision resolver regression must stay green on merge.

### Recommended next sprint
- P1-3 — Blood / iron / oxygen domain card (after CBC/adjudication hygiene), or P2-1 kidney prose substrate in parallel.

---

## P1-3 — Blood / iron / oxygen domain card

**Status:** Complete  
**Date closed:** 2026-06-20  
**Programme block(s):** Block 1 Core health systems model; Block 2 Subsystems and depth model; Block 3 Layer B intelligence/prose substrate  

### Delivered / ticked off
- Second missing launch-core domain implemented as `wave1_blood_iron_oxygen` with compiled oxygen-carrying subsystem evidence.
- Domain assembler, subsystem routing, narrative copy, replay contract, and targeted tests added. Scoring policy unchanged (existing cbc rail reused).

### Carry-forwards
- Launch-visible CBC / iron signal wiring deferred pending frame adjudication.
- Iron / ferritin / transferrin scoring bands and TIBC/UIBC remain open.
- Frontend render-only integration and P2 blood/iron prose substrate remain open.

### Blockers / risks
- Fifth domain increases replay/DTO surface area; frontend must remain render-only.
- Kidney collision and P1-2 regression tests must stay green on merge.

### Recommended next sprint
- P1-4 — Thyroid / energy regulation domain card (after FT3 register reconciliation), or P2-1 prose substrate in parallel.

---

## Build programme register rule for future sprints

At closure, future beta-readiness sprints should append a short entry using this format:

```markdown
## <WORK_ID> — <Sprint title>

**Status:** Complete / Partial / Blocked  
**Date closed:** <YYYY-MM-DD>  
**Programme block(s):** <e.g. Block 1 Core systems, Block 3 Layer B prose>  

### Delivered / ticked off
- <what this sprint completed against the beta-readiness programme>
- <major decision, map, document, implementation or validation outcome>

### Carry-forwards
- <what still needs to be done later>
- <known gaps exposed by this sprint>

### Blockers / risks
- <only material blockers or risks that affect future work>

### Recommended next sprint
- <next work package recommendation>
```

Rules:

* Keep the entry short.
* Do not list every file touched.
* Do not list every file not touched.
* Do not duplicate the formal audit or closure report.
* Focus on programme continuity: what is now done, what remains, and what comes next.
