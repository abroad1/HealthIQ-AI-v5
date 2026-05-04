# HealthIQ AI — Interpretation Display Layer: Governed Design Lock Document

**Status: Design Decision Document — for approval before implementation**
**Date: 2026-04-16**
**Scope: Section 5 "Patterns across your body" — interpretation-display contract**

---

## 1. Executive Summary

HealthIQ currently has nine governed interpretation entities prefixed `ph_`. These entities produce signals that drive analytical output, but there is no governed display contract specifying how those entities should be named, classified, or rendered for a user-facing frontend layer.

This document defines that contract.

It locks the following:

- A four-class interpretation classification model
- The correct class for each of the nine current entities
- Approved clinical and retail labels for each entity
- The minimum required fields for the display contract
- Strict naming rules including when "phenotype" is and is not permitted
- Alignment of each entity to the commercial screening strategy

This document is the governing design lock. Once approved, no implementation sprint for Section 5 should proceed without compliance with this contract.

---

## 2. Why This Layer Is Needed

The current system produces interpretation signals but does not govern how those signals are described, classified, or presented. Three problems follow from this gap:

**Problem 1 — Classification inconsistency.** All nine entities use the `ph_` prefix, suggesting they are all phenotypes. They are not. Several are risk constructs. Several are organ-level stress patterns. Using a single classification creates scientific imprecision and exposes the product to challenge.

**Problem 2 — No approved display labels.** The entities have internal IDs. There is no governed, approved translation from internal ID to a label that can appear on a user screen. This means any frontend implementation would either invent labels ad hoc or render the internal ID, both of which are unacceptable.

**Problem 3 — No language governance.** The word "phenotype" is sensitive in a retail context. Without a contract that explicitly states whether each entity is allowed to use this word, frontends and marketing surfaces will make inconsistent choices. The contract must eliminate this ambiguity.

The existence-check sprint already confirmed: this layer does not currently exist in a form strong enough for frontend implementation. This document defines what it must become.

---

## 3. Interpretation Classification Model

Four classes are defined. These are not exhaustive scientific categories. They are the classes HealthIQ needs to govern its current and near-future interpretation layer correctly.

---

### Class A — Phenotype

**Definition:** A reproducible, multi-system biological pattern with established mechanistic basis, population-level evidence, and a stable clinical identity. A phenotype reflects what a person biologically is in a measurable, sustained sense — not merely a risk they carry.

**Use when:**
- The entity has a defined, named clinical phenotype (e.g., metabolic syndrome, haemochromatosis phenotype)
- Multi-system evidence convergence exists
- The entity is stable and trait-like, not transient
- Population prevalence and risk association are well-characterised

**Do not use when:**
- The signal reflects early-stage or sub-clinical risk that has not yet reached phenotypic expression
- The entity is organ-localised without cross-system convergence
- The classification would require inferring genetic basis that has not been tested

**Suitable for retail UI:** Only with a plain-English subtitle. The word "phenotype" itself is not suitable for the retail layer unless the user population is clinical.

**"Phenotype" allowed on frontend:** No, for the current nine entities (see Section 4). In future, only if an entity has a formally established clinical phenotype with confirmed multi-system convergence, and only with clinical-context framing.

---

### Class B — Risk Construct

**Definition:** A composite signal derived from two or more biomarkers indicating elevated probability of a current sub-clinical condition or a future clinical event. The risk construct does not assert that a condition is present; it asserts that a pattern of risk markers is elevated.

**Use when:**
- The signal is driven by two or more convergent biomarkers
- The primary value is predictive or indicative, not diagnostic
- The entity does not yet meet the threshold for a defined clinical syndrome or phenotype
- The appropriate user message is "your markers suggest elevated risk of X", not "you have X"

**Do not use when:**
- The entity has a recognised clinical syndrome definition (use Syndrome/State instead)
- The signal is localised to a single organ without a cross-system composite (use Organ-Pattern instead)

**Suitable for retail UI:** Yes. Risk constructs are the workhorse of consumer health displays.

**"Phenotype" allowed on frontend:** No.

---

### Class C — Syndrome / State

**Definition:** A recognised clinical entity with an established definition, ICD-adjacent identity, or widely accepted clinical consensus. Unlike a phenotype, a syndrome is defined by a co-occurrence of signs and markers meeting a threshold, not by biological trait. Unlike a risk construct, a syndrome asserts a current state, not merely a risk.

**Use when:**
- A recognised clinical framework defines the entity (e.g., iron deficiency anaemia, subclinical hypothyroidism)
- The biomarker pattern meets or approaches a threshold that has clinical consensus
- The entity describes a current condition, not a future risk

**Do not use when:**
- The entity is early-stage risk without meeting threshold criteria
- The entity does not have established clinical consensus

**Suitable for retail UI:** Yes, with mandatory plain-English translation. The word "syndrome" is acceptable in a clinical display label but must be simplified for the retail label.

**"Phenotype" allowed on frontend:** No.

---

### Class D — Organ-Pattern

**Definition:** A pattern of dysfunction or stress localised to a specific organ or physiological system, evidenced by organ-specific biomarkers. An organ-pattern does not assert systemic disease; it asserts that a particular organ's markers are elevated in a pattern that warrants attention.

**Use when:**
- The signal is organ-localised (e.g., liver, kidney, thyroid axis)
- The biomarkers are primarily organ-function markers rather than systemic risk markers
- The entity reflects a signal cluster, not a composite risk score

**Do not use when:**
- The entity involves multi-organ or multi-system convergence (use Risk Construct or Phenotype instead)

**Suitable for retail UI:** Yes. Organ-patterns translate well to plain language ("liver stress markers", "kidney stress markers").

**"Phenotype" allowed on frontend:** No.

---

**Overlap rule:** Where an entity could plausibly belong to two classes, apply the more conservative class. A risk construct with organ-localised markers should use Organ-Pattern. A syndrome with strong risk-predictive framing should use Syndrome/State. When in doubt, the class that makes the weakest assertion takes precedence. This prevents over-claiming.

---

## 4. Current 9-Entity Mapping Table

| Internal ID | Recommended Class | Clinical Display Label | Retail Display Label | Why It Matters (1 sentence) | "Phenotype" on frontend | Rationale |
|---|---|---|---|---|---|---|
| `ph_metabolic_early_ir_v1` | Risk Construct | Early Insulin Resistance Risk Pattern | Early signs of insulin resistance | Insulin resistance is a foundational driver of type 2 diabetes and metabolic disease; detecting it early creates the largest window for intervention. | No | Pattern meets early composite signal criteria but has not yet crossed into established metabolic syndrome threshold; risk construct is the correct and more conservative class. |
| `ph_hba1c_metabolic_stress_v1` | Risk Construct | HbA1c-Indicated Metabolic Stress | Blood sugar regulation under stress | Sustained elevation in HbA1c indicates that blood sugar regulation has been impaired for months, not days, and represents meaningful metabolic risk. | No | HbA1c plus metabolic markers is a composite risk signal. The entity does not assert diabetes; it asserts a risk pattern. |
| `ph_hepatic_alt_inflammatory_v1` | Organ-Pattern | Hepatic Stress Pattern (ALT-Inflammatory) | Liver stress markers elevated | Elevated liver enzymes alongside inflammation suggest the liver is under stress, which may indicate early metabolic liver involvement. | No | Signal is organ-localised to the liver. ALT elevation plus inflammatory co-signal is a hepatic stress pattern, not a multi-system phenotype. |
| `ph_renal_stress_v1` | Organ-Pattern | Renal Stress Pattern | Kidney stress markers elevated | Kidney stress markers indicate that the kidneys may be working harder than normal, which warrants monitoring and possible follow-up. | No | Organ-localised signal. Renal stress markers do not constitute a multi-system risk construct at this stage. |
| `ph_iron_deficiency_inflammation_v1` | Syndrome / State | Iron Deficiency with Concurrent Inflammation | Iron deficiency with inflammatory context | Iron deficiency is common and impactful; when combined with elevated inflammation, it may reflect a more complex picture than simple dietary deficiency. | No | Iron deficiency has established clinical criteria. The co-occurring inflammation is a modifier. The entity describes a current state, not a risk probability. |
| `ph_vascular_hcy_inflammation_v1` | Risk Construct | Vascular Inflammatory Risk Pattern | Raised vascular and inflammatory markers | Elevated homocysteine combined with inflammatory markers suggests increased vascular stress that may be relevant to cardiovascular and cerebrovascular risk. | No | Composite signal spanning vascular and inflammatory pathways. Not a phenotype; no established named phenotype corresponds to this specific combination at sub-clinical levels. |
| `ph_thyroid_lipid_disturbance_v1` | Functional State (sub-class of Syndrome/State) | Thyroid-Mediated Lipid Disturbance | Thyroid and cholesterol signals linked | Thyroid function directly influences cholesterol metabolism; when both are disturbed together, it suggests thyroid axis dysfunction may be driving lipid changes. | No | Thyroid dysfunction affecting lipid output is a functional state, not a phenotype. The entity reflects a causal pattern rather than a stable biological trait. |
| `ph_tsh_axis_metabolic_v1` | Functional State (sub-class of Syndrome/State) | TSH Axis Metabolic Disturbance | Thyroid function affecting metabolism | TSH variations can subtly influence metabolic rate, energy regulation, and downstream markers; this pattern suggests the thyroid axis warrants attention. | No | TSH-level signal affecting metabolic output is a functional state. Without confirmed clinical hypothyroidism or hyperthyroidism, this does not reach phenotype or formal syndrome level. |
| `ph_iron_overload_v1` | Risk Construct | Iron Overload Risk Pattern | Elevated iron storage markers | Chronically elevated iron stores can cause oxidative stress and organ damage; this pattern flags the need for further investigation. | No | Without genetic confirmation of haemochromatosis, elevated ferritin with supporting markers is a risk construct. The entity makes no diagnostic assertion. |

**Note on "Functional State":** This is a recognised sub-class of Syndrome/State used where the entity reflects a functional or axis-level disturbance rather than a named syndrome. It does not require a separate top-level class; it is governed by Syndrome/State rules.

---

## 5. Recommended Display Contract Fields

This defines the fields each governed entity must carry in the interpretation-display layer. The principle: include what the frontend needs; exclude what creates confusion or governance burden without value.

| Field | Required / Optional / Not Needed | Rationale |
|---|---|---|
| `internal_id` | Required | Governance anchor. Every frontend call must be traceable to an internal entity. |
| `scientific_class` | Required | Classification governance. Not rendered directly to users, but governs downstream field choices and audit. |
| `clinical_display_label` | Required | Used in clinical-context surfaces (PDFs, health integrations, detailed views). Precision anchor. |
| `retail_display_label` | Required | The primary user-facing label. Must exist for every entity before any frontend rendering is permitted. |
| `subtitle` | Required | One line contextualising the retail label. Prevents label-only displays that lack meaning. |
| `why_it_matters` | Required | 1–2 sentence user-safe explanation of why this pattern is relevant. Non-negotiable for health literacy and commercial value. |
| `severity_status` | Required | A governed severity or state descriptor (e.g., `detected`, `borderline`, `not_detected`). Frontends need this to render state-appropriate UI. Exact enum to be defined in the implementation sprint. |
| `supporting_biomarkers_summary` | Required | List of the primary biomarkers that drove this entity's detection. Required for transparency and to allow the user to connect the pattern to their own results. |
| `supporting_systems_summary` | Optional | Higher-level organ/system summary (e.g., "Liver, Metabolic"). Useful for complex multi-system entities. Not required for organ-pattern entities where the organ is already in the label. |
| `user_safe_description` | Required | 2–4 sentence plain-English body text. Expands on why_it_matters with more context. Used in expand-for-more detail views. |
| `frontend_allowed_term` | Required | The single governed word or phrase that the frontend may use to describe this entity class (e.g., "pattern", "risk signal", "state"). Eliminates ad hoc language choices. No "phenotype" for any current entity. |
| `future_commercial_domain` | Optional | Alignment tag to a commercial screening domain. Governance and roadmap use only. Not rendered to users. |
| `display_order_priority` | Required | Integer. Controls rendering order within Section 5. Must be set per entity, not computed ad hoc by the frontend. |
| `enabled_for_frontend` | Required | Boolean gate. No entity renders to Section 5 unless explicitly enabled. Prevents partial implementations. |
| `confidence_caveat` | Optional | Short display-safe caveat where a pattern's evidence base is limited or where additional testing is recommended before interpretation. Not required for all entities, but must be available as a governed field for entities that warrant it. |

**Fields not included:**

- Raw biomarker values: these belong in Section 3/4 (the biomarker detail layer), not in the interpretation card.
- Diagnostic language fields: this layer does not diagnose. No ICD code, diagnostic confidence score, or condition-confirmed field should exist at this level.
- Personalised narrative fields: dynamic generation from a user's name, age, or exact values should not be part of the static display contract. These are rendering-layer concerns.

---

## 6. Frontend Rendering Requirements for Section 5

Section 5 renders "Patterns across your body" — a mid-level interpretation layer between raw biomarker results and actionable insight. Each entity should render as a card.

**Must have (non-negotiable):**

- `retail_display_label` — rendered as the card heading
- `subtitle` — rendered as a sub-heading or category line beneath the label
- `why_it_matters` — rendered as the visible body text on the collapsed card
- `supporting_biomarkers_summary` — rendered as a compact marker list (e.g., "Driven by: HbA1c, Fasting glucose, Insulin")
- `severity_status` — rendered as a visual state indicator (colour, badge, or label — implementation decision, but the field must be present and used)

**Nice-to-have (render if present, skip gracefully if absent):**

- Expand-for-more interaction: reveals `user_safe_description` and `clinical_display_label` in an expanded view
- `supporting_systems_summary`: adds a system-level context line for multi-system entities
- `confidence_caveat`: renders as a subdued note below the card body when the field is populated

**Must not appear on the card:**

- `internal_id` — internal governance only
- `scientific_class` — too clinical for retail
- The word "phenotype" for any current entity
- Raw biomarker numeric values — these are Section 3/4 content
- `future_commercial_domain` — internal roadmap field
- Any diagnostic or disease-confirmed language
- Probability scores or confidence percentages (these are not governed for display at this stage)

**Structural requirement:** The `enabled_for_frontend` flag must be checked before rendering any entity. A card must not render for an entity where this flag is false, regardless of whether a detection signal exists.

---

## 7. Naming Rules

These rules are operational. They govern every surface where interpretation entity labels appear: the product UI, marketing materials, PDF reports, and API response labels.

**Rule 1 — Clinical display label standards**
Clinical display labels must use established clinical terminology where it exists. They must not contain colloquialisms, marketing language, or speculative framing. Clinical labels are the precision anchor. If a clinical term does not exist for the pattern, the label must be clearly descriptive without over-claiming (e.g., "Hepatic Stress Pattern (ALT-Inflammatory)" rather than "Liver Disease Risk").

**Rule 2 — Retail label standards**
Every entity must have a retail label. Retail labels must be written at a reading level appropriate for a general adult population. The retail label must not introduce clinical terms that require medical literacy to interpret. Maximum length: 6 words. If 6 words cannot convey the pattern, the subtitle carries the remainder.

**Rule 3 — Subtitle is mandatory**
A retail label without a subtitle is incomplete. The subtitle's job is to add the one piece of context that makes the label meaningful without medical training. Example: label "Liver stress markers elevated", subtitle "Based on your ALT and inflammatory markers". Without a subtitle, the label floats without grounding.

**Rule 4 — "Phenotype" is prohibited in retail UI for all current entities**
None of the nine current entities meet the bar for phenotype designation at the retail display layer. This rule is locked. Future entities may qualify if they meet Class A criteria (Section 3), but that determination requires a governed classification decision, not an ad hoc editorial choice.

**Rule 5 — Prohibited terms in retail labels**
The following terms are prohibited from appearing in any retail-facing label, subtitle, or card body text:

- phenotype, endotype, genotype
- syndrome (except where embedded in an established plain-English term like "metabolic syndrome" in a supporting text context)
- morbidity, comorbidity, pathology, aetiology
- "you have [condition]" (diagnostic framing)
- "your health is…" (vague bucket framing)
- probability percentages or risk scores as primary label components

**Rule 6 — Generic buckets are grouping labels only**
Terms like "Metabolic Health" or "Organ Health" may be used as section grouping labels in the UI. They are not permitted as entity display labels. Each entity must have a specific label. "Metabolic Health" is not a display label for `ph_metabolic_early_ir_v1`.

**Rule 7 — `frontend_allowed_term` is the single source of truth**
The `frontend_allowed_term` field in the display contract governs what class-level term the frontend may use to describe an entity. If the contract says "pattern", the frontend uses "pattern". If it says "risk signal", it uses "risk signal". No deviation without a contract update through the governed sprint process.

**Rule 8 — Label consistency across surfaces**
The `retail_display_label` in the contract is the canonical label. Marketing copy, PDF reports, and any external-facing communication must use this label or a governed derivative. Drift from the contract label is a governance failure. The implementation sprint must make the registry the single source for all surface labels.

---

## 8. Commercial Alignment Note

The six commercially prioritised domains are:
1. Dysglycaemia / insulin resistance
2. Atherogenic cardiometabolic risk
3. CKD / kidney risk
4. MASLD / liver fibrosis risk
5. Integrated metabolic clustering
6. Iron deficiency (secondary high-volume lane)

**Entity alignment:**

| Entity | Commercial Domain Fit | Strength |
|---|---|---|
| `ph_metabolic_early_ir_v1` | #1 Dysglycaemia / insulin resistance | Strong — this is a direct signal in the core commercial lane |
| `ph_hba1c_metabolic_stress_v1` | #1 Dysglycaemia / insulin resistance | Strong — HbA1c is the primary glycaemic screening biomarker |
| `ph_renal_stress_v1` | #3 CKD / kidney risk | Strong — maps cleanly to the kidney risk commercial expansion path |
| `ph_hepatic_alt_inflammatory_v1` | #4 MASLD / liver fibrosis risk | Strong — ALT-inflammatory pattern is the primary liver risk signal in the current system |
| `ph_iron_deficiency_inflammation_v1` | #6 Iron deficiency | Strong — high-volume secondary lane; inflammation modifier adds clinical depth |
| `ph_vascular_hcy_inflammation_v1` | #2 Atherogenic cardiometabolic risk | Moderate — homocysteine is a secondary cardiometabolic marker; inflammation component is relevant but the entity lacks the lipid-centric core of atherogenic risk |
| `ph_iron_overload_v1` | #6 Iron (overload sub-lane) | Moderate — lower volume than deficiency; clinically important but not a primary commercial volume driver |
| `ph_thyroid_lipid_disturbance_v1` | #2 Atherogenic cardiometabolic (lipid component) | Moderate — the lipid disturbance component is commercially relevant; thyroid axis is not itself a primary commercial domain |
| `ph_tsh_axis_metabolic_v1` | No primary domain | Weak — TSH-axis metabolic disturbance does not map cleanly to any of the six priority commercial domains; thyroid functional states are secondary |

**Observations:**

1. **Strongest strategic entities:** `ph_metabolic_early_ir_v1`, `ph_hba1c_metabolic_stress_v1`, `ph_renal_stress_v1`, `ph_hepatic_alt_inflammatory_v1`, and `ph_iron_deficiency_inflammation_v1`. These five entities directly underpin the highest-priority commercial screening domains. They should be treated as the commercial core of the interpretation layer.

2. **Weaker strategic entities:** The two thyroid-axis entities (`ph_thyroid_lipid_disturbance_v1`, `ph_tsh_axis_metabolic_v1`) have partial commercial relevance via lipid and metabolic signals but thyroid is not a top-tier commercial domain. These entities carry clinical value but should not anchor commercial expansion strategy. Future consolidation of the two thyroid entities into a single entity should be considered.

3. **Secondary lane:** `ph_iron_overload_v1` and the vascular/homocysteine entity are real clinical signals but sit outside the primary commercial expansion path. They should be maintained and displayed, but are not candidates for commercial differentiation.

4. **Future expansion implication:** The current nine entities do not include an explicit atherogenic dyslipidaemia entity or an integrated metabolic cluster entity. Both of these are named commercial priorities. The next round of interpretation entity creation — after this display contract is implemented — should address those gaps.

---

## 9. Final Design Decision

**What the interpretation-display layer should be:**

A governed SSOT registry — `interpretation_display_registry.yaml` — containing one entry per governed interpretation entity, carrying the full display contract for that entity. This registry is the single source of truth for all frontend rendering of Section 5 content. No implementation may generate Section 5 cards from any other source.

**Fields it must contain:**

Required: `internal_id`, `scientific_class`, `clinical_display_label`, `retail_display_label`, `subtitle`, `why_it_matters`, `severity_status` (enum), `supporting_biomarkers_summary`, `user_safe_description`, `frontend_allowed_term`, `display_order_priority`, `enabled_for_frontend`

Optional (must be available as governed fields): `supporting_systems_summary`, `confidence_caveat`, `future_commercial_domain`

**How the current nine map into it:**

All nine current entities have been mapped. Classifications are locked in Section 4. None of the nine are classified as phenotypes. None permit "phenotype" on the retail frontend. Five are risk constructs; two are organ-patterns; two are functional states (sub-class of syndrome/state).

**Naming and classification rules that are locked:**

- Four-class model: Phenotype, Risk Construct, Syndrome/State, Organ-Pattern (with Functional State as a sub-class)
- "Phenotype" is prohibited on the retail frontend for all nine current entities
- Eight prohibited terms defined in Section 7
- `frontend_allowed_term` field is the single source of truth for class-level language
- Generic buckets are grouping labels only — not entity labels
- Retail labels: maximum 6 words, GCSE reading level, no clinical jargon

**What implementation sprint should be done next:**

A single CONTENT sprint to create `interpretation_display_registry.yaml` implementing this contract for all nine entities, with all required fields populated and `enabled_for_frontend` explicitly set for each entity. This sprint has no behavioural scope — it creates a data registry. It becomes MIXED risk when the frontend or any compiler loads from it.

---

## 10. Next Implementation Consequence

The governing pre-condition for Section 5 frontend implementation is this registry existing in a complete and approved state.

The next sprint must:

1. Create `interpretation_display_registry.yaml` in the appropriate SSOT location
2. Populate all required fields for all nine entities, using the classifications and labels locked in this document
3. Define the `severity_status` enum (e.g., `detected`, `borderline`, `not_detected`, `insufficient_signal`) as part of the registry schema — this enum must be locked before any frontend implementation begins
4. Set `enabled_for_frontend` explicitly for each entity
5. Produce a schema definition file for the registry contract so downstream loaders can validate against it

**This sprint must not:**
- Modify any analytical pipeline, evaluator, or compiler
- Change any existing entity detection logic
- Introduce any frontend rendering code
- Expand the entity set beyond the current nine

**After the registry exists and is approved**, a subsequent BEHAVIOUR sprint may wire a frontend loader to this registry, at which point risk classification escalates to HIGH and Intelligence Core rules apply.

Until the registry sprint is complete and merged, Section 5 frontend implementation must not proceed.

---

*Document ends.*
