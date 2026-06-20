# P1-8 — Scoring Lab-Range Engine

## 1. Summary

- **Architecture blocker addressed:** P1-6R proved that biomarker bands were structurally required at schema validation and `BiomarkerRule` construction, blocking lab-range-only system membership even though `calculate_biomarker_score()` already scored from lab ranges at the primitive level.
- **Lab-range-only scoring supported?** **Yes** — via explicit `scoring_type: lab_range_only` policy entries that load into system orchestration without bands.
- **Production thyroid scoring:** **Still blocked** — production `scoring_policy.yaml` unchanged; hormonal rail remains inert; no TSH/FT3/FT4 entries.
- **What changed:** `scoring_policy_registry.py` validator extended; `BiomarkerRule` supports optional bands; `_build_biomarker_rule()` branches on `scoring_type`; targeted tests added.

## 2. Authority baseline

| Document | Role |
|---|---|
| P1-6R recovery report | Identified band requirement at load time vs lab-range primitive |
| ADR-THYROID-SCORING-LAB-RANGE-ARCHITECTURE-1 | Required engine sprint before hormonal policy |
| P1-7 adequacy gate | Confirmed systemic promotion gap; recommended this sprint |
| ADR-LAYER-BOUNDARY-RECONCILIATION-1 | Layer A lab ranges authoritative; scoring is Layer B |

## 3. Existing scoring architecture before P1-8

- **Band-based scoring:** All production biomarkers declared `scoring_type: range_position` with six YAML band sub-ranges. Runtime scoring used lab reference ranges in `calculate_biomarker_score()`, not band tuples.
- **Where bands were required:** `scoring_policy_registry.py:69-78` rejected any non-`range_position` type and required all six bands. `rules.py:131-145` accessed band keys unconditionally. `BiomarkerRule` required six non-optional band tuple fields.
- **Why thyroid was blocked:** Cannot add TSH/FT3/FT4 to hormonal system without either hardcoded bands (P1-6 anti-pattern) or silent drop at load (`rules.py:154-156`).

## 4. Design decision

### Chosen pattern

```yaml
biomarker_id:
  scoring_type: lab_range_only
  unit: "<canonical unit>"
  weight: <float>
  # bands: MUST NOT be present
```

- **Explicit and governed:** Only `scoring_type: lab_range_only` activates bandless rule construction. `range_position` remains the default; all existing biomarkers unchanged.
- **No global/default ranges:** Scoring still uses `input_reference_range` only; missing lab range returns `missing_lab_reference_range`.
- **Preserves existing scoring:** Production policy untouched; all existing biomarkers remain `range_position` with bands; regression tests pass unchanged.

### Implementation details

- `BiomarkerRule` gains `scoring_type` and optional band fields (`None` for lab-range-only).
- Legacy `_determine_score_range` / `_calculate_range_score` guard against bandless rules (not used by live scoring path).
- Tests use isolated fixture policy (`fixture_lab_range_marker`) — not production thyroid markers.

## 5. Runtime/code changes

| File | Change |
|---|---|
| `backend/core/analytics/scoring_policy_registry.py` | Accept `lab_range_only`; validate unit required, bands forbidden |
| `backend/core/scoring/rules.py` | `BiomarkerRule` optional bands; `_build_biomarker_rule()` branch; band-method guards |
| `backend/tests/unit/test_scoring_lab_range_only_rules.py` | New P1-8 test suite with fixture policy |
| `backend/tests/unit/test_scoring_rules.py` | Skip band-order checks for `lab_range_only` rules |

**Production scoring policy impact:** **None** — `backend/ssot/scoring_policy.yaml` unchanged.

## 6. Safety boundaries

Confirmed:

- No placeholder bands
- No hardcoded global/default clinical ranges
- No thyroid signal activation
- No thyroid domain card, compiled card, DTO row, narrative, frontend, Gemini, or fallback parser
- No Knowledge Bus source packages or Pass 3 artefacts changed
- No forbidden analytics/knowledge files modified

## 7. Tests and validation

**Tests added/updated:**

- `backend/tests/unit/test_scoring_lab_range_only_rules.py` (11 tests)
- `backend/tests/unit/test_scoring_rules.py` (lab_range_only skip in validation)

**Commands run:**

```powershell
python -m pytest backend/tests/unit/test_scoring_rules.py backend/tests/unit/test_scoring_lab_range_only_rules.py backend/tests/test_scoring_lab_range_only.py backend/tests/unit/test_scoring_policy_registry.py -q
```

**Result:** 47 passed.

**Limitations:** Full-engine `score_biomarkers()` integration requires canonical biomarker SSOT registration; system orchestration path verified via `_score_health_system` with injected rules and canonical dict.

## 8. Effect on thyroid programme

| Question | Answer |
|---|---|
| Hormonal rail safely enableable in later sprint? | **Yes, architecturally** — future sprint may add `lab_range_only` entries for tsh/free_t3/free_t4 with governed units and directionality, plus non-zero `system_weight` |
| P1-4 retry still blocked? | **Yes** — TSH kb52c launch authority, compiled thyroid card, domain assembler, and hormonal policy activation remain separate preconditions |
| What must happen next | P1-SCORING-HORMONAL-POLICY sprint (add lab_range_only markers to policy + enable rail); TSH promotion governance; then P1-4 retry |

## 9. Carry-forwards

- Populate hormonal scoring rail with `lab_range_only` entries (separate sprint)
- TSH package authority (kb52c)
- Thyroid domain card (P1-4 retry)
- eGFR and iron markers may also benefit from `lab_range_only` pattern in future policy sprints

## 10. Recommended next sprint

**P1-SCORING-HORMONAL-POLICY** — Add governed `lab_range_only` entries for thyroid-axis markers (minimum TSH + FT4), set hormonal `system_weight` and `min_biomarkers_required`, with medical sign-off and no FT3 low activation. STOP if TSH launch authority unresolved.
