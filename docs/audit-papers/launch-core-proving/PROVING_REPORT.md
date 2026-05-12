# Launch-core proving harness — comparison report

- **Stamp:** `20260512T204032Z`
- **Git (short):** `4edb9e0`
- **Matrix:** `backend\tests\fixtures\proving\launch_core_matrix.json`

## Scenario matrix (panels × scenarios)

| Panel | Scenario | Description |
|-------|----------|-------------|
| AB | `baseline` | No lifestyle fixture; questionnaire_data omitted (minimal intake). |
| AB | `lifestyle_context` | Existing SSOT lifestyle fixture; no questionnaire_data. |
| AB | `statin_off` | Explicit statin-off questionnaire answer; no lifestyle fixture. |
| AB | `statin_on` | Statin-on — must use exact SSOT option label. |
| VR | `baseline` | No lifestyle fixture; questionnaire_data omitted (minimal intake). |
| VR | `lifestyle_context` | Existing SSOT lifestyle fixture; no questionnaire_data. |
| VR | `statin_off` | Explicit statin-off questionnaire answer; no lifestyle fixture. |
| VR | `statin_on` | Statin-on — must use exact SSOT option label. |

## Per-run fingerprints (compact)

### `AB__baseline`

- **status:** completed
- **top findings (order):** `signal_homocysteine_elevation_context, signal_homocysteine_high, signal_mcv_high, signal_total_cholesterol_high, signal_apoa1_cardio_risk, signal_ldl_cholesterol_high, signal_ldl_high, signal_transferrin_low, signal_systemic_inflammation, signal_oxygen_transport_capacity, signal_lipid_transport_dysfunction, signal_vascular_inflammatory_stress, signal_renal_metabolic_stress`
- **consumer band labels:** `['strong', 'stable', 'review']`
- **intervention present:** False classes=[]
- **retail summary (head):** The ranked lead pattern is **Homocysteine Elevation Context** (at_risk), centred on **Homocysteine**. Layer B frames this as the priority focus for interpretati...
- **body overview (head):** Lead ranked finding **Homocysteine Elevation Context** (at_risk) is interpreted alongside the wider deterministic system snapshot below.

Primary driver system ...
- **clinician primary_concern (head):** Homocysteine Elevation Context: warrants attention on this panel...
- **IDL enabled patterns:** 4 titles=['', '', '', '']

### `AB__lifestyle_context`

- **status:** completed
- **top findings (order):** `signal_homocysteine_elevation_context, signal_homocysteine_high, signal_mcv_high, signal_total_cholesterol_high, signal_apoa1_cardio_risk, signal_ldl_cholesterol_high, signal_ldl_high, signal_transferrin_low, signal_systemic_inflammation, signal_oxygen_transport_capacity, signal_lipid_transport_dysfunction, signal_vascular_inflammatory_stress, signal_renal_metabolic_stress`
- **consumer band labels:** `['strong', 'stable', 'review']`
- **intervention present:** False classes=[]
- **retail summary (head):** The ranked lead pattern is **Homocysteine Elevation Context** (at_risk), centred on **Homocysteine**. Layer B frames this as the priority focus for interpretati...
- **body overview (head):** Lead ranked finding **Homocysteine Elevation Context** (at_risk) is interpreted alongside the wider deterministic system snapshot below.

Primary driver system ...
- **clinician primary_concern (head):** Homocysteine Elevation Context: warrants attention on this panel...
- **IDL enabled patterns:** 4 titles=['', '', '', '']

### `AB__statin_off`

- **status:** completed
- **top findings (order):** `signal_homocysteine_elevation_context, signal_homocysteine_high, signal_mcv_high, signal_total_cholesterol_high, signal_apoa1_cardio_risk, signal_ldl_cholesterol_high, signal_ldl_high, signal_transferrin_low, signal_systemic_inflammation, signal_oxygen_transport_capacity, signal_lipid_transport_dysfunction, signal_vascular_inflammatory_stress, signal_renal_metabolic_stress`
- **consumer band labels:** `['strong', 'stable', 'review']`
- **intervention present:** False classes=[]
- **retail summary (head):** The ranked lead pattern is **Homocysteine Elevation Context** (at_risk), centred on **Homocysteine**. Layer B frames this as the priority focus for interpretati...
- **body overview (head):** Lead ranked finding **Homocysteine Elevation Context** (at_risk) is interpreted alongside the wider deterministic system snapshot below.

Primary driver system ...
- **clinician primary_concern (head):** Homocysteine Elevation Context: warrants attention on this panel...
- **IDL enabled patterns:** 4 titles=['', '', '', '']

### `AB__statin_on`

- **status:** completed
- **top findings (order):** `signal_homocysteine_elevation_context, signal_homocysteine_high, signal_mcv_high, signal_total_cholesterol_high, signal_apoa1_cardio_risk, signal_ldl_cholesterol_high, signal_ldl_high, signal_transferrin_low, signal_systemic_inflammation, signal_oxygen_transport_capacity, signal_lipid_transport_dysfunction, signal_vascular_inflammatory_stress, signal_renal_metabolic_stress`
- **consumer band labels:** `['strong', 'stable', 'review']`
- **intervention present:** True classes=['lipid_lowering_statin']
- **retail summary (head):** The ranked lead pattern is **Homocysteine Elevation Context** (at_risk), centred on **Homocysteine**. Layer B frames this as the priority focus for interpretati...
- **body overview (head):** Lead ranked finding **Homocysteine Elevation Context** (at_risk) is interpreted alongside the wider deterministic system snapshot below.

Primary driver system ...
- **clinician primary_concern (head):** Homocysteine Elevation Context: warrants attention on this panel...
- **IDL enabled patterns:** 4 titles=['', '', '', '']

### `VR__baseline`

- **status:** completed
- **top findings (order):** `signal_homocysteine_elevation_context, signal_homocysteine_high, signal_alp_low, signal_hypercortisolism, signal_vitamin_d_low, signal_cortisol_high, signal_creatine_kinase_high, signal_systemic_inflammation, signal_oxygen_transport_capacity, signal_lipid_transport_dysfunction, signal_vascular_inflammatory_stress, signal_renal_metabolic_stress`
- **consumer band labels:** `['strong', 'strong', 'strong']`
- **intervention present:** False classes=[]
- **retail summary (head):** The ranked lead pattern is **Homocysteine Elevation Context** (suboptimal), centred on **Homocysteine**. Layer B frames this as the priority focus for interpret...
- **body overview (head):** Lead ranked finding **Homocysteine Elevation Context** (suboptimal) is interpreted alongside the wider deterministic system snapshot below.

Primary driver syst...
- **clinician primary_concern (head):** Homocysteine Elevation Context: is outside the optimal range on this panel...
- **IDL enabled patterns:** 2 titles=['', '']

### `VR__lifestyle_context`

- **status:** completed
- **top findings (order):** `signal_homocysteine_elevation_context, signal_homocysteine_high, signal_alp_low, signal_hypercortisolism, signal_vitamin_d_low, signal_cortisol_high, signal_creatine_kinase_high, signal_systemic_inflammation, signal_oxygen_transport_capacity, signal_lipid_transport_dysfunction, signal_vascular_inflammatory_stress, signal_renal_metabolic_stress`
- **consumer band labels:** `['strong', 'strong', 'strong']`
- **intervention present:** False classes=[]
- **retail summary (head):** The ranked lead pattern is **Homocysteine Elevation Context** (suboptimal), centred on **Homocysteine**. Layer B frames this as the priority focus for interpret...
- **body overview (head):** Lead ranked finding **Homocysteine Elevation Context** (suboptimal) is interpreted alongside the wider deterministic system snapshot below.

Primary driver syst...
- **clinician primary_concern (head):** Homocysteine Elevation Context: is outside the optimal range on this panel...
- **IDL enabled patterns:** 2 titles=['', '']

### `VR__statin_off`

- **status:** completed
- **top findings (order):** `signal_homocysteine_elevation_context, signal_homocysteine_high, signal_alp_low, signal_hypercortisolism, signal_vitamin_d_low, signal_cortisol_high, signal_creatine_kinase_high, signal_systemic_inflammation, signal_oxygen_transport_capacity, signal_lipid_transport_dysfunction, signal_vascular_inflammatory_stress, signal_renal_metabolic_stress`
- **consumer band labels:** `['strong', 'strong', 'strong']`
- **intervention present:** False classes=[]
- **retail summary (head):** The ranked lead pattern is **Homocysteine Elevation Context** (suboptimal), centred on **Homocysteine**. Layer B frames this as the priority focus for interpret...
- **body overview (head):** Lead ranked finding **Homocysteine Elevation Context** (suboptimal) is interpreted alongside the wider deterministic system snapshot below.

Primary driver syst...
- **clinician primary_concern (head):** Homocysteine Elevation Context: is outside the optimal range on this panel...
- **IDL enabled patterns:** 2 titles=['', '']

### `VR__statin_on`

- **status:** completed
- **top findings (order):** `signal_homocysteine_elevation_context, signal_homocysteine_high, signal_alp_low, signal_hypercortisolism, signal_vitamin_d_low, signal_cortisol_high, signal_creatine_kinase_high, signal_systemic_inflammation, signal_oxygen_transport_capacity, signal_lipid_transport_dysfunction, signal_vascular_inflammatory_stress, signal_renal_metabolic_stress`
- **consumer band labels:** `['strong', 'strong', 'strong']`
- **intervention present:** True classes=['lipid_lowering_statin']
- **retail summary (head):** The ranked lead pattern is **Homocysteine Elevation Context** (suboptimal), centred on **Homocysteine**. Layer B frames this as the priority focus for interpret...
- **body overview (head):** Lead ranked finding **Homocysteine Elevation Context** (suboptimal) is interpreted alongside the wider deterministic system snapshot below.

Primary driver syst...
- **clinician primary_concern (head):** Homocysteine Elevation Context: is outside the optimal range on this panel...
- **IDL enabled patterns:** 2 titles=['', '']

## Analytical invariants — statin-off vs statin-on (same panel, no lifestyle)

Expect: identical **top-finding order**, **signal_state** map, and **consumer band labels**; intervention/statin wording differs only on statin-on.

- **AB:** invariants match — **PASS**
  - statin intervention absent→present: **PASS** (absent_when_off=True, present_when_on=True)
  - narrative body differs (expected): **False**
  - CV consequence_sentence head differs (expected on statin-on): **True**

- **VR:** invariants match — **PASS**
  - statin intervention absent→present: **PASS** (absent_when_off=True, present_when_on=True)
  - narrative body differs (expected): **False**
  - CV consequence_sentence head differs (expected on statin-on): **True**

## Lifestyle/context payoff — baseline vs lifestyle_context

Expect: lifestyle-derived fields present under lifestyle_context; narrative heads may diverge.

- **AB:** top_findings unchanged=True; bands unchanged=True; narrative block differs=True

- **VR:** top_findings unchanged=True; bands unchanged=True; narrative block differs=True

## Artifact paths

- Golden outputs (per run): `docs/audit-papers/launch-core-proving/artifacts/20260512T204032Z/` — written by `run_golden_panel`; omit bulk artefacts from git if desired.
- Latest fingerprints JSON: `docs/audit-papers/launch-core-proving/latest_fingerprints.json`
