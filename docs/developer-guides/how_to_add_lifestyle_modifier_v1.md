# How to Add a Lifestyle Modifier v1

## Questionnaire mapping

- Bridge: `backend/core/pipeline/questionnaire_mapper.py`
- Submission model: `backend/core/models/questionnaire.py`
- Orchestrator applies mapped lifestyle factors before scoring overlays

## Lifestyle modifier computation

- Overlays: `backend/core/scoring/overlays.py` — `LifestyleOverlays`
- Must not invent biomarker values from questionnaire alone

## Confidence / caveat / explanation limits

- Visible payoff must match LC-S13 narrative coherence rules
- No prescriptive medical advice in consumer text

## Allowed and forbidden claims

**Allowed:** lifestyle context modifiers that adjust scoring overlays when policy permits

**Forbidden:**

- Diagnosis or treatment directives
- Hidden Gemini/LLM interpretation in deterministic path
- Raw internal IDs in user-facing strings

## Visible user-surface requirements

- Lifestyle modifiers must surface in DTO fields consumed by frontend (see LC-S19 payload contract)

## Sentinel

See Sentinel expectations below.

## Sentinel expectations

- `backend/tests/regression/test_lc_s13_lifestyle_coherence_narrative.py` must pass
- Add Sentinel entry if new lifestyle defect class emerges

## Standing maintenance

Future KB-WAVE or scaffold sprints must update this document if they introduce or change the relevant architectural pattern.
