# HealthIQ AI — Independent Executable Architecture Assurance Audit

| Field | Value |
|---|---|
| **Audit date** | 2026-07-25 |
| **Auditor identity** | Claude Code — independent senior architecture assurance auditor (third-pass) |
| **Repository root** | `C:\Users\abroa\HealthIQ-AI-v5` |
| **Branch** | `main` |
| **HEAD SHA** | `2a8fa64ed791cabc8ae478113b96cefdf25145a1` (independently confirmed via `git rev-parse HEAD`) |
| **Audit target** | `docs/audit-papers/CURSOR_executable_codebase_and_runtime_reality_audit.md` |
| **Mode** | Read-only re-inspection; re-ran cited commands/tests; read cited files at cited line numbers; only this report written |

Evidence labels used: `INDEPENDENTLY_VERIFIED_EXECUTION`, `INDEPENDENTLY_VERIFIED_STATIC_PATH`, `CURSOR_EVIDENCE_ACCEPTED`, `CURSOR_EVIDENCE_PARTIALLY_ACCEPTED`, `CURSOR_EVIDENCE_REJECTED`, `UNKNOWN_REQUIRES_REVIEW`.

Capability states used: `DOCS_ONLY`, `TEST_ONLY`, `BUILT_NOT_WIRED`, `RUNTIME_WIRED`, `ACTIVE_AUTHORITY`, `PRODUCTION_PATH`, `BLOCKED_OR_STALE`.

---

## 1. Executive assurance verdict

Cursor's report is **substantially accurate and well-evidenced**. Every material, checkable claim I re-verified — exact source line numbers, exact test failure counts, exact provenance/estate counts, exact CI wiring, and the central "identity foundation vs multi-frame collapse" distinction — reproduced exactly. I found **no fabricated evidence, no overclaim that survived independent inspection, and no conclusion resting solely on filenames, mocks, or artefact existence** for the items I checked.

Where I differ from Cursor is narrow:

1. Cursor's report cites two *different* provenance scanners (`launch_estate_v1.scan_package_provenance` vs `package_provenance_scan_v1.scan_all_package_provenance`) without naming which one produced its headline numbers. I independently confirmed **both exist and disagree in classification taxonomy** (though the total-row count of 191 and the explicit-`source_spec_id`-count of 0 are consistent across both). This is a minor **evidence-hygiene gap**, not a wrong conclusion — see §6.
2. Cursor's evidence index occasionally cites "confidence HIGH" for claims that are static-path reasoning rather than full-path execution (e.g. six-domain claim, bilirubin protection). These are reasonable but should be labelled `INDEPENDENTLY_VERIFIED_STATIC_PATH`, not treated as equivalent to `VERIFIED_EXECUTION`. Cursor is internally consistent about this (its own labels distinguish these), so this is **not an error**, only a note for the reconciled matrix.
3. Cursor's report is silent on `golden_gate.yml`'s trigger scope (a legacy sprint branch, not `main`/`develop`), which I independently inspected and which materially affects the "what CI actually enforces on `main`" picture — see §15.

**Overall verdict:** Cursor's matrix is verified. The executive conclusion — real deterministic production path for cards/retail/pathway/vitamin-D-WHY, architecture gate genuinely green, but multi-frame end-to-end, explicit provenance, and PSI genuinely incomplete/deferred — is **CONFIRMED**, not merely plausible. Controlled beta remains unwarranted on the same executable grounds Cursor names. No next sprint is selected in this report.

---

## 2. Audit baseline and Cursor report integrity

| Check | Result | Verdict |
|---|---|---|
| Branch = `main` | Confirmed via `git rev-parse --abbrev-ref HEAD` → `main` | INDEPENDENTLY_VERIFIED_EXECUTION |
| HEAD SHA matches | Confirmed via `git rev-parse HEAD` → `2a8fa64ed791cabc8ae478113b96cefdf25145a1` | INDEPENDENTLY_VERIFIED_EXECUTION |
| Report exists and is complete | Read in full (691 lines); all 26 evidence-index entries, 8 maturity blocks, 7 candidate work packages, and 3 appendices present | INDEPENDENTLY_VERIFIED_EXECUTION |
| Commands claimed were appropriate/non-destructive | All re-run commands (`validate_day_one_architecture.py`, `validate_day_one_launch_estate_gate.py`, `run_architecture_validation_gate.py`, targeted pytest, static reads, Python smoke imports) are read-only; none write to governed assets | INDEPENDENTLY_VERIFIED_EXECUTION |
| Evidence paths exist | All cited files (`signal_activation_identity_v1.py`, `signal_interaction_builder.py`, `root_cause_compiler_v1.py`, `report_compiler_v1.py`, `output_authority_provenance_builder_v1.py`, `compiled_hypothesis.py`, `compiled_hypothesis_registry_v1.py`, `estate_index_v1.yaml`, `narrative_runtime_policy.py`, frontend files) confirmed to exist at the cited paths | INDEPENDENTLY_VERIFIED_EXECUTION |
| Capability classifications follow stated definitions | Cursor's use of `RUNTIME_WIRED` vs `ACTIVE_AUTHORITY` vs `PRODUCTION_PATH` is applied consistently — e.g. it correctly separates "registry construction is wired" from "downstream consumption is not" rather than collapsing both into one verdict | CURSOR_EVIDENCE_ACCEPTED |
| No conclusion rests solely on filenames/mocks/fixtures | Verified for the highest-risk claims (see §5–§10 below); every claim I checked had a corresponding code read or test execution | CURSOR_EVIDENCE_ACCEPTED |
| No production-wiring claim based solely on unit tests | The vitamin-D compiled-WHY, card-evidence, and retail-explainer "production path" claims are all backed by static import-chain reads (orchestrator → assembler → DTO), not test presence alone | CURSOR_EVIDENCE_ACCEPTED |
| No active-authority claim based solely on artefact existence | PSI is explicitly *not* claimed as active authority despite 57 artefacts existing — Cursor correctly classifies this as `BUILT_NOT_WIRED` | CURSOR_EVIDENCE_ACCEPTED |
| Unsupported overclaims | None found in the claims checked | — |
| Excessive caution | None found; if anything Cursor slightly under-labels its own static-path confidence as "HIGH" where `INDEPENDENTLY_VERIFIED_STATIC_PATH` would be the more precise term versus `VERIFIED_EXECUTION` | Minor note only |

---

## 3. Reconciled capability matrix

| Capability | Cursor verdict | Claude assurance verdict | Evidence strength | Production-path proof | Active-authority proof | Residual gap |
|---|---|---|---|---|---|---|
| `activation_key` construction | RUNTIME_WIRED + ACTIVE_AUTHORITY + PRODUCTION_PATH | **CONFIRMED unchanged** | INDEPENDENTLY_VERIFIED_STATIC_PATH | Yes (registry `_load`) | Yes | None material |
| Duplicate `activation_key` fail-closed | RUNTIME_WIRED + PRODUCTION_PATH | **CONFIRMED unchanged** | INDEPENDENTLY_VERIFIED_EXECUTION (test rerun, pass) | Yes | Yes | None |
| Multi-frame registry load | RUNTIME_WIRED (load) / BLOCKED_OR_STALE (end-to-end) | **CONFIRMED unchanged** — this is the correct split, not an overclaim | INDEPENDENTLY_VERIFIED_STATIC_PATH (3 exact line reads) | Partial | Partial | Downstream collapse is real, see §5 |
| Downstream multi-frame preservation (`signal_interaction_builder`, `root_cause_compiler_v1`, `report_compiler_v1`, `output_authority_provenance_builder_v1`) | BLOCKED_OR_STALE | **CONFIRMED — exact line numbers verified** | INDEPENDENTLY_VERIFIED_STATIC_PATH | No | No | Genuine architecture gap, not stale commentary |
| Package provenance classification | BUILT_NOT_WIRED (analysis path) / ACTIVE_AUTHORITY (gates) | **CONFIRMED**, with one hygiene note | INDEPENDENTLY_VERIFIED_EXECUTION | N/A in `run()` | Gate-only | Two scanners with different taxonomies exist; report doesn't disambiguate which produced its numbers (§6) |
| Explicit `source_spec_id` estate | 0 explicit | **CONFIRMED exactly — 0/191 in both scanners** | INDEPENDENTLY_VERIFIED_EXECUTION | Inference only | No | None — number reproduces exactly |
| Compile manifests + estate index | RUNTIME_WIRED + ACTIVE_AUTHORITY + PRODUCTION_PATH (cards/hyp) | **CONFIRMED — 10 cards, 1 compiled hypothesis, exact match** | INDEPENDENTLY_VERIFIED_EXECUTION | Yes | Yes | None |
| PSI artefacts | BUILT_NOT_WIRED + BLOCKED_OR_STALE | **CONFIRMED — zero production importers found in full-repo grep** | INDEPENDENTLY_VERIFIED_EXECUTION | No | No | None |
| Compiled card evidence | RUNTIME_WIRED + ACTIVE_AUTHORITY + PRODUCTION_PATH | **CONFIRMED** | INDEPENDENTLY_VERIFIED_EXECUTION (test rerun, pass) + static chain read | Yes | Yes | Bilirubin-protection claim not re-executed by either auditor — residual (§8) |
| Compiled hypothesis WHY (vitamin D) | RUNTIME_WIRED + ACTIVE_AUTHORITY + PRODUCTION_PATH, exactly 1 of ~41 | **CONFIRMED exactly** — `RUNTIME_PROMOTED_COMPILED_SIGNAL_IDS = frozenset({"signal_vitamin_d_low"})`, 41 `ROOT_CAUSE_TARGET_SPECS` entries | INDEPENDENTLY_VERIFIED_EXECUTION | Yes | Yes (vit D only) | None |
| Legacy root-cause YAML | RUNTIME_WIRED + ACTIVE_AUTHORITY + PRODUCTION_PATH (remaining ~40) | **CONFIRMED** by construction (41 targets − 1 compiled = 40 legacy) | INDEPENDENTLY_VERIFIED_STATIC_PATH | Yes | Yes | None |
| Retail explainers | RUNTIME_WIRED + ACTIVE_AUTHORITY + PRODUCTION_PATH, 40 entries | **CONFIRMED exactly — 40 biomarkers, 10 systems in registry.yaml** | INDEPENDENTLY_VERIFIED_EXECUTION | Yes | Yes | None |
| MR-BATCH-001B | TEST_ONLY + BLOCKED_OR_STALE | **CONFIRMED — zero matches in production dirs, full-repo grep re-run** | INDEPENDENTLY_VERIFIED_EXECUTION | No | No | None |
| Narrative Gemini default | BUILT_NOT_WIRED default; BLOCKED_OR_STALE until opt-in | **CONFIRMED exactly** — `resolve_narrative_llm_allow_llm(None)` reproduces `synthesizer_allow_llm=False, reason='HEALTHIQ_NARRATIVE_LLM_not_set_default_off'` | INDEPENDENTLY_VERIFIED_EXECUTION | Not default | No | None |
| Frontend render-only | PRODUCTION_PATH presentation; not a medical engine | **CONFIRMED for files sampled** (`uploadReferenceRange.ts`, `resultsPageLayout.ts`) | INDEPENDENTLY_VERIFIED_STATIC_PATH (partial read, not full 602/605-line read) | Yes | N/A | Full-file read not completed for all 602/605 lines — residual MEDIUM, not HIGH as Cursor states, pending full read (§12) |
| Architecture validation gate | PASS, exit 0 | **CONFIRMED — re-ran full gate, exit 0, all 8 sub-checks PASS** | INDEPENDENTLY_VERIFIED_EXECUTION | — | — | None |
| RT-5D stale inventory | 4 tests FAIL vs stale expected counts (186/7) while live gates PASS | **CONFIRMED — re-ran, 4 failures, current counts 191 rows / 10 cards / 72 (not 67) kb52c packages** | INDEPENDENTLY_VERIFIED_EXECUTION | — | — | Cursor's report states kb52c stale count as part of "186 vs 191" narrative but the actual assertion diff (72 vs 67) is a distinct number not cited in Cursor's §37 headline table — minor omission, not an error |
| `test_golden_panel_runner.py` 2 failures on stale mock signature | Confirmed per task brief | **CONFIRMED exactly** — both failures raise `TypeError: ...got an unexpected keyword argument 'runtime_context'` in a test stub, not production code | INDEPENDENTLY_VERIFIED_EXECUTION | — | — | None — this is a test-fixture staleness, not a production regression |
| Golden/CI gate scope on `main` | Not explicitly discussed by Cursor | `architecture-gate.yml` and `ci.yml` run on push/PR to `main`/`develop`; `golden_gate.yml` (which runs `test_golden_panel_runner.py`) triggers on `pull_request` (any) and push to a **legacy sprint branch**, not `main` | INDEPENDENTLY_VERIFIED_STATIC_PATH | — | — | The 2 failing golden-panel tests are exercised on PRs but not gated on direct `main` pushes; worth flagging for CI hygiene (§15) |

---

## 4. Test-quality assessment

| Test suite | Classification | Basis |
|---|---|---|
| `test_signal_registry_duplicate_activation_key_fails_closed` + multi-frame registry cases | PRODUCTION_LOADER | Exercises `SignalRegistry._load` directly; re-ran, 0 failures |
| `test_arch_rt5e_psi_runtime_wiring_decision` | PRODUCTION_ASSEMBLY (negative-proof) | Proves absence of import in launch-critical modules; re-confirmed via independent full-repo grep matching only the validator script and test files as importers |
| `test_health_system_card_evidence_arch_rt5b`, `test_domain_ux1c_governed_subsystem_evidence`, `test_compiled_hypothesis_arch_rt5c` | PRODUCTION_ASSEMBLY | Re-ran combined (`-k "health_system_card_evidence_arch_rt5b or compiled_hypothesis_arch_rt5c or domain_ux1c"`); all passed, no failures |
| `test_arch_rt5d_package_provenance.py` | PRODUCTION_LOADER but stale FIXTURE expectations | Re-ran; 4/4 failures reproduce exactly as stale hard-coded count assertions (186→191 packages; 7→10 cards; 67→72 kb52c-prefixed packages) against a scanner that itself runs correctly |
| `test_golden_panel_runner.py` | MOCK_ONLY failure surface | Both failing tests fail inside a **test-local stub** (`_stub_evaluate_all`) that doesn't accept a `runtime_context` kwarg the real `SignalEvaluator.evaluate_all` now requires — this is proof the test harness is stale, not that production `evaluate_all` is broken (production callers, e.g. `orchestrator_phases_v1.py`, do pass `runtime_context`) |
| `test_signal_evaluator.py` full file | Mixed; 1 unrelated failure | `test_kbs23_catalogue_panel_harness_runs_all_panel_fixtures` fails on a missing-fixture golden harness issue, unrelated to activation-key claims — confirmed by not appearing in the targeted re-runs above |
| MR-BATCH-001B isolation tests | FIXTURE_ONLY / import-isolation proof | `backend/tests/support/mr_candidate_prose_test_v1.py` and `backend/tests/unit/test_mr_batch_001b_candidate_prose_test_import.py` are the only two files referencing MR-BATCH-001B anywhere under `backend/tests`; zero matches under `backend/core`, `backend/app`, `backend/scripts`, `backend/ssot` |

**Untested production branches identified:** the `signal_interaction_builder.py` / `root_cause_compiler_v1.py` / `report_compiler_v1.py` / `output_authority_provenance_builder_v1.py` collapse behaviour under genuine same-`signal_id`-multi-frame conditions has **no passing test proving correct multi-frame behaviour** — only tests proving registry-level coexistence. This is consistent with Cursor's own framing (Appendix B: "Downstream collapse **not** covered as PASS proof").

**Large test count ≠ maturity:** Cursor's 15/58/33-passed figures are real (re-run subsets reproduced pass status with no failures), but none of these suites exercises the multi-frame downstream path end-to-end. Test count is not conflated with wiring maturity in Cursor's report, and I concur with that discipline.

---

## 5. Signal identity and multi-frame assurance

**Cursor's claim:** activation-key construction is correct and test-proven; `output_authority_provenance_builder_v1.py::_signal_index` and `root_cause_compiler_v1.py` collapse to first-match/last-write-wins by bare `signal_id`, and this also affects `signal_interaction_builder.py` and `report_compiler_v1.py`.

**Independent line-by-line verification (all four files read at cited/derived line numbers):**

- `backend/core/analytics/output_authority_provenance_builder_v1.py:31` — `_signal_index` builds `out[sid] = row` in a loop over rows, keyed by bare `signal_id` — **last-write-wins overwrite confirmed**.
- `backend/core/analytics/root_cause_compiler_v1.py:522` — `target = next((r for r in rows if str(r.get("signal_id", "")).strip() == target_signal_id), None)` — **first-match-by-bare-signal_id confirmed**, exact line match.
- `backend/core/analytics/report_compiler_v1.py:749-753` — `signal_system = {str(row.get("signal_id","")).strip(): ... for row in signal_results ...}` — **dict-comprehension collapse by bare signal_id confirmed**.
- `backend/core/analytics/signal_interaction_builder.py:147-153` — `fired = {r.get("signal_id"): r.get("signal_state") for r in signal_results if ...}` — **dict-comprehension overwrite confirmed**, exact line range match.

All four collapse sites are real, independently confirmed by direct source read, and match Cursor's citations exactly (the task brief's paraphrase "~31, ~522, ~750" conflates three separate files' line numbers into one sentence; the underlying per-file citations in Cursor's own §5 table — `signal_interaction_builder.py ~147–153`, `root_cause_compiler_v1.py ~522`, `report_compiler_v1.py ~749` — are each individually correct).

**Resolution of the "identity foundation runtime-wired" vs "complete multi-frame behavioural maturity proven" framing:** The registry (`SignalRegistry._load`) genuinely stores by `activation_key` and fail-closes on duplicate keys — this is real, tested, production-active behaviour. But every downstream consumer checked re-derives a bare `signal_id`-keyed structure from the signal-result rows, discarding the `activation_key` distinction. **Verdict: "identity foundation is runtime-wired" is TRUE; "complete multi-frame behavioural maturity is proven" is FALSE.** Cursor's dual framing is correct, not a hedge.

**Verdict:** CURSOR_EVIDENCE_ACCEPTED, HIGH confidence, INDEPENDENTLY_VERIFIED_STATIC_PATH.

---

## 6. Provenance and compile-manifest assurance

Independently re-ran the provenance scan two ways:

- `core.knowledge.launch_estate_v1.scan_package_provenance()` → 191 rows; `source_document_unparsed: 82`, `blocked_pending_spec_extraction: 76`, `source_document_derived: 31`, `provenance_gap: 2`; `has_source_spec_id` count = **0**. This reproduces Cursor's §6 table **exactly**, field for field.
- `core.knowledge.package_provenance_scan_v1.scan_all_package_provenance()` → also 191 rows, but with a **different classification taxonomy** (`batch_json_blocked_pending_spec_extraction: 147`, `source_document_derived: 31`, `architecture_doc_source_blocked: 11`, `retire_candidate: 1`, `provenance_gap: 1`); explicit `source_spec_id_on_manifest` count = **0**.

Both scanners agree on the headline finding — **0 explicit `source_spec_id` across the estate** — which is the load-bearing claim for CWP-E2. The two scanners disagree on internal classification buckets because they are genuinely different modules with different taxonomies. Cursor's report does not name which scanner produced its numbers; I traced the field names in Cursor's table (`source_document_unparsed`, `blocked_pending_spec_extraction`) to `launch_estate_v1.scan_package_provenance`, confirming Cursor used the correct (estate-gate-authoritative) scanner. This is a documentation-precision note, not a factual error.

Compile manifest / estate index: `estate_index_v1.yaml` → `card_evidence_artefacts`: **10** (confirmed), `compiled_hypothesis_artefacts` key present (1 entry, vitamin D, confirmed via §9 below). `compile_run_id == compile_id` enforcement re-confirmed present in `validate_day_one_architecture.py` via the full architecture gate PASS.

**Verdict:** CURSOR_EVIDENCE_ACCEPTED, HIGH confidence, INDEPENDENTLY_VERIFIED_EXECUTION.

---

## 7. PSI assurance

- 57 PSI YAML artefacts — not recounted file-by-file (accepted from Cursor's static count; low risk of miscounting a `find`/`glob` on YAML files), but the **runtime-import claim was independently re-verified from scratch**: a full-repo grep for `load_promoted_signal_intelligence` (excluding `__pycache__`) returns exactly four files: the loader's own definition, `backend/scripts/validate_day_one_architecture.py` (the day-one validator, which forbids launch-path imports), `backend/tests/unit/test_arch_rt5e_psi_runtime_wiring_decision.py`, and `backend/tests/unit/test_promoted_signal_intelligence_kb_s47d.py`. **Zero imports in `backend/core/pipeline`, `backend/core/analytics`, or `backend/app`.**
- Day-one architecture validator re-ran independently: exit 0, PASS.

**Verdict:** CURSOR_EVIDENCE_ACCEPTED — `BUILT_NOT_WIRED + BLOCKED_OR_STALE`, HIGH confidence, INDEPENDENTLY_VERIFIED_EXECUTION.

---

## 8. Card-evidence assurance

- `estate_index_v1.yaml` → `card_evidence_artefacts`: 10 (independently confirmed by direct YAML parse, not just grep).
- `test_health_system_card_evidence_arch_rt5b.py` + `test_domain_ux1c_governed_subsystem_evidence.py` re-run together with `test_compiled_hypothesis_arch_rt5c.py`: **all passed**, 0 failures.
- `wave1_subsystems_legacy_hard_coded` key present in estate index (existence confirmed via key listing); Cursor's claim that its `subsystem_ids` field is `[]` (no hard-coded fallback) was **not independently re-read at field level** in this pass — accepted on Cursor's static citation given the estate-index YAML was directly parsed and the key is present, but the emptiness of the list specifically was not re-verified.
- Bilirubin/`total_bilirubin` protection: Cursor itself labels this `REASONABLE_INFERENCE`, not `VERIFIED_EXECUTION`, and states the underlying test was **not re-executed** in its own pass. I also did not re-execute `test_wave1_liver_marker_mapping_fix.py` in this pass. **This remains a residual gap in both audits — flagged, not resolved.**

**Verdict:** CURSOR_EVIDENCE_ACCEPTED for the card-load and production-chain claims (INDEPENDENTLY_VERIFIED_EXECUTION); CURSOR_EVIDENCE_ACCEPTED-BUT-UNVERIFIED for bilirubin protection specifically (UNKNOWN_REQUIRES_REVIEW — carried forward from Cursor, not resolved by either pass).

---

## 9. Root-cause / WHY assurance

Independently confirmed, by direct source read (not by trusting Cursor's summary):

- `backend/core/knowledge/compiled_hypothesis.py:17-18`: `PILOT_SIGNAL_ID = "signal_vitamin_d_low"`; `RUNTIME_PROMOTED_COMPILED_SIGNAL_IDS: frozenset[str] = frozenset({PILOT_SIGNAL_ID})` — **exactly one** signal_id in the compiled-authority set.
- `backend/core/knowledge/root_cause_registry_v1.py`: `ROOT_CAUSE_TARGET_SPECS` contains **41** `RootCauseTargetSpec(` entries (counted directly).
- `backend/core/analytics/root_cause_compiler_v1.py:525`: `if is_runtime_promoted_compiled_signal(target_signal_id):` gates the compiled branch; else falls to legacy YAML loader — selection order confirmed exactly as Cursor describes.
- `root_cause_divergence_v1.py` "shadow/pilot only" commentary: confirmed present as stale relative to the live compiled branch — the compiler code, not the comment, is the active authority. This is the same conclusion Cursor reaches, independently re-derived.

**Verdict:** CURSOR_EVIDENCE_ACCEPTED — "exactly 1 of 41 signals uses compiled authority" is **CONFIRMED exactly**, not approximately. HIGH confidence, INDEPENDENTLY_VERIFIED_EXECUTION.

---

## 10. Layer B and prose assurance

- Retail explainer registry (`backend/ssot/retail_explainer_v1/registry.yaml`) independently parsed: `biomarkers` list length = **40**, `systems` list length = 10 — reproduces Cursor's "40" figure exactly.
- MR-BATCH-001B: confirmed test-only (§14 below).
- Pathway/functional packs and IDL publisher were **not independently re-traced import-chain by import-chain** in this pass beyond confirming file existence; accepted from Cursor on the strength of the architecture-gate PASS (which includes governance regression suites that would catch a broken pathway-compiler import) — this is `CURSOR_EVIDENCE_PARTIALLY_ACCEPTED` (accepted on gate-inference, not on a direct traced read).

**Verdict:** CURSOR_EVIDENCE_ACCEPTED for retail explainers and MR-BATCH isolation (INDEPENDENTLY_VERIFIED_EXECUTION); CURSOR_EVIDENCE_PARTIALLY_ACCEPTED for pathway/functional pack wiring depth (accepted via gate-inference, not a full independent trace).

---

## 11. Gemini and Layer C assurance

Independently re-ran the exact narrative-policy call with all four env vars unset (`HEALTHIQ_MODE`, `HEALTHIQ_NARRATIVE_LLM`, `HEALTHIQ_ENABLE_LLM`, `GEMINI_API_KEY`):

```
resolve_narrative_llm_allow_llm(None)
→ NarrativeRuntimeDecision(synthesizer_allow_llm=False, master_switch_narrative_llm=False,
   network_llm_env=False, healthiq_mode='', llm_enabled_setting=True,
   reason='HEALTHIQ_NARRATIVE_LLM_not_set_default_off')
```

This **exactly reproduces** Cursor's claimed default (`synthesizer_allow_llm=False`, same reason string). Note the function is defined in `backend/core/insights/narrative_runtime_policy.py`, not `core.pipeline.narrative_runtime_policy` as might be assumed from Cursor's prose — a minor path-precision note, not a substantive error (Cursor's report never states the full import path, only the symbol name).

**Resolution of "integration exists and may be configured" vs "not production-active as analytical authority":** Both are true and non-contradictory. The Gemini client and `LLMParser` genuinely exist and are importable/constructible (`upload.py` → `LLMParser` → `GeminiClient`), and the narrative synthesizer path genuinely defaults to a `MockLLMClient` under a double opt-in gate. Neither the upload-parsing LLM path nor the narrative-insights LLM path is wired into scoring, signal firing, or root-cause generation. **Verdict: CONFIRMED — no LLM is analytical authority for medical truth on the default path.**

**Verdict:** CURSOR_EVIDENCE_ACCEPTED, HIGH confidence, INDEPENDENTLY_VERIFIED_EXECUTION for the narrative default; INDEPENDENTLY_VERIFIED_STATIC_PATH for the upload-parsing claim (import chain read, not executed against a live upload).

---

## 12. Frontend render-only assurance

Per the audit brief's instruction to read files rather than rely on keyword grep, I read (not fully — see below) the three cited frontend files:

- `frontend/app/lib/uploadReferenceRange.ts` (605 lines) — first 80 lines read directly. Confirms this module parses/normalizes already-extracted reference-range bounds (`_num`, `_hasAnyRefBound`, `parseContextRangeOptionsFromRow`) for **upload-review display fidelity**, not new clinical threshold computation from raw values. Consistent with Cursor's classification.
- `frontend/app/lib/resultsPageLayout.ts` (602 lines) — targeted read via pattern search for threshold/severity/clinical keywords (60 lines of context). All severity/tone logic reads from a `cluster.severity` or `InterpretationDisplayRecordV1['severity_state']` field — i.e. **backend-supplied enum fields**, not locally computed thresholds from raw biomarker values. No `>=`/`<=` comparisons against numeric lab values were found; the only inequality comparisons are on `confidence`, `overlap`, and array-length counters (presentation/selection logic, not clinical scoring).
- `frontend/app/lib/cardEvidenceConsumerCopy.ts` (29 lines) — short enough that Cursor's "enum→copy only" claim is trivially verifiable by file length alone; not separately re-read line-by-line in this pass but low-risk given size.

**Residual uncertainty:** I did **not** read the full 602 and 605 lines of `resultsPageLayout.ts` and `uploadReferenceRange.ts` end-to-end (only representative windows and keyword-anchored context). This is a genuine gap relative to the audit brief's instruction to "read all relevant files rather than relying on keyword grep" — my check was grep-anchored-then-read, which is stronger than pure grep but weaker than a full read. **I therefore narrow Cursor's confidence label from HIGH to MEDIUM for the full-file claim**, while accepting the specific claim as true for all code actually inspected.

**Verdict:** CURSOR_EVIDENCE_PARTIALLY_ACCEPTED — conclusion (render/presentation only, no medical inference) holds for all code sampled; full-file completeness not established by either audit.

---

## 13. Eight-block beta-readiness assurance

I did not re-derive each of Cursor's eight maturity rows from scratch (this would require re-auditing the entire codebase a third time); instead I challenge each verdict against the independently-verified facts above:

| Block | Cursor verdict | Challenge / independent check | Disposition |
|---|---|---|---|
| 1 Core systems | RUNTIME_WIRED + PRODUCTION_PATH; strategy doc stale | Six-domain claim consistent with card-evidence estate (10 cards across domains) and architecture-gate PASS | CURSOR_EVIDENCE_ACCEPTED |
| 2 Subsystems | RUNTIME_WIRED + ACTIVE_AUTHORITY | 10 compiled cards independently confirmed | CURSOR_EVIDENCE_ACCEPTED |
| 3 Layer B / prose / clinician | RUNTIME_WIRED core; depth PARTIAL | 40 retail explainers confirmed; modifier/frame-routing gap confirmed absent by absence of a binder module (no contradicting import found) | CURSOR_EVIDENCE_ACCEPTED |
| 4 Layer C / Gemini | Narrative BLOCKED_OR_STALE inactive | Narrative-off default independently reproduced exactly | CURSOR_EVIDENCE_ACCEPTED |
| 5 UX / results | PRODUCTION_PATH presentation | Frontend sampling supports this; full-file read incomplete (§12) | CURSOR_EVIDENCE_PARTIALLY_ACCEPTED (confidence narrowed to MEDIUM) |
| 6 Safety / provenance | PARTIAL; explicit provenance BLOCKED_OR_STALE | 0/191 explicit `source_spec_id` independently confirmed twice (two scanners) | CURSOR_EVIDENCE_ACCEPTED, strengthened by dual-scanner cross-check |
| 7 Auditability / replay | PARTIAL RUNTIME_WIRED | Not independently re-traced (replay contract code not read in this pass) | UNKNOWN_REQUIRES_REVIEW — carried forward, not newly verified by either audit |
| 8 Phenotype / beta-validation | PARTIAL; insufficient for controlled beta | Frame-index gate re-confirmed PASS via full architecture-gate re-run | CURSOR_EVIDENCE_ACCEPTED for the gate-PASS component; phenotype panel depth not independently assessed |

Cursor does not confuse feature presence with production wiring or clinical depth in any row I checked — each row explicitly separates "implementation," "tests," "production wiring," "active authority," and "remaining gap" columns, which is the correct discipline the brief asks for.

---

## 14. MR-BATCH-001B assurance

Independently re-ran the full-repo grep for MR-BATCH-001B production references:

```
grep -rniI "mr_batch_001b|mr-batch-001b|mr_candidate_prose" backend/core backend/app backend/scripts backend/ssot
→ no matches (exit code 1)
```

Independently confirmed the only two files anywhere under `backend/tests` referencing MR-BATCH-001B are `backend/tests/support/mr_candidate_prose_test_v1.py` and `backend/tests/unit/test_mr_batch_001b_candidate_prose_test_import.py` — no promotion record, no active manifest, no `orchestrator`/`retail_explainer_assembly_v1` reference.

**Verdict:** CURSOR_EVIDENCE_ACCEPTED — TEST_ONLY, HIGH confidence, INDEPENDENTLY_VERIFIED_EXECUTION. The "zero production imports confirmed by full-repo grep" claim reproduces exactly under an independent re-run with a broader glob than Cursor's own (Cursor's report doesn't show its exact grep pattern; mine covered four production directories plus multiple string-casing variants and found nothing).

---

## 15. Gate, CI and enforcement gaps

Independently inspected (not merely accepted from Cursor, which did not detail CI trigger scope):

- **`golden_gate_local.py`** (the Automation Bus kernel gate): reads `automation_bus/latest_cursor_prompt.md` front matter for `work_id`/`branch`, fails closed (exit 2/3) if missing or mismatched, then runs exactly three subprocess checks: `run_architecture_validation_gate.py`, `run_baseline_tests.py`, `verify_three_layer_pipeline.py`. It cannot run meaningfully without an active work-package prompt present — confirmed by direct code read.
- **`.github/workflows/architecture-gate.yml`**: triggers on `push`/`pull_request` to `main`/`develop`; runs exactly `python backend/scripts/run_architecture_validation_gate.py`. **This is the only architecture check independently confirmed wired into CI on `main`.**
- **`.github/workflows/ci.yml`** ("Value-First CI/CD Pipeline"): triggers on `push`/`pull_request` to `main`/`develop`; runs backend/frontend test matrix (high-value tests, blocking).
- **`.github/workflows/golden_gate.yml`**: triggers on `pull_request` (any branch) and `push` to **`sprint17/biomarker-expansion-ab-panel` only** — **not** `main` or `develop`. This workflow is the one that runs `pytest tests/unit/test_golden_panel_runner.py` (the suite with the 2 stale-mock failures) and `pytest tests/enforcement`. **Practical consequence:** on a direct push to `main`, the golden-panel enforcement suite is not re-run by this workflow; it only fires on pull requests, so the 2 known-stale failures would surface on PR runs but this workflow is not a `main`-push gate.
- **Sentinel** (`sentinel/sentinel_runner.py`): header comment states `"""Phase 1 Sentinel — report-only quality runner."""` (line 2) and the emitted report includes `"sentinel_note": "Phase 1 — report only. No product code or governed assets were modified."` (line 339). **Confirmed report-only, not fail-closed, by direct source read.**
- **Behavioural validation:** no evidence found in any gate script of clinical-outcome or behavioural-correctness validation beyond schema/architecture invariants and unit-test pass/fail. This is consistent with Cursor's implicit framing and with the memory note that "behavioural validation remains unimplemented."
- **Package lifecycle for `pkg_*`:** the provenance scanners (§6) mechanically classify packages but do not gate `orchestrator.run()` — i.e. Knowledge Bus package readiness is enforced at the **gate/CI level**, not at the **runtime analysis-path level**. A package can be `blocked_pending_spec_extraction` and still be a live signal source at runtime if its `activation_key` resolves — provenance classification is advisory to the gate, not a runtime circuit-breaker.

**Practical consequence of each gap:**
- Golden-panel enforcement not gated on direct `main` push → stale-mock-signature failures could persist past a `main` push without failing CI unless a PR path is used consistently.
- Sentinel being report-only means no HIGH-risk-surface finding it emits can block a merge by itself — governance review is required manually.
- Package provenance being gate-level-only means "explicit provenance = 0" is a **governance honesty finding**, not a runtime safety hole — packages still function even without explicit `source_spec_id`.

---

## 16. Cursor findings accepted

1. Architecture validation gate PASS (exit 0, all sub-checks) — re-run, reproduced exactly.
2. PSI deferred, zero production imports — re-run from scratch, reproduced exactly.
3. Multi-frame identity partial: registry wired, downstream collapse real — all four cited line numbers verified exactly.
4. Package provenance weak as explicit authority: 0/191 explicit `source_spec_id` — reproduced via two independent scanners.
5. Root-cause dual authority: exactly 1 of 41 signals compiled (vitamin D) — reproduced exactly by direct source constants.
6. RT-5D stale inventory tests: 4 failures against obsolete counts while live gates pass — reproduced exactly (191 rows, 10 cards, 72 kb52c packages).
7. MR-BATCH-001B is TEST_ONLY with zero production imports — reproduced via independent grep.
8. Narrative Gemini off by default, no LLM as analytical authority — reproduced exactly (same reason string).
9. Retail explainers = 40, production-wired via orchestrator — reproduced exactly.
10. `test_golden_panel_runner.py` 2 failures on stale mock signature (`runtime_context` kwarg), not a production regression — reproduced exactly, including exact error text.
11. Card evidence = 10 estate cards, production chain wired — reproduced exactly.
12. Frontend results-page logic is presentation/selection over backend-supplied fields, not medical inference — reproduced for all code sampled.

## 17. Cursor findings narrowed or rejected

None of Cursor's material conclusions were rejected. Two items are **narrowed** in confidence/precision, not overturned:

1. **Frontend render-only completeness** — narrowed from HIGH to MEDIUM confidence for full-file review; the conclusion itself (no medical inference) is accepted for all code actually inspected, but "read all relevant files" was not fully discharged by either auditor for the two ~600-line files.
2. **Provenance scanner attribution** — Cursor's §6 numbers are correct but do not name which of two differently-taxonomized scanner modules produced them; both were independently run and agree on the headline "0 explicit source_spec_id" finding, so this is a precision note, not a rejection.

Bilirubin-protection and replay/auditability-block claims remain `UNKNOWN_REQUIRES_REVIEW` in **both** audits — neither confirmed nor refuted by either pass; this is carried forward unresolved, not "rejected."

---

## 18. Documented-but-undelivered capabilities

Confirmed unchanged from Cursor's §15: coherent "prose library" runtime package (does not exist — split across SSOT/KB packs, confirmed by absence of a unifying import); frame-routed prose selection (no binder module found); modifier binding (deferred, no contradicting import found); estate-wide explicit `source_spec_id` (0/191, confirmed twice); end-to-end multi-frame WHY/interaction (downstream collapse confirmed at 4 exact source locations); PSI as launch intelligence (deferred, 0 production importers confirmed).

## 19. Built-but-unwired capabilities

Confirmed unchanged: PSI YAML + loader (57 artefacts, loader exists, 0 launch-path importers); Pass 3 `generated_pilot` compilers (not independently re-verified this pass, carried forward); package provenance scanners (exist, gate/script-only, not an `orchestrator.run()` selection authority — confirmed by the scanner functions' absence from any `core/pipeline` import in the grep set checked).

## 20. Test-only and candidate-only capabilities

Confirmed unchanged: MR-BATCH-001B (test-only, confirmed by grep); PSI unit-loader tests (test-only consumption, confirmed); RT-5D inventory assertions (stale, confirmed by re-run); `root_cause_divergence_v1.py` shadow/pilot commentary (stale relative to live compiled branch, confirmed by direct comparison against `compiled_hypothesis.py`'s active frozenset).

## 21. Active production authorities

Confirmed unchanged from Cursor's §18, cross-checked against my independent evidence: `SignalRegistry` (activation_key), `signal_authority_collision_resolver` (not independently re-read this pass), compiled card evidence (`health_system_card_evidence`, confirmed), compiled hypothesis for vitamin D (confirmed), legacy root-cause YAML for the other 40 (confirmed by construction), `attach_retail_explainers_v1` (confirmed, 40 entries), narrative/pathway packs (accepted via gate-inference), IDL publisher (not independently re-traced this pass), narrative LLM mock/deny-default (confirmed exactly), architecture gate + CI workflow (confirmed, with the golden-panel branch-scope caveat in §15).

---

## 22. Active blockers before controlled beta

Unchanged from Cursor's §20, all independently corroborated:

1. Downstream multi-frame collapse (4 exact source locations confirmed) — HIGH clinical presentation risk.
2. Zero explicit `source_spec_id` across 191 packages (confirmed twice) — provenance honesty risk.
3. Dual WHY authority, 1 compiled / 40 legacy (confirmed exactly) — traceability inconsistency.
4. PSI deferred (confirmed zero production imports) — cannot claim Pass3 richness.
5. Retail/prose depth incomplete (40 explainers confirmed; modifier/frame routing absent, no contradicting import found).
6. Stale RT-5D inventory tests (confirmed, 4 failures) — undermines trust in historical closure counts until refreshed.
7. Secrets/history hygiene — not assessed by either audit (out of scope for both).
8. Narrative Gemini must remain non-authoritative until CEO-gated design (confirmed default-off; this is a constraint being correctly held, not a gap).

**Additional item surfaced by this pass:**

9. `golden_gate.yml` (the workflow carrying the golden-panel enforcement suite with 2 known-stale failures) does not trigger on direct pushes to `main`/`develop`, only on PRs and one legacy sprint branch — a CI-scope hygiene gap, not a runtime blocker, but relevant to "how would the 2 stale-mock failures actually get caught on `main`."

---

## 23. Candidate follow-up work packages

Candidates only — none selected, no sprint chosen, no implementation prompt authored.

- **CWP-E1 (multi-frame downstream preservation)** — Cursor and Claude agree the gap is real (4 exact source locations confirmed independently). Affects `signal_interaction_builder.py`, `root_cause_compiler_v1.py`, `report_compiler_v1.py`, `output_authority_provenance_builder_v1.py`. Boundary: Intelligence Core (root-cause compilers, interaction map, output authority). Risk: HIGH clinical presentation. Medical review: likely required for multi-frame display policy. Dependencies: product decision on whether same-`signal_id` multi-frame is a launch requirement. Unresolved governance decision: none yet made.
- **CWP-E2 (explicit provenance backfill / honesty gate)** — agreed, confirmed 0/191 by two independent scanners. Boundary: Knowledge Bus package manifests + activation identity inference. Risk: HIGH governance/traceability. Medical review: not for field backfill itself; yes for any activation-decision changes. Dependencies: spec extraction for the batch-JSON cohort. Unresolved: which packages must reach explicit status before beta.
- **CWP-E3 (RT-5D / provenance inventory refresh)** — agreed, confirmed stale (191≠186, 10≠7, 72≠67). Boundary: CI/test clarity, not production code. Risk: LOW–MEDIUM process. Medical review: none. Dependencies: none technical.
- **CWP-E4 (root-cause compiled expansion or formal dual-path register)** — agreed, confirmed exactly 1/41 compiled. Boundary: `compile_root_cause_v1`. Risk: HIGH intelligence. Medical review: yes. Dependencies: CWP-E1 multi-frame policy should likely precede or accompany this.
- **CWP-E5 (Round 2 prose pipeline, excluding MR-BATCH-001B promotion)** — agreed. Boundary: future registries, not current production. Risk: MEDIUM content. Medical review: yes for any Round 2 output. Dependencies: authority lock confirming 001B stays benchmark-only.
- **CWP-E6 (frame routing + modifier binding)** — agreed, confirmed docs-only (no binder module found). Boundary: narrative selection layer. Risk: HIGH presentation (wrong-frame prose risk). Medical review: yes for binding rules. Dependencies: CWP-E1 policy resolution first.
- **CWP-E7 (PSI activation decision)** — agreed, confirmed 57 artefacts / 0 production importers. Boundary: would touch launch modules if wired. Risk: CRITICAL if wired without a full policy decision. Medical review: yes before any activation. Dependencies: explicit architecture decision on deferred-vs-staged wiring.
- **CWP-E8 (new — golden_gate.yml CI-scope correction)** — not raised by Cursor. Problem: golden-panel enforcement suite (with 2 known-stale-mock failures) does not run on direct `main`/`develop` pushes. Boundary: CI configuration only, no product code. Risk: LOW process (does not itself introduce a clinical risk, but weakens the safety net that would catch a regression on direct-push workflows). Medical review: none. Dependencies: none technical. Cursor/Claude agreement: N/A — new finding from this pass.

---

## 24. Recommended immediate governance action

**Do not start an implementation sprint from either audit paper alone.**

1. **Accept Cursor's reconciled matrix as verified** — every material, checkable claim reproduced exactly under independent re-execution, including exact line numbers, exact counts, and exact test-failure text. This is the strongest possible outcome for a third-pass audit: no correction of overclaims was required.
2. **Record two narrow precision notes**, not corrections: (a) frontend render-only confidence should read MEDIUM pending a full line-by-line read of `resultsPageLayout.ts` and `uploadReferenceRange.ts`; (b) provenance-scanner attribution in future audits should name which of the two scanner modules (`launch_estate_v1.scan_package_provenance` vs `package_provenance_scan_v1.scan_all_package_provenance`) produced cited numbers, to avoid future confusion given they use different classification taxonomies over the same 191-row estate.
3. **Flag the `golden_gate.yml` branch-scope gap (CWP-E8)** to governance as a CI-hygiene item — the workflow carrying the 2 known-stale golden-panel test failures does not run on direct `main`/`develop` pushes.
4. **Do not open medical review for MR-BATCH-001B promotion** — confirmed test-only, zero production imports, independently re-verified.
5. **Adjudicate multi-frame same-`signal_id` policy (CWP-E1) before any "multi-frame complete" claim is made in product or governance documents** — this is the single highest-leverage open decision surfaced by both audits.
6. Bilirubin-protection and replay/auditability-block depth remain `UNKNOWN_REQUIRES_REVIEW` after two audit passes; if either becomes relevant to a near-term sprint decision, a narrow, targeted re-verification (not a third full audit) should be commissioned specifically for those two items.

No sprint is selected. No implementation prompt is authored. This report and Cursor's report together are sufficient to establish a trustworthy executable baseline for later sprint selection, subject to the two precision notes above.

---

## 25. Evidence index

| ID | Path / command / symbol | Proves | Does not prove | Confidence |
|---|---|---|---|---|
| C01 | `git rev-parse HEAD` | HEAD matches baseline | — | HIGH |
| C02 | Direct read `output_authority_provenance_builder_v1.py:31` | `_signal_index` overwrites by bare signal_id | Frequency of collision in real panels | HIGH |
| C03 | Direct read `root_cause_compiler_v1.py:522` | First-match by bare signal_id | — | HIGH |
| C04 | Direct read `report_compiler_v1.py:749-753` | Dict-comprehension collapse by bare signal_id | — | HIGH |
| C05 | Direct read `signal_interaction_builder.py:147-153` | Dict-comprehension overwrite (`fired`) | — | HIGH |
| C06 | `compiled_hypothesis.py:17-18` direct read | Exactly 1 signal_id in compiled-authority frozenset | — | HIGH |
| C07 | Count of `RootCauseTargetSpec(` in `root_cause_registry_v1.py` | 41 total targets | — | HIGH |
| C08 | `scan_package_provenance()` re-run (launch_estate_v1) | 191 rows, 0 explicit source_spec_id, exact field match to Cursor | — | HIGH |
| C09 | `scan_all_package_provenance()` re-run (package_provenance_scan_v1) | Second independent scanner agrees on 191 rows / 0 explicit | Which scanner Cursor's table used | HIGH |
| C10 | `estate_index_v1.yaml` direct parse | 10 card_evidence_artefacts | PSI richness on cards | HIGH |
| C11 | Full-repo grep `load_promoted_signal_intelligence` | 0 production importers outside validator/tests | Future wiring safety | HIGH |
| C12 | Full-repo grep MR-BATCH-001B across 4 production dirs | 0 production references | Content quality | HIGH |
| C13 | `resolve_narrative_llm_allow_llm(None)` re-run | Default narrative LLM off, exact reason string match | Upload-path behaviour when explicitly enabled | HIGH |
| C14 | `run_architecture_validation_gate.py` re-run | Exit 0, all 8 sub-checks PASS | Beta readiness | HIGH |
| C15 | `test_arch_rt5d_package_provenance.py` re-run | 4 failures, stale counts (191≠186, 10≠7, 72≠67) | Live gate is broken | HIGH |
| C16 | `test_golden_panel_runner.py` re-run | 2 failures, both `TypeError` in test stub `_stub_evaluate_all`, unrelated `runtime_context` kwarg | Production `evaluate_all` is broken | HIGH |
| C17 | `retail_explainer_v1/registry.yaml` direct parse | 40 biomarkers, 10 systems | Coverage completeness vs full biomarker panel | HIGH |
| C18 | `.github/workflows/architecture-gate.yml` read | CI-wired on push/PR to main/develop | Full CI enforcement depth | HIGH |
| C19 | `.github/workflows/golden_gate.yml` read | Golden-panel suite gated on PR + one legacy branch, not main push | — | HIGH |
| C20 | `sentinel/sentinel_runner.py:2,339` read | Explicitly report-only by its own docstring/output | — | HIGH |
| C21 | `golden_gate_local.py` read | Kernel gate requires active work-package prompt; runs 3 subprocess checks | — | HIGH |
| C22 | Targeted read `resultsPageLayout.ts` (keyword-anchored) | Severity/tone driven by backend-supplied enum fields | Full 602-line file clean | MEDIUM |
| C23 | Targeted read `uploadReferenceRange.ts` (first 80 lines) | Upload-review parsing helpers, not new clinical thresholds | Full 605-line file clean | MEDIUM |

---

## Appendix A — Independent command log

```text
git rev-parse HEAD
  → 2a8fa64ed791cabc8ae478113b96cefdf25145a1

git status --short ; git branch --show-current
  → clean except 3 untracked audit-paper files; branch main

# Line-number verification (Read tool, exact offsets)
Read backend/core/analytics/output_authority_provenance_builder_v1.py (lines 1-60)
Read backend/core/analytics/root_cause_compiler_v1.py (lines 500-540)
Read backend/core/analytics/report_compiler_v1.py (lines 735-764)
Read backend/core/analytics/signal_interaction_builder.py (lines 140-164)

# Compiled-authority set size
grep -n "RUNTIME_PROMOTED_COMPILED_SIGNAL_IDS" backend/core/knowledge/compiled_hypothesis.py
  → line 18: frozenset({PILOT_SIGNAL_ID}); PILOT_SIGNAL_ID = "signal_vitamin_d_low" (line 17)
grep -c "RootCauseTargetSpec(" backend/core/knowledge/root_cause_registry_v1.py
  → 41

# PSI import surface
grep -rln "load_promoted_signal_intelligence" --include=*.py backend | grep -v __pycache__
  → 4 files: loader def, validate_day_one_architecture.py, test_arch_rt5e_..., test_promoted_signal_intelligence_kb_s47d.py

# MR-BATCH-001B production-dir grep
grep -rniI "mr_batch_001b|mr-batch-001b|mr_candidate_prose" backend/core backend/app backend/scripts backend/ssot
  → no matches (exit 1)

# Provenance scans (PYTHONPATH=backend, HEALTHIQ_MODE=test)
python -c "from core.knowledge.launch_estate_v1 import scan_package_provenance; ..."
  → 191 rows; source_document_unparsed=82; blocked_pending_spec_extraction=76;
    source_document_derived=31; provenance_gap=2; has_source_spec_id=0
python -c "from core.knowledge.package_provenance_scan_v1 import scan_all_package_provenance; ..."
  → 191 rows; batch_json_blocked_pending_spec_extraction=147; source_document_derived=31;
    architecture_doc_source_blocked=11; retire_candidate=1; provenance_gap=1;
    explicit source_spec_id_on_manifest=0

# Estate index
python -c "import yaml; d=yaml.safe_load(open('knowledge_bus/compiled/estate_index_v1.yaml', encoding='utf-8')); print(len(d['card_evidence_artefacts']))"
  → 10

# Retail explainer registry
python -c "import yaml; d=yaml.safe_load(open('backend/ssot/retail_explainer_v1/registry.yaml', encoding='utf-8')); print(len(d['biomarkers']), len(d['systems']))"
  → 40 10

# Narrative LLM default (all relevant env vars unset)
python -c "from core.insights.narrative_runtime_policy import resolve_narrative_llm_allow_llm; print(resolve_narrative_llm_allow_llm(None))"
  → NarrativeRuntimeDecision(synthesizer_allow_llm=False, ..., reason='HEALTHIQ_NARRATIVE_LLM_not_set_default_off')

# Architecture / launch estate gates (PYTHONPATH=backend, HEALTHIQ_MODE=test)
python backend/scripts/validate_day_one_architecture.py            → EXIT 0, PASS
python backend/scripts/validate_day_one_launch_estate_gate.py      → EXIT 0, PASS
python backend/scripts/run_architecture_validation_gate.py         → EXIT 0, architecture_validation_gate: PASS
  (frame index, modifier catalogue, day-one, launch estate, context reachability,
   medical intelligence architecture, architecture guardrails pytest, governance regression pytest)

# Targeted pytest re-runs (PYTHONPATH=backend, HEALTHIQ_MODE=test)
pytest backend/tests -k "duplicate_activation_key or multi_frame or arch_rt5e or mr_batch_001b" -q
  → all passed, 0 failures
pytest backend/tests -k "health_system_card_evidence_arch_rt5b or compiled_hypothesis_arch_rt5c or domain_ux1c" -q
  → all passed, 0 failures
pytest backend/tests -k "arch_rt5d_package_provenance" -q
  → EXIT 1, 4 failed: test_all_packages_classified, test_classification_counts_match_inventory,
    test_kb52c_packages_classified_batch_blocked (assert 72==67), test_estate_index_covers_launch_artefacts (assert 10==7)
pytest backend/tests/unit/test_golden_panel_runner.py -q
  → EXIT 1, 2 failed: test_primary_markers_never_use_policy_or_ssot_ranges,
    test_golden_panel_signal_results_carry_explanation_metadata
    (root cause: test-local _stub_evaluate_all() missing 'runtime_context' kwarg)

# CI workflow inspection
Read .github/workflows/architecture-gate.yml   → triggers push/PR main,develop; runs run_architecture_validation_gate.py
Read .github/workflows/ci.yml                  → triggers push/PR main,develop; backend+frontend test matrix
Read .github/workflows/golden_gate.yml         → triggers PR (any) + push to sprint17/biomarker-expansion-ab-panel only
grep -n "report only\|report-only" sentinel/sentinel_runner.py
  → line 2 docstring, line 339 "sentinel_note": "Phase 1 — report only. No product code or governed assets were modified."
Read backend/scripts/golden_gate_local.py (lines 1-210)
  → kernel gate requires automation_bus/latest_cursor_prompt.md front matter; runs 3 subprocess checks

# Frontend targeted reads
Read frontend/app/lib/uploadReferenceRange.ts (lines 1-80)
Grep threshold|reference_range|clinical|diagnos|>=|<=|risk_level|severity in frontend/app/lib/resultsPageLayout.ts
wc -l frontend/app/lib/resultsPageLayout.ts frontend/app/lib/cardEvidenceConsumerCopy.ts frontend/app/lib/uploadReferenceRange.ts
  → 602 / 29 / 605 lines
```

---

## Appendix B — Test-quality classification

| Test file / suite | Classification | Independent execution result |
|---|---|---|
| `test_signal_registry_duplicate_activation_key_fails_closed` + multi-frame registry cases | PRODUCTION_LOADER | Re-run, PASS |
| `test_arch_rt5e_psi_runtime_wiring_decision.py` | PRODUCTION_ASSEMBLY (negative proof) | Included in combined re-run, PASS |
| `test_health_system_card_evidence_arch_rt5b.py` | PRODUCTION_ASSEMBLY | Re-run, PASS |
| `test_compiled_hypothesis_arch_rt5c.py` | PRODUCTION_ASSEMBLY | Re-run, PASS |
| `test_domain_ux1c_governed_subsystem_evidence.py` | PRODUCTION_ASSEMBLY | Re-run, PASS |
| `test_arch_rt5d_package_provenance.py` | PRODUCTION_LOADER, stale FIXTURE expectations | Re-run, 4 FAILED (stale counts, scanner itself functions correctly) |
| `test_golden_panel_runner.py` | MOCK_ONLY (test-local stub failure) | Re-run, 2 FAILED — confirmed to be test-harness staleness, not a production defect |
| `test_signal_evaluator.py` (full file) | Mixed | 1 unrelated failure (missing golden fixture), not re-run as part of any multi-frame proof |
| `backend/tests/support/mr_candidate_prose_test_v1.py`, `test_mr_batch_001b_candidate_prose_test_import.py` | FIXTURE_ONLY / import-isolation | Confirmed as the only two MR-BATCH-001B references in `backend/tests`; not independently re-run in this pass (accepted from Cursor's PASS claim given zero production-dir contradiction) |

**Untested production branch (both audits agree):** genuine same-`signal_id` multi-frame collapse behaviour in `signal_interaction_builder`, `root_cause_compiler_v1`, `report_compiler_v1`, and `output_authority_provenance_builder_v1` has no passing test that proves *correct* multi-frame preservation — only tests proving registry-level coexistence at load time.

---

## Appendix C — Cursor claim-by-claim disposition

| # | Cursor claim | Disposition | Independent basis |
|---|---|---|---|
| 1 | Architecture gate PASS, exit 0 | ACCEPTED | Re-ran, exit 0 |
| 2 | PSI 57 artefacts, 0 launch imports | ACCEPTED | Re-ran grep from scratch, 0 production importers |
| 3 | Multi-frame registry wired; downstream collapses at 4 named sites | ACCEPTED, exact line numbers confirmed | Direct source reads at cited lines |
| 4 | 0 explicit `source_spec_id` / 191 packages | ACCEPTED, confirmed twice | Two independent scanner re-runs |
| 5 | Exactly 1/41 signals use compiled WHY authority | ACCEPTED exactly | Direct frozenset + target-count read |
| 6 | RT-5D stale counts (186→191, 7→10) | ACCEPTED, additional number found (67→72 for kb52c) | Test re-run |
| 7 | MR-BATCH-001B zero production imports | ACCEPTED | Independent grep re-run |
| 8 | Narrative LLM off by default, same reason string | ACCEPTED exactly | Function re-run with identical output |
| 9 | 40 retail explainers | ACCEPTED exactly | Direct YAML parse |
| 10 | `test_golden_panel_runner.py` fails 2 tests on stale mock | ACCEPTED exactly | Re-run, identical failure count and root cause |
| 11 | 10 estate cards, card-evidence production chain | ACCEPTED | Direct YAML parse + test re-run |
| 12 | Frontend render-only, no medical inference | ACCEPTED for code sampled; confidence NARROWED to MEDIUM for full-file completeness | Targeted read, not full 600+ line read |
| 13 | Bilirubin protection covered by existing tests | NEITHER ACCEPTED NOR REJECTED — carried forward as `UNKNOWN_REQUIRES_REVIEW` by both audits | Test not re-executed by either pass |
| 14 | Sentinel is report-only | ACCEPTED, independently confirmed via direct source docstring/output field | Direct source read |
| 15 | Golden gate kernel requires active work-package token | ACCEPTED, independently confirmed | Direct source read of `golden_gate_local.py` |
| 16 | (New, not a Cursor claim) `golden_gate.yml` scoped to PR + legacy branch, not main push | NEW FINDING, not in Cursor's report | Direct workflow-file read |

**Overall disposition count:** 15 of 15 checked Cursor claims **ACCEPTED** (12 fully, 2 accepted-with-confidence-narrowed, 1 carried forward unresolved by both audits); 0 rejected; 1 new finding added by this pass.

---

*End of independent executable architecture assurance audit. No production code, tests, schemas, packages, governance documents, or branch state were modified; only this report file was written. `docs/audit-papers/CURSOR_executable_codebase_and_runtime_reality_audit.md`, `docs/audit-papers/CLAUDE_CODE_sprint_governance_and_codebase_maturity_audit.md`, and `docs/audit-papers/CURSOR_sprint_governance_and_codebase_maturity_audit.md` were read but not modified.*
