# ARCH-CONV-E — ALT Knowledge Bus Package Asset-Build Report

## Scope and activation status

This report records the bounded ARCH-CONV-E package build from validated Pass 3 research,
and the governed runtime eligibility boundary fix that keeps that build inert. Six
one-package-per-sub-pattern asset sets were created or regenerated. No ratio registry,
SSOT registry, compiled card, DTO, frontend, `latest_knowledge_status.json`, or
collision-policy file was changed. None of the six packages was promoted or activated.

## Resolved — runtime eligibility boundary (supersedes the recorded STOP)

The build initially triggered a STOP because package placement alone was runtime-reachable:

- `backend/core/analytics/signal_evaluator.py` scans every
  `knowledge_bus/packages/*/signal_library.yaml`;
- `backend/core/knowledge/package_runtime_eligibility_v1.py` classified every package
  outside the `pkg_kb47_*` launch-critical cohort as `ELIGIBILITY_OUT_OF_COHORT`;
- `is_production_reachable()` treated `ELIGIBILITY_OUT_OF_COHORT` as reachable, so all six
  non-promoted ARCH-CONV-E ALT frames loaded into the live registry;
- the focused registry check reported seven `signal_alt_high` frames against an expected
  four.

Under the architecture decision recorded for this work package, that boundary was fixed in
scope. Placement under `knowledge_bus/packages/` is now a promotion act only. Runtime
activation of a non-launch-critical frame requires an explicit entry in a governed
activation register keyed by `activation_key` (`signal_id::source_spec_id`, ADR-RT-002).

Implemented semantics:

| Eligibility | Loads in production | Contract |
|---|---|---|
| `ELIGIBILITY_PRODUCTION_REACHABLE` | Yes | `pkg_kb47_*` with beta-eligible explicit lineage, or a non-launch-critical package with at least one registered activation key |
| `ELIGIBILITY_OUT_OF_COHORT` | No | Non-launch-critical and not present in the activation register |
| `ELIGIBILITY_TEST_ONLY_OPT_IN` | Only under the existing launch-critical opt-in | Unchanged `allow_launch_critical_blocked` / `HEALTHIQ_ALLOW_LAUNCH_CRITICAL_BLOCKED` contract |
| `ELIGIBILITY_NON_REACHABLE` | No | Unchanged launch-critical fail-closed path |

Boundary properties:

- the launch-critical cohort keeps its existing lineage-based contract and its existing
  14-package exclusion audit surface; the register deliberately does not cover it;
- the launch-critical test opt-in does not activate unregistered non-launch-critical
  packages, so it cannot be used to reach the six;
- the ratified `REJECTED` frame authority keeps precedence over the activation gate, so
  `signal_homocysteine_high::inv_homocysteine_high_metabolic` is still recorded as
  `REJECTED_NOT_RUNTIME_ELIGIBLE` rather than merely unactivated;
- the register describes the governed estate only. Signal libraries supplied from outside
  `knowledge_bus/packages/` (harness fixtures) retain pre-fix behaviour via an explicit
  `enforce_activation_register=False` argument, which production never sets;
- a missing, malformed, or count-inconsistent register raises rather than admitting every
  package on disk.

### Affected runtime files

| File | Change |
|---|---|
| `knowledge_bus/governance/package_runtime_activation_register_v1.yaml` | New governed register: 173 activated frames, plus the six withheld ARCH-CONV-E frames recorded with their reason |
| `backend/core/knowledge/package_activation_register_v1.py` | New fail-closed register loader and activation predicates |
| `backend/core/knowledge/package_runtime_eligibility_v1.py` | `ELIGIBILITY_OUT_OF_COHORT` removed from `is_production_reachable()`; non-launch-critical classification now register-driven |
| `backend/core/analytics/signal_evaluator.py` | Per-frame activation gate; new `excluded_unactivated_packages` / `excluded_unactivated_frames` audit surfaces; rejection authority evaluated first |

The register was derived as a baseline-parity snapshot of the non-launch-critical frames
that `SignalRegistry` loaded immediately before the fix, minus every frame contributed by
the six ARCH-CONV-E packages. No currently active frame outside the ARCH-CONV-E scope
changed state.

### Before/after registry evidence

| Registry state | Total frames | Loaded packages | `signal_alt_high` frames |
|---|---|---|---|
| Clean `HEAD` (4d09048), pre-ARCH-CONV-E | 182 | 176 | 4 |
| Asset build applied, pre-boundary fix | 185 | 179 | 7 |
| Asset build plus boundary fix | 179 | 173 | 1 |

The single remaining ALT frame is
`signal_alt_high::inv_alt_high_hepatocellular_injury` from
`pkg_s24_alt_high_hepatocellular_injury`, the only explicitly activated ALT frame.

The `HEAD`-to-final delta of three frames is intentional and is the substantive runtime
consequence of this work package. The three regenerated `pkg_kb52c_*` ALT packages were
loading at `HEAD` under their superseded spec IDs while their estate rows recorded
`requires_review: true` and `runtime_loaded: false`. Regeneration replaced their lineage,
so their activation keys changed, and neither the old nor the new keys are promoted. They
are therefore withheld with the three new packages. Restoring any of them to production is
a promotion decision, made by appending the activation key to the register.

`SignalRegistry` audit surfaces after the fix:

- `excluded_launch_critical_packages`: 14 (unchanged);
- `excluded_unactivated_packages`: the six ARCH-CONV-E packages plus
  `pkg_s24_homocysteine_high_metabolic`, whose only frame is separately ratified `REJECTED`;
- `excluded_unactivated_frames`: exactly the six ARCH-CONV-E activation keys, each recorded
  `NOT_RUNTIME_ACTIVATED`;
- `excluded_rejected_frames`: `signal_homocysteine_high::inv_homocysteine_high_metabolic`
  (unchanged).

Canonical source:

- Path: `knowledge_bus/research/investigation_specs/multi_llm_research/ALT_High_Hepatic_Pattern_Classification_ARCH_CONV_E_Pass_3.json`
- SHA-256: `7F20BF9A06B3427217AD7F753C4D9304E5D5A2C46C484699257778844B9D3267`
- Investigation-spec contract: `3.0.0`
- Promotion marker: `manual-promotion-v1`
- Promotion mode: `PACKAGE_MANUAL`
- `promoted_utc`: `null`

Supporting research provenance retained with ARCH-CONV-E:

- Pass 1: `knowledge_bus/research/investigation_specs/multi_llm_research/ALT_High_Hepatic_Pattern_Classification_ARCH_CONV_E_Pass_1.json`
  (`057F13627A29DC5ED18CB5C56E80E440A05BA41406677E5D31F05D2D07C19F9E`)
- Pass 2: `knowledge_bus/research/investigation_specs/multi_llm_research/ALT_High_Hepatic_Pattern_Classification_ARCH_CONV_E_Pass_2.json`
  (`1A2285B3B36C379DF58C0E191CB8C119F52DCB71C5C1BFD9FD9D850C8D67960C`)

Pass 1 and Pass 2 are supporting provenance only. They are not package, promotion, or
runtime authority. Every package manifest and promoted signal-intelligence translation
continues to identify Pass 3 as the sole canonical promotion source.

## Package set and source assignment

| Package | Assigned source spec | Files | Disposition / readiness |
|---|---|---|---|
| `pkg_kb52c_alt_high_hepatocellular_injury_pattern` | `inv_alt_high_r_value_hepatocellular_biochemical_pattern` | `research_brief.yaml`, `signal_library.yaml`, `package_manifest.yaml`, `promoted_signal_intelligence.yaml` regenerated | `REGENERATED_FROM_CANONICAL_RESEARCH`; `DEFERRED_WITH_EXPLICIT_REASON` |
| `pkg_kb52c_alt_high_muscle_source_or_exertional_pattern` | `inv_alt_high_muscle_source_or_exertional_contribution` | same four assets regenerated | `REGENERATED_FROM_CANONICAL_RESEARCH`; validator PASS; not promoted |
| `pkg_kb52c_alt_high_metabolic_steatotic_liver_pattern` | `inv_alt_high_metabolic_masld_context` | same four assets regenerated | `REGENERATED_FROM_CANONICAL_RESEARCH`; validator PASS; not promoted |
| `pkg_kb52c_alt_high_mixed_biochemical_pattern` | `inv_alt_high_r_value_mixed_biochemical_pattern` | same four assets created | `DEFERRED_WITH_EXPLICIT_REASON` |
| `pkg_kb52c_alt_high_cholestatic_alp_predominant_context` | `inv_alt_high_r_value_cholestatic_alp_predominant_context` | same four assets created | `DEFERRED_WITH_EXPLICIT_REASON` |
| `pkg_kb52c_alt_high_bilirubin_severity_context` | `inv_alt_high_bilirubin_hys_law_severity_context` | same four assets created | validator PASS; not promoted |

The three R-value package manifests explicitly state that they are not runtime-promoted.
The package validator's `ready_for_implementation: True` output means only that the package
is structurally valid under current package contracts; it is not treated here as runtime
promotion authority.

## Source-field mapping

The same deterministic mapping was applied independently to each assigned spec:

- `research_domain`, evidence sources, registered biomarkers, derived metrics,
  `evidence.physiological_claim`, `evidence.evidence_strength`, hypotheses, caveats,
  limitations, contradiction context, and missing-data boundaries → `research_brief.yaml`.
- `signal_id`, primary marker, trigger direction, lab-range activation, dependencies,
  source-supported overrides, output marker order, and narrative → `signal_library.yaml`.
- Full signal-layer primary/supporting markers, relationship kinds, contradiction markers,
  missing-data policies, overrides, evidence, and confirmatory tests →
  `promoted_signal_intelligence.yaml`.
- Package identity, source spec ID, activation key, source path/hash, behavioural impact,
  and non-activation/deferral wording → `package_manifest.yaml`.

The signal-library v2 contract does not accept `expected_direction: either` or
`role: exclusion_marker`; those values are reduced to `any` and `differential_marker`
respectively in `signal_library.yaml`. The full source values remain unchanged in
`promoted_signal_intelligence.yaml`.

The current SSOT biomarker registry does not contain source marker IDs `inr` or `hdl`.
They are therefore omitted only from the registry-validated `research_brief.biomarkers`
list and explicitly identified in its summary; their canonical signal context remains
preserved in the signal-layer assets. No SSOT registry entry was invented.

The mixed-pattern override cites `source_fda_dili_guidance_2009` but its local evidence
array omits the citation object. The citation details were resolved from the same canonical
Pass 3 source file, where that source object is present, so the override's governed
`source_refs` remains resolvable without introducing an external source.

## R-value derived-metric contract

The hepatocellular, mixed, and cholestatic/ALP-predominant package briefs record:

- formula intent: `(ALT / ALT ULN) / (ALP / ALP ULN)`;
- ALT result and laboratory ULN required;
- ALP result and laboratory ULN required;
- contemporaneous same-sample pairing required;
- fail closed if any input is absent;
- classifications: `R >= 5`, `2 < R < 5`, and `R <= 2`.

Their signal libraries declare `r_value_alt_alp` as a derived dependency. The governed
compute asset is absent from `backend/core/analytics/ratio_registry.py`, so all three
remain `DEFERRED_WITH_EXPLICIT_REASON`. This work did not add a compute implementation.

## Output hashes

### `pkg_kb52c_alt_high_hepatocellular_injury_pattern`

- `package_manifest.yaml`: `4D0A43FDF7B5359F996F8940725D4C1EAA856E7B0B281689E750B1D63EC773CF`
- `promoted_signal_intelligence.yaml`: `D04A6C8E6463632238C0F84652C6323875A18CE13A000068099B8B701209292C`
- `research_brief.yaml`: `BB455036443CAC440D90470F8C9BD6E876599913C244EFBC8EA580127CD438CE`
- `signal_library.yaml`: `74FA5B389E55AEDB8C16FCE0F00A0B7880F2FC84E8691623DC451C23CC796315`

### `pkg_kb52c_alt_high_muscle_source_or_exertional_pattern`

- `package_manifest.yaml`: `509D7D878FE32DF8D64A46D31A050A5431BEEA02E1B1465233C9FEA0ADD714D6`
- `promoted_signal_intelligence.yaml`: `4C4500DE60150EFF427A7C4CF172228F75A8BFEB180ECC4B154095DAF77A4ED1`
- `research_brief.yaml`: `762634525F3C28CD3055FE2049D4CF5B7C6B2F52E05BA7F9703A789DD5E730CB`
- `signal_library.yaml`: `532E60F4B3ABB69E145BA2F385AFF140167C49E4D37122F204F35D5F622318E4`

### `pkg_kb52c_alt_high_metabolic_steatotic_liver_pattern`

- `package_manifest.yaml`: `BF78B7A107882A1B02465CE414345015D6A2954047464C5AAF0FAEA05E2E4C27`
- `promoted_signal_intelligence.yaml`: `3EE8730825E083805215CEBC7D9676D5D4A5887F3ABBD90A37934A1F0DD8E895`
- `research_brief.yaml`: `6B93AD1E828647167CB6358296305806E4B6390EFBDFFE467A8D2DC8AA27083B`
- `signal_library.yaml`: `0015459DAB0724CC9A31A525388BDA2EDABCCEF5D117A4E7B3D8E50B8221B031`

### `pkg_kb52c_alt_high_mixed_biochemical_pattern`

- `package_manifest.yaml`: `2EF39C260ED26E7310B0882910743E521281959B4DF2299266A7AFED65F377AB`
- `promoted_signal_intelligence.yaml`: `1B4898CE93744A5982156ACCBE198CD14D50B2A9C73E1D85C2F70A05B8093A70`
- `research_brief.yaml`: `ED70D1E7AAAD2047ED8CFF20FFA0609DD72511F2385A6DD9DCAEFBEACA0B3060`
- `signal_library.yaml`: `170FC11F2FC26BF4FD8D0241231AC292D1276C7B39E98F1BAD063E8FE1900FD8`

### `pkg_kb52c_alt_high_cholestatic_alp_predominant_context`

- `package_manifest.yaml`: `9C9CD10C06D2DC663309B5587FE823B249DDBC48D9125F740A889A6F0D3DB7ED`
- `promoted_signal_intelligence.yaml`: `FFFBD5E31614AEEAE773944EBC92F3C1B57844B0BAACA80947C69F65E9777700`
- `research_brief.yaml`: `96D247584DE7CE1E8A5E73F343B1D4B98FAAAF7E1B46EB29C81557C0AD093471`
- `signal_library.yaml`: `2FDB8FD678C2A1518AC053F4A59D7335863A436EE29A47DAB7234F607D77B93E`

### `pkg_kb52c_alt_high_bilirubin_severity_context`

- `package_manifest.yaml`: `BAAE60A2BE9A3E51865F8084ED72BDF6907666244316849D0BF3E4FE81F4A7C6`
- `promoted_signal_intelligence.yaml`: `846C06C881332A6AB703334A0AB7EF5DFACE93BA15924BF6D313D578F24C1CD2`
- `research_brief.yaml`: `F26FD3B65743582CBF1443369CBCC8686D4345289CC620D77948E946E881ACF4`
- `signal_library.yaml`: `8BE94AD13406F843A1BB8905A500CBA021F66E8B74FAF902E7A06B7BD1FBE249`

## Validation and tests

Commands and outcomes:

- YAML parse of all 24 package assets: PASS.
- `python backend/scripts/validate_knowledge_package.py --package-dir <package>`:
  PASS for each of the six packages (manifest, research brief, signal library, and
  promoted signal intelligence all PASS; intelligence model SKIP).
- Combined affected package, KB-S52C, estate, and collision tests:
  `python -m pytest backend/tests/unit/test_wave_a_inventory_kb_s52c.py backend/tests/unit/test_arch_conv_e_alt_package_assets.py backend/tests/regression/test_lc_s18a_package_estate_inventory.py backend/tests/regression/test_signal_authority_collision_enforcement.py -q`
  — PASS.
- `python backend/scripts/run_baseline_tests.py`: PASS (`38 passed`).
- `python backend/scripts/validate_launch_critical_provenance_reachability_gate.py`: PASS
  (`production_kb47=6 excluded=14 optin_kb47=20`).
- `python backend/scripts/validate_arch_conv_correct1_gate.py`: PASS.
- `python -m pytest backend/tests/unit/test_signal_evaluator.py -q`: the ARCH-CONV-E
  failure is cleared. Only the pre-existing catalogue-fixture failure remains.

### Boundary tests

`backend/tests/unit/test_arch_conv_e_runtime_activation_boundary.py` is new and proves:

| Requirement | Test |
|---|---|
| The six packages remain present with their mandatory assets | `test_six_alt_packages_remain_present_with_mandatory_assets` |
| The six still validate | `test_six_alt_packages_still_validate` (runs `validate_knowledge_package.py` per package) |
| They are absent from the production registry | `test_six_alt_packages_absent_from_production_registry` |
| Their withholding is auditable | `test_withheld_packages_and_frames_are_auditable` |
| Rejected-frame authority keeps precedence | `test_rejected_frame_authority_keeps_precedence_over_activation` |
| The pre-existing active ALT frame still loads | `test_pre_existing_active_alt_frame_still_loads` |
| Production-reachable packages still load | `test_production_reachable_packages_still_load`, `test_every_loaded_frame_is_explicitly_activated_or_launch_critical` |
| Test-only opt-in still works and cannot reach the six | `test_launch_critical_test_opt_in_still_loads_blocked_fixtures`, `test_launch_critical_opt_in_does_not_activate_withheld_packages` |
| `OUT_OF_COHORT` is not production-reachable | `test_out_of_cohort_is_not_production_reachable` |
| Placement does not imply activation | `test_placement_under_packages_root_does_not_imply_activation` |
| Register integrity and fail-closed loading | `test_register_withholds_the_six_and_declares_its_own_count`, `test_missing_register_fails_closed`, `test_malformed_register_fails_closed` |

Two existing tests were updated to the corrected boundary rather than to preserve the
defect:

- `backend/tests/unit/test_signal_evaluator.py::test_signal_registry_alt_high_multi_frame_pilot`
  previously asserted four ALT frames including three unpromoted `pkg_kb52c_*` frames. It
  now asserts the single activated ALT frame, and preserves the original ARCH-RT-2
  intent — frames must not collapse to one lexicographic winner — against the registry's
  47 remaining multi-frame families, including the three-frame `signal_ggt_high` family.
- `backend/tests/unit/test_arch_conv_pkg2_provenance_reachability.py::test_non_kb47_packages_unaffected`
  is renamed `test_non_kb47_packages_load_only_when_explicitly_activated`, because
  ARCH-CONV-E deliberately changes what PKG2 left untouched.

### Pre-existing estate debt, unchanged

`test_kbs23_catalogue_panel_harness_runs_all_panel_fixtures` fails with
`ValueError: Golden panel fixture must include biomarkers and user`
(`backend/tools/run_golden_panel.py:74`). The identical failure was reproduced on a clean
detached worktree at `HEAD` (4d09048), confirming it predates this work package. Its cause
is a malformed panel fixture, independent of signal activation. It was not altered and it
did not block any ARCH-CONV-E gate.

Package-count inventories directly affected by the three new package directories were
also reconciled (191 → 194) in:

- `backend/scripts/validate_day_one_architecture.py`
- `backend/tests/unit/test_arch_rt5d_package_provenance.py`

The six ARCH-CONV-E packages are classified `explicit_source_spec_id`. Stale bucket
expectations and the older “no package may declare `source_spec_id`” claim are recorded
as pre-existing estate debt where they already failed at `HEAD`; only the total count and
the six packages' explicit classification are asserted under ARCH-CONV-E.

The estate inventory was reconciled only for the six ARCH-CONV-E ALT packages:

- the three regenerated rows now record Pass 3 lineage and their PSI assets;
- the three new package rows were added as `WHY-enabled`, `requires_review: true`,
  `runtime_loaded: false`;
- inventory counts were updated from 185 to 188 governed packages and from 112 to 115
  review-queue packages;
- the KB-S52C test now distinguishes the original Wave A set, the three regenerated ALT
  packages, and three supplemental ALT packages.

The following five unregistered packages remain explicitly recorded as pre-existing estate
debt and are not attributed to ARCH-CONV-E:

- `pkg_kb52c_ferritin_high_inflammatory_hyperferritinemia`
- `pkg_kb52c_ferritin_high_iron_overload_context`
- `pkg_kb52c_iron_high_iron_overload_context`
- `pkg_kb52c_iron_low_absolute_iron_deficiency`
- `pkg_kb52c_iron_low_functional_iron_restriction_inflammation`

## Authority reconciliation

| Authority / lineage | Disposition | Rationale |
|---|---|---|
| `pkg_s24_alt_high_hepatocellular_injury` | `MAPPED_TO_CANONICAL_RESEARCH` | Legacy S24 remains unchanged and non-retired; its ALT-high territory maps to the canonical ARCH-CONV-E research set pending later authority adjudication. |
| Three prior Batch 5 ALT sibling packages | `REGENERATED_FROM_CANONICAL_RESEARCH` | Existing package IDs/directories were preserved while source lineage and content were replaced by their assigned ARCH-CONV-E specs. |
| Six ARCH-CONV-E Pass 3 specs | `ACCEPTED_WITH_RATIONALE` | Each validated spec maps one-to-one to a distinct package; no medical sub-pattern was collapsed. |
| Existing `liver_injury_axis` ALP/GGT authority | `ACCEPTED_WITH_RATIONALE` | Existing governed runtime authority remains unchanged and continues to own the ALP-primary/GGT-supporting cholestatic-source axis. |
| Three ALT R-value packages | `DEFERRED_WITH_EXPLICIT_REASON` | Governed `r_value_alt_alp` computation and collision-policy adjudication do not yet exist. |

No adjacent `spec_id` was treated as identical lineage. No legacy authority was retired,
and no package was runtime-activated.

## Future dependencies

Before any R-value package can be considered for runtime promotion:

1. a governed `r_value_alt_alp` compute asset must implement the recorded formula,
   required ULN inputs, contemporaneous pairing, classifications, and fail-closed policy;
2. the ALT R-value package family must be adjudicated against
   `knowledge_bus/governance/signal_authority_collision_model_v1.yaml`'s existing
   `liver_injury_axis`, where `signal_alp_high` is primary and `signal_ggt_high` is
   supporting;
3. that future work must decide consolidation/suppression without editing this asset
   build into runtime authority.

## Scoped diff summary

In-scope implementation consists of:

- 12 regenerated files across three existing ALT packages;
- 12 created files across three new ALT packages;
- the governed runtime activation register and its fail-closed loader;
- the eligibility and `SignalRegistry` boundary change with its new audit surfaces;
- one scoped content-contract test and one boundary test module;
- two existing runtime tests updated to the corrected boundary;
- directly affected KB-S52C and package-estate inventory/test reconciliation;
- Pass 1 and Pass 2 supporting-provenance files, with Pass 3 retained as sole authority;
- this evidence report.

## Recommendations recorded, not implemented

1. The estate inventory marks 115 review-queue packages `runtime_loaded: false`, yet 109 of
   them are in the activation register because they were loading before this fix. Honouring
   the inventory instead would have deactivated 109 packages, far outside ARCH-CONV-E, so
   baseline parity was chosen. Reconciling the register against the estate review queue
   needs its own work package.
2. `pkg_s24_homocysteine_high_metabolic` now appears in `excluded_unactivated_packages` as
   well as contributing the ratified `REJECTED` frame. A future cleanup could retire the
   package rather than leaving it inert on two surfaces.
3. The five unregistered `pkg_kb52c_*` ferritin/iron packages listed above remain estate
   debt and are absent from both the inventory and the activation register.

The modified Automation Bus prompt/hardening predate Stage 4 implementation and remain
governed handoff artefacts for this same work ID. Pass 3 is the canonical upstream
promotion authority required by this work package.
