# Note to GPT — ARCH-CONV-A Medical Review Wave Plan: resurface for beta-readiness planning
# Claude Code | 2026-08-06

## What this is

Anthony asked me to check what "Wave 1 / Wave 2" documents he half-remembered actually were, while we were discussing main-system/subsystem sequencing. That led to finding `docs/architecture/ARCH-CONV-A_medical_review_wave_plan.md` (2026-07-27) — a 7-wave, organ-system-organised plan for ratifying compiled-WHY medical identity across the remaining signal estate. It is not retired or superseded by anything on record. It appears to have been quietly abandoned in practice, not by decision.

This note is not a recommendation to resume it. It's a surfacing note so the three of us can decide together whether/how it should shape near-term build sequencing toward beta readiness.

## Current state of the plan (repository-verified)

| Wave | Scope | Status |
|---|---|---|
| Wave 0 | Homocysteine elevation-context disposition | **Closed** — `ARCH-CONV-PKGB-1` |
| Wave 1 | Thyroid axis completion | Not started |
| Wave 2 | Lipid / cardiometabolic panel | **Partially closed** — urate (`ARCH-CONV-G`) and HbA1c (`ARCH-CONV-H`) done; rest of the panel unconfirmed |
| Wave 3 | Renal function panel | Not started |
| Wave 4 | Hepatic / biliary panel | **Partially closed** — ALT (`ARCH-CONV-I`) done |
| Wave 5 | Iron / haematology panel | Not started |
| Wave 6 | Metabolic / systemic residual | Not started |

Roughly 2 of 7 waves fully closed, 2 partially closed, 3 untouched.

## Why I'm calling it "stalled" rather than "in progress"

The day-one architecture sprint plan's own carry-forward register — the last thing written against this track, immediately after `ARCH-CONV-I` closed on 2026-08-02 — says explicitly: *"Sequencing note: run a repository-grounded Stage 0 advisory before selecting the next residual (Package B / dual-authority sequencing)."* That advisory was never run. Programme execution instead moved to CLIN-PRIORITY-CORE-1, CLIN-PRIORITY-RESULT-REGEN-1, and the ALT presentation-authority fix — none of which are part of, or a substitute for, this wave plan. No document anywhere records a decision to pause, deprioritise, or abandon it. It just stopped being picked up.

## Why it looked useful to Anthony

Separately, this week I ran a B2 audit of main-system/subsystem completion (`docs/audit-papers/HEALTHIQ_MAIN_SYSTEM_SUBSYSTEM_COMPLETION_AUDIT.md`). Backend domain assembly is done for all 6 launch-core systems; 3 (kidney, blood/iron/oxygen, thyroid) are fully built but never wired into the frontend. That's a different track from this wave plan (domain/subsystem visibility vs. compiled-WHY medical identity per signal), but both are genuine long-view build-planning documents that got separated from active sequencing when CLIN-PRIORITY work took priority. Worth deciding both together, not just this one.

## What's actually being asked of the three of us

Not "should Claude resume the wave plan" — that's not my decision to make. The open questions are:
1. Does the remaining wave-plan work (Waves 1, 3, 5, 6 untouched; Wave 2/4 partial) still matter for beta readiness, or has CLIN-PRIORITY-CORE-1's cross-domain concern-set work made some of it moot (e.g. does per-signal compiled-WHY still matter the same way once cross-domain consolidation exists)?
2. If it still matters, where does it sit relative to the other open sequencing items already on the table (the consumer-copy/presentation programme, the Wave-2 domain-card frontend wiring, the thyroid firing-defect fix)?
3. Who runs the overdue Stage 0 advisory the carry-forward register itself called for, and under what mode (B1/B2)?

I'm not proposing an answer here — this needs GPT's architecture-governance view and Anthony's product-priority call, then I can harden whatever gets decided.
