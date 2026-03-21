# HealthIQ AI v5 — Audit Report & Sprint Planning Brief
**Audit date:** 2026-03-20 | **Auditor:** Claude Code (Sonnet 4.6) | **Basis:** Live codebase read

> **Sprint ID superseded (2026-03-21):** The specific sprint IDs proposed in Section 4 of this document (KB-S45 through KB-S49 as pure WHY sprints) have been superseded by the agreed 12-month strategic plan (`docs/HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan.md`), which interleaves ingestion and WHY sprints under the same ID range. The **gap analysis, blocker identification, capability matrix, and earliest honest claim criteria in this document remain valid** and were used as inputs to the 12-month plan. Only the specific sprint numbering is superseded.

---

# 1. Executive Verdict

**The codebase is structurally further along than it probably feels, but it is not at the target state.**

The three-layer pipeline is real and deterministically verified. Signal evaluation is fully wired with 51 signals. Interaction chains exist and are wired. The clinician report contract (KB-S44a) and frontend renderer (FE-S1) are complete. These are genuine, not scaffolding.

**But the product claim — "full AB & VR panel with root cause WHY and plain-English narrative" — cannot yet be made honestly.** The reason is specific:

> Root cause reasoning covers **4 signals out of 51**. The other 47 signals produce signal state and confidence — but no WHY. They fire and stop.

Additionally, the LLM narrative layer is conditionally wired but explicitly **disabled** (`HEALTHIQ_ENABLE_LLM=0`) in the golden runner. It is not production-ready as tested.

The codebase is not early-stage. It is **mid-completion**: the engine architecture is sound, the contracts are real, and the hardest infrastructure problems are solved. What remains is content depth (root cause coverage) and a specific production-enablement step (LLM narrative).

---

# 2. Completed vs Incomplete Capability Matrix

| Capability | Status | Evidence |
|---|---|---|
| Canonical ingestion / normalisation | **COMPLETE** | Layer A wired; SSOT enforced via `validate_canonical_only()` |
| Derived metrics | **COMPLETE** | `ratio_registry.py`, BMI, HOMA-IR, waist-to-height, TyG index etc. all computed |
| Cluster scoring | **IMPLEMENTED BUT NOT WIRED** | `ClusterEngineV2` exists; sprint comment: "not wired to runtime" |
| InsightGraph production | **COMPLETE** | 262-field contract, fully populated in runtime |
| Root cause reasoning | **PARTIAL** | `root_cause_compiler_v1.py` wired — covers **4 signals only** (homocysteine, HbA1c, ALT, TSH) |
| Clinician report runtime contract | **COMPLETE** | `compile_clinician_report_v1()` wired in DTO layer (KB-S44a) |
| Clinician report frontend rendering | **COMPLETE** | `ClinicianReportRenderer.tsx` with null guard (FE-S1) |
| Signal libraries | **COMPLETE** | 51 signals across 46 packages, SHA-versioned, deterministically loaded |
| Runtime signal evaluator | **COMPLETE** | `signal_evaluator.py` 377 lines, fully wired in orchestrator |
| Signal results in runtime output | **COMPLETE** | Signal results in InsightGraphV1 + ReportV1 |
| Signal confidence | **COMPLETE** | Confidence model per-signal, stamped in InsightGraph |
| Interaction chains / pathway reasoning | **COMPLETE** | `signal_interaction_builder.py` wired; 23 edges, 3 pathway clusters |
| Intervention evidence layer | **COMPLETE** | `intervention_selector_v1.py` wired; safety-checked, denylist-validated |
| Stable report handoff object | **COMPLETE** | `ReportV1` + `ClinicianReportV1` both structurally complete |
| User-facing narrative layer | **IMPLEMENTED BUT NOT WIRED** | `InsightSynthesizer` exists with Gemini client — explicitly disabled (`HEALTHIQ_ENABLE_LLM=0`) in golden runner |
| AB/VR full-panel acceptance coverage | **NOT IMPLEMENTED** | No formal AB/VR panel distinction in codebase; no panel-specific config or acceptance test by panel type |

---

# 3. Current Blockers

Ordered by criticality to the product claim.

## Blocker 1 — Root cause coverage: 4/51 signals (8%)

This is the primary structural gap. The root cause compiler is correctly architected and the 4 implemented signals work properly. But 47 signals return `None` from `compile_root_cause_v1()`. Every one of those signals can fire, produce a state and confidence score, and appear in the clinician report — with zero WHY reasoning behind it.

Until this is substantially expanded, the "full-panel WHY" claim is not honest for the majority of biomarker findings.

The four covered signals (homocysteine, HbA1c, ALT, TSH) are high-value, but they represent a narrow slice of metabolic, inflammatory, hematologic, lipid, renal, and nutritional findings that the 51-signal library can surface.

## Blocker 2 — LLM narrative layer is production-disabled

`InsightSynthesizer` is wired and Gemini is configured, but `HEALTHIQ_ENABLE_LLM=0` in the golden runner means the narrative layer is never exercised in any verified production path. The plain-English user narrative — a stated requirement — does not run in any tested path. Before the claim can be made, the LLM layer must be production-enabled, hardened with a structured input contract, and tested with representative InsightGraph output.

## Blocker 3 — Clustering not wired to runtime

`ClusterEngineV2` exists but the sprint comment says "not wired to runtime." Cluster scoring is architecturally upstream of health system scores, burden vector calculation, and system-level interpretation. This affects the richness of the structured output that feeds the LLM narrative and the clinician report.

## Blocker 4 — No formal AB / VR panel distinction

The brief defines the target as "full AB and VR panel coverage." The codebase currently has no concept of AB vs VR panels — no separate configs, no acceptance tests by panel type, no formal definition of what biomarkers constitute each. The golden fixture has 124 biomarkers but is simply named `golden_panel_160`. Before the target claim can be validated, AB and VR must be defined as specific panel profiles with acceptance tests.

## Blocker 5 — Root cause expansion requires KB content authoring

Even after the root cause compiler architecture is extended, each new signal's WHY reasoning requires authored hypotheses: evidence rules, hypothesis confidence models, confirmatory test mappings. This is KB content work, not just code. The rate at which new signals gain WHY coverage is gated by KB authoring throughput.

## Blocker 5a — Renal pathway has a hard sequencing prerequisite

The renal pathway is the only one of the seven agreed pathways with **zero active interaction map edges**. `phenotype_map_v1.yaml` documents that `signal_creatinine_high → signal_urea_high` requires research promotion before the edge can be added to `interaction_map_v1.yaml`. Renal hypothesis authoring cannot begin until that research promotion step completes. This makes KB-S49 structurally dependent on a governance step that must be initiated before the sprint is planned — not as part of it.

---

# 4. Proposed Sprint Sequence

All sprints are proposed from **today's actual codebase**. Stale sprint IDs (KB-S13–S16) are not referenced — see Q1 below.

## Phase 1 — Root Cause Coverage Expansion *(Mandatory Before Claim)*

> **Amendment 2026-03-20:** Sprint order revised after metabolic pathway coverage audit. Inflammation moved to KB-S45 (first) because it is the most connected pathway in the interaction map (9 active edges, 3 phenotype fixtures already wired). Lipid moves to KB-S46. Renal is split from hepatic extension into a separate sprint (KB-S49) due to a hard prerequisite: renal interaction map edges require research promotion before hypotheses can be authored. See Blocker 5a below.

### KB-S45 — Root Cause Compiler: Systemic Inflammation Signal WHY Coverage
- **Why needed:** `signal_systemic_inflammation`, `signal_crp_high`, `signal_inflammation_crp_context`, `signal_neutrophils_high`, `signal_wbc_high` — all five signals fire and return no WHY. CRP sits at the centre of the interaction map (9 active edges), acting as driver of homocysteine elevation, connected to hepatic stress, and modulating ferritin/iron signals. Without WHY here, the majority of interaction chain reasoning lacks narrative ground truth.
- **What it unlocks:** WHY reasoning for the most cross-connected pathway in the system. Immediately enriches chain reasoning across metabolic, hepatic, iron, and vascular pathways.
- **Signals targeted:** `signal_crp_high`, `signal_systemic_inflammation`, `signal_inflammation_crp_context`; `signal_neutrophils_high` and `signal_wbc_high` to be scoped within sprint.
- **Mandatory before claim:** YES
- **Risk tier:** HIGH (backend/core/analytics/)
- **Type:** Backend / KB

### KB-S46 — Root Cause Compiler: Lipid & Vascular Signal WHY Coverage
- **Why needed:** `signal_lipid_transport_dysfunction`, `signal_ldl_cholesterol_high`, `signal_hdl_cholesterol_low`, `signal_triglycerides_high` — all four uncovered. 7 active interaction map edges already wired and 2 phenotype fixtures exist (`ph_metabolic_early_ir_v1`, `ph_thyroid_lipid_disturbance_v1`). Lipid findings are the most frequent in AB and VR panels clinically.
- **What it unlocks:** WHY reasoning for the full cardiovascular/lipid domain. Completes the lipid-thyroid and lipid-metabolic interaction chain WHY paths.
- **Mandatory before claim:** YES
- **Risk tier:** HIGH (backend/core/analytics/)
- **Type:** Backend / KB

### KB-S47 — Root Cause Compiler: Iron, Oxygen Transport & Nutritional Signal WHY Coverage
- **Why needed:** `signal_iron_deficiency_context`, `signal_iron_overload_context`, `signal_ferritin_low`, `signal_ferritin_high`, `signal_hemoglobin_low`, `signal_oxygen_transport_capacity` — all six uncovered. 5 active interaction map edges wired. Iron deficiency anemia and macrocytosis patterns are common in both AB and VR panels. Note: the iron overload pattern also has no phenotype fixture — this sprint should author `ph_iron_overload_v1` alongside hypothesis assets.
- **What it unlocks:** WHY reasoning for hematologic and iron transport domains; closes the iron overload phenotype fixture gap.
- **Mandatory before claim:** YES
- **Risk tier:** HIGH (backend/core/analytics/)
- **Type:** Backend / KB

### KB-S48 — Root Cause Compiler: Hepatic Extension Signal WHY Coverage
- **Why needed:** `signal_hepatic_metabolic_stress`, `signal_ggt_high` — uncovered despite `signal_hepatic_alt_context` already having `alt_hypotheses_v1.yaml`. GGT is a significant hepatic stress and metabolic syndrome marker with 7 active interaction edges. ALP and albumin also require WHY coverage. This sprint extends hepatic coverage beyond the existing ALT hypothesis asset.
- **What it unlocks:** WHY reasoning for hepatic stress beyond ALT; completes the hepatic-inflammatory chain WHY path.
- **Mandatory before claim:** YES
- **Risk tier:** HIGH (backend/core/analytics/)
- **Type:** Backend / KB

### KB-S49 — Renal Interaction Map Edge Promotion + Root Cause WHY Coverage
- **Why needed:** Renal metabolic stress is the only pathway with **zero active interaction map edges**. `signal_creatinine_high → signal_urea_high` is documented in `phenotype_map_v1.yaml` as requiring research promotion before the edge can be added to `interaction_map_v1.yaml`. This sprint has a **hard two-step sequencing requirement**: (1) promote renal edges through the research promotion process first, (2) then author renal hypotheses for `signal_creatinine_high`, `signal_urea_high`, `signal_urate_high`, `signal_renal_metabolic_stress`. These cannot be done in a single atomic commit — the edge promotion is a KB governance step that must precede hypothesis authoring.
- **What it unlocks:** First active WHY reasoning for the renal pathway; closes the only pathway with zero interaction map coverage.
- **Mandatory before claim:** YES
- **Risk tier:** HIGH (backend/core/analytics/ + interaction map governance)
- **Type:** Backend / KB
- **Prerequisite:** Research promotion of renal edges must complete before hypothesis sprint can begin.

---

## Phase 2 — LLM Narrative Production-Enablement *(Mandatory Before Claim)*

### BE-S1 — LLM Narrative Layer: Production Enablement & Structured Prompt Contract
- **Why needed:** `InsightSynthesizer` is conditionally wired but explicitly disabled in the golden runner. The LLM narrative is a stated requirement. This sprint enables LLM in the production path, hardens the structured InsightGraph → prompt contract, validates Gemini integration under representative input, and adds a golden narrative acceptance test. **LLM does not gain reasoning authority** — it remains a translation layer over governed InsightGraph output.
- **What it unlocks:** The actual user-facing plain-English explanation of findings.
- **Mandatory before claim:** YES
- **Risk tier:** STANDARD (Layer C boundary, not Layer B analytics)
- **Type:** Backend / Mixed

---

## Phase 3 — Panel Formalisation & Acceptance *(Mandatory Before Claim)*

### BE-S2 — AB & VR Panel Definition and Acceptance Test Harness
- **Why needed:** The codebase cannot make a claim about "full AB and VR panel" coverage if AB and VR are undefined. This sprint formally defines what biomarkers constitute each panel, creates panel-specific fixtures, and creates acceptance tests asserting full-panel signal coverage against each defined profile.
- **What it unlocks:** The ability to make an honest, auditable claim about panel coverage.
- **Mandatory before claim:** YES
- **Risk tier:** STANDARD
- **Type:** Backend / KB

---

## Phase 4 — Cluster Wiring *(Recommended, Non-Blocking)*

### BE-S3 — Wire ClusterEngineV2 to Runtime Pipeline
- **Why needed:** `ClusterEngineV2` exists but is not wired. Cluster scores (metabolic, cardiovascular, hepatic, inflammatory) feed health system scores, burden vectors, and LLM narrative input. Without it, system-level scores are incomplete.
- **What it unlocks:** Proper system-level health scores and richer LLM narrative input.
- **Mandatory before claim:** RECOMMENDED — the claim can technically be made without it, but narrative quality and system-level interpretation are weaker.
- **Risk tier:** HIGH (orchestrator wiring)
- **Type:** Backend

---

## Phase 5 — Follow-up Polish *(Non-Blocking)*

### FE-S2 — User-Facing Narrative Display
- Render the LLM narrative in the frontend results page alongside the clinician report.
- **Risk:** LOW | Frontend | Non-blocking

### KB-S49+ — Additional Signal WHY Coverage
- Continue expanding root cause hypotheses for remaining signal gaps beyond KB-S45–S48 domains.
- **Risk:** HIGH per sprint | Backend/KB | Non-blocking for initial claim

---

# 5. Earliest Honest Claim Point

**The honest claim becomes true after KB-S45 + KB-S46 + KB-S47 + KB-S48 + KB-S49 + BE-S1 + BE-S2 are all complete.**

That is the point at which we can honestly say:

> "AB and VR panels now support full-panel WHY interpretation with a plain-English narrative."

- **KB-S45** brings WHY to the most interaction-connected pathway (systemic inflammation, 9 edges)
- **KB-S46** brings WHY to the lipid/vascular domain (most clinically frequent in real panels)
- **KB-S47** brings WHY to iron, oxygen transport, and hematologic domain; closes iron overload phenotype gap
- **KB-S48** extends hepatic WHY beyond ALT to GGT, ALP, and albumin
- **KB-S49** completes renal WHY — but only after research promotion of renal edges (prerequisite, see Blocker 5a)
- **BE-S1** enables the LLM narrative in the production path
- **BE-S2** defines AB and VR as formal panel profiles and proves coverage with acceptance tests

None of these is optional. The claim is not honest if any one is missing. Note that KB-S49 has a hard prerequisite that must be initiated in parallel with earlier sprints — do not wait until KB-S48 is complete to begin the renal edge research promotion process.

---

# 6. Specific Questions

### Q1. Are KB-S13 to KB-S16 still genuinely outstanding in repo reality?

**No.** There are zero references to KB-S13, KB-S14, KB-S15, or KB-S16 anywhere in the live codebase — no files, no tests, no sprint artifacts, no prompt files. These IDs either predated the current sprint numbering scheme or were superseded entirely.

The work those sprints would have targeted has been delivered under later sprint IDs:
- Signal evaluator → delivered (KB-S2x/S3x era)
- Interaction map → KB-S28
- Precedence engine → KB-S27
- Root cause compiler → KB-S33
- Intervention selector → KB-S31
- Report compiler → KB-S32

Do not plan against these IDs. They are stale.

---

### Q2. Is the signal evaluator still the main missing component?

**No.** The signal evaluator is fully wired and operational (`signal_evaluator.py`, 377 lines, instantiated in `AnalysisOrchestrator.__init__()`). It evaluates all 51 signals deterministically at runtime.

The main missing component is now **root cause coverage**. The evaluator produces signal state and confidence for 51 signals. The root cause compiler then produces WHY reasoning for only 4 of them. The bottleneck has shifted from "does signal evaluation exist?" to "does WHY reasoning exist for the signals that fire?"

---

### Q3. Is current root-cause logic broad enough to support "full AB/VR panel WHY"?

**No.** Coverage gaps by domain:

| Domain | Signals With WHY | Signals Without WHY |
|---|---|---|
| Metabolic/Glycaemic | HbA1c ✓ | Glucose, HOMA-IR, TyG index ✗ |
| Hepatic | ALT ✓ | GGT, ALP, Bilirubin, Albumin ✗ |
| Thyroid | TSH ✓ | Free T3, Free T4 ✗ |
| Cardiovascular/Lipid | — | LDL, HDL, Triglycerides, ApoB, ApoA1, Lipoprotein(a), TC:HDL ✗ |
| Inflammatory | — | CRP, Ferritin (high), IL-6 signals ✗ |
| Hematologic | — | Hemoglobin, MCV, Ferritin (low), RDW, Platelets, WBC patterns ✗ |
| Nutritional | Homocysteine (partial) ✓ | Vitamin D, Folate, B12, Iron, Zinc, Magnesium ✗ |
| Renal | — | Creatinine, Urea, Urate ✗ |
| Hormonal | — | Testosterone, SHBG, Cortisol, DHEA, Oestradiol, FSH, LH ✗ |

Approximately 43 of 51 signals have no WHY reasoning.

---

### Q4. Does the current clinician report path prove the product is close to the goal, or does it only prove the shell/UI path exists?

**It proves the shell/UI path exists.** Be explicit: this is not a criticism of KB-S44a or FE-S1 — both are correctly built and architecturally necessary. But the clinician report contract and the frontend renderer are pass-through layers. They render whatever the backend provides.

When the backend provides WHY for 4 signals, the clinician report contains WHY for 4 signals. The renderer's completeness does not advance WHY coverage. The report shell is not equivalent to biological intelligence — it is a governed delivery channel waiting for biological intelligence to flow through it.

The completion of KB-S44a and FE-S1 proves: **the delivery pipe is built**. The remaining sprints fill the pipe with content.

---

### Q5. What exact sprint marks the first point at which we can honestly say: "AB and VR now support full-panel WHY interpretation with a plain-English narrative"?

**BE-S2** — the panel formalisation and acceptance test sprint — is the final gate.

After BE-S2 completes, all of the following will be true:
1. Root cause WHY exists for all major signal domains (KB-S45–S48)
2. The LLM narrative runs in the production path (BE-S1)
3. AB and VR are formally defined as panel profiles and have acceptance tests proving full-panel coverage (BE-S2)

BE-S2 is the sprint that converts a working system into a proven, auditable claim.

---

# 7. Risks / Traps

**Trap 1 — Confusing the report shell with biological intelligence completion.**
The clinician report frontend renderer and runtime contract are real — but they render whatever the backend provides. Renderer completion does not advance WHY coverage. Do not use FE-S1 / KB-S44a as evidence the product is near-complete.

**Trap 2 — Counting signals as equivalent to WHY coverage.**
51 signals are evaluated. This is genuine signal breadth. But signal state + confidence ≠ WHY. `at_risk: 0.85` tells you *that* something is wrong; only root cause hypotheses tell you *why* and *what it means biologically*. Do not use the signal count as a proxy for product completeness.

**Trap 3 — Believing the LLM narrative is almost there.**
The `InsightSynthesizer` code exists and Gemini is configured, but `HEALTHIQ_ENABLE_LLM=0` in the golden runner means it has never been production-exercised in the current verified pipeline. Production-enabling it requires structured prompt contract hardening, output validation, denylist enforcement, and narrative acceptance testing — not just removing a flag.

**Trap 4 — Planning sprints against KB-S13–S16.**
These sprint IDs do not exist in the live codebase. They are stale. All the work they would have targeted has been delivered under later sprint IDs. See Q1 above.

**Trap 5 — Treating root cause expansion as a single sprint.**
KB-S45–S48 are each individually HIGH risk. Each requires authored hypotheses, target registration, evidence rule implementation, hypothesis confidence modelling, confirmatory test suppression logic, and deterministic test fixtures. Combining all domains into one sprint risks scope explosion and architectural drift.

**Trap 6 — Assuming clustering is a minor gap.**
`ClusterEngineV2` is not wired. Health system scores (metabolic, cardiovascular, etc.) are downstream of clustering. The LLM narrative relies on system-level scoring for meaningful cross-domain narrative. If clustering is not wired when the LLM narrative is enabled, the narrative input will be less rich than designed.

---

# 8. Recommended Next Sprint

**KB-S45 — Root Cause Compiler: Systemic Inflammation Signal WHY Coverage**

> **Amendment 2026-03-20:** Changed from Lipid (original recommendation) to Inflammation, based on the metabolic pathway coverage audit. Rationale below.

Systemic inflammation is the right starting point for three reasons grounded in the pathway audit:

1. **Most connected pathway.** CRP and its associated signals are present in 9 of the 23 active interaction map edges — more than any other pathway. Adding WHY here immediately enriches chain reasoning across metabolic, hepatic, iron, and vascular pathways that are already structurally wired.

2. **Infrastructure is most ready.** 3 phenotype fixtures already exist and reference inflammation signals (`ph_vascular_hcy_inflammation_v1`, `ph_hepatic_alt_inflammatory_v1`, `ph_iron_deficiency_inflammation_v1`). The acceptance test harness for inflammation is more mature than any other uncovered pathway.

3. **Clinically foundational.** CRP elevation is present as a primary or secondary finding in a high proportion of real AB and VR panels. Covering it first maximises the per-sprint impact on real-world WHY coverage.

The root cause compiler architecture is proven at 4 signals. Extending it requires only hypothesis authoring, target registration, and deterministic tests. All downstream components are already wired to consume root cause output.

**Action in parallel:** Begin the research promotion process for renal interaction map edges now, before KB-S45 starts, so KB-S49 is not blocked when Phase 1 otherwise completes.

**Risk tier:** HIGH — requires Claude audit + GPT architectural review + dual approval per SOP §10.
