# ADR-THYROID-TSH-LAUNCH-SCORING-ONLY-1 — TSH Launch Scoring vs Signal Intelligence

## Status

Accepted — P1-22 bounded launch decision.

## Date

2026-06-22

## Context

P1-4 stopped because the hormonal scoring rail was inert and TSH launch authority was ambiguous relative to kb52c packages. P1-8 delivered `lab_range_only` scoring engine support. ADR-THYROID-FT3-AUTHORITY-RECONCILIATION-1 records that TSH high/low signal intelligence is not launch-active while kb47 FT3/FT4 signals are cleared with companion gates.

P1-22 activates `wave1_thyroid` as the final launch-core domain.

## Decision

1. **TSH enters hormonal `lab_range_only` scoring at launch** — lab-provided reference ranges remain authoritative; no hardcoded production bands.
2. **TSH signal intelligence is not promoted in P1-22** — kb52c TSH packages and legacy s24 TSH signals remain outside the thyroid domain launch allowlist.
3. **Domain output must not imply TSH clinical-context intelligence is active** — TSH contributes lab-range scoring/status only via the hormonal rail.
4. **FT3 high, FT4 high, and FT4 low** may appear in `active_signal_ids` per ADR-THYROID-FT3-AUTHORITY-RECONCILIATION-1 companion-gate rules already enforced in SignalEvaluator.
5. **FT3 low remains excluded** from all thyroid domain allowlists and activation paths.

## Consequences

- `wave1_thyroid` domain card uses hormonal scoring rail for TSH/FT4/FT3 lab-range status.
- TSH kb52c promotion remains a separate Knowledge Bus / Medical Review sprint.
- Compiled thyroid subsystem card evidence remains a follow-on sprint.

## References

- `docs/architecture/ADR-THYROID-FT3-AUTHORITY-RECONCILIATION-1.md`
- `docs/sprints/beta_readiness/P1-4_thyroid_energy_regulation_domain_card.md`
- `backend/ssot/scoring_policy.yaml`
