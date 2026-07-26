# ARCH-CONV-CORRECT-1 — Implementation and Verification Report

**Work ID:** `ARCH-CONV-CORRECT-1`
**Branch:** `feature/arch-conv-correct-1-e2e-authority-layerc`
**Baseline HEAD (kernel start):** `c933d794c9e57c1ee6180d8b943fed009727fd70`
**Final SHA:** recorded in the Automation Bus status at kernel finish (implementation commit on this branch)
**UAT analysis ID:** `e34aaedf-b09f-42f0-8cc8-4653a00b4c10`
**change_type:** RUNTIME
**runtime_change:** BACKEND + FRONTEND

---

## 1. Outcome

The four confirmed `ARCH-CONV-FINAL-AUDIT` defect themes are closed with executable enforcement:

1. **WS1** — the ratified `REJECTED` homocysteine metabolic frame is inactive end to end.
2. **WS2** — the legacy “methylation capacity” / “Methylation pathway pattern” wording is retired from every active runtime surface.
3. **WS3** — MCV frame co-service is governed: the anchor frame cannot co-emit a duplicate causal WHY, and the megaloblastic / non-megaloblastic frames cannot co-serve causally without explicit authority.
4. **WS4** — every Layer C `BOUNDARY_LEAK` in the audit inventory is closed; Layer C now performs presentation and translation only.

### Final package recommendation

# GO

All identified final-audit corrections are closed; `ARCH-CONV-FINAL-AUDIT` can resume.

`GO` here means *the correction package's obligations are met*. It is **not** a programme PASS: a
human UAT re-check of the live results page for the audited analysis is still required, and the
programme decision remains with `ARCH-CONV-FINAL-AUDIT` under human authority.

Controlled-beta readiness: **not assessed, not claimed**.

---

## 2. Files changed

### New runtime authority modules

| Path | Role |
|---|---|
| `backend/core/knowledge/frame_runtime_authority_v1.py` | Canonical answer to “may this frame exist as an active medical result at all”, derived from the ratified WHY authority register |
| `backend/core/knowledge/frame_co_service_v1.py` | Resolves co-service roles for a governed frame family from policy |
| `backend/core/analytics/primary_driver_authority_v1.py` | Projects Layer B's governed ranked lead onto the cluster identity Layer C needs |
| `knowledge_bus/governance/frame_co_service_policy_v1.yaml` | Governed MCV co-service policy (roles, evidence gates, suppression) |

### Modified runtime surfaces

| Path | Change |
|---|---|
| `backend/core/analytics/signal_evaluator.py` | `SignalRegistry._load` refuses to load rejected frames (recorded in `excluded_rejected_frames`); `SignalEvaluator.evaluate_all` re-asserts eligibility on its output |
| `backend/core/analytics/insight_graph_builder.py` | Filters externally supplied `signal_results` and emits `primary_driver_v1` |
| `backend/core/analytics/root_cause_compiler_v1.py` | Applies family co-service resolution: assigns `why_role`, suppresses non-authorised causal siblings, validates anchor content |
| `backend/core/contracts/root_cause_v1.py` | Additive `why_role` on `RootCauseFindingV1` |
| `backend/core/contracts/insight_graph_v1.py` | Additive `primary_driver_v1` on `InsightGraphV1` |
| `knowledge_bus/root_cause/hypotheses/hcy_hypotheses_v1.yaml` | Ratified replacement wording for the elevation-context B12 hypothesis |
| `knowledge_bus/interpretation_display_layer_v1/idl_records_v1.yaml` | Retail label → “One-carbon pathway pattern” |

### Frontend (Layer C)

| Path | Change |
|---|---|
| `frontend/app/(app)/results/page.tsx` | Consumes `primary_driver_v1`; stops inventing `0.85` confidence; stops calling FE pattern prose |
| `frontend/app/lib/resultsPageLayout.ts` | `selectGovernedPrimaryDriver` replaces FE driver arbitration; FE severity/confidence ranking helpers removed |
| `frontend/app/components/biomarkers/BiomarkerDials.tsx` | Dial colour from backend `status` only; unknown → neutral |
| `frontend/app/components/clusters/ClusterSummary.tsx` | Colour from backend severity band; confidence rendered only when supplied |
| `frontend/app/components/insights/InsightsPanel.tsx` | Backend emission order preserved |
| `frontend/app/components/results/LayerCInsightSection.tsx` | Fixed display order + governed copy module |
| `frontend/app/components/results/SystemUnderstandingSection.tsx` | Governed copy module |
| `frontend/app/components/actions/ActionHubCardList.tsx` | FE evidence-strength binning replaced with action provenance (`Source:`) |
| `frontend/app/lib/layerCInsightCopy.ts`, `frontend/app/lib/systemUnderstandingCopy.ts` | New governed static product copy |
| `frontend/app/components/clusters/ClusterInsightPanel.tsx` | **Deleted** (FE-authored clinical recommendations) |
| `frontend/app/lib/biomarkerPatternRelevance.ts` | **Deleted** (FE-authored causal-ish relevance prose) |
| `frontend/app/types/analysis.ts`, `frontend/app/components/clusters/index.ts` | DTO type + export cleanup |

### Verification assets

| Path | Role |
|---|---|
| `backend/scripts/validate_arch_conv_correct1_gate.py` | Correction gate covering WS1–WS4 |
| `backend/tests/regression/test_arch_conv_correct1_programme_closure.py` | 16 closure regressions |
| `backend/scripts/replay_arch_conv_correct1_uat_case.py` | Deterministic replay of the audited case (`--baseline` reproduces the pre-correction state) |
| `backend/scripts/rerun_arch_conv_final_13_scenarios.py` | Re-runs the 13 final-audit Layer B scenarios |
| `frontend/tests/components/LayerCMedicalBoundary.test.tsx` | Layer C boundary render proofs |
| `backend/tests/unit/test_signal_evaluator.py`, `backend/tests/unit/test_narrative_report_compiler_v1.py`, `backend/tests/fixtures/panels/phenotypes/phenotype_expectations_v1.yaml` | Existing expectations that asserted the retired behaviour, updated to the governed behaviour |

---

## 3. Per-defect before/after evidence

Source of evidence: `backend/scripts/replay_arch_conv_correct1_uat_case.py` on the audited panel,
run in both corrected and `--baseline` modes.

| # | Defect (final audit) | Before | After |
|---|---|---|---|
| 1 | Rejected frame fires | `signal_homocysteine_high::inv_homocysteine_high_metabolic` in fired set (8 rows) | Absent (7 rows); recorded in `SignalRegistry.excluded_rejected_frames` as `REJECTED_NOT_RUNTIME_ELIGIBLE` |
| 2 | Rejected frame ranked | Present in `report_v1.top_findings` at position `#3` | Absent from all 7 `top_findings` rows |
| 3 | Rejected frame drives interventions | 2 interventions cite the rejected `activation_key` | 0 citations |
| 4 | Rejected frame contributes interpretation text | “Reflects methylation capacity and B-vitamin status.” reachable via the signal card | Row never reaches the payload, so no interpretation, summary or provenance text is emitted |
| 5 | Legacy wording active | Clinician summary “reduced B12-related methylation capacity”; consumer label “Methylation pathway pattern” | Ratified B-vitamin availability wording; “One-carbon pathway pattern” |
| 6 | MCV frames co-emit | Anchor + megaloblastic + non-megaloblastic all serving causal WHY | Anchor `why_role=morphology_context`; specific frames suppressed unless their ratified evidence gate is met |
| 7 | Layer C boundary leaks | 12 inventory rows, incl. FE driver arbitration, invented confidence, dial colour invention, FE prose | 12/12 closed |

Detail with payload extracts: `docs/architecture/ARCH-CONV-CORRECT-1_end_to_end_leakage_correction_report.md`.

---

## 4. Rejected-frame lifecycle trace

| Lifecycle stage | Enforcement | Behaviour for `…::inv_homocysteine_high_metabolic` |
|---|---|---|
| Package on disk | none (intentional) | Package remains, still validates — history is not rewritten |
| Registry load | `SignalRegistry._load` → `frame_runtime_exclusion_reason` | Not loaded; exclusion recorded |
| Signal evaluation | `SignalEvaluator.evaluate_all` → `filter_runtime_eligible_rows` | Cannot be emitted even by an injected/stub registry |
| Insight graph assembly | `build_insight_graph_v1` → `filter_runtime_eligible_rows` | Cannot enter via externally supplied `signal_results` |
| WHY compilation | PKG3 authority (pre-existing) + absence of the row | No hypothesis |
| Ranking / `top_findings` | absent input | Cannot rank |
| Interventions | absent activation key | Cannot be cited |
| Narrative / IDL / clinician report | absent input | No interpretation or summary text |
| Persisted replay | absent input | Replays inert |

Fail-closed: an unreadable authority register raises rather than admitting a frame.

Design rationale: `docs/architecture/ARCH-CONV-CORRECT-1_rejected_frame_inactivation_design.md`.

---

## 5. Legacy fingerprint results

Scanned phrases: `methylation capacity`, `Methylation pathway pattern`, `B12-related methylation`.

| Surface | Result |
|---|---|
| Runtime knowledge (`knowledge_bus/**` active YAML, uncommented) | 0 hits |
| Compiled WHY artefacts | 0 hits |
| Backend runtime code | 0 hits |
| Frontend code and copy modules | 0 hits |
| Live replay payload (signals, findings, IDL, narrative, clinician report) | 0 hits |

Remaining references are **historical only** and deliberately preserved: the audit papers that
recorded the defect, the ratified medical review documents, the rejected KB-S24 package on disk
(unreachable at runtime by WS1), and this correction pack. The gate excludes exactly those paths
and fails on anything else.

Differentiation preserved: the B-vitamin frame
(`signal_homocysteine_high::inv_homocysteine_high_b_vitamin_related_methylation_impairment`) and the
renal frame (`…::inv_homocysteine_high_renal_clearance_reduction`) remain distinct, and the
elevation-context legacy family still reads B12 availability and renal clearance as separate
contributors.

---

## 6. MCV co-service matrix

Policy: `knowledge_bus/governance/frame_co_service_policy_v1.yaml`. Family `mcv_high`.

| Frame | Governed role |
|---|---|
| `signal_mcv_high::inv_mcv_high_macrocytosis` (anchor) | `morphology_context` — never a causal WHY |
| `…::inv_mcv_high_megaloblastic` | causal only when hematinic evidence supports it |
| `…::inv_mcv_high_non_megaloblastic` | causal only when hepatic evidence (GGT/ALT) supports it |

| Scenario | Evidence | Result |
|---|---|---|
| Anchor alone | — | Anchor serves morphology context only |
| High MCV + low B12/folate | hematinics support | Megaloblastic causal; non-megaloblastic suppressed; anchor context |
| High MCV + raised GGT/ALT | hepatic support | Non-megaloblastic causal; megaloblastic suppressed; anchor context |
| Both evidence sets present | ambiguous | No combined causal claim invented; fail-closed to the authorised single lead plus context |
| No supporting evidence (the audited UAT panel) | none | Both specific frames suppressed; anchor context only |

Design rationale and the ratified basis for each gate: `docs/architecture/ARCH-CONV-CORRECT-1_mcv_co_service_design.md`.

---

## 7. Layer C boundary closure matrix

12/12 inventory rows closed; matrix with the governing Layer B field and the missing-field
behaviour for each row is in
`docs/architecture/ARCH-CONV-CORRECT-1_layer_c_boundary_closure_report.md`, and the audit
inventory has been annotated with the closure status.

Missing governed fields fail safely: absent `primary_driver_v1` renders no hero driver rather than
an FE-chosen one; absent `confidence` omits the row rather than substituting a number; unknown
`status` renders neutral rather than a guessed colour; absent severity renders neutral.

---

## 8. Live analysis replay evidence

```text
cd backend
python scripts/replay_arch_conv_correct1_uat_case.py            # corrected  → exit 0
python scripts/replay_arch_conv_correct1_uat_case.py --baseline  # baseline   → reproduces all 6 leaks
```

Corrected run: rejected frame absent from fired signals, `top_findings` and intervention
citations; no retired wording anywhere in the payload; MCV anchor `morphology_context` with both
specific frames suppressed; `primary_driver_v1` present and consistent with `top_findings[0]`.

Baseline run reproduces the audited pre-correction state, which is what makes the corrected run
evidence rather than assertion.

---

## 9. Automated scenario results

| Suite | Command | Result |
|---|---|---|
| Final-audit 13 scenarios | `python scripts/rerun_arch_conv_final_13_scenarios.py` | 13/13 PASS, exit 0 |
| Correction regressions | `python -m pytest tests/regression/test_arch_conv_correct1_programme_closure.py -q` | 16 passed, exit 0 |
| Layer C boundary + hero alignment (FE) | `npm test -- tests/components/LayerCMedicalBoundary.test.tsx tests/lib/resultsHeroAlignment.test.ts` | 2 suites, 12 tests passed (4 boundary), exit 0 |

---

## 10. Test commands and exit codes

| Command | Exit |
|---|---|
| `python scripts/validate_arch_conv_correct1_gate.py` | 0 (`arch_conv_correct1_gate: PASS`) |
| `python scripts/run_architecture_validation_gate.py` (wraps identity-provenance, provenance/reachability, compiled WHY authority, frame identity, Layer B integrity, medical-intelligence architecture, guardrail + governance pytest) | 0 (`architecture_validation_gate: PASS`) |
| `python scripts/validate_compiled_why_authority_gate.py` | 0 (`frames=10 compiled_active=9 rejected=1`) |
| `python scripts/validate_launch_path_frame_identity_gate.py` | 0 (`families=8 frames=21`) |
| `python scripts/validate_layer_b_integrity_gate.py` | 0 |
| `python -m pytest tests/regression/test_arch_conv_correct1_programme_closure.py -q` | 0 |
| `python -m pytest tests/unit/test_phenotype_suite_v1.py tests/unit/test_narrative_report_compiler_v1.py -q` | 0 |
| `python scripts/rerun_arch_conv_final_13_scenarios.py` | 0 |
| `python scripts/replay_arch_conv_correct1_uat_case.py` | 0 |

### Full backend suite comparison

The backend suite was run on this branch and, for the same scopes, on a detached worktree at the
baseline SHA, so that pre-existing failures could be separated from regressions.

| Run | Failures |
|---|---|
| Branch, `tests/unit` + `tests/regression`, before triage | 46 — of which **3 new**; the 14 that failed only at baseline were caused by the worktree lacking `backend/.env` |
| Baseline, same scope | 57 (= the 43 shared + those 14 env artefacts) |
| Branch, full `tests` tree, after triage | 61 |
| Baseline, the remaining scopes (`tests/enforcement`, `tests/governance`, `tests/integration`, root-level alias tests) with `.env` copied in | 18 — byte-identical set to the branch |

**Every one of the 61 remaining failures is present at the baseline SHA** (43 + 18). Their causes are
unrelated to this package: Gemini/LLM insight generation disabled in this environment, an SSOT
`ldl` alias collision, a stale governance frame index relative to the committed frame-tree doc, and
a scoring-policy import enforcement expectation that main does not satisfy.

The three branch-only failures were all expectations that encoded the retired behaviour, and were
updated to assert the governed behaviour instead:

| Test | Why it failed | Resolution |
|---|---|---|
| `test_kbs24_signals_trigger_suboptimal_then_escalate[signal_homocysteine_high]` | Asserted the rejected KB-S24 frame must fire | Removed from the KB-S24 fixture; replaced with `test_kbs24_rejected_homocysteine_metabolic_frame_is_not_runtime_eligible`, which asserts registry exclusion and evaluator exclusion |
| `test_n9b_retail_summary_and_body_overview_with_published_idl` | Asserted the retail summary contains “methylation” | Asserts “One-carbon pathway pattern” and the absence of “methylation” |
| `test_phenotype_suite_v1_regression_harness` | Phenotype expectation listed `signal_homocysteine_high` as `must_fire` | Expectation updated; the phenotype still requires the elevation-context and MCV signals |

No pre-existing failure was hidden, silenced or “fixed while testing”.

---

## 11. Validation-gate evidence

Package 1–3 protections re-verified intact after the change. The umbrella
`run_architecture_validation_gate.py` — which runs the identity-provenance,
provenance/reachability, compiled WHY authority, frame identity, Layer B integrity,
active-signal-context reachability and medical-intelligence architecture gates plus the
architecture-guardrail and governance-regression pytest suites — exits 0
(`architecture_validation_gate: PASS`). WS1 tightens rather than weakens those controls: it
consumes the ratified register and adds a refusal, and it introduces no new bypass or override flag.

---

## 12. Acceptance criteria

| Criterion | Status |
|---|---|
| Rejected homocysteine metabolic frame inactive end to end | PASS |
| Rejected frame cannot appear in top findings | PASS |
| Rejected frame cannot contribute to interventions | PASS |
| Rejected frame cannot contribute interpretation or summary text | PASS |
| No active “methylation capacity” legacy wording remains | PASS |
| B-vitamin and renal homocysteine frames remain differentiated | PASS |
| MCV anchor cannot co-emit duplicate causal WHY | PASS |
| Megaloblastic / non-megaloblastic do not co-serve without authority | PASS |
| Every final-audit Layer C `BOUNDARY_LEAK` closed | PASS (12/12) |
| No safety-material `UNRESOLVED` Layer C item remains | PASS |
| Layer C performs presentation/translation only | PASS |
| Missing governed medical fields fail safely | PASS |
| Live analysis `e34aaedf-…` passes corrected leakage checks | PASS (deterministic replay) |
| All 13 original end-to-end scenarios pass | PASS |
| New focused correction scenarios pass | PASS (16 backend, 4 frontend) |
| Package 1–3 protections intact | PASS |
| No unrelated medical or architecture scope entered | PASS |
| No controlled-beta readiness claim made | PASS |

---

## 13. STOP-condition assessment

| # | Condition | Triggered |
|---|---|---|
| 1 | Rejected-frame inactivation needs approved activation rules changed | No — activation rules untouched; the frame is refused at load |
| 2 | Legacy wording cannot be removed without reopening ratified content | No — replacement wording sourced from the ratified pack |
| 3 | MCV co-service requires new medical policy | No — policy encodes the ratified frame decisions; no new medical claim |
| 4 | Layer C closure requires unrelated redesign | No — changes confined to the results surface and its copy |
| 5 | Scope grew >25% without reauthorisation | No — all four workstreams were in the authorised package |
| 6 | >1 unplanned mandatory follow-on package | No — zero mandatory follow-ons; the remaining items are optional |
| 7 | Unexplained clinical drift in corrected live output | No — every payload delta traces to a listed defect |
| 8 | Package 1–3 safety gate regressed | No — all exit 0 |
| 9 | Correction would weaken provenance/identity/authority controls | No — WS1 strengthens them |
| 10 | Substantive correction impossible in this package | No — completed |

No STOP condition triggered.

---

## 14. Unresolved limitations

1. **Human UAT outstanding.** Post-correction evidence is deterministic replay plus component
   render tests. A human re-check of the live page for `e34aaedf-…` is required before programme PASS.
2. **MCV evidence gates are enforced at WHY co-service, not at activation.** All three MCV frames
   still activate on lab range; only their WHY service is governed. Activation-level gating would
   change approved activation rules and is therefore out of scope here.
3. **The homocysteine elevation-context family remains on the legacy WHY estate.** WS2 corrected its
   wording; migrating it to compiled authority is separate, unauthorised work.
4. **Pre-existing backend suite failures remain** (61, every one reproduced at the baseline SHA) and
   are unrelated to this package.
5. **`frontend/tests/components/BiomarkerDials.test.tsx` has a pre-existing fixture defect** in its
   expand-affordance assertion — it fails identically at the baseline SHA (1 failed, 9 passed);
   not caused by and not fixed in this package.
6. **No controlled-beta readiness claim** is made or implied.

---

## 15. Remaining obligations outside this package

- Resume `ARCH-CONV-FINAL-AUDIT` for the programme decision, after human UAT.
- Optional, separately authorised: MCV activation-level evidence gating; legacy hcy family migration;
  estate-wide WHY migration beyond the 5/10 pilot; controlled-beta readiness assessment.

Do not merge without explicit human authority.
