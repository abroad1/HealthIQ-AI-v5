You are producing a tightly scoped design decision document for HealthIQ AI.

This is not a coding task.
This is not a frontend build task.
This is not a broad research paper.

Your job is to define the **Interpretation Display Layer** that must exist before HealthIQ can implement Section 5 (“Patterns across your body”) in a governed, medically credible, and commercially aligned way.

This document is the bridge between:
- our existing internal interpretation entities
- our taxonomy research
- our commercial screening strategy
- the future frontend pattern layer

Important context

We have already completed:
1. a results journey strategy defining Section 5 as a middle interpretation layer
2. taxonomy research showing that not every current entity should be called a phenotype
3. commercial screening research showing that future expansion should align to high-value domains such as:
   - dysglycaemia / insulin resistance
   - atherogenic cardiometabolic risk
   - CKD / kidney risk
   - MASLD / liver fibrosis risk
   - integrated metabolic clustering
   - iron deficiency as a secondary high-volume lane
4. an existence-check sprint which concluded that the current system does **not** yet have a governed interpretation-display layer strong enough for frontend implementation

So this document must not ask whether a display layer is needed.
It is needed.

Your job is to define what that display layer should be.

Core objective

Define the **governed interpretation-display contract** that HealthIQ should build before implementing the frontend “Patterns across your body” layer.

This must include:

- classification model
- naming model
- mapping from current internal entities
- required display fields
- optional display fields
- rules for when “phenotype” is allowed
- alignment with future commercial screening strategy

This is a design lock document, not an implementation prompt.

---

## Required tasks

### 1. Define the interpretation classification model

Define the allowed scientific/display classes for HealthIQ’s interpretation layer.

At minimum, address:

- phenotype
- risk construct
- syndrome/state
- organ-pattern

For each class, define:
- what it means
- when it should be used
- when it should not be used
- whether it is suitable for retail UI
- whether the word “phenotype” can appear on the frontend for that class

Be strict.
Do not allow sloppy overlap.

---

### 2. Map the current 9 governed entities into that model

Current entities:

- `ph_vascular_hcy_inflammation_v1`
- `ph_renal_stress_v1`
- `ph_metabolic_early_ir_v1`
- `ph_thyroid_lipid_disturbance_v1`
- `ph_iron_deficiency_inflammation_v1`
- `ph_iron_overload_v1`
- `ph_hba1c_metabolic_stress_v1`
- `ph_hepatic_alt_inflammatory_v1`
- `ph_tsh_axis_metabolic_v1`

For each entity, define:

- internal id
- recommended scientific class
- approved clinical display label
- approved retail/plain-English label
- short why-it-matters statement
- whether “phenotype” is allowed on the frontend
- rationale

This must be grounded in the prior naming/taxonomy direction.
Do not invent a new taxonomy.

---

### 3. Define the display contract fields

Specify the fields the interpretation-display layer should contain for each entity.

At minimum, decide whether the contract should include:

- internal_id
- scientific_class
- clinical_display_label
- retail_display_label
- subtitle
- why_it_matters
- severity/status
- supporting_biomarkers_summary
- supporting_systems_summary
- user_safe_description
- frontend_allowed_term
- future_commercial_domain
- display_order_priority
- enabled_for_frontend
- confidence/display caveat field

For each field, state:
- required / optional / not needed
- why

Do not over-design.
Only include fields that genuinely help the frontend and governance model.

---

### 4. Define frontend rendering requirements

Without designing visuals, define what a Section 5 “pattern card” must minimally contain.

For example:
- display label
- subtitle
- why-it-matters
- supporting marker/system summary
- severity/state
- optional expand-for-more detail

Be explicit about:
- what the frontend must have
- what is nice-to-have
- what should not be shown

---

### 5. Define naming rules

Create strict naming rules for the interpretation display layer.

Address:
- when a label should be clinical
- when a plain-English subtitle is mandatory
- when the word “phenotype” is allowed
- which terms should be avoided
- whether generic buckets like “Metabolic Health” or “Organ Health” are acceptable
- how to avoid drift across product, commercial, and technical surfaces

This section should be operational, not philosophical.

---

### 6. Align to commercial strategy

For each current entity, comment on whether it aligns to one of the commercially valuable future domains.

Then state:
- which current entities already fit the long-term screening strategy well
- which are weaker or secondary
- what this implies for future interpretation expansion

This does not require future roadmap design in detail.
It does require strategic alignment.

---

### 7. End with a clear design decision

The document must end by stating clearly:

- what the interpretation-display layer should be
- what fields it must contain
- how the current 9 map into it
- which naming/classification rules are locked
- what implementation sprint should be done next

---

## Output format

Write the document with these sections:

1. Executive summary
2. Why this layer is needed
3. Interpretation classification model
4. Current 9-entity mapping table
5. Recommended display contract fields
6. Frontend rendering requirements for Section 5
7. Naming rules
8. Commercial alignment note
9. Final design decision
10. Next implementation consequence

---

## Important constraints

- Do not write code
- Do not write a Cursor sprint prompt
- Do not re-run the broad research from scratch
- Do not speculate beyond the current 9 unless needed for commercial alignment commentary
- Do not call everything a phenotype
- Do not produce vague strategy language
- Be concrete enough that this can become the direct basis for the next implementation sprint

---

## Final instruction

This document must be good enough that, once approved, it can serve as the governing design lock for the future Section 5 interpretation-display contract.

Be precise.
Be disciplined.
Be implementation-aware.