# ARCH-CONV-A — Wave 3 Renal Medical-Review Pack (STOP B)

> **Preserved preparation only (ARCH-CONV-B branch prep).**  
> This document is a historical source pack cherry-picked for `ARCH-CONV-B`.  
> Active work identity is `ARCH-CONV-B` on `feature/arch-conv-b-renal-why-authority`.  
> Do not treat `ARCH-CONV-A` / Wave 3 as the active work package.  
> Phase 0 refreshes this material into ARCH-CONV-B authority documents.  
> No medical approval, compilation, runtime activation, or legacy disconnection is implied by this file.

**Original Work ID (historical):** `ARCH-CONV-A`  
**Original Wave (historical):** 3 — Renal function panel (specification-ready subset)  
**Date (UTC):** 2026-07-28  
**Pack role:** Gate 1 / Gate 2 **submission evidence** assembled by Cursor (preserved)  
**Medical decisions in this pack:** **NONE** — all decision fields left for GPT + Anthony  

Allowed decision values (for reviewers only):

```text
APPROVE
APPROVE_WITH_NARROWING
REJECT
DEFER_EVIDENCE_INSUFFICIENT
CONTEXT_ONLY
```

**Wave 2 audit prerequisite (recorded):**

```text
Wave 2 STOP C: PASS
audit recommendation: PROCEED_TO_WAVE_3_PLANNING
new regressions versus main: 0
```

**Explicit non-actions in this pack:** no Gate 1 medical decisions; no Wave 3 compile; no runtime activation; no signal-gate changes; no legacy disconnection; no Wave 1/2 behaviour change; no Wave 4 work.

Canonical identities use **embedded** investigation-spec `spec_id` values. Do not create activation keys from filenames.

---

## Identity verification (pre-pack)

| signal_id | filename | embedded `spec_id` | primary biomarker | proposed activation_key | sha256 prefix |
|---|---|---|---|---|---|
| signal_creatinine_high | inv_creatinine_high_renal_v1.yaml | **inv_creatinine_high_renal** | creatinine | signal_creatinine_high::inv_creatinine_high_renal | `b53c0d924fde540c` |
| signal_urea_high | inv_urea_high_renal.yaml | **inv_urea_high_renal** | urea | signal_urea_high::inv_urea_high_renal | `3c8d3d2e8c813802` |
| signal_urate_high | inv_uric_acid_high_metabolic.yaml | **inv_uric_acid_high_metabolic** | **urate** | signal_urate_high::inv_uric_acid_high_metabolic | `a7edef6ee3c28a4d` |

### Identity discrepancies (Gate 1 must confirm)

1. **Creatinine filename `_v1`:** Phase-1 / Phase-2 index previously listed `inv_creatinine_high_renal_v1` as source_spec_id / activation key. Embedded canonical `spec_id` is `inv_creatinine_high_renal` (no `_v1`). Filename `_v1` is **not** activation-key material (Wave 2 precedent).
2. **Urate / uric_acid naming:** `signal_id` and primary biomarker use `urate`; investigation `spec_id` uses `uric_acid` (`inv_uric_acid_high_metabolic`). These are intentional naming variants for one frame — do not invent a parallel `inv_urate_*` activation key from the biomarker name alone.
3. **Phase-1 map row** recorded `inv_creatinine_high_renal_v1` — superseded for STOP B by the embedded `spec_id` verification above.

---

## Pack summary

| # | signal_id | activation_key (proposed) | canonical inv | medical decision | GPT ref | Anthony ref |
|---:|---|---|---|---|---|---|
| 1 | signal_creatinine_high | signal_creatinine_high::inv_creatinine_high_renal | inv_creatinine_high_renal_v1.yaml | **PENDING** | | |
| 2 | signal_urea_high | signal_urea_high::inv_urea_high_renal | inv_urea_high_renal.yaml | **PENDING** | | |
| 3 | signal_urate_high | signal_urate_high::inv_uric_acid_high_metabolic | inv_uric_acid_high_metabolic.yaml | **PENDING** | | |

---

## Cross-wave / adjacency constraints (non-decision)

| Constraint | Status for reviewers |
|---|---|
| Do not silently displace separately governed `signal_egfr_low` | Live packages: `pkg_kb47_egfr_low_chronic_kidney_function_reduction`, `pkg_kb47_egfr_low_hemodynamic_filtration_drop`. Not a Wave 3 compile target. Creatinine framing must treat eGFR as supporting/severity context, not absorb eGFR WHY. |
| Homocysteine renal-clearance pilot frame | Already `COMPILED_ACTIVE`: `signal_homocysteine_high::inv_homocysteine_high_renal_clearance_reduction`. Different signal_id — narrative must not contradict, but is not a dual on creatinine/urea/urate. |
| Wave 1 thyroid / Wave 2 lipid | Must remain unchanged. |
| Layer C | Must not reconstruct renal medical meaning. |

---

## Estate collision inventory (all three targets)

### Creatinine — packages / identities

| Package | signal_id | activation_key | status class |
|---|---|---|---|
| pkg_s24_creatinine_high_renal | signal_creatinine_high | signal_creatinine_high::inv_creatinine_high_renal | S24 canonical candidate (matches embedded spec) |
| pkg_kb52c_creatinine_high_reduced_glomerular_filtration | signal_creatinine_high | signal_creatinine_high::inv_creatinine_high_reduced_glomerular_filtration | Pass-3 parallel — **same signal_id, different source_spec_id** |
| pkg_kb52c_creatinine_low_low_muscle_mass_or_low_generation | signal_creatinine_low | signal_creatinine_low::inv_creatinine_low_low_muscle_mass_or_low_generation | Adjacent low-direction (out of Wave 3 high targets) |
| KBP-0001 | signal_renal_metabolic_stress | composite | Composite adjacency — not Wave 3 target |

**Legacy WHY:** `knowledge_bus/root_cause/hypotheses/creatinine_high_hypotheses_v1.yaml`  
(`creatinine_elevated_filtration_stress_v1`, `creatinine_urea_co_rise_renal_context_v1`) — comparison only.

**Compiled WHY authority:** none for creatinine (not in pilot / not COMPILED_ACTIVE).  
**Current runtime WHY authority:** legacy path (out of Package A pilot cohort).

**Duplicate / collision:** same-signal dual between S24 renal frame and Pass-3 reduced-glomerular-filtration frame. Named duplicate-authority resolution (Wave 1) applies only after Gate 1 chooses the winning medical identity; **do not resolve mechanically in this pack**.

### Urea — packages / identities

| Package | signal_id | activation_key | status class |
|---|---|---|---|
| pkg_s24_urea_high_renal | signal_urea_high | signal_urea_high::inv_urea_high_renal | S24 canonical candidate |
| pkg_kb52c_urea_high_prerenal_volume_depletion_or_catabolic_load | signal_urea_high | signal_urea_high::inv_urea_high_prerenal_volume_depletion_or_catabolic_load | Pass-3 parallel — **same signal_id, different source_spec_id** |
| pkg_kb52c_urea_low_low_protein_or_reduced_urea_cycle_input | signal_urea_low | … | Adjacent low-direction |

**Legacy WHY:** `knowledge_bus/root_cause/hypotheses/urea_high_hypotheses_v1.yaml`  
(`urea_elevated_excretory_burden_v1`, `urea_creatinine_ratio_context_v1`) — comparison only.

**Compiled WHY authority:** none. **Current runtime:** legacy path.

**Duplicate / collision:** S24 renal vs Pass-3 prerenal/catabolic — medical differentiation is Gate 1 scope (renal filtration context vs dehydration / protein / catabolic load).

### Urate — packages / identities

| Package | signal_id | activation_key | status class |
|---|---|---|---|
| pkg_s24_urate_high_metabolic | signal_urate_high | signal_urate_high::inv_uric_acid_high_metabolic | S24 canonical candidate (`uric_acid` in spec_id; `urate` biomarker) |
| pkg_kb52c_urate_high_gout_crystal_deposition_risk | signal_urate_high | signal_urate_high::inv_urate_high_gout_crystal_deposition_risk | Pass-3 parallel — gout/crystal-risk framing |
| pkg_kb52c_urate_low_reduced_urate_pool_or_renal_loss | signal_urate_low | … | Adjacent low-direction |

**Legacy WHY:** `knowledge_bus/root_cause/hypotheses/urate_high_hypotheses_v1.yaml`  
(`urate_elevated_serum_hyperuricaemia_v1`, `urate_inflammatory_coupling_v1`) — comparison only.

**Compiled WHY authority:** none. **Current runtime:** legacy path.

**Duplicate / collision:** prevent parallel activation of both `inv_uric_acid_high_metabolic` and `inv_urate_high_gout_crystal_deposition_risk` as competing causal authorities without Gate 1 disposition. Do not invent `signal_uric_acid_high` or filename-derived aliases.

### eGFR adjacency (not a Wave 3 target)

| Package | activation_key |
|---|---|
| pkg_kb47_egfr_low_chronic_kidney_function_reduction | signal_egfr_low::inv_egfr_low_chronic_kidney_function_reduction |
| pkg_kb47_egfr_low_hemodynamic_filtration_drop | signal_egfr_low::inv_egfr_low_hemodynamic_filtration_drop |

eGFR appears in health-system card evidence (`wave1_ren_glomerular_filtration`) but is **not** a Package A Wave 3 WHY compile candidate. Creatinine Wave 3 must not absorb or retire eGFR authority.

---

## Frame 1 — signal_creatinine_high

### Identity

| Field | Value |
|---|---|
| signal_id | signal_creatinine_high |
| embedded source_spec_id | inv_creatinine_high_renal |
| proposed activation_key | signal_creatinine_high::inv_creatinine_high_renal |
| filename (source path only) | knowledge_bus/research/investigation_specs/inv_creatinine_high_renal_v1.yaml |
| source sha256 prefix | b53c0d924fde540c |
| wave | 3 |

### Canonical source summary (from inv — not a medical approval)

| Field | Value |
|---|---|
| research_domain | renal |
| primary marker | creatinine |
| evidence_strength | strong |
| cited sources (spec) | NICE NG203 (2021) CKD assessment and management |
| physiological claim (spec) | Creatinine filtered freely by glomerulus; serum rises as filtration falls |
| narrative interpretation (spec) | Rising creatinine requires checking eGFR; low eGFR may suggest AKI or CKD context |

### Proposed interpretation (for reviewer — PENDING)

Elevated creatinine as a filtration-marker / renal-clearance-stress candidate, with mandatory recognition that isolated high creatinine does **not** prove reduced kidney function.

### Specificity question (Gate 1 — do not resolve here)

Is `inv_creatinine_high_renal` sufficiently specific for one compiled frame, or does it risk collapsing distinct interpretations that Pass-3 already separates?

| Interpretation class | Where it appears today | Gate 1 question |
|---|---|---|
| Reduced glomerular filtration / renal | S24 inv + Pass-3 reduced_glomerular_filtration | One frame or retain parallel? |
| High muscle mass / generation | Spec confounder; creatinine_low Pass-3 package (inverse) | Context-only caveats vs separate frame? |
| Creatine supplementation | Spec confounder | Context modifier only? |
| Dehydration / pre-renal | Spec confounder | Shared with urea Pass-3 prerenal? |
| Acute vs chronic | Spec narrative (AKI vs CKD) | Fail-closed without serial data / known CKD? |
| Medication effects on secretion / renal function | Spec implications mention nephrotoxin review; limited structured confounder list | Sufficient canonical authority? |

### Evidence boundaries from inv

| Field | Value |
|---|---|
| supporting markers | egfr low (severity); urea high (corroborator); potassium high (severity) |
| override / escalation | eGFR < 60 → at_risk (CKD Stage 3+ context per NICE NG203 in spec); creatinine high + potassium above_max → at_risk |
| confounders | high muscle mass; creatine supplementation; dehydration |
| UACR | Spec implications mention urine protein check — **no structured UACR marker row in inv**; Gate 1 should treat UACR as optional clinical correlation unless separately governed |
| known CKD | Not a structured input field in inv — acute vs chronic distinction limited without history/serial labs |
| exercise | Not explicitly listed as confounder in inv (muscle mass / creatine are); reviewers may note strenuous exercise as related muscle-generation context if canonical authority supports |

### Creatinine vs eGFR authority

| Rule for pack | Detail |
|---|---|
| Preserve `signal_egfr_low` | Separately governed; two live KB47 frames |
| Creatinine MUST NOT become a surrogate that displaces eGFR WHY | eGFR is supporting/severity in the creatinine inv, not a license to compile eGFR under creatinine |
| Concordance | Creatinine high + eGFR low may strengthen filtration-stress context |
| Discordance | Creatinine high + eGFR not low (or absent) must not auto-claim CKD/AKI |

### Consumer / clinician / intervention implications (for reviewer)

| Surface | Implications to review |
|---|---|
| Consumer | Permitted: above range; may reflect filtration-marker stress; worth clinical correlation. Prohibited: “your kidneys are failing”; automatic CKD/AKI diagnosis; medication start/stop. |
| Clinician | May describe phenotype; note eGFR/urea/K concordance; list generation/supplement/hydration confounders already in canonical authority; recommend clinical correlation. Must not auto-diagnose CKD or prescribe. |
| Intervention | Spec implications mention BP monitoring, nephrotoxin review, urine protein — **do not encode treatment plans** without separate intervention authority. |

### Medical decision register (blank)

| Field | Value |
|---|---|
| medical decision | PENDING |
| GPT review reference | |
| Anthony ratification reference | |
| narrowing bounds (if any) | |

---

## Frame 2 — signal_urea_high

### Identity

| Field | Value |
|---|---|
| signal_id | signal_urea_high |
| embedded source_spec_id | inv_urea_high_renal |
| proposed activation_key | signal_urea_high::inv_urea_high_renal |
| source path | knowledge_bus/research/investigation_specs/inv_urea_high_renal.yaml |
| source sha256 prefix | 3c8d3d2e8c813802 |
| wave | 3 |

### Canonical source summary (from inv — not a medical approval)

| Field | Value |
|---|---|
| research_domain | renal |
| primary marker | urea |
| evidence_strength | strong |
| cited sources (spec) | source_ref_9 “Renal Function Tests”, Clinical Biochemistry 2019 |
| narrative interpretation (spec) | Marker of renal function and metabolic/hydration state |

### Proposed interpretation (for reviewer — PENDING)

Elevated urea as possible renal-filtration or excretory-burden context, explicitly distinguished from dehydration, protein load, GI bleed (Hb-low differential in spec), and catabolic states. Isolated urea elevation must not diagnose renal impairment.

### Differential checklist for Gate 1

| Context | Canonical support in inv / estate | Reviewer note |
|---|---|---|
| Renal filtration (with creatinine) | Supporting creatinine high; override or_urea_intrinsic_renal | Concordant rise more suggestive of intrinsic renal pattern — still not a diagnosis |
| Dehydration / volume depletion | Spec confounder; Pass-3 prerenal package | May deserve CONTEXT_ONLY or competing frame disposition |
| High protein intake | Spec confounder | Generation/load context |
| GI bleeding | Spec differential via low hemoglobin | Differential marker — not automatic diagnosis |
| Catabolic illness / corticosteroids | Pass-3 package title includes catabolic load; **corticosteroids not explicit in S24 inv confounders** | Evidence gap if reviewers require steroid callout |
| Creatinine / eGFR concordance | Creatinine in inv; eGFR not a urea supporting marker row | Use creatinine concordance; do not invent eGFR authority under urea |

### Evidence boundaries from inv

| Field | Value |
|---|---|
| supporting markers | creatinine high (corroborator); hemoglobin low (differential) |
| override / escalation | urea high + creatinine above_max → at_risk |
| confounders | high protein diet; dehydration |

### Consumer / clinician / intervention implications (for reviewer)

| Surface | Implications to review |
|---|---|
| Consumer | Above range; may reflect hydration, protein load, or excretory burden; not a kidney-failure diagnosis. |
| Clinician | Distinguish isolated urea from creatinine-concordant pattern; note GI-bleed differential when Hb low if data present. |
| Intervention | No treatment plan from urea alone. |

### Research completeness note

S24 urea inv cites a single generic biochemistry source (`source_ref_9`). Pass-3 prerenal/catabolic package encodes richer differential titles. Gate 1 should decide whether S24 renal framing is adequate, needs narrowing/context-only, or needs research deferral relative to Pass-3.

### Medical decision register (blank)

| Field | Value |
|---|---|
| medical decision | PENDING |
| GPT review reference | |
| Anthony ratification reference | |

---

## Frame 3 — signal_urate_high

### Identity

| Field | Value |
|---|---|
| signal_id | signal_urate_high |
| embedded source_spec_id | inv_uric_acid_high_metabolic |
| proposed activation_key | signal_urate_high::inv_uric_acid_high_metabolic |
| primary biomarker_id | urate |
| naming note | hyperuricaemia / uric acid language appears in rationale and narrative; identity remains `urate` signal + `uric_acid` spec_id |
| source path | knowledge_bus/research/investigation_specs/inv_uric_acid_high_metabolic.yaml |
| source sha256 prefix | a7edef6ee3c28a4d |
| wave | 3 |

### Canonical source summary (from inv — not a medical approval)

| Field | Value |
|---|---|
| research_domain | metabolic |
| evidence_strength | strong |
| cited sources (spec) | source_ref_4 “Uric acid and renal disease”, Nature Reviews Nephrology 2018 |
| threshold notes (spec) | Solubility ~360 µmol/L (6 mg/dL) — biochemical context, not a gout diagnosis |
| narrative implications (spec) | Risk of gouty arthritis flares and potential kidney stones — **must not become product diagnosis language** |

### Proposed interpretation (for reviewer — PENDING)

Hyperuricaemia as a biochemical finding with possible gout-risk, renal-handling, dietary/alcohol, medication, and metabolic associations — without diagnosing gout, kidney stones, or metabolic syndrome from urate alone.

### Differential checklist for Gate 1

| Context | Canonical support | Restriction |
|---|---|---|
| Biochemical hyperuricaemia | Primary high-urate signal | Allowed framing candidate |
| Gout risk context | Spec narrative / Pass-3 gout_crystal_deposition_risk | Risk context ≠ diagnosis of gout |
| Renal handling | Supporting creatinine high; override with eGFR < 60 | Supporting only; do not absorb eGFR |
| Medication effects | Not structured in S24 inv confounders | Evidence gap unless other governed authority supplies |
| Alcohol / dietary (purine) | Spec confounder: high purine diet (meat, seafood, beer) | Context modifier |
| Metabolic associations | Supporting triglycerides high; narrative metabolic-syndrome cluster language | Association ≠ metabolic-syndrome diagnosis |

### Parallel activation prevention

| Competing key | Disposition required |
|---|---|
| signal_urate_high::inv_uric_acid_high_metabolic | Proposed Wave 3 canonical (PENDING) |
| signal_urate_high::inv_urate_high_gout_crystal_deposition_risk | Pass-3 parallel — Gate 1 must APPROVE/CONTEXT_ONLY/REJECT/DEFER relative to S24; do not leave dual causal WHY |

Do **not** create:

- `signal_uric_acid_high::*`
- `signal_urate_high::inv_urate_high_metabolic` (invented alias)
- filename-derived `_v1` keys

### Consumer / clinician / intervention implications (for reviewer)

| Surface | Implications to review |
|---|---|
| Consumer | Above range; may reflect hyperuricaemia / gout-risk context; no “you have gout/stones/metabolic syndrome”. |
| Clinician | Describe biochemical phenotype; note renal/TG concordance; dietary/alcohol confounders per canonical authority. |
| Intervention | No urate-lowering therapy recommendation from this frame alone. |

### Medical decision register (blank)

| Field | Value |
|---|---|
| medical decision | PENDING |
| GPT review reference | |
| Anthony ratification reference | |

---

## Unresolved evidence / identity gaps (summary)

| Gap | Affects | Suggested Gate 1 handling class |
|---|---|---|
| Creatinine single-frame vs muscular / acute / Pass-3 GFR frame | creatinine | APPROVE_WITH_NARROWING / CONTEXT_ONLY / multi-frame disposition — **medical** |
| eGFR adjacency (must not displace) | creatinine (+ urate override uses eGFR) | Preserve separate `signal_egfr_low` |
| UACR not structured in creatinine inv | creatinine | Clinical correlation / DEFER if required |
| Acute vs chronic without serial labs / known CKD input | creatinine | Fail-closed or caveat |
| Urea S24 inv thin vs Pass-3 prerenal/catabolic richness | urea | Narrowing vs DEFER_EVIDENCE / parallel disposition |
| Corticosteroids / GI bleed / catabolic not fully structured in S24 urea inv | urea | Evidence gap |
| Urate gout Pass-3 vs metabolic S24 dual | urate | Choose one causal / context hierarchy |
| Medication confounders sparse for urate | urate | Evidence gap |
| Phase-1 creatinine `_v1` index error | creatinine identity | Corrected here to embedded `inv_creatinine_high_renal` |

### Package B / later-wave hand-offs (if Gate 1 declines single-frame compile)

| Candidate hand-off | When |
|---|---|
| Creatinine multi-frame selector (renal vs generation vs acute) | If one S24 frame is medically insufficient |
| Urea prerenal vs intrinsic selector | If Pass-3 prerenal must coexist with S24 renal |
| Urate gout-risk vs metabolic hyperuricaemia coexistence | If both retained |
| eGFR WHY Package A wave (separate) | Explicitly out of Wave 3 — do not fold into creatinine |

---

## STOP B readiness

```text
Wave 3 STOP B pack status: ASSEMBLED — PENDING Gate 1 / Gate 2
frames proposed for medical review: 3
frames ready for Gate 1 structured review: 3 (with recorded evidence/identity gaps)
frames compiled: 0
runtime activated: 0
```

Required next human/medical actions (not Cursor):

1. Gate 1 structured medical review of the three frames above.
2. Confirm creatinine / urate identity and Pass-3 collision dispositions.
3. Preserve eGFR as separate authority.
4. Anthony Gate 2 ratification of Gate 1 outcomes.
5. Only after ratified decisions: Wave 3 compile / STOP C (separate authorised step).

Cursor stop line: **Wave 3 STOP B pack assembly complete — no medical review or compilation performed.**
