# ARCH-CONV-A — Bilirubin Provisional Frames Research Pack

**Work ID:** `ARCH-CONV-A`  
**Date (UTC):** 2026-07-27  
**Purpose:** Assemble canonical research evidence for three provisional `signal_hyperbilirubinemia` frames after D-3 MERGE_TO_ONE.  
**Medical approval:** **NONE** — frames remain unapproved  
**Compile / runtime WHY activation:** **FORBIDDEN** by current authority  

Survivor identity: `signal_hyperbilirubinemia`  
Retired WHY target (aliased): `signal_bilirubin_high`  
Alias register: `knowledge_bus/governance/arch_conv_a_why_identity_alias_register_v1.yaml`

---

## Provisional frames (identity index)

Source: `knowledge_bus/governance/medical_frame_identity_index_v1.yaml` (`signal_family_id: signal_hyperbilirubinemia`)

| # | medical_frame_id | frame_label | research_spec_id | activation_key | promotion_state | clinical_adjudication |
|---:|---|---|---|---|---|---|
| 1 | frame_bilirubin_pass3_gilbert_deferred | Gilbert pattern unconjugated elevation | inv_bilirubin_high_gilbert_pattern | signal_hyperbilirubinemia::inv_bilirubin_high_gilbert_pattern | deferred | required_before_activation |
| 2 | frame_bilirubin_pass3_hemolytic_deferred | Haemolytic / pre-hepatic pattern | inv_bilirubin_high_hemolytic_turnover_pattern | signal_hyperbilirubinemia::inv_bilirubin_high_hemolytic_turnover_pattern | deferred | required_before_activation |
| 3 | frame_bilirubin_pass3_hepatobiliary_deferred | Hepatobiliary / conjugated excretion impairment | inv_bilirubin_high_hepatobiliary_excretion_impairment | signal_hyperbilirubinemia::inv_bilirubin_high_hepatobiliary_excretion_impairment | deferred | required_before_activation |

---

## Canonical research locations

| research_spec_id | Primary research path | Package / notes |
|---|---|---|
| inv_bilirubin_high_gilbert_pattern | `knowledge_bus/research/investigation_specs/multi_llm_research/Batch_5_Pass_3.json` | Pass3 deferred; no dedicated `inv_*.yaml` yet |
| inv_bilirubin_high_hemolytic_turnover_pattern | same Batch_5 Pass 3 JSON | Pass3 deferred; no dedicated `inv_*.yaml` yet |
| inv_bilirubin_high_hepatobiliary_excretion_impairment | Batch_5 Pass 3 + `knowledge_bus/packages/pkg_kb52c_bilirubin_high_hepatobiliary_excretion_impairment/` | Package exists under `signal_bilirubin_high` naming; identity survivor is `signal_hyperbilirubinemia` |

**Gap:** no standalone `knowledge_bus/research/investigation_specs/inv_bilirubin_*.yaml` files. Research commissioning / Pass3→inv promotion remains a precondition before any future Wave 4 Gate 1 on these frames.

---

## Legacy WHY assets (not authority)

| Asset | primary_signal_id | hypotheses (ids) | disposition |
|---|---|---|---|
| `hyperbilirubinemia_hypotheses_v1.yaml` | signal_hyperbilirubinemia | `hbn_bilirubin_led_pattern_v1`; `hbn_alp_within_range_context_v1` | Retained; still loadable via survivor WHY registry row |
| `bilirubin_high_hypotheses_v1.yaml` | signal_bilirubin_high | `bh_hepatobiliary_excretion_pattern_v1`; `bh_mixed_hepatic_injury_context_v1` | Retained on disk; **not** in `ROOT_CAUSE_TARGET_SPECS` after D-3 |

Legacy wording must not be treated as approved medical content.

---

## What this pack is / is not

**Is:** research inventory + identity-aligned activation_key map for later Wave 4 medical review.  
**Is not:** Gate 1 completion, Gate 2 ratification, compile authority, or runtime activation.

---

## Recommended next medical-research actions (for programme owners)

1. Extract/promote three Pass3 specs into governed `inv_*.yaml` under survivor `signal_id: signal_hyperbilirubinemia`  
2. Reconcile kb52c package `signal_bilirubin_high` naming with survivor identity (non-runtime docs/package metadata — separate authorised task)  
3. Only then schedule Wave 4 STOP B medical review for the three frames  
