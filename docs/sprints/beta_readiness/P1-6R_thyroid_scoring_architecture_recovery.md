# P1-6R — Thyroid Scoring Architecture Recovery and Lab-Range Rail Decision

## 1. Summary

- **Why this recovery sprint was required:** Failed sprint P1-6 (`work/P1-6-thyroid-launch-core-unlock-and-domain-card`) violated STOP gates by adding hardcoded TSH/FT3/FT4 scoring bands, modifying prohibited Intelligence Core files, creating thyroid domain/compiled artefacts, and extending DTO/replay contracts. That branch was abandoned. P1-6R establishes the scoring architecture truth before any thyroid runtime work is retried.
- **Main confirmed clean:** Yes. Baseline `main` at `51f087d0861adc39c963eb83c457e6876f5f4c95`; local equals `origin/main`. No failed P1-6 artefacts on main. Failed branch exists locally but is not merged.
- **Lab-range-only thyroid scoring supported?** **No.** The scoring primitive (`calculate_biomarker_score`) can score from lab reference ranges alone, but system orchestration requires a loaded `BiomarkerRule`, and rule construction requires a full six-band YAML block. Bandless hormonal entries are silently dropped at load time.
- **Thyroid scoring/domain implementation blocked?** **Yes.** Hormonal rail remains inert; scoring-engine architecture must change before thyroid markers can be added without hardcoded bands.
- **Recommended next sprint:** **P1-SCORING-LAB-RANGE-ENGINE** — governed scoring-engine change to support bandless biomarker membership with lab-range-only runtime scoring, before any hormonal scoring-policy or P1-4 domain-card retry.

## 2. Recovery verification

| Check | Result |
|---|---|
| Starting branch | `main` @ `51f087d0861adc39c963eb83c457e6876f5f4c95` |
| Sprint branch | `work/P1-6R-thyroid-scoring-architecture-recovery` |
| Failed P1-6 branch merged? | **No** — `git merge-base --is-ancestor work/P1-6-thyroid-launch-core-unlock-and-domain-card main` returned non-zero |
| Failed P1-6 files on main? | **Absent** — all four contamination paths return `False` via `Test-Path` |
| Failed branch files reused? | **No** — no cherry-pick, copy, or salvage from `work/P1-6-thyroid-launch-core-unlock-and-domain-card` |

Contamination paths verified absent:

- `docs/sprints/beta_readiness/P1-6_thyroid_launch_core_unlock_and_domain_card.md`
- `docs/architecture/ADR-THYROID-LAUNCH-CORE-UNLOCK-1.md`
- `knowledge_bus/compiled/health_system_cards/wave1_thy_thyroid_axis.yaml`
- `knowledge_bus/compiled/manifests/p1_6_thyroid_energy_axis_card_evidence.yaml`

## 3. Authority baseline

| Document | Role in P1-6R |
|---|---|
| `docs/strategy/beta_readiness/HEALTHIQ_AI_BETA_READINESS_DEFINITIVE_STRATEGY_FINAL_2026-06-20.md` | Eight-block programme baseline; thyroid domain deferred until authority and scoring rails resolved |
| `docs/sprints/beta_readiness/P1-1_launch_core_domain_build_materials_map.md` | Thyroid rated partial readiness; FT3 register drift documented; kb52c TSH and kb59 antibodies inactive |
| `docs/sprints/beta_readiness/P1-4_thyroid_energy_regulation_domain_card.md` | STOP report: inert hormonal rail, TSH gap, FT3 low conflict (pre-P1-5) |
| `docs/sprints/beta_readiness/P1-5_ft3_thyroid_authority_reconciliation.md` | FT3 low reconciled to deferred/inactive; P1-4 retry still requires scoring rail + TSH authority |
| `docs/architecture/ADR-THYROID-FT3-AUTHORITY-RECONCILIATION-1.md` | Authoritative launch positions for all thyroid patterns; FT3 low deferred |
| `docs/architecture/ADR-LAYER-BOUNDARY-RECONCILIATION-1.md` | Layer A preserves lab ranges; Layer B owns scoring; no Layer C reasoning in scoring paths |

P1-5 and ADR-THYROID-FT3-AUTHORITY-RECONCILIATION-1 are authoritative for FT3 low: **deferred / inactive / not launch-visible.**

## 4. Scoring architecture audit

### Scoring files inspected

| Path | Purpose |
|---|---|
| `backend/ssot/scoring_policy.yaml` | SSOT policy: systems, biomarkers, bands, directionality |
| `backend/core/analytics/scoring_policy_registry.py` | Policy loader and schema validator |
| `backend/core/scoring/rules.py` | `BiomarkerRule` construction, `calculate_biomarker_score` |
| `backend/core/scoring/engine.py` | System orchestration via `_score_health_system` |
| `backend/tests/unit/test_scoring_rules.py` | Biomarker scoring behaviour |
| `backend/tests/test_scoring_lab_range_only.py` | Lab-range-only primitive and SSOT non-invocation |
| `backend/tests/regression/test_lc_s14_direction_aware_scoring.py` | Directionality-aware lab-range scoring |
| `backend/tests/unit/test_scoring_policy_registry.py` | Band schema validation at load time |
| `backend/tests/enforcement/test_scoring_policy_not_hardcoded.py` | Policy literals live in YAML not code |

### How `scoring_policy.yaml` is loaded

`load_scoring_policy()` in `backend/core/analytics/scoring_policy_registry.py` reads `backend/ssot/scoring_policy.yaml`, validates structure, and caches a stamped policy. `ScoringRules.__init__` calls this loader at `rules.py:112`.

### How `BiomarkerRule` objects are constructed

`_load_biomarker_rules()` (`rules.py:147-163`) iterates each system's `biomarkers` list, looks up each name in the YAML `biomarkers` dict, and calls `_build_biomarker_rule()` only when the entry is a dict.

`_build_biomarker_rule()` (`rules.py:131-145`) reads `item.get("bands", {})` then accesses **direct dict keys** `bands["optimal"]`, `bands["normal"]`, `bands["borderline"]`, `bands["high"]`, `bands["very_high"]`, `bands["critical"]`. Missing any key raises `KeyError` at load time.

### Whether bands are schema/constructor-required

**Yes — at two independent layers:**

1. **Schema validation** (`scoring_policy_registry.py:64-78`): every entry in the `biomarkers` mapping must have a `bands` dict with all six named sub-bands, each with numeric `min`/`max`.
2. **Rule construction** (`rules.py:131-145`): direct key access with no `.get()` fallback.

Bands are **not** used as runtime scoring fallback for lab-provided biomarkers. `calculate_biomarker_score()` (`rules.py:361-436`) explicitly states lab-provided biomarkers use **only** lab reference ranges and never SSOT/rule fallback (`rules.py:423-425`). The `BiomarkerRule` band tuples are used by legacy helpers `_determine_score_range` and `_calculate_range_score` (`rules.py:565-598`) which are **not** invoked from `calculate_biomarker_score`.

### Whether lab-provided ranges are used during scoring

**Yes — at the primitive level.** When `input_reference_range` is provided with valid min/max, scoring uses `position_in_range`, `position_in_one_sided_lab_range`, and directionality overrides (`rules.py:381-421`). Proven by `backend/tests/test_scoring_lab_range_only.py` and `backend/tests/unit/test_scoring_rules.py`.

### Whether a lab-range-only path exists at system-orchestration level

**No — not for bandless biomarkers.** `_score_health_system()` (`engine.py:192-212`) iterates only `system_rules.biomarkers`, which contains only successfully loaded `BiomarkerRule` instances. A biomarker listed under `systems.hormonal.biomarkers` without a corresponding `biomarkers:` YAML entry is **silently skipped** at `rules.py:154-156` (`if isinstance(policy_item, dict)` guard).

### Whether directionality-only scoring exists

**Partially.** `biomarker_directionality.markers` (`scoring_policy.yaml:288-308`) supplies `direction_class` for markers already in the biomarkers block (e.g. glucose, crp). Directionality adjusts interpretation of lab-range position (`rules.py:197-247`) but **does not substitute for band blocks** at rule-load time. No thyroid markers appear in directionality.

### Audit question answers

| # | Question | Answer |
|---|---|---|
| 1 | Does scoring_policy.yaml require biomarker bands for every scored biomarker? | **Yes** — schema validator requires all six bands for every `biomarkers` entry; system membership requires a matching biomarkers dict entry |
| 2 | Are bands fallback or required to construct rules? | **Required for construction** — not used as runtime scoring fallback for lab biomarkers |
| 3 | Does engine support lab-range-only scoring without bands? | **Primitive yes, orchestration no** — `calculate_biomarker_score` supports it; system loop does not reach bandless biomarkers |
| 4 | Does engine support directionality-only without bands? | **No** — directionality augments lab-range scoring for loaded rules only |
| 5 | Can a biomarker be listed under a system without a bands block? | **Listed yes, loaded no** — silent skip; never enters `system_rules.biomarkers` |
| 6 | Biomarker in panel with lab range but absent from scoring_policy biomarkers? | **Not scored via system orchestration** — not in system loop; direct call to `calculate_biomarker_score` would return unscored (`missing_lab_reference_range`) without a rule for unit check, or score if called directly with lab range |
| 7 | Biomarker in scoring_policy with directionality but no bands? | **Cannot exist** — schema validation fails at load; directionality alone is insufficient |
| 8 | Tests proving behaviour? | `test_scoring_lab_range_only.py`, `test_scoring_rules.py`, `test_lc_s14_direction_aware_scoring.py`, `test_scoring_policy_registry.py` (band validation) |
| 9 | TSH/FT4/FT3 added to hormonal rail without bands? | **Silently dropped** — no BiomarkerRule constructed; hormonal system score unchanged (weight 0.0 anyway) |
| 10 | Safe existing policy pattern for thyroid now? | **None** — hormonal rail empty (`scoring_policy.yaml:31-34`); no bandless pattern exists |

### Current hormonal rail state

```yaml
# backend/ssot/scoring_policy.yaml:31-34
hormonal:
  min_biomarkers_required: 0
  system_weight: 0.0
  biomarkers: []
```

No TSH, FT3, FT4, or thyroid antibody entries exist anywhere in the biomarkers or directionality sections.

## 5. Thyroid marker scoring feasibility table

| Marker | Authority position | Signal status | Can be scored now without hardcoded bands? | Reason | Remaining blocker |
|---|---|---|---|---|---|
| TSH | SSOT present (`biomarkers.yaml`); scoring rail absent | kb52c packages **not launch-active** (P1-5) | **No** | System orchestration requires bands block to load rule; no bandless pattern; hormonal rail empty | Scoring-engine architecture change + TSH launch authority sprint |
| FT4 / free_t4 | SSOT present; scoring rail absent | FT4 high/low runtime_active_canonical with TSH gates (P1-5 ADR) | **No** | Same band requirement at rule load; bands would be hardcoded clinical thresholds if added now | Scoring-engine architecture change before policy sprint |
| FT3 / free_t3 | SSOT present; scoring rail absent | FT3 high gated; **FT3 low deferred/inactive** (P1-5) | **No** | Same band requirement; FT3 low must not be activated | Scoring-engine architecture change + FT3 low remains deferred |
| Thyroid antibodies (tpo_ab, tgab) | SSOT present; scoring rail absent | kb59 packages **inactive** (P1-5) | **No** | Same band requirement; no antibody bands or rail | Scoring-engine architecture change + kb59 promotion governance |

## 6. Architectural decision

**Existing architecture does not support safe lab-range-only thyroid scoring yet.**

**Why (Phase 3 outcome B):**

The product correctly treats lab-provided reference ranges as authoritative at runtime (`rules.py:3-4`, `rules.py:423-425`). However, **membership in a scored health system requires a YAML biomarker entry with six hardcoded band sub-ranges**, enforced by both schema validation (`scoring_policy_registry.py:71-78`) and constructor key access (`rules.py:135-140`). Adding TSH/FT3/FT4 to the hormonal system list without bands produces **silent non-scoring** (`rules.py:154-156`), not lab-range scoring.

Failed P1-6 attempted to bypass this by adding hardcoded thyroid bands — exactly the anti-pattern this recovery sprint rejects. The safe path is a **scoring-engine architecture sprint** introducing a governed bandless biomarker pattern (e.g. `scoring_type: lab_range_only`) that loads into system orchestration without clinical threshold bands, then a separate scoring-policy sprint listing thyroid markers under that pattern.

## 7. P1-4 / thyroid domain-card status

| Item | Status |
|---|---|
| P1-4 retry permitted? | **No** — preconditions from P1-5 remain unmet |
| Thyroid domain card blocked? | **Yes** |
| TSH authority blocker? | **Yes** — kb52c not launch-active |
| Hormonal scoring rail blocker? | **Yes** — rail inert and architecture cannot accept bandless entries |

P1-4 retry requires, at minimum:

1. Scoring-engine architecture change (this sprint's recommended next step)
2. Governed hormonal scoring-policy sprint using the new pattern (not hardcoded bands)
3. TSH launch authority resolution (separate governance sprint)

FT3 low must remain excluded from launch domain allowlists.

## 8. Future implementation recommendation

### Next sprint: P1-SCORING-LAB-RANGE-ENGINE

| Field | Value |
|---|---|
| Title | Lab-range-only biomarker scoring rule pattern |
| Risk level | HIGH |
| Change type | BEHAVIOUR |
| May change | `backend/core/scoring/rules.py`, `backend/core/analytics/scoring_policy_registry.py` (schema extension), `backend/ssot/scoring_policy.yaml` (pattern definition only — no thyroid bands), targeted tests |
| Must not change | Domain assembler, compiled cards, DTO/replay, narrative wave, frontend, Gemini, fallback parsers, thyroid signal activation, FT3 low activation |
| STOP gates | No hardcoded global/default thyroid ranges; no placeholder clinical-unit bands; no thyroid domain row; no signal activation; identical input → identical output |

### Sequence after engine sprint

1. **P1-SCORING-HORMONAL-POLICY** (CONTENT/MIXED) — add tsh, free_t4, free_t3 under lab-range-only pattern; set hormonal `system_weight` and `min_biomarkers_required`; **no six-band blocks**
2. **P1-TSH-PROMOTION** (governance) — kb52c launch authority
3. **P1-4 retry** — thyroid domain card only after 1–3

| Question | Answer |
|---|---|
| Can scoring_policy.yaml change safely in next sprint? | **Not until engine sprint completes** |
| Must scoring-engine code change first? | **Yes** |
| Thyroid domain card blocked? | **Yes** |
| TSH package authority separate blocker? | **Yes** |
| P1-4 retry blocked? | **Yes** |

## 9. Safety and architecture boundaries

Confirmed — this sprint made **no** changes to:

- Runtime code (`backend/core/`, `backend/ssot/scoring_policy.yaml`)
- Thyroid compiled card or domain row
- DTO/replay contract
- Frontend / Gemini / fallback parser
- Knowledge Bus source packages or Pass 3 material
- Thyroid signal activation

Deliverables are documentation only.

## 10. Validation

Commands run:

```powershell
git branch --show-current
git status --short
git stash list
git merge-base --is-ancestor work/P1-6-thyroid-launch-core-unlock-and-domain-card main
git rev-parse main
Test-Path docs/sprints/beta_readiness/P1-6_thyroid_launch_core_unlock_and_domain_card.md
Test-Path knowledge_bus/compiled/health_system_cards/wave1_thy_thyroid_axis.yaml
git diff --stat
git diff --name-only
```

Results:

- Branch: `work/P1-6R-thyroid-scoring-architecture-recovery`
- Stash: empty
- P1-6 not merged: confirmed
- Main SHA: `51f087d0861adc39c963eb83c457e6876f5f4c95`
- Contamination files: absent
- Runtime/code files changed: none (docs only)

## 11. Recommended next sprint

**P1-SCORING-LAB-RANGE-ENGINE** — Add a governed scoring-engine pattern allowing biomarkers to join a health system rail and score exclusively from lab-provided reference ranges without hardcoded band blocks. This unblocks a subsequent hormonal scoring-policy sprint and is prerequisite to P1-4 retry. TSH promotion governance remains a parallel/separate blocker.
