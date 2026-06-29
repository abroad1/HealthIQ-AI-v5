# P3-PROSE-DEPTH-1 — MR Batch 001 Brief (Candidate Assets Only)

**Work ID:** P3-PROSE-DEPTH-1  
**Batch ID:** MR-BATCH-001  
**Output status:** `CANDIDATE` only — do not write to runtime or production registries.

## Instructions for Medical Research LLM

You are authoring **candidate prose assets** for HealthIQ AI's governed prose library. Follow `P3-PROSE-DEPTH-1_mr_candidate_asset_schema.yaml` and use `P3-PROSE-DEPTH-1_mr_candidate_asset_template.yaml` as structural templates.

### Mandatory rules

1. **Do not write directly to runtime files** (`retail_explainer_v1/registry.yaml`, pathway packs, missing-marker packs, modifier catalogues, compilers, or frontend).
2. **Do not claim diagnosis** — use pattern-and-association / educational language only.
3. **Do not recommend treatment**, dose changes, supplements, or medication actions.
4. **Cite evidence** for each non-educational claim in `evidence_refs`.
5. **State uncertainty** where interpretation is limited.
6. Use **cautious UK consumer-facing language** for retail assets.
7. Separate retail and clinician variants **only where required**.
8. Create sex/age-specific wording **only where medically justified** (not for reference-range-only differences).
9. Mark every asset `review_status: CANDIDATE`.
10. Flag assets requiring medical review in `notes_for_medical_reviewer`.

### Composition model (do not invent bespoke paragraphs per combination)

Hybrid minimum viable composition:

`base explainer + signal/frame explainer + pathway explainer + additive modifier fragment + missing-marker caveat + resilience qualifier`

Modifiers are **additive caveats** (1–2 sentences), not paragraph replacements.

---

## Batch 001 scope (beta-critical depth)

### 1. Hepatic pathway explainer candidate

- **asset_type:** `pathway_explainer`
- **scope:** `wave1_liver` / hepatic enzyme and processing context
- **destination_mapping placeholder:** `knowledge_bus/pathway_explainers_v1/pathway_explainers_v1.yaml`
- **Gap rationale:** DYNAMIC-PROSE-ARCH-1 — hepatic pathway absent; launch-core domain gap.

### 2. Metabolic / glycaemic pathway explainer candidate

- **asset_type:** `pathway_explainer`
- **scope:** `wave1_blood_sugar` / glycaemic and insulin-metabolic context
- **destination_mapping placeholder:** `knowledge_bus/pathway_explainers_v1/pathway_explainers_v1.yaml`
- **Gap rationale:** DYNAMIC-PROSE-ARCH-1 — metabolic pathway absent.

### 3. Top 10 missing retail biomarker explainers (beta priority)

Author `base_biomarker_explainer` candidates for:

| Priority | biomarker_id | Rationale |
|----------|--------------|-----------|
| 1 | cystatin_c | Renal filtration context; complements creatinine/eGFR |
| 2 | uacr | Kidney damage marker; launch renal depth |
| 3 | white_blood_cells | CBC / inflammation context |
| 4 | platelets | CBC completeness |
| 5 | creatine_kinase | Statin/muscle monitoring education |
| 6 | calcium | Electrolyte panel gap |
| 7 | cortisol | Endocrine axis gap |
| 8 | shbg | Hormone interpretation context |
| 9 | free_testosterone | Androgen panel gap |
| 10 | total_protein | Liver/nutrition context |

Source gap inventory: `P3-PROSE-DEPTH-1_prose_coverage_matrix.yaml` (retail section).

### 4. Missing-marker caveat candidates

Author `missing_marker_caveat` candidates where gaps exist:

| Context | suggested missing_marker scope |
|---------|-------------------------------|
| Hepatic | alt absent; ggt absent; ast absent |
| Metabolic | insulin absent; hba1c absent (if panel partial) |
| Lipid | apob absent; lipoprotein_a absent |
| Kidney | cystatin_c absent; urea absent |

Align field structure with existing pack: `caution_when_absent`, `interpretive_limit`, `interpretive_caution`.

### 5. Lifestyle modifier fragment candidates

Only where supported by `context_modifier_catalogue_draft_v1.yaml`:

| Modifier class | Context |
|----------------|---------|
| mod_q_lifestyle_alcohol | ggt, alt, ast, triglycerides |
| mod_q_lifestyle_smoking | inflammation markers (if catalogue supports) |
| mod_q_lifestyle_exercise | creatinine / muscle enzyme context |
| mod_q_hydration | creatinine / renal concentration context |

### 6. Medication modifier fragment candidates

Only where supported by `intervention_effects_registry_v1.yaml`:

| Class | Context |
|-------|---------|
| lipid_lowering_statin | LDL, non-HDL, apoB; monitoring caveat for ALT/AST/CK |
| biguanide_metformin | glucose/HbA1c; B12 context if supported |
| raas_inhibitor | creatinine/eGFR interpretation context (NSAID/renal adjacent) |

### 7. Supplement modifier fragment candidates

| Modifier | Context |
|----------|---------|
| mod_sup_creatine | creatinine interpretation |
| mod_sup_iron | ferritin / iron markers |
| mod_sup_b12 | homocysteine / B12 markers |
| mod_sup_folate | homocysteine / folate context |

---

## Deliverable format

- One YAML file per asset **or** one batch YAML with a list of assets conforming to the schema.
- Store outputs outside production paths (e.g. `knowledge_bus/generated_pilot/mr_batch_001/` when promotion sprint authorises).
- All assets: `review_status: CANDIDATE`.

## Medical review flags

Flag for `NEEDS_MEDICAL_REVIEW` before any promotion:

- Any wording implying causation between lifestyle/medication/supplement and disease state
- Any frame-level signal prose (frame routing deferred)
- Positive resilience qualifiers without explicit governing signal state
- Hepatic/metabolic pathway claims beyond educational association

## Not in scope for MR Batch 001

- Runtime activation
- Modifier binding
- Gemini narrative generation
- Production registry edits
- Sex/age-specific prose unless medically justified
