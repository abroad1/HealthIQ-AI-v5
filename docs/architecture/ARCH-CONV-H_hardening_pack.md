# ARCH-CONV-H — Phase 0 Hardening Pack (Gate 1 / Gate 2 STOP)

**Work ID:** `ARCH-CONV-H`  
**Branch:** `feature/arch-conv-h-hba1c-compiled-why-authority`  
**Risk:** HIGH  
**Change type:** MIXED  
**Execution model:** TWO_PHASE_START_FINISH  
**Implementation owner:** Core Engine agent  
**Status:** Gate 1 `APPROVED_WITH_NARROWING` (`ARCH-CONV-H-GATE1-HMR-2026-08-01`). Gate 2 `APPROVED` (`ARCH-CONV-H-GATE2-ANTHONY-2026-08-01`). **Runtime implementation authorised.**

**Hardening clearance:** `automation_bus/latest_prompt_hardening.json` — `ARCH-CONV-H` / `HARDENED`.

---

## 0. Baseline (repository-grounded)

| Check | Result |
|---|---|
| Local `main` / `origin/main` at start | Equal (`8f8c840`) |
| Stash | Empty |
| Active WP before start | None |
| `compiled_why_authority_register_v1.yaml` HbA1c rows | **Zero** |
| Baseline counts | `COMPILED_ACTIVE=24`, `LEGACY_RETIRED=19`, `REJECTED=1`, frames=44 |
| Compiled HbA1c artefact | **Absent** |
| `signal_hba1c_high` in `_PILOT_SIGNAL_IDS` | **Absent** |
| Legacy WHY path | `root_cause_registry_v1.py` → `hba1c_hypotheses_v1.yaml` (**present / eligible**) |
| Stage 1B reality check | **YES** — proceed (gap remains; not a no-op) |
| Canonical package validation | `pkg_s24_hba1c_high_glycaemia` → **PASS** |
| Competing package validation | `pkg_kb52c_hba1c_high_diabetes_range_hyperglycemia` → **PASS** |
| Collision class | `signal_hba1c_high` — **2 packages, Governed arbitration** |

Canonical investigation-spec SHA-256:

`2CFA335DEBBA2F430C12E2F0605823B9752A3AD78389F32A7D978B8286501247`

Source path: `knowledge_bus/research/investigation_specs/inv_hba1c_high_glycaemia_v1.yaml`

---

## 1. Canonical source mapping

| Element | Repository content |
|---|---|
| `spec_id` | `inv_hba1c_high_glycaemia` |
| `signal_id` | `signal_hba1c_high` |
| Primary marker | `hba1c` — average plasma glucose over prior ~8–12 weeks |
| Activation | `lab_range_exceeded`, upper-bound only → baseline `suboptimal` |
| Supporting — glucose | `corroborator` — point-in-time confirmation |
| Supporting — triglycerides | `mechanism_marker` — insulin-resistance / metabolic association |
| Supporting — hdl_cholesterol | `mechanism_marker` — metabolic triad component |
| Supporting — alt | `mechanism_marker` — NAFLD / insulin-resistance association |
| Override `or_hba1c_diagnostic_diabetes` | `hba1c >= 48` mmol/mol → `at_risk` (WHO 2011 / NICE NG28) |
| Override `or_hba1c_metabolic_syndrome` | TG above lab max **AND** HDL below lab min → `at_risk` (IDF 2006) |
| Evidence strength | strong |
| Physiological claim | Non-enzymatic glycation of HbA N-terminal valine |
| Narrative implications (raw) | Retinopathy/neuropathy/CVD risk; **directive** “Requires lifestyle intervention or pharmacological management” — **must not compile verbatim** |

### Approved compiled-WHY content boundary (Gate 1)

- Identify a **persistent hyperglycaemia / sustained glycaemic-exposure pattern** supported by the canonical source.
- HbA1c is **not** an independently proven cause of diabetes-related pathology.
- HbA1c `>= 48 mmol/mol`: **diabetes-range concern requiring clinical confirmation only**.
- One HbA1c result must not be an unqualified diabetes diagnosis.
- TG/HDL: **subordinate metabolic-pattern context only**; **no metabolic-syndrome diagnosis**.
- Prohibited: treatment directives, chronicity inference, diabetes subtype, complications, causal attribution, or diagnosis from HbA1c alone.

### 2.1 Approved WHY role (Gate 1 ratified)

**Approved:** `why_role: morphology_context` (flat, no `conditional_why_role`).

Gate reference: `ARCH-CONV-H-GATE1-HMR-2026-08-01` (`APPROVED_WITH_NARROWING`).

The alternative narrowed-causal option from Phase 0 is **withdrawn** — not selected.

---

## 2. Package collision and ownership table

| Package | Activation key | Source / provenance | WHY ownership (current) | Package / PSI | Proposed disposition |
|---|---|---|---|---|---|
| `pkg_s24_hba1c_high_glycaemia` | `signal_hba1c_high::inv_hba1c_high_glycaemia` | `inv_hba1c_high_glycaemia_v1.yaml` | Legacy WHY via registry (no compiled row) | Active package; **no PSI file** | **RETAIN / COMPILE** as canonical (Gate 1) |
| `pkg_kb52c_hba1c_high_diabetes_range_hyperglycemia` | `signal_hba1c_high::inv_hba1c_high_diabetes_range_hyperglycemia` | `Batch_6_Pass_3.json` | Competing same-`signal_id` frame | Active package; `behavioural_impact: NONE`; **no PSI file** | **LEGACY_RETIRED_FOR_WHY_ONLY** (Gate 1) |

Collision inventory confirms governed arbitration (2 packages). Hardening notes SignalRegistry lexicographic overwrite currently prefers S24 live winner — WHY retirement still required so the competitor cannot dual-serve as compiled/legacy WHY owner after pilot inclusion.

**Expected post-Gate-2 register delta:** `+1 COMPILED_ACTIVE` / `+1 LEGACY_RETIRED`.

---

## 3. Adjacent identity exclusion table

| Identity | Activation key(s) | Relation to `signal_hba1c_high` WHY | ARCH-CONV-H action |
|---|---|---|---|
| `signal_hba1c_pct_high` | `…::inv_hba1c_pct_high_chronic_hyperglycemia_diabetes`; `…::inv_hba1c_pct_high_red_cell_turnover_bias_or_iron_deficiency` | **Separate signal family** (collision inventory: multi-frame support on pct family) | **No change** — not competing for `signal_hba1c_high` WHY |
| `signal_glucose_dysregulation_hba1c_context` | `…::inv_dysregulation_hba1c_context` | **Separate signal_id / package** | **No change** |
| `signal_hba1c_low` | shortened erythrocyte lifespan context | Separate direction/family | **Out of scope** |

No alias, merge, retirement, or suppression of these adjacent identities is permitted.

---

## 4. Approved retained and retired authority rows (Gate 1)

```text
RETAIN / COMPILE:
signal_hba1c_high::inv_hba1c_high_glycaemia
  why_role: morphology_context
  artefact: knowledge_bus/compiled/hypotheses/inv_hba1c_high_glycaemia.yaml  # post-Gate-2 only

RETIRE FOR WHY OWNERSHIP ONLY:
signal_hba1c_high::inv_hba1c_high_diabetes_range_hyperglycemia
  authority_state: LEGACY_RETIRED
  artefact_path: null
```

Package deletion forbidden. Package-layer activation and PSI status unchanged. Adjacent identities unchanged.

---

## 5. Override / escalation interpretation (Gate 1 approved)

| Rule | Condition | Result | Approved presentation |
|---|---|---|---|
| `or_hba1c_diagnostic_diabetes` | `hba1c >= 48` mmol/mol | `at_risk` | Diabetes-range concern requiring clinical confirmation only; **not** diagnosis from HbA1c alone |
| `or_hba1c_metabolic_syndrome` | TG above max AND HDL below min (canonical lab-boundary form) | `at_risk` | Subordinate metabolic-pattern context only; **no** metabolic-syndrome diagnosis |

Note: S24 `signal_library.yaml` encodes metabolic override with fixed numeric TG `>1.7` / HDL `<1.0`, while the investigation spec uses lab-range boundaries. Phase 0 / Gate 1 recording does **not** change package overrides. Compiled wording (post-Gate-2) must stay within Gate 1 boundaries above.

---

## 6. Prohibited claims (Gate 1)

- Diagnosis from HbA1c alone / unqualified diabetes diagnosis from a single result.
- Treatment directives (medication, lifestyle-prescription, pharmacological-management; raw S24 implications must not compile verbatim).
- Chronicity inference.
- Diabetes subtype.
- Complications (retinopathy/neuropathy/CVD as established disease) from this frame alone.
- Causal attribution (HbA1c independently proves diabetes-related pathology).
- Metabolic-syndrome diagnosis from TG/HDL pattern.
- Any merge with `signal_hba1c_pct_high` or glucose-dysregulation context.

---

## 7. Expected runtime and test delta (post-gate only)

| Surface | Expected change after Gate 2 |
|---|---|
| Compiled artefact | +1 under `knowledge_bus/compiled/hypotheses/` |
| Authority register | +1 `COMPILED_ACTIVE`, +1 `LEGACY_RETIRED` |
| `_PILOT_SIGNAL_IDS` | +`signal_hba1c_high` |
| Estate index / root_cause bookkeeping | Consistency updates |
| Validator `EXPECTED_KEYS` / count prints | +2 keys; active 25 / retired 20 |
| Focused ARCH-CONV-H tests | New regression module |
| Compiler / root_cause_registry mechanism | **No new mechanism** |
| Packages / PSI / SSOT / scoring / frontend | **Unchanged** |
| F / G regression suites | Must remain green |

---

## 8. Mechanism sufficiency

Existing static `why_role`, override-rule evaluator, compiled register/loader, and `LEGACY_RETIRED` → `skip` paths (proven through ARCH-CONV-B/C/F/G) are sufficient. **No change expected** in `root_cause_compiler_v1.py` or `root_cause_registry_v1.py` beyond reuse.

Hardening gap flagged for Gate 1 awareness: `pkg_s24_hba1c_high_glycaemia` carries a pre-existing non-Pass-3 revalidation flag at package layer — out of scope for WHY-only work.

---

## 9. Gate status

Gate 1: `ARCH-CONV-H-GATE1-HMR-2026-08-01` — `APPROVED_WITH_NARROWING` (recorded)  
Gate 2: `ARCH-CONV-H-GATE2-ANTHONY-2026-08-01` — `APPROVED` (ratifies Gate 1)

**Runtime implementation authorised.** Proceed under the active Automation Bus work package with Gate 1 boundaries unchanged.
