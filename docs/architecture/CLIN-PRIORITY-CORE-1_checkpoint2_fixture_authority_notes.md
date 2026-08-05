# CLIN-PRIORITY-CORE-1 Checkpoint 2 — Fixture authority alignment notes

**Work ID:** CLIN-PRIORITY-CORE-1  
**Date:** 2026-08-05  
**Scope:** Acceptance-scenario fixture expectations vs ratified domain rules

## Purpose

Where approval-pack v1.2 scenario *narrative* wording conflicted with ratified hepatic / electrolyte numeric rules already compiled into the prioritisation package, fixtures were aligned to the **ratified domain authority**, not to pack prose that implied a different threshold.

No new clinical thresholds were invented. `[U]` items remain excluded.

## Alignments

### 1. ALT 6.1× is not same-day (XD-AS-1, RE-AS-12)

| Source | Claim |
|---|---|
| Approval pack v1.2 (XD-AS-1 / RE-AS-12) | ALT300 (~6.1× ULN) treated as same-day Tier 0 co-equal with K⁺ |
| Hepatic ruleset (ratified) | Same-day enzyme rule requires ≥10× ULN **or** absolute >1000; 5–10× is **within_days Tier 1** |

**Fixture alignment:** `RE-F3` / hyperkalaemia remains same_day Tier 0; `HEP-F1` is within_days Tier 1. Potassium leads on time band. Not `same_day_coequal`.

### 2. Na⁺ 128 is not same-day (XD-AS-7)

| Source | Claim |
|---|---|
| Approval pack v1.2 (XD-AS-7) | Na128 + TG24 as same-day co-equal |
| Renal ruleset (ratified) | Same-day hyponatraemia is Na **&lt;125**; Na 125–129 is within_days |

**Fixture alignment:** `CN-F1` (TG&gt;20) same_day Tier 0; `RE-F5` within_days Tier 1 with pseudohyponatraemia caveat when TG&gt;20.

### 3. Hypernatraemia severity bands (XD-AS-15)

Na 152 sits in **151–154 moderate** (146–150 mild; ≥155 same_day). Fixture severity updated from `mild` to `moderate`; `[J]` caveat retained.

### 4. XD-AS-17 lipid class

Pack inputs TC 8.9 / non-HDL 7.2 do **not** meet specialist thresholds (TC&gt;9 or non-HDL&gt;7.5). With full risk-factor set, fixture expects consolidated `CN-F3` Tier 1 with CV-risk quarantine (R2), not `CN-F2`.

### 5. XD-AS-25 pattern class

R-value ≈2.8 is **mixed** → `HEP-F3` (one consolidated finding with nested constituents). Pack said “one hepatic concern” without forcing F1.

## Non-alignments (constructor follows domain rules as written)

- Hy's law (XD-AS-23b): ALT≥3× + bili≥2× + ALP&lt;2× → same_day Tier 0 hepatocellular — implemented.
- FIB-4 / CV-risk % / haemochromatosis consumer naming remain quarantined.
