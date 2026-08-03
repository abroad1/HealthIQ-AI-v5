# HealthIQ Upload Questionnaire Context Audit v0.1

**Type:** Read-only repository audit. No code, tests, schemas, configuration, registers, or data were changed.
**Date:** 2026-08-03

Legend: `DOCUMENTED CONTRACT` (what a governing artefact states should happen) · `REPOSITORY-VERIFIED CURRENT STATE` (read directly from code/config this session) · `GAP` (difference between the two) · `RECOMMENDED REMEDIATION` (structural suggestion only, not implemented).

---

## 1. Exact governing files and fields

| Layer | File | Relevant field(s) |
|---|---|---|
| SSOT questionnaire schema | `backend/ssot/questionnaire.json` | `biological_sex` (present); **no pregnancy field of any kind** |
| API request model | `backend/app/routes/analysis.py` | `AnalysisStartRequest.questionnaire_data: Optional[Dict[str, Any]]` |
| Context assembly | `backend/core/context/context_factory.py` | `ContextFactory.create_analysis_context`, `_create_user_context`, `_parse_sex` |
| Runtime context contract | `backend/core/models/context.py` | `AnalysisContext.questionnaire_responses: Optional[Dict[str, Any]]` |
| Runtime clinical-context mapping | `backend/core/analytics/runtime_context_evaluator.py` | `build_runtime_context_snapshot`, `pregnancy_status` handling (lines 320-342) |
| Signal-gate governance policy | `knowledge_bus/governance/active_signal_context_gate_reachability_policy_v1.yaml` | pregnancy-gate allowed-values policy |
| Signal-gate validator (architecture gate) | `backend/scripts/validate_active_signal_context_gate_reachability.py` | `_validate_pregnancy_gate`, `_PREGNANCY_SAFE` (lines 34-35, 128-150) |
| Frontend questionnaire renderer | `frontend/app/components/forms/QuestionnaireForm.tsx` | generic `question.required` handling |
| Persistence | `backend/core/models/database.py:118` | `Analysis.questionnaire_data = Column(JSON, nullable=True)` |
| Prior carry-forward record | `docs/sprints/launch_core_carry_forward_register.md:83` | `CF-BETA-READINESS-1` |

---

## 2. Current question wording and answer values

**Sex — REPOSITORY-VERIFIED CURRENT STATE**, `backend/ssot/questionnaire.json:25-37`:
```
id: biological_sex
question: "Biological Sex"
type: dropdown
options: ["Male", "Female", "Intersex"]
required: true
importance: mandatory
```

**Pregnancy — REPOSITORY-VERIFIED CURRENT STATE:** **No such question exists anywhere in the SSOT questionnaire.** No `not_pregnant` / `pregnant` / `may_be_pregnant` values, no `pregnancy_status` question entry, in `questionnaire.json` at all. This is not a wording or option-set mismatch — the question is entirely absent.

---

## 3. Required/optional status

| Field | SSOT status | Frontend enforcement | Backend enforcement |
|---|---|---|---|
| `biological_sex` | `required: true`, `importance: mandatory` | Enforced generically (§4) | **Not enforced** (§5, GAP) |
| Pregnancy status | Does not exist | N/A — nothing to render | N/A — nothing to validate |

---

## 4. Frontend validation

**REPOSITORY-VERIFIED CURRENT STATE:** `QuestionnaireForm.tsx` reads each question's `required`/`importance` field from the SSOT-derived schema generically and renders inline "This field is required" hints and per-field error messages (lines 260-277, 428-430). This means `biological_sex`, being `required: true` in the schema, receives this treatment automatically in the normal UI flow.

There is no pregnancy-specific frontend code anywhere — `grep -rl "pregnan" frontend/app --include=*.ts --include=*.tsx` returned **zero results**. Nothing in the frontend collects, displays, or validates pregnancy status.

---

## 5. Backend validation

**REPOSITORY-VERIFIED CURRENT STATE — this is the most significant finding of the audit:**

- `AnalysisStartRequest.questionnaire_data: Optional[Dict[str, Any]] = Field(default=None, ...)` (`backend/app/routes/analysis.py:27-30`) — the entire questionnaire payload is optional at the API boundary. A request can omit it, or send `null`, and the Pydantic model still validates successfully.
- `ContextFactory.create_analysis_context` (`context_factory.py:123-135`) only raises if the payload is **missing `biomarkers` or `user` sections**. It never checks for a `questionnaire`/`questionnaire_data` section at all.
- `ContextFactory.create_analysis_context` accepts an optional `validate_requirements: Optional[Dict[str, Any]] = None` parameter that, if supplied, would run `analysis_context.validate_analysis_requirements(validate_requirements)` and raise on failure (lines 197-202) — **but `grep -rn "validate_requirements" backend/app/routes/analysis.py backend/core/pipeline/orchestrator.py` returns zero matches.** This hook is never called anywhere in the real request path. It is dead capability, not active enforcement.
- `_create_user_context` (`context_factory.py:298-304`):
  ```python
  sex_raw = raw_user_data.get('sex')
  if sex_raw is None:
      sex_raw = raw_user_data.get('gender', 'other')
  sex = self._parse_sex(sex_raw)
  ```
  and `_parse_sex` (`context_factory.py:414-438`):
  ```python
  if value is None:
      return Sex.OTHER
  ```
  **If `sex` is genuinely absent from the request, the system silently defaults to `Sex.OTHER` rather than raising.** This is a confirmed silent default, not an inference from other data — it happens with zero information about the user's actual sex.
- Persistence has no constraint either: `Analysis.questionnaire_data = Column(JSON, nullable=True)` (`database.py:118`) — the column accepts `NULL`.

**Net effect:** an analysis can currently be started and completed with **zero** questionnaire data submitted at all — mandatory or otherwise — provided the request contains a `biomarkers` section and a minimal `user` section. Even the `user` section's `sex` field silently defaults rather than blocking.

---

## 6. Runtime context mapping

**REPOSITORY-VERIFIED CURRENT STATE**, `runtime_context_evaluator.py:270-342`:

- `biological_sex`, if present in `questionnaire_responses`, is mapped into `snapshot["demographic"]["sex"]` (lines 294-296) — **only if present and non-empty; no default is injected at this layer.** (Note: this is a *separate* code path from `ContextFactory`'s `UserContext.sex`, which is derived earlier from the request's `user` block, not from `questionnaire_responses`. There are two independent sex-determination points in the pipeline, and only the earlier one — `ContextFactory` — has the silent-default behaviour documented in §5.)
- `pregnancy_status`, if present in either `questionnaire_responses` or `lifestyle_factors`, is mapped into `snapshot["clinical_context"]["pregnancy_status"]` as a **disclosure state** (`answered_yes` / `answered_no` / `not_answered` / `unknown` / `not_applicable`), via `_field_answered` / `_disclosure_state_from_value` (lines 320-336). When absent, it is explicitly set to `DISCLOSURE_NOT_ANSWERED` (lines 337-342) — this part is honest; it does not silently mark the state as "no" or "not pregnant," it correctly records "not answered."
- **However**, this disclosure state then feeds into per-signal `runtime_context_requirements` gates (`knowledge_bus/packages/*/signal_library.yaml`), and the **governance policy validated by `validate_active_signal_context_gate_reachability.py`** requires those gates to treat `not_answered` as an **allowed, passing** value:
  ```python
  _PREGNANCY_SAFE = frozenset({"answered_no", "not_answered", "not_applicable"})
  ```
  and explicitly **forbids** `answered_yes` from ever being an allowed value for a pregnancy gate (`_validate_pregnancy_gate`, lines 140-144):
  ```python
  if "answered_yes" in allowed_set:
      errors.append(f"... pregnancy_status must not allow answered_yes (pregnancy-specific logic unavailable)")
  ```

This is a **governed, deliberate, architecture-gate-enforced policy**, not an oversight: every pregnancy-gated signal in the estate is *required by this validator* to proceed with standard rules whenever pregnancy status is unanswered, and is *forbidden* from having any path that responds to a "yes" answer at all — because, per the code's own comment, no pregnancy-specific interpretation logic exists in the product today.

**Prior history — `docs/sprints/launch_core_carry_forward_register.md:83`, `CF-BETA-READINESS-1`:** this exact gap ("questionnaire has no pregnancy_status field") was already found once before, by a work package (`DHEA-S-HIGH-ACTIVATION-1`), and the recorded resolution was `BETA-READINESS-SPRINT-2`, which **widened the gates to accept `not_answered`/`not_applicable`** rather than adding the missing question. The validator was then "promoted to architecture gate" — meaning this "fail open on unanswered pregnancy" behaviour is now actively protected against regression.

---

## 7. Persistence and provenance

**REPOSITORY-VERIFIED CURRENT STATE:**
- `analyses.questionnaire_data` is a nullable JSON column (`database.py:118`) — whatever raw dict is submitted is persisted as-is; no schema enforcement at the DB layer.
- Cross-checked against a real persisted analysis this session's prior UAT trace work (`analysis_id b07848c6-c22d-4565-a7c0-f4e2ea620614`): the persisted `questionnaire_data` keys were exactly `['date_of_birth', 'biological_sex', 'height', 'weight', 'waist_circumference', 'long_term_medications', 'alcohol_drinks_weekly', 'tobacco_use', 'sleep_hours_nightly', '_questionnaire_contract']` — no pregnancy field present, consistent with the schema having no such question to submit.
- Original response text is preserved as submitted (the JSON blob is not overwritten or normalised away) — the "original response must remain available for provenance" requirement is **structurally satisfied for any field that is actually asked**, since nothing in the pipeline strips or rewrites raw questionnaire answers before persistence. It cannot be satisfied for pregnancy status specifically, because there is no question to preserve an answer to.

---

## 8. Bypass or legacy paths

**REPOSITORY-VERIFIED CURRENT STATE:**
- The primary "bypass" is not a secondary code path — it is the **default behaviour of the primary path**: `questionnaire_data` being `Optional` at the API model, combined with `ContextFactory` only hard-requiring `biomarkers` + `user`, means **no dedicated bypass is needed** to skip mandatory questionnaire fields; omitting them is simply within contract today.
- A **regeneration path** exists (`backend/app/routes/analysis.py`, ~lines 553-616) that reads `questionnaire_data` from a **previously stored** analysis result rather than requiring fresh submission — legitimate for its purpose (re-running analysis against the same inputs), but it means a user's original (possibly incomplete) questionnaire state can be silently carried forward into new analyses indefinitely without ever being asked again.
- No other legacy upload path was found that diverges from this behaviour — the gap is uniform across the one active submission path.

---

## 9. Relevant tests

- `backend/tests/test_context_factory.py:177` — `test_create_context_invalid_sex` (tests malformed/unparseable sex values raise); `line 525, 544` — tests that an **explicitly submitted** `"sex": "other"` parses to `Sex.OTHER` correctly. **No test found asserting that a genuinely *missing* `sex` field is rejected** — consistent with the current silent-default behaviour being untested-against, not merely unguarded in production code.
- `backend/tests/regression/test_runtime_context_evaluation.py:357` — a single `"pregnancy_status": False` fixture value exists in one test case; not a dedicated pregnancy-requirement test suite.
- `backend/tests/regression/test_active_signal_context_gate_reachability.py`, `backend/tests/governance/test_active_signal_context_gate_reachability_governance.py` — govern the `not_answered`-is-safe pregnancy-gate policy described in §6; these tests **enforce** the current (gap) behaviour, they do not flag it as a defect.
- No test anywhere was found asserting that an analysis is rejected, blocked, or deferred when pregnancy status is unknown for a pregnancy-sensitive signal, or that `pregnancy_sensitive_interpretation_required` exists as a computed flag — because no such flag exists in the codebase to test.

---

## 10. Gaps against required behaviour

| # | Gap | Severity |
|---|---|---|
| G1 | No pregnancy question exists in `backend/ssot/questionnaire.json` — none of `not_pregnant`/`pregnant`/`may_be_pregnant` can ever be captured from a user | **Critical** |
| G2 | Because G1, `pregnancy_sensitive_interpretation_required` does not exist anywhere in the codebase — there is no field, flag, or derived value by this name or equivalent | **Critical** |
| G3 | The governance-gated architecture validator (`validate_active_signal_context_gate_reachability.py`) actively **forbids** any pregnancy gate from accepting `answered_yes`, and **requires** all such gates to treat `not_answered` as safe-to-proceed — i.e. even if G1 were fixed today, there is currently no governed path for a "pregnant"/"may_be_pregnant" answer to change any signal's behaviour | **Critical** |
| G4 | `biological_sex` is mandatory in the SSOT schema and enforced in the normal frontend flow, but **not enforced server-side**; a request omitting `user.sex` entirely silently resolves to `Sex.OTHER` rather than failing | **High** |
| G5 | `AnalysisStartRequest.questionnaire_data` is fully optional at the API model layer, and `ContextFactory` never requires questionnaire presence at all — **all** "mandatory" questionnaire fields (not just sex/pregnancy) can be bypassed by any API caller that isn't the standard frontend flow | **High** |
| G6 | The one built-in server-side mandatory-field enforcement mechanism (`ContextFactory.create_analysis_context(..., validate_requirements=...)`) exists in code but is never invoked in the live request path | **Medium** (this is the natural remediation seam for G4/G5, currently unused) |
| G7 | Gestational week / trimester is not captured — moot today because no pregnancy question exists at all (§12) | Follows from G1 |

---

## 11. Recommended remediation (structural only, not implemented)

1. **Add the pregnancy question to `backend/ssot/questionnaire.json`** with exactly the three required values, `required: true`, `importance: mandatory`. Whether it should be unconditionally shown or conditionally displayed (the schema already supports `conditionalDisplay`, used today for `menstrual_hormonal_status`/`low_testosterone_symptoms` keyed on `biological_sex`) is a **product/clinical decision**, not an engineering one — particularly given the `Intersex` option on `biological_sex` needs an explicit answer too, not an assumed exclusion.
2. **Add a derived `pregnancy_sensitive_interpretation_required` boolean** in `runtime_context_evaluator.py`'s snapshot construction, computed from the raw response (`pregnant`/`may_be_pregnant` → `true`, `not_pregnant` → `false`), **alongside** (not replacing) the existing raw disclosure-state field — preserving the original response for provenance and wording per the stated requirement.
3. **Resolve G3 before, or together with, G1/G2**: this is the load-bearing decision. Adding the question without also deciding what "pregnancy-sensitive interpretation" means today creates a dead end — a user could answer "pregnant" and the system would still have no governed rule set to route them to, since the validator's own comment states pregnancy-specific logic is currently unavailable. This is a **medical/clinical decision**, not a schema change.
4. **Add server-side enforcement of mandatory questionnaire fields** — either by wiring the existing but unused `validate_requirements` hook into the real request path, or by giving `AnalysisStartRequest`/`ContextFactory` explicit required-field validation for at least `biological_sex` and (once added) pregnancy status, so the frontend is no longer the only enforcement point.
5. **Fix `_parse_sex`** to raise `ValidationError` when the value is genuinely absent, while still accepting explicit `"other"`/`"intersex"` answers as valid — closing G4 without removing the legitimate "Other" option.

None of the above is implemented by this audit.

---

## 12. Is gestational week or trimester currently captured?

**REPOSITORY-VERIFIED CURRENT STATE: No.** There is no pregnancy question at all (§2, G1), so there is, a fortiori, no gestational-week or trimester field, question, or mapping anywhere in `backend/ssot/questionnaire.json`, `runtime_context_evaluator.py`, or any signal package.

---

## 13. Does the existing contract support a pregnancy-specific ruleset later?

**Partially — contract shape yes, interpretation logic no.**

- **Schema flexibility:** `questionnaire.json` is a flat, easily-extensible list of question objects with an existing `conditionalDisplay` mechanism already used for sex-dependent questions — adding a new mandatory pregnancy question is structurally straightforward and precedented.
- **Runtime mapping flexibility:** `runtime_context_evaluator.py`'s disclosure-state pattern (`_field_answered` / `_disclosure_state_from_value` / `_set_disclosure_state`) is already a generic, reusable mechanism used for several `clinical_context` flags (pregnancy_status among them) — adding a derived boolean alongside it is a small, well-precedented change.
- **What is *not* ready:** the governance policy (`active_signal_context_gate_reachability_policy_v1.yaml`) and its enforcing validator currently **actively forbid** any pregnancy-aware branch in signal gating (G3), and no signal package anywhere in `knowledge_bus/packages/` contains pregnancy-specific interpretation content, thresholds, or hypotheses. So while the *contract* (schema + mapping mechanism) could carry a pregnancy-specific ruleset with modest, additive changes, the *medical content and governance policy* that would make such a ruleset meaningful does not exist today and would need its own Gate 1/Gate 2-class decision, not just an engineering change.

---

## Conclusions

1. **Pregnancy requirement:** the upload flow does not require an answer, because no question exists. The three required values, the resulting clinical mapping, and `pregnancy_sensitive_interpretation_required` are all absent from the codebase. The current, governance-enforced behaviour is the precise inverse of the stated requirement: unanswered pregnancy status is treated as safe to proceed under standard (non-pregnant) rules by design, and no path exists for a "pregnant" answer to ever change behaviour even if one were captured.
2. **Sex requirement:** the question, wording, and allowed values are correctly defined and mandatory in the SSOT schema, and reach the runtime context snapshot when present. It is enforced in the normal frontend flow. It is **not** enforced server-side — a request missing `sex` entirely is silently resolved to `Sex.OTHER` rather than rejected, and no test asserts otherwise.
3. Both gaps trace to the same root architectural pattern: **questionnaire completeness is enforced only by the frontend UI, not by any backend contract**, and the one mechanism that could enforce it server-side (`validate_requirements`) is present in code but never called.

```text
QUESTIONNAIRE_CONTRACT_REMEDIATION_REQUIRED
```
