# HealthIQ AI — AB Gold Standard Narrative Target Lock

## Purpose
This note formally locks the AB gold-standard narrative benchmark as the target-state narrative reference for the deterministic narrative workstream defined in `docs/golden-narrative/HealthIQ_Deterministic_Narrative_Sprint_Strategy_FINAL.md`.

Its role is to prevent drift in later sprints by making clear which benchmark narrative is authoritative for comparison, what it is being used for, and what it must not be mistaken for.

## Approved benchmark file
The approved benchmark narrative for this workstream is:

`docs/golden-narrative/AB_GOLD_STANDARD_NARRATIVE_REPORT_CHAT_2_FINAL.md`

This is the benchmark file that later deterministic narrative sprints must use when assessing supportability, gap closure, and runtime quality.

## What the benchmark is
- A target-state narrative standard for the AB case.
- A benchmark for reverse-engineering deterministic support requirements.
- A reference artifact for identifying missing data/contract support, governed narrative assets, compiler layers, and output structures.
- A comparison target for future runtime validation sprints.

## What the benchmark is not
- Not current product truth.
- Not current deterministic runtime output.
- Not a copy deck to paste into frontend components.
- Not itself an authoritative backend asset.
- Not a substitute for governed SSOT, Knowledge Bus assets, contracts, compilers, or report outputs.

## How later sprints must use it
Later sprints must use the benchmark in the following controlled way:

1. Treat it as the target narrative behaviour to support deterministically.
2. Work backwards from its narrative moves into governed asset and compiler requirements.
3. Compare future compiled runtime outputs against it for structure, supportability, and quality.
4. Avoid copying benchmark prose directly into product outputs unless and until equivalent governed deterministic assets and compilers exist.
5. Keep authority distinctions explicit:
   - benchmark target
   - authoritative source files
   - fixtures/examples
   - compiled outputs
   - display-layer artifacts

## Relation to the final sprint strategy
This target lock is the authority anchor for Sprint `N-1` in:

`docs/golden-narrative/HealthIQ_Deterministic_Narrative_Sprint_Strategy_FINAL.md`

That strategy defines the broader deterministic narrative support stack and the planned sprint sequence. This file defines the benchmark reference that the strategy is organizing around.

## Related source authorities
The key supporting authority files for this lock are:

- `docs/golden-narrative/AB_GOLD_STANDARD_NARRATIVE_REVERSE_ENGINEERING_CURSOR.md`
- `docs/golden-narrative/AB_GOLD_STANDARD_NARRATIVE_REVERSE_ENGINEERING_CLAUDE.md`
- `docs/golden-narrative/HealthIQ_Deterministic_Narrative_Sprint_Strategy_FINAL.md`

## Authority statement
For the deterministic narrative sprint family, `AB_GOLD_STANDARD_NARRATIVE_REPORT_CHAT_2_FINAL.md` is now the approved target-state benchmark narrative reference for the AB case.
