# ARCH-CONV-E3 Implementation Evidence

**Work ID:** `ARCH-CONV-E3`  
**Branch:** `feature/arch-conv-e3-alt-contextual-authority`  
**Gate 1:** `ARCH-CONV-E3-GATE1-HMR-2026-08-01`  
**Gate 2:** `ARCH-CONV-E3-GATE2-ANTHONY-2026-08-01` (RATIFIED)

## Gate 2 ratification record

Anthony explicitly ratified Gate 1 under reference `ARCH-CONV-E3-GATE2-ANTHONY-2026-08-01`
(2026-08-01). Authority surfaces updated to `gate2_status: RATIFIED`:

- `docs/architecture/ARCH-CONV-E3_medical_decision_register.yaml`
- `docs/architecture/ARCH-CONV-E3_GATE_2_Anthony_ratification.md`
- `knowledge_bus/governance/signal_authority_collision_model_v1.yaml` (`alt_biochemical_pattern_axis`)
- `knowledge_bus/governance/package_runtime_activation_register_v1.yaml`
- package `gate2_reference` metadata on the four E3 ALT contextual package manifests
  (reference string only; no signal/PSI/medical content changes)

No runtime behaviour, medical rules, or unresolved blocker dispositions were changed by
the Gate 2 recording commit. Test assertion strings that mirror the Gate 2 reference were
aligned to the ratified ID.

## Verified starting state

- ARCH-CONV-E2 merged to `main` and Gate 2 ratified.
- Six ALT packages present with mandatory assets.
- Hepatocellular + mixed activated; four contextual packages withheld.
- Canonical Pass 3 hash `7F20BF9A06B3427217AD7F753C4D9304E5D5A2C46C484699257778844B9D3267` unchanged.
- No stash entries present at preflight.

## Research rule → runtime mechanism mapping

| Context | Disposition | Runtime mechanism |
|---|---|---|
| Cholestatic / ALP-predominant | ACTIVATE subordinate contextual | Existing R≤2 `mandatory_pre_emission_gates`; hyp selection returns `None` for hepatocellular when R≤2; role subordination (not `liver_injury_axis` supporting family) |
| Muscle / exertional | ACTIVATE lab-only subordinate | `mandatory_pre_emission_gates`: `creatine_kinase` `lab_range_boundary` `above_max` |
| Bilirubin severity | OVERRIDE escalation only | `or_alt_high_with_bilirubin_high` (+ siblings) on active ALT frames with `presentation_safety.consumer_hys_law_diagnosis: PROHIBITED`; package withheld |
| Metabolic / MASLD | ACTIVATE lab-only subordinate | Compound `any_of` gate via extended `_passes_mandatory_pre_emission_gates` (`hba1c`/`triglycerides`/`ggt` above_max or `hdl_cholesterol` below_min) |

## Collision / coexistence table

| Pair | Behaviour |
|---|---|
| ALP/GGT primary vs ALT cholestatic | ALP/GGT remain sole cholestatic SOURCE primary; ALT R≤2 is biochemical pattern context. `signal_alt_high` not added as liver supporting family (named-key filter / family-level suppress would harm hepatocellular/mixed). Activation-key-level suppress deferred as contract gap. |
| Hepatocellular vs mixed vs cholestatic | Band ownership: R≥5 hep; 2\<R\<5 mixed; R≤2 cholestatic; R missing → hep rank-2 general |
| Muscle vs hep | Coexist when CK above lab max; muscle does not suppress liver concern |
| Bilirubin | Escalation on active frames only; no competing primary package |

## Activation-register delta

- Version `1.3.0` → `1.4.0`; work_id `ARCH-CONV-E3`
- `activated_frame_count` `174` → `177`
- Added: cholestatic, muscle, metabolic activation keys
- Withheld retained: bilirubin severity only

## Before / after runtime ALT identities

**Before:** hepatocellular, mixed  
**After:** hepatocellular, mixed, cholestatic, muscle, metabolic  
**Still withheld:** bilirubin severity  
**Still superseded:** S24 ALT-high

## Unresolved blockers (explicit)

1. No governed runtime user-context contract (`context_modifier_catalogue_draft_v1.yaml` non-runtime) — blocks exercise/metabolic declared-history paths only.
2. No Pass 3 numeric threshold for “very high ALT” — blocks that specific suppress safeguard only.
3. Activation-key-level suppress of cholestatic ALT when ALP primary present requires collision-contract extension — deferred.

## Proof: no invented medical thresholds / no raw Pass 3 runtime read / no frontend inference

- Gates use lab-range status only.
- Hypothesis selection and package assets remain the runtime path; Pass 3 JSON is not imported by evaluator code.
- No frontend files modified.

## Tests run

```text
PYTHONPATH=backend python -m pytest \
  backend/tests/unit/test_arch_conv_e3_alt_contextual_authority.py \
  backend/tests/unit/test_arch_conv_e2_r_value_runtime_authority.py \
  backend/tests/unit/test_arch_conv_e_runtime_activation_boundary.py \
  backend/tests/unit/test_arch_conv_e_alt_package_assets.py \
  backend/tests/unit/test_signal_evaluator.py::test_signal_registry_alt_high_multi_frame_pilot \
  -q
```

Result: **PASS** (exit 0).

Package validators: muscle + metabolic + other ALT packages validated via activation-boundary suite.

## Files changed (implementation)

See `git diff --name-only` on the feature branch for the authoritative list.

---

## Test-harness remediation (post-audit; bounded)

**Scope:** test harness + evidence only. No production, runtime, governance, package, Gate 1, collision, activation, or blocker changes.

### Helper ambiguity

`backend/tests/unit/test_signal_evaluator.py` helper `_load_signal_definition(signal_id)` resolved by bare `signal_id` and returned `matches[0]` (after preferring `pkg_s24_*`).

That assumption became invalid after ARCH-CONV-E3 multi-frame ALT activation: `signal_alt_high` now has **five** production-reachable frames. Registry iteration order is not a governed selector, so the KB-S24 ALT baseline/escalation case could bind the wrong frame.

### Exact harness fix

1. `_KB_S24_SIGNAL_CASES["signal_alt_high"]` now carries:
   `activation_key: signal_alt_high::inv_alt_high_r_value_hepatocellular_biochemical_pattern`
2. `_load_signal_definition(..., activation_key=None)` resolves by exact activation key when provided; raises on ambiguous multi-frame `signal_id` without a key.
3. `_single_signal_evaluator` and KB-S24 baseline/escalation tests pass the case `activation_key`.
4. ALT escalate assertions require:
   - canonical hepatocellular `activation_key`
   - rank-2 general hypothesis when derived R-value is empty
   - `suboptimal` → `at_risk` when bilirubin exceeds governed lab max

### Full `test_signal_evaluator.py` command and output

```text
PYTHONPATH=backend python -m pytest backend/tests/unit/test_signal_evaluator.py -q
```

Output (feature branch after harness fix):

```text
........................................................................ [ 43%]
F....................................................................... [ 86%]
.......................                                                  [100%]
================================== FAILURES ===================================
C:\Users\abroa\HealthIQ-AI-v5\backend\tools\run_golden_panel.py:74: ValueError: Golden panel fixture must include biomarkers and user
=========================== short test summary info ===========================
FAILED backend\tests\unit\test_signal_evaluator.py::test_kbs23_catalogue_panel_harness_runs_all_panel_fixtures
```

- ALT KB-S24 baseline/escalation case: **PASS** against the canonical hepatocellular activation key.
- Sole remaining failure in this file: `test_kbs23_catalogue_panel_harness_runs_all_panel_fixtures`.

### Pre-existing catalogue failure (re-confirmed on clean `main`)

Detached worktree at `main` (`6d28d30`):

```text
PYTHONPATH=backend python -m pytest \
  backend/tests/unit/test_signal_evaluator.py::test_kbs23_catalogue_panel_harness_runs_all_panel_fixtures -q
```

```text
F                                                                        [100%]
================================== FAILURES ===================================
...\backend\tools\run_golden_panel.py:74: ValueError: Golden panel fixture must include biomarkers and user
FAILED backend\tests\unit\test_signal_evaluator.py::test_kbs23_catalogue_panel_harness_runs_all_panel_fixtures
MAIN_EXIT=1
```

Recorded as **pre-existing on main**; out of scope for this remediation.

### Focused regression + validators (remediation)

```text
PYTHONPATH=backend python -m pytest \
  backend/tests/unit/test_arch_conv_e3_alt_contextual_authority.py \
  backend/tests/unit/test_arch_conv_e2_r_value_runtime_authority.py \
  backend/tests/unit/test_arch_conv_e_alt_package_assets.py \
  backend/tests/unit/test_arch_conv_e_runtime_activation_boundary.py \
  backend/tests/regression/test_signal_authority_collision_enforcement.py -q
```

Result: **PASS** (exit 0).

Four ARCH-CONV-E3 package validators (`cholestatic`, `muscle`, `bilirubin_severity`, `metabolic`): each `manifest/research/signal/PSI` **PASS**.

### Production/runtime/governance unchanged in remediation

`git diff --name-only` for this remediation commit is limited to:

- `backend/tests/unit/test_signal_evaluator.py`
- `docs/architecture/ARCH-CONV-E3_implementation_evidence.md`
