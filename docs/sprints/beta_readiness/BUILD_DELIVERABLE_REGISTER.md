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
