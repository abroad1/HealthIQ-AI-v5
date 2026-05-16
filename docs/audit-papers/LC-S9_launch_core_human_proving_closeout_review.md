# LC-S9 — Launch-Core Human Proving Closeout Review

**work_id:** LC-S9  
**branch (work package):** `launch-core/lc-s9-human-proving-closeout-review`  
**date:** 2026-05-16  
**classification:** STANDARD-risk CONTENT — audit / decision artefact only  
**auditor role:** Cursor investigation and draft (not programme authority)

---

## 1. Executive verdict

LC-S8D and FE-S8E have **successfully remediated the unit-governance and Layer C presentation blocker** on the mixed-unit LC-S8D sentinel fixture. Post-merge human UAT shows stable API/UI behaviour with no regressions on that fixture (`e4dc8e59-2588-4943-b37b-a299c89f9442` vs `a817efa9-f915-4309-8b25-51c44cf98d62` — identical analytical and upload payloads).

**Full Sprint 5 launch-core human proving** as defined in [`healthiq_launch_core_transformation_plan_FINAL.md`](../planning-papers/healthiq_launch_core_transformation_plan_FINAL.md) (AB/VR panels, contrasting questionnaire profiles, visible lifestyle and medication payoff, fresh harness evidence, governed WHY on the bounded biology slice, coherence across surfaces) **is not yet closed**.

| Decision | Verdict |
|----------|---------|
| Position in launch-core plan | **B — Between Sprint 5 and Sprint 6** |
| Sprint 5 closeout | **SPRINT_5_PASS_WITH_GAPS** |
| Unit-governance remediation track | **Passed** (fixture-scoped) |
| Recommended next work package | **B — Targeted correction sprint before Sprint 6** (proposed ID: **LC-S9B** or programme-assigned WHY/proving closure sprint) |

Cursor does **not** certify programme closure, Sprint 6 authorisation, or merge readiness.

---

## 2. Evidence reviewed

### 2.1 Governing and audit artefacts

| Artefact | Status | Notes |
|----------|--------|-------|
| [`docs/planning-papers/healthiq_launch_core_transformation_plan_FINAL.md`](../planning-papers/healthiq_launch_core_transformation_plan_FINAL.md) | **Present** | Sprint 5/6 definitions; launch-core slice criteria (§ “What the launch-core slice must prove”; Sprint 5 §421–445; Sprint 6 §449–473) |
| [`docs/audit-papers/LC-S8C_ssot_wide_unit_governance_preflight.md`](LC-S8C_ssot_wide_unit_governance_preflight.md) | **Present** | Pre-remediation baseline and Phase B evidence gate |
| [`docs/audit-papers/LC-S8D_uk_si_unit_governance_remediation_notes.md`](LC-S8D_uk_si_unit_governance_remediation_notes.md) | **Present** | Phases A/C/D/E complete; Phase B blocked; Sentinel `lc_s8d_unit_governance_v1` |
| [`docs/audit-papers/LC-S8D_frontend_layer_c_uat_report.md`](LC-S8D_frontend_layer_c_uat_report.md) | **Present** | Pre–FE-S8E: Mode A UI missing; superseded for UI by FE-S8E |
| [`docs/audit-papers/FE-S8E_uploaded_panel_fidelity_uat_notes.md`](FE-S8E_uploaded_panel_fidelity_uat_notes.md) | **Present** | Mode A implementation and browser UAT |
| [`docs/audit-papers/FE-S8E_post_merge_comparison_uat.md`](FE-S8E_post_merge_comparison_uat.md) | **Present** | Post-merge stability; identical payloads on same fixture |
| [`docs/audit-papers/launch-core-proving/PROVING_REPORT.md`](launch-core-proving/PROVING_REPORT.md) | **Present — STALE** | Stamp `20260512T204616Z`; git SHA `a87df29` (WP2-era) |
| [`docs/audit-papers/launch-core-proving/latest_fingerprints.json`](launch-core-proving/latest_fingerprints.json) | **Present — STALE** | `git_short_sha`: `a87df29`; predates LC-S8D/FE-S8E merges |
| [`docs/audit-papers/lc_s5_proving_readiness_preflight_audit.md`](lc_s5_proving_readiness_preflight_audit.md) | **Present** | CHECK 2/4/5/6 partial; human walkthrough not done; harness must be re-run |
| [`docs/audit-papers/LAUNCH_GRADE_ANALYTICAL_GAP_MAP_2026-05.md`](LAUNCH_GRADE_ANALYTICAL_GAP_MAP_2026-05.md) | **Present** (cross-check) | May 2026 baseline on coherence, lifestyle visibility, fallback depth |
| `automation_bus/latest_audit_summary.md` | **Missing** | Not in repo at review time; no findings inferred from it |

LC-S9 did **not** run `launch_core_proving_harness.py` (out of scope for docs-only package). Stale harness artefacts are treated as **missing post–LC-S8D/FE-S8E evidence**, not as pass.

### 2.2 Git state at review time

Recorded on **2026-05-16** (review execution environment):

```text
git branch --show-current
main

git status --short
 M frontend/.env.local.example
?? docs/audit-papers/FE-S8E_post_merge_comparison_uat.md

git log --oneline -n 5
dfba562 chore(bus): FE-S8E kernel COMPLETE status
4dd2634 chore(bus): FE-S8E kernel IN_PROGRESS status
ffcfded docs: FE-S8E uploaded-panel fidelity UAT notes
9477d5e feat(frontend): FE-S8E Layer C Mode A uploaded-panel fidelity rendering
851f889 chore(bus): FE-S8E work package definition and LC-S8D UAT authority doc

git diff --name-only  (before LC-S9 file write)
frontend/.env.local.example
```

**Note:** Work package specified branch `launch-core/lc-s9-human-proving-closeout-review`; review ran on `main`. Uncommitted `frontend/.env.local.example` and untracked `FE-S8E_post_merge_comparison_uat.md` do not affect this docs-only decision artefact. LC-S9 adds only the file named in § Acceptance criteria.

---

## 3. Current position in the launch-core plan

**Verdict: B — Between Sprint 5 and Sprint 6**

| Option | Assessment |
|--------|------------|
| A. Still inside Sprint 5 human proving | **Partially** — proving activity occurred (LC-S8D fixture UAT, FE-S8E merge) but not the full Sprint 5 matrix |
| B. Between Sprint 5 and Sprint 6 | **Yes** — unit blocker cleared; Sprint 5 acceptance criteria not fully met |
| C. Ready to enter Sprint 6 protection | **No** — for the **whole** launch-core slice; scoped Sprint 6 for unit governance only is appropriate |
| D. Blocked — another correction sprint | **Partially** — targeted correction needed before declaring Sprint 5 closed; not a full programme reset |

The programme has exited **infrastructure-rescue mode for unit governance** on the LC-S8D sentinel fixture. It has **not** completed the transformation plan’s Sprint 5 human proving bar (AB/VR, questionnaire contrast, visible personalisation payoff, fresh harness, named human sign-off).

---

## 4. What recent LC-S8D / FE-S8E work proved

Evidence: [`LC-S8D_uk_si_unit_governance_remediation_notes.md`](LC-S8D_uk_si_unit_governance_remediation_notes.md), [`FE-S8E_uploaded_panel_fidelity_uat_notes.md`](FE-S8E_uploaded_panel_fidelity_uat_notes.md), [`FE-S8E_post_merge_comparison_uat.md`](FE-S8E_post_merge_comparison_uat.md), [`LC-S8D_frontend_layer_c_uat_report.md`](LC-S8D_frontend_layer_c_uat_report.md) (historical pre-FE-S8E gap).

### 4.1 Proven on the mixed-unit LC-S8D sentinel fixture

| Claim | Evidence status |
|-------|-----------------|
| UK/SI unit governance for tested mixed-unit panel | **Proven** — canonical Layer B units; equivalence (K/uL ↔ 10^9/L, mEq/L ↔ mmol/L); strict conversions for glucose, lipids, creatinine, HbA1c, haematocrit |
| Layer B canonicalisation (HbA1c mmol/mol, haematocrit L/L, counts, electrolytes, glucose/lipids/creatinine, BUN→urea) | **Proven** on fixture |
| Phase B blocked-marker safety (Ca, Mg, free T4, Hb, urate passthrough) | **Proven** — no silent mis-conversion on reviewed markers |
| Layer C Mode A uploaded-panel fidelity | **Proven** (post–FE-S8E) — `Uploaded panel values` UI; HbA1c % equivalent row; upload K/uL, mEq/L, % preserved |
| Layer C Mode B analytical collapse | **Proven** — single HbA1c in `biomarkers[]`; no `0.438 %` haematocrit; urea separate from urate |
| Frontend renderer-only | **Proven** — `uploadPanelFidelity.ts` displays API values; no conversion constants in new paths |
| Reproducibility | **Proven on same fixture** — two analysis IDs, identical biomarker/upload payloads |
| API health | **Proven** — `/results` loads; `GET /api/analysis/result` 200; `clinician_report_v1` and meta fields present |

### 4.2 Explicitly not proven by LC-S8D / FE-S8E alone

- AB/VR launch-core panels end-to-end in **current** build (harness stale).
- Two contrasting questionnaire profiles changing user-visible fields.
- Visible lifestyle and statin payoff on consumer surfaces (see §5).
- Full launch-core WHY coverage and fallback quality on all leads under test.
- Programme-wide regression protection for launch-core proving matrix (harness/CHECK automation incomplete).

---

## 5. What remains unproven

Per [`healthiq_launch_core_transformation_plan_FINAL.md`](../planning-papers/healthiq_launch_core_transformation_plan_FINAL.md) and [`lc_s5_proving_readiness_preflight_audit.md`](lc_s5_proving_readiness_preflight_audit.md):

| Sprint 5 criterion | Status | Grounding |
|--------------------|--------|-----------|
| AB, VR, and additional representative panels tested (current build) | **Unproven post–LC-S8D** | [`PROVING_REPORT.md`](launch-core-proving/PROVING_REPORT.md) / [`latest_fingerprints.json`](launch-core-proving/latest_fingerprints.json) stale at SHA `a87df29` |
| Multiple contrasting questionnaire profiles | **Unproven** | No fresh human UAT or harness diff documenting user-visible field changes |
| Medication/drug modifier tested with **visible** payoff | **Partially evidenced** | Stale harness: statin intervention present/absent **PASS**; narrative body differs **False** for AB/VR statin-off vs statin-on ([`PROVING_REPORT.md`](launch-core-proving/PROVING_REPORT.md) § analytical invariants) |
| Alcohol/lifestyle bridge in user-readable language | **Partially evidenced** | Harness: lifestyle_context `narrative block differs=True`; CHECK 2 not automated; no LC-S9 browser sign-off on AB/VR lifestyle run |
| Governed WHY for launch-core lead findings | **Partially evidenced** | Stale harness: homocysteine lead with hypothesis line on AB; mixed-unit UAT: hero **“No governed WHY for signal_renal_metabolic_stress”** on different panel |
| Honest fallback where WHY absent | **Partially evidenced** | Fallback is **visible** but **weak** on renal-metabolic-stress hero (clinical trust gap on that path) |
| Legacy `insights[]` removed/gated on launch-core path | **Evidenced in prior sprint** | LC-S4 / lc_s5 cite gating; **not re-tested in LC-S9** |
| Mock-mode honesty | **Evidenced in prior sprint** | LC-S4 / lc_s5; **not re-tested in LC-S9** |
| IDL consumer surfacing decision | **Unproven / thin** | Stale harness: IDL titles empty strings; gap map notes depth unverified |
| Coherent UX (hero, overview, domains, clinician, PDF) | **Partial** | Mixed-unit UAT only; trust-strip DQ copy wrong for panel size |
| Reproducibility (launch-core matrix) | **Unproven** | Reproduced only on LC-S8D sentinel fixture |
| Regression/Sentinel protection for launch-core slice | **Partial** | Unit: `test_lc_s8d_unit_governance_sentinel.py` per LC-S8D notes; launch-core CHECK 2/5/6 and fresh fingerprints **not** done |

---

## 6. Known issues classification

### 6.1 “No governed WHY for signal_renal_metabolic_stress”

**Classification: TARGETED CORRECTION BEFORE SPRINT 6** (for launch-core clinical trust; not a unit-governance defect)

| Context | Assessment |
|---------|------------|
| LC-S8D mixed-unit fixture (`e4dc8e59…`) | Hero shows explicit ungoverned-WHY fallback — **honest** but **undermines trust** on that analysis path |
| AB/VR launch-core proving slice (homocysteine lead) | Stale harness shows governed-style homocysteine lead copy and top hypothesis line — **do not conflate** with renal-metabolic-stress hero on unit fixture |
| Blocks LC-S8D/FE-S8E unit merge retroactively | **No** |
| Blocks declaring Sprint 5 closed on full plan bar | **Yes** — if launch-core leads can surface without acceptable WHY or fallback copy |

### 6.2 Polish issues (from UAT)

| Issue | Classification | Blocks Sprint 5? | Blocks Sprint 6? |
|-------|----------------|------------------|------------------|
| Trust strip “We received 3 of 3 expected markers” on 24-marker panel | **POLISH** (consider **FOLLOW-UP BEFORE EXTERNAL TESTING** for commercial demo) | No | No |
| `white_blood_cells` dial label | **POLISH** — FE-S8E added display name per implementation notes; pre–FE-S8E UAT reported slug | No | No |
| `remnant_cholesterol` unscored / empty policy bounds | **NOT A DEFECT** — explicit “Not scored - no compatible policy bounds” | No | No |

---

## 7. Sprint 5 closeout decision

**Verdict: SPRINT_5_PASS_WITH_GAPS**

### 7.1 What Sprint 5 can claim as passed

- Unit-governance remediation (LC-S8C → LC-S8D → FE-S8E) on the **defined mixed-unit sentinel fixture**.
- Layer C Mode A/B behaviour on `/results` in current frontend build (per FE-S8E UAT and post-merge comparison).
- No regression observed on that fixture between pre- and post-merge analysis IDs.

### 7.2 What must still be proven for full Sprint 5 PASS

1. **Fresh** `launch_core_proving_harness` run on current `main` (post–LC-S8D/FE-S8E) and updated `latest_fingerprints.json` / `PROVING_REPORT.md`.
2. **Named human walkthrough** on AB/VR × (baseline, lifestyle_context, statin_off, statin_on) per lc_s5 checklist — traceable reviewer ownership.
3. **Binary CHECK 2, 5, 6** (and CHECK 4 confirmation) per lc_s5 §5 — not fully automated today.
4. **Visible** lifestyle and statin payoff on consumer surfaces (not only backend intervention flags or harness metadata).
5. **Governed WHY or acceptable fallback** on all launch-core lead findings exercised in the proving matrix.
6. **Coherence sign-off** across hero, body overview, domain cards, clinician report (and PDF/export if in launch-core surface scope).

Until these are evidenced, Sprint 5 cannot be closed as **SPRINT_5_PASS** without qualification.

---

## 8. Sprint 6 protection target

Sprint 6 is **appropriate in scoped form** but must not be treated as protection of the entire launch-core programme until §7.2 is addressed.

### 8.1 Protect now (LC-S8D + FE-S8E)

| Behaviour | Suggested protection |
|-----------|---------------------|
| Layer B canonical units and equivalence | `backend/tests/regression/test_lc_s8d_unit_governance_sentinel.py`; Sentinel pack `lc_s8d_unit_governance_v1` |
| HbA1c single analytical identity; haematocrit L/L; BUN→urea | Same sentinel + `test_hba1c_governance.py` |
| Frontend no unit repair | Sentinel `frontend_no_unit_repair`; FE-S8E scan discipline |
| Mode A uploaded-panel fidelity | `frontend/tests/lib/uploadPanelFidelity.test.ts`; contract via `meta.upload_panel_observations` |
| Mode B analytical dials from `biomarkers[]` only | FE integration tests / manual UAT checklist item |

### 8.2 Protect after fresh harness run

| Behaviour | Suggested protection |
|-----------|---------------------|
| AB/VR lead-finding order and homocysteine-led narrative | Fingerprint diff vs new golden; optional pytest on fingerprint JSON |
| Statin intervention isolation (analytical invariants) | Harness invariant checks (already in harness; refresh + CI) |
| Lifestyle narrative delta when lifestyle fixture active | CHECK 2 binary assertion |
| Band/headline consistency | CHECK 5 |
| primary_concern ↔ retail_summary same lead | CHECK 6 |

### 8.3 Defer (not Sprint 6 launch-core minimum)

- Full WHY Wave 2 across signal estate.
- Broad medication ontology beyond statin architecture proof.
- Phase B true conversions (Ca, Mg, free T4, Hb) — remains **parked** per LC-S8D Phase B block unless evidence pack approved.

---

## 9. Recommended next work package

**Choice: B — Targeted correction sprint before Sprint 6**

| Field | Value |
|-------|--------|
| Proposed work ID | **LC-S9B** (or programme-assigned equivalent, e.g. LC-S5B-proving-closeout) |
| Purpose | Close remaining Sprint 5 trust and evidence gaps: refresh launch-core proving harness and fingerprints; complete named human walkthrough on AB/VR questionnaire matrix; add CHECK 2/5/6 automation; improve governed WHY or governed fallback for active lead findings (including unacceptable raw fallback strings on hero); then authorise full Sprint 6 protection. |

**Parallel option (if programme wants split tracks):**

- **A — Sprint 6 (narrow):** Lock LC-S8D/FE-S8E unit and Mode A/B behaviours only.
- **C — Additional human proving sprint:** AB/VR matrix walkthrough while WHY/copy fixes land.

**Not recommended as next primary blocker:**

- **D — Phase B unit evidence pack** — explicitly parked unless product reverses LC-S8D Phase B policy.
- **E — Launch-core gate reopening** — not warranted; Pre-Sprint 1 decisions stand; execution evidence is incomplete, not void.

---

## 10. Blockers and deferred items

### 10.1 Blockers (programme level)

| Blocker | Severity | Notes |
|---------|----------|-------|
| Stale launch-core proving fingerprints | **High** for Sprint 5 closeout | Cannot claim AB/VR behaviour on current build |
| Incomplete Sprint 5 human walkthrough | **High** | lc_s5: “Human validation walkthrough executed — NOT DONE” |
| Visible statin/lifestyle payoff unproven on UI | **Medium–High** | Architecture exists; consumer-visible delta not demonstrated |
| Weak/unacceptable WHY fallback on some lead paths | **Medium** | TARGETED CORRECTION — especially if similar leads appear on AB/VR in fresh runs |

### 10.2 Deferred (explicitly parked)

| Item | Owner track |
|------|-------------|
| Phase B conversions (Ca, Mg, free T4, Hb) | LC-S8D Phase B — pending primary evidence |
| `hba1c_pct` knowledge_bus package remap | LC-S8D deferred list |
| Upload-review / upload-edit surfaces for Mode A | FE-S8E §9 known gaps |
| `automation_bus/latest_audit_summary.md` | Missing — no automation bus summary consumed |

### 10.3 Decision table

| Area | Evidence status | Verdict | Blocks Sprint 5 closeout? | Blocks Sprint 6? |
|------|-----------------|---------|---------------------------|------------------|
| Unit governance | Strong — LC-S8D sentinel + UAT + Sentinel pack | **Pass** (fixture-scoped) | No (for unit track) | No for **scoped** unit Sprint 6 |
| Layer C Mode A | Strong — FE-S8E UAT + post-merge comparison | **Pass** | No | No for scoped protection |
| Layer C Mode B | Strong — same evidence | **Pass** | No | No for scoped protection |
| Lifestyle visible payoff | Stale harness narrative diff only; no CHECK 2; no fresh UI proof | **Unproven** | **Yes** (full PASS) | Yes (full slice protection) |
| Medication visible payoff | Stale harness: flag toggles; body unchanged | **Partial** | **Yes** (full PASS) | Yes (full slice protection) |
| WHY coverage | Homocysteine partial (stale); renal-metabolic fallback weak on unit fixture | **Partial** | **Yes** (full PASS) | Yes (full slice protection) |
| Fallback quality | Visible but weak on some leads | **Partial** | **Yes** (full PASS) | Yes (trust-sensitive leads) |
| Legacy `insights[]` | LC-S4 gating cited; not re-tested LC-S9 | **Assumed pass** (prior sprint) | No | No |
| Mock-mode honesty | LC-S4 cited; not re-tested LC-S9 | **Assumed pass** (prior sprint) | No | No |
| IDL surfacing | Stale harness empty titles; depth unverified | **Unproven** | Yes (if IDL in launch surface) | Partial |
| Report coherence | Mixed-unit partial; DQ trust strip wrong | **Partial** | Yes (full commercial sign-off) | Partial |
| Regression/Sentinel protection | Unit sentinel yes; launch-core harness/CHECKs no | **Partial** | **Yes** (full PASS) | Yes (full programme Sprint 6) |

---

## 11. Final recommendation

1. **Accept** LC-S8D and FE-S8E as **complete and stable** for the **unit-governance and Layer C presentation** workstream on the mixed-unit sentinel fixture. Do not reopen unit merge for that scope.

2. **Do not** declare **full Sprint 5 PASS** or **programme ready for Sprint 6 (whole slice)** until fresh launch-core proving artefacts, human walkthrough, CHECK automation, and acceptable WHY/fallback behaviour are evidenced.

3. **Proceed** with a **targeted correction sprint (B)** before broad Sprint 6: refresh harness, close WHY/fallback trust gaps on active leads, prove visible lifestyle/statin payoff, complete lc_s5 human validation checklist.

4. **Optionally run a narrow Sprint 6 in parallel** protecting only LC-S8D/FE-S8E behaviours — does not substitute for Sprint 5 closeout.

5. **Keep Phase B unit evidence parked** unless leadership explicitly reprioritises it over launch-core proving closeout.

---

## Explicit non-authority statement

This document is an **investigation and draft decision artefact** prepared under LC-S9. Cursor does **not**:

- self-certify programme or Sprint 5 closure;
- authorise Sprint 6 for the full launch-core slice;
- approve merge to `main` or any release branch;
- create or update `automation_bus/latest_audit_summary.md`;
- substitute for named human tester sign-off or programme decision authority.

Final approval rests with the programme owner and named decision authority per the transformation plan Pre-Sprint 1 gate model.

---

## Appendix — Related audit papers

- [`LC-S8D_frontend_layer_c_uat_report.md`](LC-S8D_frontend_layer_c_uat_report.md)
- [`FE-S8E_post_merge_comparison_uat.md`](FE-S8E_post_merge_comparison_uat.md)
- [`lc_s5_proving_readiness_preflight_audit.md`](lc_s5_proving_readiness_preflight_audit.md)
