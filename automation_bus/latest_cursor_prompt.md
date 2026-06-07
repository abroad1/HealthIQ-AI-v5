---
work_id: BATCH2-EGFR-AUTHORITY-1_renal_signal_authority_and_reusable_collision_model
branch: work/BATCH2-EGFR-AUTHORITY-1-renal-signal-authority-and-reusable-collision-model
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# BATCH2-EGFR-AUTHORITY-1 — Renal Signal Authority and Reusable Collision Model

## Purpose

Resolve the Batch 2 eGFR blocker and create a reusable signal-authority / anti-double-counting pattern for future overlapping biomarker families.

This sprint must address the two remaining Batch 2 eGFR packages:

```text
pkg_kb47_egfr_low_chronic_kidney_function_reduction
pkg_kb47_egfr_low_hemodynamic_filtration_drop
````

The immediate problem:

```text
eGFR-low overlaps with existing creatinine-high / eGFR escalation reasoning.
```

The architectural opportunity:

```text
Create a reusable model for cases where multiple biomarkers describe overlapping biology and must not be double-counted.
```

Do not build a one-off renal hack.

---

## Strategic framing

HealthIQ AI will repeatedly face overlapping biomarker families:

```text
- creatinine / eGFR / uACR / cystatin C
- ALT / AST / GGT / bilirubin
- HbA1c / glucose / fasting insulin / HOMA-IR
- ferritin / CRP / inflammation
- testosterone / SHBG / FAI / free testosterone
- TSH / FT3 / FT4
```

This sprint must produce reusable governance and, if safe, minimal runtime support for:

```text
signal authority groups
primary vs supporting signal roles
anti-double-counting rules
collision resolution metadata
runtime-safe suppression or consolidation behaviour
```

The eGFR packages are the first implementation case.

---

## Baseline requirement

Start from clean `main`.

Expected prior completed work:

```text
BATCH2-REMAINING-BLOCKERS-1 merged
BATCH2-THYROID-GATE-1 merged
BATCH2-ACTIVATION-1 merged
BATCH2-PROMOTE-1 merged
BATCH2-CLOSURE-1 merged
PASS3-BATCH2-FRAME-INDEX-1 merged
PASS3-BATCH2-FRAME-INDEX-2 merged
ARCH-SENTINEL-1 merged
CI-ARCH-GATE-1 / CI-ARCH-GATE-1A merged
```

Before starting, run and report:

```powershell
git branch --show-current
git status --short
git log --oneline -n 12
git rev-parse HEAD
git rev-parse origin/main
```

STOP if:

```text
- current branch is not main
- local main does not equal origin/main
- working tree is not clean
- medical_frame_identity_index_v1.yaml is missing
- batch2_remainder_resolution_register_v1.yaml is missing
- eGFR packages cannot be found
- creatinine authority/frame entries cannot be found
```

---

## Required inputs

Read before implementation:

```text
knowledge_bus/governance/batch2_remainder_resolution_register_v1.yaml
knowledge_bus/governance/medical_frame_identity_index_v1.yaml
knowledge_bus/governance/batch2_final_promotion_decision_register_v1.yaml
knowledge_bus/governance/batch2_promote_1_execution_register_v1.yaml
knowledge_bus/governance/batch2_runtime_activation_execution_register_v1.yaml
docs/audit-papers/BATCH2-REMAINDER-RESOLUTION-1_remaining_batch2_package_resolution_investigation.md
docs/sprints/launch_core_carry_forward_register.md
```

Inspect relevant renal packages / governance:

```text
knowledge_bus/packages/pkg_kb47_egfr_low_chronic_kidney_function_reduction/
knowledge_bus/packages/pkg_kb47_egfr_low_hemodynamic_filtration_drop/
knowledge_bus/packages/*creatinine*
knowledge_bus/packages/*renal*
```

Inspect runtime and governance mechanisms:

```text
backend/core/analytics/signal_evaluator.py
SignalRegistry / package registry loader
domain score / report assembly logic if relevant
existing signal suppression / collision / authority handling if any
backend/tests/regression/
```

---

## In-scope packages

```text
pkg_kb47_egfr_low_chronic_kidney_function_reduction
pkg_kb47_egfr_low_hemodynamic_filtration_drop
```

Also inspect, but do not modify unless required and safe:

```text
existing creatinine-high packages / frames
existing renal-filtration frames
existing eGFR escalation frames under creatinine
```

---

## Required architectural output

Create a reusable governance model for overlapping signal authority.

Preferred artefact:

```text
knowledge_bus/governance/signal_authority_collision_model_v1.yaml
```

It must be non-runtime by default unless explicitly wired later:

```yaml
runtime_consumed: false
```

It should support reusable concepts such as:

```yaml
authority_group_id:
biological_axis:
primary_signal_family:
supporting_signal_families:
collision_policy:
  no_duplicate_user_facing_signal:
  suppress_supporting_when_primary_present:
  consolidate_into_shared_interpretation:
  allow_parallel_if_distinct_risk_layer:
runtime_action:
  none_governance_only | suppress | consolidate | annotate
requires_runtime_support:
notes:
```

This model must be designed so future marker families can reuse it.

---

## Required eGFR authority decision

Answer explicitly:

```text
1. Is eGFR-low its own signal family?
2. Is eGFR-low stronger renal-filtration evidence than creatinine-high?
3. Should creatinine-high remain active as a separate signal?
4. Should eGFR-low suppress creatinine-high filtration framing when both are present?
5. Can creatinine still contribute as supporting evidence?
6. Does potassium / acute risk remain a separate complication layer?
7. Can the two Batch 2 eGFR packages be activated safely now?
8. If not, exactly what is missing?
```

Preferred architectural decision unless evidence proves otherwise:

```text
eGFR-low should be the primary renal-filtration authority when available.
Creatinine-high can remain relevant as supporting evidence or a separate biochemical abnormality.
The system must avoid presenting low eGFR + high creatinine as two independent renal-filtration problems.
```

---

## Required reusable implementation principle

If runtime implementation is needed, implement the smallest reusable mechanism possible.

Do not hardcode “eGFR vs creatinine” inside ad hoc logic.

Prefer a reusable declarative pattern, for example:

```yaml
authority_resolution:
  authority_group_id: renal_filtration_axis
  primary_when_present: signal_egfr_low
  supporting_when_primary_present:
    - signal_creatinine_high
  duplicate_surface_policy: consolidate
```

If current runtime cannot safely consume this pattern without broader redesign, keep it governance-only and formally block eGFR activation.

---

## Phase 1 — Investigation and design

Before changing runtime or activation state, report:

```text
1. Current creatinine/eGFR frame relationships.
2. Current eGFR package state.
3. Whether any runtime anti-double-counting mechanism already exists.
4. Whether a reusable authority/collision model can be added safely.
5. Whether eGFR activation requires runtime support now.
6. Exact files proposed for change.
7. Rollback path.
```

STOP if:

```text
- creatinine/eGFR relationship cannot be resolved from existing evidence
- activating eGFR would create duplicate renal signalling
- runtime suppression/consolidation requires broad redesign
- rollback path cannot be defined
```

---

## Phase 2 — Implement reusable governance model

Create the reusable authority/collision governance artefact.

At minimum, include one renal authority group:

```yaml
authority_group_id: renal_filtration_axis
biological_axis: kidney_filtration_function
primary_signal_family: signal_egfr_low
supporting_signal_families:
  - signal_creatinine_high
collision_policy:
  no_duplicate_user_facing_signal: true
  allow_parallel_if_distinct_risk_layer: true
  distinct_risk_layers:
    - hyperkalemia_or_electrolyte_complication
    - acute_safety_escalation
runtime_action: governance_only_pending_runtime_support
requires_runtime_support: true
```

Also include placeholder examples for future reusable groups, but do not author fake medical decisions.

Acceptable placeholders:

```text
metabolic_glycaemic_axis
thyroid_axis
androgen_axis
liver_injury_axis
iron_inflammation_axis
```

These should be marked as:

```yaml
status: placeholder_not_adjudicated
```

---

## Phase 3 — Decide activation outcome

After the authority model is created, decide whether eGFR can activate now.

Allowed outcomes:

```text
A. Activate both eGFR packages with safe anti-double-counting support.
B. Governance-promote / authority-classify eGFR but keep runtime inactive pending reusable runtime support.
C. Keep eGFR formally blocked if authority remains unresolved.
```

Do not activate eGFR unless duplicate renal signalling is preventable now.

---

## Mandatory STOP gate before activation

If and only if activation is recommended, STOP and report:

```text
READY_FOR_HUMAN_STOP_GATE
```

STOP report must include:

```text
- eGFR authority decision
- anti-double-counting mechanism
- packages proposed for activation
- files changed
- tests added
- rollback path
- confirmation creatinine behaviour remains safe
```

Approval phrase:

```text
APPROVE BATCH2 EGFR AUTHORITY ACTIVATION
```

No runtime activation may occur without approval.

---

## Runtime activation after STOP approval

If approved, activate only:

```text
pkg_kb47_egfr_low_chronic_kidney_function_reduction
pkg_kb47_egfr_low_hemodynamic_filtration_drop
```

Do not activate or modify androgen packages.

Do not change unrelated renal packages unless necessary for the authority model and explicitly justified.

---

## Required tests

If runtime anti-double-counting / authority behaviour is implemented, add regression tests proving:

```text
1. eGFR-low can emit when activation criteria are met.
2. creatinine-high does not produce duplicate renal-filtration output when eGFR-low is primary.
3. creatinine can still contribute supporting evidence where appropriate.
4. distinct acute complication layers remain allowed where medically distinct.
5. unrelated signals are unaffected.
6. eGFR packages remain inactive if approval is not given.
```

If no runtime behaviour is changed, tests are required only for created validators / governance artefacts if applicable.

---

## Required artefacts

Create:

```text
knowledge_bus/governance/signal_authority_collision_model_v1.yaml
docs/audit-papers/BATCH2-EGFR-AUTHORITY-1_renal_signal_authority_and_reusable_collision_model.md
```

Create or update:

```text
knowledge_bus/governance/batch2_egfr_authority_execution_register_v1.yaml
docs/sprints/launch_core_carry_forward_register.md
```

Update only if activated or authority state changes:

```text
knowledge_bus/governance/medical_frame_identity_index_v1.yaml
knowledge_bus/packages/pkg_kb47_egfr_low_chronic_kidney_function_reduction/package_manifest.yaml
knowledge_bus/packages/pkg_kb47_egfr_low_hemodynamic_filtration_drop/package_manifest.yaml
```

Do not update:

```text
signal_library.yaml
research_brief.yaml
thresholds
clinical wording
frontend
SSOT
scoring
report compiler
```

unless there is an explicit STOP-level justification.

---

## Required report

Report must include:

```text
- executive verdict
- artefacts inspected
- creatinine/eGFR relationship summary
- reusable authority/collision model created
- renal authority decision
- eGFR activation decision
- anti-double-counting decision
- runtime behaviour changed, if any
- tests added / not added and why
- packages activated or kept inactive
- rollback path
- validation output pasted in full
- architecture gate output pasted in full
- carry-forward updates
- confirmation no unrelated package/frontend/SSOT/scoring changes
```

---

## Carry-forward handling

Update:

```text
docs/sprints/launch_core_carry_forward_register.md
```

Expected handling:

```text
CF-BATCH2-007
Resolve only if eGFR authority is either:
- safely activated with anti-double-counting support, or
- formally closed with a reusable authority blocker.

If runtime support remains needed, consolidate it under a reusable authority/collision runtime carry-forward rather than marker-specific fragmentation.
```

Possible new consolidated carry-forward only if genuinely needed:

```text
CF-AUTHORITY-RUNTIME-1 — implement runtime consumption of signal_authority_collision_model_v1.yaml
```

Do not create separate carry-forwards per eGFR package.

---

## Required validations

Run and paste actual output:

```powershell
python backend/scripts/run_architecture_validation_gate.py
python backend/scripts/validate_medical_frame_identity_index.py --index knowledge_bus/governance/medical_frame_identity_index_v1.yaml
python backend/scripts/validate_context_modifier_catalogue.py --catalogue knowledge_bus/governance/context_modifier_catalogue_draft_v1.yaml
```

Validate the two eGFR packages:

```powershell
python backend/scripts/validate_knowledge_package.py --package-dir <package_dir>
```

Run any new regression tests if runtime behaviour or governance validators are added.

---

## Runtime boundary

Runtime changes are allowed only if they are minimal, reusable, fail-safe, and directly support the authority/collision model.

Do not modify:

```text
frontend
SSOT
scoring thresholds
unit conversion
domain score assembly
report compiler
clinical wording
reference ranges
unrelated signal behaviour
```

STOP if implementation requires broad redesign.

---

## Success criteria

This sprint is complete only if:

```text
1. eGFR vs creatinine authority is explicitly decided
2. reusable authority/collision model exists
3. eGFR packages are either safely activated or formally blocked with exact reusable blocker
4. no duplicate renal dysfunction signalling is introduced
5. no clinical wording or thresholds change
6. no unrelated runtime behaviour changes
7. validators pass
8. architecture gate passes
9. rollback path is documented
10. future overlapping biomarker families can reuse the pattern
```

```
```
