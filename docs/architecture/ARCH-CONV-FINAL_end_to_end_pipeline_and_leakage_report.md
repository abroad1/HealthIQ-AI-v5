# ARCH-CONV-FINAL — End-to-End Pipeline and Leakage Report

**Work ID:** `ARCH-CONV-FINAL-AUDIT`  
**Branch:** `audit/arch-conv-final-programme`  
**Baseline HEAD:** `522873428882d9f47093e283a3ab31dc16fcd684`  
**Scope:** Automated Layer A→B→WHY→DTO path plus fingerprint scan. Frontend rendering UAT deferred to Anthony.

---

## Pipeline under test

```text
Layer A facts → Layer B signals → activation_key → provenance/eligibility
→ WHY authority → root_cause compile → report DTO fields
```

Layer C rendered UX is covered in the boundary inventory + human UAT plan (not claimed complete here).

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
