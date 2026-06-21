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

## P1-4 — Thyroid / energy regulation domain card

**Status:** Blocked  
**Date closed:** 2026-06-20  
**Programme block(s):** Block 1 Core health systems model; Block 2 Subsystems and depth model; Block 3 Layer B intelligence/prose substrate  

### Delivered / ticked off
- Phase 1 thyroid authority and FT3/register reconciliation completed and documented.
- STOP decision recorded: unresolved FT3-low register conflict, inert hormonal scoring rail, inactive TSH runtime packages — no runtime implementation performed.

### Carry-forwards
- Reconcile FT3 low across Batch 2 thyroid governance registers before retry.
- Define hormonal scoring rail or explicit unscored-card authority before domain assembler work.
- kb52c TSH and kb59 antibody promotion/adjudication remain open.

### Blockers / risks
- Implementing now would require scoring-policy improvisation or activation of deferred/context-dependent signals.
- A partial FT3/FT4-only domain without TSH would be clinically misleading at launch.

### Recommended next sprint
- P3-FT3-REGISTER-RECONCILIATION (governance) then P1-4 retry; or continue P2 prose substrate in parallel.

---

## P1-5 — FT3 / thyroid authority reconciliation

**Status:** Complete  
**Date closed:** 2026-06-20  
**Programme block(s):** Block 1 Core health systems model; Block 3 Layer B intelligence/prose substrate; Block 6 Medical safety, research provenance and governance  

### Delivered / ticked off
- Conservative reconciliation of FT3 low register drift across frame index, full-coverage activation, and readiness registers.
- ADR-THYROID-FT3-AUTHORITY-RECONCILIATION-1 accepted with authoritative launch positions for all thyroid patterns.
- P1-4 retry preconditions explicitly documented (scoring rail + TSH authority still required).

### Carry-forwards
- Hormonal scoring rail remains inert; requires dedicated scoring sprint.
- kb52c TSH and kb59 antibody packages remain inactive for launch.
- FT3 low remains deferred pending future activation-control sprint.

### Blockers / risks
- P1-4 thyroid domain card still blocked until hormonal scoring and TSH launch authority are resolved.
- Partial FT3/FT4-only domain without TSH remains clinically misleading.

### Recommended next sprint
- Hormonal scoring rail sprint, then TSH promotion governance, then P1-4 retry.

---

## P1-6R — Thyroid scoring architecture recovery

**Status:** Complete  
**Date closed:** 2026-06-20  
**Programme block(s):** Block 1 Core health systems model; Block 3 Layer B intelligence/prose substrate; Block 6 Medical safety, research provenance and governance  

### Delivered / ticked off
- Recovery verification: failed P1-6 branch not merged; contamination artefacts absent from main.
- Scoring architecture audit from code/tests: lab-range primitive exists but system orchestration requires six-band YAML blocks.
- ADR-THYROID-SCORING-LAB-RANGE-ARCHITECTURE-1 accepted: thyroid scoring blocked until scoring-engine architecture change.

### Carry-forwards
- Scoring-engine must gain governed lab-range-only biomarker membership pattern before hormonal policy sprint.
- TSH kb52c launch authority and kb59 antibody inactivity unchanged.
- FT3 low remains deferred/inactive.

### Blockers / risks
- P1-4 thyroid domain card remains blocked (scoring engine + TSH authority).
- Adding hardcoded thyroid bands would repeat failed P1-6 anti-pattern.

### Recommended next sprint
- P1-SCORING-LAB-RANGE-ENGINE, then P1-SCORING-HORMONAL-POLICY, then TSH promotion governance, then P1-4 retry.

---

## P1-7 — Research-to-runtime adequacy gate

**Status:** Complete  
**Date closed:** 2026-06-20  
**Programme block(s):** Block 1 Core health systems model; Block 2 Subsystems and depth model; Block 3 Layer B intelligence/prose substrate; Block 6 Medical safety, research provenance and governance; Block 7 Auditability, reproducibility and traceability  

### Delivered / ticked off
- Programme-level research-to-runtime adequacy gate across launch-core and second-wave domain candidates.
- Machine-readable readiness matrix (14 candidates) distinguishing research presence from runtime promotion readiness.
- Systemic finding: estate is research-rich but unevenly promoted; thyroid pattern recurs as promotion-discipline risk.

### Carry-forwards
- Thyroid launch-core gap (#6 of 6) blocked until P1-SCORING-LAB-RANGE-ENGINE and TSH authority resolution.
- Five MED-REV-1 hidden subsystems and orphan wave1_liver_flat_v1 estate drift.
- Second-wave silent inflammation and hormone balance deferred.

### Blockers / risks
- Implementing thin runtime cards without compiled evidence + scoring rail + signal authority repeats P1-4/P1-6 failure mode.
- Frame adjudication backlog blocks signal depth on P1-2/P1-3 implemented domains.

### Recommended next sprint
- P1-SCORING-LAB-RANGE-ENGINE (scoring-engine architecture prerequisite for hormonal/thyroid path).

---

## P1-8 — Scoring lab-range engine

**Status:** Complete  
**Date closed:** 2026-06-20  
**Programme block(s):** Block 1 Core health systems model; Block 3 Layer B intelligence/prose substrate; Block 6 Medical safety, research provenance and governance; Block 7 Auditability, reproducibility and traceability  

### Delivered / ticked off
- Governed `scoring_type: lab_range_only` biomarker rule path in scoring engine and policy validator.
- ADR-SCORING-LAB-RANGE-ONLY-BIOMARKER-RULES-1 accepted; production scoring policy unchanged.

### Carry-forwards
- Hormonal rail population with lab_range_only thyroid markers (separate policy sprint).
- TSH kb52c launch authority and P1-4 domain card retry remain blocked.

### Blockers / risks
- Enabling hormonal rail without TSH authority or medical sign-off remains prohibited.
- Production thyroid scoring not activated by this sprint.

### Recommended next sprint
- P1-SCORING-HORMONAL-POLICY — add lab_range_only thyroid-axis entries and enable hormonal rail.

---

## P1-9 — Pass 3 research-to-runtime exploitation map

**Status:** Complete  
**Date closed:** 2026-06-20  
**Programme block(s):** Block 1 Core health systems model; Block 2 Subsystems and depth model; Block 3 Layer B intelligence/prose substrate; Block 6 Medical safety, research provenance and governance; Block 7 Auditability, reproducibility and traceability  

### Delivered / ticked off
- Direct inspection of 10 Pass 3 JSON files (173 v3.0.0 investigation specs extracted).
- Research-to-runtime exploitation map and machine-readable matrix (18 material clusters).
- Confirmed large unpromoted tail between Pass 3 JSON corpus and runtime-visible surfaces.

### Carry-forwards
- CBC/hematology Pass 3 cluster (22 specs) blocked on frame adjudication before signal promotion.
- Thyroid/hormonal Pass 3 research blocked on hormonal policy + TSH authority.
- MED-REV-1 hidden subsystems have Pass 3 backing but await medical-review promotion.

### Blockers / risks
- Promotion factory must use batch cohorts with STOP gates — not one-marker sprints or mass promotion.
- KB-S24 YAML tracker (30 specs) is parallel line, not full Pass 3 JSON coverage.

### Recommended next sprint
- P1-SCORING-HORMONAL-POLICY (hormonal lab_range_only policy + rail enablement).

---

## P1-10 — Pass 3 launch-core signal intelligence Batch A

**Status:** Complete  
**Date closed:** 2026-06-20  
**Programme block(s):** Block 1 Core health systems model; Block 2 Subsystems and depth model; Block 3 Layer B intelligence/prose substrate; Block 6 Medical safety, research provenance and governance; Block 7 Auditability, reproducibility and traceability  

### Delivered / ticked off
- First governed Pass 3 → PSI batch promotion factory run (16 staged PSI entries, 6 clusters).
- Authoritative repository confirmed (ADR-008 per-package PSI + `generated_pilot` staging).
- Runtime activation unchanged; production package manifests untouched.

### Carry-forwards
- Manifest opt-in wiring for staged Batch A PSI deferred to P1-11.
- CBC/iron, thyroid, hormone, inflammation clusters deferred per P1-9.
- eGFR scoring-policy wiring remains blocked.

### Blockers / risks
- Medical review required for homocysteine, liver, urea clusters before activation.
- Frame adjudication blocks CBC/iron Batch B.

### Recommended next sprint
- P1-SCORING-HORMONAL-POLICY; then P1-11 Batch B (CBC/iron + manifest opt-in).

---

## P1-11 — Pass 3 CBC / iron / oxygen signal intelligence Batch B

**Status:** Complete  
**Date closed:** 2026-06-20  
**Programme block(s):** Block 1 Core health systems model; Block 2 Subsystems and depth model; Block 3 Layer B intelligence/prose substrate; Block 6 Medical safety, research provenance and governance; Block 7 Auditability, reproducibility and traceability  

### Delivered / ticked off
- Second governed Pass 3 → PSI batch promotion (18 staged PSI entries, 7 CBC/iron/oxygen clusters).
- Frame adjudication completed: hemoglobin-primary and derived-metric clusters explicitly deferred with documented blockers.
- Runtime activation unchanged; production package manifests and scoring policy untouched.

### Carry-forwards
- Hemoglobin Pass 3 research authoring required before primary oxygen-carrying promotion.
- Medical-review cohort for MCHC spherocytic and clonal/marrow platelet patterns.
- Manifest opt-in wiring for Batch A + Batch B deferred to post-review activation sprint.

### Blockers / risks
- `transferrin_saturation` derived-metric dependency remains unresolved for primary promotion.
- Clonal myeloproliferative and marrow-suppression platelet frames require medical sign-off.

### Recommended next sprint
- P1-12 Batch C (leukocyte/residual CBC + hemoglobin research); then manifest opt-in governance sprint.

---

## P1-12 — Pass 3 deferred CBC / iron / haematology Batch C

**Status:** Complete  
**Date closed:** 2026-06-21  
**Programme block(s):** Block 1 Core health systems model; Block 2 Subsystems and depth model; Block 3 Layer B intelligence/prose substrate; Block 6 Medical safety, research provenance and governance; Block 7 Auditability, reproducibility and traceability  

### Delivered / ticked off
- Re-adjudicated all eight P1-11 deferred CBC/iron/haematology clusters with direct Pass 3 source inspection.
- Promoted 7 staged non-runtime PSI entries (iron panel partial + leukocyte shift); six clusters remain deferred with explicit blockers.
- Reclassified hemoglobin and transferrin-saturation deferrals as source-support gaps, not schema gaps.

### Carry-forwards
- Hemoglobin Pass 3 research authoring required before primary oxygen-carrying promotion.
- Medical-review cohort for MCHC spherocytic and clonal/marrow platelet patterns.
- Manifest opt-in for Batch A/B/C staged PSI deferred to post-review activation sprint.

### Blockers / risks
- High-risk haematology frames (MCHC spherocytic, clonal/marrow platelet) require medical sign-off before staging.
- transferrin_saturation derived-metric runtime dependency unresolved for primary promotion.

### Recommended next sprint
- P1-MED-REV-HEMATOLOGY-1 (medical-review cohort) plus hemoglobin Pass 3 research authoring.

---

## P1-13 — Staged PSI activation-readiness gate

**Status:** Complete  
**Date closed:** 2026-06-21  
**Programme block(s):** Block 1 Core health systems model; Block 2 Subsystems and depth model; Block 3 Layer B intelligence/prose substrate; Block 6 Medical safety, research provenance and governance; Block 7 Auditability, reproducibility and traceability  

### Delivered / ticked off
- Inventoried all 41 staged PSI artefacts from P1-10, P1-11 and P1-12 with activation-readiness classification per package.
- Added report-only validator `validate_staged_psi_activation_readiness.py` with targeted unit tests; no staged PSI or compile manifest mutations.

### Carry-forwards
- Universal compile-manifest hash mismatch across 41 packages requires dedicated recompile sprint before opt-in.
- SSOT biomarker identity adjudication for `wbc`, `lym`, `plt`, `non_hdl`; derived-marker review for `transferrin_saturation` (7 iron-panel PSI).
- Medical-review, frame-authority and leukocyte system-mapping overlays from prior batches remain blocking after hash repair.

### Blockers / risks
- Zero artefacts activation-ready until manifest hash integrity and SSOT/derived-marker blockers are resolved through authority sprints.

### Recommended next sprint
- P1-14 staged compile manifest integrity recompile plus SSOT biomarker adjudication prep; parallel medical-review cohort for high-risk haematology frames.

---

## P1-14 — Staged PSI hash repair and activation cohort lock

**Status:** Complete  
**Date closed:** 2026-06-21  
**Programme block(s):** Block 1 Core health systems model; Block 2 Subsystems and depth model; Block 3 Layer B intelligence/prose substrate; Block 6 Medical safety, research provenance and governance; Block 7 Auditability, reproducibility and traceability  

### Delivered / ticked off
- Repaired SHA-256 hash integrity on all 41 staged compile manifests without altering PSI medical content.
- Re-ran P1-13 activation-readiness validator and locked cohort map: 22 activation-ready candidates, 19 blocked across biomarker, derived-marker, and medical-review classes.

### Carry-forwards
- Production opt-in pilot for 22 activation-ready candidates; SSOT adjudication for 9 biomarker-blocked PSI; derived-metric review for 7 iron-panel PSI; medical review for 3 homocysteine/leukocyte PSI.

### Blockers / risks
- Blocked cohorts must not enter production opt-in until respective authority sprints complete.

### Recommended next sprint
- P1-15 production PSI opt-in pilot for activation-ready cohort only.

---

## P1-15 — First production PSI opt-in pilot

**Status:** Complete  
**Date closed:** 2026-06-21  
**Programme block(s):** Block 3 Layer B intelligence/prose substrate; Block 6 Medical safety, research provenance and governance; Block 7 Auditability, reproducibility and traceability  

### Delivered / ticked off
- Verified production PSI opt-in contract: validation-governed only on launch-critical path with `behavioural_impact: NONE`.
- Completed 18 ID-matched production PSI opt-ins with byte-identical PSI copies.

### Carry-forwards
- 4 activation-ready candidates blocked pending package identity/provenance adjudication (`BLOCKED_AMBIGUOUS_PACKAGE_MAPPING`); cross-ID `pkg_kb52c_* → pkg_kb58_*` placements reverted per GPT Option B.
- 19 other staged PSI remain blocked (biomarker, derived-marker, medical-review).

### Blockers / risks
- P1-15 no longer contains cross-ID production PSI placements; deferred cohort requires explicit package identity decision before opt-in.

### Recommended next sprint
- P1-16 SSOT biomarker identity adjudication for blocked staged PSI cohort.

---

## P1-16 — PSI identity & blocker remediation pack

**Status:** Complete  
**Date closed:** 2026-06-21  
**Programme block(s):** Block 3 Layer B intelligence/prose substrate; Block 6 Medical safety, research provenance and governance; Block 7 Auditability, reproducibility and traceability  

### Delivered / ticked off
- Adjudicated all 4 P1-15 package-identity deferrals — all remain `BLOCKED_PACKAGE_IDENTITY_UNRESOLVED` (STOP gate 1; no cross-ID placement).
- Adjudicated all 9 biomarker-identity blocked candidates; 4 production PSI opt-ins via canonical ID normalisation only (no SSOT edits).
- Production opt-ins: urea high prerenal, non-HDL high, plt high reactive, plt low peripheral consumption.

### Carry-forwards
- 4 package-identity candidates require KB-S52c vs KB-S58 provenance / re-staging sprint.
- 3 biomarker candidates blocked (erythropoietin/jak2/host-package gaps).
- 2 leukocyte PSI remain medical-review out of scope.
- 7 derived-marker and 3 medical-review staged PSI unchanged.

### Blockers / risks
- Cross-ID `pkg_kb52c_*` → `pkg_kb58_*` PSI placement remains architecturally forbidden without identity-normalisation tooling.

### Recommended next sprint
- P1-17 package provenance adjudication for deferred KB-S58 CBC cohort; parallel derived-marker authority sprint for iron-panel PSI.

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
