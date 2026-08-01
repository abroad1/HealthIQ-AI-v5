---
work_id: ARCH-CONV-E3
branch: feature/arch-conv-e3-alt-contextual-authority
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# ARCH-CONV-E3 — Complete Remaining ALT Contextual Authority

This prompt is for Claude Code hardening before Cursor execution.

Govern under:

- `AUTOMATION_BUS_SOP_v1.3.1.md`
- `KNOWLEDGE_BUS_SOP_v1.3.1.md`
- `KNOWLEDGE_BUS_PASS3_PROMOTION_PROTOCOL_v1.1.md`
- current merged ARCH-CONV-E / E2 governance, activation and medical-decision artefacts

## Product outcome

Complete the remaining four validated ALT contexts from canonical Pass 3 research:

1. ALP-predominant / cholestatic biochemical context
2. muscle or exertional contribution
3. bilirubin severity context
4. metabolic / MASLD context

Translate the existing research rules into governed runtime eligibility, ranking, coexistence, suppression and escalation behaviour.

Do not commission new medical research unless hardening proves a specific clinical ambiguity that the canonical Pass 3 source does not resolve.

## Canonical medical authority

Use:

`knowledge_bus/research/investigation_specs/multi_llm_research/ALT_High_Hepatic_Pattern_Classification_ARCH_CONV_E_Pass_3.json`

Expected SHA-256:

`7F20BF9A06B3427217AD7F753C4D9304E5D5A2C46C484699257778844B9D3267`

Relevant specs:

- `inv_alt_high_r_value_cholestatic_alp_predominant_context`
- `inv_alt_high_muscle_source_or_exertional_contribution`
- `inv_alt_high_bilirubin_hys_law_severity_context`
- `inv_alt_high_metabolic_masld_context`

Preserve the already-active E2 authority:

- canonical general / hepatocellular ALT frame
- mixed ALT/ALP frame
- governed `r_value_alt_alp`
- existing ALP/GGT `liver_injury_axis`
- current activation-register semantics
- current Gate 1 / Gate 2 medical-governance model

## Role boundary

Claude Code hardening must extract the exact application rules from the Pass 3 source and existing contracts.

Cursor implements those hardened rules.

Cursor must not make new medical judgements, infer missing thresholds, or decide authority precedence not supported by the canonical research and existing governance.

If the research does not resolve a material medical decision, STOP and return the exact ambiguity for Head of Medical Research review.

## Phase 0 — repository-grounded hardening

Before producing the hardened execution prompt, inspect:

- all four relevant Pass 3 specs in full;
- their existing package assets;
- current activation register;
- current medical decision register;
- `signal_authority_collision_model_v1.yaml`;
- existing ALP/GGT `liver_injury_axis`;
- E2 R-value selector and runtime implementation;
- current override-rule evaluator;
- current package activation and collision mechanisms;
- current biomarker, user-context and missing-data contracts;
- current tests for ALT, ALP/GGT, bilirubin, CK, metabolic context and authority collisions.

Hardening must map every research rule to an exact runtime mechanism or identify a gap.

Do not leave application logic to Cursor discretion.

## Required authority decisions to harden

### 1. ALP-predominant / cholestatic ALT context

Canonical rules:

- primary ALT must be high;
- eligible `r_value_alt_alp <= 2` supports ALP-predominant biochemical context;
- ALP predominance alone does not prove cholestasis, obstruction or disease;
- raised GGT supports hepatic-source confidence;
- normal or missing GGT reduces hepatic-source confidence;
- bilirubin adds severity / excretory context;
- non-hepatic ALP remains a required caveat where source is not established;
- this frame must not compete with or duplicate the existing ALP/GGT `liver_injury_axis`.

Hardening must decide, from existing governance:

- whether this emits as subordinate ALT context under the existing ALP/GGT primary authority;
- whether it is suppressed when the ALP/GGT axis already owns the primary WHY;
- exact coexistence / suppression / precedence behaviour;
- exact confidence downgrade when GGT is absent or normal;
- whether runtime can represent low-confidence wording without a contract change.

### 2. Muscle / exertional contribution

Canonical rules:

- ALT high is necessary;
- raised CK supports muscle-source contribution;
- recent strenuous exercise, trauma, myopathy or statin-related muscle context may support the frame where governed user context exists;
- muscle contribution does not exclude concurrent liver disease;
- raised bilirubin or GGT strongly contradicts isolated muscle-source wording;
- raised ALP with GGT or bilirubin redirects toward liver/biliary context;
- normal or borderline CK weakens significant exertional attribution;
- very high ALT must not be explained away by a plausible muscle context;
- absent CK/history must not produce confident muscle attribution.

Hardening must specify:

- exact pre-emission corroboration threshold using lab-range status, not invented numeric cut-offs;
- exact use of user context if a governed context contract exists;
- fallback when CK or exercise history is absent;
- coexistence versus suppression with canonical general ALT-high and R-value frames;
- contradiction handling when bilirubin, GGT or ALP context is present;
- whether the frame is advisory/subordinate rather than primary authority.

### 3. Bilirubin severity context

Canonical rules:

- ALT high plus bilirubin above its lab range supports a higher-concern biochemical context;
- this is severity / escalation, not cause attribution;
- do not state or imply Hy’s Law in consumer output;
- formal Hy’s-Law-like logic requires DILI context, bilirubin/aminotransferase thresholds, lack of substantial cholestasis and exclusion of alternatives;
- ALP and GGT modify interpretation;
- unconjugated bilirubin or haemolysis context may contradict hepatic-excretory framing;
- albumin and INR add synthetic-function context;
- missing bilirubin or missing bilirubin lab range must fail closed.

Hardening must specify:

- whether this is represented as override/escalation on the active canonical ALT frame rather than a separate competing primary frame;
- exact state escalation;
- exact suppression of prohibited terminology;
- interaction with mixed and ALP-predominant patterns;
- behaviour when ALP is missing;
- behaviour when bilirubin fractionation is unavailable;
- whether package activation is needed or whether the package remains a governed non-primary severity layer.

### 4. Metabolic / MASLD context

Canonical rules:

- ALT high is necessary;
- metabolic context requires corroboration from available governed markers or declared risk context;
- supporting evidence may include HbA1c high, triglycerides high, HDL low, GGT high and governed user context;
- ALT alone must not produce MASLD or fatty-liver claims;
- imaging / fibrosis assessment is required for structural or fibrosis claims;
- raised bilirubin or INR redirects away from routine metabolic framing;
- high CK redirects toward muscle contribution;
- very high ALT must not be explained away as metabolic;
- absent metabolic context weakens or suppresses the frame.

Hardening must specify:

- the minimum safe corroboration rule from the existing research and contracts;
- whether one supporting marker is enough or whether a compound rule is required;
- exact relationship to the canonical general ALT-high frame;
- coexistence/suppression with R-value pattern frames;
- contradiction handling for bilirubin, INR and CK;
- wording limits preventing MASLD diagnosis, steatosis claims or fibrosis staging.

## Promotion and activation decisions

For each of the four packages, hardening must produce one explicit decision using existing repository vocabulary:

- activate as primary authority;
- activate as subordinate/contextual authority;
- represent as override/escalation only;
- keep withheld with an exact unresolved blocker.

Do not activate all four by default.

Do not keep any package withheld merely because application logic has not been worked through. The purpose of hardening is to derive that logic from the research and existing contracts.

Any remaining deferral must identify:

- exact unresolved medical or contract ambiguity;
- exact affected package/spec;
- why the canonical research and current contracts are insufficient;
- the minimum decision or implementation needed to unblock it.

## Required tests

Hardening must define exact tests for at least:

### ALP-predominant
- ALT high + eligible R <= 2 + GGT high
- ALT high + eligible R <= 2 + GGT normal
- ALT high + eligible R <= 2 + GGT missing
- non-hepatic ALP uncertainty
- no duplication with ALP/GGT primary authority
- bilirubin escalation interaction

### Muscle/exertional
- ALT high + CK high
- ALT high + CK high + bilirubin high
- ALT high + CK high + GGT high
- ALT high + CK absent
- ALT high + exercise context but CK absent
- ALT high + normal/borderline CK
- very high ALT with plausible muscle context
- no suppression of concurrent liver concern

### Bilirubin severity
- ALT high + bilirubin above lab range
- bilirubin missing
- bilirubin range missing
- mixed pattern + bilirubin high
- ALP-predominant pattern + bilirubin high
- prohibited Hy’s Law wording absent
- synthetic-function context where governed inputs exist

### Metabolic
- ALT high + corroborating metabolic markers
- ALT high without metabolic corroboration
- ALT high + bilirubin high
- ALT high + INR high where available
- ALT high + CK high
- no MASLD diagnosis
- no fibrosis/steatosis claim without governed evidence

### Cross-cutting
- exact runtime activation identities
- no duplicate primary ALT authority
- no non-ALT activation delta
- existing E2 hepatocellular/general and mixed behaviour preserved
- R-value boundaries preserved
- package validators pass
- launch-critical, rejected-frame and test-only opt-in behaviour preserved
- deterministic repeatability
- raw Pass 3 not read at runtime
- no frontend inference

## Medical governance

This work changes active medical interpretation authority.

Require:

- Head of Medical Research Gate 1 decision record;
- Anthony Gate 2 ratification;
- per-package disposition;
- collision/precedence decision table;
- activation-register references;
- explicit wording and safety restrictions;
- no merge before Gate 2 and independent Claude Code audit.

## Evidence deliverables

Publish an ARCH-CONV-E3 evidence report containing:

- exact research rule → runtime mechanism mapping;
- per-package authority disposition;
- collision and coexistence table;
- activation-register delta;
- before/after runtime identities;
- all test commands and outputs;
- package validator results;
- source and output hashes;
- medical decision references;
- unresolved blockers, if any;
- proof that no new medical rule was invented.

## Mandatory STOP conditions

STOP and return for review if:

- existing contracts cannot represent subordinate/contextual authority;
- low-confidence source-localisation wording cannot be represented safely;
- user-context corroboration is required but no governed context contract exists;
- “very high ALT” requires a numeric threshold absent from canonical research;
- bilirubin severity cannot be represented without creating a competing primary frame;
- the current collision model cannot represent required precedence;
- any implementation requires a new medical threshold or unsupported inference;
- any non-ALT runtime state changes unexpectedly;
- prohibited files become necessary outside hardened authority.

Do not use retrospective ratification to bypass a missed STOP.

## Completion boundary

STOP after:

- all four package dispositions are implemented or explicitly blocked with evidence;
- all eligible contexts are activated through governed mechanisms;
- collision, escalation and suppression behaviour is proven;
- Gate 1 and Gate 2 records are complete;
- kernel finish passes;
- evidence is committed.

Do not merge.

Return for independent Claude Code audit, GPT review and Anthony final merge authority.
