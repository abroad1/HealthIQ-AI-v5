---
work_id: ARCH-CONV-H
branch: feature/arch-conv-h-hba1c-compiled-why-authority
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# ARCH-CONV-H — HbA1c Compiled-WHY Authority

## Objective

Deliver governed compiled-WHY authority for:

```text
signal_hba1c_high::inv_hba1c_high_glycaemia
```

Retain one canonical HbA1c WHY authority, retire the genuinely competing HbA1c package frame from WHY ownership only, and preserve all separate non-competing HbA1c-percentage and glucose-dysregulation identities.

This sprint must not alter package-layer activation, PSI status, scoring policy, biomarker thresholds, frontend behaviour, or unrelated glucose/HbA1c signal families.

## Governing instructions

Follow:

- `AUTOMATION_BUS_SOP_v1.3.1.md`
- `KNOWLEDGE_BUS_SOP_v1.3.1.md`
- `KNOWLEDGE_BUS_PASS3_PROMOTION_PROTOCOL_v1.1.md` only as the current draft companion governance where relevant
- accepted ADR-RT-001, ADR-RT-002, ADR-RT-003 and ADR-RT-004
- the current merged repository and latest Build Deliverables Register

Do not rely on conversational summaries where repository evidence differs.

## Required repository baseline

Before any implementation work:

1. Confirm the current branch is exactly:

```text
feature/arch-conv-h-hba1c-compiled-why-authority
```

2. Confirm the branch starts from current clean `main` and report:

```powershell
git branch --show-current
git status --short
git rev-parse HEAD
git rev-parse main
git rev-parse origin/main
```

3. Confirm local `main == origin/main` before branch creation or sprint start.

4. Read the current authoritative files in full before proposing changes.

## Stage 1A — Authority preflight

Verify and cite the exact current repository paths and line numbers for all of the following:

### Canonical research authority

The canonical investigation spec for:

```text
spec_id: inv_hba1c_high_glycaemia
signal_id: signal_hba1c_high
```

Read and extract the repository-backed content needed to confirm:

- activation conditions;
- hypotheses and ranking;
- contradictions;
- confirmatory tests;
- override or escalation rules;
- evidence;
- narrative fields relevant to compiled WHY;
- the governed diabetes-range threshold already present in source research;
- any metabolic-context override involving triglyceride/HDL evidence.

### Current package and identity estate

Identify every package and authority row associated with:

```text
signal_hba1c_high
```

For each, record:

- package ID;
- activation key;
- source/provenance;
- runtime reachability;
- package activation status;
- PSI status;
- current legacy or compiled WHY ownership status.

Explicitly verify the expected collision shape:

- canonical retained frame:
  `signal_hba1c_high::inv_hba1c_high_glycaemia`
- genuine competing WHY frame:
  `pkg_kb52c_hba1c_high_diabetes_range_hyperglycemia`

Do not assume this shape if the merged repository differs.

### Adjacent identities that must remain separate

Inspect and classify all relevant entries for:

```text
signal_hba1c_pct_high
signal_glucose_dysregulation_hba1c_context
```

Confirm whether they are separate signal families or activation-frame identities and prove they do not compete for `signal_hba1c_high` WHY ownership.

No alias, identity merge, retirement, suppression or authority change is permitted for these adjacent identities in this sprint.

### Current WHY runtime path

Read and cite:

- the existing HbA1c legacy hypothesis asset;
- root-cause registry or selector entries;
- compiled-WHY authority register;
- compiled-WHY loader/compiler;
- collision and exclusivity governance;
- DTO/report projection paths carrying `why_role` or equivalent authority metadata;
- existing HbA1c and compiled-WHY tests.

Confirm that no compiled artefact or active compiled-WHY register row already exists for the canonical activation key.

## Stage 1B — Reality check

Before authoring any code or artefact change, answer:

> Does the current merged baseline still lack compiled-WHY authority for `signal_hba1c_high::inv_hba1c_high_glycaemia`, while a legacy HbA1c WHY path remains active or eligible?

If NO, STOP and report a no-op or re-scope condition.

## Stage 1C — Intelligence preflight

Identify the exact Intelligence Core surface affected by this sprint, including:

- compiled-WHY artefact generation or authored compiled artefact path;
- compiled-WHY authority register;
- legacy root-cause ownership/selector path;
- runtime compiler/loader only if an existing mechanism must be reused;
- output-authority and report projection tests;
- architecture validation gate and authority-count expectations.

No new compiler mechanism may be introduced unless current repository evidence proves the existing mechanism cannot represent the approved HbA1c contract. If that occurs, STOP before implementation.

## Phase 0 — Mandatory Gate 1 / Gate 2 STOP

Phase 0 is evidence and decision recording only. Do not create the compiled artefact, alter authority registers, retire legacy ownership, or change runtime behaviour before Gate 2 is recorded.

### Phase 0 deliverables

Create a concise repository-grounded medical and authority review pack containing:

1. Canonical source mapping.
2. Package collision and ownership table.
3. Adjacent identity exclusion table.
4. Proposed compiled-WHY content.
5. Proposed retained and retired authority rows.
6. Prohibited claims.
7. Expected runtime and test delta.

The pack must preserve source terminology and must not introduce medical meaning absent from the canonical investigation spec.

### Proposed medical boundary for Gate 1 review

Submit the following proposed boundary to the Head of Medical Research for explicit adjudication:

- HbA1c represents sustained glycaemic exposure over the preceding period, not an independently proven cause of diabetes-related pathology.
- The compiled WHY may identify a persistent hyperglycaemia / glycaemic-exposure pattern supported by the canonical source.
- Diabetes-range escalation may be included only using the governed source threshold and cautious wording.
- A single HbA1c result must not be presented as an unqualified diagnosis where the source or runtime context requires confirmation, repeat testing, symptoms, or clinical assessment.
- Triglyceride/HDL or metabolic-pattern evidence may modify context only to the extent explicitly authorised by the canonical research.
- No treatment recommendation, medication instruction, complication diagnosis, chronicity claim beyond the marker's supported interpretation, or unsupported causal claim may be introduced.
- `signal_hba1c_pct_high` and `signal_glucose_dysregulation_hba1c_context` remain separate and non-owning for this authority decision.

### Proposed authority disposition for Gate 1 review

Submit:

```text
RETAIN / COMPILE:
signal_hba1c_high::inv_hba1c_high_glycaemia

RETIRE FOR WHY OWNERSHIP ONLY:
the confirmed competing activation key hosted by
pkg_kb52c_hba1c_high_diabetes_range_hyperglycemia
```

Retirement is limited to WHY ownership. Do not delete the package or alter its package-layer, PSI, validation or historical status unless separately authorised.

### Gate 1 STOP

STOP and obtain a repository-recorded Head of Medical Research decision.

Required decision values:

```text
APPROVED
APPROVED_WITH_NARROWING
BLOCKED
```

The decision record must state:

- approved `why_role`;
- approved summary/claim boundary;
- approved diabetes-range escalation wording;
- approved use or exclusion of TG/HDL metabolic context;
- prohibited claims;
- retained activation key;
- retired competing WHY activation key.

Do not proceed on verbal or conversational approval alone.

### Gate 2 STOP

After Gate 1 approval, STOP again and obtain Anthony's explicit repository-recorded production ratification.

Required decision values:

```text
APPROVED
BLOCKED
```

No implementation may begin until both Gate 1 and Gate 2 records exist and match the proposed activation keys and medical boundary.

## Implementation scope after Gate 2

Implement only the ratified decision.

Expected scope:

1. Create or update the governed compiled-WHY artefact for:

```text
signal_hba1c_high::inv_hba1c_high_glycaemia
```

2. Add one `COMPILED_ACTIVE` authority row for the canonical activation key.

3. Add one `LEGACY_RETIRED` row for the confirmed competing HbA1c WHY activation key.

4. Preserve the existing legacy HbA1c asset only where required for historical compatibility or non-owning comparison; prevent it from remaining an active competing WHY owner.

5. Reuse the existing compiled-WHY loader, compiler, register and exclusivity mechanisms.

6. Preserve package-layer activation and PSI state for every affected package.

7. Preserve all non-competing identities and signal families.

## Explicit prohibitions

Do not:

- introduce a new signal ID, activation key format, alias or SSOT biomarker;
- merge `signal_hba1c_high` with `signal_hba1c_pct_high`;
- merge HbA1c with glucose-dysregulation context signals;
- change HbA1c scoring bands or reference-range policy;
- activate or deactivate packages outside WHY ownership;
- alter PSI opt-in or runtime PSI wiring;
- add frontend medical logic or copy;
- diagnose diabetes solely from one result unless the ratified wording explicitly permits the precise bounded statement;
- introduce treatment, medication, complication or prognosis claims;
- use triglyceride/HDL context beyond the ratified source-backed role;
- modify unrelated compiled-WHY frames;
- create a new generic compiler mechanism;
- delete historical packages or evidence assets.

## Required tests

At minimum, add or update tests proving:

### Authority and exclusivity

- canonical HbA1c activation key is `COMPILED_ACTIVE`;
- exactly one genuine competing HbA1c WHY owner becomes `LEGACY_RETIRED`;
- no duplicate active WHY authority remains for `signal_hba1c_high`;
- compiled-WHY authority counts change only by the expected delta;
- adjacent `signal_hba1c_pct_high` and glucose-dysregulation identities remain unchanged.

### Medical boundary

- approved base HbA1c explanation is emitted without unsupported diagnosis or causality;
- diabetes-range escalation occurs only at the ratified threshold and with ratified wording;
- below-threshold cases do not receive diabetes-range escalation;
- TG/HDL context is applied only if ratified conditions are satisfied;
- absent or incomplete supporting context fails closed;
- prohibited treatment, complication, unsupported chronicity and unqualified diagnostic wording is absent.

### Runtime preservation

- package-layer reachability and activation status are unchanged;
- PSI status is unchanged;
- no non-HbA1c compiled-WHY frame changes;
- report/DTO authority metadata remains structurally stable;
- existing ARCH-CONV-F and ARCH-CONV-G regression suites remain green;
- the compiled-WHY authority gate and full architecture validation gate pass.

Use existing project test patterns and canonical test modules. Do not create redundant test harnesses when current suites can be extended.

## STOP conditions during implementation

STOP immediately if:

- the canonical investigation spec differs materially from Phase 0 evidence;
- more than one genuine competing `signal_hba1c_high` WHY frame is found;
- the retained or retired activation key differs from the Gate records;
- adjacent identities are aliases or competing authorities rather than separate signals;
- the approved medical content cannot be represented by the existing compiled-WHY schema;
- implementation would require a new compiler mechanism, signal identity, alias, SSOT biomarker or scoring rule;
- package-layer activation or PSI status would need to change;
- a diabetes diagnosis, chronicity claim, treatment claim or metabolic causal claim would have to be inferred rather than sourced;
- unrelated compiled-WHY frames change;
- expected authority-count deltas do not match repository reality;
- baseline failures prevent attribution of sprint regressions.

Produce a blocker report rather than improvising.

## Verification requirements

Run and report:

1. Focused HbA1c compiled-WHY tests.
2. Compiled-WHY authority and collision tests.
3. Existing ARCH-CONV-F and ARCH-CONV-G regression suites.
4. Output-authority / report projection tests relevant to compiled WHY.
5. Canonical architecture validation gate.
6. Any current programme closure suite that protects compiled-WHY authority counts and legacy retirement.

Where broader tests fail, compare against clean `main` and prove whether failures are pre-existing. Do not claim PASS without attribution evidence.

## Post-implementation closure protocol

Before running Automation Bus finish, execute and report:

```powershell
git branch --show-current
git status --short
git log --oneline -n 5
git diff --name-only
git diff --cached --name-only
git stash list
```

Explicitly classify:

- tracked modified files;
- staged files;
- untracked files;
- tooling files;
- out-of-scope files;
- relevant stash entries.

Do not run finish unless the branch is clean, all changes are in scope, no tooling leakage exists, and no stash ambiguity remains.

Then run:

```powershell
python backend/scripts/run_work_package.py finish
```

After finish, follow the kernel status artefact policy in Automation Bus SOP v1.3.1 and re-confirm branch cleanliness.

## Independent audit requirements

After finish, Claude Code must independently review:

- Gate 1 and Gate 2 decision records;
- canonical source fidelity;
- compiled artefact content;
- authority register delta;
- retired legacy ownership;
- package and PSI non-change;
- adjacent identity non-change;
- prohibited-claim absence;
- focused and regression test results;
- Automation Bus gate evidence;
- repository diff and closure cleanliness.

The audit must explicitly state whether:

- deterministic behaviour is preserved;
- no unintended behavioural drift occurred;
- output structure is unchanged except for the authorised HbA1c WHY content;
- exactly one canonical HbA1c compiled authority is active;
- the competing WHY owner is retired only for WHY ownership;
- all separate HbA1c-percentage and glucose-dysregulation identities remain unchanged.

## Closure deliverables

Produce or update only the repository artefacts required by the established compiled-WHY sprint pattern, including:

- Phase 0 medical/authority review pack;
- Gate 1 decision record;
- Gate 2 ratification record;
- compiled-WHY artefact;
- authority-register update;
- implementation and verification report;
- focused tests and necessary regression updates;
- Build Deliverables Register entry;
- central carry-forward register only if this sprint creates a genuine new programme carry-forward.

The Build Deliverables Register entry must record the actual merge SHA after merge and publication.

## Success criteria

This sprint is complete only when:

- Gate 1 and Gate 2 are repository-recorded and aligned;
- `signal_hba1c_high::inv_hba1c_high_glycaemia` is the sole active compiled-WHY authority for the canonical HbA1c-high frame;
- the one confirmed competing HbA1c WHY owner is retired for WHY ownership only;
- medical wording remains within the ratified canonical source boundary;
- diabetes-range escalation is precise, cautious and threshold-governed;
- package-layer and PSI status are unchanged;
- adjacent HbA1c-percentage and glucose-dysregulation identities are unchanged;
- all focused and required regression gates pass;
- independent audit passes;
- the branch is closure-clean and ready for Head of Architecture review and Anthony's merge authority.
