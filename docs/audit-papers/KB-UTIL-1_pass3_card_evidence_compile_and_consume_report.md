# KB-UTIL-1 — Pass 3 Card Evidence Compile and Consume Report

**Work ID:** `KB-UTIL-1_pass3_card_evidence_compile_and_consume`  
**Branch:** `work/KB-UTIL-1-pass3-card-evidence-compile-and-consume`  
**Change type:** MIXED (Layer A compiled enrichment + Layer B DTO + Layer C render)

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
- `knowledge_bus/compiled/manifests/kb_util1_*.yaml` — compile manifests (pending hash refresh)

## Layer B changes

- `backend/core/knowledge/health_system_card_evidence.py` — pass through enrichment fields; `kb_util1_package_enrichment` compile status
- `backend/core/knowledge/domain_flat_card_evidence.py` — new flat loader/assembler
- `backend/core/models/results.py` — `SubsystemEvidenceV1` enrichment fields; `DomainFlatEvidenceV1`; `ConsumerDomainScoreV1.flat_domain_evidence`
- `backend/core/analytics/wave1_subsystem_evidence.py` — `assemble_wave1_flat_domain_evidence`
- `backend/core/analytics/domain_score_assembler.py` — liver attaches `flat_domain_evidence`
- `backend/scripts/validate_day_one_architecture.py` — `validate_kb_util1_wave1_card_enrichment`

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

All PASS.

## Manual validation

Not executed in this session. Use a **regenerated** result (not immutable `746f2b0a` snapshot) for browser UAT per sprint prompt. Assembly regression tests confirm enriched fields on fresh engine output.

## Remaining risks / carry-forwards

- Manual browser UAT on regenerated analysis pending human verification
- Compile manifest output hashes remain `pending_inventory_refresh`
- Full Pass 3 estate compiler deferred (CF-KBUTIL1-001)
- Hypothesis/contradiction surfacing deferred (CF-KBUTIL1-002)
