# KB-S54B Preflight — Primary Concern and Ranked Ambiguity Policy

**work_id:** `KB-S54B-PREFLIGHT`  
**Mode:** READ-ONLY investigation (no implementation).  
**Date:** 2026-04-04  

---

## 1. Executive summary

| Question | Answer |
|----------|--------|
| **What the future sprint is trying to change** | Move from **implicit** primary selection (fixed sort + lexicographic tie-break) to an **explicit, governed “primary concern / ranked ambiguity” policy**: when to foreground one concern, when to surface **multiple plausible interpretations**, and how **confidence**, **missing data**, **confirmatory tests**, and **contradictions** should affect **ranking** — without ad hoc edits during unrelated delivery sprints. |
| **Is the repo ready?** | **Partially.** The pipeline already exposes **ordered** `top_findings` with **confidence**, **confidence_reasons**, and **supporting_markers**, and **`RootCauseV1`** already carries **multiple findings** with **multi-hypothesis** structures. The **clinician headline** and **page-1 narrative** are still **structurally singular** (`primary_concern` string; **one** `root_cause` block on the clinician contract tied to `top_findings[0]`). |
| **Likely change surface** | **Cross-layer:** `compile_report_v1` ordering rules (and possibly tie/ambiguity metadata), **`compile_clinician_report_v1`** selection and copy, **Pydantic contracts** (`ClinicianReportV1` / `Page1SummaryBlockV1` at minimum), **AB/VR clinician fixtures** and any snapshot tests, and **frontend** types + `ClinicianReportRenderer` (single “Primary concern” line today). |

**Final recommendation (see §6):** **`SPLIT_INTO_PHASED_SEQUENCE`** — policy/governance artifact first, then bounded runtime + contract, then fixture/harness, then FE rendering (unless product explicitly accepts a backend-only phase with unchanged UI).

---

## 2. Strategic decision grounding (repo evidence)

### 2.1 What has already been decided

**Sources:** `docs/investigations/VR_PRIMARY_CONCERN_RANKING_INVESTIGATION.md`, `docs/investigations/KB-S53_VR_FIXTURE_OPERATOR_REVIEW.md` §0–§1, `KB-S53_AB_VR_ACCEPTANCE_HARNESS.md` (operator acceptance block).

| Decision | Evidence |
|----------|----------|
| **Keep current deterministic ranking operationally for now** | VR investigation documents **exact** sort: state rank → confidence → **ascending `signal_id`**. Operator accepted regenerated clinician JSON as **consistent with that behaviour**, not as a KB-S53 defect. |
| **Do not reopen KB-S53 for ranking** | Explicit sprint boundary: KB-S53 = AB/VR harness formalisation; ranking philosophy **out of scope**. |
| **Do not make ad hoc ranking-policy changes inside delivery** | VR doc: changing tie-break / “who wins” belongs in a **follow-on, explicit ranking-policy** sprint, not fixture rejection. |

### 2.2 What has *not* been authorised yet

- **No** new tie-break rule (e.g. vascular vs nutritional priority, homocysteine vs ALP) is encoded in repo strategy docs beyond “defer to future sprint.”
- **No** product spec in-repo defines **multi-headline** or **ranked ambiguity** UX (contrast with existing **singular** `primary_concern` contract).
- **No** sprint prompt exists yet for KB-S54B implementation (this preflight only).

### 2.3 What the future sprint is intended to change

- Replace **implicit** “`top_findings[0]` = truth” with **governed** rules for:
  - **primary** vs **co-primary** vs **explicit ambiguity**
  - how **confidence** and **evidence gaps** adjust **rank** or **presentation**
- Align **runtime**, **contracts**, **fixtures**, and **UI** so behaviour matches that policy — **without** treating it as a bugfix to KB-S53/KB-S54.

---

## 3. Current behaviour — how `primary_concern` is selected today

### 3.1 `report_v1.top_findings` ordering

**File / function:** `backend/core/analytics/report_compiler_v1.py` — `compile_report_v1`.

**Logic:** All `signal_results` rows are sorted with key:

1. **Descending** coarse state severity (`_STATE_RANK`: `at_risk` > `suboptimal` > `optimal` > `unknown`).
2. **Descending** numeric `confidence`.
3. **Ascending** `signal_id` (string) — **tie-break**.

**Output:** `top_findings` is that order with `priority_rank = 1, 2, …` (`ReportTopFindingV1` in `backend/core/contracts/report_v1.py`).

**Downstream:** `compile_clinician_report_v1` **does not re-rank**; it consumes the payload as given.

### 3.2 Clinician headline and narrative

**File / function:** `backend/core/analytics/report_compiler_v1.py` — `compile_clinician_report_v1`.

| Step | Behaviour |
|------|-----------|
| Primary row | `primary = top_findings[0]` if non-empty, else `{}`. |
| `primary_concern` | Single string: `{primary_signal_id} ({primary_state})` or fallback copy. |
| Root-cause block | **One** `RootCauseFindingV1`: first `root_cause_v1.findings` row whose `signal_id` matches **primary** (`next(...)`). |
| Top hypothesis | **First** hypothesis of **that** root-cause finding (`hypotheses[0]`). |
| Confirmatory section | Derived from **primary** root-cause finding + suppression logic. |
| Data quality | Uses **all** `top_findings` for metric set / caveats, but **headline** remains singular. |

**Contract:** `backend/core/contracts/clinician_report_v1.py` — `Page1SummaryBlockV1.primary_concern` is a **required** `str` (max 160); no parallel “secondary concerns” or “ambiguity” field.

### 3.3 Other uses of ranking / primary

- **`insight_graph`:** `report_v1` is embedded post-`compile_report_v1` in `insight_graph_builder.py`; arbitration / `primary_driver_system_id` are **system-burden / graph** concepts — **not** the same as report `top_findings[0]` (KB-S54 addressed burden keys; KB-S54B is report-headline policy).
- **Tests:** `backend/tests/unit/test_report_compiler_v1.py` asserts ordering (e.g. `at_risk` before `suboptimal`). `test_clinician_report_runtime_alignment.py` asserts `primary_concern` non-empty.

---

## 4. Existing governed building blocks (ambiguity / confidence)

| Building block | Location / role | Supports ranked ambiguity? |
|----------------|-----------------|----------------------------|
| **Ordered `top_findings`** | `ReportV1` | **Yes (partial):** full ranked list with `priority_rank`, `confidence`, `confidence_reasons`, `supporting_markers`, `why_it_matters`. |
| **Multi finding root cause** | `RootCauseV1.findings: List[RootCauseFindingV1]` | **Yes (partial):** multiple signals can have root-cause payloads; clinician compiler **surfaces one** aligned to primary. |
| **Multi-hypothesis per signal** | `HypothesisV1` list + `evidence_for` / `evidence_against` / `missing_data` | **Yes:** within-one-signal ambiguity; not cross-signal “co-primary” in headline. |
| **Confirmatory tests + suppression** | `compile_clinician_report_v1` + `_collect_confirmatory_with_suppression` | **Partial:** affects **primary** path only today. |
| **Interaction chains / summary** | `top_chains` in `ReportV1`; clinician uses **first two** chain lines | **Partial:** secondary narrative, not formal “ranked concerns.” |
| **Signal-level confidence** | `signal_results` / `ReportTopFindingV1.confidence` | **Yes:** already input to sort; policy could redefine **how** it combines with ties. |
| **Singular clinician headline** | `Page1SummaryBlockV1` | **No:** blocks multi-concern headline without contract change. |
| **FE rendering** | `ClinicianReportRenderer.tsx` — one “Primary concern” line | **No:** assumes single string. |

**Absent (today):** explicit **ambiguity label** (e.g. “competing interpretations”), **co-primary** slots, **policy version / rationale stamp** on report for ranking, and **UI** for multiple ranked concerns on page 1.

---

## 5. Contract impact

| Contract | Change needed for multi–primary / ranked ambiguity? |
|----------|-----------------------------------------------------|
| **`ReportV1` / `ReportTopFindingV1`** | Possibly **extend** (e.g. `tie_group`, `ambiguity_class`, or explicit `display_tier`) — not strictly required if policy only changes **sort** and keeps one headline (narrowest sprint). |
| **`ClinicianReportV1` / `Page1SummaryBlockV1`** | **Likely required** if product wants **more than one** foreground concern or an **explicit ambiguity** string: new fields or structured list; `extra="forbid"` forces versioned schema change. |
| **`RootCauseV1`** | **Optional:** already multi-finding; clinician **selection logic** may change without schema change if still emitting one block — or **multiple** sections if product requires. |
| **Frontend `ClinicianReportV1` type + renderer** | **Likely required** for any new page-1 fields. |
| **AB/VR `clinician_report_v1_*.json`** | **Required** if compiler output shape or headline policy changes acceptance snapshots. |

**Conclusion:** If the strategic direction is **only** “better tie-break, still one headline” → **runtime-only** bounded change is conceivable. If the direction is **true ranked ambiguity** (multiple plausible leads) → **contracts + FE + fixtures** are in play — **not** `PURE_POLICY_TRANSLATION`.

---

## 6. Policy vs implementation boundary

| Policy layer (must be decided explicitly) | Implementation layer (then coded) |
|----------------------------------------|-------------------------------------|
| When to show **one** vs **more than one** foreground concern | `compile_report_v1` sort and/or post-sort **tiers** |
| How **ties** are broken (replace lexicographic `signal_id`?) | Sort key / stable tie pipeline |
| Whether **confidence** is **only** sort input or also **display** (e.g. “jointly plausible”) | Copy templates in `compile_clinician_report_v1` |
| How **missing markers / confirmatory** affect **rank** vs **wording only** | Interaction with root-cause and suppression |
| **Contradiction** handling in ranking (if any) | May touch signal / interaction layers — **careful scope** |
| **Versioning** of ranking policy for replay | `ReportMetaV1` or new stamp fields |

**Do not blur:** KB-S54B is **not** KB-S54 (burden coherence) and **not** KB-S53 (harness); ranking-policy work must **not** be smuggled in as bugfixes.

---

## 7. Bounded change assessment (future sprint in-scope / out-of-scope)

| Area | In-scope likelihood | Notes |
|------|---------------------|--------|
| **`compile_report_v1`** | **High** | Single authority for `top_findings` order. |
| **`compile_clinician_report_v1`** | **High** | Headline and root-cause **selection** logic. |
| **Root-cause compiler content** | **Medium** | Only if policy ties hypothesis ranking to new rules. |
| **Contracts / DTOs** | **Medium–high** | Required for multi-concern or ambiguity **surface**. |
| **FE** | **Medium–high** | Required if UX shows multiple concerns or ambiguity. |
| **AB/VR fixtures + harness docs** | **High** | Any change to deterministic clinician/report snapshots. |
| **SSOT signal packages** | **Low** unless policy requires new signal metadata for ranking. |
| **System burden / arbitration** | **Out of scope** unless explicitly linking “driver” to “headline” (risky coupling). |

---

## 8. Recommendation

### **`SPLIT_INTO_PHASED_SEQUENCE`**

**Rationale:** The strategic direction (“ranked ambiguity / confidence-weighted interpretation”) almost certainly touches **policy text**, **runtime ordering + selection**, **clinician contract**, **golden fixtures**, and **UI**. Doing all in one undifferentiated sprint increases regression risk and blurs governance. A **pure documentation** sprint alone does **not** change behaviour — so **`PROCEED_AS_PURE_POLICY_TRANSLATION`** is **insufficient** if the goal is user-visible change.

**Proposed phases (grounded, minimal):**

1. **Policy / governance phase** — Authoritative policy doc: tie rules, multi-concern rules, confidence display rules, versioning; explicit **non-goals** (e.g. no silent `signal_id` tie-break without stamp).
2. **Runtime + contract phase (bounded)** — Implement policy in `report_compiler_v1` / `compile_clinician_report_v1`; extend **`ClinicianReportV1`** only as needed; add replay/policy stamp if required.
3. **Fixture + harness phase** — Regenerate or add AB/VR expected JSON; extend tests (similar to KB-S54 burden contract tests).
4. **Frontend phase** — Types + `ClinicianReportRenderer` (and any results page assumptions).

**Alternative:** If product scope is **narrow** (“replace `signal_id` tie-break with one deterministic clinical rule, still one headline”), a single sprint could be framed as **`PROCEED_AS_POLICY_TRANSLATION_PLUS_BOUNDED_RUNTIME_CHANGE`** with **explicit** “no contract / no FE change” boundary — but that is **not** full “ranked ambiguity” as commonly interpreted.

---

## 9. References (repo)

- `docs/investigations/VR_PRIMARY_CONCERN_RANKING_INVESTIGATION.md`
- `docs/investigations/KB-S53_VR_FIXTURE_OPERATOR_REVIEW.md`
- `docs/investigations/KB-S53_AB_VR_ACCEPTANCE_HARNESS.md` (operator acceptance)
- `backend/core/analytics/report_compiler_v1.py` (`compile_report_v1`, `compile_clinician_report_v1`)
- `backend/core/contracts/report_v1.py`, `clinician_report_v1.py`, `root_cause_v1.py`
- `frontend/app/components/results/ClinicianReportRenderer.tsx`, `frontend/app/types/analysis.ts`
