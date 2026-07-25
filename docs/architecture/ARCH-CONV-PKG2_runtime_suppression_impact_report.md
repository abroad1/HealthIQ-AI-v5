# ARCH-CONV-PKG2 — Runtime Suppression Impact Report

**Work ID:** `ARCH-CONV-PKG2`  
**Branch:** `feature/arch-conv-pkg2-provenance-reachability`  
**Baseline HEAD:** `d696fca3ba5483ae59d547a55a817c9284b2e981`  
**Human approval basis:** Gate 0 merged dispositions (INCLUDE / DEFER / EXCLUDE_FROM_BETA + medical-review)

---

## 1. Scope of suppression

| Slice | Count | Runtime effect |
|---|---:|---|
| Wave 1 INCLUDE (thyroid free_t3/t4 + egfr×2) | 6 | Remain production-reachable after lineage attach |
| Androgen kb47 | 8 | Non-reachable in production registry |
| CK / eosinophil kb47 | 6 | Non-reachable in production registry |
| Package directories deleted | 0 | Assets retained; test opt-in still loads |

---

## 2. Golden / representative panels reviewed

### `backend/tests/fixtures/golden_panel_160.json`

| Check | Result | Classification |
|---|---|---|
| Biomarkers present for androgen/CK | Yes (`dhea`, `fai`, `free_testosterone`, `creatine_kinase`) | Context |
| Biomarkers present for eosinophils / egfr | No | Context |
| Direct `SignalEvaluator` fire differential (prod vs opt-in) on fixture values | No kb47 androgen/CK/thyroid/egfr frames fired in either mode (lab-range / gate constrained) | **Intended / no user-visible delta on this fixture** |
| Full `run_golden_panel` blob mentions of `signal_dhea_high` / `signal_creatine_kinase_high` / `pkg_kb47_*` as active results | No active excluded-signal findings observed | **Intended** |
| Biomarker name strings (e.g. `free_testosterone`) in payload/meta | May appear as inputs, not as suppressed signal findings | Not a regression |

### Forced biomarker stress (not golden values)

| Mode | `creatine_kinase=500` | Classification |
|---|---|---|
| Production registry | `signal_creatine_kinase_high` **does not fire** | **Intended** (Gate 0 DEFER → MAKE_NON_REACHABLE) |
| Test opt-in registry | `signal_creatine_kinase_high` **can fire** | **Intended** (fixtures retained) |

### `golden_panel_sprint14_2_thyroid_immune_mini.json`

| Check | Result |
|---|---|
| Excluded androgen/CK/eos signal ids in narrative/IDL/scores | Not observed |
| Wave 1 thyroid markers as biomarkers | Present (not removed) |

---

## 3. Product / medical impact of non-reachability

| Family | Wave 1 reliance | Product impact | Medical impact | Approval |
|---|---|---|---|---|
| Androgen (8) | Not Wave 1 INCLUDE | Removes previously loadable androgen kb47 frames from production path | Context/MR still open; not claimed for controlled beta | Gate 0 EXCLUDE_FROM_BETA / medical-review |
| CK (2) | Not Wave 1 INCLUDE | Removes dual CK frames from production path | Deferred cohort | Gate 0 DEFER |
| Eosinophils (4) | Not Wave 1 INCLUDE | Removes eos frames from production path | Deferred cohort | Gate 0 DEFER |
| Wave 1 thyroid + egfr (6) | Relied upon | **None** — kept reachable with EXPLICIT_SPEC | Lineage recovered from Pass 3; no medical reinterpretation | Gate 0 INCLUDE |

No Wave 1 finding was removed.

---

## 4. Unintended / unresolved regressions

| Item | Status |
|---|---|
| Unexplained clinical regression on golden_panel_160 for suppressed families | None observed |
| Estate-wide package regen side effects | None (kb47-only policy) |
| WHY / prose / PSI / Gemini / threshold changes | Out of scope; not changed |

---

## 5. Approval summary

Intended removal of user-visible production reachability for the 14 non–Wave-1 kb47 packages is authorised by **Gate 0 merged cohort dispositions**. STOP Gate 1 (Package 2) passed because Wave 1 packages were not proposed for suppression.

Replay / report honesty: reachable Wave 1 results carry `provenance_status=EXPLICIT_SPEC` and `activation_key=signal_id::source_spec_id`. Exclusions remain auditable via `SignalRegistry.excluded_launch_critical_packages`.
