---
work_id: ARCH-CONV-F
branch: feature/arch-conv-f-haematology-compiled-why
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# ARCH-CONV-F — Haematology Compiled-WHY Authority

## Governing authority

Implement the ratified ARCH-CONV-F medical and architectural decisions.

Gate references:

- Gate 1: `ARCH-CONV-F-GATE1-HMR-2026-08-01`
- Gate 2: `ARCH-CONV-F-GATE2-ANTHONY-2026-08-01`

Controlling design:

- `docs/architecture/ARCH-CONV-F_hardening_pack.md`

Governing SOPs:

- `AUTOMATION_BUS_SOP_v1.3.1.md`
- `KNOWLEDGE_BUS_SOP_v1.3.1.md`
- `KNOWLEDGE_BUS_PASS3_PROMOTION_PROTOCOL_v1.1.md`

Do not deviate from the ratified hardening pack. If repository reality conflicts with it, STOP and return for Claude Code hardening.

## Product outcome

Complete governed compiled-WHY authority for:

- `signal_ferritin_high`
- `signal_hemoglobin_low`

This sprint must:

1. compile the two canonical WHY artefacts;
2. activate them through the existing compiled-WHY authority path;
3. retire the three competing frames for WHY ownership only;
4. preserve existing package-layer and PSI status;
5. prove that ferritin never emits causal iron-overload or haemochromatosis authority;
6. preserve the separate unresolved haemoglobin oxygen-carrying PSI research requirement.

This sprint does not create new signal libraries or new medical research.

## Stage 0 — branch and baseline

Before implementation:

1. Confirm `main` is clean and synchronized with `origin/main`.
2. Create and switch to:

   `feature/arch-conv-f-haematology-compiled-why`

3. Confirm the branch matches the front matter.
4. Confirm no active Automation Bus work-package token conflicts with `ARCH-CONV-F`.
5. Confirm the baseline still lacks compiled-WHY authority rows and compiled artefacts for both canonical activation keys.
6. Confirm the three competing frames have not already been retired for WHY ownership.
7. Confirm the authoritative register and loader paths below are current and unique.

If the intended outcome is already delivered, partially delivered in a conflicting form, or controlled by a different authoritative path, STOP. Do not run a redundant sprint.

## Authoritative paths

The authoritative compiled-WHY register is:

- `knowledge_bus/governance/compiled_why_authority_register_v1.yaml`

The runtime compiled-WHY authority resolver is:

- `backend/core/knowledge/why_authority_v1.py`

The runtime consumer/compiler is:

- `backend/core/analytics/root_cause_compiler_v1.py`

The existing legacy target registry is:

- `backend/core/knowledge/root_cause_registry_v1.py`

Canonical research specifications:

- `knowledge_bus/research/investigation_specs/inv_ferritin_high_overload_v1.yaml`
- `knowledge_bus/research/investigation_specs/inv_hgb_low_anemia.yaml`

Additional governed ferritin corroborator research:

- `knowledge_bus/research/investigation_specs/multi_llm_research/Batch_4_Pass_3.json`
  - `inv_ferritin_high_iron_overload_context`
  - `inv_ferritin_high_inflammatory_hyperferritinemia`

Relevant packages:

- `knowledge_bus/packages/pkg_s24_ferritin_high_overload/`
- `knowledge_bus/packages/pkg_kb52c_ferritin_high_inflammatory_hyperferritinemia/`
- `knowledge_bus/packages/pkg_kb52c_ferritin_high_iron_overload_context/`
- `knowledge_bus/packages/pkg_s24_hgb_low_anemia/`
- `knowledge_bus/packages/pkg_kb52c_hgb_low_normocytic_underproduction_context/`

Read the actual contents of every source and authority file before changing anything.

## Ratified medical authority

### 1. Haemoglobin low

Canonical activation key:

`signal_hemoglobin_low::inv_hgb_low_anemia`

Implement:

- `why_role: causal`
- the causal scope is limited to anaemia / reduced oxygen-carrying capacity;
- MCV and RDW are non-owning morphology/context markers only;
- haemoglobin plus MCV/RDW must not independently establish an aetiology;
- no independent “underproduction” claim may be emitted.

Retain as canonical source:

- `pkg_s24_hgb_low_anemia`

Retire for WHY ownership only:

- `pkg_kb52c_hgb_low_normocytic_underproduction_context`

Preserve valid normocytic morphology content as subordinate context within the canonical haemoglobin frame.

Retain the existing haemoglobin `<80 g/L` override only as an `at_risk` concern escalation.

Presentation safeguards:

- not a universal definition of severe anaemia;
- not an automatic transfusion threshold;
- not a treatment recommendation.

Do not alter or claim to resolve the separate haemoglobin primary oxygen-carrying PSI research requirement.

### 2. Ferritin high

Canonical activation key:

`signal_ferritin_high::inv_ferritin_high_overload`

Implement:

- `why_role: morphology_context`
- flat and non-causal under every data state;
- no conditional causal branch;
- no haemochromatosis diagnosis;
- no causal systemic iron-overload claim.

Context enrichment only:

- elevated CRP may support reactive/inflammatory-context wording;
- elevated ALT may support hepatic/metabolic-context wording;
- elevated serum iron is weak contextual corroboration only and is insufficient alone for overload attribution;
- `transferrin_saturation` may provide additional non-causal context enrichment only.

Transferrin saturation must not:

- upgrade the ferritin frame to causal;
- independently establish systemic iron overload;
- diagnose haemochromatosis;
- create a new independently owning transferrin frame;
- modify transferrin package or PSI authority.

When corroboration is absent, fail closed to a bare elevated-ferritin context finding with no attribution.

Retain the existing ferritin `>1000 µg/L` override only as an `at_risk` concern escalation.

Presentation safeguards:

- not a haemochromatosis diagnosis;
- not a causal iron-overload claim;
- concern escalation only.

Retain as canonical source:

- `pkg_s24_ferritin_high_overload`

Retire for WHY ownership only:

- `pkg_kb52c_ferritin_high_inflammatory_hyperferritinemia`
- `pkg_kb52c_ferritin_high_iron_overload_context`

Do not delete either package or revoke existing PSI activation.

## Required implementation boundary

Expected changes:

- `knowledge_bus/governance/compiled_why_authority_register_v1.yaml`
  - add two `COMPILED_ACTIVE` canonical rows;
  - add three `LEGACY_RETIRED` competing-frame rows.
- `backend/core/knowledge/why_authority_v1.py`
  - add the two signal IDs to the existing compiled-WHY cohort using the established mechanism.
- `knowledge_bus/compiled/hypotheses/`
  - add one ferritin compiled hypothesis artefact;
  - add one haemoglobin compiled hypothesis artefact.
- `knowledge_bus/governance/root_cause_authority_register_v1.yaml`
  - bookkeeping consistency only, if required by established precedent.
- focused tests and committed evidence/governance documents.

No change is expected in:

- `backend/core/knowledge/root_cause_registry_v1.py`
- `backend/core/analytics/root_cause_compiler_v1.py`

A change to either file requires a STOP unless it is proven to be a pre-existing, governed mechanism reuse that was omitted from the hardening boundary. Do not introduce a new compiler mechanism.

Do not change:

- any `signal_library.yaml`;
- any package activation or eligibility logic;
- PSI opt-in state;
- SSOT biomarker definitions;
- derived-metric registries;
- frontend files;
- unrelated compiled-WHY authority.

## Explicit exclusions

Do not modify or compile authority for:

- `signal_ferritin_low`
- `signal_transferrin_high`
- `signal_transferrin_low`
- `signal_iron_deficiency_context`
- `signal_iron_overload_context` as an independently owning frame
- `signal_oxygen_transport_capacity`
- `signal_urate_high`
- `signal_hba1c_high`
- any ALT signal
- completed thyroid, lipid, creatinine, urea, ALP or GGT authority

Do not introduce a new biomarker, threshold, ranking, diagnosis, alias or activation-key convention.

## Governance records

Create or update the ARCH-CONV-F governance records so they accurately record:

- Gate 1 reference: `ARCH-CONV-F-GATE1-HMR-2026-08-01`
- Gate 2 reference: `ARCH-CONV-F-GATE2-ANTHONY-2026-08-01`
- exact canonical activation keys;
- ratified WHY roles;
- override presentation restrictions;
- competing-frame retirement for WHY ownership only;
- unchanged package and PSI status;
- unchanged separate haemoglobin oxygen-carrying PSI research gap.

Do not forge any additional human or medical approval.

## Required tests

Prove all of the following:

1. `signal_hemoglobin_low::inv_hgb_low_anemia` resolves through compiled authority.
2. Haemoglobin emits only the governed anaemia/reduced oxygen-carrying-capacity finding.
3. MCV and RDW remain subordinate context and cannot independently emit an aetiology.
4. The normocytic-underproduction competitor resolves to `skip` for WHY ownership.
5. `signal_ferritin_high::inv_ferritin_high_overload` resolves through compiled authority.
6. Ferritin remains `morphology_context` under every tested input combination.
7. Normal CRP never creates causal iron-overload authority.
8. Elevated CRP produces reactive/inflammatory context only.
9. Elevated ALT may enrich hepatic/metabolic context only.
10. Serum iron alone never produces iron-overload attribution.
11. Transferrin saturation may enrich context but never upgrade authority to causal.
12. Missing corroborators fail closed to bare ferritin-elevation wording.
13. Ferritin `>1000 µg/L` produces concern escalation only.
14. Haemoglobin `<80 g/L` produces concern escalation only.
15. No haemochromatosis diagnosis, transfusion recommendation or treatment recommendation is emitted.
16. All three competing kb52c frames resolve to `skip` for WHY ownership.
17. No signal-library, package activation or PSI behaviour changes.
18. No raw Pass 3 or investigation-spec file is read at runtime.
19. No unrelated compiled-WHY authority changes.
20. Deterministic repeatability.
21. The full compiled-WHY authority validator passes.
22. Package validators for all five affected packages pass.
23. Existing compiled-WHY regression suites for thyroid, lipid, renal and ALP/GGT remain passing.
24. Full relevant test modules must be run; do not cite only selected nodes where a complete module is available.

Record exact before/after counts for:

- `COMPILED_ACTIVE` rows;
- `LEGACY_RETIRED` rows;
- loaded compiled frames;
- affected signal families.

Expected register delta:

- `+2 COMPILED_ACTIVE`
- `+3 LEGACY_RETIRED`

Any different delta requires explanation and a STOP before finish.

## Evidence requirements

Commit an implementation evidence report containing:

- baseline proof;
- exact authority and loader paths;
- source-to-runtime rule mapping;
- exact files changed;
- before/after register counts;
- source and output hashes;
- all test commands and complete outputs;
- validator outputs;
- deterministic repeatability proof;
- proof that no runtime research-file read was introduced;
- proof that no signal-library, package activation or PSI state changed;
- proof that no new medical rule or threshold was invented;
- confirmation that the separate haemoglobin oxygen-carrying PSI research gap remains open;
- known unrelated baseline failures, with clean-main comparison where needed.

Do not omit failing tests from evidence. Any new sprint-attributable failure blocks completion.

## Mandatory STOP conditions

STOP and return to Claude Code hardening if:

- ferritin can emit a causal claim in any data state;
- transferrin saturation requires new SSOT, derived-metric or package work;
- implementation requires a new threshold, ranking, alias or activation-key convention;
- haemoglobin PSI research becomes entangled with compiled-WHY work;
- completed authority outside the two target signals changes;
- `root_cause_compiler_v1.py` requires a new mechanism;
- a package or PSI activation would need to be deleted or revoked;
- the ratified medical disposition cannot be represented exactly;
- the register delta differs from `+2 COMPILED_ACTIVE / +3 LEGACY_RETIRED`;
- an authority source or loader differs from the paths declared above;
- the baseline no longer exhibits the intended gap;
- any new sprint-attributable test failure remains.

Retrospective ratification is forbidden. STOP before implementing any deviation.

## Automation Bus lifecycle

This is an SOP-governed work package.

After the prompt has been hardened by Claude Code and `latest_prompt_hardening.json` reports `HARDENED`, run:

```powershell
python backend/scripts/run_work_package.py start
```

Do not implement unless kernel start succeeds for `ARCH-CONV-F`.

Use the TWO_PHASE_START_FINISH execution model.

After implementation and committed evidence, perform the mandatory Post-Implementation Closure Protocol from Automation Bus SOP v1.3.1 before running finish.

Then run:

```powershell
python backend/scripts/run_work_package.py finish
```

If finish leaves only the kernel-owned `automation_bus/latest_cursor_status.json` dirty and it records `COMPLETE` for `ARCH-CONV-F`, commit it exactly as:

```text
chore(bus): ARCH-CONV-F kernel COMPLETE status
```

Do not merge.

STOP after successful finish and closure-clean verification for independent Claude Code audit, GPT review and final human merge authority.
