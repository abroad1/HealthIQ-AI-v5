---
work_id: P1-4
branch: work/P1-4-thyroid-energy-regulation-domain-card
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# P1-4 — Thyroid / Energy Regulation Domain Card

## Objective

Implement the third missing launch-core domain if, and only if, the thyroid authority and FT3 register position can be reconciled safely:

```text id="gvcsk4"
Thyroid / energy regulation
```

This sprint must follow the launch-core domain pattern established by P1-2 kidney function and P1-3 blood / iron / oxygen, but thyroid is clinically more context-sensitive. Therefore, this sprint has an internal STOP gate before implementation.

The sprint has two phases:

```text id="7c7jza"
Phase 1 — Thyroid authority and FT3/register reconciliation
Phase 2 — Bounded thyroid / energy regulation domain implementation, only if Phase 1 passes safely
```

If Phase 1 exposes unresolved authority conflict, blocked signal ambiguity, unsafe FT3 handling, or missing medical-review authority, stop and produce a blocker report. Do not improvise.

---

## Prerequisite

Do not start unless P1-3 has been merged to `main`.

Required files on `main`:

```text id="sr7q41"
docs/sprints/beta_readiness/P1-1_launch_core_domain_build_materials_map.md
docs/sprints/beta_readiness/P1-2_kidney_function_domain_card.md
docs/sprints/beta_readiness/P1-3_blood_iron_oxygen_domain_card.md
docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md
```

If any file is missing on `main`, stop and report:

```text id="bcdtx4"
P1 launch-core prerequisite evidence is not present on main. P1-4 must not proceed.
```

---

## Critical architectural boundary

This sprint is Layer B implementation work only if the Phase 1 authority gate passes.

Layer B owns:

```text id="uz6bva"
biomarker interpretation
signal activation/suppression
domain/system reasoning
subsystem reasoning
WHY/root-cause
hierarchy
surfacing decisions
clinician-report content
prose/explainer selection
safety
provenance
```

Layer C, Gemini and frontend must not perform thyroid / energy regulation reasoning.

Do not create frontend medical inference.

Do not use Gemini.

Do not create or rely on fallback parser logic.

Do not substitute global/default ranges where lab-provided ranges exist.

Do not activate blocked or context-dependent thyroid signals unless explicit governed authority says they are safe for runtime activation.

Do not create diagnostic hypothyroidism, hyperthyroidism, thyrotoxicosis, thyroiditis, Graves’ disease, pituitary disease or non-thyroidal illness language unless already governed, explicitly supported, non-diagnostic, and safe.

The default posture is educational interpretation of thyroid-axis markers and energy-regulation context, not diagnosis.

---

## Branch and state checks

Start from `main`.

```powershell id="spuemi"
git switch main
git pull
git status --short
git switch -c work/P1-4-thyroid-energy-regulation-domain-card
```

Do not proceed if the working tree is dirty.

Confirm the Automation Bus active work package/state file if required by SOP.

---

## First authority documents

Read these first, in this order:

```text id="rsdkn5"
docs/strategy/beta_readiness/HEALTHIQ_AI_BETA_READINESS_DEFINITIVE_STRATEGY_FINAL_2026-06-20.md
docs/sprints/beta_readiness/P1-1_launch_core_domain_build_materials_map.md
docs/sprints/beta_readiness/P1-2_kidney_function_domain_card.md
docs/sprints/beta_readiness/P1-3_blood_iron_oxygen_domain_card.md
docs/architecture/ADR-LAYER-BOUNDARY-RECONCILIATION-1.md
docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md
```

P1-1 is the immediate scope authority for thyroid / energy regulation.

P1-2 and P1-3 are implementation pattern references for adding bounded launch-core domain rows after the original Wave 1 domains.

Do not exceed the thyroid / energy regulation scope proven by P1-1.

---

## Additional authority and reference files

Read as relevant and only if present:

```text id="v9t1yw"
docs/strategy/eight_block_beta_readiness/EIGHT_BLOCK_BETA_READINESS_COMPARISON_AND_PROGRAMME_RECOMMENDATION_2026-06-18.md
docs/strategy/LAYER_ARCHITECTURE_AUTHORITY_INDEX_2026-06-17_r2.md
docs/architecture/User Health to Systems Map_FINAL.md
docs/AUTHORITY_MAP.md
backend/ssot/scoring_policy.yaml
backend/core/analytics/domain_score_assembler.py
backend/core/analytics/domain_narrative_wave1.py
backend/core/analytics/wave1_subsystem_evidence.py
backend/core/contracts/narrative_payload_v1.py
backend/core/dto/persisted_replay_contract_v1.py
backend/core/knowledge/health_system_card_evidence.py
backend/core/analytics/report_compiler_v1.py
backend/core/analytics/root_cause_compiler_v1.py
knowledge_bus/
knowledge_bus/compiled/
knowledge_bus/pathway_explainers_v1/
backend/tests/
docs/testing/
docs/intelligence/
docs/architecture/
docs/medical_review/
```

Also search the repository for thyroid-specific authority, including terms:

```text id="zg8hs3"
FT3
Free T3
free_t3
T3
FT4
Free T4
free_t4
T4
TSH
thyroid
thyrotoxicosis
low T3
non-thyroidal illness
Batch 2 Thyroid
thyroid authority
FT3 register
```

If a path listed by P1-1 no longer exists or differs from the map, record that honestly and adjust only within the authorised scope.

---

## Phase 1 — Thyroid authority and FT3/register reconciliation

Before any implementation, create a short authority reconciliation section in the sprint implementation note.

You must determine:

```text id="9vax5o"
1. Which thyroid markers are present in the existing governed estate.
2. Which thyroid signals are active, inactive, blocked, or context-dependent.
3. Whether FT3 low remains blocked or requires medical-review/context gating.
4. Whether FT3 high, FT4 high, FT4 low, TSH high/low or other thyroid patterns have clear runtime authority.
5. Whether any register, map, package, signal index, frame index or audit document conflicts.
6. Whether any thyroid signal would require context evidence before runtime activation.
7. Whether a safe domain card can be emitted using existing scoring/card evidence without activating blocked/context-dependent signals.
```

### Phase 1 STOP conditions

Stop before implementation if any of the following are true:

```text id="r3kb48"
- FT3 low authority is unresolved or contradictory.
- Any required thyroid marker or signal status cannot be established from repo evidence.
- Implementation would require activation of a blocked or context-dependent thyroid signal.
- Implementation would require new global/default thyroid reference ranges.
- Implementation would require new thyroid scoring bands not already governed.
- Implementation would require diagnostic hypothyroid/hyperthyroid/thyrotoxicosis/non-thyroidal illness claims.
- Implementation would require Gemini, frontend inference or Layer C medical reasoning.
- Existing thyroid medical-review authority is absent, ambiguous or contradictory.
```

If a STOP condition is triggered:

```text id="n9dwoi"
- do not touch runtime code;
- do not modify scoring policy;
- do not create a compiled runtime card;
- do not wire a thyroid domain row;
- create the P1-4 implementation note as a blocker report;
- update the build deliverable register with Status: Blocked or Partial;
- return for GPT architectural review.
```

---

## Phase 2 — Implementation scope only if Phase 1 passes

If Phase 1 confirms a safe bounded scope, implement a thyroid / energy regulation domain card / domain output using existing repository patterns.

The sprint may include, if required by the existing architecture:

```text id="x8wtdc"
- domain assembler wiring for thyroid / energy regulation
- domain score/card output wiring
- subsystem evidence wiring where supported
- compiled health-system card evidence where supported
- DTO/replay/report inclusion where existing Layer B contracts require it
- deterministic tests for thyroid / energy regulation domain output
- minimal documentation of implementation decisions
- build deliverable register update
```

The sprint must stay inside the safe thyroid scope established by Phase 1.

---

## Candidate biomarker scope

Use only biomarkers supported by P1-1 and repository evidence.

Candidate markers to verify include:

```text id="j9kljp"
TSH
Free T4
Free T3
thyroid antibodies only if present and governed
```

Do not invent additional markers.

Do not add interpretation logic for unavailable markers.

Do not treat FT3 low as safe unless the authority review clearly supports runtime activation.

Do not use symptoms, lifestyle context or medication assumptions unless the existing runtime has governed structured context available and the relevant thyroid authority explicitly requires or allows it.

If a marker is absent from an uploaded panel, handle it through existing missing-marker patterns only where those patterns are already governed.

---

## Clinical safety rules

Thyroid / energy regulation output must remain:

```text id="3xe95r"
educational
non-diagnostic
cautious
lab-range grounded
traceable
proportionate
context-aware where required
```

Do not state or imply a diagnosis of:

```text id="zw9r6w"
hypothyroidism
hyperthyroidism
thyrotoxicosis
T3-toxicosis
thyroiditis
Graves’ disease
Hashimoto’s disease
pituitary disease
non-thyroidal illness
low T3 syndrome
```

unless an existing governed source explicitly allows the wording and the output remains non-diagnostic.

Preferred framing:

```text id="npvro2"
thyroid-axis markers
thyroid hormone signalling context
markers that can relate to energy regulation
a pattern that may be worth discussing with a clinician if out of range or persistent
```

Avoid:

```text id="wpy0f8"
you have hypothyroidism
this proves hyperthyroidism
this confirms thyrotoxicosis
this means low T3 syndrome
this indicates pituitary disease
diagnostic staging
urgent disease claims
```

---

## Lab-range rules

Use lab-provided reference ranges where available.

Do not hardcode global/default reference ranges.

Do not introduce new global reference intervals.

Do not rebalance existing biomarker weights unless explicitly justified by an existing governed scoring policy and P1-1 evidence.

Do not repeat the P1-2 scoring-policy error: if implementation would require new range bands, diagnostic thresholds, or a new scoring policy, stop and report the blocker rather than improvising.

---

## Scoring and policy rules

Inspect existing scoring rails before modifying anything.

If thyroid / energy regulation scoring is already present in `backend/ssot/scoring_policy.yaml`, reuse it.

Do not rewrite scoring policy broadly.

Do not create a new scoring model from memory.

If a minimal scoring-policy update appears necessary, only proceed if:

```text id="g0l0tz"
- Phase 1 found clear authority for the relevant markers;
- P1-1 identified it as required or expected;
- the existing scoring-policy structure clearly supports the change;
- the change is bounded to thyroid / energy regulation;
- it does not introduce hardcoded global reference intervals;
- it does not silently rebalance existing governed weights;
- tests are added or updated;
- the final report explains the policy change.
```

If scoring-policy ambiguity is significant, stop and report the blocker.

---

## Signal-routing rules

Do not route thyroid signals by broad system-field matching.

Use a signal-id allowlist only.

The allowlist must include only signals with clear runtime authority.

If all thyroid signals are blocked or context-dependent, the allowlist must be empty.

If the allowlist is empty but a safe scored/card domain row can be emitted from governed scoring/card evidence, that is acceptable only if Phase 1 supports it.

If an empty allowlist would make the thyroid domain misleading or unsupported, stop and report the blocker.

---

## Subsystem rules

Only implement subsystem groupings supported by P1-1 and repository evidence.

Possible subsystem candidates must be evidence-backed.

Potential areas to verify, not assume:

```text id="oo2b7e"
thyroid axis
thyroid hormone signalling
energy regulation
TSH / FT4 relationship
T3 conversion only if medically governed
```

Do not invent polished subsystem names solely for UX.

Subsystems remain Layer B.

Frontend must only render governed outputs.

---

## Prose, explainer and clinician-report rules

This sprint may wire existing thyroid / energy regulation material into governed Layer B surfaces if required by the runtime pattern.

Do not create a broad prose expansion sprint inside P1-4.

Do not write a full new thyroid explainer estate.

Do not use Gemini to produce prose.

If existing retail explainer, pathway explainer or clinician-report assets are insufficient, record the gap as a carry-forward to P2-1 or later Layer B prose work.

---

## Runtime constraints

Do not:

```text id="ybvf4u"
- read raw Pass 3 material at runtime
- read raw Knowledge Bus research files at runtime
- modify Knowledge Bus source packages
- promote Pass 3 material
- activate blocked/context-dependent signals
- add frontend medical inference
- add Gemini runtime calls
- add fallback parser logic
- introduce hardcoded clinical thresholds
- infer thyroid disease context from marker names alone
```

---

## Required deliverables

### 1. Phase 1 authority reconciliation

Create or update the implementation note with a Phase 1 section.

Required path:

```text id="hd4cpp"
docs/sprints/beta_readiness/P1-4_thyroid_energy_regulation_domain_card.md
```

The Phase 1 section must state:

```text id="qoc9jd"
- thyroid authority sources found;
- active / inactive / blocked / context-dependent signal status;
- FT3 low status;
- any authority conflicts;
- whether implementation proceeded or stopped;
- rationale for that decision.
```

### 2. Runtime/domain implementation, only if Phase 1 passes

If safe to proceed, implement the bounded thyroid / energy regulation domain output according to existing architecture and P1-1 evidence.

Expected candidate areas may include:

```text id="zbbvf7"
backend/core/analytics/domain_score_assembler.py
backend/core/analytics/domain_narrative_wave1.py
backend/core/analytics/wave1_subsystem_evidence.py
backend/core/dto/persisted_replay_contract_v1.py
backend/core/knowledge/health_system_card_evidence.py
backend/ssot/scoring_policy.yaml
knowledge_bus/compiled/
backend/tests/
```

Only modify what is necessary.

### 3. Tests

Add or update targeted tests if implementation proceeds.

Tests should verify, as applicable:

```text id="c5hjoz"
- thyroid / energy regulation domain appears in the expected output surface
- relevant biomarkers map correctly
- missing biomarkers do not create fabricated claims
- lab-provided ranges are respected
- output remains non-diagnostic
- unsupported disease claims are absent
- blocked/context-dependent thyroid signals are not routed
- FT3 low is not activated unless explicitly authorised
- no Layer C/Gemini/frontend inference is required
- existing domains are not regressed
- P1-2 kidney output is not regressed
- P1-3 blood / iron / oxygen output is not regressed
```

If Phase 1 stops before implementation, tests may be limited to documentation/validation checks. State this honestly.

### 4. Implementation note

Create:

```text id="q2ohjk"
docs/sprints/beta_readiness/P1-4_thyroid_energy_regulation_domain_card.md
```

Use this structure:

```markdown id="e8v7qs"
# P1-4 — Thyroid / Energy Regulation Domain Card

## 1. Summary
- whether Phase 1 passed or stopped
- what was implemented, if anything
- what remains out of scope

## 2. Phase 1 authority reconciliation
- authority documents and files reviewed
- marker scope
- signal status
- FT3 low status
- conflicts or ambiguities
- implementation decision

## 3. P1-1 evidence used
- key evidence from P1-1 that justified this sprint scope

## 4. Runtime changes
- concise description of the domain/card/scoring/report/test changes
- or “not applicable — stopped at authority gate”

## 5. Safety boundaries
- non-diagnostic wording
- lab-range use
- avoided unsupported thyroid disease claims
- no blocked/context-dependent signal activation
- no Gemini / no frontend inference

## 6. Tests and validation
- tests added/updated
- commands run
- result

## 7. Carry-forwards
- FT3/register gaps
- prose/explainer gaps
- clinician-report gaps
- UX/display implications
- safety/provenance gaps
```

Do not turn this into a large audit paper.

### 5. Build deliverable register update

At closure, update:

```text id="o1xuy6"
docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md
```

Append a short entry:

```markdown id="uj521r"
## P1-4 — Thyroid / energy regulation domain card

**Status:** Complete / Partial / Blocked  
**Date closed:** <YYYY-MM-DD>  
**Programme block(s):** Block 1 Core health systems model; Block 2 Subsystems and depth model; Block 3 Layer B intelligence/prose substrate  

### Delivered / ticked off
- <what this sprint completed against the beta-readiness programme>
- <major implementation, authority or validation outcome>

### Carry-forwards
- <what still needs to be done later>
- <known gaps exposed by this sprint>

### Blockers / risks
- <only material blockers or risks that affect future work>

### Recommended next sprint
- <next work package recommendation>
```

Keep the register entry short.

Do not list every file touched.

Do not duplicate the full implementation note or audit.

---

## Expected changed file categories

If Phase 1 stops before implementation, expected files are only:

```text id="zy2jsh"
docs/sprints/beta_readiness/P1-4_thyroid_energy_regulation_domain_card.md
docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md
automation_bus/
```

If Phase 2 proceeds, expected categories may include:

```text id="o4ih8k"
backend/core/analytics/
backend/core/dto/
backend/core/knowledge/
backend/ssot/
backend/tests/
knowledge_bus/compiled/
docs/sprints/beta_readiness/
automation_bus/
```

Do not change frontend files unless the existing architecture requires a purely render-only snapshot/test update. If any frontend file appears necessary, stop and explain why before making the change if the workflow allows; otherwise record it as a blocker.

Do not change Knowledge Bus source packages or raw Pass 3 source material.

Do not update the final strategy baseline.

Do not update AUTHORITY_MAP.

---

## Validation

Run:

```powershell id="do1lcr"
git diff --stat
git diff --name-only
git status --short
```

If Phase 2 implementation proceeds, run relevant tests.

Suggested test discovery command:

```powershell id="m1d2oq"
python -m pytest --collect-only
```

At minimum, if implementation proceeds, run tests covering:

```text id="7neagn"
domain score assembler
governed subsystem evidence
thyroid / energy regulation domain card
kidney domain card regression from P1-2
blood / iron / oxygen domain card regression from P1-3
scoring rules if scoring policy changed
day-one architecture validator if compiled card estate changed
```

If existing project test commands are documented, use the documented commands.

The final report must state:

```text id="jz14tl"
- tests run
- whether they passed
- any tests not run
- reason any tests could not be run
```

If tests fail because of pre-existing unrelated failures, isolate and document the failure.

If tests fail because of this sprint, fix or report the sprint as blocked.

---

## Required final report

Return:

```text id="x56128"
- branch name
- whether Phase 1 passed or stopped
- files changed
- summary of thyroid authority reconciliation
- FT3 low status
- summary of implementation, if any
- whether scoring policy changed
- whether report/DTO/compiler surfaces changed
- tests run and results
- safety constraints applied
- carry-forwards
- recommended next sprint
- confirmation no frontend inference added
- confirmation no Gemini added
- confirmation no fallback parser added
- confirmation no Knowledge Bus source packages or Pass 3 artefacts changed
- validation output
- git status --short
```

Do not merge until Claude audit, GPT architectural review and human approval.

---

## Acceptance criteria

This sprint is complete only if:

```text id="f5uhsz"
1. Phase 1 thyroid authority reconciliation is completed and documented.

2. FT3 low status is explicitly resolved as active, blocked, context-dependent, or unresolved.

3. Any authority conflict is documented honestly.

4. If Phase 1 does not support safe implementation, no runtime implementation is performed and the sprint is reported as Blocked or Partial.

5. If Phase 2 proceeds, thyroid / energy regulation is implemented as a bounded launch-core domain/card output using existing governed assets and P1-1 evidence.

6. The implementation remains Layer B governed and does not move medical reasoning into Layer C, Gemini or frontend.

7. The output is non-diagnostic and does not make unsupported hypothyroid, hyperthyroid, thyrotoxicosis, thyroiditis, Graves’, Hashimoto’s, pituitary disease, low T3 syndrome or non-thyroidal illness claims.

8. Lab-provided reference ranges remain authoritative where available.

9. No hardcoded global/default reference ranges or diagnostic thresholds are introduced.

10. No unauthorised scoring weight rebalancing is introduced.

11. No blocked or context-dependent thyroid signals are activated without explicit governed authority.

12. No fallback parser logic is introduced.

13. No Gemini runtime or prompt path is introduced.

14. No Knowledge Bus source packages or raw Pass 3 artefacts are modified or read at runtime.

15. Targeted tests are added or updated and run if implementation proceeds.

16. Existing implemented domains, including P1-2 kidney and P1-3 blood / iron / oxygen, are not regressed.

17. `docs/sprints/beta_readiness/P1-4_thyroid_energy_regulation_domain_card.md` is created.

18. `docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md` is updated with a short P1-4 entry.

19. The final report clearly states carry-forwards into P2 prose/explainer work, P3 safety/provenance work, and P5 UX work where relevant.
```
