# Product Reality and Direction Audit

**Mode:** read-only investigation (no implementation).  
**Date:** 2026-04-01  
**Scope:** codebase paths, governance artifacts, strategic documents, and reproducible runtime checks.

---

## 1. Executive summary

HealthIQ has a **real, deterministic three-layer pipeline** (orchestrator → insight graph / report → DTOs and golden-runner artifacts) with a **large and growing Knowledge Bus package estate** and **137 registered signals** loaded by `SignalRegistry`. Strategic documents still describe **breadth/depth braiding**, **AB/VR as test harnesses (not the product boundary)**, and **Phase 1 “best deterministic metabolic reasoning engine in the market.”**

**Runtime reality diverges from that ambition in predictable places:** (a) **`lab_range_exceeded` activation does not honour `enable_upper_bound` / `enable_lower_bound` flags**, which produces **contradictory signals on the same analyte value** (observed on AB/VR-style panels for total cholesterol and cortisol); (b) **per-biomarker scoring in the orchestrator requires both numeric min and max** for the “scored” path, so **one-sided lab ranges** yield **“Not scored - insufficient numeric bounds for scoring”** even when the lab supplied a partial range; (c) **root-cause / WHY compilation is wired for only six signal IDs**—most fired signals have **no hypothesis assets** in `compile_root_cause_v1`; (d) **clinician summary** is a **real compiled object** (`ClinicianReportV1`) but **keys off `top_findings[0]`**, which can **omit root-cause content** when that primary signal is not one of the six targets; (e) **questionnaire mapping populates context and insight synthesis input**, while **UK lifestyle JSON** affects analysis **only when `lifestyle_inputs` is supplied** to `run` / golden runner.

**Package expansion remains necessary for biological coverage, but the bottleneck visible in harness outputs has shifted toward activation/scoring correctness, WHY surface area, and report/clinician alignment.**

---

## 2. Answers to investigation questions

### Q1 — Why are some biomarker ranges not recognised correctly? (dual high/low; “insufficient numeric bounds”; which layer?)

#### 2.1 Same analyte → both “high” and “low” signals (runtime-observed, code-grounded)

**Observed behaviour (reproducible):** On fixtures such as `ab_full_panel_with_ranges.json`, **`signal_total_cholesterol_high` and `signal_total_cholesterol_low`** both appear in `signal_results` for the **same numeric `total_cholesterol` value**. On `vr_full_panel_with_ranges.json`, **`signal_cortisol_high` and `signal_cortisol_low`** both fire for the **same cortisol value** (e.g. above the lab max).

**Root cause (implementation):** `SignalEvaluator._evaluate_lab_range_activation_state` applies

```163:164:backend/core/analytics/signal_evaluator.py
        if high is not None and primary_value > high:
            return upper_bound_state
```

**without checking `activation_config.enable_upper_bound`.** Packages correctly set `enable_upper_bound: false` on “low” semantics (e.g. `signal_total_cholesterol_low`, `signal_cortisol_low`) and `enable_lower_bound: true` only for the lower tail—but when the value is **above** the lab maximum, the **first branch still runs** and returns `upper_bound_state` for **both** signal definitions that share the same `primary_metric` and lab range.

**Contrast with package intent:** e.g. `pkg_kb60_total_cholesterol_low_hypocholesterolemia_context` sets `enable_upper_bound: false` and `enable_lower_bound: true`; `pkg_kb52c_cortisol_low_adrenal_insufficiency` sets `enable_upper_bound: false` and `enable_lower_bound: true`.

| Layer | Role |
|--------|------|
| Fixture input shape | Provides lab `reference_range` min/max; not the bug source. |
| Parsing / normalisation | Supplies lab ranges to evaluator; not the bug source. |
| **Signal activation logic** | **`_evaluate_lab_range_activation_state` ignores enable flags for the upper branch** → **authoritative defect location.** |
| Range binding | Lab min/max read correctly; issue is conditional application. |
| Scoring / arbitration | Separate from signal firing; does not fix mutual exclusion. |
| Report assembly | Surfaces all fired signals via `compile_report_v1` ordering; amplifies the defect. |

#### 2.2 “Not scored - insufficient numeric bounds for scoring” despite panel ranges

**String origin:** `backend/core/pipeline/orchestrator.py` sets this interpretation when building biomarker DTOs.

**Logic:** `_has_valid_numeric_bounds` requires **both** `min` and `max` to be numeric **and** `min < max`:

```915:924:backend/core/pipeline/orchestrator.py
            def _has_valid_numeric_bounds(ref: Any) -> bool:
                if not isinstance(ref, dict):
                    return False
                min_val = ref.get("min")
                max_val = ref.get("max")
                return (
                    isinstance(min_val, (int, float))
                    and isinstance(max_val, (int, float))
                    and float(min_val) < float(max_val)
                )
```

If the biomarker row is on the **“scored via health_system_scores”** path and `unscored_reason` is set, or `status == "unknown"`, or **`not _has_valid_numeric_bounds`**, the interpretation becomes “insufficient numeric bounds” when **any** single-sided bound exists (`_has_any_numeric_bound`).

**Therefore:** common commercial panels with **only an upper OR lower bound** (e.g. LDL max-only, HDL min-only) produce **unknown status** on the DTO path that depends on both bounds (see nearby `frontend_status_from_value_and_range` usage at lines ~1645–1652) and the **“insufficient numeric bounds”** copy—even though the lab range object exists.

| Layer | Role |
|--------|------|
| Fixture | Often one-sided ranges—valid real-world shape. |
| **Orchestrator DTO/scoring bridge** | **Requires two-sided numeric bounds for full scoring + status on that path** → message. |
| Signal evaluator | Uses one-sided lab logic in places (`_evaluate_lab_range_activation_state` allows high-only or low-only for activation). |
| Report | `compile_clinician_report_v1` labels range quality “one-sided” separately—orthogonal to orchestrator score message. |

---

### Q2 — How complete are the signal packages?

**Quantitative (filesystem, 2026-04-01):** `knowledge_bus/packages` contains **186** directories with names starting `pkg_` (Python `pathlib` count during this audit).

**Governance snapshot (may lag repo growth):** `knowledge_bus/governance/package_estate_KB-S49_v1.yaml` (`generated_date: '2026-03-28'`) records **`pkg_directories_total: 74`**, **`governed_packages_in_inventory: 73`**, and explicitly states **runtime does not branch on package tier**—`SignalRegistry` merges `knowledge_bus/packages/*/signal_library.yaml` with deterministic duplicate handling.

**Runtime signal count:** `SignalRegistry` loads **137 unique `signal_id` values** (verified via `python -c` importing `SignalRegistry` in `backend/`).

**Coverage vs ingestion:** Ingestion has **materially increased** package/signal surface area compared to older audit documents (e.g. `docs/AUDIT_SPRINT_PLAN_2026-03-20.md` cites **51 signals**—**stale relative to current registry**).

**Bottleneck assessment:** **Package/signal count is no longer the only limiting factor.** The estate note in KB-S49 already flags **no tier gating at runtime**; combined with **activation bugs (Q1)** and **shallow WHY coverage (Q3)**, **quality and coherence of outputs** are now co-equal bottlenecks with **raw package expansion**.

---

### Q3 — How complete are the WHY analysis paths?

**Where WHY lives at runtime**

- `compile_report_v1` in `backend/core/analytics/report_compiler_v1.py` calls `compile_root_cause_v1(...)`, attaching `root_cause_v1` to `ReportV1`.
- `compile_root_cause_v1` in `backend/core/analytics/root_cause_compiler_v1.py` only iterates **`_ROOT_CAUSE_TARGETS`**—a **fixed list of six** `(signal_id, hypotheses_loader)` pairs:

```31:37:backend/core/analytics/root_cause_compiler_v1.py
_ROOT_CAUSE_TARGETS = [
    ("signal_homocysteine_elevation_context", load_hcy_hypotheses_v1),
    ("signal_hba1c_high", load_hba1c_hypotheses_v1),
    ("signal_hepatic_alt_context", load_alt_hypotheses_v1),
    ("signal_thyroid_tsh_context", load_tsh_hypotheses_v1),
    ("signal_insulin_resistance", load_insulin_resistance_hypotheses_v1),
    ("signal_systemic_inflammation", load_systemic_inflammation_hypotheses_v1),
]
```

- Hypothesis YAML assets on disk: `knowledge_bus/root_cause/hypotheses/*.yaml` (**six files**), loaded via `backend/core/knowledge/load_root_cause_hypotheses.py`.

**Shallow / missing / not surfacing**

- **~131 / 137 signals** have **no** dedicated root-cause hypothesis pipeline in `compile_root_cause_v1` (they may still appear in `top_findings` and chains).
- **`docs/METABOLIC_PATHWAY_COVERAGE_AUDIT_2026-03-20.md`** documents broad pathway gaps; it is **partially stale** (e.g. it lists systemic inflammation as lacking hypotheses, but **`systemic_inflammation_hypotheses_v1.yaml` now exists**). It remains directionally correct that **lipid, renal, iron, and many hepatic/inflammatory sub-signals still lack registered hypothesis targets** matching the **six** compiler entries.
- **Package content vs runtime WHY:** Many packages supply **`explanation` blocks** on `SignalResult` (signal layer) but **not** the structured **root_cause_v1** finding unless the signal is one of the six targets and meets state filters (`suboptimal` / `at_risk` in fired set).

**Distinction**

| Mechanism | Delivers |
|-----------|----------|
| Signal `explanation` dict | Per-signal narrative fragments in `signal_results`. |
| Interaction chains | Graph / ordering / summaries in `interaction_summary`. |
| **`root_cause_v1`** | **Structured hypotheses + confirmatory tests**—**only for six signal IDs.** |

---

### Q4 — When and how can lifestyle / questionnaire inputs influence analysis?

**Questionnaire (`questionnaire_data` on orchestrator `run`)**

- `backend/core/pipeline/orchestrator.py` validates and maps questionnaire → **`lifestyle_factors`** and **`medical_history`** dicts on `user_data`, then embeds them in **analysis context** (`create_context(..., lifestyle_factors=..., medical_history=...)`).
- **Insight synthesis** receives `lifestyle_profile=user.get('lifestyle_factors', {})`:

```1586:1591:backend/core/pipeline/orchestrator.py
            insights_result = self._synthesize_from_insight_graph(
                context=context,
                insight_graph=insight_graph,
                explainability_report=explainability_report,
                lifestyle_profile=user.get('lifestyle_factors', {}) or {},
            )
```

**UK lifestyle fixture (`lifestyle_inputs`)**

- `run(..., lifestyle_inputs=...)` triggers **`LifestyleModifierEngine`** only when a non-empty dict is provided (`orchestrator.py` ~1406–1415, lazy import). Same for `tools.run_golden_panel` **`--lifestyle-fixture`** path.

**What is not yet “governed analytical truth”**

- Questionnaire → **narrative / overlay-style consumption** in synthesis; not the same as **signal thresholds** or **root_cause rules** unless explicitly wired (no evidence in this audit that lifestyle fields rewrite signal activation).
- Strategic doc `docs/HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan_v1.4_amended.md` treats **structured context inputs** as **vision**; runtime wiring is **partial** (context + burdens + synthesis), not full **reasoning-core integration**.

---

### Q5 — Where is the clinician report?

**Generation path**

1. `ReportV1` built in pipeline with `root_cause_v1`, `top_findings`, `top_chains`, etc. (`compile_report_v1`).
2. `compile_clinician_report_v1` in `backend/core/analytics/report_compiler_v1.py` projects **`report_v1` + biomarker rows** → **`ClinicianReportV1`**.
3. `build_analysis_result_dto` in `backend/core/dto/builders.py` attaches **`clinician_report_v1`** to the API-shaped result.

**Output shape**

- Contract: `backend/core/contracts/clinician_report_v1.py`.
- Golden runner writes `analysis_result.json`, `insight_graph.json`, etc.; **clinician report is derived** in DTO build / tests (e.g. `backend/tests/unit/test_clinician_report_runtime_alignment.py`).

**Structural completeness vs runtime**

- The **contract is real and populated** for panels where **`top_findings[0]` matches a `root_cause_v1` finding** (e.g. homocysteine-primary AB scenarios in tests).
- **Gap:** `compile_clinician_report_v1` selects **primary = `top_findings[0]`** and then **`primary_root`** only if **`signal_id` matches** a row in `root_cause_v1.findings`. If primary is e.g. **`signal_alp_low`**, and **ALT/root-cause target is not that signal**, **`sections.root_cause` is `null`** and **hypothesis lines fall back** to **“No hypothesis set available for this concern in v1.”** (`report_compiler_v1.py` ~292–306, 304–305).

**Assessment:** **Structurally complete contract, behaviourally thin or inconsistent** when **report ordering** and **root-cause targets** diverge.

---

### Q6 — Are we still building along phenotype paths?

**Active artifacts**

- Fixtures: `backend/tests/fixtures/panels/phenotypes/*.json`.
- Expectations harness: `backend/tests/fixtures/panels/phenotypes/phenotype_expectations_v1.yaml` exercised by **`backend/tests/unit/test_phenotype_suite_v1.py`** (uses `run_golden_panel`).
- Maps: `knowledge_bus/phenotypes/` and references in `docs/METABOLIC_PATHWAY_COVERAGE_AUDIT_2026-03-20.md` to **`phenotype_map_v1.yaml`**.

**Status:** **Live as a test / coverage harness**, not shown in this audit as the **primary runtime driver** of production `AnalysisOrchestrator` (phenotypes are **validation and documentation-oriented** unless separately wired into default runs).

---

### Q7 — Is the strategic goal still “most comprehensive metabolic reasoning engine”?

**Strategy (documented intent)**

- `docs/HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan_v1.4_amended.md` **§3 Long-Term Company Vision — Phase 1 — Engine moat:** *“Build the best deterministic metabolic reasoning engine in the market.”*
- Same file **§1 Executive Intent:** reference platform for **deterministic metabolic intelligence**, Class II trajectory, acquisition-scale ambition.
- **§2.2 What it is not:** explicitly **not** a narrow AB/VR-only interpreter.

**Current reality**

- Engine **is** deterministic and broad in **signal/package count**; **WHY depth** remains **narrow** (six root-cause targets). **Strategic wording remains; implementation is mid-maturity** on reasoning depth.

---

### Q8 — Is the go-to-market questionnaire still driving product direction?

**Harness role (verified)**

- AB/VR JSON fixtures under `backend/tests/fixtures/panels/` are referenced by **`test_golden_panel_runner.py`**, **`test_clinician_report_runtime_alignment.py`**, **`test_root_cause_v1_homocysteine.py`**, and **`test_phenotype_suite_v1.py`**.
- Strategic plan **explicitly** states AB/VR are **“realistic minimum commercial test harnesses, not the final product boundary”** (`HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan_v1.4_amended.md` §1).

**Questionnaire**

- **Runtime:** `QuestionnaireMapper`, validation, and context attachment in **`orchestrator.py`** (see Q4).
- **No single `knowledge_bus` questionnaire SSOT file** was found by filename search during this audit; questionnaire shape is **code-level** (`QuestionnaireSubmission`, validators).

**Distinction**

| Concept | Role |
|---------|------|
| AB/VR + golden runner | **Floor / regression harness** for deterministic pipeline. |
| Strategic boundary | **Broader panels + longitudinal context** per vision doc—not locked to AB/VR. |

**Older audit caveat:** `docs/AUDIT_SPRINT_PLAN_2026-03-20.md` claimed **no formal AB/VR distinction**; **tests and fixtures now provide de facto panel profiles** (`ab_full_panel_with_ranges.json`, `vr_full_panel_with_ranges.json`) even if not a separate runtime `panel_type` enum.

---

## 3. Evidence references (by topic)

| Topic | Primary evidence |
|--------|------------------|
| Dual signal bug | `backend/core/analytics/signal_evaluator.py` `_evaluate_lab_range_activation_state`; packages `pkg_kb60_total_cholesterol_low_*`, `pkg_kb52c_cortisol_low_*` |
| Insufficient bounds message | `backend/core/pipeline/orchestrator.py` `_has_valid_numeric_bounds`, DTO interpretation branches |
| Signal / package counts | `SignalRegistry` (137 signals); `knowledge_bus/packages` (186 `pkg_*` dirs); `package_estate_KB-S49_v1.yaml` |
| WHY scope | `root_cause_compiler_v1.py` `_ROOT_CAUSE_TARGETS`; `knowledge_bus/root_cause/hypotheses/*.yaml` |
| Clinician report | `report_compiler_v1.py` `compile_clinician_report_v1`; `dto/builders.py`; `clinician_report_v1.py` contract |
| Lifestyle / questionnaire | `orchestrator.py` questionnaire mapping; `LifestyleModifierEngine` lazy path; `run_golden_panel.py` `--lifestyle-fixture` |
| Phenotypes | `test_phenotype_suite_v1.py`, `phenotype_expectations_v1.yaml` |
| Strategy | `docs/HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan_v1.4_amended.md` |
| Stale vs current | `docs/AUDIT_SPRINT_PLAN_2026-03-20.md` (51 signals); `docs/METABOLIC_PATHWAY_COVERAGE_AUDIT_2026-03-20.md` (hypothesis gaps partially superseded) |
| Runtime harness | `backend/tools/run_golden_panel.py`; tests under `backend/tests/unit/` |

---

## 4. Strategy vs current reality

| Strategy (documents) | Current reality (code + runs) |
|----------------------|-------------------------------|
| Best deterministic metabolic reasoning engine | **Strong** deterministic stack, **large signal library**; **WHY narrow** (6 root-cause targets). |
| Full-panel WHY / root cause | Most signals: **explanations + chains only**; **structured WHY** only for **six** IDs. |
| AB/VR as harness, not boundary | **Tests align**; fixtures are **active** regression anchors. |
| Context-rich (lifestyle, questionnaire) | **Wired into context and synthesis**; **not** shown as rewiring **signal activation** globally. |
| Tiered package quality (KB-S49) | **Documented** tiers; **runtime ignores tier** per governance YAML. |

---

## 5. Top 5 platform truths

1. **Determinism and contracts are real:** InsightGraph, ReportV1, replay manifest, explainability, and golden runner are implemented—not vaporware (`run_golden_panel.py`, orchestrator Step 4–7).
2. **Signal registry scale:** **137** signals loaded from packages; **186** package dirs on disk (2026-04-01 count).
3. **Lab-range sovereignty is explicit** in orchestrator comments for DTO range sourcing—**scoring tightness** is a **product rule**, not an accident.
4. **Root-cause WHY is a small, explicit allowlist** of six signals—everything else depends on signal text + chains.
5. **Strategic narrative remains engine-first** (Phase 1 moat) in **v1.4 amended** roadmap, aligned with **not** being “AB/VR-only.”

---

## 6. Top 5 platform gaps

1. **`lab_range_exceeded` ignores `enable_upper_bound` / lower-bound gating symmetry** → **opposite-direction signals on the same value** (code defect, Q1).
2. **Two-sided bound requirement** for parts of biomarker scoring → **“insufficient numeric bounds”** on **valid one-sided lab reports** (Q1).
3. **WHY / root_cause coverage** tiny vs **137 signals**—**content and compiler registration** must scale together (Q3).
4. **Clinician report primary concern** can **lack root_cause** when **`top_findings[0]` is not in `_ROOT_CAUSE_TARGETS`** (Q5).
5. **Governance inventory (KB-S49) understates current package count**—**risk/completeness tracking** may be **out of date** unless regenerated (Q2).

---

## 7. Recommended next strategic sprint (repo reality, not nostalgia)

**Title (suggested):** *Signal activation integrity + report-primary / root-cause alignment.*

**Why (evidence-based):**

- Fixing **`enable_upper_bound` / `enable_lower_bound` semantics** in `_evaluate_lab_range_activation_state` removes **clinically false dual signals** without new KB prose.
- Pair with **either** expanding `_ROOT_CAUSE_TARGETS` for top traffic signals **or** changing **`compile_clinician_report_v1`** to select primary concern from **first finding that has root-cause** (product choice—either way addresses **observed null `root_cause`** on VR-style primaries).
- **One-sided range scoring policy** (explicit product rule: score vs unknown vs band-only) resolves **user-visible “not scored”** friction on real panels.

**Explicitly deferred here:** LLM narrative production enablement (strategically important per audit doc, but **separate** from the **deterministic false-signal** defect above).

---

## 8. Method notes

- Code inspection paths as cited; **no repository code was modified** for this artifact.
- **Runtime counts:** `SignalRegistry` and `pathlib` directory enumeration executed from `backend/` on 2026-04-01.
- Prior conversation validated AB/VR golden runs; this document **does not duplicate** full JSON dumps but references the same paths (`tools.run_golden_panel`, AB/VR fixtures).
