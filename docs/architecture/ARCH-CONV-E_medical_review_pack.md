# ARCH-CONV-E — ALT medical review pack

**Status:** `DRAFT_FOR_STOP_A_ARCHITECTURE_REVIEW`  
**Medical decisions:** none  
**Collision-policy decisions:** none

This pack reconstructs the questions that Phase 1 must submit to Head of
Medical Research after independent STOP A approval. It does not adjudicate any
frame, threshold, supporting-marker role, collision rule, or legacy disposition.

## 1. Canonical ALT frame

Target:

```text
signal_alt_high::inv_alt_high_hepatocellular_injury
```

Canonical source: `inv_alt_high_hepatocellular_injury_v1.yaml`.

Source facts:

- ALT is the primary high marker.
- AST is a corroborator.
- GGT and ALP are mechanism/differential context.
- bilirubin and albumin are severity context.
- exercise, statins, and alcohol are confounders/interpretation modifiers.
- the source contains one numeric ALT escalation (`120`, described as a
  typical 3×ULN assumption) and lab-boundary bilirubin/ALP rules.
- source narrative names possible NAFLD, viral, alcohol-related, and
  drug-induced contexts, but does not provide a governed runtime decision for
  specific-disease attribution.

Required Gate 1 decisions:

1. `APPROVE`, `APPROVE_WITH_NARROWING`, `REJECT`,
   `DEFER_EVIDENCE_INSUFFICIENT`, or `CONTEXT_ONLY`.
2. Causal versus context-only WHY role.
3. Whether ALT alone can support a hepatocellular biochemical-pattern WHY.
4. Magnitude/severity and serial-result requirements.
5. Symptom, history, medication, toxin, viral, alcohol, exercise, and exposure
   requirements.
6. Specific-disease prohibitions.
7. Missing-data fail-closed rules.

## 2. Pass 3 candidates

### Hepatocellular injury pattern

`signal_alt_high::inv_alt_high_hepatocellular_injury_pattern`

- AST corroborates but is not liver-specific.
- high CK strongly contradicts a liver-first interpretation.
- ALP differentiates mixed/cholestatic context.
- alcohol, medicines, viral risk, metabolic context, bilirubin, GGT, imaging,
  and exposure history are declared missing-data needs.
- current provenance is blocked for explicit-lineage WHY authority.

### Metabolic steatotic liver pattern

`signal_alt_high::inv_alt_high_metabolic_steatotic_liver_pattern`

- triglycerides and HbA1c provide metabolic context.
- CK is a strong competing muscle-source differentiator.
- adiposity, diabetes, alcohol, medication, exposure, and imaging context are
  missing.
- current provenance is blocked for explicit-lineage WHY authority.

### Muscle source or exertional pattern

`signal_alt_high::inv_alt_high_muscle_source_or_exertional_pattern`

- CK and AST support muscle/exertional context.
- high GGT weakens a muscle-only interpretation.
- exercise, trauma, muscle symptoms, medication exposures, repeat-after-rest,
  and liver-specific context are missing-data requirements.
- current provenance is blocked for explicit-lineage WHY authority.

For each candidate Gate 1 must separately decide approval, causal/context role,
provenance sufficiency, required supporting data, prohibited attribution, and
compile/defer disposition.

## 3. Current legacy ALT WHY

Asset: `knowledge_bus/root_cause/hypotheses/alt_hypotheses_v1.yaml`.

### Hypothesis 1 — `alt_hepatic_cell_stress_pattern_v1`

| Field | Current content |
|---|---|
| title / strength | Hepatic cell stress pattern / moderate |
| required | ALT |
| confirmatory | AST, GGT |
| differentiators | bilirubin, ALP |
| evidence for | ALT high/flagged; `signal_hepatic_alt_context` fired |
| evidence against | ALT clearly normal |
| missing data | AST, GGT |
| confirmatory test | `test_liver_ggt_alt_ast_v1` |

Traceability:

- ALT, AST, GGT, bilirubin, and ALP roles broadly overlap the canonical source.
- the family signal requirement is legacy implementation authority, not
  canonical research authority.
- the summary is narrower than the canonical disease examples and remains
  biochemical/contextual.

### Hypothesis 2 — `alt_inflammatory_coupling_context_v1`

| Field | Current content |
|---|---|
| title / strength | Hepatic-inflammatory coupling context / exploratory |
| required | ALT |
| confirmatory | CRP |
| evidence for | CRP high; `signal_systemic_inflammation` fired |
| evidence against | none |
| missing data | CRP |
| confirmatory tests | `test_liver_ggt_alt_ast_v1`, `test_crp_repeat_v1` |

Traceability gap:

- CRP/systemic-inflammatory coupling is not present in the canonical ALT
  investigation spec. It must not be silently transferred.

### Current runtime route and duplicate risk

```text
ROOT_CAUSE_TARGET_SPECS
→ signal_hepatic_alt_context
→ load_alt_hypotheses_v1()
→ alt_hypotheses_v1.yaml
→ family-level legacy compiler path
```

Observed baseline:

- predecessor only: both legacy hypotheses emit;
- canonical only: generic `why_engine_fallback_v1` emits;
- both live ALT signals: generic canonical fallback and legacy predecessor WHY
  emit in parallel.

This can create duplicate ALT user-facing framing. No disconnection is allowed
before Gate 1 and Gate 2 specify the replacement condition.

## 4. Threshold reconstruction

Baseline activation in both packages is `lab_range_exceeded`; `9999.0` is a
validator placeholder and is not the activation cutoff.

| Signal / rule | Literal | Governed source | Purpose | Runtime effect | Canonical-source relation | Transfer risk |
|---|---:|---|---|---|---|---|
| canonical placeholder ALT | 9999 | none; validator compatibility | schema placeholder | none while lab-range activation applies | not medical | must not become runtime cutoff |
| canonical ALT severity | 120 | canonical numeric rule; assumes typical ULN≈40 | 3×ULN escalation | upgrades to `at_risk` | explicit, but fixed-value translation loses per-lab ULN | changing to lab status changes behavior |
| canonical bilirubin | 20 | package literal; canonical source says `above_max` | impaired-function context | upgrades to `at_risk` | translation is not source-equivalent | transfer/retention needs decision |
| canonical ALP | 130 | package literal; canonical source says `above_max` | mixed/cholestatic context | upgrades to `at_risk` | translation is not source-equivalent | transfer/retention needs decision |
| predecessor placeholder ALT | 9999 | none; validator compatibility | schema placeholder | none while lab-range activation applies | no canonical identity | must not become runtime cutoff |
| predecessor AST | 45 | package-local only | multimarker escalation | any one arm upgrades to `at_risk` | AST is canonical corroborator, not fixed at 45 | silent transfer changes behavior |
| predecessor GGT | 60 | package-local only | multimarker escalation | any one arm upgrades to `at_risk` | GGT is canonical context, not fixed at 60 | silent transfer changes behavior |
| predecessor ALP | 130 | package-local only | multimarker escalation | any one arm upgrades to `at_risk` | canonical source uses lab boundary | silent transfer changes behavior |
| predecessor bilirubin | 20 | package-local only | multimarker escalation | any one arm upgrades to `at_risk` | canonical source uses lab boundary | silent transfer changes behavior |

None of the package-local fixed values is read from governed biomarker SSOT at
evaluation time. Gate 1 must select one allowed threshold disposition for each.

## 5. Proposed hepatocellular authority boundary (not adjudicated)

Questions for Gate 1:

- Can canonical ALT be primary for a hepatocellular biochemical pattern, and
  under what minimum evidence?
- Is AST corroborating context only?
- Are bilirubin and albumin severity/function context only?
- Do ALP/GGT redirect toward a concurrent cholestatic/mixed pattern without
  changing `cholestatic_source_axis`?
- Do CK, exercise, trauma, and muscle symptoms contradict or redirect hepatic
  attribution?
- Are metabolic markers context only unless the metabolic candidate is
  independently approved?
- Are alcohol, medicines, viral risk, toxins, symptoms, and serial results
  required before narrower causal language?

Potential group requirement:

- reserve a new `hepatocellular_injury_axis`;
- select by explicit activation key;
- keep ALT authority separate from `cholestatic_source_axis`;
- permit parallel output only for medically distinct, ratified layers;
- consolidate or refuse duplicate ALT-family output;
- never grant independent AST or bilirubin WHY authority through this axis.

No group name, primary eligibility, consolidation rule, or medical policy is
approved by this Phase 0 record.

## 6. Legacy disposition options

Gate 1 must choose exactly one:

- `CONDITIONAL_REPLACE`
- `PARTIAL_CONTENT_TRANSFER`
- `RETAIN_TEMPORARILY`
- `RETIRE_WITHOUT_TRANSFER`
- `DEFER`

It must specify when the registry target for `signal_hepatic_alt_context` may be
disconnected, whether either legacy hypothesis transfers, and how generic WHY
fallback for `signal_alt_high` becomes unreachable when governed authority is
present.

## 7. Preserved exclusions

No independent authority is requested for AST, bilirubin,
hyperbilirubinemia, or ALP-low. No change is requested to ALP/GGT compiled
content, `cholestatic_source_axis`, liver-card scoring, or frontend logic.
