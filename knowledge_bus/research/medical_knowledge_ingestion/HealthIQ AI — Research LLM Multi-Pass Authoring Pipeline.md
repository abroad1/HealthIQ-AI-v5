# HealthIQ AI — Research LLM Multi-Pass Authoring Pipeline
## Operator Checklist

## 1. Purpose

This checklist governs operational use of the approved three-pass research authoring pipeline.

It exists to ensure that:
- each pass is used for its intended purpose
- failures are detected at the correct stage
- no pass silently takes over the responsibilities of another
- schema validity is not mistaken for gold-standard research quality
- final ingestion authority remains with human review

This checklist must be used together with:
- the approved Research LLM Multi-Pass Authoring Pipeline paper
- `investigation_spec_schema_v3.0.0.yaml`
- the approved pass prompts
- the governed exemplar assets

This checklist is not optional.
It is the operating gate for the pipeline.

---

## 2. Stage map

The governed sequence is:

1. Pass 1 — Research generation
2. Pass 2 — Contract and logic hardening
3. Pass 3 — Clinical claim calibration
4. Deterministic validation gate
5. Final human / architectural spot-check
6. Ingestion submission decision

No batch may skip a stage.
No batch may proceed to ingestion directly from an LLM pass.

---

## 3. Pre-run prerequisites

Before starting Pass 1, confirm all of the following:

### 3.1 Governance assets exist
- approved pipeline paper exists
- approved operator checklist exists
- approved Pass 1 / Pass 2 / Pass 3 prompts exist
- governed exemplar assets exist in the agreed repo location
- current `investigation_spec_schema_v3.0.0.yaml` is the supplied schema authority

### 3.2 Input batch is ready
- the canonical biomarker list for the batch is final
- biomarker names and canonical IDs are correct
- the batch scope is clearly defined
- there is no unresolved ambiguity about whether the batch is discovery, regeneration, or uplift

### 3.3 Prompt pack is frozen for the run
- the exact prompt version for each pass is fixed before the run begins
- later prompt changes during the same run are not allowed unless the run is aborted and restarted

### 3.4 Operator recording is ready
Prepare a simple run log with:
- batch name
- date
- operator
- Pass 1 model/session
- Pass 2 model/session
- Pass 3 model/session
- validation results
- final disposition

---

## 4. Pass 1 — Research generation checklist

## 4.1 Entry criteria
Pass 1 may begin only if:
- the batch biomarker list is final
- the Pass 1 prompt is approved
- the schema file is attached or supplied
- the governed exemplars are attached or supplied
- the model is instructed to research all clinically relevant abnormal directions and all materially distinct condition frames for each biomarker

## 4.2 Pass 1 operator instructions
The operator must confirm that the Pass 1 prompt includes:
- v3.0.0 contract requirement
- JSON-only instruction
- one object per biomarker-direction-condition
- explicit multi-condition discovery rule
- explicit multi-direction discovery rule where justified
- evidence hierarchy constraint
- no invented thresholds
- no invented confirmatory tests
- no promotional language
- no generic umbrella objects

## 4.3 Pass 1 acceptance criteria
Pass 1 may proceed to Pass 2 only if all of the following are true:

### Coverage
- all requested biomarkers are represented
- where clinically justified, both high and low directions are present
- where clinically justified, multiple materially distinct condition frames are present

### Object scope
- each object appears to be single-scope
- no object is clearly combining multiple primary biomarkers
- no object is clearly combining multiple directions
- no object is clearly combining multiple unrelated condition frames

### Structural completeness
- each object appears to contain:
  - activation
  - states
  - supporting markers
  - hypotheses
  - hypothesis ranking
  - confirmatory tests
  - override rules
  - evidence
  - narrative

### Quality floor
- no obvious invented or implausible condition frames dominate the batch
- no obvious marketing or dramatic wording dominates the batch
- no obvious major condition-space gap exists for common biomarkers

## 4.4 Pass 1 reject / re-run triggers
Reject or re-run Pass 1 if any of the following occurs:
- major biomarkers are omitted
- only one obvious/familiar condition frame is produced where multiple distinct frames should exist
- the output collapses broad biomarker meaning into generic umbrella objects
- the batch is structurally sparse
- weak-evidence or speculative frames dominate
- the model ignores the exemplar quality bar
- the batch is too small to be credible for the biomarker set

### Pass 1 disposition options
- ACCEPT to Pass 2
- RE-RUN Pass 1 with same prompt and clarified operator input
- ABORT run and revise prompt pack before retry

---

## 5. Pass 2 — Contract and logic hardening checklist

## 5.1 Entry criteria
Pass 2 may begin only if:
- Pass 1 was accepted
- the full Pass 1 JSON is supplied intact
- the Pass 2 prompt is approved
- the operator explicitly instructs Pass 2 to revise the supplied JSON, not regenerate from zero

## 5.2 Pass 2 operator instructions
The operator must confirm that the Pass 2 prompt includes:
- revise-not-regenerate rule
- deduplication responsibility
- single-scope enforcement
- override description vs machine-logic matching
- hypothesis hardening responsibility
- condition-frame clarity responsibility
- explicit ban on becoming a second discovery pass
- explicit failure threshold

## 5.3 Pass 2 acceptance criteria
Pass 2 may proceed to Pass 3 only if all of the following are true:

### Deduplication
- no obvious near-duplicate condition objects remain
- repeated frames with only cosmetic label differences have been removed or merged appropriately

### Scope discipline
- each object remains one biomarker / one direction / one condition
- object naming is internally consistent
- `spec_id` and `signal_id` patterns are consistent with object scope

### Logic integrity
- override rule descriptions match their machine-readable conditions
- no obvious contradictory operator/boundary combinations remain
- supporting markers look functionally justified
- contradiction markers exist where clearly clinically needed
- hypothesis ranking is coherent

### Hypothesis sufficiency
- hypotheses are materially distinct
- placeholder hypotheses have been removed or strengthened
- single-hypothesis objects are rare and only present where genuinely justified

## 5.4 Pass 2 failure-threshold rule
Pass 2 must fail the batch and return it to Pass 1 if more than 30% of objects would require:
- de facto regeneration rather than revision
- major condition-space replacement
- substantial biological reframing
- extensive hypothesis reconstruction due to weak discovery quality

This is a hard governance rule.
Pass 2 must not silently become a second discovery pass.

## 5.5 Pass 2 reject / re-run triggers
Reject or re-run Pass 2 if:
- duplicates still dominate the batch
- override logic remains obviously inconsistent
- object scope is still blurred
- the pass appears to have rewritten the batch from scratch
- the pass invented new speculative condition frames
- more than 30% of objects needed discovery-level rebuilding

### Pass 2 disposition options
- ACCEPT to Pass 3
- FAIL back to Pass 1
- ABORT run and revise prompt pack before retry

---

## 6. Pass 3 — Clinical claim calibration checklist

## 6.1 Entry criteria
Pass 3 may begin only if:
- Pass 2 was accepted
- the full Pass 2 JSON is supplied intact
- the Pass 3 prompt is approved
- the operator explicitly instructs Pass 3 to preserve structure and logic unless a direct wording/logic mismatch requires limited correction

## 6.2 Pass 3 operator instructions
The operator must confirm that the Pass 3 prompt includes:
- evidence-strength calibration
- anti-inflation wording rules
- anti-promotional tone rules
- anti-pseudo-certainty rules
- explicit ban on reopening discovery unnecessarily
- explicit ban on redesigning structure

## 6.3 Pass 3 acceptance criteria
Pass 3 may proceed to deterministic validation only if all of the following are true:

### Tone and restraint
- no obvious promotional or dramatic language remains
- no obvious persuasive copywriting style remains
- narrative tone is clinically neutral

### Evidence calibration
- strong claims align with strong evidence
- moderate evidence is written cautiously
- exploratory evidence is explicitly limited
- no unsupported causal certainty is obvious

### Threshold honesty
- threshold notes are restrained
- no pseudo-precision or invented universality is obvious
- no wording implies certainty beyond the encoded logic

### Label honesty
- condition labels do not overclaim
- interpretations are framed as clinically plausible, not automatically definitive

## 6.4 Pass 3 reject / re-run triggers
Reject or re-run Pass 3 if:
- inflated terms remain throughout the batch
- the batch still reads like persuasive copy
- causal claims are over-stated
- diagnostic certainty is over-stated
- threshold framing is too absolute
- Pass 3 has drifted into structural redesign

### Pass 3 disposition options
- ACCEPT to deterministic validation
- RE-RUN Pass 3 on the same input
- FAIL back to Pass 2 if the issue is actually structural/logic-related

---

## 7. Deterministic validation gate checklist

## 7.1 Entry criteria
Deterministic validation may begin only if:
- Pass 3 was accepted
- the final JSON batch is saved in the agreed batch location
- the batch identifier and file path are known

## 7.2 Required validation commands
Run:

```powershell
python backend/scripts/validate_investigation_spec.py --spec-dir knowledge_bus/research/investigation_specs/<batch>
````

And once implemented:

```powershell
python backend/scripts/validate_research_batch.py --batch-file knowledge_bus/research/investigation_specs/<batch>/<batch_file>.json
```

## 7.3 Validation result classes

The gate must classify findings as:

### HARD FAIL

Examples:

* invalid JSON
* schema non-compliance
* duplicate `spec_id`
* missing required fields
* invalid enums
* malformed override conditions
* broken reference shape
* structural contract violations

### WARN

Examples:

* suspiciously similar condition labels
* repeated object titles
* fallback classifications such as `other`
* promotional phrasing patterns
* possible condition overlap
* likely missing contradiction markers

### HUMAN REVIEW FLAG

Examples:

* technically valid but medically ambiguous frames
* condition labels that may be too broad or too narrow
* evidence wording that may still be slightly over-strong
* plausible but borderline duplicate objects

## 7.4 Deterministic gate acceptance

A batch may proceed only if:

* all hard-fail issues are resolved
* warn-level issues are reviewed and accepted or corrected
* human-review flags are logged for final spot-check

### Deterministic gate disposition options

* PASS to final human / architectural review
* FAIL for correction
* HOLD for human judgement

---

## 8. Final human / architectural spot-check checklist

## 8.1 Entry criteria

Final review may begin only if:

* the deterministic validation gate passed or is on HOLD with specific flagged items
* the operator log is complete
* the final batch file is frozen for review

## 8.2 Final review questions

The reviewer must answer:

1. Does the batch look materially complete for the biomarker set?
2. Are any obvious major condition frames missing?
3. Are any objects still duplicates in substance?
4. Are the strongest claims actually justified by the evidence presented?
5. Do any condition labels still feel premature or overclaiming?
6. Are there any objects that are structurally valid but intellectually weak?
7. Does the batch feel ingestion-grade rather than merely passable?

## 8.3 Final review outcomes

* APPROVE for ingestion submission
* RETURN to Pass 3 for wording/evidence calibration fixes
* RETURN to Pass 2 for logic/dedupe fixes
* RETURN to Pass 1 for discovery failure

---

## 9. Ingestion submission readiness checklist

A batch is ready for ingestion submission only if all of the following are true:

* Pass 1 accepted
* Pass 2 accepted
* Pass 3 accepted
* deterministic validation gate passed
* final human / architectural review approved
* batch file path is final
* run log is complete
* no unresolved hard-fail items remain
* any accepted warnings are documented

If any of the above is false, the batch is not ready.

---

## 10. Operator logging requirements

For every run, record:

* batch name
* operator
* date
* Pass 1 model/session
* Pass 2 model/session
* Pass 3 model/session
* whether governed exemplars were supplied
* whether schema was supplied
* Pass 1 outcome
* Pass 2 outcome
* Pass 3 outcome
* deterministic validation outcome
* final review outcome
* final disposition

This log may be simple, but it must exist.

---

## 11. Failure handling rules

### 11.1 Do not patch downstream what should fail upstream

* discovery failures go back to Pass 1
* contract/logic failures go back to Pass 2
* tone/evidence-calibration failures go back to Pass 3

### 11.2 Do not skip back and forth casually

Only step back one stage unless the defect clearly originated earlier.

### 11.3 Do not let script PASS overrule expert rejection

A script PASS is necessary, not sufficient.

### 11.4 Do not let subjective preference override real coverage

The reviewer must distinguish between:

* genuine defect
* personal wording preference

---

## 12. Recommended immediate next steps

1. approve this checklist alongside the pipeline paper
2. commit two governed exemplar assets
3. finalise the three prompts
4. build the `validate_research_batch.py` script
5. run the first live batch through the full pipeline
6. inspect where the first operational failures occur
7. tighten prompts or checklist only after observing real pipeline behaviour

---

## 13. Recommendation

Approve this checklist and use it as the operating control document for the new research pipeline.

The pipeline paper defines the model.
This checklist defines how it is actually run.

```

If you want, the next thing I should produce is the first-pass prompt in final governed form, using this checklist and the approved pipeline paper as authority.
```
