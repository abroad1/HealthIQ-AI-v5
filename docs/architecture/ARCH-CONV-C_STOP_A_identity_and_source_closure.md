# ARCH-CONV-C — STOP A Identity, Source, and Collision-Boundary Closure

**Work ID:** `ARCH-CONV-C`  
**Date (UTC):** 2026-07-30  
**Author role:** Cursor (`healthiq-core-engine`) — repository evidence only  
**Authority:** Automation Bus SOP v1.3.1; Knowledge Bus SOP v1.3.1; Pass 3
Promotion Protocol v1.1; `automation_bus/latest_cursor_prompt.md`  
**Status:** `STOP_A_APPROVED_BY_HEAD_OF_ARCHITECTURE`

> **STOP A approval (recorded 2026-07-30):** Head of Architecture approved this
> STOP A evidence in-session and authorised Phase 1 (Gate 1 medical-review-pack
> and decision-register finalisation) only. No formal approval reference string
> was supplied; the Head of Architecture may attach one to
> `head_of_architecture_stop_a_reference` in
> `docs/architecture/ARCH-CONV-C_medical_decision_register.yaml`. Approval does
> not authorise medical decisions, collision-policy population, compilation,
> runtime authority changes, legacy disconnection, Automation Bus finish, or
> Phase 2.

This record contains no medical approval, collision-policy adjudication, runtime
authorisation, compilation, authority registration, or legacy disconnection.

## Work-package state

| Field | Evidence |
|---|---|
| Branch | `feature/arch-conv-c-alp-ggt-why-authority` |
| Baseline | local `main == origin/main == cdc6cf3d463d50902a080b51136ef1a98b431f4a` before branch creation |
| Handoff commit | `0b3d10c` — hardened ARCH-CONV-C prompt and hardening record |
| Kernel authority | `automation_bus/state/work_package_active.json`: `ARCH-CONV-C`, matching branch |
| Kernel status | `IN_PROGRESS` |
| Stash | empty; no convenience stash created |
| Change boundary reached | Phase 0 evidence only |
| Medical/collision decisions | **None** |
| Runtime/compiled/authority changes | **None** |

## Stage 1A — authority preflight

### Embedded canonical identities

| Target | Embedded identity evidence | Canonical path | SHA-256 |
|---|---|---|---|
| ALP high | `spec_id: inv_alp_high_bone_biliary`; `signal_id: signal_alp_high` at lines 1-2 | `knowledge_bus/research/investigation_specs/inv_alp_high_bone_biliary.yaml` | `1a8e2da95d4aeae0505897da445709632f5ea4c39c34d4aaf906ef3462eb61ef` |
| GGT high | `spec_id: inv_ggt_high_hepatic`; `signal_id: signal_ggt_high` at lines 1-2 | `knowledge_bus/research/investigation_specs/inv_ggt_high_hepatic.yaml` | `3e2cc6cf074dcb73b825e9a97fe93b43c4f50dc874a0c85cbaa34b754d46c8a1` |

Confirmed activation keys:

```text
signal_alp_high::inv_alp_high_bone_biliary
signal_ggt_high::inv_ggt_high_hepatic
```

No identity was inferred from a filename or package name.

### Current legacy WHY authority

| Signal | Registry | Loader | Legacy asset |
|---|---|---|---|
| `signal_alp_high` | `backend/core/knowledge/root_cause_registry_v1.py:75` | `backend/core/knowledge/load_root_cause_hypotheses.py:159-160` | `knowledge_bus/root_cause/hypotheses/alp_high_hypotheses_v1.yaml` |
| `signal_ggt_high` | `backend/core/knowledge/root_cause_registry_v1.py:67` | `backend/core/knowledge/load_root_cause_hypotheses.py:139-140` | `knowledge_bus/root_cause/hypotheses/ggt_high_hypotheses_v1.yaml` |

`backend/core/knowledge/why_authority_v1.py:22-44` excludes both families from
the compiled cohort; lines 154-155 preserve legacy behavior out of cohort.

### Current compiled authority

No `signal_alp_high` or `signal_ggt_high` row exists in:

- `knowledge_bus/governance/compiled_why_authority_register_v1.yaml`
- `knowledge_bus/governance/root_cause_authority_register_v1.yaml`
- `knowledge_bus/compiled/estate_index_v1.yaml`

No registered compiled ALP/GGT hypothesis artefact or manifest exists. Therefore
both canonical targets remain on active legacy WHY authority and no ALP/GGT
compiled WHY frame is active.

### Signal-layer frame reality

The current `SignalRegistry` deterministically loads:

```text
signal_alp_high::inv_alp_high_bone_biliary
signal_alp_high::inv_alp_high_cholestatic_pattern
signal_ggt_high::inv_ggt_high_hepatic
signal_ggt_high::inv_ggt_high_hepatobiliary_cholestatic_context
signal_ggt_high::inv_ggt_high_alcohol_or_enzyme_induction_context
```

The two S24 frames are `SOURCE_DOCUMENT_DERIVED`. The translated Pass 3 package
frames are present but carry `BLOCKED` provenance. Signal presence does not grant
causal-WHY eligibility.

### Runtime consumer path

The current path is:

1. package `signal_library.yaml` files are loaded by
   `backend/core/analytics/signal_evaluator.py::SignalRegistry`;
2. embedded/package source identity is resolved into activation keys;
3. post-evaluation signal collision enforcement is handled by
   `backend/core/analytics/signal_authority_collision_resolver.py`;
4. root-cause compilation uses
   `backend/core/analytics/root_cause_compiler_v1.py` and the family registry;
5. WHY selection uses `backend/core/knowledge/why_authority_v1.py`;
6. report output passes through
   `backend/core/analytics/report_compiler_v1.py`,
   `backend/core/contracts/clinician_report_v1.py`, and
   `backend/core/dto/builders.py`.

The compiled role path already requires explicit `causal` or
`morphology_context`, but ALP/GGT do not enter it until later ratified authority
integration.

## Candidate and parallel-source closure

### ALP high

Canonical target:

```text
signal_alp_high::inv_alp_high_bone_biliary
```

Candidate decomposition:

| Identity | Source | Current state |
|---|---|---|
| `signal_alp_high::inv_alp_high_cholestatic_pattern` | v3 record in `Batch_5_Pass_3.json`; translated package `pkg_kb52c_alp_high_cholestatic_pattern` | Signal frame loaded, provenance blocked; no compiled WHY |
| `signal_alp_high::inv_alp_high_high_bone_turnover_pattern` | v3 record in `Batch_5_Pass_3.json` | No separate runtime package found; no compiled WHY |

The Pass 3 coverage audit at lines 439-457 reports four frames under
`signal_alp_high`, but two are `inv_alp_low_*`. They are excluded ALP-low
directional frames, not ALP-high candidates.

ALP source-boundary findings:

- The canonical target explicitly combines liver and bone interpretation.
- High GGT is the source differential; normal/absent GGT leaves bone and other
  non-hepatic explanations unresolved.
- High bilirubin strengthens cholestatic context.
- Calcium supports bone context; Pass 3 additionally identifies phosphate,
  vitamin D, PTH, history and isoenzyme evidence gaps.
- The canonical source records pregnancy and adolescence as confounders.
- The legacy first hypothesis can present hepatobiliary/cholestatic context from
  an ALP-high signal without a ratified high-GGT eligibility gate.

### GGT high

Canonical target:

```text
signal_ggt_high::inv_ggt_high_hepatic
```

Candidate decomposition:

| Identity | Source | Current state |
|---|---|---|
| `signal_ggt_high::inv_ggt_high_hepatobiliary_cholestatic_context` | v3 record in `Batch_6_Pass_3.json`; translated package and staged PSI | Signal frame loaded, provenance blocked; no compiled WHY |
| `signal_ggt_high::inv_ggt_high_alcohol_or_enzyme_induction_context` | v3 record in `Batch_6_Pass_3.json`; translated package and staged PSI | Signal frame loaded, provenance blocked; no compiled WHY |

GGT source-boundary findings:

- The canonical source combines hepatobiliary, alcohol, NAFLD, oxidative-stress,
  and enzyme-induction implications.
- High ALP is the canonical escalation companion marker.
- ALT and bilirubin appear only as context markers; their excluded authority
  families are not granted WHY authority by this package.
- MCV is non-specific and cannot establish alcohol exposure.
- Alcohol history and medication exposure are not structured runtime inputs.
- Pass 3 explicitly says isolated GGT must not infer alcohol exposure or
  liver-disease severity.
- The legacy asset does not preserve hepatobiliary versus alcohol/medicine versus
  metabolic context as governed causal/context roles.

## Stage 1B — reality check

| Required baseline fact | Result |
|---|---|
| ALP-high remains legacy WHY | CONFIRMED |
| GGT-high remains legacy WHY | CONFIRMED |
| No ALP/GGT compiled WHY active | CONFIRMED |
| `liver_injury_axis` remains placeholder | CONFIRMED |
| ALP biliary-versus-bone interpretation unresolved | CONFIRMED |
| GGT hepatobiliary-versus-alcohol/enzyme-induction interpretation unresolved | CONFIRMED |
| ALT, AST, bilirubin/hyperbilirubinemia and ALP-low remain excluded | CONFIRMED |
| Sprint is not a no-op | CONFIRMED |

## `liver_injury_axis` reconstruction

Current fields from
`knowledge_bus/governance/signal_authority_collision_model_v1.yaml:110-122`:

| Field | Current value |
|---|---|
| `authority_group_id` | `liver_injury_axis` |
| `biological_axis` | `hepatocellular_injury` |
| `status` | `placeholder_not_adjudicated` |
| `primary_signal_family` | null |
| `supporting_signal_families` | `[]` |
| `no_duplicate_user_facing_signal` | null |
| `suppress_supporting_when_primary_present` | null |
| `consolidate_into_shared_interpretation` | null |
| `allow_parallel_if_distinct_risk_layer` | null |
| `runtime_action` | `none_governance_only` |
| `requires_runtime_support` | false |
| notes | ALT / AST / GGT / bilirubin placeholder; ALP omitted |

The collision resolver loads the governance model but only enforces adjudicated
groups. No current liver-axis policy selects ALP or GGT.

### Questions requiring medical/collision adjudication

1. Can ALP or GGT ever be primary authority?
2. Must either remain supporting or context-only?
3. Is ALP+GGT concordance required before hepatobiliary/cholestatic causality?
4. What deterministic action applies when ALP is high and GGT is normal?
5. What deterministic action applies when GGT is high and ALP is normal?
6. How do bilirubin, ALT and MCV alter context without acquiring authority?
7. How are bone-turnover, alcohol, medicine induction, and metabolic context
   represented without unsupported causality?
8. When are parallel findings allowed, consolidated, suppressed, or refused?
9. Does the axis label need narrowing or renaming to cover cholestatic and
   non-hepatic ALP boundaries?
10. How can future ALT and bilirubin packages join without being pre-empted?
11. Which explicit policy/precondition fields eliminate filename, package,
    lexical, filesystem and load-order selection?

No answer is supplied by Cursor.

## Stage 1C — affected surfaces

### Read and potentially affected after ratification

- canonical ALP/GGT research specs and Pass 3 candidate records;
- S24 and KB52C packages and staged GGT PSI views;
- legacy ALP/GGT WHY assets and loaders;
- root-cause registry and compiled WHY authority register;
- compiled hypothesis artefacts, manifests and estate index;
- `liver_injury_axis` collision model and resolver;
- signal evaluator and activation identity;
- root-cause compiler, clinician report contract/compiler and DTO output;
- liver card evidence/scoring regression surfaces;
- authority, role, collision, duplicate-key, liver, alias and unrelated-domain
  regression tests.

### Expected later output changes, only after all gates

- ALP/GGT may move from family-level legacy WHY to specifically ratified
  activation-key authority.
- Only a ratified causal frame may emit causal WHY.
- Context-only, rejected and deferred candidates must remain non-causal or
  unreachable.
- A ratified `liver_injury_axis` may explicitly govern concordant/discordant
  ALP/GGT selection.

### Outputs that must remain unchanged

- ALT and `signal_hepatic_alt_context` identities and WHY behavior;
- AST behavior and absence of invented WHY;
- bilirubin/hyperbilirubinemia identity and legacy behavior;
- ALP-low signal and WHY behavior;
- existing liver scoring/card behavior unless later explicitly ratified;
- thyroid, lipid, renal, iron/haematology, metabolic/systemic and other domains;
- report shape and frontend render-only behavior.

## Evidence-gap classification

| Gap | Classification | Effect |
|---|---|---|
| Combined ALP bone/biliary canonical frame | `MEDICAL_DISPOSITION_REQUIRED` | Gate 1 must decide narrow/decompose/cause/context/defer |
| ALP Pass 3 high/low grouping in audit | `GOVERNANCE_AUDIT_GROUPING_GAP` | Partition by direction; do not pull ALP-low into scope |
| ALP high-bone-turnover candidate lacks runtime package | `PASS3_UNPACKAGED_CANDIDATE` | Do not infer runtime or compiled authority |
| Missing ALP source-attribution inputs | `FAIL_CLOSED_POLICY_REQUIRED` | No silent hepatic or bone diagnosis |
| GGT mixed canonical implications | `MEDICAL_DISPOSITION_REQUIRED` | Separate hepatobiliary from exposure/metabolic context |
| Alcohol/medication history absent from runtime inputs | `STRUCTURED_CONTEXT_GAP` | No attributive alcohol/medicine causal claim |
| ALT/bilirubin appear as supporting markers but are excluded authorities | `CROSS_SIGNAL_BOUNDARY` | Context cannot grant or displace authority |
| `liver_injury_axis` omits ALP and has all policy fields null | `COLLISION_POLICY_UNADJUDICATED` | No runtime enforcement until ratified |
| Legacy family loaders serve multiple activation keys | `DUPLICATE_MEDICAL_AUTHORITY_RISK` | Later migration must be activation-key explicit |

## STOP A checklist

| Requirement | Result |
|---|---|
| Embedded ALP/GGT identities confirmed | PASS |
| Canonical, Pass 3, package and legacy sources distinguished | PASS |
| Active legacy WHY authority identified | PASS |
| Compiled authority state identified | PASS — none |
| Live signal activation keys enumerated | PASS |
| ALP-high separated from ALP-low audit rows | PASS |
| ALP bone-versus-biliary risk recorded | PASS |
| GGT hepatobiliary-versus-context risk recorded | PASS |
| `liver_injury_axis` placeholder and fields reconstructed | PASS |
| Medical/collision-policy questions enumerated | PASS |
| ALT/AST/bilirubin/ALP-low exclusions recorded | PASS |
| Medical approval made by Cursor | **NO** |
| Collision policy populated by Cursor | **NO** |
| Runtime/compiled/legacy authority changed | **NO** |

## STOP A verdict

```text
STOP A APPROVED BY HEAD OF ARCHITECTURE — PHASE 1 (GATE 1 PACK FINALISATION) AUTHORISED
```

Approval authorises finalisation of the Gate 1 medical-review pack and decision
register for Head of Medical Research only. It does not authorise Cursor to make
medical decisions, populate collision policy, compile frames, register or modify
runtime authority, disconnect legacy authority, run Automation Bus finish, or
proceed to Phase 2.
