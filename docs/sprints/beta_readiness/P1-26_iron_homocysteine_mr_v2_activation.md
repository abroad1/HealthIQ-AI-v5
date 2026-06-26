# P1-26 — MR-v2 Iron + Homocysteine Signal Activation

**Work ID:** P1-26  
**Date closed:** 2026-06-26

## 1. Start state

P1-25 closed thyroid MR-v2 activation. Iron signals deferred since P1-3/P1-18; homocysteine production packages existed without PSI; homocysteine card referenced legacy pkg_s24.

## 2. MR-v2 authority

Medical_Research_Activation_Review_Deferred_Wave_1_Items_v2.md (2026-06-23) cleared five candidates with directly reported transferrin_saturation gates.

## 3. Iron implementation

- Created production packages for absolute iron-low, functional inflammatory iron-low, and iron-high overload contexts.
- Mandatory pre-emission gates enforce TSAT and ferritin/CRP requirements per frame.
- `signal_iron_low` and `signal_iron_high` added to `_BLOOD_IRON_OXYGEN_LAUNCH_SIGNAL_IDS`; `signal_transferrin_high` retained.

## 4. Homocysteine implementation

- Production PSI authored for B-vitamin and renal-clearance frames.
- `behavioural_impact: NONE` retained on homocysteine manifests (predicate cardiovascular routing pre-live; no assembler allowlist change).
- Consumer-facing PSI fields sanitized for prohibited diagnostic framing.

## 5. Allowlist / routing

- Iron allowlist expanded in `domain_score_assembler.py`.
- Homocysteine `_is_wave1_cardiovascular` predicate unchanged.

## 6. Compiled card updates

- `wave1_bio_oxygen_carrying_capacity` enriched with three iron source specs and serum-iron marker.
- `wave1_cv_homocysteine_pathway` updated to KB-S52C packages with explicit provenance.
- P1-26 compile manifest; estate index updated for both cards.

## 7. Validation

- Package and PSI validation PASS for all five candidates.
- P1-26 unit tests PASS; architecture validation PASS at closure.

## 8. Carry-forwards

- Calculated TSAT remains blocked.
- Hepatocellular/haemolytic iron-high standalone deferred.
- WBC/lymphocyte/neutrophil out of scope.

## 9. Recommended next sprint

- Programme backlog per BUILD_DELIVERABLE_REGISTER (WBC cohort or questionnaire carry-forwards).
