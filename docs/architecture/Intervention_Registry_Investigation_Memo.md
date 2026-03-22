# Intervention Registry Investigation Memo

## Scope

This memo records the repo-grounded investigation into the unresolved design mechanics required before implementing the HealthIQ intervention-effects registry.

No files were modified during the investigation.

The memo addresses:
1. hypothesis-link model
2. v1 intervention class list
3. mapping-layer governance
4. registry governance / promotion model
5. registry schema / validator architecture
6. relationship to BE-S0 and context inputs
7. recommended execution sequence
8. blockers or required preconditions

---

## 1. Hypothesis-link model

### What exists today

- Locked `intelligence_model_schema_v1.yaml` defines hypothesis objects with:
  - `hypothesis_id`
  - `rank`
  - `physiological_claim`
  - `evidence_strength`
  - `caveats`
  - `missing_data`
  - `supporting_markers`
  - `contradiction_markers`

There is no intervention or medication field on the hypothesis today.

- At signal level, `future_bucket2_homes` already reserves a nullable home for `medication_effects`.
  This is a placeholder home, not a populated contract for how hypotheses reference intervention knowledge.

- The second-pass design pack treats medication effects as “required later, schema home now” and ties medication context to the governed context roadmap, not to a drug-library model.

### Conclusion

There is no hypothesis-level extension point for intervention classes today; only a signal-level nullable bucket.

#### Smallest clean amendment (recommended)
Add an optional field on each hypothesis, e.g. `intervention_class_refs` or `intervention_relevance`, as a list of objects with at minimum:
- `intervention_class_id`
- `relation_type`

That keeps intervention knowledge out of prose, avoids inventing a drug library, and stays aligned with the “reasoning objects not blobs” principle.

#### IDs only vs IDs + relation
IDs + `relation_type` is the minimal honest structure.  
Class ID alone does not say whether the link is confounding, expected pharmacologic effect, monitoring-only, or caveat-only.

#### Relation types worth having in v1
Recommended bounded set:

| relation_type | Meaning |
|---|---|
| `interpretation_confounder` | Marker or pattern may be biased or misread because of the exposure |
| `expected_biomarker_effect` | Documented directional class effect on relevant biomarkers |
| `monitoring_relevance` | Labs or classes warrant follow-up when this class is present |
| `caveat_only` | Interpretation should remain cautious but not threshold-altered |

No separate contradiction type is needed for interventions if hypothesis-level contradiction markers already exist.  
Intervention links are not the same primitive as contradiction markers.

### Governance implication

This is a narrow schema amendment plus a registry artifact.  
It should be its own small KB sprint, not folded silently into registry implementation.

---

## 2. Proposed v1 intervention class list

### Evidence sources used
This proposal was grounded in repo evidence, not memory, including:
- `backend/ssot/biomarkers.yaml` known modifiers
- `docs/context/INSIGHTS.md`
- package and signoff text referring to medication effects on interpretation

### Defensible minimum v1 class set

| intervention_class_id | Biomarker / domain groups materially affected | Why include in v1 |
|---|---|---|
| `lipid_lowering_statin` | LDL, non-HDL, ApoB, ALT/AST, CK | explicit interpretation relevance |
| `systemic_glucocorticoid` | glucose/HbA1c, WBC/neutrophils, lipids | multi-system confounder |
| `thyroid_hormone_replacement` | TSH, fT4/fT3, lipids | central to thyroid signals |
| `raas_inhibitor` | creatinine, potassium, sodium | common renal/electrolyte monitoring story |
| `thiazide_or_loop_diuretic` | sodium, potassium, urate, renal function | direct electrolyte relevance |
| `biguanide_metformin` | B12, glucose context | metabolic + micronutrient relevance |
| `ppi_long_term_high_dose` | B12, magnesium where in scope | deficiency narrative |
| `sex_hormone_therapy` | SHBG, testosterone interpretation, lipids | common and materially relevant |

### Grouped matrix summary

| Class | Lipids | Glycaemic | Thyroid | LFT / muscle | Renal / electrolytes | CBC / inflammation | Micronutrients |
|---|---|---|---|---|---|---|---|
| Statin | primary | minor | minor | material | minor | minor | minor |
| Glucocorticoid | material | primary | minor | minor | minor | primary | minor |
| Thyroid replacement | material | minor | primary | minor | minor | minor | minor |
| RAAS inhibitor | minor | minor | minor | minor | primary | minor | minor |
| Diuretic | minor | minor | minor | minor | primary | minor | minor |
| Metformin | minor | material | minor | minor | minor | minor | material |
| PPI high-dose | minor | minor | minor | minor | minor | minor | material |
| Sex hormone therapy | material | minor | minor | minor | minor | minor | minor |

This is not completeness.  
It is the smallest serious set the repo already treats as interpretation-relevant.

---

## 3. Mapping-layer governance recommendation

### Recommendation

Use a separate governed alias-mapping file inside the Knowledge Bus, for example:
`knowledge_bus/interventions/intervention_class_alias_map_v1.yaml`

### Minimum structure
A list of:
- `alias_string`
- `intervention_class_id`
- optional `source`

### Unknown names
Unknown names should resolve to a single governed bucket such as:
- `unclassified_medication`

That bucket should only support `caveat_only` behaviour in v1, or otherwise remain flagged as not assessed.

### When mapping runs
Mapping should run at input normalisation / preprocessing time so the reasoning layer only sees canonical class IDs.

### Anti-drift rule
The alias map must be:
- versioned
- validated
- changed only through PR
- not treated as ad hoc application config

---

## 4. Registry governance / promotion recommendation

### Recommendation

Use a governance path lighter than full signal-package promotion, but stronger than an ungoverned YAML file.

### Proposed model
- registry YAML
- schema validation
- dedicated validator
- targeted evidence structure
- PR review
- architectural review for scope expansions

### Difference from signal packages
The registry should not require:
- full `research_brief.yaml`
- full `signal_library.yaml`
- full package-manifest lifecycle

It is registry reference data, not a signal package.

---

## 5. Registry schema / validator architecture recommendation

### Recommendation

Use an independent schema and dedicated validator, not the signal-library chain.

### Why
- intervention effects are canonical reference knowledge, not per-signal architecture
- changes to intervention classes should not imply signal-library version churn
- clearer operational separation
- easier long-term governance

### Alignment with KB
This fits existing KB patterns where different artifact types have distinct schemas and validators.

---

## 6. Relationship to BE-S0 and context inputs

### Baseline context only
These remain context inputs:
- current smoking level
- current alcohol level
- exercise level
- sleep baseline
- stress baseline
- other static descriptors

### Intervention / exposure records
These are intervention events:
- started medication
- stopped medication
- dose changed
- alcohol reduced
- exercise increased
- major diet change
- similar discrete longitudinal changes

### Practical rule
- baseline descriptors stay in context
- discrete changes with longitudinal relevance become intervention/exposure records

### Relationship to BE-S0
BE-S0 remains input hardening.  
The intervention-effects registry remains canonical effect knowledge.  
They should be linked, not merged.

---

## 7. Recommended execution sequence

### Recommended order

1. intervention registry schema + validator + v1 class rows + alias-map skeleton
2. narrow hypothesis-schema amendment for intervention references, after class IDs are stable
3. alias-map population and tests
4. user intervention / exposure record schema, potentially overlapping with BE-S0b implementation

### Why
- stable class IDs must exist before hypotheses can reference them
- avoids dangling references
- keeps each sprint bounded

---

## 8. Blockers or required preconditions

1. Hypothesis objects have no intervention hook today  
   A later optional-field amendment is required if hypotheses are to reference intervention classes cleanly.

2. Phase-1 medication boundary must be respected  
   Registry content can represent caveats, confounders, expected effects, and monitoring relevance, but not threshold modification or signal-firing override logic.

3. No single AB/VR panel manifest was found  
   Scope was inferred from repo evidence. A dedicated future panel manifest would tighten later pruning decisions.

4. Existing `intervention_library_v1.yaml` must not be confused with the new registry  
   It is user-facing suggested actions, not a canonical pharmacologic/intervention-effects registry.

---

## Bottom line

The clean architecture is:

- intervention class IDs plus `relation_type` on hypotheses in a later small schema patch
- canonical effects and aliases in a dedicated KB registry with its own validator
- deterministic mapping before reasoning
- BE-S0 as input hardening that feeds class IDs, not as the registry itself

This keeps HealthIQ out of drug-library territory, keeps canonical knowledge separate from user state, and avoids rewriting the intelligence model later.