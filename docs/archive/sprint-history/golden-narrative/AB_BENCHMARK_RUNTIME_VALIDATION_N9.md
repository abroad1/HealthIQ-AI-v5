# AB benchmark runtime validation — N-9

## 1. Purpose

This document validates **actual deterministic runtime output** for the **AB acceptance panel** against the **locked AB gold-standard narrative**, using repo-grounded evidence from a full `AnalysisOrchestrator.run` path (the same stack that attaches `NarrativeReportV1` to `AnalysisDTO`).

**Work ID:** N-9  
**Validation date:** 2026-04-22  
**Constraint:** No compiler, contract, or knowledge-bus code changes were made during this validation sprint—only this report and automation-bus prompt alignment.

---

## 2. Source authorities used

| Authority | Path |
|-----------|------|
| Benchmark narrative (comparison target) | `docs/golden-narrative/AB_GOLD_STANDARD_NARRATIVE_REPORT_CHAT_2_FINAL.md` |
| Target lock | `docs/golden-narrative/AB_GOLD_STANDARD_NARRATIVE_TARGET_LOCK.md` |
| Merged reverse-engineering matrix | `docs/golden-narrative/AB_GOLD_STANDARD_NARRATIVE_REVERSE_ENGINEERING_MERGED.md` |
| Sprint strategy | `docs/golden-narrative/HealthIQ_Deterministic_Narrative_Sprint_Strategy_FINAL.md` |
| Compiler architecture | `docs/golden-narrative/HealthIQ_Deterministic_Narrative_Compiler_Architecture_v1.md` |
| AB acceptance fixture (biomarkers + minimal user) | `backend/tests/fixtures/panels/ab_full_panel_with_ranges.json` |
| Questionnaire template (benchmark context; not injected in run) | `docs/golden-narrative/AB_SPECIFIC_QUESTIONNAIRE_TEMPLATE_v1.json` |
| Narrative compiler | `backend/core/analytics/narrative_report_compiler_v1.py` |
| Narrative contract | `backend/core/contracts/narrative_report_v1.py` |
| Orchestrator integration | `backend/core/pipeline/orchestrator.py` (`compile_narrative_report_v1` → `AnalysisDTO.narrative_report_v1`) |
| DTO field | `backend/core/models/results.py` |
| Golden runner (repro harness) | `backend/tools/run_golden_panel.py` |
| IDL registry (explains retail gating) | `knowledge_bus/interpretation_display_layer_v1/idl_records_v1.yaml` |

---

## 3. Runtime output inspected

### 3.1 How output was obtained

A deterministic golden run was executed from the repo root:

- **Fixture:** `backend/tests/fixtures/panels/ab_full_panel_with_ranges.json` (KB-S53 **ab_acceptance** profile).
- **Harness:** `backend/tools/run_golden_panel.run_golden_panel(...)` with `db_session=_EmptySession()` (standard golden-runner behaviour: **no persisted prior snapshots**).
- **Run ID:** `n9-ab-validation-20260422`
- **Primary artifact:** `backend/artifacts/golden_runs/n9-ab-validation-20260422/analysis_result.json` (full `AnalysisDTO` dump, including `meta.insight_graph`, `interpretation_display_layer_v1`, and `narrative_report_v1`).

**Reproduce (from `backend/`):**

```text
set PYTHONPATH=.
python -c "from pathlib import Path; from tools.run_golden_panel import run_golden_panel; run_golden_panel(fixture_path=Path('tests/fixtures/panels/ab_full_panel_with_ranges.json'), run_id='n9-ab-validation-20260422')"
```

### 3.2 Proof this is the N-8 compiler path

- `run_golden_panel` constructs `AnalysisOrchestrator` and calls `orchestrator.run(...)` (`backend/tools/run_golden_panel.py`, ~L346–L353).
- The orchestrator publishes IDL, then calls `compile_narrative_report_v1(...)` and assigns **`narrative_report_v1`** on the returned DTO (`backend/core/pipeline/orchestrator.py`).
- The captured `analysis_result.json` contains a populated `narrative_report_v1` object with `narrative_report_version: "1.0.0"` and compiler `meta.compiler_version: "1.0.0"`.

### 3.3 Fairness note (benchmark vs harness inputs)

The locked benchmark narrative assumes **rich questionnaire/lifestyle context** and **panel 0 vs current longitudinal framing** (`AB_GOLD_STANDARD_NARRATIVE_REPORT_CHAT_2_FINAL.md`, patient context preamble).

The AB acceptance JSON fixture used here provides **biomarkers + `user.age` / `user.biological_sex` only** (no `questionnaire_data` block). The golden runner uses **`_EmptySession`**, so **`linked_snapshot_ids`** is empty and **no prior-panel snapshot** is linked.

Therefore:

- **Longitudinal narrative** in `NarrativeReportV1` is expected to be **empty** on this harness (no `state_transitions` / no `prior_biomarker_lab_snapshot_v1`), independent of compiler quality.
- **Retail / lifestyle bridging** that depends on questionnaire or bridges may be **under-exercised** relative to the benchmark story.

This validation still stands as **“real stack, AB biomarker truth”**; a second pass with a merged fixture (questionnaire + synthetic prior graph) would be needed for **strict parity** with the benchmark’s *inputs*.

---

## 4. Benchmark comparison table

Mapped benchmark **narrative moves** (from `AB_GOLD_STANDARD_NARRATIVE_REPORT_CHAT_2_FINAL.md`) to **`NarrativeReportV1`** sections and observed runtime.

| Benchmark narrative area | Runtime surface (`NarrativeReportV1` / related) | Runtime output status | Quality judgement | Remaining gap type | Notes |
|---------------------------|-----------------------------------------------|------------------------|-------------------|--------------------|-------|
| Placeholder patient summary / retail framing | `retail_summary` | **Absent** (`""`) | **Materially weaker than benchmark** | **Governed asset / IDL policy + compiler rule** | Compiler only assembles retail copy from IDL rows with `frontend_allowed_term: phenotype_allowed`. Benchmark lead/secondary IDL rows for one-carbon and residual-LDL patterns are **`clinical_only`** in `idl_records_v1.yaml`, so **no retail card qualifies** → `retail_summary_no_enabled_phenotype_cards` in compiler `meta.skipped`. |
| §1 Body overview (multi-paragraph systemic framing) | `body_overview` | **Present but thin** | **Materially weaker than benchmark** | **Compiler assembly gap** | Runtime: single sentence naming `primary_driver_system_id` (here `cardiovascular_4_biomarkers`). Benchmark: long integrated overview (glycaemic, inflammatory, renal, lipid, lead pattern). |
| §2 “What is working well” (multi-system reassurance) | *(no dedicated field)* | **Not represented** | **Absent / still unsupported** | **Compiler assembly gap** | No `NarrativeReportV1` section compiles “working well” narrative; benchmark section has no deterministic counterpart in v1 contract. |
| §3 Lead phenotype — methylation / homocysteine | `lead_narrative` | **Substantial text** | **Partially there** (assets strong; framing differs) | **Wording polish + arbitration/surfacing** | Pathway explainer + functional interpretation + clarification paths present and long-form. Benchmark emphasises *lead* pattern and marker evidence prose; runtime **primary driver** line points at **cluster-style id** `cardiovascular_4_biomarkers`, not the benchmark’s consumer-facing “methylation lead” hierarchy. |
| Secondary lipid transport theme | `secondary_narratives` | **Substantial text** | **Partially there** | **Compiler assembly + governance** | Strong pathway + functional assembly for lipid domain. Benchmark’s tighter “residual LDL in protective context” story is partially mirrored; IDL retail gating still blocks retail layer. |
| Longitudinal direction (panel 0 → current) | `longitudinal_narrative` | **Absent** (`""`) | **Absent in this harness** | **Missing deterministic support (harness)** + **product gap for real users** | Empty with `longitudinal_empty` / no transitions. Golden run: `replay_manifest.linked_snapshot_ids: []`, `state_transition_version` / hash **unset**. With DB-linked priors, compiler can populate; benchmark longitudinal paragraphs are **not** reproduced here. |
| Next steps / follow-up prioritisation | `next_steps_narrative` | **Present** | **Partially there** | **Wording polish + breadth** | Governed `clarification_paths` bullets for lead + secondary domains are emitted under a clear header. Benchmark’s prioritised “homocysteine/RBC pathway first” is **not explicitly ranked** across domains in this v1 assembly. |
| Clinician-facing synthesis | `clinician_synthesis` | **Present, long** | **Partially there** | **Compiler assembly gap + surfacing** | Concatenates multiple IDL clinical excerpts (several strong/watch patterns) plus functional limits/monitoring blocks. Benchmark is a more **linear** clinical story with integrated physiology; runtime output is **stacked modular blocks** (accurate but not the same narrative shape). |
| Lifestyle bridges (alcohol, fasting, weight loss) | `lead_narrative` / `meta` (bridges) | **Not observed in this run** | **Partially there / input-limited** | **Runtime integration / inputs gap** | Fixture lacked lifestyle/questionnaire payload; benchmark context explicitly includes alcohol, fasting, weight loss. |

---

## 5. Strongest wins

1. **Deterministic lead and secondary narrative cores** — `lead_narrative` and `secondary_narratives` successfully compose **N-5 pathway explainers** and **N-6 functional interpretation** text for the AB signal pattern; this is the main technical proof that the governed asset stack + compiler wiring function end-to-end on real biomarker input.
2. **Next-steps bullets** — `next_steps_narrative` delivers **governed, non-LLM clarification paths** suitable for controlled surfacing.
3. **Clinician synthesis depth** — `clinician_synthesis` demonstrates that **IDL + functional tails** can produce a **long, inspectable** clinician-facing block (even if structure ≠ benchmark prose).
4. **Traceability** — `narrative_report_v1.meta` records `assets_resolved` and `skipped`, supporting audit of **why** sections are empty (e.g. retail gating, longitudinal).

---

## 6. Remaining weaknesses (material)

1. **`retail_summary` is empty** for AB benchmark phenotypes because IDL marks those patterns **`clinical_only`**, while the compiler’s retail section only consumes **`phenotype_allowed`** rows. This is a **direct mismatch** with the benchmark’s retail-facing patient summary intent unless policy changes or a separate governed retail channel is introduced.
2. **`body_overview` is a single arbitration line**, not the benchmark’s multi-paragraph overview. This is a **compiler assembly / contract scope** gap, not “polish” alone.
3. **Longitudinal narrative absent** in the golden harness: **no linked priors** → no `state_transitions` / prior lab snapshot. The benchmark’s longitudinal story is **not testable** on this runner without extending the fixture or running with a real `db_session` + user history.
4. **Primary driver presentation** (`cardiovascular_4_biomarkers`) does not match the benchmark’s **narrative lead** (methylation / homocysteine-first). This is a **deterministic arbitration vs consumer narrative** alignment issue for surfacing.
5. **No dedicated “what is working well” section** in `NarrativeReportV1` — benchmark §2 has no deterministic counterpart in v1 output.

---

## 7. Frontend-readiness recommendation

**Choice 2 — Deterministic runtime is materially improved but still needs one bounded refinement sprint before broad frontend re-entry.**

**Rationale (evidence-linked):**

- Core **educational / clinical** blocks are strong enough to **pilot** in clinician-oriented or “deep dive” UI, but **member retail** narrative (`retail_summary`) is **empty by design/policy** on the AB case, and **body overview / longitudinal / reassurance** layers are **not** at benchmark parity.
- Shipping only current `NarrativeReportV1` to a retail primary surface would **under-deliver** vs the locked benchmark without additional assembly or IDL policy work.

---

## 8. Recommended next sprint or next phase

**Smallest bounded sprint that materially improves runtime vs benchmark:**

1. **Retail pathway decision** — Either (a) promote governed retail copy for benchmark phenotypes (`phenotype_allowed` or parallel retail-safe IDL rows), or (b) explicitly scope `retail_summary` as “retail-eligible phenotypes only” and accept benchmark retail as **future**—but then **do not** claim benchmark parity for member summary.
2. **Body overview assembly v1.1** — Deterministic second layer: structured bullets for “calm systems” / driver / secondary themes using existing graph + IDL (without LLM).
3. **Validation harness parity** — Extend **one** golden fixture (or test) to include **questionnaire_data** + **prior snapshot** (or embedded `prior_biomarker_lab_snapshot_v1` + `state_transitions`) so **longitudinal** and **lifestyle bridges** are benchmark-fair.

Frontend re-entry can proceed **in parallel** only for surfaces that **do not** depend on `retail_summary` or full benchmark parity (e.g. clinician blocks, IDL-backed cards).

---

## 9. STOP conditions check

| Condition | Result |
|-----------|--------|
| Reliable runtime output obtainable | **Pass** — `analysis_result.json` from golden runner |
| Output reflects N-8 compiler path | **Pass** — orchestrator → `compile_narrative_report_v1` |
| Fair comparison to benchmark | **Partial** — biomarkers align with AB acceptance; **context/longitudinal inputs** not fully aligned (documented above) |
| Upstream blocker | **None** — no early stop |

---

## 10. Completion note (SOP v1.3.1)

- **Runtime output inspected:** `backend/artifacts/golden_runs/n9-ab-validation-20260422/analysis_result.json` (`narrative_report_v1` + `replay_manifest`).
- **Frontend-readiness judgement:** **Option 2** — one bounded refinement sprint recommended before broad retail re-entry; targeted/clinician pilot feasible.
- **Recommended next move:** Retail IDL/compiler policy alignment + `body_overview` assembly upgrade + benchmark-fair harness inputs for longitudinal/bridges.

---

## Evidence appendix — compiler `meta` snapshot (abridged)

From the inspected run’s `narrative_report_v1.meta`:

- **`assets_resolved`:** `lead_domain_composed`, `secondary_domain_composed`, `next_steps_from_functional_domains`, `clinician_synthesis_idl`, `clinician_synthesis_functional`
- **`skipped`:** `retail_summary_no_enabled_phenotype_cards`, `longitudinal_empty`
- **`idl_bundle_present`:** `true`

This confirms **why** retail and longitudinal were empty without hand-waving.
