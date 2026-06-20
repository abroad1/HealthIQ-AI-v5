# P1-7 — Research-to-Runtime Adequacy Gate for Remaining Systems and Subsystems

## 1. Executive summary

- **Why this gate was run:** P1-4 through P1-6R showed that rich upstream medical research does not automatically translate into governed, testable, runtime-safe launch artefacts. A programme-level gate was required before further system-card work proceeds.
- **What it found:** The estate is **research-rich but unevenly promoted**. Five of six launch-core consumer domains have Layer B domain rows and compiled subsystem evidence; thyroid remains blocked; second-wave domains are uncompiled. Five compiled subsystems exist but are MED-REV-1 hidden. One compiled liver artefact is orphaned from the estate index.
- **Isolated or systemic?** **Systemic.** The thyroid failure pattern (register drift, inert scoring rail, inactive TSH authority, band-required scoring architecture) is not thyroid-specific — it reflects recurring gaps between research packages, governance registers, compiled cards, scoring rails, signal promotion, and runtime integration.
- **Ready areas:** Cardiovascular and blood sugar domains (full runtime integration); kidney and blood/iron/oxygen domains (implemented with bounded carry-forwards); four user-visible compiled subsystems.
- **Blocked areas:** Thyroid/energy regulation (scoring architecture + signal authority); second-wave silent inflammation and hormone balance (uncompiled/unmapped); five hidden subsystems pending medical-review promotion; orphan `wave1_liver_flat_v1` estate drift.
- **Recommended next sprint:** **P1-SCORING-LAB-RANGE-ENGINE** — scoring-engine architecture change prerequisite to hormonal rail and thyroid domain retry (per P1-6R ADR).

## 2. Programme context

| Prior sprint | Outcome relevant to P1-7 |
|---|---|
| P1-2 kidney | First missing launch-core domain implemented (`wave1_kidney`, `wave1_ren_glomerular_filtration`); urea/eGFR/ACR carry-forwards remain |
| P1-3 blood / iron / oxygen | Second missing domain implemented (`wave1_blood_iron_oxygen`); empty signal allowlist; cbc rail only |
| P1-4 thyroid | STOP at authority gate — no runtime implementation |
| P1-5 FT3 reconciliation | FT3 low deferred/inactive; P1-4 retry still requires scoring rail + TSH authority |
| P1-6R scoring architecture | Lab-range primitive exists; system orchestration requires six-band YAML blocks; thyroid scoring blocked until engine sprint |

Launch-core progress: **5 of 6** consumer domains wired in `domain_score_assembler.py` (cardiovascular, blood sugar, liver, kidney, blood/iron/oxygen). **Thyroid absent.**

## 3. Method

### Authority documents read

- `docs/strategy/beta_readiness/HEALTHIQ_AI_BETA_READINESS_DEFINITIVE_STRATEGY_FINAL_2026-06-20.md`
- `docs/sprints/beta_readiness/P1-1` through `P1-6R` sprint reports
- `docs/architecture/ADR-THYROID-FT3-AUTHORITY-RECONCILIATION-1.md`
- `docs/architecture/ADR-THYROID-SCORING-LAB-RANGE-ARCHITECTURE-1.md`
- `docs/architecture/ADR-LAYER-BOUNDARY-RECONCILIATION-1.md`
- `docs/architecture/User Health to Systems Map_FINAL.md`
- `docs/strategy/eight_block_beta_readiness/EIGHT_BLOCK_BETA_READINESS_COMPARISON_AND_PROGRAMME_RECOMMENDATION_2026-06-18.md`
- `docs/strategy/LAYER_ARCHITECTURE_AUTHORITY_INDEX_2026-06-17_r2.md`
- `docs/AUTHORITY_MAP.md` (read only)
- `docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md`

### Directories inspected (read only)

- `knowledge_bus/compiled/`, `knowledge_bus/compiled/health_system_cards/`, `knowledge_bus/compiled/manifests/`
- `knowledge_bus/governance/`, `knowledge_bus/packages/`, `knowledge_bus/pathway_explainers_v1/`
- `backend/core/analytics/`, `backend/core/knowledge/`, `backend/core/dto/`
- `backend/ssot/scoring_policy.yaml`, `backend/tests/`
- `docs/intelligence/`, `docs/testing/`, `docs/architecture/`

**Absent path (recorded honestly):** `docs/medical_review/` does not exist. Medical-review status was inferred from MED-REV-1 visibility tiers in code and governance registers, not from a dedicated review directory.

### Search terms used

system, subsystem, health_system, compiled card, card evidence, runtime_active_canonical, compiled_not_promoted, deferred, activation_eligibility, scoring_policy, system_weight, Pass 3, frame identity, authority register, pathway explainer, package_refs, thyroid, inflammation, hormone.

### Classification taxonomy

Single primary classification per row from the approved P1-7 taxonomy; secondary blockers listed where evidence supports multiple constraints.

### Limitations

- No runtime execution or package loading tests were run (CONTENT-only sprint).
- Package estate breadth (187 packages) was sampled via representative paths and P1-1 map; not every package was individually classified.
- Medical-review status for hidden subsystems is inferred from `WAVE1_MED_REV1_HIDDEN_SUBSYSTEM_IDS` rather than per-subsystem review documents (no `docs/medical_review/` tree).

## 4. Estate-level finding

The medical research estate is best described as:

**Research-rich but unevenly promoted**, with concurrent **governance-conflicted** pockets (thyroid/TSH), **scoring-blocked** hormonal rail, **prose/explainer-thin** areas (liver, blood/iron, second-wave domains), and **test-thin** gaps for unimplemented domains.

It is not research-thin at the package level (187 KB packages). The bottleneck is promotion discipline: compiled cards, signal authority alignment, scoring-rail membership, domain assembler wiring, and prose substrate must move together — thyroid demonstrated the cost of skipping this gate.

## 5. Readiness matrix

| System / subsystem candidate | Primary classification | Upstream research | KB packages | Pass 3/spec support | Signal authority | Frame/root-cause authority | Scoring readiness | Compiled card evidence | Prose/explainer readiness | Test readiness | Runtime integration readiness | Evidence paths | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Cardiovascular health (domain) | READY_FOR_RUNTIME_CARD | Strong | Strong | Partial | Strong | Partial | Strong | Strong | Partial | Strong | Strong | domain_score_assembler.py; wave1_subsystem_evidence.py:20-25 | 2 of 3 subsystems hidden |
| Blood sugar control (domain) | READY_FOR_RUNTIME_CARD | Strong | Strong | Partial | Strong | Partial | Strong | Strong | Partial | Strong | Strong | domain_score_assembler.py; wave1_subsystem_evidence.py:26-29 | insulin-metabolic hidden |
| Liver health (domain) | RESEARCH_PRESENT_RUNTIME_READY_AFTER_MINOR_WIRING | Strong | Strong | Partial | Partial | Partial | Strong | Strong | Weak | Partial | Strong | domain_score_assembler.py; wave1_liver_flat_v1.yaml | orphan flat card drift |
| Kidney function (domain) | RESEARCH_PRESENT_RUNTIME_READY_AFTER_MINOR_WIRING | Strong | Partial | Partial | Partial | Partial | Partial | Strong | Partial | Strong | Strong | P1-2 report; test_p1_2_kidney_domain_card.py | urea excluded; eGFR bands deferred |
| Blood / iron / oxygen (domain) | RESEARCH_PRESENT_RUNTIME_READY_AFTER_MINOR_WIRING | Strong | Strong | Partial | Blocked | Partial | Partial | Strong | Weak | Strong | Strong | P1-3 report; test_p1_3_blood_iron_oxygen_domain_card.py | empty signal allowlist |
| Thyroid / energy regulation (domain) | SCORING_ARCHITECTURE_BLOCKED | Strong | Partial | Partial | Blocked | Partial | Blocked | Absent | Weak | Partial | Absent | P1-4; P1-6R; ADR-THYROID-SCORING-LAB-RANGE-ARCHITECTURE-1 | launch-core gap #6 |
| Silent inflammation (second-wave) | RESEARCH_PRESENT_UNCOMPILED | Strong | Partial | Weak | Partial | Weak | Partial | Absent | Absent | Partial | Absent | User Health map; pkg_chronic_inflammation | defer past launch-core |
| Hormone balance (second-wave) | RESEARCH_PRESENT_UNMAPPED | Partial | Partial | Weak | Weak | Weak | Blocked | Absent | Absent | Weak | Absent | User Health map; pkg_kb47 testosterone packages | hormonal rail inert |
| wave1_met_insulin_metabolic | COMPILED_NOT_PROMOTED | Strong | Strong | Partial | Partial | Partial | Strong | Strong | Weak | Partial | Partial | health_system_card_evidence.py:40-51 | MED-REV-1 hidden |
| wave1_cv_homocysteine_pathway | COMPILED_NOT_PROMOTED | Strong | Strong | Partial | Partial | Partial | Strong | Strong | Partial | Partial | Partial | estate_index; pathway_explainers_v1 | one pathway explainer exists |
| wave1_cv_vascular_strain | COMPILED_NOT_PROMOTED | Strong | Strong | Partial | Partial | Partial | Strong | Strong | Weak | Partial | Partial | estate_index; health_system_card_evidence.py | hidden |
| wave1_liv_enzyme_pattern | COMPILED_NOT_PROMOTED | Strong | Strong | Partial | Partial | Partial | Strong | Strong | Weak | Partial | Partial | estate_index | hidden |
| wave1_liv_processing_context | COMPILED_NOT_PROMOTED | Strong | Strong | Partial | Partial | Partial | Strong | Strong | Weak | Partial | Partial | estate_index | hidden |
| wave1_liver_flat_v1 (orphan) | UNKNOWN_INSUFFICIENT_EVIDENCE | Unknown | Unknown | Unknown | Absent | Unknown | N/A | Partial | Unknown | Absent | Absent | compiled card on disk; absent from estate_index | estate drift |
| signal_vitamin_d_low (hypothesis) | READY_FOR_COMPILED_CARD_ONLY | Partial | Partial | Weak | Strong | Partial | N/A | Strong | Weak | Partial | Partial | estate_index:46-52 | compiled hypothesis only |

Full machine-readable matrix: `docs/sprints/beta_readiness/P1-7_research_to_runtime_readiness_matrix.yaml`

## 6. Ready or near-ready candidates

### READY_FOR_RUNTIME_CARD

**Cardiovascular health** and **blood sugar control** — domain rows, compiled subsystems, scoring rails (metabolic/cardiovascular), subsystem tests, and assembler integration confirmed. Minor gaps: two CV and one metabolic subsystem remain MED-REV-1 hidden; dedicated pathway explainers partial (homocysteine only).

**Safe next shape:** P2 prose substrate sprint for depth; separate medical-review sprint for hidden subsystem promotion — not new domain-card implementation.

### RESEARCH_PRESENT_RUNTIME_READY_AFTER_MINOR_WIRING

**Kidney function** — P1-2 complete. Gaps: urea frame adjudication, eGFR scoring bands (deferred), ACR package absent. Safe next shape: governance sprint for urea visibility; scoring extension only after lab-range engine pattern if eGFR bands avoided.

**Blood / iron / oxygen** — P1-3 complete. Gaps: empty `active_signal_ids`, iron/ferritin scoring bands absent, TIBC/UIBC absent. Safe next shape: CBC/iron frame adjudication sprint before signal activation.

**Liver health** — domain row exists; compiled subsystems wired but both hidden. Gaps: orphan `wave1_liver_flat_v1.yaml`, no liver pathway explainer. Safe next shape: estate hygiene for orphan; P2 liver prose; promotion review for hidden subsystems.

## 7. Blocked candidates

### Governance conflict

- **Thyroid / energy regulation** — partially reconciled (P1-5 FT3 low); TSH kb52c and kb59 antibodies remain inactive (`P1-5`, `ADR-THYROID-FT3-AUTHORITY-RECONCILIATION-1`).

### Scoring architecture blocked

- **Thyroid / energy regulation** — hormonal rail inert; six-band requirement blocks bandless lab-range policy (`P1-6R`, `rules.py:131-145`, `scoring_policy_registry.py:71-78`).
- **Hormone balance (second-wave)** — same inert hormonal rail; no domain mapping.

### Signal authority blocked

- **Blood / iron / oxygen** — launch-visible CBC/iron signals blocked pending frame adjudication (`P1-3`: empty allowlist).
- **Thyroid** — TSH not launch-active; FT3 low deferred.

### Medical review required

- **Five hidden compiled subsystems** — `WAVE1_MED_REV1_HIDDEN_SUBSYSTEM_IDS` in `health_system_card_evidence.py:49-51`.

### Root-cause / WHY thin

- Second-wave domains and several hidden subsystems lack mapped root-cause promotion to consumer-facing WHY surfaces (inferred from P1-1 partial ratings).

### Prose / explainer thin

- Liver, blood/iron/oxygen, thyroid, silent inflammation, hormone balance — pathway explainers sparse (`pathway_explainers_v1.yaml` has two pathways only: homocysteine, lipid transport).

### Test estate thin

- Unimplemented domains (thyroid, silent inflammation, hormone balance) lack domain-card assembly tests (contrast `test_p1_2_*`, `test_p1_3_*`).

### Unknown / insufficient evidence

- **wave1_liver_flat_v1** — compiled file on disk but excluded from `estate_index_v1.yaml` and `WAVE1_COMPILED_SUBSYSTEM_IDS`.

## 8. Research-to-runtime promotion gaps

| Promotion surface | Gap pattern | Example |
|---|---|---|
| Runtime packages → signal intelligence | kb52c TSH, kb59 antibodies exist but not launch-loaded | P1-5 package estate table |
| Signal intelligence → compiled card evidence | Thyroid, inflammation, hormone balance have packages but no estate_index card | estate_index_v1.yaml (9 cards, no thyroid/inflammation/hormone) |
| Compiled cards → domain assembler | Thyroid domain row absent | domain_score_assembler.py (5 domains only) |
| Compiled cards → user visibility | 5 subsystems compiled but MED-REV-1 hidden | health_system_card_evidence.py:49-51 |
| Research → scoring rails | Hormonal rail empty; iron markers lack bands; eGFR bands deferred | scoring_policy.yaml |
| Research → prose/explainer | Two pathway explainers for entire estate | pathway_explainers_v1.yaml |
| Governance registers → consistent authority | Thyroid pattern resolved for FT3 low; TSH still split | P1-5, P1-6R |
| Tests → replay/audit surfaces | New domains add replay contract entries; unimplemented domains lack tests | persisted_replay_contract_v1.py (P1-2/P1-3 pattern) |

## 9. Specific thyroid lesson

Thyroid exposed a **recurring estate maturity pattern**:

1. **Register drift** — FT3 low contradicted across governance files (P1-4/P1-5); fixed conservatively but TSH/kb59 drift remains.
2. **Inert scoring rail** — hormonal system `system_weight: 0.0`, empty biomarkers (`scoring_policy.yaml:31-34`).
3. **Inactive primary marker authority** — TSH packages exist but kb52c not launch-loaded.
4. **Scoring architecture band requirement** — lab-range primitive cannot reach system orchestration without hardcoded bands (P1-6R).
5. **Research ≠ runtime** — 13+ thyroid KB packages and kb47 runtime-active FT3/FT4 signals did not justify a domain card without scoring rail + TSH + compiled evidence.

**Recurrence risk:** Any domain with rich packages but missing compiled card + scoring membership + signal promotion + prose substrate will hit the same STOP pattern. Silent inflammation and hormone balance are current candidates if sequenced prematurely.

## 10. Recommended programme sequencing

Outcome-based packages (3–6 sprints):

1. **P1-SCORING-LAB-RANGE-ENGINE** (BEHAVIOUR/HIGH) — governed bandless biomarker pattern in scoring engine; prerequisite for hormonal/thyroid policy without hardcoded bands.
2. **P1-SCORING-HORMONAL-POLICY + TSH-PROMOTION** (MIXED/HIGH) — populate hormonal rail under new pattern; resolve kb52c TSH launch authority; FT3 low remains deferred.
3. **P1-4 retry — Thyroid domain card** (MIXED/HIGH) — only after 1–2; compiled card + assembler wiring with STOP gates from P1-4/P1-6R.
4. **P2-PROSE-SUBSTRATE-WAVE1** (CONTENT/MIXED) — kidney, blood/iron, liver pathway/retail depth; parallel-safe after launch-core scoring path clear.
5. **P1-FRAME-ADJUDICATION-CBC-IRON-UREA** (MIXED/STANDARD) — unblock signal allowlists for P1-2/P1-3 depth without improvising clinical activation.
6. **P2-ESTATE-HYGIENE-HIDDEN-SUBSYSTEMS** (CONTENT) — MED-REV-1 promotion decisions + orphan `wave1_liver_flat_v1` reconciliation.

Second-wave domains (silent inflammation, hormone balance) remain **after** launch-core six closure.

## 11. Immediate next sprint recommendation

### P1-SCORING-LAB-RANGE-ENGINE

| Field | Value |
|---|---|
| Title | Lab-range-only biomarker scoring rule pattern |
| risk_level | HIGH |
| change_type | BEHAVIOUR |
| Expected scope | `backend/core/scoring/rules.py`, `scoring_policy_registry.py` schema extension, targeted tests; optional scoring_policy pattern definition (no thyroid bands) |
| STOP gates | No hardcoded thyroid/global ranges; no domain card; no signal activation; no FT3 low activation; determinism preserved |
| Why next | P1-6R ADR blocks all hormonal/thyroid scoring-policy work; thyroid is launch-core domain #6; without engine change the programme cannot close Block 1 launch-core gap |

## 12. Carry-forwards by beta-readiness block

### Block 1 Core health systems model

- Thyroid domain unimplemented (launch-core gap).
- Second-wave silent inflammation and hormone balance unmapped.
- Hormonal scoring rail inert.

### Block 2 Subsystems and depth model

- Five compiled subsystems MED-REV-1 hidden.
- Orphan `wave1_liver_flat_v1` estate drift.

### Block 3 Layer B intelligence/prose substrate

- Pathway explainers thin (2 pathways).
- Kidney, blood/iron, liver retail/prose depth carry-forwards from P1-2/P1-3.

### Block 6 Medical safety, research provenance and governance

- TSH/kb59 launch authority unresolved.
- Frame adjudication backlog for CBC/iron/urea signals.
- Hidden subsystem promotion requires medical review.

### Block 7 Auditability, reproducibility and traceability

- Replay contract updated for P1-2/P1-3; thyroid absent.
- Readiness matrix is planning-only (not runtime SSOT).

### Block 5 UX/results page

- Fifth consumer domain row live (blood/iron); thyroid row absent — UX cannot show complete launch-core six until P1-4 retry.
