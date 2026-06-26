# P2-1 — Prose Substrate Wave 1 Wired

**Work ID:** P2-1  
**Date closed:** 2026-06-26

## 1. Start state

P1-25 and P1-26 activated thyroid and iron/homocysteine MR-v2 signals. Layer C infrastructure existed; `_LEAD_SIGNAL_HINTS` covered homocysteine/MCV only. Iron and thyroid signals could not trigger lead YAML inclusion.

## 2. Confirmed compiler limitation

Entity loop assigns one lead block via last-match overwrite across `benchmark_lead_domain` rows. Frame-level signal-to-entity routing is out of scope for P2-1.

## 3. Behaviour wiring result

Extended `_LEAD_SIGNAL_HINTS` in both narrative compiler modules with `signal_iron_low`, `signal_iron_high`, `signal_free_t3_low`, and `signal_tpo_ab_high`. Aligned container type to `frozenset` in `narrative_report_compiler_v1.py`. Secondary lipid hints unchanged.

## 4. YAML content result

Added iron and thyroid interpretation entities, pathway explainers, and functional interpretation domains from governed P1-25/P1-26 PSI framing. Homocysteine and lipid content preserved.

## 5. Tests / validation result

P2-1 unit tests cover hint alignment, YAML inclusion flags, lead block emission, homocysteine/lipid regression, claim boundaries, and missing-asset graceful handling.

## 6. Known limitations

Lead prose content follows last-match entity ordering (homocysteine entity last for regression). Signal-specific iron/thyroid pathway prose selection awaits `P2-FRAME-ROUTING-ARCHITECTURE-1`.

## 7. Carry-forwards

See `P2-1_prose_substrate_carry_forward.yaml`.

## 8. Recommended next sprint

`P2-FRAME-ROUTING-ARCHITECTURE-1` — signal-aware lead entity selection or multi-slot prose routing design.
