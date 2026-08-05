# CLIN-PRIORITY-CORE-1 Checkpoint 2 — Fixture authority alignment notes

**Work ID:** CLIN-PRIORITY-CORE-1  
**Date:** 2026-08-05 (corrected after independent START STOP review)  
**Scope:** Acceptance-scenario fixture expectations vs ratified domain / cross-domain authority

## Purpose

Record where fixture expectations differ from a literal reading of approval-pack v1.2 prose, and how authority hierarchy was applied.

No new clinical thresholds were invented. `[U]` items remain excluded.

## Cross-domain versus generic domain-band tension (corrected)

During START, an apparent tension was identified between:

* ratified **cross-domain** scenario outcomes (ruleset v0.5 §13; approval pack v1.2); and
* subordinate **generic domain urgency bands** (hepatic enzyme ≥10×ULN same-day; sodium same-day Na &lt;125).

Cursor originally resolved that tension **incorrectly** in favour of the subordinate generic domain bands for items 1 and 2 below, and weakened fixture expectations to match. Independent START STOP review applied the governing source hierarchy: the ratified cross-domain ruleset and approved scenario outcomes control these specific cases. Implementation and fixtures were corrected accordingly.

### 1. XD-AS-1 / RE-AS-12 — same-day co-equal (restored)

| Source | Claim |
|---|---|
| Cross-domain ruleset v0.5 §13 / approval pack v1.2 | K⁺ 6.8 + ALT 300 (~6.1× ULN): **both same-day Tier 0**, co-equal group, no ordering, no manufactured lead |
| Generic hepatic enzyme band | ≥5×ULN is within_days; same-day requires ≥10×ULN or absolute &gt;1000 |

**Correction:** Cross-domain / RE-AS-12 outcomes control. `RE-F3` and `HEP-F1` are both `same_day` Tier 0 with `same_day_coequal`. The generic hepatic within_days band must not override this ratified outcome.

### 2. XD-AS-7 — same-day co-equal with artefact caveat (restored)

| Source | Claim |
|---|---|
| Cross-domain ruleset v0.5 / `XD-ARTEFACT-1` / approval pack v1.2 | TG 24 + Na⁺ 128: **both same-day Tier 0**, co-equal; sodium carries mandatory pseudohyponatraemia caveat and must not be suppressed |
| Generic renal sodium band | Same-day hyponatraemia is Na &lt;125; Na 125–129 is within_days |

**Correction:** `XD-ARTEFACT-1` is the governing cross-domain override for this artefact condition. `CN-F1` and `RE-F5` are both `same_day` Tier 0 with `same_day_coequal`; caveat retained without downgrade.

## Retained legitimate alignments (accepted by independent review)

### 3. Hypernatraemia severity bands (XD-AS-15)

Na 152 sits in **151–154 moderate** (146–150 mild; ≥155 same_day). Fixture severity updated from `mild` to `moderate`; `[J]` caveat retained. Arithmetic correction against the ratified band table — not a policy override.

### 4. XD-AS-17 lipid class

Pack inputs TC 8.9 / non-HDL 7.2 do **not** meet specialist thresholds (TC&gt;9 or non-HDL&gt;7.5). With full risk-factor set, fixture expects consolidated `CN-F3` Tier 1 with CV-risk quarantine (R2), not `CN-F2`. Correct application of domain thresholds.

### 5. XD-AS-25 pattern class

R-value ≈2.8 is **mixed** → `HEP-F3` (one consolidated finding with nested constituents). Pack said “one hepatic concern” without forcing F1. Correct application of the governed R-value formula.

## Non-alignments (constructor follows domain rules as written)

- Hy's law (XD-AS-23b): ALT≥3× + bili≥2× + ALP&lt;2× → same_day Tier 0 hepatocellular — implemented.
- FIB-4 / CV-risk % / haemochromatosis consumer naming remain quarantined.
