# KB-UTIL-1 — Pass 3 Card Evidence Compile and Consume Report

**Work ID:** `KB-UTIL-1_pass3_card_evidence_compile_and_consume`  
**Branch:** `work/KB-UTIL-1-pass3-card-evidence-compile-and-consume`  
**Change type:** MIXED (Layer A compiled enrichment + Layer B DTO + Layer C render)  
**Audit status:** Narrative alignment defects fixed — **ready for Claude re-audit** (2026-05-31)

## Preflight findings

| Check | Result |
|---|---|
| Baseline | `main` @ `db530e2` == `origin/main` before activation commit |
| MED-REV-1/2 merged | Yes |
| Carry-forward register | Present; updated in this sprint |
| Visible Wave 1 surfaces | Atherogenic lipid pattern, Long-term blood sugar, liver flat model |
| Pass 3 runtime reads | Not required — compile-time enrichment from packages into YAML |

## Pass 3 / package fields assessed

| Field family | Compiled (KB-UTIL-1) | Deferred |
|---|---|---|
| `explanation.mechanism` / `supporting_marker_roles` | → `mechanism_line`, `subsystem_summary`, `domain_summary_line` | — |
| `supporting_metrics[].rationale` | → `rationale_short` on markers | — |
| `relationship_kind` / `marker_role` | Already in schema; preserved in DTO | UI chips only (no inference) |
| `missing_policy_line` | Preserved + rendered | — |
| `evidence_limitations_line` | New governed scope lines | — |
| `hypotheses[]`, `contradiction_markers`, `confirmatory_tests` | — | CF-KBUTIL1-002 |
| Full estate automated compiler | — | CF-KBUTIL1-001 |

## Selected enrichment model

**Subsystem artefacts (lipid, glycaemic):** optional `subsystem_summary`, `evidence_limitations_line`, enriched `rationale_short` / `mechanism_line`.

**Liver flat artefact:** `wave1_liver_flat_v1.yaml` (`domain_flat_card_evidence_v1`) → `DomainFlatEvidenceV1` on `ConsumerDomainScoreV1.flat_domain_evidence`.

## Artefacts changed

- `knowledge_bus/schema/health_system_card_evidence_schema_v1.yaml` — optional enrichment fields
- `knowledge_bus/schema/health_system_domain_flat_evidence_schema_v1.yaml` — new
- `knowledge_bus/compiled/health_system_cards/wave1_cv_lipid_transport.yaml` — KB-UTIL-1 enrichment
- `knowledge_bus/compiled/health_system_cards/wave1_met_glycaemic_control.yaml` — KB-UTIL-1 enrichment
- `knowledge_bus/compiled/health_system_cards/wave1_liver_flat_v1.yaml` — new flat liver model
- `knowledge_bus/compiled/manifests/kb_util1_*.yaml` — compile manifests (SHA-256 output hashes refreshed)

## Layer B changes

- `backend/core/knowledge/health_system_card_evidence.py` — pass through enrichment fields; `kb_util1_package_enrichment` compile status
- `backend/core/knowledge/domain_flat_card_evidence.py` — new flat loader/assembler
- `backend/core/models/results.py` — `SubsystemEvidenceV1` enrichment fields; `DomainFlatEvidenceV1`; `ConsumerDomainScoreV1.flat_domain_evidence`
- `backend/core/analytics/wave1_subsystem_evidence.py` — `assemble_wave1_flat_domain_evidence`
- `backend/core/analytics/domain_score_assembler.py` — liver attaches `flat_domain_evidence`; flat completeness; lipid/glycaemic narrative authority wiring
- `backend/core/analytics/domain_narrative_wave1.py` — visible-subsystem narrative alignment (CV lipid-only, MET HbA1c limited-coverage, liver D-7 band gate)
- `backend/scripts/validate_day_one_architecture.py` — `validate_kb_util1_wave1_card_enrichment`; `domain_flat_card_evidence.py` in launch-critical paths; KB-UTIL-1 manifests in compile manifest validation

## Layer C changes

- `frontend/app/types/analysis.ts` — mirror new DTO fields
- `frontend/app/components/results/Wave1SubsystemEvidenceSection.tsx` — render summary, limitations, missing policy, rationales
- `frontend/app/components/results/Wave1FlatDomainEvidenceSection.tsx` — new flat liver panel evidence
- `frontend/app/components/results/Wave1DomainCards.tsx` — wire flat section

## Evidence preservation

- Marker IDs and thresholds unchanged; `total_bilirubin` prohibition intact
- MED-REV-1 hidden subsystems remain `hidden_v1` with `None` DTO emission
- No scoring rails, SignalEvaluator, or activation threshold changes

## Hidden subsystem protection

Regression tests assert all `WAVE1_MED_REV1_HIDDEN_SUBSYSTEM_IDS` still suppress DTO rows. Lipid limitations line explicitly excludes inflammation/homocysteine as score basis.

## Carry-forward register updates

Added `CF-KBUTIL1-001` (automated compile pipeline) and `CF-KBUTIL1-002` (hypotheses/contradictions deferred).

## Tests run

```powershell
python backend/scripts/validate_day_one_architecture.py
python -m pytest backend/tests/architecture/test_day_one_architecture_guardrails.py -q
python -m pytest backend/tests/regression/test_kb_util1_pass3_card_evidence_compile_and_consume.py -q
python -m pytest backend/tests/regression/test_med_rev1_wave1_subsystem_visibility.py -q
python -m pytest backend/tests/regression/test_med_rev2_domain_card_copy_and_regeneration.py -q
python -m pytest backend/tests/unit/test_health_system_card_evidence_arch_rt3.py -q
```

All PASS (including four UAT-defect regression tests added 2026-05-31).

## Human UAT narrative alignment defects (fixed 2026-05-31)

Human UAT on regenerated `70601969-87e1-4968-b0f8-3dfee55d9472` found score/copy/evidence misalignment on collapsed card prose despite enriched evidence panels passing. Root cause: Layer B narrative still followed hidden IDL pathways (homocysteine/inflammation, HbA1c strain copy, rail-based liver completeness) instead of visible subsystem / flat evidence authority.

| # | Defect | Source traced | Fix (Layer B) |
|---|---|---|---|
| 1 | CV anchor “Atherogenic lipid pattern” but “Why this score” cited inflammation/homocysteine | `cv_contributor_primary` + `ph_vascular_hcy_inflammation_v1` IDL won when lipid IDL `not_observed` | `cv_uses_lipid_subsystem_narrative_authority` → lipid-only contributor/consequence when visible scored subsystem is `wave1_cv_lipid_transport` |
| 2 | Blood sugar 100/100 Strong with HbA1c-only limited coverage implied active glycaemic strain | `met_consequence_primary` / `headline_met_coherent` pulled governed HbA1c `why_it_matters` and conflict headline | `met_consequence_for_glycaemic_visible_card` + limited-coverage headline gate when contributor reads in-range / markers not included |
| 3 | Liver completeness “1 of 2” vs flat panel showing 5 included markers | `_wave1_card_contract_extras` fell back to scoring-rail completeness when `subsystems` empty | `_evidence_completeness_from_flat_domain` applied after `assemble_wave1_flat_domain_evidence` |
| 4 | Liver consequence overclaimed MASLD/fibrosis on stable limited flat read | `liv_consequence_primary` D-7 gate blocked by non-enzyme `active_signal_ids` | Band-aware neutral gate: stable/strong surface without enzyme-strain signals uses proportionate consequence |

Regression coverage: `test_cv_why_this_score_aligns_with_lipid_visible_subsystem_not_hcy_inflammation`, `test_blood_sugar_strong_hba1c_only_does_not_imply_active_glycaemic_strain`, `test_liver_flat_completeness_matches_flat_marker_model`, `test_liver_stable_limited_flat_card_does_not_overclaim_masld_fibrosis`.

**Re-UAT note:** Regenerate from `746f2b0a-b470-4d87-8ed8-e2c3d1e68c02` after backend reload to produce a fresh sibling analysis with corrected collapsed-card copy.

## Manual validation

**Executed:** 2026-05-31  
**Operator:** Cursor agent (browser + authenticated API)  
**Login:** `test-user3@example.com`  
**Method:** Regenerated from preserved upload via `POST /api/analysis/746f2b0a-b470-4d87-8ed8-e2c3d1e68c02/regenerate` (not stale snapshot)

**Regenerated analysis ID:** `70601969-87e1-4968-b0f8-3dfee55d9472`  
**URL:** `http://localhost:3000/results?analysis_id=70601969-87e1-4968-b0f8-3dfee55d9472`

**Stale control (immutable snapshot):** `746f2b0a-b470-4d87-8ed8-e2c3d1e68c02` — API confirms 3 legacy subsystem rows (Lipid transport, Homocysteine pathway, Vascular strain context) with no `subsystem_summary`; not used for enrichment UAT.

### Browser UAT checklist

| # | Criterion | Result | Evidence |
|---|---|---|---|
| 1 | Enriched lipid evidence renders correctly | **PASS** | Expanded CV card: subsystem summary (LDL/HDL/TG balance), mechanism line, limitations line (“does not treat inflammation or homocysteine as the score basis”), per-marker rationales with role chips |
| 2 | Enriched glycaemic evidence renders correctly | **PASS** | Expanded MET card: “Long-term blood sugar” summary, HbA1c rationale, limitations (“Insulin-resistance… not shown as scored subsystems”), glucose listed as missing with policy line |
| 3 | Liver flat evidence renders correctly | **PASS** | Expanded liver card: **Panel evidence** section (not subsystem rows); domain summary, mechanism, limitations (no MASLD/fibrosis over-claim); included markers ALT/GGT/ALP/Albumin/Bilirubin with rationales; AST not on panel |
| 4 | Hidden MED-REV-1 subsystems remain hidden | **PASS** | No Homocysteine pathway, Vascular strain, Insulin/metabolic, or liver enzyme/processing subsystem rows in DOM |
| 5 | No raw Pass 3/package/internal IDs/source traces | **PASS** | DOM search: no `signal_*`, `wave1_cv_*`, `pkg_`, `Pass_3`, `health_system_card_evidence`, `inv_` strings |
| 6 | No frontend clinical inference | **PASS** | Role labels from backend enums only (`USED IN THIS SCORE`, `SUPPORTS CONFIDENCE`, `CONTEXT MARKER`); no marker-ID parsing in components |
| 7 | Stale snapshot not mistaken for current output | **PASS** | Regenerated ID differs; stale API retains 3 legacy subsystems without enrichment fields |

### Compile manifest hashes (closure item 3)

| Manifest | Output artefact | SHA-256 |
|---|---|---|
| `kb_util1_lipid_transport_card_evidence.yaml` | `wave1_cv_lipid_transport.yaml` | `01e8be67…e8ed0` |
| `kb_util1_glycaemic_card_evidence.yaml` | `wave1_met_glycaemic_control.yaml` | `7a0a72cb…5df18` |
| `kb_util1_liver_flat_card_evidence.yaml` | `wave1_liver_flat_v1.yaml` | `b4b90bb0…9a5e2` |

Verified by regression test `test_kb_util1_launch_manifests_have_resolved_output_hashes` and `validate_compile_manifests`.

## Remaining risks / carry-forwards

- Full Pass 3 estate automated compiler deferred (CF-KBUTIL1-001)
- Hypothesis/contradiction surfacing deferred (CF-KBUTIL1-002)
