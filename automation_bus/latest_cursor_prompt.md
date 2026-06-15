---
work_id: DHEA-DHEAS-CANONICALISATION-1_unit_aware_marker_identity_and_adrenal_androgen_resolution
branch: work/DHEA-DHEAS-CANONICALISATION-1-unit-aware-marker-identity-and-adrenal-androgen-resolution
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: BEHAVIOUR
---

# DHEA-DHEAS-CANONICALISATION-1 — Unit-Aware Marker Identity and Adrenal Androgen Resolution

## Purpose

Resolve the DHEA / DHEA-S identity ambiguity and introduce a reusable unit-aware biomarker canonicalisation rule for ambiguous lab markers.

This sprint must not treat DHEA as a one-off manual correction.

The immediate problem is:

```text
Some commercial lab panels may label a result as "DHEA" or "DHEA (Venous)" even when the unit, reference range and laboratory convention indicate the measured analyte is actually DHEA-S / DHEAS.
```

The wider architectural problem is:

```text
HealthIQ must not canonicalise ambiguous biomarkers by name alone.
```

The strategic goal is:

```text
Use marker name + unit + reference range + lab context + assay convention to resolve canonical biomarker identity safely.
```

---

## Strategic context

The Batch 2 medical research authority concluded:

```text
- DHEA high should not activate unless the source marker is clearly DHEA-S.
- DHEA low should not activate as a primary runtime signal.
- DHEA-S high may be clinically meaningful as an adrenal androgen excess context, but only if marker identity and runtime gates are explicit.
```

The human owner has also reviewed the commercial AB full-panel lab report and external lab references. The panel labels the result as:

```text
DHEA (Venous)
```

but reports it in:

```text
µmol/L
```

with a reference range consistent with DHEA-S / DHEAS reporting conventions.

This sprint must convert that evidence into repo-governed canonicalisation and package behaviour.

---

## Governance classification

This sprint is classified as:

```yaml
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: BEHAVIOUR
```

Rationale:

```text
- biomarker identity canonicalisation may change
- alias resolution may change
- parsed marker identity may change
- DHEA-S package activation may be considered
- signal package metadata may change
- endocrine interpretation is clinically sensitive
```

Required route:

```text
Cursor implementation
Claude hardening / audit
GPT architectural review
Human approval before merge
```

Do not merge without explicit human approval.

---

## Required branch

Work only on:

```text
work/DHEA-DHEAS-CANONICALISATION-1-unit-aware-marker-identity-and-adrenal-androgen-resolution
```

Do not work on `main`.

Do not merge.

---

## Non-negotiable constraints

This sprint must not:

```text
- silently map all DHEA labels to DHEA-S
- merge DHEA and DHEA-S into one ambiguous canonical identity
- activate DHEA low
- activate unsulfated DHEA high
- activate any adrenal androgen signal without deterministic gates
- change lab-derived reference range policy
- substitute global/default ranges where lab ranges exist
- change frontend rendering
- introduce frontend medical inference
- introduce fallback or dummy parsers
- introduce raw Pass 3 / investigation-spec runtime reads
- introduce LLM clinical reasoning into runtime canonicalisation or signal evaluation
- diagnose adrenal disease
- diagnose PCOS
- recommend treatment, supplements or hormones
```

This sprint must preserve original lab evidence.

For ambiguous markers, HealthIQ must retain:

```text
- original raw label
- original unit
- original reference range
- canonical identity decision
- identity confidence
- identity resolution reason
```

---

## Core design rule

Create or formalise this rule:

```text
Known ambiguous biomarkers must not be canonicalised by label alone.
```

Canonicalisation for ambiguous markers must consider:

```text
- raw reported name
- unit
- lab-provided reference range
- panel context
- known assay/reporting convention
- existing alias registry
- source lab metadata where available
```

For DHEA / DHEA-S specifically:

```text
If raw label is "DHEA", "DHEA (Venous)", "DHEA-S", "DHEAS", "Dehydroepiandrosterone sulphate" or similar
AND unit is µmol/L or umol/L
AND the reference range resembles DHEA-S / DHEAS reporting
THEN canonicalise as DHEA-S / DHEAS with documented identity reason.

If raw label is DHEA
AND unit/range are missing or ambiguous
THEN do not guess.
Return unresolved marker identity or fail-closed canonicalisation.

If true unsulfated DHEA appears with a unit/range consistent with unsulfated DHEA
THEN keep it separate from DHEA-S.
```

---

## Authoritative inputs

Read before implementation:

```text
docs/audit-papers/BATCH2-FULL-COVERAGE-ACTIVATION-1_activate_research_supported_thyroid_and_androgen_signals.md
docs/audit-papers/ARCH-COMPLETION-3_full_traceability_manifest_and_launch_estate_gate.md
docs/sprints/launch_core_carry_forward_register.md

knowledge_bus/research/medical_reviews/batch2_thyroid_androgen_context_authority_review_v1.md
knowledge_bus/governance/batch2_full_coverage_activation_execution_register_v1.yaml
knowledge_bus/governance/batch2_full_coverage_activation_readiness_register_v1.yaml
knowledge_bus/governance/day_one_full_traceability_manifest_v1.yaml
knowledge_bus/governance/day_one_launch_estate_gate_v1.yaml
knowledge_bus/governance/medical_frame_identity_index_v1.yaml
```

Inspect all biomarker identity and canonicalisation files, including but not limited to:

```text
backend/config/biomarker_alias_registry.yaml
backend/config/biomarker_catalogue.yaml
backend/config/derived_biomarkers.yaml
backend/ssot/**
backend/core/data/**
backend/core/parsing/**
backend/core/normalisation/**
backend/core/analytics/signal_evaluator.py
backend/core/analytics/runtime_context_evaluator.py
```

Inspect package files:

```text
knowledge_bus/packages/pkg_kb47_dhea_high_androgen_excess_context/
knowledge_bus/packages/pkg_kb47_dhea_low_adrenal_androgen_reduction/
```

Inspect any sample panel fixtures used for AB full-panel testing.

Locate the AB full-panel sample that contains:

```text
DHEA (Venous)
unit: µmol/L / umol/L
reference range similar to 0.94 - 15.44
```

If the sample cannot be found, report that as an evidence gap.

---

## Authority preflight

Before editing, verify and report:

```powershell
git branch --show-current
git status --short
git rev-parse HEAD
git log --oneline -n 10
```

Confirm:

```text
1. Current branch matches this work package branch.
2. Working tree is clean.
3. ARCH-COMPLETION-3 is merged.
4. Day-one architecture verdict is complete with non-blocking carry-forward.
5. DHEA high package is currently inactive.
6. DHEA low package is currently inactive.
7. No DHEA / DHEA-S package is currently active.
8. Existing DHEA carry-forward remains open.
9. Lab-derived range policy remains active.
10. Repository secret-file gate remains remediated.
```

STOP if baseline is unclear.

---

# Phase 1 — DHEA / DHEA-S identity audit

Before changing code, produce a read-only identity audit.

Document:

```text
- where DHEA currently appears in canonical registry / alias registry / packages
- whether DHEA-S or DHEAS already exists as a canonical biomarker
- whether DHEA and DHEA-S are currently conflated
- what sample panel evidence exists
- what unit is reported
- what reference range is reported
- whether the unit/range strongly indicates DHEA-S
- whether true unsulfated DHEA appears anywhere
- which package(s) currently depend on the ambiguous identity
```

Allowed identity conclusions:

```text
DHEA_S_CONFIRMED
DHEA_UNSULFATED_CONFIRMED
AMBIGUOUS_IDENTITY_FAIL_CLOSED
DHEA_AND_DHEAS_CONFLATED_BLOCKER
INSUFFICIENT_SAMPLE_EVIDENCE
```

STOP if the identity cannot be resolved safely.

---

# Phase 2 — Define reusable multi-factor canonicalisation model

Create or update a governed model for ambiguous biomarker canonicalisation.

Preferred artefact:

```text
knowledge_bus/governance/unit_aware_biomarker_canonicalisation_model_v1.yaml
```

The model must define:

```text
- purpose
- scope
- ambiguous biomarker handling
- required identity evidence fields
- allowed confidence levels
- fail-closed conditions
- raw label preservation requirement
- unit-aware canonicalisation rules
- DHEA / DHEA-S rule
- future extension pattern for other ambiguous markers
```

Required confidence levels:

```text
HIGH_CONFIDENCE_UNIT_RANGE_MATCH
MODERATE_CONFIDENCE_UNIT_MATCH
LOW_CONFIDENCE_LABEL_ONLY
AMBIGUOUS_FAIL_CLOSED
```

The DHEA rule must explicitly state:

```text
label-only DHEA is insufficient for DHEA-S canonicalisation unless supported by unit/range/lab-context evidence.
```

The governance file must be marked:

```yaml
runtime_consumed: true
```

only if runtime code actually reads it.

If runtime does not consume it yet, mark:

```yaml
runtime_consumed: false
```

and explain where implementation lives.

---

# Phase 3 — Implement or extend canonicalisation logic

Implement the smallest safe reusable canonicalisation change.

Allowed implementation patterns:

```text
- add multi-factor identity resolution helper
- extend existing alias resolver to accept unit/reference range context
- add DHEA/DHEAS special-case only through a general ambiguous-marker framework
- add identity confidence/provenance metadata if current marker model supports it
```

Forbidden implementation patterns:

```text
- broad parser rewrite
- fallback parser
- dummy parser
- hardcoded silent remapping with no provenance
- label-only DHEA → DHEA-S remap
- deleting true DHEA support if already present
```

If current architecture cannot persist canonicalisation provenance, do not force a large rewrite. Instead:

```text
- implement safe canonical_id resolution
- preserve raw label/unit/range wherever current structures allow
- add carry-forward for richer provenance if genuinely required
```

Canonicalisation must fail closed where:

```text
- raw label is ambiguous
- unit is missing
- reference range is missing
- unit/range conflict with DHEA-S convention
- true DHEA vs DHEA-S cannot be distinguished
```

---

# Phase 4 — Update canonical IDs and aliases

If Phase 1 confirms DHEA-S identity:

```text
- create or confirm canonical biomarker ID for DHEA-S / DHEAS
- map DHEA-S / DHEAS aliases to that ID
- map "DHEA (Venous)" to DHEA-S only when unit/range rule passes
- do not map true unsulfated DHEA to DHEA-S
- update package metadata to refer to DHEA-S where justified
```

If Phase 1 does not confirm DHEA-S identity:

```text
- do not update package identity to DHEA-S
- keep packages inactive
- document unresolved identity blocker
```

Expected canonical ID preference:

```text
dhea_s
```

Use the repo’s existing naming convention if different, but document the choice.

---

# Phase 5 — DHEA-S high package handling

If and only if DHEA-S identity is confirmed, assess whether the existing DHEA high package should become a DHEA-S high package.

Allowed outcomes:

```text
RENAME_TO_DHEA_S_HIGH_AND_ACTIVATE_WITH_GATES
RENAME_TO_DHEA_S_HIGH_KEEP_INACTIVE_PENDING_GATES
KEEP_DHEA_HIGH_INACTIVE_IDENTITY_UNRESOLVED
KEEP_DHEA_HIGH_INACTIVE_UNSULFATED_DHEA
```

Activation is allowed only if all required gates from the medical research authority can be encoded deterministically.

Required DHEA-S high gates:

```text
- DHEA-S high relative to lab-provided reference range
- biological sex present
- age present
- DHEA supplementation context answered
- testosterone therapy / AAS exposure context answered
- hormone therapy context answered where applicable
- androgen excess symptoms disclosure captured
- pregnancy status answered where applicable
- companion testosterone / SHBG availability captured where available
```

Required exclusions:

```text
- suppress endogenous adrenal-androgen interpretation if DHEA supplementation answered_yes
- suppress endogenous interpretation if testosterone therapy / AAS answered_yes
- suppress if pregnancy answered_yes and pregnancy-specific logic is unavailable
- use clinician-review wording for severe or rapid-onset virilisation if symptom severity available
```

Safe wording only:

```text
May say:
  "This pattern may support an adrenal contribution to androgen excess when interpreted alongside sex, age, symptoms, testosterone, SHBG and supplement/medication context."

Must not say:
  "You have adrenal androgen excess."
  "You have an adrenal tumour."
  "You have PCOS."
  "Your adrenal glands are overactive."
```

Do not activate if any required gate cannot be represented safely.

---

# Phase 6 — DHEA / DHEA-S low handling

Do not activate DHEA low or DHEA-S low as a primary runtime signal in this sprint.

Required outcome:

```text
DHEA_LOW_DO_NOT_ACTIVATE_EVIDENCE_INSUFFICIENT
```

If package identity is converted to DHEA-S low, keep it inactive unless a separate future medical authority explicitly supports activation.

Update governance to make this explicit.

---

# Phase 7 — Governance and carry-forward updates

Update relevant governance artefacts to reflect the outcome.

Likely files:

```text
knowledge_bus/governance/batch2_full_coverage_activation_execution_register_v1.yaml
knowledge_bus/governance/batch2_full_coverage_activation_readiness_register_v1.yaml
knowledge_bus/governance/day_one_full_traceability_manifest_v1.yaml
knowledge_bus/governance/day_one_launch_estate_gate_v1.yaml
knowledge_bus/governance/medical_frame_identity_index_v1.yaml
docs/sprints/launch_core_carry_forward_register.md
```

Required carry-forward handling:

```text
- close DHEA/DHEA-S identity carry-forward if resolved
- keep DHEA-S low inactive with explicit reason
- keep DHEA-S high active only if deterministic gates are complete
- if DHEA-S high remains inactive, record exact missing gate/reason
- do not leave vague DHEA carry-forward text
```

If day-one launch estate verdict remains valid, do not unnecessarily reopen day-one architecture.

If this work changes the launch estate verdict, document why.

---

# Phase 8 — Required tests

Add or update tests proving:

## Canonicalisation tests

```text
1. "DHEA (Venous)" + µmol/L + DHEA-S-like reference range canonicalises to DHEA-S.
2. "DHEA" + µmol/L + DHEA-S-like reference range canonicalises to DHEA-S.
3. "DHEAS" canonicalises to DHEA-S.
4. "DHEA-S" canonicalises to DHEA-S.
5. Ambiguous "DHEA" with no unit/range does not silently canonicalise to DHEA-S.
6. Unit/range conflict fails closed or remains unresolved.
7. Raw label is preserved.
8. Unit is preserved.
9. Reference range is preserved where current model supports it.
10. Canonicalisation reason/confidence is recorded where current model supports it.
```

## Package tests

If DHEA-S high is activated, tests must prove:

```text
- fires only when DHEA-S is high and all required gates are satisfied
- suppresses when DHEA supplementation answered_yes
- suppresses when AAS/testosterone therapy answered_yes
- suppresses when sex missing
- suppresses when age missing
- suppresses when pregnancy answered_yes
- does not diagnose adrenal disease, adrenal tumour or PCOS
```

If DHEA-S high remains inactive, tests must prove:

```text
- package remains inactive
- no adrenal androgen signal is emitted from ambiguous DHEA
- DHEA low remains inactive
```

## Regression tests

Must prove:

```text
- existing Batch 2 activated signals remain active and unchanged
- inactive androgen packages remain inactive unless explicitly changed
- raw Pass 3 runtime reads remain absent
- day-one launch estate validator still passes
```

---

# Phase 9 — Required validation

Run and paste full output.

## Architecture / governance validators

```powershell
python backend/scripts/run_architecture_validation_gate.py
python backend/scripts/validate_day_one_architecture.py
python backend/scripts/validate_day_one_launch_estate_gate.py
python backend/scripts/validate_medical_frame_identity_index.py --index knowledge_bus/governance/medical_frame_identity_index_v1.yaml
python backend/scripts/validate_context_modifier_catalogue.py --catalogue knowledge_bus/governance/context_modifier_catalogue_draft_v1.yaml
```

## Regression tests

```powershell
python -m pytest backend/tests/regression/test_runtime_context_evaluation.py -q
python -m pytest backend/tests/regression/test_context_threading.py -q
python -m pytest backend/tests/regression/test_batch2_full_coverage_activation.py -q
python -m pytest backend/tests/regression/test_output_authority_provenance.py -q
```

Run all new canonicalisation tests.

Run all relevant governance tests.

## Secret-file guardrail

Run:

```powershell
python scripts/check_no_secret_files.py
```

if present.

---

# Phase 10 — Required audit paper

Create:

```text
docs/audit-papers/DHEA-DHEAS-CANONICALISATION-1_unit_aware_marker_identity_and_adrenal_androgen_resolution.md
```

The audit paper must include:

```text
- executive verdict
- files inspected
- files changed
- DHEA / DHEA-S identity audit
- sample panel evidence
- unit/reference-range evidence
- canonicalisation model summary
- canonicalisation implementation details
- DHEA-S high package outcome
- DHEA/DHEA-S low package outcome
- governance updates
- carry-forward impact
- confirmation raw label/unit/range preservation
- confirmation no label-only DHEA to DHEA-S remap
- confirmation no unsupported DHEA activation
- confirmation no DHEA low activation
- confirmation no SSOT changed unless explicitly justified
- confirmation no frontend changed
- confirmation no scoring changed
- confirmation no report compiler changed unless explicitly justified
- confirmation no raw research runtime reads introduced
- confirmation no diagnosis wording introduced
- confirmation no treatment/supplement recommendation introduced
- full validator output
- full test output
- rollback path
- recommended next action
```

Validation and test output must be pasted in full, not summarised.

---

# Phase 11 — Git evidence requirements

Before commit, report:

```powershell
git branch --show-current
git status --short
git diff --name-only
git diff --cached --name-only
```

Commit message if DHEA-S high is activated:

```text
feat(canonicalisation): resolve DHEA-S identity and activate gated adrenal androgen signal
```

Commit message if identity is resolved but DHEA-S high remains inactive:

```text
feat(canonicalisation): add unit-aware DHEA-S biomarker identity resolution
```

Commit message if identity cannot be resolved:

```text
docs(governance): document DHEA identity blocker and fail-closed canonicalisation
```

After commit, report:

```powershell
git status --short
git log --oneline -n 5
git diff --name-only main...HEAD
```

Do not merge.

Return evidence for Claude audit and GPT architectural review.

---

## STOP conditions

STOP and report if:

```text
1. AB full-panel DHEA evidence cannot be located.
2. DHEA and DHEA-S are conflated but cannot be safely separated.
3. Canonicalisation would require label-only DHEA to DHEA-S mapping.
4. Unit/reference-range evidence is missing or contradictory.
5. Raw label/unit/range cannot be preserved sufficiently for audit.
6. DHEA-S high activation would lack required context gates.
7. DHEA supplementation context cannot suppress endogenous interpretation.
8. AAS/testosterone therapy context cannot suppress endogenous interpretation.
9. Pregnancy context cannot suppress where required.
10. Changes would require frontend rendering edits.
11. Changes would require broad SSOT redesign.
12. Changes would require scoring changes.
13. Changes would require report compiler changes.
14. Diagnosis wording would be introduced.
15. Treatment/supplement recommendation would be introduced.
16. Validators fail.
17. Tests fail.
18. Secret-file guardrail fails.
19. Rollback path cannot be defined.
```

Do not perform ad hoc remediation beyond scope if a STOP condition is triggered.

---

## Success criteria

This sprint succeeds only if:

```text
- DHEA / DHEA-S identity is resolved or safely failed closed
- unit-aware ambiguous-marker canonicalisation is defined
- label-only DHEA is not silently mapped to DHEA-S
- raw label/unit/reference range are preserved where supported
- DHEA and DHEA-S remain separate canonical concepts
- sample AB full-panel DHEA evidence is tested
- DHEA low remains inactive
- DHEA-S high is either safely activated with gates or explicitly remains inactive with exact reason
- governance and carry-forward registers are updated
- no frontend changes occur
- no scoring changes occur
- no unsupported signal activation occurs
- validators pass
- tests pass
- audit paper contains full evidence
```

Expected next action after success:

```text
Claude audit
GPT architectural review
Human approval
Merge

Then proceed to product/beta readiness estate or a short architecture-debt closure pass if any non-blocking carry-forward remains.
```
