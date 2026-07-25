# HealthIQ AI — Executable Codebase and Runtime Reality Audit

| Field | Value |
|---|---|
| **Audit date** | 2026-07-25 |
| **Auditor identity** | Cursor — independent repository reality and runtime execution auditor |
| **Repository root** | `C:\Users\abroa\HealthIQ-AI-v5` |
| **Branch** | `main` |
| **HEAD SHA** | `2a8fa64ed791cabc8ae478113b96cefdf25145a1` |
| **Working tree** | DIRTY — only untracked prior audit papers under `docs/audit-papers/` (no production/code changes) |
| **Mode** | Read-only inspection + execution of existing validators/tests; only this report written |

Evidence labels:

- **VERIFIED_EXECUTION** — command/test/smoke load ran in this audit with recorded exit code
- **VERIFIED_STATIC_PATH** — production import/call chain read in source
- **REASONABLE_INFERENCE** — strongly supported by multiple static paths
- **UNVERIFIED_CLAIM** — document claim without executable confirmation
- **UNKNOWN_REQUIRES_REVIEW** — insufficient or conflicting evidence

Capability states used: `DOCS_ONLY`, `TEST_ONLY`, `BUILT_NOT_WIRED`, `RUNTIME_WIRED`, `ACTIVE_AUTHORITY`, `PRODUCTION_PATH`, `BLOCKED_OR_STALE`.

---

## 1. Executive verdict

HealthIQ AI has a **real production analysis path** that is architecture-gated and largely deterministic: signals evaluate by `activation_key`, Wave 1 domain cards load compiled evidence, clinician/narrative Layer B compilers run without Gemini by default, and MR-BATCH-001B is **not** on that path.

The decisive executable findings are:

1. **Architecture validation gate PASS** (`architecture_validation_gate: PASS`, exit 0) including day-one architecture, launch estate gate, medical frame index, and governance regression suites.
2. **PSI is correctly deferred** on launch-critical modules (tests + static import proof); 57 PSI artefacts on disk are **not** production authority.
3. **Multi-frame identity is only partially delivered**: registry load preserves distinct `activation_key`s and fail-closes on duplicates, but **downstream interaction map, root-cause, and several report consumers collapse on `signal_id`** — so end-to-end multi-frame preservation is **not** production-complete.
4. **Package provenance is weak as active authority**: scanned estate shows **0 packages with explicit `source_spec_id`**; classifications are dominated by `source_document_unparsed` and `blocked_pending_spec_extraction`.
5. **Root-cause active authority is dual**: only `signal_vitamin_d_low` uses compiled hypothesis artefacts at runtime; remaining registry targets use legacy YAML.
6. **Stale inventory tests**: ARCH-RT-5D provenance count assertions fail against current estate (191 vs expected 186; 10 cards vs 7) even while live day-one/launch gates pass — inventory docs/tests lag reality.

**Controlled beta remains unwarranted** on executable grounds: provenance honesty, multi-frame collapse, dual WHY authority, deferred PSI richness, partial retail prose coverage, and candidate-only MR prose depth.

No next sprint is selected in this report.

---

## 2. Audit baseline

| Item | Value | Label |
|---|---|---|
| Branch | `main` | VERIFIED_EXECUTION |
| HEAD | `2a8fa64ed791cabc8ae478113b96cefdf25145a1` — *Update MR-BATCH-001B benchmark carry-forward status* | VERIFIED_EXECUTION |
| Working tree | 2 untracked audit markdown files only | VERIFIED_EXECUTION |
| Latest 20 commits | See Appendix A | VERIFIED_EXECUTION |
| Active WP token | Absent (`automation_bus/state/` empty) | VERIFIED_EXECUTION |
| Cursor status | `P3-PROSE-DEPTH-1` COMPLETE; `bus_version: "1.2"`; older SHA — **stale vs HEAD** | VERIFIED_EXECUTION |
| KB status expected path | `knowledge_bus/current/latest_knowledge_status.json` **missing** | VERIFIED_EXECUTION |
| Fallback KB artefact | `backend/artifacts/knowledge_status.json` — `ready_for_implementation: true`; PSI validation SKIP | VERIFIED_EXECUTION |
| Env flags (this shell) | `HEALTHIQ_NARRATIVE_LLM` UNSET; `HEALTHIQ_ENABLE_LLM` UNSET; `GEMINI_API_KEY` UNSET | VERIFIED_EXECUTION |
| Narrative default (no test mode) | `synthesizer_allow_llm=False`, reason `HEALTHIQ_NARRATIVE_LLM_not_set_default_off` | VERIFIED_EXECUTION |
| Full audit without modifying repo | **Yes** (validators/tests/read-only smoke loads only) | VERIFIED_EXECUTION |

---

## 3. Commands executed and test results

| Command | Exit | Result | Notes |
|---|---:|---|---|
| `python backend/scripts/validate_day_one_architecture.py` | 0 | `day_one_architecture_validation: PASS` | VERIFIED_EXECUTION |
| `python backend/scripts/validate_day_one_launch_estate_gate.py` | 0 | `day_one_launch_estate_gate: PASS` | VERIFIED_EXECUTION |
| `python backend/scripts/run_architecture_validation_gate.py` | 0 | `architecture_validation_gate: PASS` | Includes frame index, modifier catalogue, day-one, launch estate, context reachability, medical intelligence, architecture/governance pytest |
| pytest multi-frame + PSI + MR-BATCH focused set | 0 | 15 passed | duplicate fail-closed, PSI isolation, MR isolation |
| pytest card evidence + compiled hyp + domain UX1C | 0 | 58 passed | production loaders exercised |
| pytest retail/pathway + output authority + launch estate governance (prior batch) | 0 | 33 passed | — |
| pytest `test_signal_evaluator.py` full file | 1 | 1 failed unrelated golden harness fixture | `test_kbs23_catalogue_panel_harness_runs_all_panel_fixtures` — fixture missing biomarkers/user; **not** used as multi-frame proof |
| pytest `test_arch_rt5d_package_provenance.py` | 1 | 4 failed | Stale expected counts (186/142/67/7) vs current 191 packages / 10 estate cards |
| pytest activation identity + duplicate/multi-frame cases | 0 | 5 passed | production registry path |
| Smoke: `scan_package_provenance()` / `load_estate_index()` / `get_card_evidence_artefact` ×10 / narrative policy | 0 | See §6–§8 | VERIFIED_EXECUTION |

**Distinction:** architecture gate PASS proves current day-one invariants; failed RT-5D inventory tests prove **stale expected counts**, not that live gates are broken.

---

## 4. Consolidated capability matrix

| Capability | Documented claim | Code exists | Production loader/consumer | Tests execute production path | Runtime wired | Active authority | Production path | Verdict | Evidence |
|---|---|---|---|---|---|---|---|---|---|
| `activation_key` construction | Day-one identity | Yes | `signal_activation_identity_v1` → `SignalRegistry._load` | Yes (unit) | Yes | Yes (registry key) | Yes | **RUNTIME_WIRED + ACTIVE_AUTHORITY + PRODUCTION_PATH** | E01–E03 |
| Duplicate `activation_key` fail-closed | Day-one | Yes | Registry raise | Yes | Yes | Yes | Yes | **RUNTIME_WIRED + PRODUCTION_PATH** | E04 |
| Multi-frame registry coexistence | Day-one | Yes | Registry by activation_key | Yes (unit) | Yes | Partial | Partial | **RUNTIME_WIRED** at load; **BLOCKED_OR_STALE** end-to-end | E05–E07 |
| Multi-frame independent fire | Claimed | Evaluator can emit both | Evaluator preserves keys | Unit only | Partial | No unified downstream | Partial | **RUNTIME_WIRED** emit; **BLOCKED_OR_STALE** consume | E05–E07 |
| Downstream multi-frame preservation | Implied | Consumers exist | Collapse on `signal_id` | Divergence notes | No | No | No | **BLOCKED_OR_STALE** | E06–E08 |
| Interaction map | Runtime map | Yes | `signal_interaction_builder` | Unit | Yes | Map YAML | Yes | **RUNTIME_WIRED + ACTIVE_AUTHORITY + PRODUCTION_PATH** for map; **signal_id collapse** | E06 |
| Phenotype map | IDL/phenotype | Yes | IDL publish path | Regression | Yes | Phenotype YAML | Yes | **RUNTIME_WIRED + PRODUCTION_PATH** | prior static + gate |
| Package provenance classification | ADR-RT-004 / RT-5D | Yes | Scripts/estate scanners — **not** orchestrator | Stale inventory tests FAIL | Gate uses scanners | Classification not explicit-spec | N/A in `run()` | **BUILT_NOT_WIRED** in analysis path; **ACTIVE_AUTHORITY** for gates; inventory **BLOCKED_OR_STALE** | E09–E11 |
| Explicit `source_spec_id` estate | Desired day-one | Fields exist | Inference at load | — | Inference used | Explicit count **0** | Inference on path | **RUNTIME_WIRED** inferred path; explicit authority **BLOCKED_OR_STALE** | E09 |
| Compile manifests + estate index | Day-one | Yes | Card/hypothesis refs; validators | Gate PASS; path resolve 0 missing | Yes (artefact load) | Estate index | Yes for cards/hyp | **RUNTIME_WIRED + ACTIVE_AUTHORITY + PRODUCTION_PATH** (compiled artefacts) | E12 |
| `compile_run_id == compile_id` | Schema | Validator enforces | Scripts | Unit exists | Governance | Manifests | Gate path | **ACTIVE_AUTHORITY** in validators | E13 |
| PSI artefacts | Pass3 / ADR-008 | 57 files; 57 opt-in | Loader exists | Unit loader + isolation | **No** launch import | **No** | **No** | **BUILT_NOT_WIRED + BLOCKED_OR_STALE** (deferred) | E14–E15 |
| Compiled card evidence | Day-one / Wave1 | 10 estate cards | `get_card_evidence_artefact` → assembler → DTO → FE | Yes | Yes | Yes | Yes | **RUNTIME_WIRED + ACTIVE_AUTHORITY + PRODUCTION_PATH** | E16–E17 |
| Hard-coded card evidence | Retired | None in estate | Assembler “no hard-coded fallback” | Sentinel tests | No hard-coded | Compiled only | Yes | **SUPERSEDED / none active** | E12, E17 |
| Compiled hypothesis WHY | Pilot | 1 artefact | `compile_root_cause_v1` compiled branch | Yes | Yes for vit D | Yes for vit D only | Yes | **RUNTIME_WIRED + ACTIVE_AUTHORITY + PRODUCTION_PATH** (vit D) | E18 |
| Legacy root-cause YAML | WHY | ~40 YAML; 41 targets | Legacy branch of compiler | Many unit | Yes | Yes for non–vit D | Yes | **RUNTIME_WIRED + ACTIVE_AUTHORITY + PRODUCTION_PATH** | E18–E19 |
| Retail explainers | Layer B | Registry 40 | `attach_retail_explainers_v1` in orchestrator | Yes | Yes | SSOT registry | Yes (fail-open) | **RUNTIME_WIRED + ACTIVE_AUTHORITY + PRODUCTION_PATH** | E20 |
| Pathway/functional packs | Layer B | YAML packs | Narrative compiler | Yes | Yes | Pack YAML | Yes | **RUNTIME_WIRED + ACTIVE_AUTHORITY + PRODUCTION_PATH** | E21 |
| Modifier binding / frame routing | P3 deferred | Templates/docs | No production binder | — | No | No | No | **DOCS_ONLY / BUILT_NOT_WIRED** | E22 |
| MR-BATCH-001B | Benchmark | Candidate YAML | Test loader only | Yes (isolation) | No | No | No | **TEST_ONLY + BLOCKED_OR_STALE** (not for prod) | E23 |
| Narrative Gemini | Layer C | Client exists | Synthesis path gated | Golden NO-LLM | Default off | Mock | Not default | **BUILT_NOT_WIRED** default; **BLOCKED_OR_STALE** until CEO/opt-in | E24 |
| Upload LLM parse | Upload | `LLMParser` + Gemini | `upload.py` | Unit (mocked) | Conditional | Parse only | Upload path when used | **RUNTIME_WIRED** when selected; **not analytical authority** | E25 |
| Frontend render-only | Policy | Results libs | DTO consumers | — | Presentation | Backend DTOs | Yes | **PRODUCTION_PATH** presentation; ranking helpers **not** medical inference engines | E26 |
| Automation Bus kernel | SOP | Scripts + gitignored state | Ops | — | Ops | Status stale | N/A | **RUNTIME_WIRED** ops tooling; status **BLOCKED_OR_STALE** | baseline |

---

## 5. Signal identity and multi-frame activation

### Construction (VERIFIED_STATIC_PATH + VERIFIED_EXECUTION)

```
AnalysisOrchestrator → evaluate_signal_evaluation_phase
  → SignalEvaluator.evaluate_all
  → SignalRegistry._load
     → resolve_activation_identity / build_activation_key
        → activation_key = "{signal_id}::{source_spec_id}"
```

- Files: `backend/core/knowledge/signal_activation_identity_v1.py`, `backend/core/analytics/signal_evaluator.py`
- Registry stores by **activation_key**, not signal_id (`_signals_by_activation_key`)
- Duplicate exact key raises `ValueError("Duplicate activation_key collision: ...")`

**Tests executed:** `test_signal_registry_duplicate_activation_key_fails_closed`, multi-frame registry cases — **PASS** (exit 0).

### What is proven

- Distinct frames can **load** if keys differ.
- Duplicate keys **fail closed** at registry load.

### What is not proven / contradicts full multi-frame product behaviour

| Consumer | Behaviour | Classification |
|---|---|---|
| `signal_interaction_builder.py` ~147–153 | `fired = {signal_id: state}` dict overwrite | **BLOCKED_OR_STALE** for multi-frame |
| `root_cause_compiler_v1.py` ~522 | `next(... signal_id == target)` first-match | **BLOCKED_OR_STALE** |
| `report_compiler_v1.py` system map ~749 | keyed by signal_id | Collapse risk |
| `root_cause_divergence_v1.py` notes | Explicitly: matches signal_id family only | VERIFIED_STATIC_PATH |

**Verdict:** Registry = `RUNTIME_WIRED + ACTIVE_AUTHORITY + PRODUCTION_PATH`. End-to-end multi-frame = `RUNTIME_WIRED` (emit) + `BLOCKED_OR_STALE` (consume). Confidence **HIGH**.

No `by_activation_key` consumer found under `backend/core` outside evaluator/collision sort keys.

---

## 6. Package provenance and compile manifests

### Executable estate scan (VERIFIED_EXECUTION)

| Metric | Value |
|---|---:|
| Package directories | 192 |
| Provenance scan rows | 191 |
| `has_source_spec_id` | **0** |
| `has_source_document` | 189 |
| `source_document_unparsed` | 82 |
| `blocked_pending_spec_extraction` | 76 |
| `source_document_derived` | 31 |
| `provenance_gap` | 2 |

### Compile / estate

| Metric | Value |
|---|---:|
| Estate card artefacts | 10 |
| Estate compiled hypotheses | 1 |
| Missing estate paths | **0** |
| Compiled card YAML files on disk | 11 |
| Compile manifest YAML files | 17 |
| Legacy hard-coded subsystem IDs | `[]` |

### Runtime use

- **Analysis path** uses activation identity inference at signal load; does **not** call `scan_package_provenance` inside `orchestrator.run()`.
- **Compiled card/hypothesis** loaders use `compile_manifest_ref` / estate membership as authority for those artefacts.
- Traceability chain for cards: research → (manifest on disk) → compiled YAML → `get_card_evidence_artefact` → Wave1 assembler → DTO — **executable for cards**.
- Traceability for packages generally: **inferred/unparsed/blocked**, not explicit `source_spec_id`.

### Validator enforcement

- `compile_run_id` must equal `compile_id` when present — enforced in `validate_day_one_architecture.py` / `validate_compile_manifest.py` (VERIFIED_STATIC_PATH; covered by architecture gate PASS).

### Stale inventory tests

`test_arch_rt5d_package_provenance.py` failed asserting 186 packages / 7 cards — estate now larger. **BLOCKED_OR_STALE** test expectations vs current reality. Live launch estate gate still PASS.

**Verdict:** Compile-manifest-backed **cards/hypotheses** = `RUNTIME_WIRED + ACTIVE_AUTHORITY + PRODUCTION_PATH`. Estate-wide explicit provenance = `BLOCKED_OR_STALE`. Confidence **HIGH**.

---

## 7. PSI

| Check | Result | Label |
|---|---|---|
| PSI files under packages | 57 | VERIFIED_EXECUTION |
| Manifest opt-in | 57 | VERIFIED_EXECUTION |
| Loader | `load_promoted_signal_intelligence_for_package` | VERIFIED_STATIC_PATH |
| Production imports of loader | **None** in launch-critical modules | VERIFIED_STATIC_PATH + VERIFIED_EXECUTION (`test_arch_rt5e_psi_runtime_wiring_decision` PASS) |
| Day-one validator | Forbids launch imports of PSI loader markers | Gate PASS |
| Launch-critical dependency | **None** | VERIFIED_EXECUTION |

**Verdict:** `BUILT_NOT_WIRED + BLOCKED_OR_STALE` (intentionally deferred / non-launch-blocking). Existence of PSI YAML is **not** runtime consumption. Confidence **HIGH**.

---

## 8. Health Systems Card evidence

### Executable proof

- Estate index lists **10** subsystems; all `get_card_evidence_artefact(sid)` smoke loads succeeded (`card_load_ok 10`).
- Production chain (VERIFIED_STATIC_PATH):

```
orchestrator.assemble_consumer_domain_scores_v1
  → assemble_wave1_subsystem_evidence
    → assemble_subsystem_from_compiled_card_evidence
      → get_card_evidence_artefact / load_card_evidence_artefact (fail-closed)
  → ConsumerDomainScore.subsystems → AnalysisDTO
  → FE Wave1DomainCards / subsystem evidence sections
```

- `wave1_subsystem_evidence.py` documents compiled-only assembly; estate `wave1_subsystems_legacy_hard_coded.subsystem_ids: []`.
- Domain set: cardiovascular, blood_sugar, liver, kidney, blood_iron_oxygen, thyroid — **six** Wave1 domains.

### Tests executed

`test_health_system_card_evidence_arch_rt5b.py`, `test_domain_ux1c_governed_subsystem_evidence.py` — **PASS**.

### Frontend

- `cardEvidenceConsumerCopy.ts` maps backend enums only; does not infer roles from marker ids.
- Presentation qualification in `wave1HealthSystemCardDisplay.ts` uses DTO score/confidence fields.

**Verdict:** `RUNTIME_WIRED + ACTIVE_AUTHORITY + PRODUCTION_PATH`. Hard-coded card authority **not active**. Confidence **HIGH**.

Bilirubin/total_bilirubin protection: covered by existing unit tests in estate (`test_wave1_liver_marker_mapping_fix.py` present); not re-executed in this pass — **REASONABLE_INFERENCE** from prior suite presence + day-one gate PASS.

---

## 9. Root-cause / WHY authority

### Selection order (VERIFIED_STATIC_PATH)

`compile_root_cause_v1`:

1. Iterate `ROOT_CAUSE_TARGET_SPECS` (41 targets).
2. Pick **first** signal_result row matching `signal_id` (not activation_key).
3. If `is_runtime_promoted_compiled_signal(signal_id)` → compiled artefact path.
4. Else → legacy YAML hypotheses loader.

### Active compiled authority (VERIFIED_EXECUTION)

| Signal | Authority |
|---|---|
| `signal_vitamin_d_low` | **Compiled** (`RUNTIME_PROMOTED_COMPILED_SIGNAL_IDS`) |
| All other registry targets (~40) | **Legacy YAML** under `knowledge_bus/root_cause/hypotheses/` |

Compiled artefact fields include `summary_template`, `activation_key`, `compile_manifest_ref` — tests assert summary_template used rather than raw `physiological_claim` for retail-facing summary (`test_compiled_hypothesis_arch_rt5c.py` PASS in this audit).

Multi-frame compiled promotion: blocked by tests (`test_multi_frame_promotion_blocked` in RT5C suite PASS).

**Note:** `root_cause_divergence_v1.py` still contains notes saying compiled is “shadow/pilot only” and “legacy remains authority for all 41” — those notes are **STALE relative to the compiler’s vitamin-D compiled branch**. Compiler code is the active authority.

**Verdict:** Dual authority — vitamin D `RUNTIME_WIRED + ACTIVE_AUTHORITY + PRODUCTION_PATH` (compiled); remainder same states on **legacy**. Multi-frame WHY = `BLOCKED_OR_STALE`. Confidence **HIGH**.

---

## 10. Prose and Layer B reasoning

| Asset | Location | Production consumer | Verdict |
|---|---|---|---|
| Retail explainers | `backend/ssot/retail_explainer_v1/registry.yaml` (40) | `orchestrator` → `attach_retail_explainers_v1` (fail-open) | **RUNTIME_WIRED + ACTIVE_AUTHORITY + PRODUCTION_PATH** |
| Pathway explainers | `knowledge_bus/pathway_explainers_v1/` | `narrative_report_compiler_v1` | **RUNTIME_WIRED + ACTIVE_AUTHORITY + PRODUCTION_PATH** |
| Functional / entity packs | knowledge_bus packs | Narrative compiler | **RUNTIME_WIRED** |
| Clinician report | `compile_clinician_report_v1` | DTO builders / FE | **RUNTIME_WIRED + PRODUCTION_PATH** |
| IDL | `publish_interpretation_display_layer_v1` | Orchestrator + FE | **RUNTIME_WIRED + ACTIVE_AUTHORITY + PRODUCTION_PATH** |
| P3 modifier templates / schema | sprint docs | None | **DOCS_ONLY** |
| Frame routing | Deferred | None | **DOCS_ONLY / BLOCKED_OR_STALE** |
| MR-BATCH-001B | sprint YAML | Test support only | **TEST_ONLY** |

Deterministic Layer B without Gemini: **Yes** under default env (narrative deny-default; compilers do not require LLM). VERIFIED_EXECUTION of policy + VERIFIED_STATIC_PATH of compilers.

No coherent single `prose_library/` runtime package exists; production authority is the set of SSOT/KB packs above.

---

## 11. Gemini and Layer C

### Narrative / insights path

| Item | Finding |
|---|---|
| Policy | `resolve_narrative_llm_allow_llm` — API default requires `HEALTHIQ_NARRATIVE_LLM` **and** `HEALTHIQ_ENABLE_LLM` |
| This audit default | `synthesizer_allow_llm=False` (`HEALTHIQ_NARRATIVE_LLM_not_set_default_off`) |
| Client construction | `MockLLMClient` unless double opt-in / explicit allow |
| Analytical authority? | **No** under defaults — synthesizer cannot become scoring/signal/root-cause authority; it generates optional `insights[]` after Layer B graph exists |
| CI/golden NO-LLM | Golden tests assert GeminiClient not instantiated in default mode (present in suite) |

### Upload parsing path

| Item | Finding |
|---|---|
| Entry | `backend/app/routes/upload.py` imports `LLMParser` |
| Client | `services/parsing/llm_parser.py` constructs `GeminiClient` |
| Role | Lab PDF/text extraction — **not** medical truth for scores/signals/WHY |
| Analytical authority? | **No** for analysis engine; may affect upstream extracted values if used |

**Architectural conclusion:** No LLM is an analytical authority for scoring, signal firing, root-cause generation, or medical truth on the default production analysis path. Confidence **HIGH**.

---

## 12. Frontend render-only verification

### Presentation / DTO display (expected)

- Wave1 domain/subsystem components render backend scores and compiled evidence labels.
- `cardEvidenceConsumerCopy.ts`: enum→copy only.
- Sanitize helpers rewrite noisy/engineering phrases.

### Borderline presentation logic (not medical engines)

`resultsPageLayout.ts`:

- `pickPrimaryDriverCluster` / `pickHeroAlignedPrimaryDriver` reorder clusters using **backend-supplied** severity and score fields plus IDL text alignment.
- Biomarker list ranking uses status fields from DTOs.
- Does **not** compute lab thresholds or change biomarker clinical state from raw values on the results page.

### Upload-stage numeric logic

`uploadReferenceRange.ts` performs band/comparator inference for upload review fidelity — aligned to parser/normalize concerns, **not** results-page diagnosis.

**Verdict:** Results UX is **PRODUCTION_PATH** render/presentation with limited **presentation selection**. No frontend medical scoring/diagnosis/root-cause invention found. Confidence **HIGH** for results path; upload band matching is a separate boundary (**MEDIUM** that all upload paths stay non-authoritative for analysis).

---

## 13. Maturity by beta-readiness block

| Block | Documented claim (strategy era) | Implementation | Tests | Production wiring | Active authority | Executable proof | Remaining gap | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 Core systems | Medium; 3 domains missing | 6 Wave1 domains + assemblers | Domain card tests PASS | Yes | Compiled cards + scoring rails | Card load smoke + gate PASS | Depth uneven; strategy stale | **RUNTIME_WIRED + PRODUCTION_PATH**; strategy claim **BLOCKED_OR_STALE** |
| 2 Subsystems | Uneven depth | 10 compiled cards | UX1C PASS | Yes | Compiled evidence | Estate + loads | PSI richness unused; visibility policy soft | **RUNTIME_WIRED + ACTIVE_AUTHORITY** |
| 3 Layer B / prose / clinician | Medium | Compilers + packs + retail 40 | Multiple PASS | Yes | Packs/SSOT/legacy+compiled WHY | Policy + assembler paths | Coverage/modifiers/frame routing | **RUNTIME_WIRED** core; depth **PARTIAL** |
| 4 Layer C / Gemini | Low | Clients + NarrativePayload | NO-LLM guards | Narrative off | Mock default | Policy execution | CEO gate | Narrative **BLOCKED_OR_STALE** inactive |
| 5 UX / results | Medium | FE consumers | Some replay smoke | Yes | Backend DTOs | Static FE review | Trust/IA polish | **PRODUCTION_PATH** presentation |
| 6 Safety / provenance | Med–High | Gates + collision + validators | Gate PASS; RT5D inventory FAIL | Gates yes; explicit specs no | Mixed/inferred | Provenance scan | Explicit specs = 0 | **PARTIAL**; explicit provenance **BLOCKED_OR_STALE** |
| 7 Auditability / replay | Medium | Replay contracts | Some regression | Partial | Version/replay fields | Gate/regression presence | Broader beta estate | **PARTIAL RUNTIME_WIRED** |
| 8 Phenotype / beta validation | Low–Med | Maps + fixtures | Partial | Partial | Phenotype/IDL | Gate frame index PASS | Thin beta panels | **PARTIAL**; insufficient for controlled beta |

---

## 14. MR-BATCH-001B verification

| Required classification | Executable status |
|---|---|
| Round 1 benchmark / test fixture | **Confirmed** — assets in sprint docs; test loader under `backend/tests/support/` |
| Not medically approved | **Confirmed** — 69/69 `review_status: CANDIDATE` (prior parse; isolation tests PASS) |
| Not for promotion | **Confirmed** — no KB promotion import/manifest for 001B |
| Not for production runtime | **Confirmed** — zero matches in `orchestrator` / `retail_explainer_assembly_v1`; isolation test PASS |
| Round 2 design benchmark only | **Consistent** with BUILD register HEAD; completion docs still mention medical review (**doc conflict**, not runtime) |

**Critical blocker check:** No contradictory **runtime** path found. Confidence **HIGH**.

---

## 15. Documented-but-undelivered capabilities

| Claim | Reality |
|---|---|
| Coherent named “prose library” runtime | No such package; split SSOT/KB packs |
| Frame-routed prose selection | Deferred — **DOCS_ONLY** |
| Modifier binding active | Deferred — **DOCS_ONLY** |
| Estate-wide explicit `source_spec_id` | **0** explicit — undelivered |
| End-to-end multi-frame WHY / interaction | Downstream collapse — undelivered |
| PSI as launch intelligence | Deferred — documented as deferred; not delivered as wired |
| Pass 3 protocol “approved” | Still DRAFT companion (governance; not re-litigated here) |

---

## 16. Built-but-unwired capabilities

| Artefact | Built | Wired? |
|---|---|---|
| PSI YAML + loader (57) | Yes | **No** launch path |
| Pass3 `generated_pilot` compilers | Yes | Stage/validate; not auto-activate |
| Package provenance scanners | Yes | Gates/scripts; not analysis selection authority for explicit specs |
| P3 schema/templates | Yes (docs) | Not imported by compilers |
| Context modifier catalogue draft | Validated by gate | Active runtime binding incomplete / draft |

---

## 17. Test-only or candidate-only capabilities

| Item | Classification |
|---|---|
| MR-BATCH-001B pack + composer | **TEST_ONLY** (+ candidate) |
| PSI unit loader tests | **TEST_ONLY** consumption |
| Divergence “shadow” notes for vit D | **BLOCKED_OR_STALE** commentary vs live compiled branch |
| RT-5D inventory assertions | **BLOCKED_OR_STALE** expected counts |

---

## 18. Active production authorities

| Domain | Active authority | Path |
|---|---|---|
| Signal evaluation registry | Package signal libraries keyed by `activation_key` | `SignalRegistry` |
| Signal collision suppression | Governed collision model | `signal_authority_collision_resolver` |
| Wave1 subsystem evidence | Compiled card YAML via estate/registered IDs | `health_system_card_evidence` |
| WHY for vitamin D | Compiled hypothesis artefact | `compile_root_cause_v1` compiled branch |
| WHY for other targets | Legacy root-cause YAML via registry | Legacy branch |
| Retail biomarker copy | SSOT retail registry | `attach_retail_explainers_v1` |
| Narrative sections | Pathway/functional/entity packs + compilers | `narrative_report_compiler_v1` |
| IDL presentation | IDL publisher + records | `publish_interpretation_display_layer_v1` |
| Narrative LLM | Mock / deny-default | `narrative_runtime_policy` |
| Day-one invariants | Validators + CI architecture gate | scripts + `.github/workflows/architecture-gate.yml` |

---

## 19. Documentation-versus-runtime mismatches

| Topic | Docs/tests claim | Runtime reality |
|---|---|---|
| Missing 3 launch-core domains | Strategy 2026-06-20 | Six domains wired |
| RT-5D package/card counts | Tests expect 186 / 7 | 191 rows / 10 estate cards |
| Compiled vit D “shadow only” | Divergence notes | Compiler uses compiled path |
| Cursor status = latest work | P3 COMPLETE | HEAD includes MR-BATCH merges |
| KB latest_knowledge_status | Expected path | Missing; fallback artefact only |
| Explicit provenance maturity | Often implied strong | **0** explicit `source_spec_id` |
| Multi-frame complete | Identity ADRs | Downstream signal_id collapse |

---

## 20. Active blockers before controlled beta

1. **Downstream multi-frame collapse** (interaction / root-cause / report) despite registry support  
2. **Zero explicit `source_spec_id`** across scanned packages — provenance honesty risk  
3. **Dual WHY authority** (1 compiled + ~40 legacy) without full migration  
4. **PSI deferred** — cannot claim Pass3 richness on cards/UX  
5. **Retail/prose depth incomplete** (40 explainers; modifiers/frame routing absent)  
6. **Stale provenance inventory tests** undermine trust in older closure counts  
7. **Secrets/history hygiene** not re-proven in this executable pass (out of analytical path; still beta-class ops risk — UNKNOWN_REQUIRES_REVIEW)  
8. **Narrative Gemini must stay non-authoritative** until CEO-gated design — constraint, not feature gap  

---

## 21. Candidate follow-up work packages

Candidates only — **none selected**.

### CWP-E1 — Multi-frame downstream preservation

- **Problem:** Consumers key on `signal_id`; first-match WHY; interaction overwrite  
- **Affected path:** `signal_interaction_builder`, `root_cause_compiler_v1`, report maps  
- **Why it matters:** Distinct frames can be silently dropped after correct evaluation  
- **Dependencies:** Product policy for multi-frame display  
- **Risk:** HIGH clinical presentation  
- **Medical review:** Likely for policy  
- **Unresolved decisions:** Whether same `signal_id` multi-frame is launch-supported  

### CWP-E2 — Explicit provenance backfill / honesty gate

- **Problem:** 0 explicit `source_spec_id`; many unparsed/blocked  
- **Affected path:** Package manifests + activation identity inference  
- **Why it matters:** Inferred provenance can be mistaken for explicit  
- **Dependencies:** Spec extraction for batch JSON cohort  
- **Risk:** HIGH governance/traceability  
- **Medical review:** No for field backfill; yes for activation decisions  
- **Unresolved:** Which packages must be explicit before beta  

### CWP-E3 — Refresh RT-5D / provenance inventory expectations

- **Problem:** Tests assert obsolete counts while gates pass  
- **Affected path:** CI clarity / audit trust  
- **Why it matters:** False failures hide real regressions  
- **Dependencies:** None technical beyond count refresh policy  
- **Risk:** LOW–MEDIUM process  
- **Medical review:** No  

### CWP-E4 — Root-cause compiled expansion or formal dual-path register

- **Problem:** Only vitamin D compiled  
- **Affected path:** `compile_root_cause_v1`  
- **Why it matters:** Traceability inconsistency  
- **Dependencies:** Multi-frame WHY policy  
- **Risk:** HIGH intelligence  
- **Medical review:** Yes  

### CWP-E5 — Round 2 prose pipeline (exclude MR-BATCH-001B promotion)

- **Problem:** Depth gaps; 001B not promotable  
- **Affected path:** Future registries — not current production  
- **Why it matters:** Consumer explanation quality  
- **Dependencies:** Authority lock on benchmark-only 001B  
- **Risk:** MEDIUM content  
- **Medical review:** Yes for Round 2 outputs  

### CWP-E6 — Frame routing + modifier binding design/implement

- **Problem:** Docs-only; deferred  
- **Affected path:** Narrative selection  
- **Why it matters:** Wrong-frame prose risk once candidates exist  
- **Dependencies:** CWP-E1 policy; content pipeline  
- **Risk:** HIGH presentation  
- **Medical review:** Yes for binding rules  

### CWP-E7 — PSI activation decision (keep deferred vs staged wire)

- **Problem:** 57 artefacts unwired by design  
- **Affected path:** Would touch launch modules if wired  
- **Why it matters:** Stranded research vs safety  
- **Dependencies:** Explicit architecture decision  
- **Risk:** CRITICAL if wired casually  
- **Medical review:** Yes before activation  

---

## 22. Recommended immediate governance action

**Do not start an implementation sprint from this paper alone.**

Immediate governance actions:

1. Accept this executable audit as evidence that **architecture gates pass** while **multi-frame end-to-end**, **explicit provenance**, and **PSI** remain incomplete or deferred.  
2. Adjudicate whether multi-frame same-`signal_id` is a launch requirement; if yes, schedule CWP-E1 before any “multi-frame complete” claim.  
3. Commission a **provenance inventory refresh** so RT-5D-style expected counts match the live 191/10 estate (CWP-E3), separate from medical content work.  
4. Keep MR-BATCH-001B locked as **TEST_ONLY / benchmark**; do not open medical review for promotion of that pack.  
5. Treat stale Automation Bus cursor status and missing `latest_knowledge_status.json` as control-plane hygiene, not as proof of product readiness.

---

## 23. Evidence index

| ID | Path / command / symbol | Proves | Does not prove | Confidence |
|---|---|---|---|---|
| E01 | `signal_activation_identity_v1.build_activation_key` | Key format | Downstream preservation | HIGH |
| E02 | `SignalRegistry._load` | Registry keyed by activation_key | End-to-end multi-frame UX | HIGH |
| E03 | Architecture gate PASS | Day-one invariants currently hold | Beta readiness | HIGH |
| E04 | `test_signal_registry_duplicate_activation_key_fails_closed` PASS | Fail-closed duplicates | Multi-frame product completeness | HIGH |
| E05 | Multi-frame unit tests PASS | Registry can hold distinct frames | Independent downstream consume | HIGH |
| E06 | `signal_interaction_builder` fired dict by signal_id | Collapse risk | Always wrong clinically | HIGH |
| E07 | `root_cause_compiler_v1` first-match by signal_id | WHY frame drop risk | Frequency in production panels | HIGH |
| E08 | `root_cause_divergence_v1` notes | Acknowledged family-only matching | Notes currency on vit D | MEDIUM |
| E09 | `scan_package_provenance` counts | 0 explicit source_spec_id; class breakdown | That inference is always wrong | HIGH |
| E10 | RT-5D pytest FAIL on counts | Inventory tests stale | Launch gate broken | HIGH |
| E11 | Launch estate gate PASS | Current estate gate green | Explicit provenance complete | HIGH |
| E12 | Estate resolve 0 missing; legacy_hc [] | Card/hyp refs resolve; no hard-coded list | Pass3 richness on cards | HIGH |
| E13 | validate compile_run_id==compile_id | Governance enforcement | All historical manifests perfect | HIGH |
| E14 | 57 PSI files / 57 opt-in | Artefacts exist | Runtime use | HIGH |
| E15 | RT-5E PSI isolation tests PASS | Launch modules do not import loader | Future wiring safe | HIGH |
| E16 | `get_card_evidence_artefact` ×10 smoke | Cards load | All panels beautiful | HIGH |
| E17 | UX1C / RT5B tests PASS | Production assembly path | Medical visibility ideal | HIGH |
| E18 | `RUNTIME_PROMOTED_COMPILED_SIGNAL_IDS` + compiler branch | Vit D compiled authority | Estate-wide compiled WHY | HIGH |
| E19 | 41 ROOT_CAUSE_TARGET_SPECS / 40 YAML | Legacy still dominant | Legacy medically perfect | HIGH |
| E20 | orchestrator `attach_retail_explainers_v1` + 40 registry | Retail on production path | Full biomarker coverage | HIGH |
| E21 | `compile_narrative_report_v1` pathway load | Pathway packs wired | Frame routing | HIGH |
| E22 | P3 carry-forward / no binder module | Modifiers/frame routing undelivered | Never needed | HIGH |
| E23 | MR isolation pytest PASS + no core imports | Not production | Content quality | HIGH |
| E24 | `resolve_narrative_llm_allow_llm(None)` | Default narrative LLM off | Upload path off | HIGH |
| E25 | `upload.py` → `LLMParser` | Upload can use Gemini | Analytical authority | HIGH |
| E26 | `resultsPageLayout.ts` ranking helpers | Presentation selection from DTO fields | Zero FE logic | HIGH |

---

## Appendix A — Full command log

```text
# Baseline
git rev-parse --abbrev-ref HEAD          → main
git rev-parse HEAD                       → 2a8fa64ed791cabc8ae478113b96cefdf25145a1
git status --porcelain                   → 2 untracked audit papers only
git log --oneline -20                    → (see section 2 / prior audit lineage from 2a8fa64 … 018dc0f)

# Validators
PYTHONPATH=backend python backend/scripts/validate_day_one_architecture.py
  → EXIT 0 ; day_one_architecture_validation: PASS

PYTHONPATH=backend python backend/scripts/validate_day_one_launch_estate_gate.py
  → EXIT 0 ; day_one_launch_estate_gate: PASS

PYTHONPATH=backend python backend/scripts/run_architecture_validation_gate.py
  → EXIT 0 ; architecture_validation_gate: PASS
  (frame index, modifier catalogue, day-one, launch estate, context reachability,
   medical intelligence architecture, architecture guardrails, governance regression)

# Targeted pytest (HEALTHIQ_MODE=test, PYTHONPATH=backend)
pytest … test_signal_evaluator.py (full)
  → EXIT 1 ; 1 failure: test_kbs23_catalogue_panel_harness_runs_all_panel_fixtures
    (golden fixture missing biomarkers/user — unrelated to activation_key proofs)

pytest … duplicate_activation_key + multi_frame + arch_rt5e + mr_batch_001b
  → EXIT 0 ; 15 passed

pytest … health_system_card_evidence_arch_rt5b + compiled_hypothesis_arch_rt5c + domain_ux1c
  → EXIT 0 ; 58 passed

pytest … test_arch_rt5d_package_provenance.py
  → EXIT 1 ; 4 failed (stale expected package/card counts)

pytest … test_signal_activation_identity_v1.py + selected multi-frame evaluator tests
  → EXIT 0 ; 5 passed

# Prior batch in session
pytest … domain_ux1c + p2_2_p2_3 retail/pathway + output_authority + day_one_launch_estate governance
  → EXIT 0 ; 33 passed

# Smoke Python inventory (counts / loads / narrative policy)
scan_package_provenance / load_estate_index / get_card_evidence_artefact×10
resolve_narrative_llm_allow_llm(None) without HEALTHIQ_MODE
  → explicit source_spec_id=0; cards load 10/10; narrative default off
```

Latest 20 commits (verbatim from audit baseline):

```text
2a8fa64 Update MR-BATCH-001B benchmark carry-forward status
c465de2 Merge branch 'docs/build-register-mr-batch-001b-session-update' …
6b5d2c8 docs: update BUILD_DELIVERABLE_REGISTER for P3-PROSE-DEPTH-1A and MR-BATCH-001B
4b6d59b MR-BATCH-001B: show full candidate prose in test output
8744b09 Merge branch 'feature/mr-batch-001b-candidate-prose-test-import' …
b7f2256 test(MR-BATCH-001B): add candidate prose test loader and output inspection pathway
6c8ef49 MR-BATCH-001B: product edit candidate prose assets
9be3835 MR-BATCH-001B: recover UTF-8 candidate prose asset file
78e3aaf P3-PROSE-DEPTH-1A: add directional marker-state prose schema rules
df56a35 Merge branch 'feature/p3-prose-depth-1-prose-library-depth-modifier-schema' …
4b106f3 chore(bus): P3-PROSE-DEPTH-1 kernel COMPLETE status
2ddc7b9 fix(P3-PROSE-DEPTH-1): carry-forward YAML syntax; …
f713698 feat(P3-PROSE-DEPTH-1): prose library schema, coverage matrix, and MR Batch 001 foundations
7fd2ddf chore(bus): P3-PROSE-DEPTH-1 work package prompt, hardening, and authority papers
8aea163 Merge branch 'feature/p2-4-narrativepayload-brief-hardening' …
4e38995 chore(bus): P2-4 kernel COMPLETE status
4b3cc42 chore(bus): P2-4 kernel IN_PROGRESS status
b643951 feat(P2-4): harden NarrativePayloadV1 B-to-C brief contract and tests
f150b09 chore(bus): P2-4 work package prompt and hardening
018dc0f chore(bus): P2-2+P2-3 kernel COMPLETE status
```

---

## Appendix B — Test-path versus production-path table

| Area | Test exercises production loader? | Production path exercised by test? | Notes |
|---|---|---|---|
| activation_key / duplicate | Yes (`SignalRegistry`) | Registry load yes; full orchestrator no | Sufficient for registry claims |
| Multi-frame end-to-end | Partial (registry) | Downstream collapse **not** covered as PASS proof | Do not over-claim |
| Card evidence | Yes | Assembler yes | Strong |
| Compiled hyp / root-cause vit D | Yes | Compiler branch yes | Strong for vit D |
| PSI | Loader unit yes; isolation yes | Launch path must **not** load — proven by absence | Deferred |
| MR-BATCH | Test loader only | Production absence asserted | TEST_ONLY |
| Retail/pathway | Registry + pack load | Orchestrator attach/compiler | Strong for presence |
| RT-5D inventory | Scanner yes | Expected counts stale | Failures ≠ gate fail |
| Golden panel harness failure | N/A | Broken fixture | Ignore for wiring claims |
| Architecture gate | Validators + selected pytest | Invariants | Strong for day-one |

---

## Appendix C — Runtime import and consumer map

```text
AnalysisOrchestrator.run
├─ SignalEvaluator / SignalRegistry
│    └─ signal_activation_identity_v1 (activation_key)     [PRODUCTION]
├─ evaluate_signal_evaluation_phase → signal results
├─ build_insight_graph_v1
│    ├─ signal_interaction_builder (signal_id collapse)    [PRODUCTION]
│    └─ compile_report_v1
│         └─ compile_root_cause_v1
│              ├─ compiled_hypothesis (vitamin D only)     [PRODUCTION AUTHORITY]
│              └─ legacy root_cause YAML (other targets)   [PRODUCTION AUTHORITY]
├─ attach_retail_explainers_v1                             [PRODUCTION; fail-open]
├─ publish_interpretation_display_layer_v1                 [PRODUCTION]
├─ compile_narrative_report_v1 (+ pathway packs)           [PRODUCTION]
├─ assemble_consumer_domain_scores_v1
│    └─ wave1_subsystem_evidence
│         └─ health_system_card_evidence                   [PRODUCTION AUTHORITY]
├─ InsightSynthesizer / narrative_runtime_policy           [DEFAULT MOCK]
└─ AnalysisDTO → frontend results consumers                [PRODUCTION PRESENTATION]

NOT ON PATH:
├─ load_promoted_signal_intelligence                       [BUILT_NOT_WIRED]
├─ mr_candidate_prose_test_v1 / MR-BATCH-001B              [TEST_ONLY]
└─ scan_package_provenance (inside run)                    [GATE/SCRIPT ONLY]
```

---

*End of executable codebase and runtime reality audit. No production code, tests, schemas, packages, governance documents, or branch state were modified; only this report file was written.*
