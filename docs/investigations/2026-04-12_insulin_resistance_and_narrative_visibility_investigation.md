# Insulin resistance, metabolic phenotype visibility, and Advanced narrative thinness — runtime-truth investigation

**Date:** 2026-04-12  
**Scope:** Bounded runtime truth only (no code changes, no copy redesign).  
**Work package:** Ad hoc investigation aligned with current UAT observations (hero/Why improved but mechanical; Advanced “Narrative summaries” thin; no obvious insulin-resistance narrative).

---

## Executive summary

1. **There is no single exported JSON snapshot of “the” live UAT analysis in this repository.** Runtime truth was established by reproducing the **governed acceptance harness** and **default golden panel** paths that the codebase already treats as authoritative regression inputs, and by reading the **insulin resistance** signal contract and **narrative runtime** policy in source.

2. **For the primary AB acceptance panel (`ab_full_panel_with_ranges.json`), `signal_insulin_resistance` does not appear in `meta.insight_graph.signal_results` at all.** It is not merely ranked below the fold: the signal is **not emitted** for this run. Grounded reason: the governed signal **requires biomarkers including `glucose`** (and derived `tyg_index`) per `knowledge_bus/packages/pkg_insulin_resistance/signal_library.yaml`, while the AB acceptance fixture **does not include a `glucose` analyte** (confirmed by searching `backend/tests/fixtures/panels/ab_full_panel_with_ranges.json`). Without those inputs, the insulin-resistance phenotype **cannot be evaluated** under current package rules—not a UI suppression bug.

3. **The VR acceptance panel (`vr_full_panel_with_ranges.json`) likewise contains no `glucose` key** in the fixture inspected; the same dependency conclusion applies unless a real user upload includes fasting glucose (or an aliased equivalent the pipeline maps to `glucose`).

4. **Contrast (panel that *does* support IR):** `backend/tests/fixtures/golden_panel_160.json` includes `glucose` (and related lipids). A `run_golden_panel` reproduction shows `signal_insulin_resistance` **at_risk** with confidence **0.9**, present in **`meta.insight_graph.signal_results`** and in **`meta.insight_graph.report_v1.top_findings`** at **rank 4** (0-based index 3 in sorted list). So insulin resistance **can** appear in stored payloads when governed inputs exist—but it will **not** drive the default hero or compiled clinician root-cause thread when **higher-ranked findings** (e.g. lipid transport) win the lead slot.

5. **Advanced “Narrative summaries” thinness** is explained by **runtime metadata**, not missing UI wiring: with `write_narrative=False` on the orchestrator path used in golden runs, `meta.narrative_runtime.policy_reason` resolves to **`orchestrator_explicit_false`**, `runtime_mode` is **`deterministic_mock`**, and `insights[]` entries are **short category templates** (e.g. `manifest_id: "legacy_v1"`, generic title/description). That matches a **non–live-LLM** path. Production `/api/analysis` behaviour for live Gemini requires **double opt-in** (`HEALTHIQ_NARRATIVE_LLM` and `HEALTHIQ_ENABLE_LLM`) per `backend/core/insights/narrative_runtime_policy.py`.

6. **Rendered UI mapping:** Hero and Why are fed from **`clinician_report_v1`** (compiler output) and related components on `frontend/app/(app)/results/page.tsx`; narrative cards are **`InsightsPanel`** consuming **`insights[]`** plus **`meta.narrative_runtime`**. There is **no separate** “insulin resistance headline” component—IR visibility is indirect (signals → report → compiler → UI).

---

## Methodology and limits

| Item | Detail |
|------|--------|
| Live UAT `analysis_id` | **Not present in-repo.** Findings below use **reproducible pipeline outputs** instead. |
| AB acceptance proxy | `tools.run_golden_panel` with `tests/fixtures/panels/ab_full_panel_with_ranges.json` via `ab_acceptance_fixture_path()` (`backend/tests/support/panel_acceptance.py`). |
| Golden contrast | `tests/fixtures/golden_panel_160.json` (includes `glucose`; IR signal appears). |
| Orchestrator flags | `write_narrative=False` for deterministic harness (matches thin narrative + explicit policy reason). |

To attach this investigation to a **specific** UAT row in storage, export `GET /api/analysis/result` (or DB JSON) for that `analysis_id` and diff against the paths listed below.

---

## Files and payload paths inspected

### Authority / fixtures

| File | Role |
|------|------|
| `backend/tests/fixtures/panels/panel_acceptance_profiles_v1.yaml` | Maps `ab_acceptance` → `panels/ab_full_panel_with_ranges.json` |
| `backend/tests/fixtures/panels/ab_full_panel_with_ranges.json` | AB acceptance biomarkers (no `glucose` key found) |
| `backend/tests/fixtures/panels/vr_full_panel_with_ranges.json` | VR acceptance biomarkers (no `glucose` key found) |
| `backend/tests/fixtures/golden_panel_160.json` | Broad regression panel (**includes `glucose`**) |
| `knowledge_bus/packages/pkg_insulin_resistance/signal_library.yaml` | IR signal dependencies (`glucose`, `triglycerides`, `hba1c`, derived `tyg_index`, etc.) |

### Runtime policy and synthesis

| File | Role |
|------|------|
| `backend/core/insights/narrative_runtime_policy.py` | LLM allow/deny; `narrative_runtime_meta_from_decision`; double opt-in for API path |
| `backend/core/insights/synthesis.py` | Attaches `narrative_runtime` to synthesis summary; category insights generation |
| `backend/app/routes/analysis.py` | Notes `allow_llm=None` for HTTP path (gating inside synthesizer) |

### Frontend (rendering map)

| File | Role |
|------|------|
| `frontend/app/(app)/results/page.tsx` | Composes `InsightPanel` (hero), `RootCauseEvidenceSummary` (Why), `InsightsPanel` (narrative), `ClinicianReportRenderer`, clusters/dials |
| `frontend/app/components/insights/InsightPanel.tsx` | Hero interpretation from `clinician_report_v1.sections.page1` |
| `frontend/app/components/results/RootCauseEvidenceSummary.tsx` | Why / evidence walkthrough from `clinician_report_v1.sections.root_cause` |
| `frontend/app/components/insights/InsightsPanel.tsx` | Advanced “Narrative summaries”; empty state uses `narrativeRuntimePresentation` |
| `frontend/app/lib/narrativeRuntimePresentation.ts` | Maps `meta.narrative_runtime` to user-facing empty copy |

### DTO / graph shape (conceptual)

| Payload path | Content |
|--------------|---------|
| `meta.insight_graph` | `signal_results`, `report_v1`, interaction summaries, biomarker context, etc. |
| `meta.insight_graph.report_v1.top_findings` | Ranked findings for hero/report compilation |
| `meta.insight_graph.report_v1.root_cause_v1` | Structured root-cause hypotheses per signal finding |
| `insights[]` | Layer C narrative cards |
| `meta.narrative_runtime` | Policy metadata (mock vs live, reasons) |

---

## 1. Stored/runtime payload — AB acceptance reproduction

**Command-class evidence:** `run_golden_panel(fixture_path=ab_acceptance, write_narrative=False)` yields:

- **`meta.insight_graph.signal_results`:** 15 rows; **`signal_insulin_resistance` absent** (not in list).
- **`meta.insight_graph.report_v1.top_findings`:** 15 rows; top entries include homocysteine / apoA1 / cholesterol patterns; **no IR row**.
- **`insights[]`:** 6 items (one per category); first item example shape: category **`metabolic`**, **`manifest_id`: `legacy_v1`**, title/description generic (“Metabolic focus: summarise structured signals…”).
- **`meta.narrative_runtime`** (representative):
  - `runtime_mode`: **`deterministic_mock`**
  - `client_kind`: **`mock`**
  - `synthesizer_allow_llm_resolved`: **`false`**
  - `policy_reason`: **`orchestrator_explicit_false`**

**Interpretation:** This is **not** “IR suppressed by ranking” on this panel—it **never enters** `signal_results`. The governed IR package requires **`glucose`** among required biomarkers (`pkg_insulin_resistance/signal_library.yaml`); the AB acceptance JSON **does not define `glucose`**, so the TyG-based IR signal **does not fire** under current KB rules.

---

## 2. Does insulin-resistance-related output exist for this run?

| Question | AB acceptance harness | Golden panel 160 |
|----------|----------------------|------------------|
| `signal_insulin_resistance` in `signal_results`? | **No** | **Yes** (`at_risk`, conf ~0.9) |
| In `report_v1.top_findings`? | **No** | **Yes** (rank **4** in reproduced ordering) |
| In `root_cause_v1.findings`? | N/A (signal absent) | **Yes** — IR appears among multiple findings |
| Drives compiled `clinician_report_v1.sections.root_cause` primary thread? | N/A | **No** — primary aligns to **lead top finding** (repro: **`signal_lipid_transport_dysfunction`**, not IR) |

**Answer for UAT-like AB acceptance data:** **No** insulin-resistance signal row exists in storage—**not** because of ranking alone, but because **required panel inputs for the governed IR signal are missing** in the acceptance fixture (no `glucose`).

**Answer when panel supports IR (golden 160):** **Yes**, IR exists in structured storage, but it is **not the lead hypothesis** in the default clinician report when higher-severity / higher-ranked patterns dominate—so the **hero and Why** stay on the **lead** thread unless product rules change (out of scope here).

---

## 3. Why Advanced “Narrative summaries” are thin

| Mechanism | Evidence |
|-----------|----------|
| **Non-live narrative path** | `meta.narrative_runtime.runtime_mode === "deterministic_mock"` and `policy_reason === "orchestrator_explicit_false"` when orchestrator runs with narrative disabled / explicit false (reproduced with `write_narrative=False`). |
| **Template insights** | `insights[]` entries carry **`legacy_v1`** manifest, **short duplicated title/description**, **empty biomarkers** in sample—consistent with **deterministic placeholder** behaviour, not rich Gemini prose. |
| **Production live path** | `resolve_narrative_llm_allow_llm` requires **`HEALTHIQ_NARRATIVE_LLM`** and **`HEALTHIQ_ENABLE_LLM`** (and `LLM_ENABLED`) for default API double opt-in (`narrative_runtime_policy.py`). If unset, narrative stays off/mock-like. |

**UI:** `InsightsPanel` renders whatever is in `insights[]`; when items are generic, the surface **looks empty** even though the section is “populated” with six shallow cards.

---

## 4. UI ↔ source field mapping (metabolic / narrative)

| UI surface | Primary source | Component |
|------------|----------------|-----------|
| Hero interpretation | `clinician_report_v1.sections.page1` (+ modes/runner-up fields) | `InsightPanel` |
| Why / evidence | `clinician_report_v1.sections.root_cause` | `RootCauseEvidenceSummary` |
| Clinician tab | Same report object | `ClinicianReportRenderer` |
| Narrative summaries | `insights[]`, `meta.narrative_runtime` | `InsightsPanel` |
| Clusters / dials | `clusters[]`, `biomarkers[]` | `ClusterSummary`, `BiomarkerDials` |

**Richer metabolic data in payload but not in hero?**  
For golden 160, **`signal_insulin_resistance`** exists in **`signal_results`** and **`top_findings`**, but **hero/root-cause** follow **`top_findings[0]`** alignment rules in the compiler—not a hidden field; it’s **ranking/presentation**, not a render bug.  
For AB acceptance, **IR does not exist in payload**, so there is nothing to surface.

---

## 5. Governance / clinical expectation on AB acceptance panel

Given **absent `glucose`** on the AB acceptance fixture:

- Emitting a **specific insulin-resistance phenotype narrative** would **not** be supported by the **current governed IR signal** (TyG-based with explicit biomarker dependencies).
- **HbA1c** and **triglycerides** alone **do not satisfy** the declared required set without **`glucose`** and derived **`tyg_index`** per the package file cited above.

So **absence of IR on this panel is consistent with governed KB rules**, not an arbitrary UI omission.

---

## 6. Structured answers (checklist)

| Question | Answer |
|----------|--------|
| IR-related output exists in AB acceptance run? | **No** (signal row absent). |
| If absent, why? | **Did not fire** — missing **`glucose`** (and thus TyG path) in harness fixture; not a ranking artefact. |
| IR on a panel that includes glucose? | **Yes** (golden 160 repro) — present at **lower rank**; **not** lead root-cause thread. |
| Advanced narrative Gemini vs mock? | Repro harness: **mock / deterministic** with explicit **`orchestrator_explicit_false`**; production needs **env opt-in** for live. |
| Richer data unrendered? | **AB:** No IR data to render. **Golden 160:** IR **present** in graph but **not** selected as lead **by design** of compiler/ranking—not “hidden in JSON.” |

---

## Smallest safe next fix scope (informational)

1. **Operator:** For any real UAT run, export **`meta.narrative_runtime`** and a list of **`signal_results` IDs** to confirm env + signal presence in one glance.  
2. **Product/data:** Confirm whether UAT uploads include **fasting glucose** (canonical **`glucose`**)—without it, **IR will not appear** under current KB.  
3. **Narrative quality:** If “world-class” prose is required, **governed env** for live narrative must be **intentionally enabled** and validated—not assumed from default API behaviour.

---

## Recommended next sprint classification (non-binding)

| Track | Rationale |
|-------|-----------|
| **BEHAVIOUR / MIXED (governed)** | Only if changing **which** finding drives hero/Why or **surfacing** non-lead metabolic signals—touches user-facing reasoning. |
| **CONTENT / CONFIG** | If work is **env + operational validation** of narrative LLM paths and UAT evidence exports. |
| **DATA / PANEL** | If UAT labs **omit glucose**, primary fix is **input completeness**, not ranking code. |

---

## Exact output path

**File written:** `docs/investigations/2026-04-12_insulin_resistance_and_narrative_visibility_investigation.md`

---

*End of report.*
