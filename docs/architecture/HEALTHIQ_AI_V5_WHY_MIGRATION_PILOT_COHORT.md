# HealthIQ AI v5 — WHY Migration Pilot Cohort

**Work ID:** `ARCH-CONV-GATE0`  
**Branch:** `feature/arch-conv-gate0-cohort-viability`  
**Baseline HEAD:** `d798beab9b2bb7dcad9b48ed0f0a4f0153be8948`  
**Status:** PROPOSED — awaiting human ratification  
**Does not authorise:** estate-wide WHY migration, Package 3 implementation, or medical-content promotion

---

## 1. Purpose

Define a bounded, representative Package 3 WHY convergence pilot that is large enough to prove architecture, and small enough to remain medically and operationally executable.

This pilot deliberately does **not** default to all **40** legacy hypothesis YAML assets.

---

## 2. Exact pilot cohort

| # | signal_id | activation frames (LIVE) | current WHY authority | canonical research availability | existing medical review | new medical review required | migration complexity | reason for inclusion |
|---|---|---|---|---|---|---|---|---|
| 1 | signal_vitamin_d_low | 1 (`…::inv_vitamin_d_low_deficiency`) | **compiled** runtime-promoted (`RUNTIME_PROMOTED_COMPILED_SIGNAL_IDS`); legacy YAML still on disk / registry row remains | Yes — package + compiled artefact + inv lineage | Existing architecture pilot; content already compiled | **Confirm retirement** of legacy path for this signal (process review, not full rewrite) | Low–medium — prove mutual exclusion + legacy retirement without dual authority | Anchor: only current compiled path; proves retirement/replay |
| 2 | signal_homocysteine_high | 3 (kb52c B-vitamin; s24 metabolic; kb52c renal) | **legacy** `hcy_hypotheses_v1.yaml` (also shared with `signal_homocysteine_elevation_context`) | Yes — multi-frame packages + legacy hypotheses | Wave 1 / MED-REV visibility history; not a compiled-WHY medical sign-off | **Yes** — new compiled hypothesis content + frame/evidence limits | High — multi-frame + shared YAML + CV lead path | Multi-frame; consumer lead hint; clinician WHY surface |
| 3 | signal_mcv_high | 3 (s24 macrocytosis; kb52c megaloblastic; kb52c nonmegaloblastic) | **legacy** `mcv_high_hypotheses_v1.yaml` | Yes | Partial historical haematology MR blockers in BUILD register; not compiled-WHY sign-off | **Yes** | High — multi-frame differential | Multi-frame; narrative lead hint; tests frame-aware WHY |
| 4 | signal_free_t3_low | 1 (`pkg_kb47_…low_t3_syndrome`) | **legacy** `free_t3_low_hypotheses_v1.yaml` | Yes — Batch_2_Pass_3.json + research_brief sources | Research brief present; no Gate 0-confirmed compiled-WHY MR owner | **Yes** — after Package 2 lineage attach for beta claim honesty | Medium — single-frame but provenance-BLOCKED package + Wave 1 thyroid + lead hint | Single-frame; Wave 1; provenance-adjacent; consumer lead |
| 5 | signal_tpo_ab_high | 2 (autoimmune hypothyroid; euthyroid autoimmune risk) | **legacy** `tpo_ab_high_hypotheses_v1.yaml` | Yes — kb59 packages | Partial thyroid programme history | **Yes** | Medium–high — multi-frame thyroid autoimmune | Multi-frame Wave 1 thyroid without kb47 BLOCKED class |

**Pilot size:** **5 signal families**, **10 activation frames** (1+3+3+1+2).

---

## 3. Architecture coverage matrix

| Required pilot dimension | Covered by | Evidence |
|---|---|---|
| Single-frame signal | vitamin_d_low; free_t3_low | registry frame counts |
| Multi-frame signal | homocysteine_high; mcv_high; tpo_ab_high | registry frame counts |
| Current compiled authority path | vitamin_d_low | `compiled_hypothesis.py` |
| Current legacy authority path | items 2–5 | `root_cause_registry_v1.py` + YAML assets |
| Consumer output path | lead hints include homocysteine_high, mcv_high, free_t3_low | `narrative_report_compiler_v1.py` `_LEAD_SIGNAL_HINTS` |
| Clinician / root-cause emission | all five are registry targets or compiled | compiler branching |
| Provenance + replay | vitamin_d (eligible); free_t3_low (BLOCKED until Package 2) | inventory + Batch_2_Pass_3.json |
| Medical-review workflow | required for items 2–5; confirmation for item 1 retirement | see §5 |
| Legacy retirement | vitamin_d_low first; then one legacy→compiled promotion | planning paper Package 3B |

---

## 4. Selection rationale

1. **Bounded:** 5 families / 10 frames vs 40 YAML / 41 registry targets.
2. **Representative:** mixes compiled vs legacy, single vs multi-frame, Wave 1 thyroid/CV/haematology adjacency.
3. **Launch-relevant:** intersects narrative lead hints and Wave 1 thyroid.
4. **Does not smuggle Package 2 into Package 3:** free_t3_low is included for WHY content coverage, but provenance attach remains Package 2; Package 3 must not invent lineage.
5. **Avoids androgen panel:** already context/MR blocked (BATCH2-MEDREVIEW-1); poor pilot choice until context gates close.

---

## 5. Medical-review dependencies

| Dependency | Status |
|---|---|
| Named medical-review owner for this pilot | **UNRESOLVED** — not evidenced in required Gate 0 inputs |
| Review inputs | Compiled/legacy hypothesis artefacts; activation-frame identity; evidence limits; non-diagnostic framing; consumer/clinician emission samples |
| Review output format | Precedents exist (`BATCH2-MEDREVIEW-1_*`, `MED-REV-1_*`, `MED-REV-2_*`) — reuse governed review artefact pattern; do not invent a new clinical standard here |
| Expected decision route | Engineering completes Package 3A machinery → medical review signs content/frame/limits → Package 3B activates only approved pilot rows → legacy retirement proof |
| Capacity within programme window | **UNRESOLVED** — see viability assessment |
| Safe reduction if MR capacity missing | Reduce Package 3B to **vitamin_d_low legacy-retirement proof only** (architecture proof without new content migration) |

---

## 6. Exclusions

| Excluded | Why |
|---|---|
| Remaining ~35 legacy hypothesis YAML assets | Out of bound; estate-wide migration is a kill-risk |
| Androgen panel signals | Context/MR incomplete; not Wave 1 architecture pilot |
| egfr_low | No root-cause registry target today — provenance/identity yes, WHY pilot no |
| PSI / prose library depth | Separate programme; not WHY authority migration |
| Dual-path content rewrite of vitamin_d | Already compiled; pilot is retirement/replay, not re-authoring |

---

## 7. Pilot success criteria

- [ ] Compiled and legacy paths remain mutually exclusive per signal_id for pilot rows.
- [ ] For vitamin_d_low: legacy authority can be retired (or proven non-reachable) without dual emission.
- [ ] At least one multi-frame legacy signal demonstrates frame-preserving WHY selection (no silent frame collapse in pilot consumers).
- [ ] Consumer and clinician surfaces for pilot rows remain deterministic under identical inputs.
- [ ] Provenance for free_t3_low is honest (lineage attached **or** explicit non-beta claim) before any beta-facing WHY claim.
- [ ] Medical-review decisions recorded as artefacts for every newly compiled pilot row.
- [ ] No expansion to all 40 legacy assets without a new Gate.

---

## 8. Quantitative totals

| Item | Count |
|---|---:|
| Proposed WHY pilot signals | **5** |
| Proposed WHY pilot activation frames | **10** |
| Medical reviews required (new content) | **4** (items 2–5) + **1 confirmation** (item 1 retirement) |
| Legacy YAML intentionally excluded | **35** (40 − vitamin_d asset retained for retirement proof until closed) |
