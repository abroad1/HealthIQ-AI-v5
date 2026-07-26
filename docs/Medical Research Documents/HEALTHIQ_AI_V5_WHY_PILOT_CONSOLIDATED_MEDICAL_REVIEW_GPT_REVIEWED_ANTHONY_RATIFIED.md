# HealthIQ AI v5 — WHY Pilot Consolidated Medical Review Pack

**Work ID:** `ARCH-CONV-PKG3`  
**Branch:** `feature/arch-conv-pkg3-why-authority-migration`  
**Artefact form:** One consolidated five-signal pack / **ten frame-level sections** (Gate 2.5 ratified)  
**Assembled by:** Cursor (evidence pack only)  
**Medical decisions:** Recorded in the Gate C annex below — GPT (Head of Medical Research) reviewed; Anthony ratified all ten frames on 2026-07-26.

## Authority banner

| Role | Named party |
|---|---|
| Structured medical review | GPT — HealthIQ AI Head of Medical Research |
| Production ratification | Anthony |
| Engineering | Implements only Anthony-ratified frame decisions |

GPT review alone is never production authorisation.

## Mandatory STOP Gate C

**Status:** `COMPLETE — GPT REVIEWED AND ANTHONY RATIFIED` (see Decision Annex and Anthony Ratification Table).  
Package 3 Phases 4–6 are **authorised** to implement only the dispositions recorded in this artefact.

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
- [x] All ten frames have Anthony ratification (no inherited family approvals)
- [x] Final implementation dispositions recorded per frame
- [x] Continuation authority issued for ARCH-CONV-PKG3 Phase 4+

**Status at assembly:** Gate C **COMPLETE** — Phase 4–6 authorised (annex + Anthony table).


---

# GPT Medical Review Decision Annex — Gate C

**Gate C status:** `COMPLETE — GPT REVIEWED AND ANTHONY RATIFIED`  
**Continuation:** `ARCH-CONV-PKG3` Phases 4–6 authorised on the existing branch and work ID.

**Reviewer:** GPT — HealthIQ AI Head of Medical Research  
**Review date (UTC):** 2026-07-26  
**Scope:** Medical coherence, safety boundaries, frame differentiation, hypothesis approval and migration disposition for the ten-frame pilot.  
**Production authority:** These are medical-review recommendations only. Anthony must ratify each frame before Phase 4 implementation.

## Executive decision table

| Frame | Activation key | GPT decision | Required engineering status pending Anthony |
|---:|---|---|---|
| 1 | `signal_vitamin_d_low::inv_vitamin_d_low_deficiency` | `RETIREMENT_CONFIRMATION_ONLY` | Keep current compiled authority; retire legacy authority only after Anthony approval and parity verification |
| 2 | `signal_homocysteine_high::inv_homocysteine_high_b_vitamin_related_methylation_impairment` | `APPROVE_WITH_REVISIONS` | Candidate only |
| 3 | `signal_homocysteine_high::inv_homocysteine_high_metabolic` | `REJECT` | Do not compile or promote |
| 4 | `signal_homocysteine_high::inv_homocysteine_high_renal_clearance_reduction` | `APPROVE_WITH_REVISIONS` | Candidate only |
| 5 | `signal_mcv_high::inv_mcv_high_macrocytosis` | `APPROVE_WITH_REVISIONS` | Candidate fallback/anchor only |
| 6 | `signal_mcv_high::inv_mcv_high_megaloblastic_macrocytosis` | `APPROVE_WITH_REVISIONS` | Candidate only |
| 7 | `signal_mcv_high::inv_mcv_high_nonmegaloblastic_macrocytosis` | `APPROVE_WITH_REVISIONS` | Candidate only |
| 8 | `signal_free_t3_low::inv_free_t3_low_low_t3_syndrome` | `APPROVE_WITH_REVISIONS` | Candidate only |
| 9 | `signal_tpo_ab_high::inv_tpo_ab_high_autoimmune_hypothyroid_pattern` | `APPROVE_WITH_REVISIONS` | Candidate only |
| 10 | `signal_tpo_ab_high::inv_tpo_ab_high_euthyroid_autoimmune_risk` | `APPROVE_WITH_REVISIONS` | Candidate only |

## Cross-frame rules

1. A raised or reduced biomarker is not, by itself, proof of the proposed cause.
2. Specific frames take precedence over broad fallback frames only when their required supporting pattern is present.
3. Contradictory markers must suppress or reduce confidence in the affected hypothesis.
4. Consumer wording must use language such as “may be consistent with”, “can be associated with” or “may warrant contextual review”; it must not diagnose or prescribe.
5. Clinician wording may be more specific but must distinguish an observed biochemical pattern from an established diagnosis.
6. No frame may recommend treatment. Follow-up testing may be described as contextual information, not as a personalised instruction.
7. Shared legacy YAML must not be promoted wholesale into several compiled frames. Only the hypotheses explicitly approved below may be assigned to the specified activation key.
8. A rejected or deferred frame must not become a runtime fallback.

---

## Frame 1 decision — Vitamin D deficiency

**Activation key:** `signal_vitamin_d_low::inv_vitamin_d_low_deficiency`  
**GPT decision:** `RETIREMENT_CONFIRMATION_ONLY`

### Medical judgement

The frame is medically coherent. Serum 25-hydroxyvitamin D is the accepted measure of vitamin D status, and low values can indicate insufficiency or deficiency in the appropriate laboratory context. The existing compiled authority may remain the canonical pilot implementation.

### Approved content boundaries

- May describe low 25-hydroxyvitamin D as reduced vitamin D status.
- May state that vitamin D contributes to calcium/phosphate homeostasis and bone health.
- May note that low levels are more common with limited sunlight exposure, higher latitude, darker skin, dietary limitation, malabsorption or other recognised risk contexts when those contexts are actually available.
- Severe deficiency may be associated with osteomalacia in adults and rickets in children, but those conditions must not be inferred from a low result alone.

### Required revisions / safeguards

- Do not equate every below-range result with “severe deficiency”.
- Do not infer a specific cause from the vitamin D result alone.
- Do not make treatment-dose or prescribing recommendations.
- Preserve laboratory-unit and threshold provenance; do not hard-code a universal threshold where the governed specification already supplies one.
- Legacy retirement requires output-parity confirmation and proof that no fallback can reactivate the retired YAML.

### Legacy-parity judgement

`COMPILED_ASSET_IMPROVES_LEGACY`, provided the compiled version preserves cautious wording and the legacy YAML is made non-runtime-reachable.

---

## Frame 2 decision — Homocysteine, B-vitamin-related methylation impairment

**Activation key:** `signal_homocysteine_high::inv_homocysteine_high_b_vitamin_related_methylation_impairment`  
**GPT decision:** `APPROVE_WITH_REVISIONS`

### Approved hypotheses

- `hyp_folate_related_hyperhomocysteinemia`
- `hyp_b12_related_or_combined_methylation_impairment`

### Required supporting pattern

At least one relevant B-vitamin marker must support the frame, such as low folate, low/indeterminate B12 or active B12, or another governed marker of impaired B12 status. Macrocytosis may add support but is neither required nor specific.

### Causal limits

- Raised homocysteine is non-specific.
- It must not be presented as proof of folate, B12 or B6 deficiency.
- Renal impairment, medicines, hypothyroid physiology, smoking, age and genetic variation may also contribute.
- Homocysteine must not be described as a validated stand-alone measure of “methylation capacity”.

### Consumer boundary

“Your raised homocysteine may be associated with reduced availability of folate or vitamin B12, particularly if those markers are also low or borderline. Other factors can also raise homocysteine.”

### Clinician boundary

May describe a B-vitamin-associated hyperhomocysteinaemia pattern when corroborating markers are present. Must state that the pattern is not a diagnosis and should be interpreted alongside renal function, thyroid status, medicines and clinical context.

### Confirmatory context

May mention review of folate, B12/active B12 and, where clinically appropriate, methylmalonic acid or other established B12-assessment pathways. Must not recommend supplementation directly.

### Legacy-parity judgement

The legacy inflammation and renal hypotheses must not be copied into this frame. Renal causation belongs to Frame 4; non-specific inflammation alone is insufficient for this frame.

---

## Frame 3 decision — Homocysteine “metabolic” frame

**Activation key:** `signal_homocysteine_high::inv_homocysteine_high_metabolic`  
**GPT decision:** `REJECT`

### Reason

The proposed frame is too broad and insufficiently differentiated from Frames 2 and 4. Its current language risks presenting homocysteine as a general measure of “methylation capacity” and as an independent vascular or cognitive risk finding without adequate contextual qualification. It contains no frame-specific hypothesis block and would function as an ungoverned catch-all.

### Production rule

- Do not compile or promote this frame.
- Do not use it as a fallback when Frames 2 or 4 are unsupported.
- The general educational description of homocysteine may be retained outside causal WHY authority if separately governed.
- Any future replacement must define a distinct, evidence-based activation pattern and pass a new medical review.

### Legacy-parity judgement

`NO_SAFE_PARITY`. The shared legacy YAML cannot be safely mapped to this broad frame.

---

## Frame 4 decision — Homocysteine, renal clearance reduction

**Activation key:** `signal_homocysteine_high::inv_homocysteine_high_renal_clearance_reduction`  
**GPT decision:** `APPROVE_WITH_REVISIONS`

### Approved hypotheses

- `hyp_renal_hyperhomocysteinemia`
- `hyp_combined_renal_and_hematinic_context`

### Required supporting pattern

The renal hypothesis requires governed evidence of reduced kidney function, such as reduced eGFR and/or raised creatinine interpreted in context. A single transient result must not be labelled chronic kidney disease.

The combined hypothesis additionally requires supporting evidence of B-vitamin insufficiency.

### Causal limits

- Reduced renal function can contribute to elevated homocysteine, but homocysteine is not a diagnostic or staging marker for kidney disease.
- Do not imply that lowering homocysteine improves cardiovascular or renal outcomes.
- Do not label reduced eGFR as chronic unless persistence criteria are available.

### Consumer boundary

“Reduced kidney filtration can contribute to a raised homocysteine result. This does not show the cause on its own and should be considered alongside kidney and vitamin markers.”

### Clinician boundary

May describe renal-associated hyperhomocysteinaemia when renal impairment is concurrently supported. Must separate renal contribution from isolated vitamin deficiency and from established CKD diagnosis.

### Legacy-parity judgement

The renal legacy hypothesis may migrate to this frame; B12 and folate hypotheses must remain assigned to Frame 2 unless the combined pattern is explicitly satisfied.

---

## Frame 5 decision — General macrocytosis anchor

**Activation key:** `signal_mcv_high::inv_mcv_high_macrocytosis`  
**GPT decision:** `APPROVE_WITH_REVISIONS`

### Medical judgement

Raised MCV is a valid morphology-led finding but is not a causal diagnosis. This frame may exist only as a non-specific anchor or fallback when the evidence does not support the more specific megaloblastic or non-megaloblastic frames.

### Approved content

- High MCV indicates macrocytosis.
- Common contexts include B12/folate deficiency, alcohol exposure, liver disease, hypothyroid physiology, reticulocytosis, medicines and marrow disorders.
- The result can occur with or without anaemia.

### Required safeguards

- No cause may be ranked from MCV alone.
- The frame must not co-serve with Frame 6 or Frame 7 as a second causal explanation.
- If a specific frame is supported, this anchor may provide morphology context but must not generate duplicate WHY hypotheses.
- Avoid “marrow stress” as a general explanation unless supported by specific markers.

### Confirmatory context

May mention contextual review of haemoglobin, blood film, reticulocytes, B12, folate, liver markers and TSH. It must not recommend invasive investigation.

### Legacy-parity judgement

Only `mcv_high_anchor_pattern_v1` belongs here. Nutrient and hepatic associations must migrate to Frames 6 and 7 respectively.

---

## Frame 6 decision — Megaloblastic macrocytosis

**Activation key:** `signal_mcv_high::inv_mcv_high_megaloblastic_macrocytosis`  
**GPT decision:** `APPROVE_WITH_REVISIONS`

### Approved hypotheses

- `hyp_megaloblastic_macrocytosis`
- `hyp_combined_or_b12_predominant_macrocytosis`

### Required supporting pattern

Raised MCV plus corroborating evidence of folate or B12 deficiency/insufficiency. Blood-film features may strengthen the frame when available. MCV alone is insufficient, and absence of macrocytosis does not exclude B12 deficiency.

### Causal limits

- Do not diagnose megaloblastic anaemia without appropriate haematological evidence.
- Do not assume isolated folate deficiency when B12 status is unknown or equivocal.
- Do not infer the underlying cause of B12 or folate deficiency from this frame.

### Consumer boundary

“The combination of larger red cells and low or borderline folate/B12 markers may fit a vitamin-related macrocytosis pattern. Other causes remain possible.”

### Clinician boundary

May describe a megaloblastic-pattern differential when biochemical and morphology evidence align. Must retain uncertainty where blood film or definitive vitamin assessment is unavailable.

### Legacy-parity judgement

`mcv_high_nutrient_association_v1` may migrate here after narrowing to evidence-supported B12/folate patterns.

---

## Frame 7 decision — Non-megaloblastic macrocytosis

**Activation key:** `signal_mcv_high::inv_mcv_high_nonmegaloblastic_macrocytosis`  
**GPT decision:** `APPROVE_WITH_REVISIONS`

### Approved hypotheses

- `hyp_alcohol_or_hepatic_macrocytosis`
- `hyp_other_nonmegaloblastic_macrocytosis`, but only as a constrained differential context rather than one combined causal assertion.

### Required supporting pattern

- Alcohol/hepatic hypothesis: raised MCV plus relevant alcohol context and/or supportive liver markers.
- Reticulocytosis hypothesis: raised reticulocyte evidence.
- Hypothyroid context: compatible TSH/FT4 pattern.
- Marrow-disorder language: clinician-only differential, never a consumer-facing inferred cause, and only when persistent unexplained macrocytosis or other cytopenias are present.

### Causal limits

- Do not infer alcohol exposure from MCV or GGT alone.
- Do not diagnose liver disease, hypothyroidism, haemolysis or marrow disease.
- “Other non-megaloblastic causes” must not become an unrestricted catch-all.

### Consumer boundary

“Larger red cells can also occur in non-vitamin contexts, including liver, thyroid, alcohol or increased red-cell turnover patterns. The cause cannot be determined from MCV alone.”

### Clinician boundary

May present a ranked differential only when each candidate has its own supporting evidence. Marrow-dysplasia wording must remain cautious and clinician-facing.

### Legacy-parity judgement

`mcv_high_hepatic_marker_association_v1` may migrate here with explicit evidence gates. The generic anchor remains in Frame 5.

---

## Frame 8 decision — Low free T3 / non-thyroidal illness context

**Activation key:** `signal_free_t3_low::inv_free_t3_low_low_t3_syndrome`  
**GPT decision:** `APPROVE_WITH_REVISIONS`

### Approved hypotheses

- `hyp_nonthyroidal_illness_pattern`
- `hyp_reduced_t4_to_t3_conversion`

### Required supporting pattern

The frame requires a compatible broader thyroid pattern and contextual evidence of acute or chronic systemic illness, inflammation, physiological stress, undernutrition or catabolic state. An isolated outpatient low FT3 without context is insufficient.

### Causal limits

- Low FT3 does not diagnose non-thyroidal illness syndrome.
- It must not be used to exclude primary or central thyroid disease.
- The phrase “reduced conversion” is a plausible mechanism, not a directly measured process.
- Interpretation must consider TSH and FT4; assay and medicine effects may also matter.
- Do not recommend thyroid hormone treatment.

### Consumer boundary

“A low free T3 result can occur during illness or physiological stress and does not necessarily mean that the thyroid gland itself is underactive. The rest of the thyroid panel and clinical context are important.”

### Clinician boundary

May describe a pattern compatible with non-thyroidal illness when TSH/FT4 and illness context support it. Must identify discordant patterns requiring alternative interpretation.

### Legacy-parity judgement

The generic `ft3_low_hormone_availability_pattern_v1` must be narrowed. `ft3_low_with_t4_context_v1` may migrate only with explicit TSH/FT4 gating.

---

## Frame 9 decision — TPO antibody positive with hypothyroid physiology

**Activation key:** `signal_tpo_ab_high::inv_tpo_ab_high_autoimmune_hypothyroid_pattern`  
**GPT decision:** `APPROVE_WITH_REVISIONS`

### Approved hypotheses

- `hyp_autoimmune_primary_hypothyroid_pattern`
- `hyp_subclinical_autoimmune_thyroid_failure`

### Required supporting pattern

- Overt-pattern hypothesis: elevated TSH with reduced FT4 plus raised TPO antibodies.
- Subclinical-pattern hypothesis: elevated TSH with FT4 within range plus raised TPO antibodies.

The exact interpretation must follow the governed thyroid frame and must not be inferred from TPO antibodies alone.

### Causal limits

- Positive TPO antibodies support autoimmune thyroid disease but are not, alone, proof of current hypothyroidism.
- Do not diagnose Hashimoto thyroiditis solely from the blood pattern.
- Do not imply that antibody titre measures disease severity.
- Do not recommend repeating TPO antibodies routinely or prescribe treatment.

### Consumer boundary

“Raised thyroid peroxidase antibodies, together with this thyroid-function pattern, may support an autoimmune contribution. The antibodies alone do not show how well the thyroid is currently functioning.”

### Clinician boundary

May describe biochemical primary hypothyroid or subclinical hypothyroid physiology with positive TPO antibodies as supportive of autoimmune thyroiditis. Must preserve the distinction between overt and subclinical patterns.

### Legacy-parity judgement

Both legacy hypotheses may migrate only after being split and gated to the appropriate TSH/FT4 pattern.

---

## Frame 10 decision — TPO antibody positive with preserved thyroid function

**Activation key:** `signal_tpo_ab_high::inv_tpo_ab_high_euthyroid_autoimmune_risk`  
**GPT decision:** `APPROVE_WITH_REVISIONS`

### Approved hypotheses

- `hyp_euthyroid_autoimmune_thyroid_risk`
- `hyp_future_primary_hypothyroid_progression_risk`

### Required supporting pattern

Raised TPO antibodies with TSH and FT4 currently within their governed reference ranges. A subclinical or overt hypothyroid pattern belongs in Frame 9, not this frame.

### Causal limits

- This is an autoimmune-risk context, not a diagnosis of current hypothyroidism.
- Progression is possible but not inevitable.
- Do not provide a personalised probability unless a validated, population-appropriate model and required variables are available.
- Do not imply that antibody titre alone predicts the timing of progression.
- Do not recommend repeated antibody measurement; future thyroid-function review may be described only in cautious contextual terms.

### Consumer boundary

“Raised TPO antibodies can indicate an autoimmune thyroid context even when thyroid hormone levels are currently preserved. This can be associated with a higher future risk of thyroid underactivity, but progression is not certain.”

### Clinician boundary

May record euthyroid TPO-antibody positivity as a risk marker for future thyroid dysfunction. Must distinguish current euthyroidism from subclinical or overt hypothyroidism and consider pregnancy-specific pathways separately.

### Legacy-parity judgement

The legacy autoimmune pattern may migrate after removing any implication of current hypothyroidism. The TSH-axis hypothesis belongs in Frame 9 when TSH is elevated.

---

# Anthony Ratification Table — Completed

Anthony explicitly ratifies the GPT medical-review decision and required revisions for every frame below. Approval of a `REJECT` decision means the frame must remain inactive and must not be compiled or promoted.

| Frame | GPT decision | Anthony decision | Final implementation disposition | Anthony notes |
|---:|---|---|---|---|
| 1 | `RETIREMENT_CONFIRMATION_ONLY` | `APPROVED` | `RETIREMENT_CONFIRMATION_ONLY` | Retain the current compiled vitamin D authority; retire legacy authority only after parity and fallback checks pass. |
| 2 | `APPROVE_WITH_REVISIONS` | `APPROVED` | `APPROVE_WITH_REVISIONS` | Implement only with the stated B-vitamin evidence gates and causal limits. |
| 3 | `REJECT` | `APPROVED` | `REJECT` | Do not compile, promote or use as a fallback. |
| 4 | `APPROVE_WITH_REVISIONS` | `APPROVED` | `APPROVE_WITH_REVISIONS` | Implement only with explicit renal-function support and no CKD inference from a single result. |
| 5 | `APPROVE_WITH_REVISIONS` | `APPROVED` | `APPROVE_WITH_REVISIONS` | Use only as a non-specific morphology anchor; prevent duplicate causal WHY output. |
| 6 | `APPROVE_WITH_REVISIONS` | `APPROVED` | `APPROVE_WITH_REVISIONS` | Require corroborating B12/folate evidence. |
| 7 | `APPROVE_WITH_REVISIONS` | `APPROVED` | `APPROVE_WITH_REVISIONS` | Require cause-specific evidence gates; no inferred alcohol or marrow diagnosis. |
| 8 | `APPROVE_WITH_REVISIONS` | `APPROVED` | `APPROVE_WITH_REVISIONS` | Require compatible illness and thyroid-panel context; no treatment recommendation. |
| 9 | `APPROVE_WITH_REVISIONS` | `APPROVED` | `APPROVE_WITH_REVISIONS` | Preserve overt versus subclinical hypothyroid distinctions. |
| 10 | `APPROVE_WITH_REVISIONS` | `APPROVED` | `APPROVE_WITH_REVISIONS` | Preserve current euthyroid status and cautious future-risk wording. |

**Ratifier:** Anthony — HealthIQ AI human project authority and production ratifier  
**Anthony ratification date (UTC):** 2026-07-26  
**Continuation authority for Package 3 Phase 4–6:** `AUTHORISED`

## Ratification declaration

Anthony approves the GPT medical-review findings, required revisions and final implementation dispositions recorded in this pack. Engineering is authorised to resume `ARCH-CONV-PKG3` on the existing branch and work ID, implementing only the decisions recorded here. Any material departure from these decisions, addition of a frame, or weakening of the specified safety boundaries requires a new STOP and explicit reauthorisation.

# Medical evidence basis used for this review

- NICE NG145, *Thyroid disease: assessment and management*.
- NICE CKS, *Hypothyroidism* and thyroid-antibody assessment guidance.
- NICE NG239, *Vitamin B12 deficiency in over 16s: diagnosis and management*.
- NICE CKS, *Vitamin D deficiency in adults*.
- British Society for Haematology, *The Full Blood Count* educational guideline.
- KDIGO 2024 Clinical Practice Guideline for the Evaluation and Management of Chronic Kidney Disease.
- Van den Berghe G. Non-thyroidal illness in critical illness, 2014.
- Effraimidis G et al. Natural history of transition from euthyroidism to overt autoimmune thyroid disease, 2011.
- Amouzegar A et al. Natural course of euthyroidism and predictors of thyroid dysfunction, 2017.

# Gate C status after GPT review

- [x] All ten frames have explicit GPT medical-review decisions.
- [x] Required revisions are recorded.
- [x] Anthony has ratified every frame.
- [x] Final implementation dispositions are recorded.
- [x] Continuation authority has been issued.

**Current status:** Gate C complete. Package 3 Phase 4–6 is authorised to resume on the existing work ID and branch.
