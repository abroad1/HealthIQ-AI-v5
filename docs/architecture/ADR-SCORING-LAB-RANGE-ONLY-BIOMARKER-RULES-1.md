# ADR-SCORING-LAB-RANGE-ONLY-BIOMARKER-RULES-1

## Status

Accepted

## Context

- Lab-provided reference ranges are authoritative for biomarker interpretation; global/default ranges are prohibited.
- P1-6 failed by adding hardcoded thyroid scoring bands.
- P1-6R proved bands were structurally required at policy validation and `BiomarkerRule` construction, even though `calculate_biomarker_score()` already implemented lab-range scoring at the primitive level.
- P1-8 introduces a governed opt-in path so biomarkers can join system orchestration without hardcoded bands.

## Decision

**Lab-range-only biomarker rules are now supported.**

### Explicit rule pattern

```yaml
<biomarker_id>:
  scoring_type: lab_range_only
  unit: "<required canonical unit>"
  weight: <numeric>
  age_adjustment: <optional bool>
  sex_adjustment: <optional bool>
```

Constraints:

- `bands` must not be present on `lab_range_only` entries.
- `scoring_type` defaults to `range_position` for backward compatibility.
- Runtime scoring uses lab-provided reference ranges via existing `calculate_biomarker_score()` logic.
- Missing lab range fails closed with `missing_lab_reference_range`.

Production `backend/ssot/scoring_policy.yaml` was not modified in P1-8. Thyroid markers are not enabled.

## Non-negotiable constraints

- No global/default reference ranges
- No placeholder bands in clinical units
- No diagnostic thresholds in scoring policy
- Opt-in via explicit `scoring_type: lab_range_only`
- Fail-closed when lab range absent
- Existing `range_position` band-based rules unchanged
- No signal activation from scoring rule changes
- No Layer C / Gemini / frontend reasoning

## Consequences

| Area | Consequence |
|---|---|
| Future scoring-policy sprints | May add `lab_range_only` biomarkers to systems (e.g. hormonal rail) without hardcoded bands |
| Thyroid | Engine unblocked; production thyroid scoring still off until separate policy sprint |
| P1-4 retry | Still blocked by TSH authority, compiled card, domain wiring |
| Other systems | eGFR, iron markers, and future markers can use same pattern |
| Tests | Fixture policies required for bandless entries; production tests unchanged |

## Files reviewed

- `backend/ssot/scoring_policy.yaml`
- `backend/core/scoring/rules.py`
- `backend/core/scoring/engine.py`
- `backend/core/analytics/scoring_policy_registry.py`
- `backend/tests/unit/test_scoring_rules.py`
- `backend/tests/test_scoring_lab_range_only.py`
- `docs/sprints/beta_readiness/P1-6R_thyroid_scoring_architecture_recovery.md`
- `docs/architecture/ADR-THYROID-SCORING-LAB-RANGE-ARCHITECTURE-1.md`

## Files changed

- `backend/core/analytics/scoring_policy_registry.py`
- `backend/core/scoring/rules.py`
- `backend/tests/unit/test_scoring_lab_range_only_rules.py` (new)
- `backend/tests/unit/test_scoring_rules.py`
- `docs/sprints/beta_readiness/P1-8_scoring_lab_range_engine.md` (new)
- `docs/architecture/ADR-SCORING-LAB-RANGE-ONLY-BIOMARKER-RULES-1.md` (new)
- `docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md`
