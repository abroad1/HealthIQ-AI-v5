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

## P1-17 — Remaining PSI blocker resolution pack

**Status:** Complete  
**Date closed:** 2026-06-21  
**Programme block(s):** Block 3 Layer B intelligence/prose substrate; Block 6 Medical safety, research provenance and governance; Block 7 Auditability, reproducibility and traceability  

### Delivered / ticked off
- Adjudicated all 11 in-scope candidates (4 package-identity + 7 derived-marker); 0 production PSI opt-ins.
- All 4 package-identity candidates remain `BLOCKED_PACKAGE_IDENTITY_UNRESOLVED` (STOP gate 1; no cross-ID placement).
- All 7 derived-marker candidates classified `BLOCKED_REQUIRES_CORE_BACKEND_AGENT` (STOP gate 2; `DERIVED_MARKER_IDS` validator policy vs SSOT-canonical `transferrin_saturation`).
- Core backend handoff manifest produced for derived-marker cohort.

### Carry-forwards
- 4 KB-S52c vs KB-S58 CBC package-identity candidates require source-research / re-staging sprint.
- 7 iron-panel PSI require core-engine validator policy resolution before KB opt-in.
- 4 iron Batch C PSI carry compound medical-review and frame-authority blockers independent of derived-marker issue.
- 3 medical-review homocysteine PSI and 2 leukocyte PSI unchanged (out of scope).

### Blockers / risks
- `transferrin_saturation` is SSOT-canonical but hardcoded as derived in activation-readiness validator — Knowledge Bus-only resolution insufficient.
- Cross-ID `pkg_kb52c_*` → `pkg_kb58_*` PSI placement remains architecturally forbidden.

### Recommended next sprint
- P1-DERIVED-METRIC-TRANSFERRIN-SAT-1 (core-engine): resolve `DERIVED_MARKER_IDS` policy; parallel package-provenance sprint for deferred CBC cohort.

---

## P1-18 — Blood/Iron/Oxygen Pass 3 System Activation Pack

**Status:** Complete  
**Date closed:** 2026-06-21  
**Programme block(s):** Block 1 Core systems; Block 3 Layer B intelligence substrate; Block 6 Medical safety and governance; Block 7 Auditability  

### Delivered / ticked off
- Resolved `DERIVED_MARKER_IDS` validator policy for SSOT-canonical lab-provided `transferrin_saturation` (7 staged PSI now activation-ready).
- Activated `signal_transferrin_high` on `wave1_blood_iron_oxygen` domain launch allowlist with test-backed runtime firing.
- Runtime reality map, carry-forward manifest, and sprint report produced.

### Carry-forwards
- Knowledge Bus PSI opt-in for pkg_kb61 and ferritin-high host packages.
- CBC pkg_kb52c identity cohort, iron Batch C medical-review PSI, calculated TSAT mode.
- Additional CBC/iron launch signals pending frame adjudication.

### Blockers / risks
- PSI semantics remain validation-only until KB opt-in sprint completes.
- Subsystem card evidence does not yet reflect fired signal state.

### Recommended next sprint
- P1-19-KB61-PSI-OPT-IN-1 (Knowledge Bus): production PSI opt-in for transferrin-high package; parallel CBC package-provenance sprint.

---

## P1-19 — Blood/Iron/Oxygen KB production intelligence expansion

**Status:** Complete  
**Date closed:** 2026-06-22  
**Programme block(s):** Block 3 Layer B intelligence/prose substrate; Block 6 Medical safety and governance; Block 7 Auditability  

### Delivered / ticked off
- Regenerated activation-ready cohort (7); adjudicated all candidates.
- Production PSI opt-in for `pkg_kb61_transferrin_high_iron_deficiency_transport_upregulation` (ID-matched byte-copy).
- Ferritin-high host creation blocked at Gate 3B (`signal_ferritin_high` collision with `pkg_s24_ferritin_high_overload`).

### Carry-forwards
- 2 ferritin-high PSI require authority reconciliation before host package creation.
- 4 CBC `pkg_kb52c_*` vs `pkg_kb58_*` identity candidates unchanged.
- Iron Batch C medical-review PSI and calculated TSAT mode unchanged.

### Blockers / risks
- Duplicate `signal_ferritin_high` authority prevents Pass 3 ferritin-high production packages without architectural resolution.

### Recommended next sprint
- P1-FERRITIN-HIGH-AUTHORITY-RECONCILIATION-1; parallel P1-CBC-PACKAGE-PROVENANCE-1.

---

## P1-20 — CBC package provenance resolution and PSI opt-in

**Status:** Complete  
**Date closed:** 2026-06-22  
**Programme block(s):** Block 3 Layer B intelligence/prose substrate; Block 6 Medical safety and governance; Block 7 Auditability  

### Delivered / ticked off
- Confirmed canonical four-candidate CBC cohort (P1-19 cf_003–cf_006).
- Provenance proved via shared `cbc_hematology_pass_3.json` source across staged compile manifests and `pkg_kb58_*` production hosts.
- Re-homed and opted in 4 production PSI byte-copies under mapped `pkg_kb58_*` packages.

### Carry-forwards
- No remaining CBC package-provenance blockers from this sprint.
- Ferritin-high authority collision and iron Batch C medical-review items unchanged (out of scope).

### Blockers / risks
- Staged activation-readiness validator continues to report `production_manifest_opt_in: false` for `pkg_kb52c_*` directory names — expected; production opt-in is under `pkg_kb58_*`.

### Recommended next sprint
- P1-FERRITIN-HIGH-AUTHORITY-RECONCILIATION-1.

---

## P1-21 — Ferritin-high signal authority reconciliation and PSI promotion

**Status:** Complete  
**Date closed:** 2026-06-22  
**Programme block(s):** Block 3 Layer B intelligence/prose substrate; Block 6 Medical safety and governance; Block 7 Auditability  

### Delivered / ticked off
- ADR Option A recorded (`ADR-FERRITIN-HIGH-SIGNAL-AUTHORITY-RECONCILIATION-1`).
- `pkg_s24_ferritin_high_overload` deprecated in-place; two `pkg_kb52c_*` ferritin-high production packages created with byte-copied PSI.
- Both packages validate; collision regression passes.

### Carry-forwards
- Iron Batch C medical-review PSI and TSAT calculated mode unchanged (out of scope).

### Blockers / risks
- pkg_s24 directory retained for test compatibility; active authority migrated to pkg_kb52c hosts.

### Recommended next sprint
- Iron Batch C medical-review sprint or bio-oxygen subsystem enrichment per P1-18 carry-forward.

---

## P1-22 — Thyroid Activation Pack

**Status:** Complete  
**Date closed:** 2026-06-22  
**Programme block(s):** Block 1 Core systems; Block 3 Layer B intelligence substrate; Block 6 Medical safety and governance  

### Delivered / ticked off
- First production `lab_range_only` hormonal scoring rail for TSH, FT4, FT3.
- Bounded TSH authority ADR (scoring only; signal intelligence deferred).
- `wave1_thyroid` sixth launch-core domain active with kb47 FT3/FT4 allowlist and TSH exclusion.

### Carry-forwards
- TSH kb52c signal intelligence promotion; FT3 low activation control; thyroid antibody packages; compiled subsystem card evidence.

### Blockers / risks
- Thyroid domain has no compiled subsystem card yet (empty subsystem routing).

### Recommended next sprint
- P1-TSH-KB52C-PROMOTION-1 and P1-22B-THYROID-SUBSYSTEM-CARD-1.

---

## P1-23 — Thyroid Intelligence Surface Completion

**Status:** Complete  
**Date closed:** 2026-06-22  
**Programme block(s):** Block 1 Core systems; Block 3 Layer B intelligence substrate; Block 6 Medical safety and governance  

### Delivered / ticked off
- kb52c TSH packages from Pass 3 Batch_4; legacy s24 TSH deprecated in-place.
- `signal_tsh_high` and `signal_tsh_low` on thyroid domain allowlist.
- `wave1_thy_hormonal_axis` compiled subsystem card registered and runtime evidence emitted.

### Carry-forwards
- FT3 low activation control; thyroid antibody packages.

### Blockers / risks
- None material for P1-23 scope.

### Recommended next sprint
- P1-24 bio-oxygen card depth or deferred thyroid narrative enrichment.

---

## P1-24 — Bio-oxygen Subsystem Signal Depth

**Status:** Complete  
**Date closed:** 2026-06-22  
**Programme block(s):** Block 3 Layer B intelligence substrate  

### Delivered / ticked off
- Enriched `wave1_bio_oxygen_carrying_capacity` with ferritin-high and transferrin-high PSI signal depth.
- New P1-24 compile manifest; estate index updated; P1-3 manifest preserved.

### Carry-forwards
- None from P1-24.

### Blockers / risks
- None material for P1-24 scope.

### Recommended next sprint
- Programme carry-forwards (iron-low, TSAT, antibodies) per prior sprints.

---

## P1-25 — Thyroid MR-v2 Activation Completion

**Status:** Complete  
**Date closed:** 2026-06-23  
**Programme block(s):** Block 3 Layer B intelligence substrate  

### Delivered / ticked off
- MR-v2-cleared activation of `signal_free_t3_low` and `signal_tpo_ab_high` with strict pre-emission gates.
- ADR-THYROID-MR-V2-ACTIVATION-1; thyroid allowlist and medical frame governance updated.
- TPOAb PSI authored; `wave1_thy_hormonal_axis` enriched with FT3-low and TPOAb depth.

### Carry-forwards
- Questionnaire alignment for FT3-low context fields (fail-closed in production).
- TPOAb euthyroid context and TgAb packages remain deferred.

### Blockers / risks
- None material for P1-25 scope; FT3-low remains fail-closed without full questionnaire context.

### Recommended next sprint
- Questionnaire thyroid context alignment or deferred antibody tranche.

---

## P1-26 — MR-v2 Iron + Homocysteine Signal Activation

**Status:** Complete  
**Date closed:** 2026-06-26  
**Programme block(s):** Block 3 Layer B intelligence substrate  

### Delivered / ticked off
- Five MR-v2-cleared iron and homocysteine candidates activated with directly reported TSAT gates.
- Iron allowlist extended; homocysteine predicate routing unchanged; compiled cards enriched.

### Carry-forwards
- Calculated TSAT blocked; hepatocellular iron-high standalone deferred; WBC cohort out of scope.

### Blockers / risks
- None material for P1-26 scope.

### Recommended next sprint
- Programme backlog per prior carry-forwards.

---

## P2-1 — Prose Substrate Wave 1 Wired

**Status:** Complete  
**Date closed:** 2026-06-26  
**Programme block(s):** Block 3 Layer B intelligence/prose substrate  

### Delivered / ticked off
- Iron and thyroid signals wired into `_LEAD_SIGNAL_HINTS` for runtime lead YAML inclusion.
- Governed KB pathway / functional prose for blood-iron-oxygen and thyroid hormone/antibody domains.
- P2-1 regression tests; homocysteine lead and lipid secondary behaviour preserved.

### Carry-forwards
- Frame-level routing (`P2-FRAME-ROUTING-ARCHITECTURE-1`) for signal-specific lead prose selection.
- Full six-domain simultaneous prose deferred (one-lead / one-secondary model).

### Blockers / risks
- Frame-level routing and multi-domain simultaneous prose remain deferred.

### Recommended next sprint
- P2-FRAME-ROUTING-ARCHITECTURE-1 if frame-level or multi-slot prose is required.

---

## P2-2+P2-3 — Retail and Pathway Explainer Expansion

**Status:** Complete  
**Date closed:** 2026-06-27  
**Programme block(s):** Block 3 Layer B intelligence/prose substrate  

### Delivered / ticked off
- Retail biomarker explainer coverage expanded from 17 to 40 governed entries.
- Renal pathway explainer added; missing-marker explainer pack bootstrapped.
- P1-26 M1 mechanical package_id header correction on three iron signal_library files.

### Carry-forwards
- Remaining biomarkers without retail entries; 10 non-iron KBP-473x headers; P2-FRAME-ROUTING, P2-4, Gemini, TSAT, WBC deferred/blocked.

### Blockers / risks
- None material for CONTENT scope.

### Recommended next sprint
- P2-FRAME-ROUTING-ARCHITECTURE-1 or continued retail coverage tranche.

---

## P2-4 — NarrativePayload Brief Hardening

**Status:** Complete  
**Date closed:** 2026-06-29  
**Programme block(s):** Block 3 Layer B → Layer C brief contract  

### Delivered / ticked off
- `NarrativePayloadV1` v1.1 hardened as governed B→C brief contract (LLM deny-default, deny-all semantics, caveat validation, missing-marker representability).
- P2-4 contract tests prove section intents, boundaries, Wave 1 hidden subsystem alignment, and Layer C compiler compatibility.
- Gemini remains inactive; CEO approval gate preserved in carry-forward.

### Carry-forwards
- Builder `future_llm_may_rewrite` explicit opt-in on consumer surfaces; P2-FRAME-ROUTING; P4-1/P4-2 blocked on CEO approval.

### Blockers / risks
- Gemini production activation requires CEO approval and P4-1 design sprint.

### Recommended next sprint
- P4-1 Gemini activation design (CEO gate) or P2-FRAME-ROUTING-ARCHITECTURE-1.

---

## P3-PROSE-DEPTH-1 — Prose Library Depth and Modifier Schema

**Status:** Complete  
**Date closed:** 2026-06-29  
**Programme block(s):** Block 3 Layer B prose content factory  

### Delivered / ticked off
- MR candidate prose asset schema, templates, and modifier fragment templates created.
- Prose coverage matrix inventories retail (40), pathway (5), missing-marker (6), modifier, and gap status.
- MR Batch 001 brief defines beta-critical candidate generation scope (pathways, top 10 retail gaps, modifiers).
- No runtime, production asset, Intelligence Core, or Gemini changes.

### Carry-forwards
- Medical review of MR-BATCH-001B; promotion/import route; modifier binding; frame routing; P4-1 CEO gate; 79/79 vs subset decision.

### Blockers / risks
- None for CONTENT scope; runtime activation intentionally deferred.

### Recommended next sprint
- Medical review of MR-BATCH-001B, then promotion/import design (still candidate-gated).

---

## P3-PROSE-DEPTH-1A — Directional Marker-State Schema Correction

**Status:** Complete  
**Date closed:** 2026-06-29  
**Programme block(s):** Block 3 Layer B prose content factory  

### Delivered / ticked off
- MR candidate schema extended with marker-state asset types (`in_range` / `high` / `low` / `borderline`).
- Required `range_state` and `context_dependencies`; generic clinician-disclaimer wording prohibited for asset caveats.
- MR Batch 001 brief and modifier templates updated to require directional marker-state explainers.

### Carry-forwards
- MR-BATCH-001B medical review; no production promotion until approved.

### Blockers / risks
- None for document/schema scope.

### Recommended next sprint
- MR-BATCH-001B candidate generation / product edit (completed in session; see next entry).

---

## MR-BATCH-001B — Candidate Prose Test Import

**Status:** Complete  
**Date closed:** 2026-06-30  
**Programme block(s):** Block 3 Layer B prose content factory  

### Delivered / ticked off
- 69 MR-BATCH-001B candidate assets retained as `CANDIDATE` in sprint docs pack.
- Test-only loader (`backend/tests/support/mr_candidate_prose_test_v1.py`) with `candidate_test_mode=True` isolation.
- Inspection report and unit tests for representative marker-state / modifier / missing-marker / resilience composition; report untruncated for full prose review.
- Retained as **ROUND_1_BENCHMARK / TEST FIXTURE** — useful for assessing candidate prose quality and future pipeline design; assets remain candidate/test-only.
- Not medically approved; not source of truth for the prose library; not for production promotion.

### Carry-forwards
- MR-BATCH-001B must not proceed to medical review or promotion.
- Round 2 medical prose work requires a new primary research pipeline and a different primary research LLM.
- MR-BATCH-001B is the Round 1 benchmark to beat, not production source content.
- Promotion/import route remains a future design need, but only for future medically accepted Round 2 assets.
- Modifier binding and frame routing deferred; P4-1 Gemini remains CEO-gated; 79/79 vs prioritised retail subset decision still open.

### Blockers / risks
- Narrative compiler / production registries still do not consume candidate assets (intentional).
- Claude Code / MR-BATCH-001B research execution is not trusted as a scalable medical research pipeline due to overlarge run, encoding corruption, scratchpad salvage requirement, and residual medical/prose concerns.
- Risk that future agents misread MR-BATCH-001B as promotion-ready unless benchmark-only status is explicit.

### Recommended next sprint
- `SPRINT-BUILD-PLAN-AUDIT-1 — Sprint build plan to actual codebase audit`
- Purpose: Audit the sprint build plan against the actual codebase and build register before selecting the next implementation sprint.

---

## ARCH-GOV-BASELINE-1 — Programme Baseline and Governance Reset

**Status:** Complete  
**Date closed:** 2026-07-25  
**Programme block(s):** Phase 0 — Governance and evidence consolidation  

### Delivered / ticked off
- Published authoritative maturity baseline: `docs/architecture/HEALTHIQ_AI_CURRENT_STATE_BASELINE_2026-07-25.md`.
- Reconciled `docs/AUTHORITY_MAP.md` to Automation Bus / Knowledge Bus SOP v1.3.1, pre-SOP v0.6.2, Pass 3 protocol DRAFT status, current-state baseline, and audit papers as EVIDENCE.
- Marked `docs/SPRINT_STATUS.md` superseded/stale; continuity remains BUILD register + baseline.
- Corrected MR-BATCH-001B completion/output docs: Round 1 benchmark/test-only; not for medical review as promotion route; candidate assets unchanged.
- Recorded historical governance exceptions for P3-PROSE-DEPTH-1A and MR-BATCH-001B (non-precedential).
- Refreshed RT-5D provenance and golden-panel stale test expectations to current estate/signatures.
- Extended `golden_gate.yml` push/PR triggers to include `main` and `develop` while preserving NO-LLM enforcement.
- No product capability or medical content added.

### Carry-forwards
- Future Stage 0 planning must start from `HEALTHIQ_AI_CURRENT_STATE_BASELINE_2026-07-25.md`.
- Pass 3 protocol remains DRAFT pending human governance ratification.
- Package estate still has zero explicit `source_spec_id` on scanned manifests; multi-frame consumer completeness incomplete; PSI intentionally unwired; controlled beta not authorised.
- Next implementation sprint must not be selected from this entry alone — use pre-SOP / Stage 0 workflow against the new baseline.

### Blockers / risks
- None introduced by this governance reset; prior programme blockers remain as documented in the current-state baseline.

### Recommended next sprint
- Do not select here. Use Stage 0 / pre-SOP workflow against the current-state baseline (planning gate such as `SPRINT-BUILD-PLAN-AUDIT-1` remains a valid planning candidate, not an implementation authorisation).

---

## ARCH-RT-IDENTITY-PROV-1 — Runtime Identity and Provenance Integrity

**Status:** Complete  
**Date closed:** 2026-07-25  
**Programme block(s):** Phase 0 / day-one architecture integrity (identity + provenance)

### Delivered / ticked off
- Subordinate ADR-RT-IDENTITY-PROV-001 published; STOP_GATE_1 PASS.
- Shared activation-frame index helper; interaction / root-cause / report / output-authority / clinician-report paths preserve frames.
- Additive clinician `root_causes` list; legacy `root_cause` only when singleton.
- Package-manifest schema 1.1.0 optional provenance fields; honest provenance status model; identity/provenance gate + inventory.
- compile_manifest_ref vs path reconciled as logical vs estate-index internal (no blind rename).
- Historical continuity note: ARCH-RT-1/2/3 BUILD entries were absent; ADRs remain authoritative (no fabricated retrospective closure).

### Carry-forwards
- Launch-critical kb47 packages remain batch-JSON sourced → provenance BLOCKED / not beta-eligible for explicit-lineage claims until inv_ extraction.
- Family-level legacy WHY still labelled family_level when multi-frame; full frame-specific compiled WHY migration is later work.
- Stale PSI activation-readiness inventory tests remain a disclosed carry-forward unless counts drift from this package.
- Four additional launch-path collapse surfaces (interpretation display publish, domain score assembler, narrative lead resolution, intervention selector) remain for follow-on identity hardening.
- Audit correction refreshed clinician AB/VR fixtures for additive `root_causes` / null multi-finding `root_cause`; expanded unit matrix in `test_arch_rt_identity_prov_1.py`.

### Blockers / risks
- Controlled beta must not claim explicit provenance for batch-JSON launch packages until investigation-spec extraction lands.

### Recommended next sprint
- Stage 0 against current-state baseline; Package 3 Layer B intelligence may proceed after identity/provenance merge (see P3-LAYERB-INTEL-1 entry).

---

## P3-LAYERB-INTEL-1 — Layer B Intelligence Completion (infrastructure slice)

**Status:** Complete (infrastructure; medical asset promotion deferred)  
**Date closed:** 2026-07-25  
**Programme block(s):** Package 3 — Layer B prose routing / WHY depth

### Delivered / ticked off
- Migration/coverage inventory bounded (9-frame cohort; BLOCKED kb47 deferred).
- STOP Gate 1: routing policy accepted; modifier activation deferred to medical review; WHY/Round 2 promotion escalated.
- Frame-routing contract + narrative compiler wiring; modifier binder fail-safe; Layer B asset authority registry; integrity gate CI-wired.
- Package 2 identity/provenance contracts unchanged; MR-BATCH-001B remains test-only; PSI/Gemini not activated.
- No controlled-beta authorisation.

### Carry-forwards
- Medical review required before Round 2 prose or compiled WHY expansion beyond vitamin_d.
- Activating context-modifier catalogue rows.
- inv_ extraction for remaining BLOCKED kb47 packs.

### Blockers / risks
- Controlled-beta reassessment of Layer B content depth remains blocked on medical-reviewed assets.

### Recommended next sprint
- Medical-reviewed Round 2 / compiled WHY expansion for the bounded cohort (do not invent unreviewed claims).

---

## ARCH-CONV-PKG1 — Launch-Path Activation-Frame Identity Closure

**Status:** Complete  
**Date closed:** 2026-07-25  
**Programme block(s):** Architecture convergence Package 1 — frame identity

### Delivered / ticked off
- STOP Gate 1 PASS: no clinical frame-priority policy; interaction-map YAML remains family-level clinical policy.
- Five launch-path surfaces closed for silent bare-`signal_id` collapse (IDL, domain scores, narrative lead, interventions, interaction builder runtime audit).
- Gate 0 pressure set exercised: 8 families / 21 frames.
- Behavioural gate `validate_launch_path_frame_identity_gate.py` wired into architecture validation.
- Additive identity metadata only; no provenance/WHY/prose/PSI/Gemini/threshold changes.
- No architecture-completion or controlled-beta claim.

### Carry-forwards
- Package 2 provenance / lineage attach for launch-critical kb47 INCLUDE rows.
- Gate 2.5 medical-review owner confirmation before Package 3B (from Gate 0 REDESIGN).

### Blockers / risks
- None for Package 1 obligation; medical-review capacity for WHY pilot remains unresolved (Gate 0).

### Recommended next sprint
- ARCH-CONV-PKG2 — provenance and runtime-reachability honesty for launch-critical INCLUDE cohort.

---

## ARCH-CONV-PKG2 — Launch-Critical Provenance and Runtime-Reachability Closure

**Status:** Complete  
**Date closed:** 2026-07-26  
**Programme block(s):** Architecture convergence Package 2 — provenance / reachability

### Delivered / ticked off
- STOP Gate 1 PASS: Wave 1 INCLUDE kept reachable; lineage recovered from Pass 3 (no invented `source_spec_id`).
- Explicit lineage attached for 6 Wave 1 `pkg_kb47_*` packages (free_t3×2, free_t4×2, egfr×2).
- 14 androgen/CK/eos kb47 packages made production non-reachable; assets retained; test opt-in preserved.
- Canonical loader eligibility (`package_runtime_eligibility_v1`) enforced in `SignalRegistry._load`.
- Reachability gate wired into architecture validation; impact + verification reports filed.
- No WHY/prose/PSI/Gemini/threshold changes; no architecture-completion or controlled-beta claim.

### Carry-forwards
- Gate 2.5 medical-review owner confirmation before Package 3B (from Gate 0 REDESIGN).
- Non–Wave-1 kb47 assets remain BLOCKED on disk pending later disposition/extraction if re-included.

### Blockers / risks
- None for Package 2 obligation; medical-review capacity for WHY pilot remains unresolved (Gate 0).

### Recommended next sprint
- Gate 2.5 / Package 3 sequencing per convergence plan (human-gated).

---

## ARCH-CONV-GATE2_5 — WHY Pilot Medical Review Ownership and Capacity

**Status:** Complete (conditions 1–4 closed 2026-07-26)  
**Date closed:** 2026-07-26  
**Programme block(s):** Architecture convergence Gate 2.5

### Delivered / ticked off
- Dual-gate operating model ratified; GPT named Head of Medical Research; Anthony named production ratifier; capacity confirmed for bounded 5/10 pilot.

### Carry-forwards
- ARCH-CONV-PKG3 Phases 1–3 evidence/design/review pack; Gate C medical review + ratification; then Phase 4–6.

### Blockers / risks
- Package 3B promotion blocked until Gate C.

### Recommended next sprint
- ARCH-CONV-PKG3 WHY authority migration (stop at Gate C for GPT + Anthony).

---

## ARCH-CONV-PKG3 — WHY Authority Migration (Phases 1–6 / Gate C closed)

**Status:** Complete — merged to `main` (`2ecb02a`)  
**Date:** 2026-07-26  
**Programme block(s):** Architecture convergence Package 3

### Delivered / ticked off
- Six standalone inv YAML extractions (PKG2 method) + lineage attach.
- TPO euthyroid frame indexed; Gate A/B passed; Gate C pack ratified (GPT + Anthony).
- Per-activation_key WHY authority register; 9 COMPILED_ACTIVE artefacts; metabolic REJECTED.
- Vitamin D legacy retirement confirmation; dual-authority prevention; parity + verification reports.
- `validate_compiled_why_authority_gate.py` wired into architecture validation gate.
- Merged and published to `origin/main`.

### Carry-forwards
- Estate-wide WHY migration beyond the 5/10 pilot (separate work).
- Final programme audit + human UAT (`ARCH-CONV-FINAL-AUDIT`).

### Blockers / risks
- None for pilot Package 3 obligations (merged).

### Recommended next sprint
- `ARCH-CONV-FINAL-AUDIT` (in progress) — independent closure audit + Anthony UAT.

---

## ARCH-CONV-FINAL-AUDIT — Final Independent Convergence Audit

**Status:** Complete — decision **CORRECT**; correction package closed; residual estate gate supersedes programme PASS claim  
**Date:** 2026-07-26 (CORRECT-1 closed 2026-07-27; residual audit 2026-07-27)  
**Programme block(s):** Architecture convergence programme closure

### Delivered / ticked off
- Independent re-verification of PKG1/PKG2/PKG3 gates and material tests (PASS).
- Rejected metabolic WHY path live-proven inert; 13/13 automated E2E scenarios PASS.
- Layer C boundary inventory (BOUNDARY_LEAKs).
- Live UAT of analysis `e34aaedf-b09f-42f0-8cc8-4653a00b4c10` with API payload inspection.
- Final programme decision: **CORRECT** (then executed as `ARCH-CONV-CORRECT-1`).

### Carry-forwards
- Estate-wide Day-One convergence not claimed; see `ARCH-CONV-RESIDUAL-AUDIT-1`.
- Controlled-beta readiness (separate).

### Blockers / risks
- None remaining from the four CORRECT themes after CORRECT-1 merge.

### Recommended next sprint
- Human ratification of residual-audit GO/NO-GO (`ARCH-CONV_v5_completion_vs_v6_decision.md`).

---

## ARCH-CONV-CORRECT-1 — End-to-End Medical Authority and Layer C Boundary Closure

**Status:** CLOSED — merged and published to `origin/main`  
**Date:** 2026-07-26 (merged/published 2026-07-27)  
**Programme block(s):** Architecture convergence programme closure (correction)  
**Merge SHA (feature tip):** `bfcb5fd` — fast-forward into `main`  
**Live UAT analysis:** `20a99882-085c-475d-bb26-2ff28a13183a`

### Delivered / ticked off
- WS1 canonical frame runtime authority (`frame_runtime_authority_v1`): the `REJECTED` metabolic homocysteine frame is inactive at registry load, evaluation output and report assembly — absent from fired signals, `top_findings`, interventions, summaries and replay.
- WS2 retired `methylation capacity` / `Methylation pathway pattern` wording from the legacy hcy elevation-context hypothesis and the IDL retail label, sourcing replacement wording from the ratified pack; executable fingerprint check added.
- WS3 governed MCV co-service policy (`frame_co_service_policy_v1.yaml` + `frame_co_service_v1`): anchor is morphology context only; specific frames serve causally only behind their ratified evidence gates; no unratified combined pattern; additive `why_role` DTO field.
- WS4 all 12 Layer C `BOUNDARY_LEAK` inventory rows closed; new backend `primary_driver_v1` authority projection; `ClusterInsightPanel` and `biomarkerPatternRelevance` deleted; governed frontend copy modules added.
- New correction gate, 16 backend regression scenarios, 4 frontend boundary render tests, 13/13 final-audit scenario harness, and a before/after replay harness for `e34aaedf-b09f-42f0-8cc8-4653a00b4c10`.
- PKG1/PKG2/PKG3, identity-provenance, Layer B integrity and architecture validation gates all re-run at exit 0.
- Closure stabilisation: explicit waist cm/inches contract; auth stale-session → 401 recovery (no `/auth/me` loop).
- Live human UAT PASS on analysis `20a99882-085c-475d-bb26-2ff28a13183a`; MCV inventory coexistence documented as intentional WHY-scoped co-service (regression locked).

### Programme status stamped
```text
ARCH-CONV-CORRECT-1 CLOSED
MIGRATED COHORT SAFE
TARGET AUTHORITY MODEL PROVEN
ESTATE-WIDE DAY-ONE CONVERGENCE NOT YET PROVEN
FINAL V5 / V6 DECISION REMAINS OPEN
```

### Carry-forwards
- Pre-existing output-authority provenance regression involving `signal_homocysteine_high::inv_homocysteine_high`.
- Historic analysis impact from the former waist-unit defect.
- Result-versioning policy advancement for regeneration after medical-authority changes.
- Estate-wide residual runtime completion programme (pending ratification of residual audit).

### Blockers / risks
- No controlled-beta readiness claim is made or implied by this package.
- Whole-estate Day-One compliance is explicitly not claimed.

### Recommended next sprint
- Ratify `ARCH-CONV-RESIDUAL-AUDIT-1` decision; only then author Package A/B/C implementation prompts.

---

## ARCH-CONV-RESIDUAL-AUDIT-1 — Estate Residual Runtime Audit and v5/v6 Gate

**Status:** Complete (decision-support; awaiting GPT review + Anthony ratification)  
**Date:** 2026-07-27  
**Programme block(s):** Final architecture decision gate (pre-SOP investigation)

### Delivered / ticked off
- Programme closure record for ARCH-CONV-CORRECT-1.
- Estate residual runtime inventory, active authority map, legacy dependency register, dual-authority findings, day-one layer assessment, v5 vs v6 decision pack.
- Principal recommendation: **GO — RETAIN V5 AND COMPLETE BOUNDED CONVERGENCE** (3 minimum packages; no implementation authored).

### Carry-forwards
- Human ratification of GO/NO-GO.
- If ratified: author Automation Bus prompts for Packages A (estate WHY), B (dual/fallback harden), C (replay/provenance/versioning).
- Controlled-beta readiness remains separate.

### Blockers / risks
- Estate WHY still legacy-dominant outside the 5/10 pilot; dual elevation-context authority remains material until Package B.

### Recommended next sprint
- Do not implement until ratification.

---

## ARCH-CONV-A Wave 0 — Homocysteine suppression / identity closure

**Status:** Complete (suppression disposition; not a compile wave)  
**Date closed:** 2026-07-27  
**Programme block(s):** Architecture convergence — Package A estate WHY / Wave 0  
**Evidence:** `docs/architecture/ARCH-CONV-A_wave0_suppression_closure.md`; `docs/architecture/ARCH-CONV-A_STOP_A_ratification_record.md` (D-2)  
**Merge into main:** `290ac18` — `merge: ARCH-CONV-A revised-scope Waves 0-2 into main`

### Delivered / ticked off
- `signal_homocysteine_elevation_context` ratified `FOLD_SUPPRESS` — no independent WHY frame; no investigation spec; no compiled artefact.
- Finding context retained only via governed non-causal signal / card / presentation surfaces.
- Existing `signal_homocysteine_high` COMPILED_ACTIVE / REJECTED pilot frames left unchanged.
- STOP A also recorded D-3 bilirubin `MERGE_TO_ONE` (WHY-target identity → `signal_hyperbilirubinemia`; not a Wave 0 compile).

### Carry-forwards
- Shared legacy `hcy_hypotheses_v1.yaml` remains connected for elevation-context and high frames — physical / selector retirement is Package B scope.
- Inflammation-only legacy hyp disposition deferred with shared-file retirement.

### Blockers / risks
- Dual-serve / shared-file shadow risk remains until Package B exclusivity / retirement work.

### Recommended next sprint
- ARCH-CONV-A Wave 1 — thyroid WHY-authority migration (completed subsequently).

---

## ARCH-CONV-A Wave 1 — Thyroid WHY-authority migration

**Status:** Complete — Gate 1/2 ratified; STOP C PASS after CORRECT re-audit  
**Date closed:** 2026-07-28  
**Programme block(s):** Architecture convergence — Package A estate WHY / Wave 1 thyroid  
**Gate 1:** `GPT-GATE1-ARCH-CONV-A-W1-THYROID-2026-07-28-v1`  
**Gate 2:** `ANTHONY-GATE2-ARCH-CONV-A-W1-THYROID-2026-07-28-v1`  
**STOP C:** `docs/architecture/ARCH-CONV-A_STOP_C_wave1_runtime_proof.md` (`STOP C final status: PASS`)  
**Merge into main:** `290ac18`

### Delivered / ticked off
- Five thyroid frames compiled and registered `COMPILED_ACTIVE`:
  - `signal_tsh_high::inv_tsh_high_hypothyroidism` (morphology_context)
  - `signal_tsh_low::inv_tsh_low_hyperthyroidism` (morphology_context)
  - `signal_free_t3_high::inv_free_t3_high_t3_predominant_thyrotoxicosis`
  - `signal_free_t4_high::inv_free_t4_high_thyrotoxicosis_context`
  - `signal_free_t4_low::inv_free_t4_low_thyroid_hormone_deficiency`
- Pass-3 parallel TSH pattern keys recorded `LEGACY_RETIRED` (WHY superseded).
- Runtime pilot cohort extended; duplicate-authority resolution hardened; FT4-low presence STOP C CORRECT applied.
- Prior pilot frames `signal_free_t3_low` / `signal_tpo_ab_high` retained as COMPILED_ACTIVE.

### Carry-forwards
- `signal_thyroid_tsh_context` remains legacy / non-compiled (not a Wave 1 frame).
- `signal_tgab_high` remains legacy-only (no Wave 1 TgAb frame).

### Blockers / risks
- None open for the five ratified Wave 1 frames after STOP C PASS.

### Recommended next sprint
- ARCH-CONV-A Wave 2 — lipid WHY-authority migration.

---

## ARCH-CONV-A Wave 2 — Lipid WHY-authority migration

**Status:** Complete — Gate 1/2 ratified; STOP C PASS (independent audit)  
**Date closed:** 2026-07-28  
**Programme block(s):** Architecture convergence — Package A estate WHY / Wave 2 lipid  
**Gate 1:** `GPT-GATE1-ARCH-CONV-A-W2-LIPID-2026-07-28-v1`  
**Gate 2:** `ANTHONY-GATE2-ARCH-CONV-A-W2-LIPID-2026-07-28-v1`  
**STOP C:** `docs/architecture/ARCH-CONV-A_STOP_C_wave2_runtime_proof.md` (`Wave 2 STOP C: PASS`)  
**Merge into main:** `290ac18`

### Delivered / ticked off
- Three lipid frames compiled and registered `COMPILED_ACTIVE`:
  - `signal_ldl_cholesterol_high::inv_ldl_high_dyslipidaemia` (causal, narrowed)
  - `signal_hdl_cholesterol_low::inv_hdl_low_cardiovascular` (CONTEXT_ONLY / morphology_context)
  - `signal_triglycerides_high::inv_triglycerides_high_metabolic` (causal, narrowed)
- Competing Pass-3 parallel LDL/HDL/TG and unauthorised total-cholesterol WHY rows recorded `LEGACY_RETIRED`.
- Wave 1 thyroid boundaries proven unchanged on lipid panels; 0 new regressions vs main at STOP C boundary.

### Carry-forwards
- `signal_total_cholesterol_high`, `signal_apoa1_cardio_risk`, `signal_lipid_transport_dysfunction` — no Wave 2 causal compiled authority.
- ApoA1 / lipid-transport remain research / legacy gaps for later waves.

### Blockers / risks
- Total-cholesterol WHY intentionally not authorised; pilot membership suppresses retired / unregistered keys (no silent legacy win).

### Recommended next sprint
- Wave 3 renal planning (delivered later as successor package ARCH-CONV-B, not as ARCH-CONV-A Wave 3 compile).

---

## ARCH-CONV-A Wave 3 — Renal creatinine/urea WHY-authority migration

**Status:** Deferred under ARCH-CONV-A; creatinine/urea outcome delivered via successor `ARCH-CONV-B` (urate not migrated)  
**Date closed:** ARCH-CONV-A Wave 3 compile never closed on Package A — STOP B pack preserved then reframed; creatinine/urea runtime closed 2026-07-30 under `ARCH-CONV-B`  
**Programme block(s):** Architecture convergence — Package A Wave 3 (historical) → `ARCH-CONV-B` renal WHY  
**ARCH-CONV-A evidence:** `docs/architecture/ARCH-CONV-A_wave3_renal_medical_review_pack.md` (preserved prep only); revised-scope split `docs/architecture/ARCH-CONV-A_revised_scope_and_split_decision.md`  
**ARCH-CONV-B Gate 1 / Gate 2:** `ARCH-CONV-B-GATE1-HMR-2026-07-30` / `ARCH-CONV-B-GATE2-ANTHONY-2026-07-30`  
**ARCH-CONV-B STOP C:** `docs/architecture/ARCH-CONV-B_STOP_C_runtime_proof.md` (`STOP_C_APPROVED_BY_HEAD_OF_ARCHITECTURE`)  
**Merge into main:** `cdc6cf3` — `merge: ARCH-CONV-B renal WHY authority (Gate PASS, STOP C approved)`

### Delivered / ticked off
- Under ARCH-CONV-A: Wave 3 STOP B pack assembled then removed from Package A branch by revised-scope split; no A Wave 3 compile/runtime on the revised-scope merge (`290ac18`).
- Under ARCH-CONV-B (successor vehicle for the creatinine/urea Wave 3 intent):
  - `signal_creatinine_high::inv_creatinine_high_renal` → `COMPILED_ACTIVE` (narrowed causal renal-clearance / filtration-marker lane)
  - `signal_urea_high::inv_urea_high_renal` → `COMPILED_ACTIVE` (CONTEXT_ONLY / morphology_context)
  - Package-only Pass-3 creatinine/urea parallels recorded `LEGACY_RETIRED` / non-reachable
  - No eGFR WHY displacement; no urate authority change

### Carry-forwards
- **`signal_urate_high` remains separate and incomplete** — investigation spec exists (`inv_uric_acid_high_metabolic`); no `COMPILED_ACTIVE` register row; legacy WHY still the runtime path. Do not treat Wave 3 / ARCH-CONV-B as having completed urate.
- eGFR WHY / chronicity / UACR gaps remain outside creatinine/urea compiled lanes.

### Blockers / risks
- Advisories must not attribute creatinine/urea compile to ARCH-CONV-A Wave 3 completion; Package A revised scope explicitly deferred Wave 3.
- Urate naming (`urate` vs `uric_acid` spec_id) remains an identity caveat for any future urate compile wave.

### Recommended next sprint
- Remaining Package A estate targets (e.g. urate; iron/haematology; metabolic residuals) and/or Package B dual-authority retirement — distinct from ALT E-track signal activation.

---

## Continuity audit — ARCH-CONV-A Waves 0–3 (2026-08-01)

Documentation-only reconciliation on `main`. Sources: STOP A/C proofs, Gate decision artefacts, `compiled_why_authority_register_v1.yaml`, `ROOT_CAUSE_TARGET_SPECS`, merged history (`290ac18`, `cdc6cf3`). No runtime, Knowledge Bus packages, tests, medical rules, activation decisions, or governance decisions changed.

### Register entries added
- `ARCH-CONV-A Wave 0` — Homocysteine suppression / identity closure
- `ARCH-CONV-A Wave 1` — Thyroid WHY-authority migration
- `ARCH-CONV-A Wave 2` — Lipid WHY-authority migration
- `ARCH-CONV-A Wave 3` — Renal creatinine/urea (deferred under A; delivered via ARCH-CONV-B; urate excluded)

### Inventory file updated
- `docs/architecture/ARCH-CONV-A_active_why_target_inventory.md` — freshness banner; re-derived classifications for Waves 0–3 affected signals + ALT post E/E2/E3; urate recorded separately.

### Exact files changed by this continuity audit
- `docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md`
- `docs/architecture/ARCH-CONV-A_active_why_target_inventory.md`

---

## ARCH-CONV-E — ALT Package Assets and Runtime Activation Boundary

**Status:** CLOSED — merged and published to `origin/main`  
**Date closed:** 2026-07-31  
**Programme block(s):** Architecture convergence — ALT WHY / Knowledge Bus activation boundary  
**Merge SHA:** `4bcdaef` — `merge(arch-conv-e): ALT package assets and runtime activation boundary`

### Delivered / ticked off
- Six governed ALT packages built/regenerated from canonical Pass 3 research (hepatocellular, mixed, cholestatic, muscle, bilirubin severity, metabolic/MASLD), with mandatory assets and lineage; none activated by placement alone.
- Governed `package_runtime_activation_register_v1.yaml` introduced: non-launch-critical production reachability requires explicit `activation_key` membership (ADR-RT-002).
- Pre-existing placement→reachability defect closed: `ELIGIBILITY_OUT_OF_COHORT` no longer treated as production-reachable.
- Lifecycle exception for the in-scope runtime-boundary excursion retrospectively ratified (`ARCH-CONV-E_lifecycle_exception_and_closure.md`).
- S24 ALT-high remained the sole loaded ALT frame at E close; six new packages withheld pending explicit promotion.

### Carry-forwards
- Runtime promotion/activation of Pass 3 ALT frames (R-value authority, contextual frames) deferred to follow-on sprints.
- Medical Gate 1 / Gate 2 decisions for ALT pattern activation not completed in E (decision register remained pre-Gate).

### Blockers / risks
- Package placement must never again imply activation; register membership is mandatory for non-launch-critical frames.

### Recommended next sprint
- ARCH-CONV-E2 — ALT R-value runtime authority and selective frame activation.

---

## ARCH-CONV-E2 — ALT R-Value Runtime Authority

**Status:** CLOSED — Gate 2 ratified; merged and published to `origin/main`  
**Date closed:** 2026-08-01  
**Programme block(s):** Architecture convergence — ALT biochemical-pattern / R-value authority  
**Gate 1:** `ARCH-CONV-E2-GATE1-HMR-2026-08-01`  
**Gate 2:** `ARCH-CONV-E2-GATE2-ANTHONY-2026-08-01` (RATIFIED)  
**Evidence:** `docs/architecture/ARCH-CONV-E2_implementation_evidence.md`

### Delivered / ticked off
- Governed `r_value_alt_alp` compute authority retained/enforced (lab ULNs only; fail-closed missing ULN/pairing).
- Canonical Pass 3 hepatocellular package activated as S24 successor with ranked hypothesis selection (R≥5 predominant; R unavailable/ineligible → general ALT-high context).
- Mixed R-value package activated for `2 < R < 5`; hepatocellular does not emit general fallback in that band.
- S24 ALT-high superseded and withheld; former Batch 5 inferred keys remain unreachable.
- `alt_biochemical_pattern_axis` collision governance updated; ALP/GGT `liver_injury_axis` preserved.
- Cholestatic / muscle / bilirubin severity / metabolic packages remained withheld at E2 close (explicit).
- Bilirubin lab-range escalation on canonical hepatocellular frame proven; consumer Hy’s Law wording prohibited.

### Carry-forwards
- Remaining four ALT contextual packages (cholestatic, muscle, bilirubin severity, metabolic) still required explicit disposition/activation work (completed later by ARCH-CONV-E3 for eligible paths).

### Blockers / risks
- None open from E2 medical design after Gate 2; withheld contextual frames were intentional, not defects.

### Recommended next sprint
- ARCH-CONV-E3 — remaining ALT contextual authority.

---

## ARCH-CONV-E3 — ALT Contextual Authority Completion

**Status:** CLOSED — Gate 2 ratified; merged and published to `origin/main`  
**Date closed:** 2026-08-01  
**Programme block(s):** Architecture convergence — ALT contextual / subordinate authority  
**Gate 1:** `ARCH-CONV-E3-GATE1-HMR-2026-08-01`  
**Gate 2:** `ARCH-CONV-E3-GATE2-ANTHONY-2026-08-01` (RATIFIED)  
**Merge SHA:** `6ccbf3f` — `merge: ARCH-CONV-E3 ALT contextual authority (Gate 2 ratified)`  
**Evidence:** `docs/architecture/ARCH-CONV-E3_implementation_evidence.md`

### Delivered / ticked off
- Cholestatic R≤2 activated as subordinate ALT biochemical-pattern context (owns R≤2 among ALT frames; does not displace ALP/GGT source primary).
- Muscle activated lab-only (`creatine_kinase` above lab max pre-emission gate).
- Metabolic/MASLD activated lab-only (compound any_of metabolic lab corroboration; no MASLD diagnosis from ALT alone).
- Bilirubin severity represented as override/escalation only on active ALT frames; package remains withheld; Hy’s Law consumer diagnosis prohibited.
- E2 hepatocellular/mixed behaviour and R-value boundaries preserved; non-ALT activation delta none.
- KB-S24 ALT escalate harness pinned to canonical hepatocellular activation key (test-harness remediation).

### Carry-forwards
- No governed, runtime-consumed user-context contract for exercise/trauma/myopathy/statin or declared metabolic-risk corroboration (`context_modifier_catalogue_draft_v1.yaml` remains non-runtime).
- No canonical Pass 3 numeric threshold for “very high ALT must not be explained away” (muscle/metabolic safeguard blocked).
- No activation-key-level suppression between subordinate ALT cholestatic context and ALP/GGT primary under the current collision contract (family-level supporting membership unsafe; contract extension deferred).

### Blockers / risks
- User-context and very-high-ALT gaps are partial blockers only; lab-only muscle/metabolic paths are active and Gate-2-ratified.
- Collision activation-key-level suppress remains a contract gap, not a silent medical override.

### Recommended next sprint
- Programme-wide: context-modifier runtime contract (if ALT user-context paths are required); Head of Medical Research numeric “very high ALT” decision; optional collision-contract extension for activation-key-level ALP/GGT vs ALT-cholestatic suppress — or continue Residual Package A/B/C estate work if prioritised over ALT residual gaps.

---

## ARCH-CONV-F — Haematology Compiled-WHY Authority

**Status:** CLOSED — Gate 2 ratified; independent audit PASS; merged and published to `origin/main`  
**Date closed:** 2026-08-01  
**Programme block(s):** Architecture convergence — haematology compiled-WHY authority (`signal_ferritin_high`, `signal_hemoglobin_low`)  
**Gate 1:** `ARCH-CONV-F-GATE1-HMR-2026-08-01` (`APPROVED_WITH_NARROWING`)  
**Gate 2:** `ARCH-CONV-F-GATE2-ANTHONY-2026-08-01` (`APPROVED`)  
**Merge SHA:** `65646cc` — `merge: ARCH-CONV-F haematology compiled-WHY authority (Gate 2 ratified)`  
**Evidence:** `docs/audit-papers/ARCH-CONV-F_implementation_and_verification_report.md`  
**Medical decision register:** `docs/architecture/ARCH-CONV-F_medical_decision_register.yaml`

### Delivered / ticked off
- Compiled-WHY authority for `signal_ferritin_high` (`signal_ferritin_high::inv_ferritin_high_overload`).
- Compiled-WHY authority for `signal_hemoglobin_low` (`signal_hemoglobin_low::inv_hgb_low_anemia`).
- `+2 COMPILED_ACTIVE` authority rows (21 → 23).
- `+3 LEGACY_RETIRED` competing WHY rows (15 → 18).
- Ferritin constrained to flat non-causal `morphology_context` authority under every tested data state.
- Haemoglobin constrained to anaemia / reduced oxygen-carrying-capacity causal authority.
- MCV/RDW retained as non-owning morphology/context only (no independent aetiology / underproduction claim).
- Concern-only escalation safeguards retained for ferritin `>1000 µg/L` and haemoglobin `<80 g/L`.
- Existing package-layer and PSI status unchanged for all five affected packages.
- Independent audit PASS.

### Carry-forwards
- Haemoglobin primary oxygen-carrying PSI research and promotion remains open (structurally distinct from compiled-WHY closure).
- `signal_hba1c_high` compiled-WHY remains open.
- `signal_urate_high` compiled-WHY remains open.
- ALT compiled-WHY identity remains unresolved and must not be treated as A3-ready.

### Blockers / risks
- None open from ARCH-CONV-F medical design after Gate 2 and independent audit PASS.
- Selecting HbA1c or urate without a repository-grounded Stage 0 sequencing advisory risks out-of-order estate work.

### Recommended next sprint
- Run a repository-grounded Stage 0 sequencing advisory before selecting HbA1c or urate as the next compiled-WHY wave.

---

## ARCH-CONV-G — Urate Compiled-WHY Authority

**Status:** CLOSED — Gate 2 ratified; independent audit PASS; merged and published to `origin/main`  
**Date closed:** 2026-08-01  
**Programme block(s):** Architecture convergence — urate compiled-WHY authority (`signal_urate_high`)  
**Gate 1:** `ARCH-CONV-G-GATE1-HMR-2026-08-01` (`APPROVED_WITH_NARROWING`)  
**Gate 2:** `ARCH-CONV-G-GATE2-ANTHONY-2026-08-01` (`APPROVED`)  
**Merge SHA:** `af2207d` — `merge: ARCH-CONV-G urate compiled-WHY authority (Gate 2 ratified)`  
**Evidence:** `docs/audit-papers/ARCH-CONV-G_implementation_and_verification_report.md`  
**Medical decision register:** `docs/architecture/ARCH-CONV-G_medical_decision_register.yaml`

### Delivered / ticked off
- Compiled-WHY authority for `signal_urate_high`.
- Canonical activation key: `signal_urate_high::inv_uric_acid_high_metabolic`.
- `why_role: morphology_context` (flat; non-causal).
- `+1 COMPILED_ACTIVE` authority row (23 → 24).
- `+1 LEGACY_RETIRED` competing WHY row (18 → 19) for `signal_urate_high::inv_urate_high_gout_crystal_deposition_risk`.
- Competing gout/crystal-deposition frame retired for WHY ownership only; valid content subordinate risk context only.
- Package-layer and PSI status unchanged.
- `or_uric_acid_renal_risk` (`egfr < 60`) retained as concern escalation only; no CKD diagnosis from one eGFR result; no eGFR-owned WHY.
- Creatinine and urea compiled authority unchanged.
- No new alias, signal identity, SSOT biomarker, derived metric, compiler mechanism, or frontend change.
- Urate versus uric acid remains existing terminology convention only.
- Independent audit PASS.

### Carry-forwards
- `signal_hba1c_high` compiled-WHY closed by ARCH-CONV-H (see ARCH-CONV-H register entry).
- ALT compiled-WHY identity remains unresolved at A4.
- Package B and Package C sequencing remains downstream of further Package A outputs.
- No eGFR/UACR/chronicity independent WHY authority was created.

### Blockers / risks
- None open from ARCH-CONV-G medical design after Gate 2 and independent audit PASS.

### Recommended next sprint
- Proceed to ALT / Package A residual sequencing per Active Carry-Forward (post-ARCH-CONV-H).

---

## ARCH-CONV-H — HbA1c Compiled-WHY Authority

**Status:** CLOSED — Gate 2 ratified; merged and published to `origin/main`  
**Date closed:** 2026-08-01  
**Programme block(s):** Architecture convergence — HbA1c compiled-WHY authority (`signal_hba1c_high`)  
**Gate 1:** `ARCH-CONV-H-GATE1-HMR-2026-08-01` (`APPROVED_WITH_NARROWING`)  
**Gate 2:** `ARCH-CONV-H-GATE2-ANTHONY-2026-08-01` (`APPROVED`)  
**Merge SHA:** `f91ef18` — `merge: ARCH-CONV-H HbA1c compiled-WHY authority (Gate 2 ratified)`  
**Evidence:** `docs/audit-papers/ARCH-CONV-H_implementation_and_verification_report.md`  
**Medical decision register:** `docs/architecture/ARCH-CONV-H_medical_decision_register.yaml`

### Delivered / ticked off
- Compiled-WHY authority for `signal_hba1c_high`.
- Canonical activation key: `signal_hba1c_high::inv_hba1c_high_glycaemia`.
- `why_role: morphology_context` (flat; non-causal).
- `+1 COMPILED_ACTIVE` authority row (24 → 25).
- `+1 LEGACY_RETIRED` competing WHY row (19 → 20) for `signal_hba1c_high::inv_hba1c_high_diabetes_range_hyperglycemia`.
- Competing diabetes-range hyperglycemia frame retired for WHY ownership only.
- Package-layer and PSI status unchanged.
- HbA1c `>= 48 mmol/mol`: diabetes-range concern requiring clinical confirmation only.
- TG/HDL: subordinate metabolic-pattern context only; no metabolic-syndrome diagnosis.
- Adjacent identities unchanged: `signal_hba1c_pct_high`, `signal_glucose_dysregulation_hba1c_context`.
- No treatment directives, chronicity inference, diabetes subtype, complications, causal attribution, or diagnosis from HbA1c alone.
- No new alias, signal identity, SSOT biomarker, derived metric, compiler mechanism, or frontend change.

### Carry-forwards
- ALT compiled-WHY identity closed by ARCH-CONV-I (see ARCH-CONV-I register entry).
- Package B and Package C sequencing remains downstream of further Package A outputs.
- No eGFR/UACR/chronicity independent WHY authority was created.
- `signal_hba1c_pct_high` and glucose-dysregulation context remain separate identities (not migrated).

### Blockers / risks
- None open from ARCH-CONV-H medical design after Gate 2.

### Recommended next sprint
- Proceed to Package B / dual-authority sequencing per Active Carry-Forward (post-ARCH-CONV-I).

---

## ARCH-CONV-I — ALT Compiled-WHY Identity Resolution

**Status:** CLOSED — Gate 2 ratified; merged and published to `origin/main`  
**Date closed:** 2026-08-02  
**Programme block(s):** Architecture convergence — ALT compiled-WHY identity (`signal_alt_high` / `signal_hepatic_alt_context`)  
**Gate 1:** `ARCH-CONV-I-GATE1-HMR-2026-08-02` (`APPROVED_WITH_NARROWING`, Outcome A `MAP_AND_COMPILE`)  
**Gate 2:** `ARCH-CONV-I-GATE2-ANTHONY-2026-08-02` (`APPROVED`)  
**Merge SHA:** `bd04648` — `merge: ARCH-CONV-I ALT compiled-WHY identity resolution (Gate 2 ratified)`  
**Evidence:** `docs/audit-papers/ARCH-CONV-I_implementation_and_verification_report.md`  
**Medical decision register:** `docs/architecture/ARCH-CONV-I_medical_decision_register.yaml`

### Delivered / ticked off
- Compiled-WHY authority for `signal_alt_high::inv_alt_high_r_value_hepatocellular_biochemical_pattern`.
- `why_role: morphology_context` (flat; non-causal).
- `+1 COMPILED_ACTIVE` (25 → 26).
- `+5 LEGACY_RETIRED` (20 → 25): legacy `signal_hepatic_alt_context::inv_alt_context` plus four live sibling WHY-skip rows.
- CRP/inflammatory-coupling excluded; no compile / no transfer.
- Hard-coded legacy thresholds not transferred.
- E2/E3 R-value, contextual-frame, package, PSI and activation behaviour unchanged.
- No runtime alias; no Hy’s Law / MASLD / fibrosis / treatment / chronicity / unsupported causal claims.
- Registry target added for `signal_alt_high` emit (stub asset only).

### Carry-forwards
- Package B and Package C sequencing remains downstream.
- eGFR / UACR / chronicity independent WHY boundary unchanged.
- Sibling ALT frames remain package-active without independent compiled WHY (by design).

### Blockers / risks
- None open from ARCH-CONV-I medical design after Gate 2.

### Recommended next sprint
- Repository-grounded Stage 0 advisory for next residual (Package B Wave 2 / Package C sequencing).

---

## ARCH-CONV-PKGB-1 — Homocysteine Dual-Authority Exclusivity and Shared Resolver Defect Closure

**Status:** CLOSED — Gate 2 ratified; merged and published to `origin/main`  
**Date closed:** 2026-08-02  
**Programme block(s):** Architecture convergence — Package B Wave 1 (homocysteine exclusivity + bare-key resolver)  
**Gate 1:** `ARCH-CONV-PKGB-1-GATE1-HMR-2026-08-02` (`APPROVED_WITH_NARROWING`)  
**Gate 2:** `ARCH-CONV-PKGB-1-GATE2-ANTHONY-2026-08-02` (`APPROVED`)  
**Merge SHA:** `027d2e7` — `merge: ARCH-CONV-PKGB-1 homocysteine exclusivity and bare-key resolver (Gate 2 ratified)`  
**Evidence:** `docs/audit-papers/ARCH-CONV-PKGB-1_implementation_and_verification_report.md`  
**Medical decision register:** `docs/architecture/ARCH-CONV-PKGB-1_medical_decision_register.yaml`

### Delivered / ticked off
- `signal_homocysteine_elevation_context` FOLD_SUPPRESS implemented as WHY-only `LEGACY_RETIRED` skip.
- `signal_homocysteine_high` remains sole compiled-WHY owner (content unchanged).
- Bare-key resolver: zero-`COMPILED_ACTIVE` all-non-owning pilot families → governed `skip`.
- Genuine ambiguity / missing governance still fail closed.
- Five zero-compiled pilots covered: `ldl_high`, `hdl_low`, `total_cholesterol_high`, `hgb_low`, `hepatic_alt_context`.
- HbA1c / urate stale hypothesis-ID assertions aligned.
- Dedicated regression suite `test_arch_conv_pkgb_1_exclusivity_resolver.py`.
- Phenotype expectations updated for elevation-context non-emit.
- `CF-ARCH-CONV-DUAL-HCY-1` resolved.

### Carry-forwards
- Package B Wave 2 (L-04 / L-05 / L-06) remains open — product-policy blocked.
- Package C replay / provenance / versioning remains downstream.
- Optional later hygiene: physical retirement/disconnect of shared `hcy_hypotheses_v1.yaml` (not required for exclusivity).
- Baseline gate still omits `test_root_cause_v1_homocysteine.py` (golden-panel heavy); disclosed in verification report.

### Blockers / risks
- None open from ARCH-CONV-PKGB-1 medical design after Gate 2.

### Recommended next sprint
- Package B Wave 2 only after L-04/L-05/L-06 product-policy decisions, or Package C sequencing per advisory.

---

## ARCH-CONV-PKGC-1 — Historic Waist-Unit Stale-Detection and Remediation

**Status:** CLOSED — Anthony merge authorised; merged and published to `origin/main`  
**Date closed:** 2026-08-02  
**Programme block(s):** Architecture convergence — Package C Wave 1 (waist stale-detection + historic remediation)  
**Data governance:** `ARCH-CONV-PKGC-1-DATA-GOV-ANTHONY-2026-08-02` (`APPROVED_WITH_CONDITIONS`)  
**Merge SHA:** `d056931` — `merge: ARCH-CONV-PKGC-1 waist stale-detection and historic remediation (Anthony merge authorised)`  
**Evidence:** `docs/audit-papers/ARCH-CONV-PKGC-1_implementation_and_verification_report.md`  
**Remediation register:** `docs/architecture/ARCH-CONV-PKGC-1_data_remediation_register.yaml`

### Delivered / ticked off
- LAUNCH-CORE-3 stale rule `legacy_waist_unit_defect:used_incorrectly` (allowlist + remediation stamp).
- Governed MARK_STALE_NO_REWRITE planner/runner (dry-run default; `--write` gated).
- Live re-verify + dry-run + write of exactly the Anthony-approved 12 analysis IDs.
- Original waist values and units preserved; audit stamp in `processing_metadata`.
- Idempotent post-write dry-run (`ALREADY_REMEDIATED` / `NO_OP_IDEMPOTENT` × 12).
- Collateral stamp check: 0 unexpected analysis IDs.
- `CF-ARCH-CONV-WAIST-1` resolved.

### Carry-forwards
- Package C provenance-identity (`CF-ARCH-CONV-PROV-1` / PKGC-2) remains open.
- Result-versioning regeneration advancement (`CF-ARCH-CONV-VERSION-1`) remains open.
- Governed waist remap / regeneration remain deferred.

### Blockers / risks
- None open for the Anthony-approved 12-row MARK_STALE_NO_REWRITE disposition.

### Recommended next sprint
- Package C Wave 2 provenance-identity / versioning per advisory, or Package B Wave 2 after product-policy decisions.

---

## Continuity audit — ARCH-CONV-E / E2 / E3 (2026-08-01)

Documentation-only post-merge reconciliation. Sources: committed implementation evidence, medical decision registers, Gate 2 ratification docs, merge state on `main` (`6ccbf3f` / aligned `origin/main`). No runtime, package medical content, tests, or governance decisions changed by this audit.

### Register entries added
- `ARCH-CONV-E`
- `ARCH-CONV-E2`
- `ARCH-CONV-E3`

### Register entries updated
- None prior incomplete E/E2/E3 rows existed; Residual-Audit recommended-next left intact (estate Package A/B/C remains open and distinct from the ALT E-track).

### Carry-forwards newly promoted to central day-one Active Carry-Forward Register
- Governed runtime user-context contract gap (ALT muscle/metabolic declared-history paths).
- Canonical numeric “very high ALT” threshold gap.
- Activation-key-level ALT-cholestatic vs ALP/GGT primary suppress contract gap.

### Stale items closed or removed
- Sprint-local E2 carry-forward “four contextual packages remain withheld” superseded by E3 delivery (recorded as closed via E3 entry delivered list; not duplicated as an open E2 programme obligation).
- No day-one Active Carry-Forward bullets were removed: none uniquely belonged to completed E/E2/E3 deliverables.

### Exact files changed by this continuity audit
- `docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md`
- `docs/sprints/healthiq_day_one_architecture_rework_sprint_plan_FINAL_updated.md`

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
