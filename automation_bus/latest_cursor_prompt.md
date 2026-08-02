---
work_id: ARCH-CONV-I
branch: feature/arch-conv-i-alt-compiled-why-identity-resolution
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# ARCH-CONV-I — ALT Compiled-WHY Identity Resolution and Governed Disposition

## Purpose

Resolve the remaining ALT compiled-WHY identity ambiguity between:

- legacy WHY identity: `signal_hepatic_alt_context`
- current multi-frame ALT family: `signal_alt_high`

This work package must complete Phase 0 repository mapping, stop for Gate 1 and Gate 2, and then implement only the ratified disposition.

The permitted implementation outcomes are:

1. narrowly compile the canonical hepatocellular ALT frame and retire the legacy WHY identity; or
2. retire the legacy WHY identity without a compiled successor.

No other disposition is authorised without re-scoping.

## Governing sources

Read and apply:

- `AUTOMATION_BUS_SOP_v1.3.1.md`
- `KNOWLEDGE_BUS_SOP_v1.3.1.md`
- `KNOWLEDGE_BUS_PASS3_PROMOTION_PROTOCOL_v1.1.md`
- `docs/architecture/ADR-RT-001_research_to_runtime_day_one_architecture.md`
- `docs/architecture/ADR-RT-002_signal_spec_identity_and_registry_policy.md`
- `docs/architecture/ADR-RT-003_hypothesis_artefact_and_root_cause_transition.md`
- `docs/architecture/ADR-RT-004_compile_manifest_and_package_provenance_policy.md`
- `automation_bus/latest_scope_advisory.md`
- `docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md`
- relevant ARCH-CONV-D, E, E2 and E3 decision/evidence artefacts

## Stage 1A — Authority preflight

Before implementation, verify and record:

1. The current canonical investigation spec for the general hepatocellular ALT frame.
2. The legacy package and live legacy WHY asset for `signal_hepatic_alt_context`.
3. The current root-cause registry wiring for the legacy identity.
4. The complete `signal_alt_high` activation-frame estate.
5. Current compiled-WHY authority-register state for both identities.
6. Current runtime reachability and activation-register state.
7. That no existing compiled ALT WHY authority already resolves this work.
8. That no raw investigation spec is read directly at runtime.
9. That the current compiler/loader mechanism can support the ratified outcome without a new compiler mechanism.
10. That package, PSI, card and signal-activation behaviour can remain unchanged under a WHY-only retirement.

Record exact paths and line references in the Phase 0 evidence pack.

## Stage 1B — Reality check

Confirm the problem still exists on current `main`:

- `signal_hepatic_alt_context` remains wired to the live legacy WHY asset;
- neither `signal_hepatic_alt_context` nor `signal_alt_high` has compiled-WHY authority;
- the legacy CRP-coupled hypothesis has no canonical `signal_alt_high` counterpart;
- the legacy hard-coded AST/GGT/ALP/bilirubin thresholds remain non-SSOT behaviour and must not be transferred.

If any of these statements is no longer true, STOP and report the changed repository reality.

## Stage 1C — Intelligence preflight

Identify all affected Intelligence Core surfaces, including at minimum:

- compiled-WHY authority register;
- legacy root-cause authority register;
- compiled hypothesis artefact and manifest paths, if Outcome A is ratified;
- WHY authority resolver/pilot membership;
- root-cause compiler and registry;
- report/output authority projection;
- regression and architecture validation gates.

Expected output change must be limited to ALT WHY ownership and wording.

Do not change signal activation, R-value classification, package reachability, PSI status, scoring, frontend behaviour or biomarker SSOT.

# Phase 0 — Mandatory Gate 1 / Gate 2 preparation

After kernel start, perform repository mapping only.

Create and commit:

- `docs/architecture/ARCH-CONV-I_hardening_pack.md`
- `docs/architecture/ARCH-CONV-I_medical_decision_register.yaml`
- `docs/architecture/ARCH-CONV-I_GATE_1_GATE_2_decision.md`

The decision pack must explicitly present these two choices.

## Outcome A — Narrow MAP_AND_COMPILE

- Compile only the canonical general hepatocellular ALT frame:
  - `signal_alt_high::<canonical hepatocellular spec_id>`
- Retire `signal_hepatic_alt_context` for WHY ownership only.
- Transfer only content jointly supported by:
  - the canonical hepatocellular ALT investigation spec; and
  - the legacy hepatocellular-stress hypothesis.
- Exclude the legacy CRP/inflammatory-coupling hypothesis.
- Do not transfer legacy hard-coded AST/GGT/ALP/bilirubin thresholds.
- Preserve all ARCH-CONV-E2/E3 R-value and contextual activation behaviour unchanged.
- Expected register delta: `+1 COMPILED_ACTIVE`, `+1 LEGACY_RETIRED`.

## Outcome B — RETIRE_WITHOUT_SUCCESSOR

- Retire `signal_hepatic_alt_context` for WHY ownership only.
- Do not create a compiled ALT WHY artefact.
- Keep package, PSI, card and activation behaviour unchanged.
- Record that canonical research was insufficient for a safe compiled successor.
- Expected register delta: `+0 COMPILED_ACTIVE`, `+1 LEGACY_RETIRED`.

## Gate 1 questions

Head of Medical Research must decide:

1. Whether the legacy hepatocellular-stress hypothesis maps safely and narrowly to the canonical hepatocellular `signal_alt_high` frame.
2. Whether Outcome A or Outcome B is approved.
3. The exact approved `why_role` if Outcome A is selected.
4. The exact consumer-safe wording boundaries.
5. The explicit disposition of the legacy CRP/inflammatory-coupling hypothesis.
6. Confirmation that no hard-coded legacy thresholds may transfer.
7. Confirmation that no Hy’s Law, MASLD, fibrosis, disease-specific, treatment or chronicity claim may be introduced.

## Gate 2

Anthony must ratify Gate 1 exactly.

No runtime implementation is authorised until both Gate 1 and Gate 2 decisions are recorded on disk and agree.

## Mandatory STOP

After committing the Phase 0 pack:

- STOP.
- Keep the work package `IN_PROGRESS`.
- Do not create a compiled artefact.
- Do not alter authority registers.
- Do not retire legacy WHY ownership.
- Do not change runtime code or tests beyond Phase 0 evidence preparation.
- Report the exact Gate 1 decision required.

# Phase 1 — Implementation after Gate 1 and Gate 2 only

Implement only the ratified outcome.

## If Outcome A is ratified

Create a governed compiled hypothesis artefact and compile manifest for the canonical hepatocellular ALT frame.

Requirements:

- one activation-key-specific compiled authority;
- approved `why_role` only;
- no CRP/inflammatory-coupling hypothesis;
- no transfer of hard-coded AST/GGT/ALP/bilirubin thresholds;
- no consumer Hy’s Law diagnosis;
- no MASLD, steatosis, fibrosis or disease-specific diagnosis from ALT alone;
- no treatment directive;
- no chronicity inference;
- no reinterpretation of E2/E3 R-value or contextual frame authority;
- no change to package/PSI/runtime activation status.

Add the canonical activation key to the existing WHY authority mechanism only if required by the current architecture.

Retire `signal_hepatic_alt_context` for WHY ownership only.

## If Outcome B is ratified

- Add only the governed legacy retirement/disposition required to stop legacy WHY ownership.
- Do not create a compiled ALT WHY artefact.
- Do not add ALT to compiled-WHY pilot membership.
- Preserve all package, PSI, card, activation and R-value behaviour.

# Explicit prohibitions

Do not:

- create a runtime alias between `signal_hepatic_alt_context` and `signal_alt_high`;
- compile the CRP/inflammatory-coupling hypothesis without new canonical research;
- transfer the legacy hard-coded thresholds;
- change the R-value formula or boundaries;
- change ALT package activation or reachability;
- alter ALP/GGT primary source authority;
- activate the bilirubin-severity package independently;
- introduce Hy’s Law diagnosis wording;
- change biomarker aliases, SSOT identities, derived metrics or scoring;
- modify frontend medical logic;
- introduce a new compiler or fallback parser;
- read raw research at runtime;
- delete package or PSI assets.

# Tests

Add a dedicated regression suite:

`backend/tests/regression/test_arch_conv_i_alt_stop_c.py`

At minimum prove:

1. The ratified disposition is represented exactly.
2. If Outcome A:
   - canonical hepatocellular activation key resolves `COMPILED_ACTIVE`;
   - approved `why_role` is flat and exact;
   - legacy ALT WHY identity resolves `LEGACY_RETIRED`;
   - CRP content is absent;
   - legacy hard-coded thresholds are absent;
   - prohibited claims are absent from emitted output.
3. If Outcome B:
   - no compiled ALT authority row exists;
   - legacy ALT WHY identity resolves retired/skip;
   - no runtime fallback silently restores the legacy WHY path.
4. All `signal_alt_high` activation and E2/E3 R-value/contextual behaviour remains unchanged.
5. ALP/GGT authority remains unchanged.
6. Package and PSI status remain unchanged.
7. No raw research file read is introduced.
8. Register counts change only by the ratified delta.
9. ARCH-CONV-F, G and H regression suites remain green.
10. Existing architecture, root-cause, output-authority and phenotype tests remain green.

Run all targeted suites plus:

- `python backend/scripts/validate_compiled_why_authority_gate.py`
- architecture validation gate
- baseline test suite required by the Automation Bus
- three-layer pipeline verification

# STOP conditions during implementation

STOP if:

- Gate 1 and Gate 2 do not match;
- the canonical hepatocellular activation key is ambiguous;
- safe mapping requires content absent from canonical research;
- CRP content is required for parity under Outcome A;
- hard-coded legacy thresholds would need to be retained;
- implementation requires a runtime alias;
- implementation changes signal activation, R-value behaviour, package reachability, PSI, scoring, frontend or SSOT;
- any non-ALT compiled-WHY authority changes;
- any relevant regression cannot be explained and bounded;
- the expected register delta differs from the ratified outcome.

# Evidence and closure

Produce:

- `docs/audit-papers/ARCH-CONV-I_implementation_and_verification_report.md`
- updated Gate decision record;
- updated medical decision register;
- updated Build Deliverables Register entry;
- updated central carry-forward register only where the ratified outcome genuinely closes or creates a programme carry-forward.

Before `finish`, complete the mandatory Post-Implementation Closure Protocol from Automation Bus SOP v1.3.1.

Run kernel finish only after:

- implementation is complete;
- targeted and required regression suites pass;
- repo hygiene is proven;
- no unrelated files remain.

Do not merge.

After kernel COMPLETE, stop for independent Claude Code audit, GPT architectural review and Anthony merge authority.
