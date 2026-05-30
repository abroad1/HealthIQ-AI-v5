# ARCH-RT-5 M4 — PSI Opt-In and Runtime Wiring Audit

**Generated:** 2026-05-30

## PSI posture

| Rule | Status |
|------|--------|
| PSI remains signal-layer semantics only | **CONFIRMED** |
| PSI not hypothesis graph | **CONFIRMED** |
| PSI not card evidence authority | **CONFIRMED** |
| PSI runtime consumed for launch-critical card/report claims | **Not required** for Wave 1 launch slice |

## Runtime usage scan

| Surface | PSI wired? |
|---------|------------|
| Health Systems Card evidence | No |
| Root-cause compiler | No |
| SignalRegistry / SignalEvaluator | No changes in ARCH-RT-5 |

## Gap classification

| Gap | Classification |
|-----|----------------|
| PSI runtime wiring for launch-critical claims | **deferred_non_launch_blocker** |
| PSI opt-in packages without runtime join | Documented in `psi_coverage_and_manifest_opt_in_report.md` |

## M4 outcome

**Complete.** PSI wiring explicitly **deferred_non_launch_blocker** with justification: Wave 1 launch path does not require PSI runtime for governed card/root-cause pilots completed in ARCH-RT-3/4.
