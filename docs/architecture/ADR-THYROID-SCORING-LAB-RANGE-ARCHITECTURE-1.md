# ADR-THYROID-SCORING-LAB-RANGE-ARCHITECTURE-1

## Status

Accepted

## Context

- **P1-4** stopped on thyroid authority: inert hormonal scoring rail, inactive TSH packages, FT3 low register conflict, and risk of misleading partial thyroid domain output.
- **P1-5** reconciled FT3 low conservatively to deferred/inactive across governance registers (`ADR-THYROID-FT3-AUTHORITY-RECONCILIATION-1`). P1-4 retry remains blocked pending scoring rail and TSH authority.
- **Failed P1-6** (`work/P1-6-thyroid-launch-core-unlock-and-domain-card`) introduced prohibited hardcoded TSH/FT3/FT4 scoring bands and Intelligence Core changes. That branch was abandoned and must not be merged or salvaged.
- **P1-6R** inspects the scoring engine to determine whether thyroid/hormonal scoring can proceed using lab-provided reference ranges alone, without hardcoded biomarker bands.

## Decision

**Current scoring architecture cannot support thyroid scoring without hardcoded bands.**

Lab-range-only scoring exists as a **primitive** in `calculate_biomarker_score()` but is **structurally inaccessible** from health-system orchestration for biomarkers that lack a full six-band YAML entry:

1. Policy schema validation requires all six bands for every `biomarkers` entry (`scoring_policy_registry.py:71-78`).
2. `_build_biomarker_rule()` requires direct access to all six band keys (`rules.py:135-140`).
3. Biomarkers listed under a system without a matching `biomarkers` dict entry are silently skipped at load (`rules.py:154-156`).
4. System scoring iterates only loaded rules (`engine.py:192`).

Therefore:

- **No thyroid scoring-policy sprint may add TSH/FT3/FT4 bands** as a workaround — that repeats the failed P1-6 anti-pattern.
- **A scoring-engine architecture sprint must precede** any hormonal scoring-policy or thyroid domain-card work.
- **Thyroid domain card implementation (P1-4 retry) remains blocked.**

## Non-negotiable constraints

- Lab-provided reference ranges remain authoritative for runtime scoring.
- No global/default thyroid reference ranges in SSOT or code.
- No placeholder bands in clinical units (mIU/L, pmol/L, etc.).
- No diagnostic thyroid thresholds introduced via scoring bands.
- No FT3 low activation.
- No thyroid signal activation from scoring changes.
- No Layer C / Gemini / frontend analytical reasoning in scoring paths.
- No fallback parser introduction.

## Consequences

| Area | Consequence |
|---|---|
| Thyroid scoring | **Blocked** until scoring-engine supports bandless lab-range-only membership |
| Hormonal scoring rail | **May be enabled later** only after engine pattern exists, then a separate policy sprint |
| Scoring-engine architecture | **Must change first** — recommended sprint: P1-SCORING-LAB-RANGE-ENGINE |
| P1-4 retry | **Blocked** — requires engine change + policy sprint + TSH authority resolution |
| TSH package authority | **Separate blocker** — kb52c not launch-active (unchanged by this ADR) |
| FT3 low | **Remains deferred/inactive** per ADR-THYROID-FT3-AUTHORITY-RECONCILIATION-1 |

## Files reviewed

- `backend/ssot/scoring_policy.yaml`
- `backend/core/analytics/scoring_policy_registry.py`
- `backend/core/scoring/rules.py`
- `backend/core/scoring/engine.py`
- `backend/tests/unit/test_scoring_rules.py`
- `backend/tests/test_scoring_lab_range_only.py`
- `backend/tests/regression/test_lc_s14_direction_aware_scoring.py`
- `backend/tests/unit/test_scoring_policy_registry.py`
- `backend/tests/enforcement/test_scoring_policy_not_hardcoded.py`
- `docs/sprints/beta_readiness/P1-4_thyroid_energy_regulation_domain_card.md`
- `docs/sprints/beta_readiness/P1-5_ft3_thyroid_authority_reconciliation.md`
- `docs/architecture/ADR-THYROID-FT3-AUTHORITY-RECONCILIATION-1.md`
- `docs/architecture/ADR-LAYER-BOUNDARY-RECONCILIATION-1.md`
- `docs/sprints/beta_readiness/P1-1_launch_core_domain_build_materials_map.md`
- `docs/strategy/beta_readiness/HEALTHIQ_AI_BETA_READINESS_DEFINITIVE_STRATEGY_FINAL_2026-06-20.md`

## Files changed

- `docs/sprints/beta_readiness/P1-6R_thyroid_scoring_architecture_recovery.md` (created)
- `docs/architecture/ADR-THYROID-SCORING-LAB-RANGE-ARCHITECTURE-1.md` (created)
- `docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md` (P1-6R entry appended)
