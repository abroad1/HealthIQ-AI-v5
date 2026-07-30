---
work_id: ARCH-CONV-E
branch: feature/arch-conv-e-alt-why-authority
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# ARCH-CONV-E — Build ALT Knowledge Bus Assets from Validated Pass 3 Research

Execute under:

- `AUTOMATION_BUS_SOP_v1.3.1.md`
- `KNOWLEDGE_BUS_SOP_v1.3.1.md`
- `KNOWLEDGE_BUS_PASS3_PROMOTION_PROTOCOL_v1.1.md`

This is a continuation of the existing active `ARCH-CONV-E` work package. Do not create a second work package or branch.

## Canonical source

Use only:

`knowledge_bus/research/investigation_specs/multi_llm_research/ALT_High_Hepatic_Pattern_Classification_ARCH_CONV_E_Pass_3.json`

SHA-256:

`7F20BF9A06B3427217AD7F753C4D9304E5D5A2C46C484699257778844B9D3267`

The six validated source specs are:

1. `inv_alt_high_r_value_hepatocellular_biochemical_pattern`
2. `inv_alt_high_r_value_mixed_biochemical_pattern`
3. `inv_alt_high_r_value_cholestatic_alp_predominant_context`
4. `inv_alt_high_muscle_source_or_exertional_contribution`
5. `inv_alt_high_bilirubin_hys_law_severity_context`
6. `inv_alt_high_metabolic_masld_context`

All six pass `validate_investigation_spec.py` individually. Do not modify or reinterpret the Pass 3 source.

## Objective

Create the normal Knowledge Bus signal packages required by the existing one-package-per-sub-pattern convention.

Do not collapse medically distinct sub-patterns into one package.

## Required package set

### Regenerate these three existing sibling packages from the new canonical Pass 3 source

1. `knowledge_bus/packages/pkg_kb52c_alt_high_hepatocellular_injury_pattern`
   - source spec: `inv_alt_high_r_value_hepatocellular_biochemical_pattern`
   - disposition of prior Batch 5 lineage: `REGENERATED_FROM_CANONICAL_RESEARCH`

2. `knowledge_bus/packages/pkg_kb52c_alt_high_muscle_source_or_exertional_pattern`
   - source spec: `inv_alt_high_muscle_source_or_exertional_contribution`
   - disposition of prior Batch 5 lineage: `REGENERATED_FROM_CANONICAL_RESEARCH`

3. `knowledge_bus/packages/pkg_kb52c_alt_high_metabolic_steatotic_liver_pattern`
   - source spec: `inv_alt_high_metabolic_masld_context`
   - disposition of prior Batch 5 lineage: `REGENERATED_FROM_CANONICAL_RESEARCH`

Preserve the established package IDs and directories unless a locked repository rule proves that a versioned replacement directory is mandatory. Do not silently rename them.

### Create these three new sibling packages

4. `knowledge_bus/packages/pkg_kb52c_alt_high_mixed_biochemical_pattern`
   - source spec: `inv_alt_high_r_value_mixed_biochemical_pattern`

5. `knowledge_bus/packages/pkg_kb52c_alt_high_cholestatic_alp_predominant_context`
   - source spec: `inv_alt_high_r_value_cholestatic_alp_predominant_context`

6. `knowledge_bus/packages/pkg_kb52c_alt_high_bilirubin_severity_context`
   - source spec: `inv_alt_high_bilirubin_hys_law_severity_context`

If an exact repository naming rule requires a different slug, apply that rule consistently and report the final path. Do not change the medical grouping.

## Mandatory assets for every package

Create or update:

- `research_brief.yaml`
- `signal_library.yaml`
- `package_manifest.yaml`

Use the established schema and nearest valid sibling packages as structural templates only. Medical content must come from the assigned Pass 3 spec.

### `research_brief.yaml`

Include the assigned source spec’s:

- primary and supporting biomarkers;
- derived metrics;
- physiological claim;
- hypotheses and evidence strength where supported by the current contract;
- source references and limitations;
- contradiction, exclusion, severity and missing-data context;
- non-diagnostic boundaries.

Do not blend content from another source spec merely because all packages use `signal_alt_high`.

### `signal_library.yaml`

Represent only the activation architecture supported by the assigned source spec and current schema:

- `signal_id: signal_alt_high`;
- direction and lab-range activation;
- dependencies;
- supporting, contradiction, exclusion and severity markers;
- override/escalation conditions;
- fail-closed missing-data behaviour;
- collision/dependency metadata supported by the existing contract.

### `package_manifest.yaml`

Use the established package manifest schema and include the maximum protocol lineage metadata the locked contract supports.

Required lineage record, either directly in the manifest or in the repository’s established equivalent evidence location:

- `source_spec_id`;
- `source_path`;
- `source_hash`;
- `compiler_version: manual-promotion-v1` or the established manual marker;
- `output_artifacts`;
- `output_hashes` after files are final;
- `validation_result`;
- `promoted_utc: null` because this step does not promote;
- `promotion_mode: PACKAGE_MANUAL` or the existing allowed equivalent.

Do not add invalid manifest fields. If the locked schema cannot carry one of these fields, record it in the normal ARCH-CONV-E evidence report with the package path and output hashes.

## Optional assets

Create or update only where the package opts in and the locked contract requires them:

- `intelligence_model.yaml`
- `promoted_signal_intelligence.yaml`

Use `intelligence_model.yaml` where needed to preserve hypotheses, ranking, contradiction logic or confirmatory-test relationships not representable in mandatory assets.

Use `promoted_signal_intelligence.yaml` only according to its locked signal-only contract.

Do not create optional assets merely for symmetry.

## R-value-dependent package disposition

The following three packages depend on `r_value_alt_alp` for functional differentiation:

- hepatocellular biochemical pattern;
- mixed biochemical pattern;
- cholestatic/ALP-predominant context.

The governed compute path for `r_value_alt_alp` does not yet exist. Therefore:

1. Build and validate the Knowledge Bus assets from the canonical Pass 3 source.
2. Record the derived-metric contract exactly as supported by the package schemas:
   - formula intent: `(ALT / ALT ULN) / (ALP / ALP ULN)`;
   - ALT result and laboratory ULN required;
   - ALP result and laboratory ULN required;
   - contemporaneous/same-sample pairing required;
   - fail closed if any input is absent;
   - `R >= 5`, `2 < R < 5`, and `R <= 2` classifications.
3. Mark each of these three packages `DEFERRED_WITH_EXPLICIT_REASON` for runtime readiness/promotion because the governed derived-metric compute authority is absent.
4. Do not mark them `ready_for_implementation: true`.
5. Do not add `r_value_alt_alp` to `ratio_registry.py` or any runtime/SSOT registry in this asset-build step.

The muscle, bilirubin-severity and metabolic packages are not automatically deferred for this reason. Determine their package readiness from their own validator results and dependencies only.

## Existing authority reconciliation

Reconcile and report:

- legacy `pkg_s24_alt_high_hepatocellular_injury` lineage;
- prior Batch 5 kb52c ALT sibling packages;
- the six ARCH-CONV-E source specs;
- existing ALP/GGT `liver_injury_axis` authority;
- `knowledge_bus/governance/signal_authority_collision_model_v1.yaml`.

Required rules:

- do not treat adjacent `spec_id` values as identical lineage;
- do not retire or activate runtime authority in this step;
- record proposed legacy dispositions using only:
  - `MAPPED_TO_CANONICAL_RESEARCH`
  - `REGENERATED_FROM_CANONICAL_RESEARCH`
  - `ACCEPTED_WITH_RATIONALE`
  - `RETIRED`
  - `DEFERRED_WITH_EXPLICIT_REASON`
- do not edit the collision model in this step;
- record the required future collision-policy dependency for ALT R-value packages versus the existing ALP/GGT axis.

## Validation and tests

For each of the six package directories:

1. Parse all YAML assets.
2. Run:

`python backend/scripts/validate_knowledge_package.py --package-dir <package-path>`

3. Run the existing package/content tests used by comparable kb52c packages, including any repository tests that load and verify:
   - activation dependencies;
   - override-condition preservation;
   - fail-closed missing-data fields;
   - optional intelligence contracts.

4. If no existing executable test covers package loading for these fields, add the minimum scoped content-contract test following the existing Knowledge Bus test pattern. Do not add runtime medical behaviour.

5. For each R-value-dependent package, prove that package readiness remains deferred and cannot be mistaken for runtime-ready while `r_value_alt_alp` compute authority is absent.

Validator authority remains final. Do not alter validator output.

## Evidence to publish

Publish one bounded ARCH-CONV-E asset-build report containing:

1. all six package paths;
2. files created or modified per package;
3. source path, source SHA-256 and assigned `source_spec_id` per package;
4. package-level mapping from source fields to generated assets;
5. output hashes;
6. validation results per package;
7. test commands and results;
8. reconciliation table for legacy S24, Batch 5 and ARCH-CONV-E lineages;
9. readiness/disposition per package;
10. explicit `DEFERRED_WITH_EXPLICIT_REASON` evidence for the three R-value-dependent packages;
11. future dependency statement for the governed `r_value_alt_alp` compute asset and ALT/ALP/GGT collision policy;
12. `git diff --name-only` and scoped diff summary.

## Prohibitions

Do not:

- modify the Pass 3 source;
- create a new research or ingestion process;
- require or build a universal Pass 3 compiler;
- collapse the six sub-patterns into one package;
- invent additional medical claims, thresholds or wording;
- create a new signal identity;
- modify executable analytics, runtime, SSOT or frontend code;
- add `r_value_alt_alp` to runtime registries;
- edit `signal_authority_collision_model_v1.yaml`;
- promote by updating `latest_knowledge_status.json`;
- activate WHY output;
- retire legacy runtime authority;
- merge or publish.

## STOP gate

STOP after:

- all six package asset sets are created or updated;
- each package has a validator result;
- scoped content-contract tests complete;
- package dispositions and reconciliation evidence are published.

If a locked schema prevents faithful representation of a required canonical field, STOP with the exact package, asset path, schema path and validator error. Do not invent a replacement contract.
