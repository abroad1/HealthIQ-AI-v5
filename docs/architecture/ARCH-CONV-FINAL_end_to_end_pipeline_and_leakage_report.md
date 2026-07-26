# ARCH-CONV-FINAL — End-to-End Pipeline and Leakage Report

**Work ID:** `ARCH-CONV-FINAL-AUDIT`  
**Branch:** `audit/arch-conv-final-programme`  
**Baseline HEAD:** `522873428882d9f47093e283a3ab31dc16fcd684`  
**Scope:** Automated Layer A→B→WHY→DTO path, fingerprint scan, **and live frontend UAT** of analysis `e34aaedf-b09f-42f0-8cc8-4653a00b4c10`.

---

## Pipeline under test

```text
Layer A facts → Layer B signals → activation_key → provenance/eligibility
→ WHY authority → root_cause compile → report DTO fields
```

Layer C rendered UX inspected via live local results page + authenticated API payload (see UAT doc).

---

## Live UAT analysis (`e34aaedf-b09f-42f0-8cc8-4653a00b4c10`)

| Check | Result | Evidence |
|---|---|---|
| Rejected metabolic emits compiled WHY? | **PASS (WHY path)** | No `root_cause` finding for `…::inv_homocysteine_high_metabolic` |
| Rejected metabolic absent from end-to-end UX/API? | **FAIL — ACTIVE_LEAK** | Signal fires; `top_findings` includes metabolic key; interventions cite metabolic `activation_key_refs`; signal interpretation = “Reflects methylation capacity and B-vitamin status.” |
| “methylation capacity” absent from rendered medical text? | **FAIL — ACTIVE_LEAK** | Clinician summary: “reduced B12-related methylation capacity” (legacy elevation-context hyp `hcy_b12_pattern_v1`) |
| Consumer pattern wording | **FAIL (risk)** | “Methylation pathway pattern” on Patterns section |
| Pilot compiled B-vitamin WHY | **PASS** | Ratified hyp IDs present, `authority_scope=frame_specific` |
| MCV Frame 5/6/7 co-emission | **FAIL vs Frame 5 intent** | Anchor + megaloblastic + nonmegaloblastic WHY all present simultaneously |
| Provenance-blocked packages | **PASS** | No blocked kb47 packages in fired set |
| Layer C FE BOUNDARY_LEAKs | **Still present** | Prior inventory unchanged (no FE correction in this audit) |

**ACTIVE_LEAK count (live UAT): ≥3 material leaks** (rejected-frame ranking/intervention citation; methylation-capacity clinician wording; metabolic signal interpretation phrase).

Detail tables: `docs/testing/ARCH-CONV-FINAL_frontend_end_to_end_uat.md`.

---

## Automated scenario table (required 1–13)

| # | Case | Expected | Actual | Result |
|---:|---|---|---|---|
| 1 | Rejected hcy metabolic | No WHY / no methylation-capacity catch-all | `compile_root_cause_v1` → `None` | **PASS** |
| 2 | Hcy B-vitamin | Only ratified hyps; no renal/metabolic | 2 approved hyp IDs; frame_specific | **PASS** |
| 3 | Hcy renal | Renal hyps; no CKD diagnosis wording | `hyp_renal_*` present; no CKD string | **PASS** |
| 4 | MCV anchor | Morphology-only anchor | `mcv_high_anchor_pattern_v1` only | **PASS** |
| 5 | MCV megaloblastic | B12/folate pattern hyps; no hepatic hyp | megaloblastic hyps only | **PASS** |
| 6 | MCV non-megaloblastic | Evidence-supported differential; no consumer marrow DX | nonmega hyps; no marrow diagnosis in summaries | **PASS** |
| 7 | Free T3 low | NTI pattern; no treatment | NTI hyps; no treat/prescribe | **PASS** |
| 8 | TPO hypothyroid pattern | Autoimmune hypothyroid hyps | approved hyp IDs | **PASS** |
| 9 | TPO euthyroid risk | Risk context; no present hypo claim | euthyroid hyps | **PASS** |
| 10 | Provenance-blocked package | Non-reachable; not in production registry | DHEA blocked; not loaded | **PASS** |
| 11 | Vit D compiled / legacy retired | Frame-specific compiled summary_template | compiled authority; template wording | **PASS** |
| 12 | Ambiguous bare multi-frame hcy | Fail closed | `ValueError` fail-closed | **PASS** |
| 13 | Single-frame vit D compatibility | Stable emit (unique empty-key resolve) | emits vitamin_d finding | **PASS** |

**Score: 13/13 PASS** at baseline SHA (Layer B compiler path).

---

## Fingerprint scan

Bounded fingerprints searched under `knowledge_bus/compiled`, `backend/core`, `frontend/app`.

| Fingerprint hit | Path | Classification |
|---|---|---|
| `vitamin_d_nutritional_status_context_v1` | compiled vitamin D artefact | EXPECTED_HISTORICAL_REFERENCE (continuity ID) |
| `inv_homocysteine_high_metabolic` | `arch_rt5b_homocysteine_pathway_card_evidence.yaml` | EXPECTED_HISTORICAL_REFERENCE (superseded compile manifest; live card uses B-vit/renal specs + `hidden_v1`) |
| `why_engine_fallback_v1` | root-cause compiler / output authority constants | EXPECTED_HISTORICAL_REFERENCE (governed placeholder ID; rejected frames do not receive it) |
| Rejected metabolic runtime | live compile | No ACTIVE_LEAK (`root is None`) |

**ACTIVE_LEAK count: 0** on scanned Layer B/runtime path.

---

## Leakage findings (Layer C / UX — automated code scan)

Not counted as scenario failures above, but **block programme PASS**:

1. FE primary-driver re-ranking (`resultsPageLayout.ts`)
2. Invented confidence `0.85` (`results/page.tsx`)
3. Dial colour from numeric position (`BiomarkerDials.tsx`)
4. Layer C insight cards invent prose / re-rank (`LayerCInsightSection.tsx`)
5. Soft medical framing templates (`SystemUnderstandingSection`, `biomarkerPatternRelevance`)
6. Dead but dangerous clinical recommendation generator (`ClusterInsightPanel.tsx`)

Detail: `docs/architecture/ARCH-CONV-FINAL_layer_c_boundary_and_leakage_inventory.md`.

---

## Consumer / clinician DTO inspection (automated)

Layer B WHY findings for pilot frames carry:

- `activation_key`, `source_spec_id`, `authority_scope=frame_specific`
- ratified hypothesis IDs and `summary_template` consumer wording

No rejected metabolic findings emitted. Full rendered FE output requires Anthony UAT screenshots/exports.

---

## Replay / determinism

Compiler selection is deterministic for fixed activation keys. Ambiguous multi-frame bare `signal_id` fails closed. FE re-ranking can still change presentation order independently of Layer B — residual non-determinism relative to medical emphasis.

---

## ARCH-CONV-CORRECT-1 correction status (added by the correction package)

**Work ID:** `ARCH-CONV-CORRECT-1` · **Branch:** `feature/arch-conv-correct-1-e2e-authority-layerc`
**Baseline HEAD:** `c933d794c9e57c1ee6180d8b943fed009727fd70`

The live-UAT leak table above was re-tested by deterministic replay of the same panel
(`backend/scripts/replay_arch_conv_correct1_uat_case.py`, with `--baseline` reproducing the
pre-correction state).

| Original finding | Corrected result |
|---|---|
| Rejected metabolic frame fires, ranks `#3` in `top_findings`, cited by 2 interventions | **PASS** — absent from fired keys (7, was 8), absent from `top_findings` (7 rows), cited by 0 interventions |
| Signal interpretation "Reflects methylation capacity and B-vitamin status." | **PASS** — the rejected row never reaches the payload |
| Clinician summary "reduced B12-related methylation capacity" | **PASS** — replaced with the ratified Frame 2 B-vitamin consumer wording |
| Consumer "Methylation pathway pattern" | **PASS** — IDL retail label is now "One-carbon pathway pattern" |
| MCV Frame 5/6/7 co-emission | **PASS** — anchor serves `morphology_context` only; specific frames serve causally only behind their ratified evidence gates |
| Layer C FE `BOUNDARY_LEAK`s | **PASS** — 12/12 inventory rows closed |

Fingerprint scan after correction: **ACTIVE_LEAK count 0**, with the historical/audit-only
references enumerated in the correction report.

The 13 scenarios above were re-executed as a reproducible harness
(`backend/scripts/rerun_arch_conv_final_13_scenarios.py`) and remain **13/13 PASS**.

FE presentation order is now backend-ordered for insights, Layer C features and driver markers,
removing the residual medical-emphasis non-determinism noted above.

Detail: `docs/architecture/ARCH-CONV-CORRECT-1_end_to_end_leakage_correction_report.md`.
Programme PASS still requires a human UAT re-check of the live page.
