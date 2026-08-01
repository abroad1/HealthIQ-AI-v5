---
work_id: ARCH-CONV-G
branch: feature/arch-conv-g-urate-compiled-why
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
implementation_owner: Core Engine agent
gate1_status: PENDING
gate2_status: PENDING
---

# ARCH-CONV-G — Urate Compiled-WHY Authority

## Purpose

Complete governed compiled-WHY authority for:

`signal_urate_high::inv_uric_acid_high_metabolic`

This is an SOP-governed Intelligence Core work package.

The canonical urate signal and Knowledge Bus packages already exist. This sprint does not create a new signal library or commission new medical research. It promotes the existing governed research into compiled-WHY authority, resolves competing WHY ownership, and proves safe runtime behaviour.

## Governing SOPs

- `AUTOMATION_BUS_SOP_v1.3.1.md`
- `KNOWLEDGE_BUS_SOP_v1.3.1.md`
- `KNOWLEDGE_BUS_PASS3_PROMOTION_PROTOCOL_v1.1.md`

## Current governance state

Gate 1 and Gate 2 are not yet approved.

Proposed references:

- Gate 1: `ARCH-CONV-G-GATE1-HMR-PENDING`
- Gate 2: `ARCH-CONV-G-GATE2-ANTHONY-PENDING`

Cursor must not implement the medical authority or mark the package complete until:

1. the Phase 0 source-to-runtime map is produced;
2. GPT, acting as Head of Medical Research and Head of Architecture, records Gate 1;
3. Anthony, acting as human project authority, records Gate 2;
4. both approvals are committed to the repository;
5. the approved disposition matches this prompt or this prompt is revised and re-hardened.

Retrospective ratification is forbidden.

## Product outcome

Once Gate 1 and Gate 2 are recorded, implement:

- one `COMPILED_ACTIVE` canonical urate WHY authority;
- one competing urate frame retired for WHY ownership only;
- unchanged package-layer and PSI state;
- no change to creatinine, urea, eGFR, UACR, chronicity, HbA1c, ALT, or other completed domains;
- no new compiler mechanism unless explicitly returned for re-hardening.

Expected canonical activation key:

`signal_urate_high::inv_uric_acid_high_metabolic`

Expected canonical source package:

`pkg_s24_urate_high_metabolic`

Expected competing package for review:

`pkg_kb52c_urate_high_gout_crystal_deposition_risk`

The expected competitor disposition is `LEGACY_RETIRED_FOR_WHY_ONLY`, but Cursor must not assume this until the package content has been fully mapped and Gate 1 approves the medical disposition.

## Mandatory source set

Read in full before proposing implementation:

- `docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md`
- `docs/architecture/ARCH-CONV-B_STOP_C_runtime_proof.md`
- `docs/architecture/signal_id_collision_inventory.md`
- `knowledge_bus/governance/compiled_why_authority_register_v1.yaml`
- `knowledge_bus/governance/root_cause_authority_register_v1.yaml`
- `backend/core/knowledge/root_cause_registry_v1.py`
- `backend/core/knowledge/why_authority_v1.py`
- `backend/core/analytics/root_cause_compiler_v1.py`
- `knowledge_bus/research/investigation_specs/inv_uric_acid_high_metabolic.yaml`
- every file under `knowledge_bus/packages/pkg_s24_urate_high_metabolic/`
- every file under `knowledge_bus/packages/pkg_kb52c_urate_high_gout_crystal_deposition_risk/`
- relevant compiled-WHY precedents from `ARCH-CONV-B`, `ARCH-CONV-C`, and `ARCH-CONV-F`

Validate the canonical investigation spec before using it.

Do not read raw Pass 3 or investigation-spec files at runtime. They are build-time medical authority only.

## Stage 0 — baseline and branch alignment

Before any governed change:

1. Confirm `main` is clean and synchronized with `origin/main`.
2. Confirm the current branch and active Automation Bus state.
3. Create or switch to:

   `feature/arch-conv-g-urate-compiled-why`

4. Confirm the work ID and branch match the front matter.
5. Confirm no conflicting active work-package token exists.
6. Confirm the intended outcome is not already delivered.
7. Record the current counts in `compiled_why_authority_register_v1.yaml`.
8. Confirm:
   - no `COMPILED_ACTIVE` urate row exists;
   - the canonical compiled urate artefact does not already exist;
   - `signal_urate_high` is not already in the compiled-WHY cohort;
   - creatinine and urea remain closed and unchanged.
9. If repository reality differs materially, STOP.

## Phase 0 — medical and architectural mapping

Before implementation, produce and commit a bounded ARCH-CONV-G decision pack that resolves the following.

### 1. Identity

Confirm:

- canonical signal ID;
- canonical spec ID;
- canonical activation key;
- canonical package;
- competing package;
- whether “urate” versus “uric acid” is only a naming convention.

Do not create a new alias, signal ID, package ID, or activation-key convention.

STOP if the naming difference cannot be resolved using existing conventions.

### 2. Canonical medical authority

Map the canonical investigation spec exactly:

- primary finding;
- `why_role`;
- supporting markers and their roles;
- contradiction behaviour;
- override rules;
- missing-data behaviour;
- presentation-safety restrictions;
- evidence provenance.

Do not infer gout, crystal deposition, chronic kidney disease, renal failure, treatment need, or causal metabolic disease from urate alone unless the canonical research explicitly authorises that wording.

### 3. Competing gout/crystal-deposition frame

Read the competing package and determine whether its content is:

- duplicate foundational authority;
- subordinate risk/context wording;
- a medically distinct frame requiring retention;
- unsupported for independent WHY ownership.

Propose one of:

- `LEGACY_RETIRED_FOR_WHY_ONLY`;
- `SUBORDINATE_CONTEXT_ONLY`;
- retain as independent authority.

Any choice other than retirement requires an explicit medical rationale and Gate 1 approval.

No package may be deleted. No PSI status may be revoked.

### 4. Supporting markers

Verify the canonical role of:

- `creatinine`;
- `triglycerides`;
- `egfr`.

Supporting markers may enrich or escalate the urate interpretation only within the limits of the canonical research.

They must not create new independently owning WHY frames.

### 5. eGFR override

Verify the existing rule:

`or_uric_acid_renal_risk`

Determine exactly:

- its activation condition;
- its resulting state;
- whether it is concern/risk escalation only;
- whether it requires a single eGFR value or an established chronicity concept;
- what presentation restrictions are required.

The sprint must not:

- diagnose chronic kidney disease from one result;
- alter creatinine or urea authority;
- create eGFR-owned WHY authority;
- add UACR or chronicity logic;
- add a new SSOT or derived metric.

STOP if the existing rule cannot be represented safely without new medical research or a new runtime mechanism.

### 6. Runtime mechanism

Confirm whether the existing mechanisms are sufficient:

- static `why_role`;
- existing override-rule handling;
- compiled-WHY register;
- existing compiled artefact loader;
- existing pilot/cohort inclusion in `why_authority_v1.py`;
- existing retirement/skip handling.

No change is expected in:

- `backend/core/analytics/root_cause_compiler_v1.py`
- `backend/core/knowledge/root_cause_registry_v1.py`

STOP if a genuinely new mechanism is required.

## Gate 1 and Gate 2 STOP

After Phase 0 mapping:

1. Create or update the ARCH-CONV-G medical decision register in draft state.
2. Create a Gate 1/Gate 2 decision document with both statuses `PENDING`.
3. Record the exact proposed:
   - activation key;
   - WHY role;
   - override interpretation;
   - package dispositions;
   - presentation restrictions;
   - exclusions.
4. Commit the Phase 0 governance artefacts.
5. STOP.

Return the decision pack for:

- GPT Gate 1 medical and architectural review;
- Anthony Gate 2 project-authority approval.

Do not implement before both approvals are recorded on disk.

## Post-gate implementation boundary

Only after Gate 1 and Gate 2 are approved and committed may Cursor implement the approved design.

Expected implementation files:

- `knowledge_bus/governance/compiled_why_authority_register_v1.yaml`
- `backend/core/knowledge/why_authority_v1.py`
- one new compiled urate hypothesis artefact under `knowledge_bus/compiled/hypotheses/`
- one compile manifest under `knowledge_bus/compiled/manifests/`
- `knowledge_bus/compiled/estate_index_v1.yaml`
- `knowledge_bus/governance/root_cause_authority_register_v1.yaml` for bookkeeping consistency if required
- focused ARCH-CONV-G tests
- implementation evidence and decision records
- relevant count-based regression tests where mechanically required

Expected authority delta, subject to Gate 1 confirmation:

- `+1 COMPILED_ACTIVE`
- `+1 LEGACY_RETIRED`

Any different delta requires a STOP.

Do not change:

- any `signal_library.yaml`;
- any package manifest except mandatory validation bookkeeping already required by the existing contract;
- package activation or eligibility;
- PSI status;
- SSOT biomarker definitions;
- derived-metric registries;
- frontend files;
- completed compiled-WHY authority outside urate;
- creatinine or urea authority.

## Explicit exclusions

Do not modify or compile authority for:

- `signal_hba1c_high`
- `signal_hba1c_pct_high`
- `signal_creatinine_high`
- `signal_urea_high`
- eGFR, UACR, or chronicity as independent WHY targets
- ferritin or haemoglobin
- ALT
- thyroid
- lipid
- ALP or GGT
- bilirubin WHY
- total-cholesterol WHY
- urate-low or any unrelated urate signal

## Required tests after approval and implementation

The final implementation must prove:

1. the canonical urate activation key resolves through compiled authority;
2. the canonical finding and `why_role` exactly match Gate 1;
3. the competing frame resolves according to the ratified disposition;
4. no dual-serving urate WHY ownership remains;
5. gout or crystal-deposition diagnosis is not emitted from urate alone unless Gate 1 explicitly authorises bounded context wording;
6. the eGFR override changes only the permitted risk/concern state;
7. one eGFR result does not produce a CKD diagnosis;
8. creatinine and urea compiled authority remain bit-for-bit unchanged;
9. missing supporting markers fail closed;
10. no raw research file is read at runtime;
11. no package-layer, PSI, SSOT, derived-metric, or frontend behaviour changes;
12. no new compiler mechanism is introduced;
13. no unrelated compiled-WHY authority changes;
14. deterministic repeatability;
15. the compiled-WHY authority validator passes;
16. both urate packages pass package validation;
17. existing thyroid, lipid, renal, ALP/GGT, ferritin, and haemoglobin compiled-WHY regression suites remain passing;
18. complete relevant test modules are run, not selected nodes only.

Record exact before/after counts for:

- total authority frames;
- `COMPILED_ACTIVE`;
- `LEGACY_RETIRED`;
- `REJECTED`;
- loaded compiled frames;
- affected signal families.

## Evidence requirements

Commit an ARCH-CONV-G implementation and verification report containing:

- baseline proof;
- exact source-to-runtime rule map;
- Gate 1 and Gate 2 references;
- canonical and competing package dispositions;
- exact files changed;
- before/after authority counts;
- source and output hashes;
- complete test commands and outputs;
- validator outputs;
- deterministic-repeatability proof;
- proof that no runtime research-file read was introduced;
- proof that package, PSI, SSOT, derived-metric, frontend, creatinine, and urea behaviour did not change;
- proof that no unsupported diagnosis or medical rule was invented;
- known unrelated baseline failures with clean-main comparison where needed.

Do not omit failures. Any new sprint-attributable failure blocks completion.

## Mandatory STOP conditions

STOP if:

- Gate 1 or Gate 2 remains unrecorded;
- the urate/uric-acid naming difference requires a new identity or alias;
- the competitor contains medically distinct authority that cannot be safely retired or subordinated;
- canonical research is insufficient;
- a new threshold, ranking, diagnosis, SSOT biomarker, or derived metric is required;
- the eGFR rule cannot be represented without implying CKD from one result;
- creatinine or urea authority changes;
- `root_cause_compiler_v1.py` or `root_cause_registry_v1.py` requires a new mechanism;
- package activation or PSI state would change;
- the authority delta differs from the ratified expectation;
- an unrelated compiled-WHY signal changes;
- a new sprint-attributable test failure remains.

Retrospective ratification is forbidden.

## Automation Bus lifecycle

This prompt must first be hardened by Claude Code.

Required hardening instruction:

`harden work_id: ARCH-CONV-G — verify source content and produce evidence checklist`

Cursor must not run the kernel unless:

`automation_bus/latest_prompt_hardening.json`

records `HARDENED` for `ARCH-CONV-G`.

After successful hardening, run:

```powershell
python backend/scripts/run_work_package.py start
```

Use the `TWO_PHASE_START_FINISH` model.

The first execution phase ends at the Gate 1/Gate 2 STOP described above.

After the gate records are approved, committed, and consistent with this hardened prompt, resume the same work package. If the approved disposition changes the implementation instructions materially, update this prompt and obtain fresh CC hardening before implementation.

After implementation and evidence are committed, carry out the mandatory Post-Implementation Closure Protocol from Automation Bus SOP v1.3.1.

As part of closure, update:

- `docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md`
- the central Active Carry-Forward Register where programme-wide obligations remain

The Build Deliverables Register entry must record:

- what ARCH-CONV-G delivered;
- authority rows added or retired;
- medical safeguards;
- packages retained;
- exclusions preserved;
- unresolved carry-forwards;
- the recommended next sequencing action.

Then run:

```powershell
python backend/scripts/run_work_package.py finish
```

If finish leaves only the kernel-owned `automation_bus/latest_cursor_status.json` dirty and it records `COMPLETE` for `ARCH-CONV-G`, commit it exactly as:

`chore(bus): ARCH-CONV-G kernel COMPLETE status`

Do not merge.

STOP after successful finish and closure-clean verification for independent Claude Code audit, GPT review, and Anthony's final merge authority.
