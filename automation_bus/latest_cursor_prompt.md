---
work_id: ARCH-CONV-E2
branch: feature/arch-conv-e2-alt-rvalue-runtime-authority
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# ARCH-CONV-E2 — ALT R-Value Authority, Collision Governance and Explicit Runtime Promotion

Execute under:

- `AUTOMATION_BUS_SOP_v1.3.1.md`
- `KNOWLEDGE_BUS_SOP_v1.3.1.md`
- `KNOWLEDGE_BUS_PASS3_PROMOTION_PROTOCOL_v1.1.md`
- accepted research-to-runtime ADRs and current repository governance artefacts

This prompt is for Claude Code hardening before Cursor execution.

## Product outcome

Complete the governed ALT-high WHY-authority migration by:

1. creating the governed `r_value_alt_alp` derived-metric compute authority;
2. adjudicating ALT R-value frames against the existing ALP/GGT liver-injury authority;
3. explicitly promoting only medically and technically eligible ALT packages;
4. proving correct runtime reachability, fail-closed behaviour and legacy disposition.

Do not reopen Pass 1–3 research or rebuild the six Knowledge Bus packages unless hardening identifies a concrete package defect.

## Repository-verified starting point

Before hardening, verify the merged repository state rather than relying on this prompt alone.

Expected starting state:

- six validated ARCH-CONV-E ALT sibling packages exist under `knowledge_bus/packages/`;
- each contains the mandatory package assets and `promoted_signal_intelligence.yaml`;
- none contains `intelligence_model.yaml`;
- all six are withheld from runtime activation;
- package placement alone no longer implies activation;
- the governed runtime activation register exists;
- `pkg_s24_alt_high_hepatocellular_injury` remains the active ALT frame;
- the three former Batch 5 ALT frames are superseded by canonical regeneration and removed from accidental runtime reachability;
- no independent medical-retirement process has yet been completed for those former frames;
- `r_value_alt_alp` has no governed runtime compute authority;
- the existing ALP/GGT `liver_injury_axis` remains governed separately.

If any expected fact is false, hardening must correct the prompt scope before execution.

## Canonical medical authority

Use only the validated Pass 3 source and its six promoted package assets as medical authority:

`knowledge_bus/research/investigation_specs/multi_llm_research/ALT_High_Hepatic_Pattern_Classification_ARCH_CONV_E_Pass_3.json`

Expected SHA-256:

`7F20BF9A06B3427217AD7F753C4D9304E5D5A2C46C484699257778844B9D3267`

Source specs:

1. `inv_alt_high_r_value_hepatocellular_biochemical_pattern`
2. `inv_alt_high_r_value_mixed_biochemical_pattern`
3. `inv_alt_high_r_value_cholestatic_alp_predominant_context`
4. `inv_alt_high_muscle_source_or_exertional_contribution`
5. `inv_alt_high_bilirubin_hys_law_severity_context`
6. `inv_alt_high_metabolic_masld_context`

Do not add, reinterpret or weaken medical claims, thresholds, exclusions, caveats or safety wording.

## Phase 0 — hardening and exact target mapping

Claude Code must inspect and harden against:

- the six ALT package manifests, signal libraries, research briefs and PSI assets;
- the current derived-metric registries and established metric-definition conventions;
- laboratory ULN handling and same-sample/contemporaneous-data conventions;
- `SignalRegistry` and package activation-register semantics;
- `signal_authority_collision_model_v1.yaml`;
- the existing ALP/GGT `liver_injury_axis`;
- current root-cause/WHY compilation and activation paths;
- the current legacy ALT runtime authority;
- tests governing package reachability, collision precedence, deterministic evaluation and missing-data behaviour.

Hardening must replace generic placeholders with exact repository paths, schema fields, IDs, commands and expected outputs.

Do not author a new parallel framework where an existing governed mechanism can represent the requirement.

## Required implementation

### 1. Governed `r_value_alt_alp` derived metric

Implement the derived metric using the repository’s established governed derived-metric architecture.

Medical definition:

```text
R = (ALT / ALT laboratory ULN) / (ALP / ALP laboratory ULN)
```

Classification:

```text
R >= 5       → hepatocellular biochemical pattern
2 < R < 5    → mixed biochemical pattern
R <= 2       → cholestatic / ALP-predominant biochemical context
```

Required eligibility:

- ALT result present;
- ALT laboratory ULN present and valid;
- ALP result present;
- ALP laboratory ULN present and valid;
- ALT and ALP satisfy the repository’s governed contemporaneous/same-sample rule;
- no divide-by-zero or invalid-reference-range path;
- deterministic output and provenance.

Required fail-closed behaviour:

- do not calculate or classify when either result is absent;
- do not calculate or classify when either ULN is absent, zero or invalid;
- do not infer a generic ULN;
- do not substitute population thresholds;
- do not emit an R-value-dependent frame when pairing eligibility is not met;
- expose the governed missing/deferred reason through the existing evidence or provenance contract.

Use existing numeric precision and boundary conventions. Harden exact boundary tests for `2` and `5`.

### 2. ALT / ALP / GGT collision governance

Extend the existing governed collision model rather than adding local evaluator branching.

The adjudication must cover:

- ALT-predominant R-value frame;
- mixed ALT/ALP R-value frame;
- ALP-predominant/cholestatic R-value context;
- existing ALP/GGT `liver_injury_axis`;
- bilirubin severity context;
- muscle/exertional contribution;
- metabolic/MASLD context;
- retained S24 ALT authority during transition.

Required principles:

- one laboratory pattern must not create contradictory primary WHY authorities;
- R-value frames must not duplicate or silently override the governed ALP/GGT axis;
- bilirubin severity is escalation/context, not a competing anatomical diagnosis;
- muscle/exertional and metabolic frames may coexist only according to canonical supporting/contradiction rules;
- no consumer-facing Hy’s Law diagnosis or terminology;
- missing R-value eligibility must fail closed, not fall through to a misleading R-value frame;
- precedence, coexistence and suppression must be explicit, deterministic and testable.

Hardening must identify the exact authority-group and collision-policy changes required.

### 3. Explicit package promotion and activation

Use the existing Knowledge Bus promotion and governed activation mechanisms.

For each of the six packages, produce an explicit readiness decision:

- `PROMOTE_AND_ACTIVATE`
- `PROMOTE_BUT_WITHHOLD`
- `DEFERRED_WITH_EXPLICIT_REASON`

Use existing repository vocabulary where it differs; do not invent a second status system.

Promotion must include the protocol-required lineage and evidence:

- source spec ID;
- source path and source hash;
- package/output artefacts and hashes;
- validation result;
- promotion mode/version;
- promotion timestamp where applicable;
- activation-register decision;
- collision-governance dependency;
- runtime proof.

Do not activate a package merely because its assets validate.

Do not activate any R-value-dependent package until the metric, collision model and runtime tests all pass.

### 4. Legacy ALT disposition

Reconcile:

- `pkg_s24_alt_high_hepatocellular_injury`;
- the three superseded Batch 5 activation keys;
- the six canonical ARCH-CONV-E package frames.

The former Batch 5 keys must remain:

> Superseded by canonical regeneration and removed from accidental runtime reachability; replacement frames remain unactivated pending explicit promotion.

Do not reactivate the old inferred keys.

Do not claim completed medical retirement unless the governing retirement process is actually executed and evidenced.

The retained S24 frame may be superseded, retained temporarily or retired only through an explicit, tested and medically governed decision. Hardening must identify the applicable repository mechanism and required authority evidence.

## Runtime and output requirements

Prove:

- `r_value_alt_alp` is calculated only from eligible paired ALT/ALP results and their own laboratory ULNs;
- all three R-value boundaries behave exactly as specified;
- absent/invalid ULNs and non-contemporaneous inputs fail closed;
- only explicitly activated packages load;
- withheld packages remain absent from the production registry;
- collision precedence produces no duplicate or contradictory primary authority;
- existing ALP/GGT behaviour is preserved except where the new governed collision decision explicitly changes it;
- no frontend medical inference is introduced;
- raw Pass 3 research is not read at runtime;
- emitted reasoning remains traceable to package/spec/metric provenance.

## Required tests

Hardening must identify exact existing tests and the minimum new tests required. At minimum cover:

1. R-value formula correctness.
2. Exact boundary cases: below, at and above `2`; below, at and above `5`.
3. Missing ALT, ALP, ALT ULN and ALP ULN.
4. Zero/invalid ULN.
5. Non-contemporaneous or mismatched sample eligibility.
6. Deterministic repeatability.
7. Hepatocellular, mixed and cholestatic frame selection.
8. ALT R-value versus ALP/GGT collision precedence.
9. Bilirubin severity escalation without diagnostic wording.
10. Muscle-source contradiction/redirect behaviour.
11. Metabolic context coexistence/suppression behaviour.
12. Production registry before/after activation.
13. Withheld-package exclusion.
14. Retained or superseded S24 behaviour according to the approved disposition.
15. No non-ALT runtime regression.
16. Package validators and promotion-lineage checks.
17. Existing launch-critical, rejected-frame and test-only opt-in behaviour.

Use a clean baseline and the gate ladder:

```text
clean HEAD probe
→ focused metric tests
→ collision/authority tests
→ package and promotion validators
→ runtime reachability tests
→ baseline harness
→ exact-node baseline attribution for any failures
```

Do not start with an uncontrolled full backend suite. Run broader suites only where required by the hardened risk assessment.

## Evidence deliverables

Publish a bounded ARCH-CONV-E2 evidence report containing:

- verified starting state;
- exact files changed;
- R-value metric definition and registration;
- eligibility and fail-closed contract;
- collision-authority decision table;
- per-package promotion and activation disposition;
- legacy ALT disposition;
- source/output hashes and promotion lineage;
- before/after runtime registry identities and counts;
- test commands and results;
- baseline attribution for any failures;
- confirmation of no raw-research runtime read;
- confirmation of no frontend inference;
- unresolved risks or deferred packages;
- `git diff --name-only` and scoped diff summary.

## Prohibitions

Do not:

- modify the canonical Pass 3 research;
- create new medical research;
- invent R-value thresholds or ULNs;
- use generic population ULNs;
- bypass package promotion with direct evaluator logic;
- encode ALT-specific collision precedence outside the governed collision mechanism unless hardening proves the current contract cannot represent it and returns for approval;
- reactivate superseded Batch 5 keys;
- activate all six packages by default;
- read raw research at runtime;
- add frontend interpretation;
- broaden into unrelated liver, package-estate or derived-metric cleanup;
- repair unrelated failing tests;
- silently expand beyond hardened scope;
- merge or publish.

## Mandatory STOP conditions

STOP and return for renewed architecture approval if:

- the established derived-metric contract cannot represent laboratory-specific ULNs or contemporaneous pairing;
- the collision model cannot represent the required ALT/ALP/GGT precedence without a contract change;
- implementation requires files explicitly prohibited by the hardened prompt;
- a package requires medical interpretation not present in canonical Pass 3;
- activating a frame would create duplicate or contradictory runtime authority;
- legacy S24 disposition cannot be made safely from existing evidence;
- any non-ALT runtime package or frame changes unexpectedly;
- a broad estate migration is required;
- validator or gate failure cannot be attributed cleanly.

Do not use a retrospective lifecycle exception in place of the required STOP-and-return path.

## Completion boundary

STOP after:

- the governed R-value metric is implemented and validated;
- collision governance is implemented and validated;
- explicit promotion/activation decisions are applied only to eligible packages;
- runtime reachability and non-regression are proven;
- evidence is committed;
- Automation Bus kernel finish completes.

Do not merge. Return for independent Claude Code audit, GPT architectural review and Anthony’s final merge authority.
