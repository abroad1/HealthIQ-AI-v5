# KB-S54B Runtime + Contract Preflight — Primary Concern and Ranked Ambiguity (Phase 2)

**work_id:** `KB-S54B-RUNTIME-PREFLIGHT`  
**Mode:** READ-ONLY investigation (no implementation).  
**Date:** 2026-04-05  
**Authority:** `docs/policy/PRIMARY_CONCERN_AND_RANKED_AMBIGUITY_POLICY_v1.md` (Phase 1 complete)  

---

## 1. Executive summary

| Question | Answer |
|----------|--------|
| **Is Phase 2 ready?** | **Yes** — policy v1 is frozen; code locations for ranking and clinician selection are **narrow and known** (see §3–§4). |
| **Minimum safe change surface** | **Smallest faithful slice:** (1) **`compile_report_v1`** — replace or supplement lexicographic tie-break; optionally attach **ranking/ambiguity metadata** to `ReportV1` / `ReportMetaV1` / `ReportTopFindingV1`; (2) **`compile_clinician_report_v1`** — align page-1 semantics with policy (single lead vs explicit ambiguity). **True** policy compliance for §6 (structured ranked ambiguity) **requires** clinician contract extension unless copy is **only** stuffed into existing strings (fragile, not recommended as final form). |
| **Is one sprint enough?** | **Risky as a single undifferentiated sprint** because **clinician golden JSON** (AB/VR) and **DTO** tests fail on any `ClinicianReportV1` shape change, while **report-only** changes can be tested with **`test_report_compiler_v1`** and insight `report_v1` snapshots **without** touching clinician fixtures first. **Recommended:** **split** runtime/report-contract work from clinician-contract + fixture work (§6). |

---

## 2. Policy translation map (Phase 2 vs later)

### 2.1 Mandatory to translate in Phase 2 (runtime / report contracts)

Grounded in **PRIMARY_CONCERN_AND_RANKED_AMBIGUITY_POLICY_v1.md**:

| Policy ref | Requirement | Phase 2 owner |
|------------|-------------|----------------|
| §4.1, §5 | **Primary concern** reflects governed intent, not “sort happened” | Ordering + explicit **metadata** or clinician copy |
| §7 (closing) | **Lexicographic `signal_id` must not be presented as clinical primacy** | Remove or demote as **last** tie-break; **stamp** when used (`§8`) |
| §8.1–§8.3 | **Deterministic total order** + **technical fallback** documented | Stable sort + machine-readable **tie-resolution / policy version** on `ReportV1` (or meta) |
| §6.3 (partial) | Rank explainable from evidence factors **where encoded** | Prefer using existing `confidence`, `supporting_markers`, `confidence_reasons` on signal rows **before** adding new SSOT |

### 2.2 Strongly coupled to Phase 2 but clinician/UX-shaped

| Policy ref | Requirement | Notes |
|------------|-------------|--------|
| §5.3, §6 | **Ranked ambiguity** when parity / under-supported single winner | Needs **detection** in runtime + **surface** in clinician output → **`ClinicianReportV1` / `Page1SummaryBlockV1`** extension is the **clean** path (`extra="forbid"`). |
| §8.2 | UI/copy reflects ambiguity when fallback used | **Frontend phase** per policy §9; Phase 2 can still emit **structured** fields or explicit strings for later rendering. |

### 2.3 Explicitly deferred (later phases per policy §9)

- **AB/VR golden clinician JSON** regeneration and harness doc updates — **after** clinician compiler + contract are stable (unless Phase 2 is **report-only** and does not change clinician output).
- **Frontend** `ClinicianReportRenderer` + `analysis.ts` — **separate** phase.
- **Full numeric formula** for §7 — policy does not require it in v1.
- **System burden / arbitration** alignment with headline — **out of scope** (policy §10).

---

## 3. Runtime change surface (exact locations)

**Single file owns `top_findings` order:** `backend/core/analytics/report_compiler_v1.py`

| Function | Role |
|----------|------|
| **`compile_report_v1`** | Sorts `signal_results` with `_STATE_RANK`, `-confidence`, **`str(signal_id)`** tie-break (lines ~436–443); builds `ReportTopFindingV1` list with `priority_rank`. |
| **`compile_clinician_report_v1`** | **`primary = top_findings[0]`** (~286); builds `primary_concern` string (~325–328); **`primary_root`** = first `root_cause_v1.findings` matching primary `signal_id` (~292–296); **`top_hypothesis_line`** from **`hypotheses[0]`** (~306–311); **confirmatory** from **`_collect_confirmatory_with_suppression(primary_root, …)`** (~299–302); **key_findings** / **chains** use primary + `top_chains[:2]` (~319–323). |

**Related (secondary for Phase 2):**

- **`compile_root_cause_v1`** (invoked inside `compile_report_v1` ~511–515) — produces **`RootCauseV1.findings`** (multi-finding already). Clinician **selection** is **downstream** in `compile_clinician_report_v1`; root-cause **compiler** change only if policy demands hypothesis ordering per signal tied to new ranking (preflight §7: **medium** likelihood).
- **`build_insight_graph_v1`** — embeds `report_v1` on graph; no separate ranking.
- **`core/dto/builders.py`** — calls `compile_clinician_report_v1`; will pick up contract/output changes automatically.

**Minimal file set for bounded Phase 2:** **`report_compiler_v1.py`** (+ **contracts** below). Optional second touch: **`root_cause_compiler_v1.py`** only if evidence-based ranking requires root-cause ordering changes.

---

## 4. Contract change surface

### 4.1 Definitely impacted (if policy is implemented beyond “silent sort”)

| Contract | Why |
|----------|-----|
| **`ReportMetaV1`** (`backend/core/contracts/report_v1.py`) | Natural home for **`ranking_policy_version`**, **`tie_break_method`**, or short **`ranking_rationale_code`** — satisfies §8 “labelled fallback” and replay alignment (policy §9, §11). |
| **`ReportTopFindingV1`** | Optional **`tie_group_id`**, **`ambiguity_tier`**, or **`ranking_note`** — supports §6 structured / explainable rank without overloading strings. **`extra="forbid"`** → version bump discipline. |

### 4.2 Impacted when clinician output must reflect ambiguity or non-lexicographic primacy honestly

| Contract | Why |
|----------|-----|
| **`Page1SummaryBlockV1` / `ClinicianReportV1`** (`backend/core/contracts/clinician_report_v1.py`) | Today: **single** `primary_concern: str` (required). **Singular headline is structurally hard-coded** for typed page-1. Multi-line ambiguity needs **new fields** (e.g. `ranked_ambiguity_summary`, `co_primary_concerns`, or `interpretation_mode: literal`). |

### 4.3 Optional / likely unchanged in narrow Phase 2a

| Contract | Notes |
|----------|--------|
| **`RootCauseV1` / `RootCauseFindingV1`** | Already **list**-based; selection logic can change **without** schema change if still emitting **one** `root_cause` on clinician contract. **Multiple** clinician root-cause sections → schema + compiler + FE. |

### 4.4 Frontend (understanding only — not Phase 2 implementation)

- **`frontend/app/types/analysis.ts`** — mirrors `ClinicianReportV1.page1.primary_concern` only.
- **`ClinicianReportRenderer.tsx`** — renders **one** “Primary concern” line.

Any new `page1` fields **require** a **later FE phase** (policy §9) even if backend ships first.

### 4.5 Minimum viable contract change (two tiers)

| Tier | Scope | Fulfils policy |
|------|--------|----------------|
| **A — Report meta only** | Extend **`ReportMetaV1`** + sort change in **`compile_report_v1`** | §7–§8 partially (no silent lexicographic **as sole story** if copy references meta in later phase); **does not** fully satisfy §6 user-visible ambiguity. |
| **B — Report + Clinician page1** | Tier A + extend **`Page1SummaryBlockV1`** + **`compile_clinician_report_v1`** | **Necessary** for **structured** ranked ambiguity and honest single-vs-multi lead (§5–§6). |

---

## 5. Narrowest viable implementation shape (grounded)

**Policy does *not* require** full §7 numeric fusion in the first implementation release; it **does** require (§7 closing) that **lexicographic `signal_id` not be treated as clinical primacy**, and (§6) **ranked ambiguity** when parity conditions hold.

**Smallest practical **Phase 2** that remains faithful:**

1. **`compile_report_v1`:** After current primary sort keys, insert **governed** secondary comparisons using **existing** row fields (`supporting_markers` length / presence, `confidence_reasons`, duplicate confidence tiers) **before** any **`signal_id`** tie-break; keep **`signal_id`** only as **documented** last-resort stabiliser.
2. **Stamp:** Add **`ranking_policy_version`** (and optionally **`tie_break_applied`**) on **`ReportMetaV1`** (or equivalent) so replay/tests can assert **policy id**, not accidental order.
3. **`compile_clinician_report_v1`:**  
   - **Either** (minimal string hack) append **one** deterministic sentence to **`key_findings` or `confidence_and_missing_data`** when near-tie / technical tie-break fires — **no** Pydantic change, **weak** for §6.3 “structured”.  
   - **Or** (recommended) add **one or two** optional/structured fields on **`Page1SummaryBlockV1`** for ambiguity / co-primary lines — **requires** Tier B contracts + **fixtures**.

**Defer to later sprint:** FE rendering, full AB/VR JSON refresh **if** Phase 2a ships report-only changes that **preserve** clinician byte-for-byte output (possible only for Tier A + no clinician compiler edits).

---

## 6. AB/VR and regression impact (map only)

| Asset / test | If only `compile_report_v1` + `ReportMeta` / `ReportTopFinding` change | If `compile_clinician_report_v1` or `ClinicianReportV1` changes |
|--------------|----------------------------------------------------------------------|------------------------------------------------------------------|
| **`test_report_compiler_v1.py`** | **Update** expected order / dump shapes | May need further updates if clinician pulls new meta |
| **`test_clinician_report_runtime_alignment.py`** | **Stable** only if clinician **output unchanged** | **Must update** `clinician_report_v1_ab.json` / `clinician_report_v1_vr.json` |
| **`KB-S53` harness docs** | No change if harness scope unchanged | **Document** if acceptance semantics for clinician snapshot shift (not reopening KB-S53 **scope**, but **downstream** of ranking policy) |
| **`test_golden_panel_runner.py`** (report_v1 stability) | May change if `report_v1` meta or top_findings order shifts | Same |
| **Insight graph JSON artefacts** | `report_v1` subtree may change in golden runs | Clinician JSON only if compiler emits it in pipeline under test |

**Conclusion:** Clinician fixture drift is **gated** on clinician compiler + contract edits. That is the main reason to **split** work: validate **report-layer** policy compliance **before** freezing new golden clinician files.

---

## 7. Recommendation

### **`SPLIT_RUNTIME_AND_CONTRACT`**

**Bounded shapes:**

| Sub-phase | Content | Exit criteria |
|-----------|---------|----------------|
| **2a — Report runtime + report contracts** | `compile_report_v1` governed ordering; `ReportMetaV1` / optional `ReportTopFindingV1` fields; unit tests; optional insight `report_v1` regression checks | No change to **`ClinicianReportV1`** serialization; lexicographic tie **demoted** and **stamped** when used |
| **2b — Clinician compiler + clinician contracts + AB/VR fixtures** | `compile_clinician_report_v1` ambiguity / co-primary logic; `Page1SummaryBlockV1` extension; regenerate **`clinician_report_v1_*.json`**; `test_clinician_report_runtime_alignment` | Policy §5–§6 reflected in **structured** page-1 output |

**Why not a single sprint:** Coupling **sort mathematics**, **report schema migration**, **clinician schema migration**, and **two golden JSON files** in one change set **inflates** review surface and blurs rollback boundaries. **Why not DO_NOT_PROCEED:** Policy and code map are **clear enough** to author implementation prompts.

**Alternative (explicitly narrower):** **`PROCEED_AS_ONE_BOUNDED_RUNTIME_CONTRACT_SPRINT`** **only if** product formally accepts **Tier A** for Phase 2 (report meta + sort only, **no** clinician contract change) **and** defers §6 user-visible ambiguity to a **follow-up** immediately queued — this is **policy-complete only for §7–§8**, **not** for §6.

---

## 8. References (repo)

- `docs/policy/PRIMARY_CONCERN_AND_RANKED_AMBIGUITY_POLICY_v1.md`
- `docs/investigations/KB-S54B_PRIMARY_CONCERN_RANKED_AMBIGUITY_PREFLIGHT.md`
- `backend/core/analytics/report_compiler_v1.py`
- `backend/core/contracts/report_v1.py`
- `backend/core/contracts/clinician_report_v1.py`
- `backend/core/contracts/root_cause_v1.py`
- `backend/tests/unit/test_clinician_report_runtime_alignment.py`
- `backend/tests/fixtures/reports/clinician_report_v1_ab.json`, `clinician_report_v1_vr.json`
- `frontend/app/types/analysis.ts`, `frontend/app/components/results/ClinicianReportRenderer.tsx`
