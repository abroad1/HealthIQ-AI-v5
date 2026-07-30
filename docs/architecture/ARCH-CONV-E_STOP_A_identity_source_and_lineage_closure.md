# ARCH-CONV-E — STOP A identity, source, and lineage closure

**Work ID:** `ARCH-CONV-E`  
**Branch:** `feature/arch-conv-e-alt-why-authority`  
**Baseline:** `main == origin/main == 39da186b7b13a1c2bf571f68c070f6201905649c`  
**Hardening:** `automation_bus/latest_prompt_hardening.json` — `ARCH-CONV-E`, `HARDENED`  
**Kernel:** `ARCH-CONV-E`, `IN_PROGRESS`  
**Status:** `STOP_A_SUBMISSION_READY_FOR_HEAD_OF_ARCHITECTURE`

This is repository and architecture evidence only. Cursor has made no medical,
collision-policy, threshold, compilation, runtime, or legacy-retirement
decision.

## 1. Lifecycle preflight

| Check | Result |
|---|---|
| local main equals origin/main | yes; `39da186b7b13a1c2bf571f68c070f6201905649c` |
| ARCH-CONV-D merged and published | yes |
| branch created from current main | yes |
| pre-start worktree | clean after committing prompt/hardening handoff |
| stash | empty; no convenience stash created |
| pre-start token | absent |
| hardening | matching `ARCH-CONV-E` / `HARDENED` |
| kernel start | exit 0 |
| active token | matching `ARCH-CONV-E` and branch |

## 2. ARCH-CONV-D decision reconfirmed

The merged repository exactly preserves the approved identity closure:

- `signal_alt_high` is the sole canonical future ALT authority identity;
- `signal_hepatic_alt_context` is a legacy predecessor/context implementation;
- no runtime alias exists;
- legacy WHY remains temporarily owned by `signal_hepatic_alt_context`;
- ARCH-CONV-E must medically adjudicate frames, govern thresholds, design the
  hepatocellular axis, adjudicate legacy transfer/retirement, and prove no
  duplicate ALT user-facing authority.

Evidence:

- `knowledge_bus/governance/arch_conv_d_alt_identity_relationship_v1.yaml`
- `docs/architecture/ARCH-CONV-D_identity_decision_register.yaml`
- `docs/architecture/ARCH-CONV-D_STOP_A_head_of_architecture_decision.md`

No discrepancy or reopening of ARCH-CONV-D was found.

## 3. Canonical identity and source

The canonical investigation spec embeds:

```text
spec_id: inv_alt_high_hepatocellular_injury
signal_id: signal_alt_high
```

Therefore the canonical migration target is unambiguously:

```text
signal_alt_high::inv_alt_high_hepatocellular_injury
```

Source:
`knowledge_bus/research/investigation_specs/inv_alt_high_hepatocellular_injury_v1.yaml`

Working-tree SHA-256:
`7189a0761558937d4dd4397e823bbe06c7bee0b13ef9bbe0b3afc70a73b7413a`

Package:
`pkg_s24_alt_high_hepatocellular_injury`, `translation_mode: creation`.

The signal is live and indexed. It has no legacy registry target and no
compiled WHY row. Current generic fallback is not governed ALT frame authority.

## 4. Candidate identity/source closure

Three separate Pass 3 identities are embedded in promoted signal intelligence:

```text
signal_alt_high::inv_alt_high_hepatocellular_injury_pattern
signal_alt_high::inv_alt_high_metabolic_steatotic_liver_pattern
signal_alt_high::inv_alt_high_muscle_source_or_exertional_pattern
```

Each has a translated package and live signal-layer representation but blocked
provenance for explicit-lineage claims and no compiled WHY authority. Their
identity-index presence does not medically approve them. Detailed mapping is in
`ARCH-CONV-E_target_to_frame_map.md`.

## 5. Legacy ALT closure

Current ownership is exact and family-level:

```text
backend/core/knowledge/root_cause_registry_v1.py
  → signal_hepatic_alt_context
  → load_alt_hypotheses_v1
  → knowledge_bus/root_cause/hypotheses/alt_hypotheses_v1.yaml
```

The legacy asset contains:

1. `alt_hepatic_cell_stress_pattern_v1`;
2. `alt_inflammatory_coupling_context_v1`.

The inflammatory/CRP hypothesis is not traceable to the canonical ALT source
and cannot transfer silently. Current dual-signal execution emits both generic
canonical fallback and predecessor legacy WHY, creating a duplicate-output
risk. No registry mapping or runtime behavior has been changed.

## 6. Threshold closure

All current numeric literals are mapped in
`ARCH-CONV-E_medical_review_pack.md`:

```text
ALT 120
AST 45
GGT 60
ALP 130
bilirubin 20
ALT placeholder 9999
```

Key closure facts:

- package baseline activation is lab-range-driven;
- the `9999` values are validator placeholders;
- canonical ALT `120` is source-backed only as a typical 3×ULN assumption;
- canonical bilirubin and ALP source rules use lab boundaries, while translated
  packages hardcode `20` and `130`;
- predecessor AST/GGT/ALP/bilirubin cutoffs are package-local;
- no fixed cutoff may be transferred by default.

Threshold remediation remains blocked pending Gate 1 and Gate 2.

## 7. ARCH-CONV-C lineage repair

The defect was present and metadata-only. Compiled ALP/GGT bytes were proved
identical to implementation commit `3dcfd39` and merged baselines. Only the two
manifest `output_hash` values were corrected.

Commit:

```text
33e32a5 fix(governance): repair ARCH-CONV-C compiled manifest hashes
```

Evidence:
`docs/architecture/ARCH-CONV-E_arch_conv_c_hash_repair_evidence.md`.

No ALP/GGT compiled artefact or medical content changed.

## 8. Proposed hepatocellular boundary

The medical-review boundary is sufficient for Phase 1:

- ALT primary eligibility remains a medical decision;
- AST is supporting/corroborating only unless separately governed later;
- bilirubin/albumin may be severity context only;
- ALP/GGT may identify a concurrent mixed/cholestatic pattern without changing
  `cholestatic_source_axis`;
- CK, exercise, trauma, and muscle symptoms may contradict hepatic attribution;
- metabolic, alcohol, medication, toxin, viral, symptom, and serial context
  require explicit rules;
- a new hepatocellular group may be required, but is not created or named here;
- selection must be activation-key-explicit and deterministic;
- duplicate ALT-family output must be consolidated, suppressed, or refused only
  under ratified policy;
- AST and bilirubin future authority remains preserved and excluded.

## 9. Explicit exclusions preserved

- no AST WHY;
- no bilirubin/hyperbilirubinemia migration;
- no ALP-low authority;
- no change to `cholestatic_source_axis`;
- no ALP/GGT medical-content change;
- no liver-card scoring change;
- no frontend logic change;
- no raw Pass 3 source change;
- no unrelated package, fixture, snapshot, report, or estate change.

## 10. Phase 0 verification

Completed focused checks:

```text
python backend/scripts/validate_investigation_spec.py --spec knowledge_bus/research/investigation_specs/inv_alt_high_hepatocellular_injury_v1.yaml
→ PASS; v2 contract; 0 errors

python backend/scripts/validate_knowledge_package.py --package-dir knowledge_bus/packages/pkg_s24_alt_high_hepatocellular_injury
→ manifest/research/signal PASS; ready_for_implementation true

python backend/scripts/validate_knowledge_package.py --package-dir knowledge_bus/packages/pkg_hepatic_alt_context
→ manifest/research/signal PASS; ready_for_implementation true

python backend/scripts/validate_medical_frame_identity_index.py
→ PASS; 0 errors

python backend/scripts/validate_compiled_why_authority_gate.py
→ PASS; 37 frames, 21 compiled active, 1 rejected, 15 legacy retired

python -m pytest backend/tests/regression/test_arch_conv_c_alp_ggt_stop_c.py -q
→ 20 passed

python -m pytest backend/tests/regression/test_med_frame_identity_index.py -q
→ 11 passed

python -m pytest backend/tests/unit/test_root_cause_v1_homocysteine.py::test_root_cause_v1_alt_hypotheses_emit_for_alt_signal -q
→ 1 passed

python -m pytest backend/tests/unit/test_signal_evaluator.py::test_signal_registry_alt_high_multi_frame_pilot backend/tests/unit/test_signal_evaluator.py::test_kbs24_signals_trigger_suboptimal_then_escalate[signal_alt_high] backend/tests/unit/test_signal_activation_identity_v1.py -q
→ 5 passed
```

## STOP A questions

1. Is the canonical migration target unambiguous? **Repository evidence: yes.**
2. Are candidates and legacy paths closed? **Repository evidence: yes; medical
   roles remain pending.**
3. Is the ARCH-CONV-C hash defect safely repaired? **Yes, metadata only.**
4. Is the threshold issue mapped? **Yes; treatment remains pending.**
5. Is the Gate 1 review boundary sufficient? **Submitted for independent
   architecture approval.**
6. Are AST, bilirubin, and cholestatic exclusions preserved? **Yes.**
7. May Phase 1 prepare Gate 1 decisions without implementation? **Awaiting Head
   of Architecture.**

## STOP A status

`AWAITING INDEPENDENT HEAD OF ARCHITECTURE APPROVAL`

Do not proceed to Phase 1.
