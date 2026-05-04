# KB-S53 Preflight — AB/VR Panel Formalisation + Acceptance Harness

**work_id (strategy lineage):** KB-S53 — AB/VR formalisation (Wave 3, adopted v1.5)  
**Preflight type:** READ_ONLY investigation  
**Date:** 2026-04-04  
**Evidence basis:** repository files as cited below  

---

## Important disambiguation: two different “KB-S53” artefacts

The adopted roadmap uses **KB-S53** for **AB/VR panel formalisation + acceptance harness** (`docs/HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan_v1.5_FINAL_ADOPTED.md` §Wave 3).

A **separate** markdown audit in the repo also uses the filename/id pattern **KB-S53**:

- `knowledge_bus/research/KB-S53_WAVE_C_CLASSIFICATION_AUDIT.md` — **Wave C ingestion classification audit** (46 specs, blocker taxonomy, tranche proposal). This is **not** the same sprint as AB/VR formalisation; it is a **work_id / naming collision** in the documentation set.

**This preflight addresses only the strategic KB-S53 = AB/VR formalisation** (v1.5). When authoring the execution sprint, prompt authors should use an explicit `work_id` (e.g. `KB-S53-ABVR-HARNESS`) or cross-reference both docs to avoid merging scopes.

---

## 1. Executive summary

### Current AB/VR maturity

- **Fixtures exist and are substantial:** AB and VR are represented by multiple JSON panel fixtures under `backend/tests/fixtures/panels/`. The **effective authority for “full panel with lab ranges”** is **`ab_full_panel_with_ranges.json`** and **`vr_full_panel_with_ranges.json`** (~16 KB each — rich biomarker payloads).
- **Parallel “minimal” fixtures** exist: `ab_full_panel.json` and `vr_full_panel.json` (~2 KB each) — same naming family but **not** the ones wired into clinician alignment or several AB/VR-specific tests.
- **Third AB variant:** `ab_full_panel_with_profiles.json` is used in at least one golden-runner unit test (lab-reference profile behaviour), not as the primary clinician/AB-VR harness path.
- **Default golden runner path is not AB/VR:** `tools/run_golden_panel.py` defaults to **`backend/tests/fixtures/golden_panel_160.json`**. The **deterministic gate** (`backend/scripts/verify_three_layer_pipeline.py`) uses that same default. So **production-ish regression is anchored on `golden_panel_160`, not AB/VR**.
- **Targeted tests already treat AB/VR-with-ranges as anchors** for clinician report contract, determinism, interaction-chain smoke checks, and some root-cause/homocysteine behaviour — i.e. **de facto partial acceptance harness**, but **without** a single named “panel profile registry” or gate integration.

### What is missing for formalisation

- **Named, versioned panel profiles** in code or a single manifest (no `panel_profiles.yaml` or equivalent was found).
- **Authoritative declaration** of which file is *the* AB acceptance input vs VR vs legacy golden — today this is **implicit** from test imports and docs.
- **Gate / CI ownership:** `golden_gate_local.py` does **not** run AB/VR; it runs baseline pytest + three-layer verify on **`golden_panel_160`**. AB/VR truth is **not** first-class in the control-plane gate.
- **Acceptance criteria** for “what AB/VR must prove” are **scattered** (per-test assertions, static JSON expected outputs for VR clinician report, gap reports) rather than one harness spec.
- **Documentation drift risk:** older audits (e.g. `docs/AUDIT_SPRINT_PLAN_2026-03-20.md`) state there is **no formal AB/VR distinction** — that is **no longer fully true** for tests that pin `*_with_ranges.json`, but it remains **true** for global gate and default runner.

### Is KB-S53 cleanly ready to author?

**Yes, with a tight scope boundary.** The repo already has the raw materials (fixtures + tests + expected clinician JSON for VR). The sprint is **primarily structural/documentation + harness wiring**, not inventing new biology. **Avoid** folding in KB-S54 (cluster/scoring coherence), Wave C ingestion (the other KB-S53-named audit), or narrative/LLM work.

---

## 2. Strategy definition (adopted v1.5)

**Source:** `docs/HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan_v1.5_FINAL_ADOPTED.md`

| Extract | Location / wording |
|--------|----------------------|
| **Principle** | §7.6: “AB and VR are the minimum commercial harnesses.” They are **not** the strategic ontology or commercial boundary. |
| **Wave 3 outcome** | After Wave 3, the application should “**treat AB/VR as real acceptance harnesses**” (§Wave 3 — What this wave improves). |
| **KB-S53 purpose** | “**Formalise AB and VR as explicit acceptance truth** rather than relying only on informal fixture meaning.” Strategic note: AB/VR remain the floor; **wider live coverage** must also be acknowledged. |
| **Relation to structural truth** | Same wave positions KB-S53 **before** KB-S54 (cluster runtime + system-level scoring completion). AB/VR formalisation is **acceptance truth / regression anchors**; KB-S54 is **coherence of runtime scoring output** (separate preflight already referenced in v1.5 for `cluster_engine_v2.py`, `system_burden_engine.py`, `scoring_policy_registry.py`). |

**v1.4 amended** (`docs/HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan_v1.4_amended.md`) adds: KB-S53 **unlocks** “**honest coverage accounting and panel-specific regression truth**” and is typed as **backend / MIXED / risk to be confirmed at prompt stage**.

**Product/platform capability KB-S53 is supposed to unlock**

- **Explicit, auditable** definition of what “AB panel” and “VR panel” mean **in the codebase** (fixtures + optional metadata).
- **Regression and acceptance** that can be cited in governance: “release X was verified against AB and VR profiles,” not only against `golden_panel_160`.
- **Coverage accounting** that is **honest** about what AB/VR exercise vs what the wider SSOT/signal estate covers (aligned with §7.6 floor-not-destination).

---

## 3. Current authoritative fixture inventory

### AB

| Path | Role |
|------|------|
| `backend/tests/fixtures/panels/ab_full_panel_with_ranges.json` | **Primary authority** for clinician runtime tests, AB/VR golden-runner parametrized tests, homocysteine/root-cause tests, interaction gap report inputs. |
| `backend/tests/fixtures/panels/ab_full_panel_with_profiles.json` | Used for **lab reference profile** golden-runner coverage (`test_golden_panel_runner.py` references this path). |
| `backend/tests/fixtures/panels/ab_full_panel.json` | **Minimal / legacy-shaped** fixture per `backend/tests/fixtures/panels/README.md` naming convention; **not** the clinician/AB-VR test anchor. |
| `backend/tests/fixtures/panels/ab_full_panel_with_ranges_notes.md` | Human notes for the ranges fixture. |
| `backend/tests/fixtures/panels/ab_full_panel_parsing_notes.md` | Parsing provenance notes. |

### VR

| Path | Role |
|------|------|
| `backend/tests/fixtures/panels/vr_full_panel_with_ranges.json` | **Primary authority** alongside AB-with-ranges for the same test and report classes. |
| `backend/tests/fixtures/panels/vr_full_panel.json` | **Minimal** sibling; not the primary test anchor. |
| `backend/tests/fixtures/panels/vr_full_panel_with_ranges_notes.md` | Notes. |
| `backend/tests/fixtures/panels/vr_full_panel_parsing_notes.md` | Notes. |

### Competing authority?

- **For “acceptance-style” tests today:** **`*_with_ranges.json` wins** (explicitly wired in `test_clinician_report_runtime_alignment.py`, parametrized tests in `test_golden_panel_runner.py`, `test_root_cause_v1_homocysteine.py`, and cited in `knowledge_bus/interaction_maps/AB_VR_chain_gap_report.md`).
- **For default harness / gate:** **`golden_panel_160.json` wins** (`run_golden_panel._default_fixture_path`, `verify_three_layer_pipeline`).

### Clinician report expected outputs

| Path | Role |
|------|------|
| `backend/tests/fixtures/reports/clinician_report_v1_ab.json` | Expected **header fields** compared for AB determinism test (subset equality). |
| `backend/tests/fixtures/reports/clinician_report_v1_vr.json` | **Full expected** compiled clinician report for VR (strict equality in test). |

---

## 4. Current usage map

### Authoritative / high-signal usages

| Surface | AB/VR usage | Notes |
|---------|-------------|--------|
| `backend/tools/run_golden_panel.py` | **Indirect** | Accepts any fixture path; **default** is `golden_panel_160.json`, not AB/VR. |
| `backend/scripts/verify_three_layer_pipeline.py` | **No AB/VR** | Uses `_default_fixture_path()` → `golden_panel_160.json`. |
| `backend/scripts/golden_gate_local.py` | **No AB/VR** | Invokes baseline tests + `verify_three_layer_pipeline.py` only. |
| `backend/tests/unit/test_clinician_report_runtime_alignment.py` | **AB + VR with_ranges** | `compile_clinician_report_v1` + DTO exposure; VR **full JSON** golden comparison. |
| `backend/tests/unit/test_golden_panel_runner.py` | **AB + VR with_ranges** | `report_v1` determinism; interaction chains / homocysteine / confidence floor parametrized on both panels. |
| `backend/tests/unit/test_root_cause_v1_homocysteine.py` | **AB + VR with_ranges** (+ `golden_panel_160` in places) | Confirmatory suppression and determinism tied to AB panel path. |
| `knowledge_bus/interaction_maps/AB_VR_chain_gap_report.md` | **AB + VR with_ranges** | Historical gap report methodology (run golden panel, inspect signals/chains). |

### Incidental / historical

| Surface | Notes |
|---------|--------|
| `backend/scripts/validate_ab_panel_ssot.py` | **AB SSOT staging** validation; staging dir **removed** post–Sprint 18 (`docs/sprints/sprint18/ab_panel_migration_log.md`). Script now **fails** when staging absent — **not** a live AB panel profile registry for acceptance. |
| `docs/sprints/sprint18/*` | Migration and audit history for AB **SSOT** expansion, not VR. |
| `docs/AUDIT_SPRINT_PLAN_2026-03-20.md` | States lack of formal AB/VR harness — **partially outdated** relative to current tests but **still true** for gate/default runner. |
| `docs/architecture/Intervention_Registry_Investigation_Memo.md` | Notes no single AB/VR panel manifest — **still accurate**. |
| `docs/investigations/PRODUCT_REALITY_AND_DIRECTION_AUDIT.md` | References golden runner paths; defers duplicate AB/VR dumps. |

### Verdict: de facto vs formal

- **De facto:** AB/VR-with-ranges **are** acceptance anchors for **clinician report** and **selected insight-graph / interaction-chain** regressions.
- **Fragmented:** **Global** release gate and **default** golden run **do not** encode AB/VR as mandatory profiles.
- **Informal meaning:** “AB” and “VR” are **filename conventions** and **test wiring**, not a declared **panel profile contract** in one place.

---

## 5. Formalisation gap assessment

To count as **explicit acceptance objects**, the following gaps should be closed (conceptually — implementation is for the execution sprint, not this preflight):

1. **Single source of truth for panel identity**  
   - e.g. manifest: panel id → fixture path → version/hash → intended clinical intent (one paragraph).  
   - Eliminates ambiguity between `ab_full_panel.json` vs `ab_full_panel_with_ranges.json`.

2. **Named acceptance criteria per profile**  
   - What must **always** be true after a run (artifacts present, contract versions, minimum signal/interaction assertions, clinician report invariants).  
   - Today criteria are **test-local**; some are **strict** (VR full JSON), some **partial** (AB header-only comparison in one test).

3. **Harness ownership**  
   - Decide whether **verify_three_layer_pipeline**, **golden_gate_local**, or a **new** thin script owns “AB/VR acceptance run” (or whether AB/VR are **additional** gate checks alongside `golden_panel_160`).

4. **Documentation**  
   - One doc under `docs/` that states what AB and VR **prove** (and explicitly what they **do not** prove vs `golden_panel_160` and vs full SSOT).

5. **Expected outputs**  
   - VR already has **full** expected clinician JSON. AB uses **partial** header matching — formalisation may **either** document that as intentional **or** align AB to a full expected artefact (bounded change — **not** assumed in this preflight).

6. **Looseness / implicit behaviour**  
   - Default runner + gate **implicitly** define “product truth” as **160-marker golden**, which can **diverge** from AB/VR truth. Formalisation should **make that relationship explicit** (floor vs extended coverage).

---

## 6. Product truth / output relevance (AB/VR vs domains)

Evidence is **from existing fixtures + tests + gap report**, not from re-running pipelines here.

| Domain | AB/VR strength (as harness) | Gaps / caveats |
|--------|---------------------------|----------------|
| **Homocysteine / vascular / inflammation context** | **Strong** | `test_golden_panel_runner.py` asserts homocysteine interaction chains and signal presence on **both** panels; `AB_VR_chain_gap_report.md` centres homocysteine and inflammation signals for AB. |
| **Lipid / vascular (broad)** | **Moderate** | Panels are large with ranges; **explicit** lipid-centric acceptance assertions are **not** centralised in one “AB lipid contract” — coverage is **implicit** in full-panel signal fire. |
| **Iron / oxygen** | **Moderate / indirect** | Gap report discusses connectors (e.g. ferritin/hemoglobin) for **MCV** chains on AB; not a dedicated iron-panel acceptance spec. |
| **Hepatic / thyroid WHY** | **Weak as dedicated acceptance** | KB-S52/S52B completion work expanded **Knowledge Bus** hypotheses; AB/VR fixtures **were not** re-authored in this preflight’s evidence set as “hepatic/thyroid acceptance panels.” Formal KB-S53 sprint should **not** claim AB/VR **fully** validate latest WHY domains **unless** assertions are added. |
| **Recently added WHY domains** | **Do not assume** | Without explicit test additions, AB/VR remain **general** full-panel stress tests, not **domain-complete** WHY harnesses. |

**Conclusion:** AB/VR are **strong** for **cross-cutting** deterministic regression (clinician contract, insight graph slices, homocysteine/interaction smoke). They are **incomplete** as **domain-complete** proof for every recent WHY wave unless the sprint **adds** scoped assertions or secondary fixtures.

---

## 7. Structural integrity check (can KB-S53 run without Intelligence Core edits?)

**Yes — if scoped as formalisation + harness + documentation only.**

Potential execution surfaces (typical, not prescriptive):

- `docs/investigations/` or `docs/` — panel profile specification  
- `backend/tests/fixtures/panels/` — README or manifest (metadata only)  
- `backend/scripts/` — optional thin runner or gate hook  
- `backend/tests/` — consolidate or add **declarative** acceptance tests that **only** call existing `run_golden_panel` + existing contracts  

**No prerequisite** to change **SSOT**, **signal packages**, **root_cause_compiler**, **scoring/arbitration**, or **interaction_map** **if** the sprint **does not** claim to “fix coverage gaps” inside those systems.

### Bounded prerequisite (if any)

**FORMALISATION_PLUS_BOUNDED_PREREQUISITE** applies if the sprint author chooses to:

- Add **new** assertions that **fail** on current outputs → may **force** fixes in analytics/pipeline (that would **exit** pure formalisation and become **MIXED/HIGH** per touched files).  
- Align AB expected clinician JSON to **full** parity with VR → may require **tolerating** or **updating** golden files (still **content/test**, not necessarily IC).

**KB-S54** (cluster/scoring coherence) is **explicitly separate** in v1.5; do not merge into KB-S53 unless preflight for KB-S54 identifies a **named** dependency.

---

## 8. Sequencing recommendation

| Option | When |
|--------|------|
| **Documentation + harness formalisation only** | Define profiles, document criteria, wire gate or script to **run existing** tests/fixtures **without** changing pass/fail semantics beyond **centralisation**. |
| **Formalisation + bounded fixture/test implementation** | Add manifest, optional AB full clinician golden parity, optional extra parametrized gate step — **still** avoid SSOT/compiler edits unless a **named** failing assertion requires it. |

**Recommendation:** Author KB-S53 as **FORMALISATION_PLUS_BOUNDED_PREREQUISITE** with **prerequisite = “none” for Intelligence Core”** unless preflight at sprint time finds a **specific** failing invariant. The **bounded** work is **harness + docs + optional gate extension**, not Wave C ingestion (see disambiguation above).

---

## 9. Acceptance-harness recommendation (what KB-S53 should deliver)

1. **Panel profile manifest** (ids, paths, version, intended use: acceptance vs lab-profile vs legacy minimal).  
2. **Single governance doc** linking manifest → gate → default runner policy (e.g. “gate runs golden_160 + AB + VR” or explicit rationale if not).  
3. **Consolidated acceptance criteria** table: profile → artefacts → assertions → owning test module.  
4. **Rename or archive** ambiguity: document when to use `ab_full_panel.json` vs `*_with_ranges.json`.  
5. **Explicit statement** in sprint output that AB/VR are **floor harnesses**, not full product ontology (per §7.6).  
6. **Cross-link** to `KB-S53_WAVE_C_CLASSIFICATION_AUDIT.md` only if ingestion scope is **explicitly** in scope — otherwise **avoid** scope merge (different meaning of KB-S53).

---

## 10. Structural recommendation (sprint shape)

| Label | Verdict |
|-------|---------|
| **PURE_FORMALISATION** | **Insufficient alone** if “acceptance harness” means **operational** verification (gate/CI). Documentation-only without wiring leaves **gate** still on `golden_panel_160` only. |
| **FORMALISATION_PLUS_BOUNDED_PREREQUISITE** | **Recommended.** **Bounded** = manifest + docs + optional script/gate extension + test consolidation; **prerequisite** = *none* for SSOT/signals/compiler **unless** a deliberate assertion addition exposes a defect (then split a follow-on HIGH sprint). |

---

## 11. Mandatory sources consulted (non-exhaustive index)

- `docs/HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan_v1.5_FINAL_ADOPTED.md` (§7.6, Wave 3, KB-S53, KB-S54 note)  
- `docs/HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan_v1.4_amended.md` (KB-S53 unlock statement)  
- `backend/tools/run_golden_panel.py` (`_default_fixture_path`)  
- `backend/scripts/verify_three_layer_pipeline.py`  
- `backend/scripts/golden_gate_local.py`  
- `backend/tests/unit/test_clinician_report_runtime_alignment.py`  
- `backend/tests/unit/test_golden_panel_runner.py` (AB/VR parametrized tests)  
- `backend/tests/unit/test_root_cause_v1_homocysteine.py`  
- `backend/tests/fixtures/panels/*` (AB/VR JSON + notes)  
- `backend/tests/fixtures/reports/clinician_report_v1_ab.json`, `clinician_report_v1_vr.json`  
- `knowledge_bus/interaction_maps/AB_VR_chain_gap_report.md`  
- `knowledge_bus/research/KB-S53_WAVE_C_CLASSIFICATION_AUDIT.md` (disambiguation only)  
- `docs/AUDIT_SPRINT_PLAN_2026-03-20.md`, `docs/sprints/sprint18/*`, `backend/scripts/validate_ab_panel_ssot.py`  

---

## 12. Output checklist (this document)

- [x] Executive summary  
- [x] Authoritative fixture inventory  
- [x] Usage map  
- [x] Formalisation gap  
- [x] Acceptance-harness recommendation  
- [x] Structural recommendation (sprint shape)  

---

## 13. Post-implementation authority (KB-S53-ABVR-HARNESS)

After sprint `KB-S53-ABVR-HARNESS`, governed acceptance authority lives in:

- `backend/tests/fixtures/panels/panel_acceptance_profiles_v1.yaml`
- `docs/investigations/KB-S53_AB_VR_ACCEPTANCE_HARNESS.md`
- `backend/scripts/run_ab_vr_acceptance_harness.py`
