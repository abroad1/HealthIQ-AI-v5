# ARCH-CONV-H — Phase 0 Hardening Pack (Gate 1 / Gate 2 STOP)

**Work ID:** `ARCH-CONV-H`  
**Branch:** `feature/arch-conv-h-hba1c-compiled-why-authority`  
**Risk:** HIGH  
**Change type:** MIXED  
**Execution model:** TWO_PHASE_START_FINISH  
**Implementation owner:** Core Engine agent  
**Status:** Phase 0 mapping complete. Gate 1 `PENDING`. Gate 2 `PENDING`. **Implementation prohibited** until both gates are recorded on disk and match this pack (or the prompt is revised and re-hardened).

**Hardening clearance:** `automation_bus/latest_prompt_hardening.json` — `ARCH-CONV-H` / `HARDENED` (Phase 0 + Gate STOP only).

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

### Proposed compiled-WHY content boundary (Gate 1 must ratify)

- Identify a **persistent hyperglycaemia / sustained glycaemic-exposure pattern** supported by the canonical source.
- HbA1c is **not** an independently proven cause of diabetes-related pathology.
- Diabetes-range escalation only via governed `>= 48 mmol/mol` threshold with **cautious** wording.
- One HbA1c result must not be an unqualified diabetes diagnosis where confirmation/repeat/symptoms/clinical assessment are required.
- TG/HDL (and ALT if mentioned) may enrich metabolic context only to the extent Gate 1 authorises from this source.
- No treatment, medication, complication diagnosis, unsupported chronicity, or unsupported causal claims.

### Proposed `why_role` (Gate 1 must ratify)

**Primary recommendation:** `morphology_context` (flat; no `conditional_why_role`).

**Alternative for Gate 1 only:** narrowed `causal` limited strictly to “sustained glycaemic-exposure / persistent hyperglycaemia pattern” with identical presentation prohibitions.

Rationale for morphology_context preference: diabetes-diagnosis and treatment-directive risks in source narrative; matches urate/HDL/urea non-diagnostic pattern when pathology claims must not fire.

---

## 2. Package collision and ownership table

| Package | Activation key | Source / provenance | WHY ownership (current) | Package / PSI | Proposed disposition |
|---|---|---|---|---|---|
| `pkg_s24_hba1c_high_glycaemia` | `signal_hba1c_high::inv_hba1c_high_glycaemia` | `inv_hba1c_high_glycaemia_v1.yaml` | Legacy WHY via registry (no compiled row) | Active package; **no PSI file** | **RETAIN / COMPILE** as canonical |
| `pkg_kb52c_hba1c_high_diabetes_range_hyperglycemia` | `signal_hba1c_high::inv_hba1c_high_diabetes_range_hyperglycemia` | `Batch_6_Pass_3.json` | Competing same-`signal_id` frame | Active package; `behavioural_impact: NONE`; **no PSI file** | **LEGACY_RETIRED_FOR_WHY_ONLY** |

Collision inventory confirms governed arbitration (2 packages). Hardening notes SignalRegistry lexicographic overwrite currently prefers S24 live winner — WHY retirement still required so the competitor cannot dual-serve as compiled/legacy WHY owner after pilot inclusion.

**Expected post-gate register delta (subject to Gate 1):** `+1 COMPILED_ACTIVE` / `+1 LEGACY_RETIRED`.

---

## 3. Adjacent identity exclusion table

| Identity | Activation key(s) | Relation to `signal_hba1c_high` WHY | ARCH-CONV-H action |
|---|---|---|---|
| `signal_hba1c_pct_high` | `…::inv_hba1c_pct_high_chronic_hyperglycemia_diabetes`; `…::inv_hba1c_pct_high_red_cell_turnover_bias_or_iron_deficiency` | **Separate signal family** (collision inventory: multi-frame support on pct family) | **No change** — not competing for `signal_hba1c_high` WHY |
| `signal_glucose_dysregulation_hba1c_context` | `…::inv_dysregulation_hba1c_context` | **Separate signal_id / package** | **No change** |
| `signal_hba1c_low` | shortened erythrocyte lifespan context | Separate direction/family | **Out of scope** |

No alias, merge, retirement, or suppression of these adjacent identities is permitted.

---

## 4. Proposed retained and retired authority rows

```text
RETAIN / COMPILE:
signal_hba1c_high::inv_hba1c_high_glycaemia
  why_role: morphology_context   # or Gate-1-chosen alternative
  artefact: knowledge_bus/compiled/hypotheses/inv_hba1c_high_glycaemia.yaml  # post-gate only

RETIRE FOR WHY OWNERSHIP ONLY:
signal_hba1c_high::inv_hba1c_high_diabetes_range_hyperglycemia
  authority_state: LEGACY_RETIRED
  artefact_path: null
```

Package deletion forbidden. Package-layer activation and PSI status unchanged.

---

## 5. Override / escalation interpretation (proposed)

| Rule | Condition | Result | Proposed presentation |
|---|---|---|---|
| `or_hba1c_diagnostic_diabetes` | `hba1c >= 48` mmol/mol | `at_risk` | Concern / diabetes-range escalation only; **not** unqualified diabetes diagnosis from one result |
| `or_hba1c_metabolic_syndrome` | TG above max AND HDL below min (canonical lab-boundary form) | `at_risk` | Metabolic-pattern concern escalation / context only if Gate 1 authorises; **not** metabolic-syndrome diagnosis |

Note: S24 `signal_library.yaml` encodes metabolic override with fixed numeric TG `>1.7` / HDL `<1.0`, while the investigation spec uses lab-range boundaries. Phase 0 does **not** change package overrides. Gate 1 should ratify whether compiled wording follows the **canonical lab-boundary** semantics and whether any fixed-number wording is prohibited.

---

## 6. Prohibited claims (proposed for Gate 1)

- Unqualified diabetes diagnosis from a single HbA1c result (unless Gate 1 explicitly authorises a precise bounded statement).
- Treatment, medication, lifestyle-prescription, or pharmacological-management directives (raw S24 implications must not compile verbatim).
- Complication diagnosis (retinopathy/neuropathy/CVD as established disease) from this frame alone.
- Unsupported chronicity beyond the marker’s supported ~8–12 week exposure interpretation.
- Causal claim that HbA1c independently proves diabetes-related pathology.
- TG/HDL/ALT use beyond Gate-1-authorised context enrichment.
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

## 9. Gate STOP

This Phase 0 pack is committed with Gate 1 / Gate 2 statuses **PENDING**.

Return for:

1. GPT / Head of Medical Research Gate 1 (`ARCH-CONV-H-GATE1-HMR-PENDING` → replace on approval) — must record approved `why_role`, claim boundary, diabetes-range wording, TG/HDL use, prohibited claims, retained key, retired key.
2. Anthony Gate 2 (`ARCH-CONV-H-GATE2-ANTHONY-PENDING` → replace on approval).

**Do not create compiled artefacts, alter authority registers, retire legacy ownership, or change runtime behaviour until both approvals are committed and consistent with this pack.**
