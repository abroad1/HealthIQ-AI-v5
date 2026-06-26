# P2-1 — Prose Substrate Wave 1 Wired

**Work ID:** P2-1  
**Date closed:** 2026-06-26

## 1. Start state

P1-25 and P1-26 activated thyroid and iron/homocysteine MR-v2 signals. Layer C infrastructure existed; `_LEAD_SIGNAL_HINTS` covered homocysteine/MCV only. Iron and thyroid signals could not trigger lead YAML inclusion.

## 2. Confirmed compiler limitation

Frame-level signal-to-frame discrimination remains out of scope. Lead entity selection is signal-scoped via optional `signal_ids` on interpretation entities.

## 3. Behaviour wiring result

Extended `_LEAD_SIGNAL_HINTS` in both narrative compiler modules with iron and thyroid signals. Added signal-aware lead entity selection in `narrative_report_compiler_v1.py` so the top finding routes to the matching `benchmark_lead_domain` entity. Secondary lipid hints unchanged.

## 4. YAML content result

Added iron and thyroid interpretation entities (with `signal_ids`), pathway explainers, and functional interpretation domains from governed P1-25/P1-26 PSI framing. Homocysteine and lipid content preserved.

## 5. Tests / validation result

P2-1 unit tests assert domain-specific lead prose routing for iron, thyroid, and homocysteine; lipid secondary regression; graceful fallback when no scoped entity matches; and claim boundaries.

## 6. Known limitations

Lead prose is one block per report. Frame-level iron-low absolute vs functional and homocysteine B-vitamin vs renal frames remain deferred. Simultaneous six-domain prose awaits `P2-FRAME-ROUTING-ARCHITECTURE-1` if multi-slot design is required.

## 7. Carry-forwards

See `P2-1_prose_substrate_carry_forward.yaml`.

## 8. Recommended next sprint

`P2-FRAME-ROUTING-ARCHITECTURE-1` — signal-aware lead entity selection or multi-slot prose routing design.
