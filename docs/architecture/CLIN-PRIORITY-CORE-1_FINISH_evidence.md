# CLIN-PRIORITY-CORE-1 — FINISH Evidence

**work_id:** `CLIN-PRIORITY-CORE-1`  
**branch:** `feature/clin-priority-core-1`  
**Starting FINISH HEAD:** `d3822e64f00d23c9fa14ec0118592a5b7546b222`  
**risk_level:** HIGH / MIXED  
**execution_model:** TWO_PHASE_START_FINISH  

## Verdict target

`FINISH_COMPLETE_READY_FOR_INDEPENDENT_AUDIT`

## Scope completed

### Checkpoint 4 — governed longitudinal

| Metric | Value |
|---|---|
| `GOVERNED_LONGITUDINAL_RULE_TOTAL` | **6** |
| `GOVERNED_LONGITUDINAL_RULE_PASSED` | **6** |
| `GOVERNED_LONGITUDINAL_RULE_COVERAGE` | **6/6** |

Rules:

1. RE-T1 AKI — `RE-AS-3`
2. RE-S-2 CKD chronicity — `RE-AS-5`
3. HEP-T1 statin enzyme doubling — `LONG-HEP-T1`
4. HAEM-T5 cytopenia chronicity windows — `LONG-HAEM-T5`
5. THY-T1 two-occasion confirmation — `LONG-THY-T1`
6. CN-T2/CN-T3 HbA1c spacing — `LONG-CN-T2-T3`

Implementation: `backend/core/analytics/longitudinal_rules.py` + annotations in `concern_constructor.py`.  
No invented thresholds; no tier promotion; no medication-cessation advice.

### Checkpoint 5 — frontend single authority

- `ClinicalConcernPrioritySection` renders server `meta.insight_graph.clinical_concern_set` (render-only).
- `technical_tiebreak_lead` demoted whenever concern set authority is present:
  - no competing ranked finding as clinical lead;
  - WhyThisLeadWon close-call framing suppressed;
  - InsightPanel / body-overview tie riders suppressed;
  - optional technical ordering note only under advanced detail.

### START invariants preserved

| Metric | Value |
|---|---|
| `SIGNAL_ACTIVATION_BASELINE_TOTAL` | **183** |
| `SIGNAL_ACTIVATION_PRESERVED_TOTAL` | **183** |
| `SIGNALS_INTENTIONALLY_RETIRED` | **0** |
| Scenario harness | **passed: 110, failed: 0** (109 unique) |
| FIB-4 | Internal calc unchanged; not finding authority; `fib_4_computed/displayed` remain false on concern set |

Corrected outcomes retained: `XD-AS-1`, `RE-AS-12`, `XD-AS-7`; accepted arithmetic: `XD-AS-15`, `XD-AS-17`, `XD-AS-25`.

## Test commands and results

```text
PYTHONPATH=backend python backend/tools/run_clinical_priority_scenarios.py
→ passed: 110, failed: 0

PYTHONPATH=backend python -m pytest \
  backend/tests/unit/test_clin_priority_longitudinal_rules.py \
  backend/tests/unit/test_clin_priority_cross_domain_corrections.py \
  backend/tests/unit/test_clinical_finding_models.py \
  backend/tests/unit/test_clinical_priority_scenario_runner.py -q
→ 21 passed

SignalRegistry().get_all_signals() → 183

frontend: jest clinicalConcernAuthority + ClinicalConcernPriority + ClinicianReportRenderer
→ 11 passed

frontend: tsc --noEmit → pass
frontend: eslint (changed files) → pass
frontend: npm run build → Compiled successfully (Next also warned on root .eslintrc next/core-web-vitals resolve; build completed)
```

### Backend unit suite classification

Full `backend/tests/unit` run completed with pre-existing failures unrelated to this FINISH delta (golden insights/LLM mocks, scoring engine panels, SSOT/PSI estate counts, interaction_summary snapshot field drift, clinician VR fixture parity).  

**Newly introduced unexplained failures attributable to CLIN-PRIORITY FINISH: none.**  
Clinical-priority, longitudinal, and scenario harness suites are green.

## Commits (FINISH span)

1. `584e3b9` — `feat(clin-priority): implement governed longitudinal rules`
2. `9778c74` — `feat(clin-priority): integrate concern set and demote technical tiebreak`
3. (this docs commit)

## Evidence paths

- `docs/architecture/CLIN-PRIORITY-CORE-1_FINISH_evidence.md` (this file)
- `docs/architecture/CLIN-PRIORITY-CORE-1_implementation_and_verification_report.md`
- `docs/architecture/CLIN-PRIORITY-CORE-1_START_evidence.md` (updated)
- Build Deliverables Register entry appended

## Release carry-forwards

- Final consumer serious-result wording copy (structured state only where ungoverned).
- Full retirement of `primary_concern_mode` field from clinician_report schema (demoted in UI; field remains for compatibility).
- Questionnaire / pregnancy context gaps (pre-existing CF register).
- Quarantines R2/R3 (CV-risk %, FIB-4 consumer finding) unchanged.

## Confirmations

- No merge performed by this phase prior to independent audit.
- No Knowledge Bus promotion / signal activation changes.
- Automation Bus `finish` run only after this evidence commit (see gate artefacts).
