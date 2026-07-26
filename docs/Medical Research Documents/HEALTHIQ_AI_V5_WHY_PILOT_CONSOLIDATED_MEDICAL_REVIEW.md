# HealthIQ AI v5 — WHY Pilot Consolidated Medical Review Pack

**Work ID:** `ARCH-CONV-PKG3`  
**Branch:** `feature/arch-conv-pkg3-why-authority-migration`  
**Artefact form:** One consolidated five-signal pack / **ten frame-level sections** (Gate 2.5 ratified)  
**Assembled by:** Cursor (evidence pack only)  
**Medical decisions:** **NOT made by Cursor** — awaiting GPT (Head of Medical Research) then Anthony ratification

## Authority banner

| Role | Named party |
|---|---|
| Structured medical review | GPT — HealthIQ AI Head of Medical Research |
| Production ratification | Anthony |
| Engineering | Implements only Anthony-ratified frame decisions |

GPT review alone is never production authorisation.

## Mandatory STOP Gate C

This pack is handed to GPT and Anthony. **Package 3 Phase 4–6 must not continue** until every frame below has an explicit GPT decision and an explicit Anthony ratification recorded in this artefact (or an authorised companion update).

## Cohort

Exactly **5** signal families / **10** activation frames. No additions.

---

## Frame 1 — `signal_vitamin_d_low::inv_vitamin_d_low_deficiency`

### Frame identity

| Field | Value |
|---|---|
| signal_id | `signal_vitamin_d_low` |
| activation_key | `signal_vitamin_d_low::inv_vitamin_d_low_deficiency` |
| source_spec_id | `inv_vitamin_d_low_deficiency` |
| package_id | `pkg_s24_vitamin_d_low_deficiency` |
| review class | RETIREMENT_CONFIRMATION_ONLY |
| current legacy / runtime WHY authority | COMPILED_ACTIVE (RUNTIME_PROMOTED_COMPILED_SIGNAL_IDS); legacy YAML still on disk |
| proposed compiled authority | Candidate compiled artefact path: `knowledge_bus/compiled/hypotheses/signal_vitamin_d_low.yaml` — **not promoted in this pack** |
| consumer surface | Not in _LEAD_SIGNAL_HINTS |
| clinician surface | Compiled root-cause branch when promoted |

### Medical interpretation (evidence excerpt — not a GPT decision)

| Field | Evidence from repository assets |
|---|---|
| Primary marker | `vitamin_d` — 25-hydroxyvitamin D is the best indicator of total body Vitamin D stores, essential for calcium homeostasis and bone health. |
| Trigger direction | `low` |
| Narrative interpretation (inv) | Low levels are common in higher latitudes. Severe deficiency leads to rickets (children) or osteomalacia (adults). |
| Mechanism (inv) | Regulates calcium and phosphate metabolism for bone mineralization. |

### Evidence summary

| Artefact | Path / status |
|---|---|
| Investigation specification | `knowledge_bus/research/investigation_specs/inv_vitamin_d_low_deficiency.yaml` (or `_v1`) — AVAILABLE |
| Legacy WHY YAML | `knowledge_bus/root_cause/hypotheses/vitamin_d_low_hypotheses_v1.yaml` — hypothesis ids: `vitamin_d_nutritional_status_context_v1` |
| Compiled artefact | `knowledge_bus/compiled/hypotheses/signal_vitamin_d_low.yaml` |
| Package | `knowledge_bus/packages/pkg_s24_vitamin_d_low_deficiency/` |

### Investigation-spec hypotheses (source research; not approved)

- _(no hypotheses block in investigation specification)_

### Causal limits / wording / modifiers / parity (for GPT completion)

| Field | Cursor assembly note | GPT completion |
|---|---|---|
| Causal limits | Derive from inv caveats / contradiction markers; do not invent | |
| Consumer wording boundary | Must remain non-diagnostic; respect lead-hint surfaces | |
| Clinician wording boundary | Root-cause compiler boundaries; no prescribing | |
| Approved hypotheses | Leave blank until GPT decides | |
| Rejected hypotheses | Leave blank until GPT decides | |
| Uncertainty | | |
| Confirmatory-test context | Inv confirmatory_tests / legacy confirmatory markers | |
| Modifier compatibility | Package gates / context requirements where present | |
| Legacy-parity assessment | Shared YAML families (hcy/mcv/tpo) require per-frame care | |

### Proposed production disposition

**PENDING_GPT_MEDICAL_REVIEW** — Cursor does **not** select among APPROVE_FOR_COMPILED_PROMOTION / APPROVE_WITH_REVISIONS / REJECT / DEFER_PENDING_RESEARCH / RETIREMENT_CONFIRMATION_ONLY.

Allowed after GPT review (exact one):

```text
APPROVE_FOR_COMPILED_PROMOTION
APPROVE_WITH_REVISIONS
REJECT
DEFER_PENDING_RESEARCH
RETIREMENT_CONFIRMATION_ONLY
```

### GPT medical-review decision (Gate C — open)

| Field | Value |
|---|---|
| GPT decision | |
| Required revisions | |
| Reviewer | GPT — HealthIQ AI Head of Medical Research |
| Review date (UTC) | |

### Anthony ratification (Gate C — open)

| Field | Value |
|---|---|
| Ratification decision | APPROVED / REJECTED / DEFERRED |
| Final implementation disposition | |
| Ratifier | Anthony |
| Ratification date (UTC) | |

**No blank, implied, batch-level, or inherited ratification is permitted. No frame may inherit approval from a sibling frame in the same signal family.**

---

## Frame 2 — `signal_homocysteine_high::inv_homocysteine_high_b_vitamin_related_methylation_impairment`

### Frame identity

| Field | Value |
|---|---|
| signal_id | `signal_homocysteine_high` |
| activation_key | `signal_homocysteine_high::inv_homocysteine_high_b_vitamin_related_methylation_impairment` |
| source_spec_id | `inv_homocysteine_high_b_vitamin_related_methylation_impairment` |
| package_id | `pkg_kb52c_homocysteine_high_b_vitamin_related_methylation_impairment` |
| review class | FULL_NEW_MEDICAL_REVIEW |
| current legacy / runtime WHY authority | LEGACY_ACTIVE via shared hcy_hypotheses_v1.yaml |
| proposed compiled authority | Candidate compiled artefact path: `_(none — candidate not compiled)_` — **not promoted in this pack** |
| consumer surface | Lead hint (family) |
| clinician surface | Legacy root-cause registry |

### Medical interpretation (evidence excerpt — not a GPT decision)

| Field | Evidence from repository assets |
|---|---|
| Primary marker | `homocysteine` — Homocysteine is a methylation-pathway intermediate and rises most commonly with folate, B12, or B6 insufficiency, renal impairment, or genetic pathway variation. |
| Trigger direction | `high` |
| Narrative interpretation (inv) | High homocysteine is biologically informative but not disease-specific on its own. |
| Mechanism (inv) | Homocysteine rises when one-carbon metabolism is limited or when renal clearance is reduced. |

### Evidence summary

| Artefact | Path / status |
|---|---|
| Investigation specification | `knowledge_bus/research/investigation_specs/inv_homocysteine_high_b_vitamin_related_methylation_impairment.yaml` (or `_v1`) — AVAILABLE |
| Legacy WHY YAML | `knowledge_bus/root_cause/hypotheses/hcy_hypotheses_v1.yaml` — hypothesis ids: `hcy_b12_pattern_v1`, `hcy_folate_pattern_v1`, `hcy_inflammation_context_v1`, `hcy_renal_clearance_context_v1` |
| Compiled artefact | `_(none — candidate not compiled)_` |
| Package | `knowledge_bus/packages/pkg_kb52c_homocysteine_high_b_vitamin_related_methylation_impairment/` |

### Investigation-spec hypotheses (source research; not approved)

- `hyp_folate_related_hyperhomocysteinemia` — High homocysteine may reflect folate-related impairment of remethylation, particularly when folate is low and macrocytic change is present.
- `hyp_b12_related_or_combined_methylation_impairment` — High homocysteine may also reflect cobalamin deficiency or combined B-vitamin insufficiency, especially when active B12 is low.

### Causal limits / wording / modifiers / parity (for GPT completion)

| Field | Cursor assembly note | GPT completion |
|---|---|---|
| Causal limits | Derive from inv caveats / contradiction markers; do not invent | |
| Consumer wording boundary | Must remain non-diagnostic; respect lead-hint surfaces | |
| Clinician wording boundary | Root-cause compiler boundaries; no prescribing | |
| Approved hypotheses | Leave blank until GPT decides | |
| Rejected hypotheses | Leave blank until GPT decides | |
| Uncertainty | | |
| Confirmatory-test context | Inv confirmatory_tests / legacy confirmatory markers | |
| Modifier compatibility | Package gates / context requirements where present | |
| Legacy-parity assessment | Shared YAML families (hcy/mcv/tpo) require per-frame care | |

### Proposed production disposition

**PENDING_GPT_MEDICAL_REVIEW** — Cursor does **not** select among APPROVE_FOR_COMPILED_PROMOTION / APPROVE_WITH_REVISIONS / REJECT / DEFER_PENDING_RESEARCH / RETIREMENT_CONFIRMATION_ONLY.

Allowed after GPT review (exact one):

```text
APPROVE_FOR_COMPILED_PROMOTION
APPROVE_WITH_REVISIONS
REJECT
DEFER_PENDING_RESEARCH
RETIREMENT_CONFIRMATION_ONLY
```

### GPT medical-review decision (Gate C — open)

| Field | Value |
|---|---|
| GPT decision | |
| Required revisions | |
| Reviewer | GPT — HealthIQ AI Head of Medical Research |
| Review date (UTC) | |

### Anthony ratification (Gate C — open)

| Field | Value |
|---|---|
| Ratification decision | APPROVED / REJECTED / DEFERRED |
| Final implementation disposition | |
| Ratifier | Anthony |
| Ratification date (UTC) | |

**No blank, implied, batch-level, or inherited ratification is permitted. No frame may inherit approval from a sibling frame in the same signal family.**

---

## Frame 3 — `signal_homocysteine_high::inv_homocysteine_high_metabolic`

### Frame identity

| Field | Value |
|---|---|
| signal_id | `signal_homocysteine_high` |
| activation_key | `signal_homocysteine_high::inv_homocysteine_high_metabolic` |
| source_spec_id | `inv_homocysteine_high_metabolic` |
| package_id | `pkg_s24_homocysteine_high_metabolic` |
| review class | FULL_NEW_MEDICAL_REVIEW |
| current legacy / runtime WHY authority | LEGACY_ACTIVE via shared hcy_hypotheses_v1.yaml |
| proposed compiled authority | Candidate compiled artefact path: `_(none — candidate not compiled)_` — **not promoted in this pack** |
| consumer surface | Lead hint (family) |
| clinician surface | Legacy root-cause registry |

### Medical interpretation (evidence excerpt — not a GPT decision)

| Field | Evidence from repository assets |
|---|---|
| Primary marker | `homocysteine` — Homocysteine is a non-protein amino acid. Elevated levels (hyperhomocysteinemia) are a sensitive marker for B-vitamin deficiencies and an independent risk factor for vascular injury and cognitive decline. |
| Trigger direction | `high` |
| Narrative interpretation (inv) | Reflects methylation capacity and B-vitamin status. |
| Mechanism (inv) | Homocysteine lies at the junction of the remethylation and transsulfuration pathways. |

### Evidence summary

| Artefact | Path / status |
|---|---|
| Investigation specification | `knowledge_bus/research/investigation_specs/inv_homocysteine_high_metabolic.yaml` (or `_v1`) — AVAILABLE |
| Legacy WHY YAML | `knowledge_bus/root_cause/hypotheses/hcy_hypotheses_v1.yaml` — hypothesis ids: `hcy_b12_pattern_v1`, `hcy_folate_pattern_v1`, `hcy_inflammation_context_v1`, `hcy_renal_clearance_context_v1` |
| Compiled artefact | `_(none — candidate not compiled)_` |
| Package | `knowledge_bus/packages/pkg_s24_homocysteine_high_metabolic/` |

### Investigation-spec hypotheses (source research; not approved)

- _(no hypotheses block in investigation specification)_

### Causal limits / wording / modifiers / parity (for GPT completion)

| Field | Cursor assembly note | GPT completion |
|---|---|---|
| Causal limits | Derive from inv caveats / contradiction markers; do not invent | |
| Consumer wording boundary | Must remain non-diagnostic; respect lead-hint surfaces | |
| Clinician wording boundary | Root-cause compiler boundaries; no prescribing | |
| Approved hypotheses | Leave blank until GPT decides | |
| Rejected hypotheses | Leave blank until GPT decides | |
| Uncertainty | | |
| Confirmatory-test context | Inv confirmatory_tests / legacy confirmatory markers | |
| Modifier compatibility | Package gates / context requirements where present | |
| Legacy-parity assessment | Shared YAML families (hcy/mcv/tpo) require per-frame care | |

### Proposed production disposition

**PENDING_GPT_MEDICAL_REVIEW** — Cursor does **not** select among APPROVE_FOR_COMPILED_PROMOTION / APPROVE_WITH_REVISIONS / REJECT / DEFER_PENDING_RESEARCH / RETIREMENT_CONFIRMATION_ONLY.

Allowed after GPT review (exact one):

```text
APPROVE_FOR_COMPILED_PROMOTION
APPROVE_WITH_REVISIONS
REJECT
DEFER_PENDING_RESEARCH
RETIREMENT_CONFIRMATION_ONLY
```

### GPT medical-review decision (Gate C — open)

| Field | Value |
|---|---|
| GPT decision | |
| Required revisions | |
| Reviewer | GPT — HealthIQ AI Head of Medical Research |
| Review date (UTC) | |

### Anthony ratification (Gate C — open)

| Field | Value |
|---|---|
| Ratification decision | APPROVED / REJECTED / DEFERRED |
| Final implementation disposition | |
| Ratifier | Anthony |
| Ratification date (UTC) | |

**No blank, implied, batch-level, or inherited ratification is permitted. No frame may inherit approval from a sibling frame in the same signal family.**

---

## Frame 4 — `signal_homocysteine_high::inv_homocysteine_high_renal_clearance_reduction`

### Frame identity

| Field | Value |
|---|---|
| signal_id | `signal_homocysteine_high` |
| activation_key | `signal_homocysteine_high::inv_homocysteine_high_renal_clearance_reduction` |
| source_spec_id | `inv_homocysteine_high_renal_clearance_reduction` |
| package_id | `pkg_kb52c_homocysteine_high_renal_clearance_reduction` |
| review class | FULL_NEW_MEDICAL_REVIEW |
| current legacy / runtime WHY authority | LEGACY_ACTIVE via shared hcy_hypotheses_v1.yaml |
| proposed compiled authority | Candidate compiled artefact path: `_(none — candidate not compiled)_` — **not promoted in this pack** |
| consumer surface | Lead hint (family) |
| clinician surface | Legacy root-cause registry |

### Medical interpretation (evidence excerpt — not a GPT decision)

| Field | Evidence from repository assets |
|---|---|
| Primary marker | `homocysteine` — Homocysteine is partly cleared by the kidney, so elevation can reflect renal impairment even without a primary hematinic defect. |
| Trigger direction | `high` |
| Narrative interpretation (inv) | High homocysteine in renal impairment is a contextual biochemical consequence and should not be over-interpreted as a vitamin deficiency by default. |
| Mechanism (inv) | Homocysteine accumulates when renal filtration and metabolic handling are reduced. |

### Evidence summary

| Artefact | Path / status |
|---|---|
| Investigation specification | `knowledge_bus/research/investigation_specs/inv_homocysteine_high_renal_clearance_reduction.yaml` (or `_v1`) — AVAILABLE |
| Legacy WHY YAML | `knowledge_bus/root_cause/hypotheses/hcy_hypotheses_v1.yaml` — hypothesis ids: `hcy_b12_pattern_v1`, `hcy_folate_pattern_v1`, `hcy_inflammation_context_v1`, `hcy_renal_clearance_context_v1` |
| Compiled artefact | `_(none — candidate not compiled)_` |
| Package | `knowledge_bus/packages/pkg_kb52c_homocysteine_high_renal_clearance_reduction/` |

### Investigation-spec hypotheses (source research; not approved)

- `hyp_renal_hyperhomocysteinemia` — High homocysteine with impaired renal function may reflect reduced renal clearance or metabolism rather than isolated vitamin deficiency.
- `hyp_combined_renal_and_hematinic_context` — High homocysteine may arise from combined renal impairment and hematinic insufficiency, especially when creatinine and B-vitamin markers are both abnormal.

### Causal limits / wording / modifiers / parity (for GPT completion)

| Field | Cursor assembly note | GPT completion |
|---|---|---|
| Causal limits | Derive from inv caveats / contradiction markers; do not invent | |
| Consumer wording boundary | Must remain non-diagnostic; respect lead-hint surfaces | |
| Clinician wording boundary | Root-cause compiler boundaries; no prescribing | |
| Approved hypotheses | Leave blank until GPT decides | |
| Rejected hypotheses | Leave blank until GPT decides | |
| Uncertainty | | |
| Confirmatory-test context | Inv confirmatory_tests / legacy confirmatory markers | |
| Modifier compatibility | Package gates / context requirements where present | |
| Legacy-parity assessment | Shared YAML families (hcy/mcv/tpo) require per-frame care | |

### Proposed production disposition

**PENDING_GPT_MEDICAL_REVIEW** — Cursor does **not** select among APPROVE_FOR_COMPILED_PROMOTION / APPROVE_WITH_REVISIONS / REJECT / DEFER_PENDING_RESEARCH / RETIREMENT_CONFIRMATION_ONLY.

Allowed after GPT review (exact one):

```text
APPROVE_FOR_COMPILED_PROMOTION
APPROVE_WITH_REVISIONS
REJECT
DEFER_PENDING_RESEARCH
RETIREMENT_CONFIRMATION_ONLY
```

### GPT medical-review decision (Gate C — open)

| Field | Value |
|---|---|
| GPT decision | |
| Required revisions | |
| Reviewer | GPT — HealthIQ AI Head of Medical Research |
| Review date (UTC) | |

### Anthony ratification (Gate C — open)

| Field | Value |
|---|---|
| Ratification decision | APPROVED / REJECTED / DEFERRED |
| Final implementation disposition | |
| Ratifier | Anthony |
| Ratification date (UTC) | |

**No blank, implied, batch-level, or inherited ratification is permitted. No frame may inherit approval from a sibling frame in the same signal family.**

---

## Frame 5 — `signal_mcv_high::inv_mcv_high_macrocytosis`

### Frame identity

| Field | Value |
|---|---|
| signal_id | `signal_mcv_high` |
| activation_key | `signal_mcv_high::inv_mcv_high_macrocytosis` |
| source_spec_id | `inv_mcv_high_macrocytosis` |
| package_id | `pkg_s24_mcv_high_macrocytosis` |
| review class | FULL_NEW_MEDICAL_REVIEW |
| current legacy / runtime WHY authority | LEGACY_ACTIVE via mcv_high_hypotheses_v1.yaml |
| proposed compiled authority | Candidate compiled artefact path: `_(none — candidate not compiled)_` — **not promoted in this pack** |
| consumer surface | Lead hint (family) |
| clinician surface | Legacy root-cause registry |

### Medical interpretation (evidence excerpt — not a GPT decision)

| Field | Evidence from repository assets |
|---|---|
| Primary marker | `mcv` — Mean Corpuscular Volume reflects red cell size. High MCV is a sensitive indicator of B12/Folate deficiency or marrow stress. |
| Trigger direction | `high` |
| Narrative interpretation (inv) | High MCV is a morphology-led investigation trigger requiring nutritional, hepatic, and alcohol-context evaluation. |
| Mechanism (inv) | MCV rises when erythrocytes are larger due to ineffective maturation or altered membrane composition. |

### Evidence summary

| Artefact | Path / status |
|---|---|
| Investigation specification | `knowledge_bus/research/investigation_specs/inv_mcv_high_macrocytosis.yaml` (or `_v1`) — AVAILABLE |
| Legacy WHY YAML | `knowledge_bus/root_cause/hypotheses/mcv_high_hypotheses_v1.yaml` — hypothesis ids: `mcv_high_anchor_pattern_v1`, `mcv_high_nutrient_association_v1`, `mcv_high_hepatic_marker_association_v1` |
| Compiled artefact | `_(none — candidate not compiled)_` |
| Package | `knowledge_bus/packages/pkg_s24_mcv_high_macrocytosis/` |

### Investigation-spec hypotheses (source research; not approved)

- _(no hypotheses block in investigation specification)_

### Causal limits / wording / modifiers / parity (for GPT completion)

| Field | Cursor assembly note | GPT completion |
|---|---|---|
| Causal limits | Derive from inv caveats / contradiction markers; do not invent | |
| Consumer wording boundary | Must remain non-diagnostic; respect lead-hint surfaces | |
| Clinician wording boundary | Root-cause compiler boundaries; no prescribing | |
| Approved hypotheses | Leave blank until GPT decides | |
| Rejected hypotheses | Leave blank until GPT decides | |
| Uncertainty | | |
| Confirmatory-test context | Inv confirmatory_tests / legacy confirmatory markers | |
| Modifier compatibility | Package gates / context requirements where present | |
| Legacy-parity assessment | Shared YAML families (hcy/mcv/tpo) require per-frame care | |

### Proposed production disposition

**PENDING_GPT_MEDICAL_REVIEW** — Cursor does **not** select among APPROVE_FOR_COMPILED_PROMOTION / APPROVE_WITH_REVISIONS / REJECT / DEFER_PENDING_RESEARCH / RETIREMENT_CONFIRMATION_ONLY.

Allowed after GPT review (exact one):

```text
APPROVE_FOR_COMPILED_PROMOTION
APPROVE_WITH_REVISIONS
REJECT
DEFER_PENDING_RESEARCH
RETIREMENT_CONFIRMATION_ONLY
```

### GPT medical-review decision (Gate C — open)

| Field | Value |
|---|---|
| GPT decision | |
| Required revisions | |
| Reviewer | GPT — HealthIQ AI Head of Medical Research |
| Review date (UTC) | |

### Anthony ratification (Gate C — open)

| Field | Value |
|---|---|
| Ratification decision | APPROVED / REJECTED / DEFERRED |
| Final implementation disposition | |
| Ratifier | Anthony |
| Ratification date (UTC) | |

**No blank, implied, batch-level, or inherited ratification is permitted. No frame may inherit approval from a sibling frame in the same signal family.**

---

## Frame 6 — `signal_mcv_high::inv_mcv_high_megaloblastic_macrocytosis`

### Frame identity

| Field | Value |
|---|---|
| signal_id | `signal_mcv_high` |
| activation_key | `signal_mcv_high::inv_mcv_high_megaloblastic_macrocytosis` |
| source_spec_id | `inv_mcv_high_megaloblastic_macrocytosis` |
| package_id | `pkg_kb52c_mcv_high_megaloblastic_macrocytosis` |
| review class | FULL_NEW_MEDICAL_REVIEW |
| current legacy / runtime WHY authority | LEGACY_ACTIVE via mcv_high_hypotheses_v1.yaml |
| proposed compiled authority | Candidate compiled artefact path: `_(none — candidate not compiled)_` — **not promoted in this pack** |
| consumer surface | Lead hint (family) |
| clinician surface | Legacy root-cause registry |

### Medical interpretation (evidence excerpt — not a GPT decision)

| Field | Evidence from repository assets |
|---|---|
| Primary marker | `mcv` — MCV reflects average erythrocyte size and high values indicate macrocytosis, not a specific diagnosis by themselves. |
| Trigger direction | `high` |
| Narrative interpretation (inv) | High MCV is clinically useful because it narrows anemia interpretation even when hemoglobin remains normal. |
| Mechanism (inv) | Macrocytosis arises from impaired DNA synthesis, altered membrane composition, reticulocytosis, or marrow dysplasia. |

### Evidence summary

| Artefact | Path / status |
|---|---|
| Investigation specification | `knowledge_bus/research/investigation_specs/inv_mcv_high_megaloblastic_macrocytosis.yaml` (or `_v1`) — AVAILABLE |
| Legacy WHY YAML | `knowledge_bus/root_cause/hypotheses/mcv_high_hypotheses_v1.yaml` — hypothesis ids: `mcv_high_anchor_pattern_v1`, `mcv_high_nutrient_association_v1`, `mcv_high_hepatic_marker_association_v1` |
| Compiled artefact | `_(none — candidate not compiled)_` |
| Package | `knowledge_bus/packages/pkg_kb52c_mcv_high_megaloblastic_macrocytosis/` |

### Investigation-spec hypotheses (source research; not approved)

- `hyp_megaloblastic_macrocytosis` — High MCV with low folate or low active B12 is consistent with megaloblastic macrocytosis from impaired DNA synthesis.
- `hyp_combined_or_b12_predominant_macrocytosis` — High MCV may also reflect a cobalamin-predominant or combined hematinic deficiency pattern rather than isolated folate deficiency alone.

### Causal limits / wording / modifiers / parity (for GPT completion)

| Field | Cursor assembly note | GPT completion |
|---|---|---|
| Causal limits | Derive from inv caveats / contradiction markers; do not invent | |
| Consumer wording boundary | Must remain non-diagnostic; respect lead-hint surfaces | |
| Clinician wording boundary | Root-cause compiler boundaries; no prescribing | |
| Approved hypotheses | Leave blank until GPT decides | |
| Rejected hypotheses | Leave blank until GPT decides | |
| Uncertainty | | |
| Confirmatory-test context | Inv confirmatory_tests / legacy confirmatory markers | |
| Modifier compatibility | Package gates / context requirements where present | |
| Legacy-parity assessment | Shared YAML families (hcy/mcv/tpo) require per-frame care | |

### Proposed production disposition

**PENDING_GPT_MEDICAL_REVIEW** — Cursor does **not** select among APPROVE_FOR_COMPILED_PROMOTION / APPROVE_WITH_REVISIONS / REJECT / DEFER_PENDING_RESEARCH / RETIREMENT_CONFIRMATION_ONLY.

Allowed after GPT review (exact one):

```text
APPROVE_FOR_COMPILED_PROMOTION
APPROVE_WITH_REVISIONS
REJECT
DEFER_PENDING_RESEARCH
RETIREMENT_CONFIRMATION_ONLY
```

### GPT medical-review decision (Gate C — open)

| Field | Value |
|---|---|
| GPT decision | |
| Required revisions | |
| Reviewer | GPT — HealthIQ AI Head of Medical Research |
| Review date (UTC) | |

### Anthony ratification (Gate C — open)

| Field | Value |
|---|---|
| Ratification decision | APPROVED / REJECTED / DEFERRED |
| Final implementation disposition | |
| Ratifier | Anthony |
| Ratification date (UTC) | |

**No blank, implied, batch-level, or inherited ratification is permitted. No frame may inherit approval from a sibling frame in the same signal family.**

---

## Frame 7 — `signal_mcv_high::inv_mcv_high_nonmegaloblastic_macrocytosis`

### Frame identity

| Field | Value |
|---|---|
| signal_id | `signal_mcv_high` |
| activation_key | `signal_mcv_high::inv_mcv_high_nonmegaloblastic_macrocytosis` |
| source_spec_id | `inv_mcv_high_nonmegaloblastic_macrocytosis` |
| package_id | `pkg_kb52c_mcv_high_nonmegaloblastic_macrocytosis` |
| review class | FULL_NEW_MEDICAL_REVIEW |
| current legacy / runtime WHY authority | LEGACY_ACTIVE via mcv_high_hypotheses_v1.yaml |
| proposed compiled authority | Candidate compiled artefact path: `_(none — candidate not compiled)_` — **not promoted in this pack** |
| consumer surface | Lead hint (family) |
| clinician surface | Legacy root-cause registry |

### Medical interpretation (evidence excerpt — not a GPT decision)

| Field | Evidence from repository assets |
|---|---|
| Primary marker | `mcv` — High MCV can occur in non-megaloblastic states and should not automatically be equated with folate or B12 deficiency. |
| Trigger direction | `high` |
| Narrative interpretation (inv) | High MCV in this pattern is a useful differential clue rather than a diagnosis on its own. |
| Mechanism (inv) | Alcohol exposure, liver disease, reticulocytosis, hypothyroidism, and marrow disorders can produce macrocytosis without classic megaloblastic change. |

### Evidence summary

| Artefact | Path / status |
|---|---|
| Investigation specification | `knowledge_bus/research/investigation_specs/inv_mcv_high_nonmegaloblastic_macrocytosis.yaml` (or `_v1`) — AVAILABLE |
| Legacy WHY YAML | `knowledge_bus/root_cause/hypotheses/mcv_high_hypotheses_v1.yaml` — hypothesis ids: `mcv_high_anchor_pattern_v1`, `mcv_high_nutrient_association_v1`, `mcv_high_hepatic_marker_association_v1` |
| Compiled artefact | `_(none — candidate not compiled)_` |
| Package | `knowledge_bus/packages/pkg_kb52c_mcv_high_nonmegaloblastic_macrocytosis/` |

### Investigation-spec hypotheses (source research; not approved)

- `hyp_alcohol_or_hepatic_macrocytosis` — High MCV with elevated GGT or liver enzymes may reflect alcohol-related or hepatic non-megaloblastic macrocytosis.
- `hyp_other_nonmegaloblastic_macrocytosis` — High MCV may also reflect other non-megaloblastic causes such as reticulocytosis, hypothyroidism, or marrow disorders when hematinic deficiency is not supported.

### Causal limits / wording / modifiers / parity (for GPT completion)

| Field | Cursor assembly note | GPT completion |
|---|---|---|
| Causal limits | Derive from inv caveats / contradiction markers; do not invent | |
| Consumer wording boundary | Must remain non-diagnostic; respect lead-hint surfaces | |
| Clinician wording boundary | Root-cause compiler boundaries; no prescribing | |
| Approved hypotheses | Leave blank until GPT decides | |
| Rejected hypotheses | Leave blank until GPT decides | |
| Uncertainty | | |
| Confirmatory-test context | Inv confirmatory_tests / legacy confirmatory markers | |
| Modifier compatibility | Package gates / context requirements where present | |
| Legacy-parity assessment | Shared YAML families (hcy/mcv/tpo) require per-frame care | |

### Proposed production disposition

**PENDING_GPT_MEDICAL_REVIEW** — Cursor does **not** select among APPROVE_FOR_COMPILED_PROMOTION / APPROVE_WITH_REVISIONS / REJECT / DEFER_PENDING_RESEARCH / RETIREMENT_CONFIRMATION_ONLY.

Allowed after GPT review (exact one):

```text
APPROVE_FOR_COMPILED_PROMOTION
APPROVE_WITH_REVISIONS
REJECT
DEFER_PENDING_RESEARCH
RETIREMENT_CONFIRMATION_ONLY
```

### GPT medical-review decision (Gate C — open)

| Field | Value |
|---|---|
| GPT decision | |
| Required revisions | |
| Reviewer | GPT — HealthIQ AI Head of Medical Research |
| Review date (UTC) | |

### Anthony ratification (Gate C — open)

| Field | Value |
|---|---|
| Ratification decision | APPROVED / REJECTED / DEFERRED |
| Final implementation disposition | |
| Ratifier | Anthony |
| Ratification date (UTC) | |

**No blank, implied, batch-level, or inherited ratification is permitted. No frame may inherit approval from a sibling frame in the same signal family.**

---

## Frame 8 — `signal_free_t3_low::inv_free_t3_low_low_t3_syndrome`

### Frame identity

| Field | Value |
|---|---|
| signal_id | `signal_free_t3_low` |
| activation_key | `signal_free_t3_low::inv_free_t3_low_low_t3_syndrome` |
| source_spec_id | `inv_free_t3_low_low_t3_syndrome` |
| package_id | `pkg_kb47_free_t3_low_low_t3_syndrome` |
| review class | FULL_NEW_MEDICAL_REVIEW |
| current legacy / runtime WHY authority | LEGACY_ACTIVE via free_t3_low_hypotheses_v1.yaml; package EXPLICIT_SPEC post-PKG2 |
| proposed compiled authority | Candidate compiled artefact path: `_(none — candidate not compiled)_` — **not promoted in this pack** |
| consumer surface | Lead hint |
| clinician surface | Legacy root-cause registry |

### Medical interpretation (evidence excerpt — not a GPT decision)

| Field | Evidence from repository assets |
|---|---|
| Primary marker | `free_t3` — Free T3 is the biologically active thyroid hormone fraction, but isolated low values commonly reflect systemic illness or altered peripheral conversion rather than primary thyroid disease. |
| Trigger direction | `low` |
| Narrative interpretation (inv) | An isolated low free T3 is more consistent with a contextual low T3 syndrome than primary thyroid failure in many clinical settings, though the broader thyroid panel is needed to confirm this interpretation. |
| Mechanism (inv) | Free T3 can fall when peripheral conversion of T4 to T3 is reduced during systemic stress, inflammation, or illness. |

### Evidence summary

| Artefact | Path / status |
|---|---|
| Investigation specification | `knowledge_bus/research/investigation_specs/inv_free_t3_low_low_t3_syndrome.yaml` (or `_v1`) — AVAILABLE |
| Legacy WHY YAML | `knowledge_bus/root_cause/hypotheses/free_t3_low_hypotheses_v1.yaml` — hypothesis ids: `ft3_low_hormone_availability_pattern_v1`, `ft3_low_with_t4_context_v1` |
| Compiled artefact | `_(none — candidate not compiled)_` |
| Package | `knowledge_bus/packages/pkg_kb47_free_t3_low_low_t3_syndrome/` |

### Investigation-spec hypotheses (source research; not approved)

- `hyp_nonthyroidal_illness_pattern` — Low free T3 may reflect a non-thyroidal illness pattern with altered peripheral thyroid hormone metabolism rather than primary thyroid gland failure.
- `hyp_reduced_t4_to_t3_conversion` — Low free T3 may reflect reduced peripheral conversion of T4 to T3 in systemic stress or catabolic states.

### Causal limits / wording / modifiers / parity (for GPT completion)

| Field | Cursor assembly note | GPT completion |
|---|---|---|
| Causal limits | Derive from inv caveats / contradiction markers; do not invent | |
| Consumer wording boundary | Must remain non-diagnostic; respect lead-hint surfaces | |
| Clinician wording boundary | Root-cause compiler boundaries; no prescribing | |
| Approved hypotheses | Leave blank until GPT decides | |
| Rejected hypotheses | Leave blank until GPT decides | |
| Uncertainty | | |
| Confirmatory-test context | Inv confirmatory_tests / legacy confirmatory markers | |
| Modifier compatibility | Package gates / context requirements where present | |
| Legacy-parity assessment | Shared YAML families (hcy/mcv/tpo) require per-frame care | |

### Proposed production disposition

**PENDING_GPT_MEDICAL_REVIEW** — Cursor does **not** select among APPROVE_FOR_COMPILED_PROMOTION / APPROVE_WITH_REVISIONS / REJECT / DEFER_PENDING_RESEARCH / RETIREMENT_CONFIRMATION_ONLY.

Allowed after GPT review (exact one):

```text
APPROVE_FOR_COMPILED_PROMOTION
APPROVE_WITH_REVISIONS
REJECT
DEFER_PENDING_RESEARCH
RETIREMENT_CONFIRMATION_ONLY
```

### GPT medical-review decision (Gate C — open)

| Field | Value |
|---|---|
| GPT decision | |
| Required revisions | |
| Reviewer | GPT — HealthIQ AI Head of Medical Research |
| Review date (UTC) | |

### Anthony ratification (Gate C — open)

| Field | Value |
|---|---|
| Ratification decision | APPROVED / REJECTED / DEFERRED |
| Final implementation disposition | |
| Ratifier | Anthony |
| Ratification date (UTC) | |

**No blank, implied, batch-level, or inherited ratification is permitted. No frame may inherit approval from a sibling frame in the same signal family.**

---

## Frame 9 — `signal_tpo_ab_high::inv_tpo_ab_high_autoimmune_hypothyroid_pattern`

### Frame identity

| Field | Value |
|---|---|
| signal_id | `signal_tpo_ab_high` |
| activation_key | `signal_tpo_ab_high::inv_tpo_ab_high_autoimmune_hypothyroid_pattern` |
| source_spec_id | `inv_tpo_ab_high_autoimmune_hypothyroid_pattern` |
| package_id | `pkg_kb59_tpo_ab_high_autoimmune_hypothyroid_pattern` |
| review class | FULL_NEW_MEDICAL_REVIEW |
| current legacy / runtime WHY authority | LEGACY_ACTIVE via tpo_ab_high_hypotheses_v1.yaml |
| proposed compiled authority | Candidate compiled artefact path: `_(none — candidate not compiled)_` — **not promoted in this pack** |
| consumer surface | Lead hint (family) |
| clinician surface | Legacy root-cause registry |

### Medical interpretation (evidence excerpt — not a GPT decision)

| Field | Evidence from repository assets |
|---|---|
| Primary marker | `tpo_ab` — TPO antibodies are a clinically established marker of thyroid autoimmunity and are most informative when interpreted with thyroid function tests. |
| Trigger direction | `high` |
| Narrative interpretation (inv) | High TPO antibodies are most clinically informative when paired with TSH elevation and reduced free T4, because that pattern supports autoimmune thyroiditis as a likely driver of primary hypothyroid physiology. |
| Mechanism (inv) | TPO antibodies reflect autoimmune targeting of thyroid peroxidase and support immune-mediated thyroid injury rather than a non-thyroidal cause of abnormal thyroid function. |

### Evidence summary

| Artefact | Path / status |
|---|---|
| Investigation specification | `knowledge_bus/research/investigation_specs/inv_tpo_ab_high_autoimmune_hypothyroid_pattern.yaml` (or `_v1`) — AVAILABLE |
| Legacy WHY YAML | `knowledge_bus/root_cause/hypotheses/tpo_ab_high_hypotheses_v1.yaml` — hypothesis ids: `tpo_high_autoimmune_thyroid_pattern_v1`, `tpo_high_tsh_axis_context_v1` |
| Compiled artefact | `_(none — candidate not compiled)_` |
| Package | `knowledge_bus/packages/pkg_kb59_tpo_ab_high_autoimmune_hypothyroid_pattern/` |

### Investigation-spec hypotheses (source research; not approved)

- `hyp_autoimmune_primary_hypothyroid_pattern` — High TPO antibodies with a primary hypothyroid biochemical pattern are consistent with autoimmune thyroiditis as a common cause of thyroid failure.
- `hyp_subclinical_autoimmune_thyroid_failure` — High TPO antibodies may identify autoimmune thyroid injury before free T4 falls, particularly when TSH is already above the reference range.

### Causal limits / wording / modifiers / parity (for GPT completion)

| Field | Cursor assembly note | GPT completion |
|---|---|---|
| Causal limits | Derive from inv caveats / contradiction markers; do not invent | |
| Consumer wording boundary | Must remain non-diagnostic; respect lead-hint surfaces | |
| Clinician wording boundary | Root-cause compiler boundaries; no prescribing | |
| Approved hypotheses | Leave blank until GPT decides | |
| Rejected hypotheses | Leave blank until GPT decides | |
| Uncertainty | | |
| Confirmatory-test context | Inv confirmatory_tests / legacy confirmatory markers | |
| Modifier compatibility | Package gates / context requirements where present | |
| Legacy-parity assessment | Shared YAML families (hcy/mcv/tpo) require per-frame care | |

### Proposed production disposition

**PENDING_GPT_MEDICAL_REVIEW** — Cursor does **not** select among APPROVE_FOR_COMPILED_PROMOTION / APPROVE_WITH_REVISIONS / REJECT / DEFER_PENDING_RESEARCH / RETIREMENT_CONFIRMATION_ONLY.

Allowed after GPT review (exact one):

```text
APPROVE_FOR_COMPILED_PROMOTION
APPROVE_WITH_REVISIONS
REJECT
DEFER_PENDING_RESEARCH
RETIREMENT_CONFIRMATION_ONLY
```

### GPT medical-review decision (Gate C — open)

| Field | Value |
|---|---|
| GPT decision | |
| Required revisions | |
| Reviewer | GPT — HealthIQ AI Head of Medical Research |
| Review date (UTC) | |

### Anthony ratification (Gate C — open)

| Field | Value |
|---|---|
| Ratification decision | APPROVED / REJECTED / DEFERRED |
| Final implementation disposition | |
| Ratifier | Anthony |
| Ratification date (UTC) | |

**No blank, implied, batch-level, or inherited ratification is permitted. No frame may inherit approval from a sibling frame in the same signal family.**

---

## Frame 10 — `signal_tpo_ab_high::inv_tpo_ab_high_euthyroid_autoimmune_risk`

### Frame identity

| Field | Value |
|---|---|
| signal_id | `signal_tpo_ab_high` |
| activation_key | `signal_tpo_ab_high::inv_tpo_ab_high_euthyroid_autoimmune_risk` |
| source_spec_id | `inv_tpo_ab_high_euthyroid_autoimmune_risk` |
| package_id | `pkg_kb59_tpo_ab_high_euthyroid_autoimmune_risk` |
| review class | FULL_NEW_MEDICAL_REVIEW |
| current legacy / runtime WHY authority | LEGACY_ACTIVE via tpo_ab_high_hypotheses_v1.yaml; identity index deferred/inactive pending review |
| proposed compiled authority | Candidate compiled artefact path: `_(none — candidate not compiled)_` — **not promoted in this pack** |
| consumer surface | Lead hint (family) |
| clinician surface | Legacy root-cause registry |

### Medical interpretation (evidence excerpt — not a GPT decision)

| Field | Evidence from repository assets |
|---|---|
| Primary marker | `tpo_ab` — TPO antibodies are a marker of thyroid autoimmunity and can identify autoimmune context even before overt thyroid dysfunction is established. |
| Trigger direction | `high` |
| Narrative interpretation (inv) | High TPO antibodies with currently preserved thyroid function are best interpreted as autoimmune thyroid context with future risk, not as proof of current overt hypothyroidism. |
| Mechanism (inv) | TPO antibody positivity indicates immune recognition of thyroid peroxidase and can precede measurable loss of thyroid hormone production. |

### Evidence summary

| Artefact | Path / status |
|---|---|
| Investigation specification | `knowledge_bus/research/investigation_specs/inv_tpo_ab_high_euthyroid_autoimmune_risk.yaml` (or `_v1`) — AVAILABLE |
| Legacy WHY YAML | `knowledge_bus/root_cause/hypotheses/tpo_ab_high_hypotheses_v1.yaml` — hypothesis ids: `tpo_high_autoimmune_thyroid_pattern_v1`, `tpo_high_tsh_axis_context_v1` |
| Compiled artefact | `_(none — candidate not compiled)_` |
| Package | `knowledge_bus/packages/pkg_kb59_tpo_ab_high_euthyroid_autoimmune_risk/` |

### Investigation-spec hypotheses (source research; not approved)

- `hyp_euthyroid_autoimmune_thyroid_risk` — High TPO antibodies with preserved thyroid hormone levels may indicate thyroid autoimmunity before overt biochemical hypothyroidism develops.
- `hyp_future_primary_hypothyroid_progression_risk` — High TPO antibodies may identify people at increased risk of progressing from euthyroid or subclinical states to overt primary hypothyroidism.

### Causal limits / wording / modifiers / parity (for GPT completion)

| Field | Cursor assembly note | GPT completion |
|---|---|---|
| Causal limits | Derive from inv caveats / contradiction markers; do not invent | |
| Consumer wording boundary | Must remain non-diagnostic; respect lead-hint surfaces | |
| Clinician wording boundary | Root-cause compiler boundaries; no prescribing | |
| Approved hypotheses | Leave blank until GPT decides | |
| Rejected hypotheses | Leave blank until GPT decides | |
| Uncertainty | | |
| Confirmatory-test context | Inv confirmatory_tests / legacy confirmatory markers | |
| Modifier compatibility | Package gates / context requirements where present | |
| Legacy-parity assessment | Shared YAML families (hcy/mcv/tpo) require per-frame care | |

### Proposed production disposition

**PENDING_GPT_MEDICAL_REVIEW** — Cursor does **not** select among APPROVE_FOR_COMPILED_PROMOTION / APPROVE_WITH_REVISIONS / REJECT / DEFER_PENDING_RESEARCH / RETIREMENT_CONFIRMATION_ONLY.

Allowed after GPT review (exact one):

```text
APPROVE_FOR_COMPILED_PROMOTION
APPROVE_WITH_REVISIONS
REJECT
DEFER_PENDING_RESEARCH
RETIREMENT_CONFIRMATION_ONLY
```

### GPT medical-review decision (Gate C — open)

| Field | Value |
|---|---|
| GPT decision | |
| Required revisions | |
| Reviewer | GPT — HealthIQ AI Head of Medical Research |
| Review date (UTC) | |

### Anthony ratification (Gate C — open)

| Field | Value |
|---|---|
| Ratification decision | APPROVED / REJECTED / DEFERRED |
| Final implementation disposition | |
| Ratifier | Anthony |
| Ratification date (UTC) | |

**No blank, implied, batch-level, or inherited ratification is permitted. No frame may inherit approval from a sibling frame in the same signal family.**

---

## Pack completion checklist

- [ ] All ten frames have GPT medical-review decisions (no blanks)
- [ ] All required revisions listed where disposition is APPROVE_WITH_REVISIONS
- [ ] All ten frames have Anthony ratification (no inherited family approvals)
- [ ] Final implementation dispositions recorded per frame
- [ ] Continuation authority issued for ARCH-CONV-PKG3 Phase 4+

**Status at assembly:** Gate C **OPEN** — Phase 4 implementation blocked.
