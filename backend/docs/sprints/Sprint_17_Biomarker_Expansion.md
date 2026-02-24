# Sprint 17 Biomarker Expansion

## Objective
- Expand supported biomarkers in a deterministic, SSOT-first manner for ingestion, scoring, burden mapping, and downstream reporting.
- Add required canonical definitions, aliases, and system mappings for the next target panel without changing arbitration behavior.
- Preserve reproducibility by maintaining stable replay/hash behavior for identical inputs.

## Non-negotiables
- Canonical collision handling remains fail-loud (`canonical_collision`) with no silent fallback or precedence merge.
- Lab-range sovereignty remains intact: primary biomarkers require lab ranges; policy bounds apply only to permitted derived markers.
- Determinism is mandatory: identical inputs must produce stable burden and explainability hashes.
- No fuzzy matching, no inferred metadata, no fallback parser behavior.

## Scope
- SSOT additions/updates where needed:
  - `backend/ssot/biomarkers.yaml` (canonical biomarker definitions, units, categories, systems)
  - `backend/ssot/biomarker_alias_registry.yaml` (raw lab label aliases -> canonical ids)
  - `backend/ssot/system_burden_registry.yaml` (risk_direction/weight/system mapping for burden engine)
  - derived ratio registry/policy files only if new derived markers are explicitly required by panel scope
- No broad refactors; only targeted SSOT + supporting tests + fixture maintenance.

## Validation Plan
- Unit tests:
  - canonical alias resolution and collision guardrails
  - scoring/range-source behavior for newly added biomarkers
  - burden/capacity integration for newly mapped systems/markers
- Enforcement tests:
  - SSOT schema and registry consistency
  - collision invariant remains enforced
- Golden run determinism:
  - run default golden panel twice and compare key hashes (`burden_hash`, `explainability_hash`)
  - run panel-specific mini fixture(s) twice and compare hashes

## Inputs Needed
- AB full panel biomarker list (raw report labels as exported by source lab).
- Marker-by-marker indication of lab-provided reference ranges (present/missing).
- Required derived ratios/markers to compute for this panel.
- Panel-specific naming patterns/quirks (synonyms, casing, punctuation variants).
- Any expected system ownership constraints for new biomarkers.

## Deliverables / Definition of Done
- Required SSOT entries added and validated for Sprint 17 panel scope.
- No canonical collisions in default regression fixture(s); intentional collision fixture remains failing as designed.
- Unit + enforcement tests pass.
- Golden runs complete successfully where expected; deterministic hashes match across repeated runs.
- Collision invariant and lab-range sovereignty behavior unchanged and verified.
