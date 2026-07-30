# ARCH-CONV-C — STOP C runtime proof

**Work ID:** `ARCH-CONV-C`  
**Branch:** `feature/arch-conv-c-alp-ggt-why-authority`  
**Status:** `AWAITING_INDEPENDENT_HEAD_OF_ARCHITECTURE_STOP_C`  
**Gate 1 reference:** `ARCH-CONV-C-GATE1-HMR-2026-07-30`  
**Gate 2 reference:** `ARCH-CONV-C-GATE2-ANTHONY-2026-07-30`  
**Governance commit:** `37f6aed`  
**Phase 2 implementation commit:** `3dcfd39`

This document is implementation evidence for independent STOP C. It is not a
self-certification or approval.

## Implemented authority

### Canonical ALP

- Activation key: `signal_alp_high::inv_alp_high_bone_biliary`
- Compiled artefact:
  `knowledge_bus/compiled/hypotheses/inv_alp_high_bone_biliary.yaml`
- Manifest:
  `knowledge_bus/compiled/manifests/arch_conv_c_alp_high.yaml`
- Base role: `causal`
- Conditional policy: `cholestatic_source_axis_v1`
- High ALP plus high GGT: one ALP
  `CAUSAL_CANDIDATE_CONDITIONAL_CHOLESTATIC_PATTERN` finding.
- High ALP plus normal or unavailable GGT: the same canonical frame fails
  closed to `morphology_context`; no hepatobiliary causal WHY is emitted.
- The compiled text preserves bone and other non-hepatic possibilities and
  does not assert a specific liver or bone disorder.

### Canonical GGT

- Activation key: `signal_ggt_high::inv_ggt_high_hepatic`
- Compiled artefact:
  `knowledge_bus/compiled/hypotheses/inv_ggt_high_hepatic.yaml`
- Manifest:
  `knowledge_bus/compiled/manifests/arch_conv_c_ggt_high.yaml`
- Role: `morphology_context` (`CONTEXT_ONLY_NON_CAUSAL`).
- High GGT with normal or unavailable ALP emits non-specific context only.
- High ALP plus high GGT consolidates GGT under the ALP primary finding; GGT
  does not appear as a parallel causal finding.
- Alcohol, medicine-induction, metabolic-disease and severity attribution
  remain prohibited without separately governed structured authority.

## Named collision policy

`knowledge_bus/governance/signal_authority_collision_model_v1.yaml` now
adjudicates `liver_injury_axis` as the named `cholestatic_source_axis`:

- runtime policy: `cholestatic_source_axis_v1`;
- primary family/key: canonical ALP;
- supporting family/key: canonical GGT;
- duplicate user-facing signal: prohibited;
- supporting GGT is suppressed when canonical ALP is present;
- consolidation is enabled;
- parallel distinct-risk-layer fallback is disabled;
- candidate selection is by explicit activation key, never filename,
  directory order, package order or load order.

The collision resolver validates the declared activation keys against their
signal families and filters non-ratified ALP/GGT frame identities before
primary/supporting resolution. Reverse-input testing produces identical
output.

## Concordance matrix proved

- ALP high, GGT high: canonical ALP only; `causal`.
- ALP high, GGT normal: canonical ALP only; `morphology_context`.
- ALP high, GGT unavailable: canonical ALP only; `morphology_context`.
- GGT high, ALP normal: canonical GGT only; `morphology_context`.
- GGT high, ALP unavailable: canonical GGT only; `morphology_context`.

## Deferred Pass 3 candidates

The four ratified deferred frames have `authority_state: LEGACY_RETIRED`,
`artefact_path: null`, and no independent compile or promotion:

- `signal_alp_high::inv_alp_high_cholestatic_pattern`
- `signal_alp_high::inv_alp_high_high_bone_turnover_pattern`
- `signal_ggt_high::inv_ggt_high_hepatobiliary_cholestatic_context`
- `signal_ggt_high::inv_ggt_high_alcohol_or_enzyme_induction_context`

Focused tests prove that direct rows for these activation keys emit neither a
root-cause finding nor WHY-engine fallback. The named collision policy also
prevents them from becoming user-facing ALP/GGT authority.

## Fail-closed and role propagation proof

- All `COMPILED_ACTIVE` rows require an explicit supported `why_role`.
- Conditional role metadata requires a non-empty policy, non-empty governed
  marker gates, a causal base role and a supported fallback role.
- Missing, blank, malformed or unsupported conditional role metadata raises
  `ValueError`; no causal default is available.
- The role survives root-cause compilation, clinician-report compilation and
  JSON serialisation.
- No frontend file was changed. Consumers receive structured `why_role` data
  and require no frontend medical inference.

## Provenance and deterministic compilation

The manifests record:

- canonical source path and SHA-256;
- compiled output path and SHA-256;
- compiler name/version;
- activation key;
- source spec ID;
- validator status.

Recorded canonical source hashes:

- ALP:
  `1a8e2da95d4aeae0505897da445709632f5ea4c39c34d4aaf906ef3462eb61ef`
- GGT:
  `3e2cc6cf074dcb73b825e9a97fe93b43c4f50dc874a0c85cbaa34b754d46c8a1`

Recorded compiled output hashes:

- ALP:
  `387c4e5170cd34ae3bbb65b9cfd9a05eb2917698d262edaa8c38ab4e675db6d7`
- GGT:
  `55c7beaff048ecf849d389f9e9aee3a5dc8f3b72ede45ef4b5eddee8bdf2af16`

Runtime loads the compiled artefacts through
`compiled_why_authority_register_v1.yaml`; it does not read raw investigation
specs to emit WHY.

## Legacy authority disposition

The canonical activation keys now resolve to compiled authority. The legacy
files remain physically present and unmodified:

- `knowledge_bus/root_cause/hypotheses/alp_high_hypotheses_v1.yaml`
- `knowledge_bus/root_cause/hypotheses/ggt_high_hypotheses_v1.yaml`

No physical deletion occurred. The branch-level runtime disconnection is the
candidate replacement under independent STOP C; merge and Automation Bus
finish remain prohibited until that approval.

## Explicit exclusions

The ratified register's six exclusions were compared semantically with the
pre-Gate-2 register and are unchanged:

- `signal_alt_high`
- `signal_hepatic_alt_context`
- `signal_ast_high`
- `signal_bilirubin_high`
- `signal_hyperbilirubinemia`
- `signal_alp_low`

No compiled WHY row was added for any excluded family. The liver card retains
ALT and AST as score contributors, ALP and GGT as confidence contributors, and
bilirubin as contextual only. No frontend, scoring or card artefact changed.

## Test evidence

Passing evidence:

- `python backend/scripts/validate_compiled_why_authority_gate.py`
  - PASS: 37 governed frames, 21 compiled active, 1 rejected, 15 legacy retired.
- `python -m pytest backend/tests/regression/test_arch_conv_c_alp_ggt_stop_c.py -q`
  - PASS: 20 tests.
- Combined current/prior authority suites:
  - PASS: 57 tests across ARCH-CONV-B, ARCH-CONV-C, collision enforcement and
    compiled-WHY authority.
- Estate sentinel plus ARCH-CONV-C:
  - PASS: 27 tests after refreshing the governed compiled-estate count to 21.
- Default golden panel:
  - completed twice;
  - semantic output is identical after removing only generated IDs,
    timestamps and their derived hash;
  - burden, signal, WHY, report and non-volatile output content are identical.
- Focused tests prove source/output hashes, role serialisation, all five
  concordance states, deferred-frame non-reachability, input-order
  independence, prohibited wording and repeat-run determinism.

## Baseline suite disposition

The full backend suite reached 100% and reported 62 failures. The repository
already has broad unrelated baseline failures spanning missing database
services, alias/SSOT inventory, stale snapshots, legacy DTO fixtures and
unrelated governance counts. No failure occurred in
`test_arch_conv_c_alp_ggt_stop_c.py`.

Three directly observed baseline examples were preserved rather than changed:

1. VR expected clinician-report mismatch. This was already recorded and
   accepted as a pre-existing baseline discrepancy in ARCH-CONV-B. The VR
   panel has normal ALP (38) and GGT (13), and ARCH-CONV-C changed neither the
   VR input nor expected report fixture.
2. `test_kbs23_catalogue_panel_harness_runs_all_panel_fixtures` fails because
   an existing catalogue fixture lacks the golden runner's required `user`
   object.
3. The total-cholesterol root-cause test supplies a blank activation key to an
   already multi-frame governed family and fails closed before any
   ARCH-CONV-C role code executes.

The full-suite run also exposed a stale estate-index expected count (17 versus
the post-ARCH-CONV-B/C total of 21). That directly relevant sentinel was
updated and passes. No unrelated snapshot, fixture, clinical output, alias,
SSOT, scoring or frontend failure was rewritten or accepted in this work
package.

## Independent STOP C checklist

The independent reviewer must verify:

1. Canonical ALP and GGT compiled artefacts and manifest hashes.
2. Conditional ALP causal/context role behavior in all concordance states.
3. GGT remains non-causal and is consolidated under concordant ALP.
4. Deferred Pass 3 activation keys are unreachable as WHY/user-facing
   authority.
5. Missing or unsupported role metadata fails closed.
6. Selection is activation-key explicit and input-order deterministic.
7. Legacy files remain present while canonical frame runtime authority is
   replaced.
8. ALT, AST, bilirubin/hyperbilirubinemia, ALP-low, scoring/card and unrelated
   domains remain outside the change.
9. Baseline failures above are not reclassified as ARCH-CONV-C regressions
   without contrary evidence.

## STOP C verdict

`AWAITING INDEPENDENT HEAD OF ARCHITECTURE STOP C APPROVAL`

Automation Bus finish has not been run.
