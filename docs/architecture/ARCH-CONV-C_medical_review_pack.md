# ARCH-CONV-C — ALP/GGT Medical-Review Pack

**Work ID:** `ARCH-CONV-C`  
**Date (UTC):** 2026-07-30  
**Pack state:** `PHASE_0_DRAFT_AWAITING_STOP_A_APPROVAL`  
**Medical decisions:** **NONE**  
**Collision-policy decisions:** **NONE**  
**Runtime authority:** **NOT AUTHORISED**

This Phase 0 draft records repository evidence and the questions that a later
Head of Medical Research Gate 1 must answer. It is not yet a Gate 1 submission.
Cursor has made no medical decision and has not compiled, registered, activated,
retired, or disconnected any WHY authority.

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

## Gate status

| Requirement | State |
|---|---|
| Embedded identities verified | COMPLETE |
| Canonical, Pass 3, package and legacy sources mapped | COMPLETE |
| Compiled authority state identified | COMPLETE — none |
| `liver_injury_axis` placeholder reconstructed | COMPLETE |
| Exclusions documented | COMPLETE |
| Independent STOP A | **PENDING** |
| Head of Medical Research Gate 1 | **NOT STARTED** |
| Anthony Gate 2 | **NOT STARTED** |
| Runtime or compiled changes | **0** |

```text
PHASE 0 DRAFT COMPLETE — AWAITING INDEPENDENT STOP A
```
