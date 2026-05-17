# LC-S11A — Trust Blocker Correction Notes

**Work ID:** LC-S11A  
**Branch:** `launch-core/lc-s11a-trust-blocker-correction`  
**Date:** 2026-05-17  
**Role:** healthiq-core-engine (Cursor implementation)

---

## 1. Preflight (governed)

| Check | Result |
| ----- | ------ |
| Branch | `launch-core/lc-s11a-trust-blocker-correction` (created from `main`) |
| Kernel start | `run_work_package.py start` → `work_package_active.json` work_id=LC-S11A |
| Stash | `stash@{0}` on `feature/questionnaire-visual-redesign` — **retained, not touched** (pre-existing, unrelated) |
| Porcelain at start | Clean after committing audit evidence |

---

## 2. Defect inventory

| Defect | Current evidence | Authority source | Proposed fix | Tests |
| ------ | ---------------- | ---------------- | ------------ | ----- |
| 1 Legacy `insights[]` placeholders | Mock InsightGraph path emitted “summarise structured signals” rows | `backend/core/insights/synthesis.py` | Return empty `insights` for InsightGraph mock path | `test_lc_s11a_no_legacy_insights_placeholder_in_dto` |
| 2 Blood sugar unsupported narrative | `met_contributor_primary` fell back to IR IDL subtitle with no active signals | `backend/core/analytics/domain_narrative_wave1.py` | Honest insufficient-evidence copy when `active_sids` empty; guard IR IDL by `severity_state` | `test_lc_s11a_blood_sugar_*`, `test_lc_s11a_met_contributor_primary_*` |
| 3 ApoA1 directionality | `signal_apoa1_cardio_risk` fired on elevated ApoA1 | `knowledge_bus/.../signal_library.yaml` + `signal_evaluator.py` | `enable_upper_bound: false` (low-only signal) | `test_lc_s11a_elevated_apoa1_*`, `test_lc_s11a_apoa1_evaluator_*` |
| 4 Low ALT false alarm | ALT 7 &lt; min 10 scored ~5/100 critical | `backend/core/scoring/rules.py` | Cap below-range ALT at mild HAS position 0.05 | `test_lc_s11a_low_alt_*`, `test_lc_s11a_high_alt_*` |
| Bonus internal string leak | `deferred_kb_content` in consumer `raw_evidence_refs` | `domain_score_assembler.py` cv_block | Removed key from consumer evidence dict | `test_lc_s11a_no_internal_sprint_strings_*` |

---

## 3. Files changed

- `backend/core/insights/synthesis.py`
- `backend/core/analytics/domain_narrative_wave1.py`
- `backend/core/analytics/domain_score_assembler.py`
- `backend/core/scoring/rules.py`
- `knowledge_bus/packages/pkg_kb45_apoa1_low_cardio_risk/signal_library.yaml`
- `backend/tests/regression/test_lc_s11a_trust_blocker_correction.py` (new)
- `sentinel/packs/lc_s10b_launch_core_protection_v1.json`
- `docs/audit-papers/LC-S11_forensic_human_uat_audit.md` (evidence, pre-existing commit)
- `docs/audit-papers/LC-S11-results-page-full.png` (evidence)

---

## 4. Before / after (AB panel fixture)

| Area | Before | After |
| ---- | ------ | ----- |
| `insights[]` | Placeholder category rows | Empty list (validator may warn; no consumer placeholder text) |
| Blood sugar contributor | “early impaired sugar and lipid handling” | Honest HbA1c in-range + missing glucose/insulin wording |
| ApoA1 signal | `signal_apoa1_cardio_risk` suboptimal when elevated | Not active; excluded from `wave1_aligned_drivers` |
| Liver domain (ALT 7) | ~5/100, review band | Non-critical score, not review-led |
| Consumer JSON | `deferred_kb_content` sprint slug | Removed from `raw_evidence_refs` |

---

## 5. Validation commands (recorded)

```text
pytest backend/tests/regression/test_lc_s11a_trust_blocker_correction.py -q  → 11 passed
pytest backend/tests/regression/test_lc_s10b_launch_core_protection.py -q  → passed
pytest backend/tests/regression/test_lc_s8f_phase_b_true_conversions.py -q → passed
pytest backend/tests/regression/test_lc_s8g_uploaded_unit_display_fidelity.py -q → passed
pytest backend/tests/regression/test_lc_s8d_unit_governance_sentinel.py -q → passed
pytest backend/tests/unit/test_scoring_rules.py -q → passed
```

**Note:** `test_lc_s5_proving_checks.py::test_check2_alcohol_bridge_language_when_moderate_threshold_met` failed in this environment due to pre-existing urate unit Unicode mismatch (Greek μ vs µ) in `ab_full_panel_with_ranges.json` — not introduced by LC-S11A. LC-S11A regression harness harmonises units in-test only.

---

## 6. Sentinel / guardrail

Added to `sentinel/packs/lc_s10b_launch_core_protection_v1.json`:

- `legacy_insights_placeholder_leakage`
- `domain_narrative_without_active_signal`
- `apoa1_directionality_misclassification`
- `low_alt_false_alarm`
- `consumer_payload_internal_sprint_string_leakage`

---

## 7. UAT replay

AB fixture orchestrator replay confirms acceptance criteria on bounded panel. Live analysis `c440dfa2-12a1-4e29-95a5-ee07a2397c59` was not re-run in this session; replay requires backend + stored panel or saved JSON.

---

## 8. Residual risks

- Empty InsightGraph mock payload triggers validator_v2 `too_short` warnings per category (insights discarded). Acceptable for launch-core (no placeholder leakage); a future sprint may add a governed empty-result schema.
- ALT below-range cap is **ALT-specific** in lab-range scoring; other enzymes unchanged by design.
- ApoB/ApoA1 ratio override rules unchanged; low ApoA1 + high ratio still escalates per governed overrides.

---

## 9. Recommendation

**Ready for Claude audit and human review** on branch `launch-core/lc-s11a-trust-blocker-correction`. Cursor does not self-certify clinical correctness, merge readiness, or launch approval.
