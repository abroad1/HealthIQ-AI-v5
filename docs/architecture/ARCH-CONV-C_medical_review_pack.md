# ARCH-CONV-C — ALP/GGT Medical-Review Pack

**Work ID:** `ARCH-CONV-C`  
**Date (UTC):** 2026-07-30 (Phase 1 finalisation)  
**Pack state:** `GATE_1_SUBMISSION_READY_FOR_HEAD_OF_MEDICAL_RESEARCH`  
**STOP A approval:** Head of Architecture, recorded 2026-07-30 (see `ARCH-CONV-C_STOP_A_identity_and_source_closure.md`)  
**Medical decisions:** **NONE — requested from Head of Medical Research (Gate 1)**  
**Collision-policy decisions:** **NONE — requested from Head of Medical Research (Gate 1)**  
**Gate 1 reference:** PENDING  
**Gate 2 reference:** PENDING  
**Runtime authority:** **NOT AUTHORISED**

This is the finalised Gate 1 submission pack. STOP A is approved by the Head of
Architecture, authorising this finalisation only. It preserves all STOP A
evidence and requests structured medical and collision-policy decisions from the
Head of Medical Research. Cursor makes no medical decision here, and this record
authorises no compilation, runtime activation, authority registration, collision
policy population, or legacy disconnection.

Allowed reviewer decisions per candidate frame:

```text
APPROVE
APPROVE_WITH_NARROWING
REJECT
DEFER_EVIDENCE_INSUFFICIENT
CONTEXT_ONLY
```

## Review scope

| Item | Review role |
|---|---|
| `signal_alp_high::inv_alp_high_bone_biliary` | Provisional canonical migration target |
| `signal_ggt_high::inv_ggt_high_hepatic` | Provisional canonical migration target |
| Two ALP Pass 3 frames | Candidate decomposition evidence |
| Two GGT Pass 3 frames | Candidate decomposition evidence |
| `liver_injury_axis` | First medical/collision-policy adjudication required |
| ALT, AST, bilirubin/hyperbilirubinemia, ALP-low | Explicit boundaries only; no decision requested |

## Identity and authority baseline

| Target | Embedded identity | Canonical source | Current WHY authority | Compiled WHY |
|---|---|---|---|---|
| ALP high | `signal_alp_high::inv_alp_high_bone_biliary` | `knowledge_bus/research/investigation_specs/inv_alp_high_bone_biliary.yaml` | Legacy `alp_high_hypotheses_v1.yaml` | none |
| GGT high | `signal_ggt_high::inv_ggt_high_hepatic` | `knowledge_bus/research/investigation_specs/inv_ggt_high_hepatic.yaml` | Legacy `ggt_high_hypotheses_v1.yaml` | none |

Both signals remain outside the compiled WHY cohort. Their live signal-layer
frames are distinct by activation key, but all fired frames currently fall
through to the same family-level legacy WHY loader.

## Candidate 1 — ALP high

### Canonical source transcription

- ALP is present in liver and bone; elevated values do not localise tissue origin.
- High GGT is recorded as a differential marker supporting hepatic origin.
- High bilirubin is recorded as a mechanism marker for cholestatic context.
- Calcium provides bone-context corroboration.
- The canonical escalation rule requires both high GGT and high bilirubin.
- Pregnancy and adolescence are recorded interpretation-shift confounders.
- Narrative text says GGT is required to determine tissue origin and lists both
  biliary and bone implications.

These are source facts, not medical approval.

### Parallel Pass 3 evidence

| Candidate | Key boundary | Current governance/runtime state |
|---|---|---|
| `inv_alp_high_cholestatic_pattern` | ALP alone cannot localise source; normal GGT strongly contradicts hepatobiliary origin | v3 Pass 3 record; translated package loaded with blocked provenance; no compiled WHY |
| `inv_alp_high_high_bone_turnover_pattern` | Normal GGT supports a provisional non-hepatic differential but does not diagnose bone disease | v3 Pass 3 record; no separate runtime package found; no compiled WHY |

The Pass 3 coverage audit also lists two ALP-low frames under the ALP-high
family. They are directionally separate and excluded.

### Current legacy risk

The legacy ALP WHY asset contains:

- `alp_high_hepatobiliary_pattern_v1`
- `alp_high_bilirubin_cholestatic_context_v1`

The first hypothesis can be produced from the ALP-high signal with GGT represented
as missing data rather than as a ratified eligibility gate. This risks presenting
hepatic/cholestatic interpretation where a bone or other non-hepatic source
remains plausible.

### Gate 1 questions after STOP A

1. Is the combined canonical ALP bone/biliary frame acceptable, or must it be
   narrowed/decomposed?
2. May ALP alone ever support causal WHY, or only a non-specific/context frame?
3. Is high GGT required before hepatobiliary interpretation becomes eligible?
4. Is high bilirubin required for cholestatic escalation, severity context, or
   causal eligibility?
5. Is the Pass 3 cholestatic frame causal, context-only, rejected, or deferred?
6. Is the Pass 3 high-bone-turnover frame causal, context-only, rejected, or
   deferred?
7. How must normal/absent GGT redirect or suppress hepatic output?
8. How must missing bilirubin, calcium, phosphate, vitamin D, age, pregnancy,
   bone history, symptoms, serial results, or imaging fail closed?
9. What wording prevents isolated ALP from diagnosing obstruction, cholestatic
   disease, high bone turnover, vitamin-D-related bone disease, or malignancy?
10. Under what conditions, if any, may legacy ALP WHY later be disconnected?

## Candidate 2 — GGT high

### Canonical source transcription

- GGT is described as a sensitive marker of hepatobiliary and oxidative stress.
- The source also names alcohol use, NAFLD, and enzyme-inducing medicines.
- High ALP is a mechanism marker for a cholestatic pattern.
- ALT is a corroborator for hepatocellular injury.
- High MCV is a differential marker for chronic alcohol-use context.
- The escalation rule requires concurrent high ALP.
- Enzyme-inducing drugs are a structured false-positive confounder.

These are source facts, not medical approval.

### Parallel Pass 3 evidence

| Candidate | Key boundary | Current governance/runtime state |
|---|---|---|
| `inv_ggt_high_hepatobiliary_cholestatic_context` | High ALP supports hepatobiliary source; normal ALP strongly weakens cholestatic interpretation | v3 Pass 3 record + translated package + staged PSI; signal frame loaded with blocked provenance; no compiled WHY |
| `inv_ggt_high_alcohol_or_enzyme_induction_context` | GGT is non-specific and must not alone infer alcohol exposure or liver-disease severity | v3 Pass 3 record + translated package + staged PSI; signal frame loaded with blocked provenance; no compiled WHY |

### Current legacy risk

The legacy GGT WHY asset contains:

- `ggt_elevated_hepatic_enzyme_v1`
- `ggt_metabolic_inflammatory_coupling_v1`

It does not preserve a governed causal/context-only split between hepatobiliary,
alcohol/enzyme-induction, and metabolic/inflammatory explanations. Alcohol and
medicine exposure are not structured runtime inputs, so attributive wording
cannot be safely inferred from absence of data.

### Gate 1 questions after STOP A

1. Is the canonical GGT frame medically acceptable, or must it be narrowed?
2. May isolated GGT ever support causal hepatobiliary WHY?
3. Is ALP concordance required for hepatobiliary/cholestatic eligibility?
4. Is the Pass 3 hepatobiliary frame causal, context-only, rejected, or deferred?
5. Is alcohol/enzyme-induction content context-only, rejected, or deferred?
6. Can high MCV ever strengthen alcohol context without structured alcohol
   history, and what wording remains non-attributive?
7. How do normal/absent ALP, ALT and bilirubin alter role or eligibility?
8. How must absent alcohol history, medication exposure, symptoms, serial
   results, metabolic context, or imaging fail closed?
9. What wording prevents isolated GGT from diagnosing alcohol misuse, NAFLD,
   cholestasis, obstruction, or hepatobiliary disease?
10. Under what conditions, if any, may legacy GGT WHY later be disconnected?

## `liver_injury_axis` decision pack

### Current placeholder

The existing governance row is not adjudicated and has no runtime action:

```yaml
authority_group_id: liver_injury_axis
biological_axis: hepatocellular_injury
status: placeholder_not_adjudicated
primary_signal_family: null
supporting_signal_families: []
collision_policy:
  no_duplicate_user_facing_signal: null
  suppress_supporting_when_primary_present: null
  consolidate_into_shared_interpretation: null
  allow_parallel_if_distinct_risk_layer: null
runtime_action: none_governance_only
requires_runtime_support: false
```

Its notes mention ALT / AST / GGT / bilirubin but omit ALP. No inference may be
drawn from this omission.

### Medical/collision decisions required

1. Can ALP or GGT ever be primary authority on this axis?
2. Must ALP or GGT remain supporting/context-only in any pattern?
3. Is concurrent high ALP and high GGT required before hepatobiliary or
   cholestatic causal output?
4. What is the deterministic outcome for high ALP with normal GGT?
5. What is the deterministic outcome for high GGT with normal ALP?
6. Does concurrent bilirubin alter severity only, eligibility, or neither?
7. How are bone-turnover, alcohol, medicine-induced enzyme induction, and
   metabolic context represented without becoming unsupported causes?
8. When are parallel ALP and GGT outputs allowed, consolidated, suppressed, or
   refused?
9. Which signal becomes primary/supporting/context for each concordant and
   discordant pattern?
10. How will future ALT and bilirubin packages join without being pre-empted,
    aliased, or medically decided by ARCH-CONV-C?
11. Is the current `biological_axis: hepatocellular_injury` label adequate for an
    ALP/GGT package that includes cholestatic and non-hepatic differentials?
12. Which policy fields and any required preconditions must be explicit so the
    runtime never relies on package, filename, lexical, filesystem, or load order?

## Explicit exclusions

- `signal_alt_high` and `signal_hepatic_alt_context`: identity and authority
  relationship unresolved; no decision or change.
- `signal_ast_high`: no canonical WHY target; none may be invented.
- `signal_bilirubin_high`: retired WHY identity; no reopening.
- `signal_hyperbilirubinemia`: surviving legacy family without canonical
  investigation spec; no migration or collision decision.
- `signal_alp_low`: separate direction; no decision or change.

ALT and bilirubin may appear only as source-recorded supporting, contradiction,
or future-boundary context. This does not grant either family WHY authority.

## Gate 1 decisions requested from Head of Medical Research

For each item below, the Head of Medical Research is asked to record a structured
decision, role, evidence rationale, and any legacy/collision disposition into
`docs/architecture/ARCH-CONV-C_medical_decision_register.yaml`. Cursor records
nothing here.

### ALP — `signal_alp_high::inv_alp_high_bone_biliary` (+ Pass 3 candidates)

| Decision item | Requested output |
|---|---|
| Causal versus context-only role | `causal` / `context_only` / `rejected` / `deferred` for the canonical frame |
| Bone versus hepatobiliary interpretation | Which interpretation(s) the frame may express, and which are prohibited from ALP alone |
| High-GGT concordance requirement | Whether high GGT is required before any hepatobiliary/cholestatic interpretation is eligible |
| Bilirubin role | Whether bilirubin is required for cholestatic escalation, severity-only, or neither |
| Pass 3 cholestatic frame | Role for `inv_alp_high_cholestatic_pattern` |
| Pass 3 high-bone-turnover frame | Role for `inv_alp_high_high_bone_turnover_pattern` (unpackaged) |
| Fail-closed handling | Behaviour when GGT, bilirubin, calcium, phosphate, vitamin D, bone history, pregnancy/age, serial results, or imaging are absent |
| Legacy disposition | Retain, conditionally replace, or unchanged for `alp_high_hypotheses_v1.yaml` |

### GGT — `signal_ggt_high::inv_ggt_high_hepatic` (+ Pass 3 candidates)

| Decision item | Requested output |
|---|---|
| Hepatobiliary causal eligibility | Whether GGT may support causal hepatobiliary WHY, and under what concordance |
| Alcohol / medicine-induction role | `causal` / `context_only` / `rejected` / `deferred` for the alcohol/enzyme-induction content |
| Metabolic-context role | Role for metabolic/steatotic-liver context |
| ALP concordance requirement | Whether high ALP is required before hepatobiliary/cholestatic eligibility, and how it changes role/confidence |
| MCV handling | Whether/how MCV may add non-attributive alcohol context |
| Pass 3 hepatobiliary frame | Role for `inv_ggt_high_hepatobiliary_cholestatic_context` |
| Pass 3 alcohol/induction frame | Role for `inv_ggt_high_alcohol_or_enzyme_induction_context` |
| Fail-closed handling | Behaviour when alcohol history, medication exposure, ALP, ALT, bilirubin, metabolic context, serial results, or imaging are absent |
| Legacy disposition | Retain, conditionally replace, or unchanged for `ggt_high_hypotheses_v1.yaml` |

### liver_injury_axis — collision-policy adjudication

| Decision item | Requested output |
|---|---|
| Primary / supporting / context roles | Whether ALP or GGT may be primary; which is supporting or context-only |
| Concordant ALP+GGT behaviour | Deterministic outcome when both are high |
| Discordant high-ALP / normal-GGT behaviour | Deterministic outcome and any redirection to bone/non-hepatic context |
| Discordant high-GGT / normal-ALP behaviour | Deterministic outcome and any suppression of cholestatic causality |
| Suppression / consolidation / refusal rules | Which of the four `collision_policy` fields become true/false, plus any preconditions |
| Axis label adequacy | Whether `biological_axis: hepatocellular_injury` is adequate or must be narrowed/renamed |
| Future-safe ALT/bilirubin boundary | How future ALT and bilirubin authority may join without displacement or pre-decision |

Deterministic selection is mandatory: no filename, package-name, lexical,
filesystem, or load-order selection is permitted. Concurrent same-signal
different-key candidates (S24 versus Pass 3) must be resolved by explicit,
ratified authority, not order.

## Gate status

| Requirement | State |
|---|---|
| Embedded identities verified | COMPLETE |
| Canonical, Pass 3, package and legacy sources mapped | COMPLETE |
| Compiled authority state identified | COMPLETE — none |
| `liver_injury_axis` placeholder reconstructed | COMPLETE |
| Exclusions documented | COMPLETE |
| Independent STOP A | **APPROVED (Head of Architecture, 2026-07-30)** |
| Structured Gate 1 decision requests assembled | COMPLETE |
| Head of Medical Research Gate 1 | **AWAITING DECISIONS** |
| Anthony Gate 2 | **NOT STARTED** |
| Runtime or compiled changes | **0** |

```text
GATE 1 SUBMISSION READY — AWAITING HEAD OF MEDICAL RESEARCH DECISIONS
```

Cursor has made no medical or collision-policy decision. Compilation, collision
policy population, and runtime work remain blocked until both Gate 1 (Head of
Medical Research) and Gate 2 (Anthony ratification) are recorded.
