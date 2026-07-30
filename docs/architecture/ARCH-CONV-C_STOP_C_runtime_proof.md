# ARCH-CONV-C — STOP C runtime proof

**Work ID:** `ARCH-CONV-C`  
**Branch:** `feature/arch-conv-c-alp-ggt-why-authority`  
**Date (UTC):** 2026-07-30  
**Author role:** Cursor (`healthiq-core-engine`) — implementation evidence only  
**Status:** `STOP_C_APPROVED_BY_HEAD_OF_ARCHITECTURE`  
**Baseline comparison:** `COMPLETE — zero new ARCH-CONV-C-attributable failures`  
**Automation Bus finish:** completed under this approval (`ab02377` kernel COMPLETE)  
**Gate 1 reference:** `ARCH-CONV-C-GATE1-HMR-2026-07-30`  
**Gate 2 reference:** `ARCH-CONV-C-GATE2-ANTHONY-2026-07-30`  
**Governance commit:** `37f6aed`  
**Phase 2 implementation commit:** `3dcfd39`  
**Baseline comparison commit:** `ab2ace2`  
**Baseline compared:** `cdc6cf3d463d50902a080b51136ef1a98b431f4a`

This document is a review submission, not self-certification. Independent STOP C
was required before Automation Bus finish, merge, or any claim of completion.

> **Independent STOP C approval (recorded 2026-07-30):** Head of Architecture
> approved independent STOP C after the baseline comparison confirmed zero new
> ARCH-CONV-C-attributable failures. Remaining suite failures are the documented
> baseline/environmental set only. Approval authorises Automation Bus finish;
> merge remains prohibited without separate human authority.

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
candidate replacement under independent STOP C. Merge remains prohibited
without separate human authority.

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

The full backend suite reached 100% and initially reported 62 failures on the
pre-commit working tree (including a stale estate-index expected count of 17).
After the intentional estate sentinel update to 21, the committed HEAD
re-run reports **61 FAILED / 0 ERROR**. No failure occurred in
`test_arch_conv_c_alp_ggt_stop_c.py`.

Three directly observed long-standing examples remain unchanged rather than
rewritten:

1. VR expected clinician-report mismatch (already recorded in ARCH-CONV-B).
2. `test_kbs23_catalogue_panel_harness_runs_all_panel_fixtures` missing `user`.
3. Total-cholesterol blank activation-key fail-closed before ARCH-CONV-C code.

## Independent STOP C baseline comparison (required)

Independent STOP C review was conditional on proving the full-suite failure
set is unchanged versus pre-ARCH-CONV-C baseline
`cdc6cf3d463d50902a080b51136ef1a98b431f4a`.

### Commands

```text
# Active branch left untouched at feature/arch-conv-c-alp-ggt-why-authority (f1e0d33)
git worktree add C:\Users\abroa\HealthIQ-AI-v5-wt-arch-conv-c-baseline cdc6cf3d463d50902a080b51136ef1a98b431f4a

# Current HEAD full suite (committed ARCH-CONV-C)
python -m pytest backend/tests -q --tb=no --junitxml=docs/architecture/_stop_c_suite_compare/current_junit.xml

# Baseline full suite in isolated worktree (after copying gitignored .env for parity)
python -m pytest backend/tests -q --tb=no --junitxml=docs/architecture/_stop_c_suite_compare/baseline_junit.xml
```

Node-ID extracts and classification lists are retained under:

```text
docs/architecture/_stop_c_suite_compare/
```

### Result counts

| Suite | Commit | FAILED | ERROR |
| --- | --- | ---: | ---: |
| ARCH-CONV-C HEAD | `f1e0d33` | 61 | 0 |
| Pre-ARCH-CONV-C baseline | `cdc6cf3` | 56 | 110 |

The first baseline attempt ran in parallel without `.env` and was discarded as
contaminated. The recorded baseline is the serial re-run with `.env` copied
into the worktree. Docker Desktop / Postgres `:5433` was unavailable for most
of the baseline window (`connection refused`), producing a large ERROR cascade
in `backend/tests/integration/*` migration setup.

### Classification summary

| Class | Count | Verdict |
| --- | ---: | --- |
| Present on both (FAILED ∩ FAILED) | 53 | Unchanged baseline failures |
| Newly introduced by ARCH-CONV-C (`current − baseline_failed − baseline_error`) | **0** | Pass criterion met |
| Baseline FAILED resolved / absent on ARCH-CONV-C | 3 | See notes below |
| Current FAILED + baseline ERROR (same node IDs) | 8 | Environmental / outcome-incomparable; baseline-reproduced as non-passing |
| Baseline ERROR only (not in current FAILED) | 102 | Environmental DB/migration cascade while Postgres unavailable |

### Newly introduced by ARCH-CONV-C

**None.** Exact set is empty.

### Failures present on both (53)

Shared FAILED node IDs include the known long-standing clusters already cited
in this proof (VR fixture, catalogue harness, total-cholesterol blank key,
alias/SSOT inventory, scoring snapshots, staged-PSI counts, orphan inventory,
LC-S20/S21 replay/fingerprint, insights golden parity, and related units).
Full list: `docs/architecture/_stop_c_suite_compare/both_failed.txt`.

### Resolved / baseline-only FAILED (3)

1. `backend/tests/unit/test_arch_rt5_launch_gate.py::test_estate_index_loads`
   - Baseline expects 17 compiled hypothesis artefacts and fails at 19
     (post-ARCH-CONV-B estate).
   - ARCH-CONV-C intentionally refreshed the sentinel to 21 after adding the
     two ratified ALP/GGT compiled artefacts. Current HEAD passes.
   - Classification: **resolved by ARCH-CONV-C** (governed estate count update).

2. `backend/tests/regression/test_arch_conv_b_renal_stop_c.py::test_canonical_source_hashes_and_embedded_identity_are_stable`
   - Baseline worktree checkout hashes LF bytes; the expected digests are the
     CRLF working-tree hashes used on the active Windows checkout.
   - Current HEAD passes. Not an ARCH-CONV-C logic change.
   - Classification: **environmental / checkout line-ending instability**.

3. `backend/tests/regression/test_persisted_result_replay_status.py::TestPersistedResultReplayStatus::test_golden_runs_corpus_exists`
   - Baseline worktree lacks `backend/artifacts/golden_runs` because
     `artifacts/` is gitignored (`.gitignore:87`).
   - Current checkout has the local corpus and passes.
   - Classification: **environmental / worktree isolation** (missing
     gitignored artefacts).

### Environmental / incomparable (8 current FAILED ∩ baseline ERROR)

These node IDs failed on ARCH-CONV-C with content assertions and errored on
baseline at integration DB migration setup while Postgres `:5433` was down:

- `...test_clustering_result_structure`
- `...test_clustering_with_different_algorithms`
- `...test_full_pipeline_with_questionnaire`
- `...test_pipeline_without_questionnaire`
- `...test_pipeline_with_specific_categories`
- `...test_insight_pipeline_metabolic_category_passes`
- `...test_health_system_scoring_accuracy_integration`
- `...test_ssot_fallback_when_lab_range_missing`

Baseline reproducibility evidence:

- Baseline full suite and targeted re-runs raise
  `RuntimeError: Could not migrate test DB to head` /
  `psycopg2.OperationalError: connection ... port 5433 failed: Connection refused`.
- Docker Desktop engine was unavailable during the comparison
  (`dockerDesktopLinuxEngine` pipe missing).
- Targeted ARCH-CONV-C re-runs of the same nodes, when the process reached the
  test body, failed on pre-existing assertions unrelated to ALP/GGT
  (`cluster_engine_v2` membership, empty insight counts, missing SSOT source).
- ARCH-CONV-C did not modify these integration modules, scoring engines, or
  DB fixtures.

Classification: **environmental instability**; same nodes are non-passing on
baseline under the same environment.

### STOP C comparison verdict

- New ARCH-CONV-C-attributable full-suite failures: **0**
- Incomparable nodes: only the DB-linked integration set above, each
  baseline-reproduced as non-passing under the same unavailable-Postgres
  environment
- Active branch was not reset; baseline used an isolated worktree only

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
9. Baseline comparison above shows zero new ARCH-CONV-C-attributable failures.
10. Environmental/incomparable nodes are baseline-reproduced as non-passing.

## Independent STOP C decision

Independent STOP C checks were completed by Head of Architecture on 2026-07-30.
The baseline comparison confirms **zero new ARCH-CONV-C-attributable failures**.
Outcome: **APPROVED**.

**STOP C status:** `STOP_C_APPROVED_BY_HEAD_OF_ARCHITECTURE`  
**Cursor verdict:** none; self-certification prohibited.

## STOP C verdict

`STOP C APPROVED BY HEAD OF ARCHITECTURE — AUTOMATION BUS FINISH AUTHORISED`

Baseline comparison complete: **zero new ARCH-CONV-C-attributable failures**.
Independent STOP C approved by Head of Architecture on 2026-07-30.

Automation Bus finish completed under this approval. Merge is not authorised by
this document.
