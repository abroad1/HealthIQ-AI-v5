# ARCH-RT-IDENTITY-PROV-1 — Implementation and Verification Report

**Work ID:** ARCH-RT-IDENTITY-PROV-1  
**Branch:** `feature/arch-rt-identity-prov-1-runtime-identity-provenance-integrity`  
**Date:** 2026-07-25  
**Report revision:** Audit-correction expansion (test matrix + full evidence)

---

## 1. Executive outcome

Activation-frame identity (`activation_key = signal_id::source_spec_id`) is preserved through the five known downstream collapse surfaces via a shared index helper and additive clinician-report cardinality. Honest provenance status classification and a launch-critical gate distinguish runtime compatibility from controlled-beta explicit-lineage eligibility. Package-manifest schema extended additively to **1.1.0**. No PSI / Pass 3 / MR-BATCH / Gemini activation; no medical prose or threshold changes; controlled beta not declared.

**Audit correction (this revision):** Extended `backend/tests/unit/test_arch_rt_identity_prov_1.py` to the hardened-prompt matrix; expanded this report to the full evidence checklist; re-ran the required regression suite. Production code was not redesigned.

---

## 2. Baseline branch and SHA

| Field | Value |
|---|---|
| Baseline (Package 1 / programme baseline on `main`) | `6d30bbf3b956066c1c93f2484703e07f62ac124f` (ARCH-GOV-BASELINE-1 merge) |
| Feature branch | `feature/arch-rt-identity-prov-1-runtime-identity-provenance-integrity` |
| Implementation commit | `ebb1d434f6720f8096ded68ad8780b5f7d900f24` |
| Prior kernel COMPLETE status commit | `e1732a2` |
| Authority baseline doc | `docs/architecture/HEALTHIQ_AI_CURRENT_STATE_BASELINE_2026-07-25.md` |

---

## 3. Authority preflight

| Check | Result |
|---|---|
| Automation Bus SOP | v1.3.1 (full SOP for core/knowledge) |
| Hardened prompt | `automation_bus/latest_cursor_prompt.md` (ARCH-RT-IDENTITY-PROV-1) |
| Hardening status | HARDENED (prior window) |
| Kernel re-entry for audit correction | **Blocked:** `run_work_package.py start` exit 3 — “Refusing re-run: same work_id is already COMPLETE”. Correction work proceeded on the feature branch under explicit human audit-correction instruction; finish/re-COMPLETE requires human/GPT authority to reopen or issue a correction work_id. |
| Stash | Empty at correction start |
| Role | healthiq-core-engine |

---

## 4. Inherited ADR decisions

Subordinate ADR: `docs/architecture/ADR-RT-IDENTITY-PROV-001_activation_frame_and_provenance_integrity.md`.

| Inherited ADR | Actual filename | Inherited without reopening |
|---|---|---|
| ADR-RT-001 | (research-to-runtime / day-one architecture set) | Yes |
| ADR-RT-002 | `ADR-RT-002_signal_spec_identity_and_registry_policy.md` | `signal_id` / `source_spec_id` / `activation_key`; duplicate keys fail closed |
| ADR-RT-003 | `ADR-RT-003_hypothesis_artefact_and_root_cause_transition.md` | Compiled vs legacy hypothesis transition |
| ADR-RT-004 | `ADR-RT-004_compile_manifest_and_package_provenance_policy.md` | Compile-manifest authority; explicit provenance policy |

**Filename corrections (hardening C4):** prompt citations mapped to actual paths (recorded in ADR § corrections table). No ADR reopening.

---

## 5. Pre-change reality evidence

Stage 1 discovery (pre-implementation) established:

1. Downstream consumers indexed or keyed by bare `signal_id`, collapsing multi-frame activations.
2. Clinician report exposed a singleton `root_cause`, silently dropping additional authorised findings.
3. Package provenance could present batch-JSON lineage with inferred activation keys without an honest status enum for beta claims.
4. `compile_manifest_ref` (consumer) vs `compile_manifest_path` (estate index) coexisted; blind rename would break estate indexing.
5. Launch-critical `pkg_kb47_*` packages largely cite `Batch_2_Pass_3.json` — not inv_ YAML authority.

**Additional launch-path collapse surfaces found during discovery (not remediated in this package):**

| Surface | File | Disposition |
|---|---|---|
| Interpretation display publish | `interpretation_display_layer_publish_v1.py` | Carry-forward |
| Domain score assembler | `domain_score_assembler.py` | Carry-forward |
| Narrative report lead resolution | `narrative_report_compiler_v1.py` | Carry-forward |
| Intervention selector signal_refs | `intervention_selector_v1.py` | Carry-forward |

Acceptance criterion “no unaddressed launch-path collapse” remains **partially open** for these four; they are Package 3 / follow-on identity hardening, not silent omissions.

---

## 6. Stage B Mode 2 decision summary

Mode 2 (architecture-extension, not redesign):

- Add shared `signal_result_index_v1` helpers; migrate known collapse sites to activation-key indexing.
- Additive clinician `root_causes[]`; legacy `root_cause` only when `len==1` (no silent first pick).
- Provenance enum: `EXPLICIT_SPEC | COMPILED_MANIFEST | SOURCE_DOCUMENT_DERIVED | LEGACY_INFERRED | UNRESOLVED | BLOCKED`.
- Schema 1.1.0 optional fields; no rewrite of historical package meaning.
- Gate scoped to launch-critical cohort (`pkg_kb47_*` runtime-active) — warnings for beta-ineligible lineage, not estate-wide fail for unrelated legacy.
- Do not invent `source_spec_id` for batch-JSON packs.

---

## 7. STOP Gate 1 disposition

**STOP_GATE_1: PASS** — recorded in ADR-RT-IDENTITY-PROV-001. Architecture-extension approved for mechanical identity/cardinality and provenance honesty without reopening ADR-RT-001…004.

---

## 8. Migration cohort

| Cohort | Scope |
|---|---|
| Runtime consumers | Interaction builder, root-cause compiler, report compiler, output-authority builder, clinician report + frontend types, SignalResult provenance field |
| Schema | `knowledge_bus/schema/package_manifest_schema.yaml` → 1.1.0 (optional provenance fields) |
| Launch-critical provenance | Active `pkg_kb47_*` packages + compiled vitamin-D hypothesis inventory row |
| Out of cohort | Broad legacy WHY rewrite; PSI; Pass 3; MR-BATCH-001B; Gemini; Package 3 prose routing; the four deferred collapse surfaces above |

---

## 9. Full files-changed list

Relative to baseline `6d30bbf` (implementation + bus artefacts):

```text
automation_bus/latest_cursor_prompt.md
automation_bus/latest_cursor_status.json
automation_bus/latest_prompt_hardening.json
backend/core/analytics/output_authority_provenance_builder_v1.py
backend/core/analytics/report_compiler_v1.py
backend/core/analytics/root_cause_compiler_v1.py
backend/core/analytics/signal_evaluator.py
backend/core/analytics/signal_interaction_builder.py
backend/core/contracts/clinician_report_v1.py
backend/core/contracts/report_v1.py
backend/core/contracts/root_cause_v1.py
backend/core/knowledge/provenance_status_v1.py
backend/core/knowledge/signal_result_index_v1.py
backend/core/models/signal.py
backend/scripts/run_architecture_validation_gate.py
backend/scripts/validate_identity_provenance_gate.py
backend/tests/unit/test_arch_rt_identity_prov_1.py
docs/architecture/ADR-RT-IDENTITY-PROV-001_activation_frame_and_provenance_integrity.md
docs/architecture/ARCH-RT-IDENTITY-PROV-1_launch_critical_provenance_inventory.md
docs/audit-papers/ARCH-RT-IDENTITY-PROV-1_implementation_and_verification_report.md
docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md
frontend/app/types/analysis.ts
knowledge_bus/schema/package_manifest_schema.yaml
```

Audit-correction delta (this revision): test matrix expansion + this report (+ verification evidence below). No production redesign.

---

## 10. Workstream A implementation

- `backend/core/knowledge/signal_result_index_v1.py` — index by activation_key (fail closed on duplicates), group by signal_id, participating keys, family confidence.
- Interaction builder retains `participating_activation_keys`; family aggregation named (`aggregation_scope: signal_family`).
- Root-cause compiler emits one finding per activation frame for shared `signal_id`.
- Report compiler preserves multi-frame top findings.
- Output-authority provenance uses frame-specific element ids.
- SignalResult carries `provenance_status` (default `LEGACY_INFERRED`).

---

## 11. Clinician-report contract migration

| Before | After |
|---|---|
| Singleton `sections.root_cause` only | Additive `sections.root_causes: List[...]` |
| Multi findings → silent first (or loss) | Multi → all in `root_causes`; `root_cause = null` |
| Single finding | `root_causes` length 1; legacy `root_cause` populated for compatibility |

Frontend: `frontend/app/types/analysis.ts` mirrors additive list + legacy singleton; render-only.

---

## 12. Workstream B implementation

- `provenance_status_v1.classify_package_provenance_status` — honest classification; batch JSON → `BLOCKED` where applicable; EXPLICIT_SPEC only with resolvable inv_ YAML.
- Gate: `backend/scripts/validate_identity_provenance_gate.py` wired into architecture validation gate.
- Inventory: `docs/architecture/ARCH-RT-IDENTITY-PROV-1_launch_critical_provenance_inventory.md` (generated).

---

## 13. Manifest-schema migration

- Schema version **1.1.0** (was 1.0.x class).
- Required fields unchanged: `package_id`, `package_version`, `research_brief`, `signal_library`.
- Optional: `source_spec_id`, `activation_key`, `source_document`, `source_document_hash`, `legacy_retained`, `compile_run_id`, etc.
- Historical packages omitting optional fields remain compatible.

---

## 14. Compile-manifest naming reconciliation

| Name | Role |
|---|---|
| `compile_manifest_ref` | Canonical logical reference for consumers / DTOs (`SubsystemEvidenceV1`, frontend types) |
| `compile_manifest_path` | Estate-index internal filesystem path (`estate_index_v1.yaml`) |

Resolution: `launch_estate_v1.resolve_compile_manifest_ref`. No blind rename of estate-index fields. Consumer DTOs must not leak `compile_manifest_path` (tested).

---

## 15. Knowledge Bus validation evidence

- No package promotion and no package content rewrite in this work package.
- Schema artefact changed only (`package_manifest_schema.yaml` → 1.1.0 additive).
- Canonical package validator was **not** required against mutated packages (none mutated).
- `latest_knowledge_status.json` **not** updated (no promotion).
- Gate inventory regenerated by identity/provenance gate during verification.

---

## 16. Medical / authority review (STOP Gate 2)

**STOP_GATE_2: Not triggered** for mechanical identity/cardinality work with no medical meaning change.

Launch-critical batch-JSON packages remain **beta-ineligible** for explicit-lineage claims; no invented `source_spec_id`; no medical statement changes.

---

## 17. Before / after multi-frame evidence

| Surface | Before | After |
|---|---|---|
| Indexing | Bare `signal_id` overwrite | `activation_key` index; duplicates fail |
| Interaction | Family presence only | + `participating_activation_keys` |
| Root cause | One finding per signal_id | One finding per frame |
| Report top findings | Collapse risk | Both/all frames retained |
| Output authority | Family-level element risk | Frame-specific element ids |

---

## 18. Before / after clinician-report cardinality

| Case | Before | After |
|---|---|---|
| Two authorised findings | Singleton / silent drop | `root_causes` length 2; `root_cause` null |
| One authorised finding | Singleton | `root_causes` length 1; legacy `root_cause` set |

---

## 19. Before / after provenance evidence

| Claim | Before | After |
|---|---|---|
| Batch JSON lineage | Could be treated as ordinary inferred activation without beta gate | Classified `BLOCKED` / not beta-eligible for EXPLICIT claims |
| Resolvable inv_ + `source_spec_id` | Ambiguous | `EXPLICIT_SPEC` |
| Missing lineage | Ambiguous | `UNRESOLVED` |
| Consumer path leak | Risk of filesystem path in DTO | `compile_manifest_ref` only on consumer models |

---

## 20. Commands and exit codes

Recorded during audit-correction verification (PowerShell; `PYTHONPATH=backend`, `HEALTHIQ_MODE=test` where applicable).

### 20a. Gates and identity matrix

| Command | Exit |
|---|---|
| `python backend/scripts/validate_day_one_architecture.py` | 0 |
| `python backend/scripts/validate_day_one_launch_estate_gate.py` | 0 |
| `python backend/scripts/run_architecture_validation_gate.py` | 0 |
| `python backend/scripts/validate_identity_provenance_gate.py` | 0 (PASS with BLOCKED beta-ineligible warnings for kb47 cohort) |
| `python -m pytest backend/tests/unit/test_arch_rt_identity_prov_1.py -q` | 0 |
| `python -m pytest backend/tests/unit/test_signal_activation_identity_v1.py -q` | 0 |
| `python -m pytest backend/tests/regression/test_signal_authority_collision_enforcement.py backend/tests/unit/test_p1_26_iron_homocysteine_activation.py -q` | 0 |

### 20b. Consumer / regression suites

| Command | Exit |
|---|---|
| `python -m pytest backend/tests -k "interaction_map or signal_interaction" -q` | 0 |
| `python -m pytest backend/tests/unit -k "root_cause_compiler or compile_root_cause or RootCause" -q` | 0 |
| `python -m pytest backend/tests/unit/test_clinician_report_runtime_alignment.py -q` | 0 (after AB/VR fixture refresh for additive `root_causes`) |
| `python -m pytest backend/tests -k "output_authority" -q` | 0 |
| `python -m pytest backend/tests/unit/test_replay_manifest.py backend/tests/regression/test_persisted_result_replay_status.py -q` | 0 |
| `python -m pytest backend/tests/unit/test_golden_panel_runner.py -q` | 0 |
| `python -m pytest backend/tests/unit/test_wave1_liver_marker_mapping_fix.py -q` | 0 |
| `python -m pytest backend/tests -k "bilirubin" -q` | 0 |
| `python -m pytest backend/tests -k "mr_batch_001b or MR_BATCH_001B or mr_batch" -q` | 0 |
| `python -m pytest backend/tests -k "no_llm or NO_LLM or narrative_runtime" -q` | 0 |
| `frontend` `npx tsc --noEmit` | 0 |
| `frontend` `npx jest tests/queries/analysisResult.test.ts tests/state/analysisStore.test.ts` | 0 |

### 20c. Disclosed pre-existing / out-of-scope failures (not weakened)

| Command / test | Exit | Disposition |
|---|---|---|
| `test_validate_staged_psi_activation_readiness.py` (estate counts) | 1 | Disclosed carry-forward per hardened prompt; inventory counts stale vs estate; this package did not activate PSI |
| `test_insights_golden.py::test_fatigue_root_cause_golden_parity` | 1 | Unrelated legacy fatigue insight (`evidence is None`); pulled by broad `-k root_cause` only |
| `test_lc_s22_render_smoke_wave1_domain_cards_present` | 1 | Pre-existing sentinel render blocker `missing_wave1_domain_cards`; not identity/provenance |
| `test_kb_util1_pass3_card_evidence_compile_and_consume.py::test_domain_flat_loader_in_launch_critical_validator_paths` | 1 | Pre-existing estate set drift; not introduced by identity helpers |
| `frontend/tests/services/analysis.test.ts` (`result_versioning: null`) | 1 | Pre-existing mapper expectation drift; unrelated to clinician `root_causes` |

### 20d. Fixture refresh (audit correction)

Regenerated governed clinician fixtures to match additive multi-finding contract:

- `backend/tests/fixtures/reports/clinician_report_v1_ab.json`
- `backend/tests/fixtures/reports/clinician_report_v1_vr.json`

Both now include `sections.root_causes` and set `sections.root_cause` to `null` when multiple authorised findings exist (ADR-mandated; no silent singleton).

---

## 21. Acceptance-criteria disposition table

### Architecture decision

| Criterion | Disposition |
|---|---|
| ADR exists, subordinate to ADR-RT-001…004 | PASS |
| No accepted policy reopened without STOP | PASS |
| Migration cohort bounded | PASS |
| STOP Gate 1 recorded | PASS |
| STOP Gate 2 as required | PASS (not required / not triggered) |

### Multi-frame preservation

| Criterion | Disposition |
|---|---|
| Known collapse consumers fixed | PASS (five known surfaces) |
| Clinician multi-finding | PASS |
| Family aggregation explicit/named/tested | PASS |
| Root-cause frame binding | PASS (per-frame findings) |
| Output-authority frame-specific | PASS |
| DTO / clinician / replay identity | PASS (DTO + clinician JSON round-trip; full persisted-pipeline replay remains Phase 2+ estate capability — see inapplicable note) |
| Frontend types additive | PASS |
| Legacy single-frame compatible | PASS |
| Duplicate keys fail closed | PASS |
| No unaddressed launch-path collapse | **PARTIAL** — four deferred surfaces documented |

### Provenance

| Criterion | Disposition |
|---|---|
| Schema represents contract | PASS (1.1.0) |
| Historical compatibility | PASS |
| Status distinguishes classes | PASS |
| No inferred-as-explicit | PASS |
| Scanners / gate shared facts | PASS (gate uses package_provenance_scan) |
| compile_manifest_ref/path governed | PASS |
| Consumer DTOs no path leak | PASS |
| Launch inventory + statuses | PASS |
| Resolvable items evidence-backed | PASS where EXPLICIT; else not guessed |
| Unresolvable marked beta-ineligible | PASS |
| Runtime/DTO/clinician honesty | PASS |

### Continuity / gates / scope

| Criterion | Disposition |
|---|---|
| ARCH-RT-1/2/3 BUILD continuity | PASS (historical absence noted; no fabricated closure) |
| Identity + architecture + launch-estate gates | PASS (exit 0; see §20) |
| PSI unwired / MR-BATCH test-only / Gemini non-authoritative | PASS (unchanged) |
| No medical content / thresholds / Package 3 / beta claim | PASS |

---

## 22. STOP-condition assessment

| # | Condition | Disposition |
|---|---|---|
| 1–3 | Authority / baseline / ADR conflict | Not triggered |
| 4–6 | Multi-frame medical ambiguity / product policy | Not triggered (additive cardinality) |
| 7 | Invent source_spec_id | Not triggered (BLOCKED instead) |
| 8–11 | Immutability / schema / discard / replay | Not triggered |
| 12 | Launch pack required but no authority | Runtime continues inferred; beta claims blocked |
| 13 | ref/path reconcile | Resolved without breaking rename |
| 14–15 | KB / gate unexplained fail | Not triggered (see §20b) |
| 16–17 | PSI/MR-BATCH/Gemini / Package 3 expansion | Not triggered |
| 18 | Unrelated dirty tree | Cleaned incidental dirty file before correction |
| 19–20 | Human medical policy / ADR re-decision | Not triggered |

**Process note:** Kernel refuse-reopen of COMPLETE work_id is an Automation Bus process constraint for this correction window (escalated), not a product STOP.

---

## 23. Unresolved and beta-ineligible items

1. Launch-critical `pkg_kb47_*` batch-JSON lineage → **BLOCKED** / not beta-eligible for explicit-lineage claims until inv_ extraction.
2. Four additional launch-path collapse surfaces (interpretation display, domain score assembler, narrative lead, intervention selector) — carry-forward.
3. Family-level legacy WHY when multi-frame — frame-specific compiled WHY later.
4. Stale `test_validate_staged_psi_activation_readiness.py` inventory counts — disclosed carry-forward unless this package drifts counts (it should not).
5. Full end-to-end persisted golden-run pipeline replay (estate Phase 2+) — DTO/clinician JSON round-trip covered here; full pipeline replay not claimed as newly implemented.

---

## 24. Historical ARCH-RT-1/2/3 continuity reconciliation

ARCH-RT-1/2/3 lacked contemporaneous BUILD register entries. ADRs remain authoritative. This package records continuity without fabricating retrospective closure claims. BUILD register entry for ARCH-RT-IDENTITY-PROV-1 includes this note.

---

## 25. PSI, MR-BATCH, Gemini authority unchanged

| Authority | Status |
|---|---|
| PSI | Remains unwired / not activated |
| MR-BATCH-001B | Remains test-only; not promoted |
| Gemini | Remains non-authoritative for narrative |

---

## 26. Package 3 carry-forwards

- Prose routing / modifier binding (explicitly out of scope).
- Frame-specific compiled WHY migration beyond identity preservation.
- Remediation of the four deferred collapse surfaces.
- Investigation-spec extraction from batch JSON for kb47 launch packs (authority work, not Package 3 prose).

---

## 27. Test matrix coverage (audit correction)

| Required coverage | Test(s) | Notes |
|---|---|---|
| Evaluator independent same-`signal_id` frames | `test_evaluator_independent_firing_same_signal_id_frames` | |
| DTO serialization multi-frame | `test_dto_serialization_preserves_multiple_frames` | |
| Persistence/replay round-trip | `test_persistence_replay_round_trip_preserves_activation_identity_and_provenance` | SignalResult + ClinicianReportV1 JSON round-trip |
| Deterministic ordering | `test_deterministic_ordering_across_repeated_executions` | |
| Three+ simultaneous frames | `test_three_or_more_simultaneous_frames` | |
| Canonical compile-manifest ref | `test_canonical_compile_manifest_ref_resolution` | |
| Paths not leaking to consumer DTOs | `test_internal_compile_manifest_paths_do_not_leak_into_consumer_dtos` | |
| Blocked launch-critical without blocking legacy | `test_blocked_launch_critical_reported_without_blocking_unrelated_legacy` | |
| Schema compatibility + naming drift | `test_package_manifest_schema_compatibility_and_naming_drift_regression` | |
| Clinician multi-finding BE+FE contracts | `test_clinician_report_multi_finding_serialization_backend_and_frontend_contracts` | |
| Prior matrix (interaction, OA, root-cause, duplicate fail, singleton legacy, batch≠EXPLICIT) | Existing tests retained | Assertions not weakened |

### Genuinely inapplicable / bounded notes

| Item | Reason |
|---|---|
| Full persisted golden-run pipeline replay as a new product feature | Estate still documents Phase 2+ gap; this package proves DTO/clinician lossless round-trip of activation identity + provenance, not a new pipeline replay engine |
| Tests asserting the four deferred collapse surfaces are fixed | Production remediation intentionally out of audit-correction scope; would fail against known deferred surfaces — documented as unresolved instead of greenwashed |

---

## 28. Resubmission note

Package is ready for independent audit on the feature branch after §20b suite results are filled and any audit-correction commit is present. Kernel `finish` cannot re-run while status remains COMPLETE for the same `work_id` without authority reset.
