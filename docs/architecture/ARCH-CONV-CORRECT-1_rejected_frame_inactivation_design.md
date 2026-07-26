# ARCH-CONV-CORRECT-1 — Rejected-Frame Total Inactivation Design

**Work ID:** `ARCH-CONV-CORRECT-1`
**Branch:** `feature/arch-conv-correct-1-e2e-authority-layerc`
**Baseline HEAD (kernel start):** `c933d794c9e57c1ee6180d8b943fed009727fd70`
**Workstream:** WS1
**Scope:** `signal_homocysteine_high::inv_homocysteine_high_metabolic` (the only `REJECTED` row in the governed register)

---

## 1. Problem restated

Package 3 recorded the metabolic homocysteine frame as `REJECTED` in
`knowledge_bus/governance/compiled_why_authority_register_v1.yaml`, and
`why_authority_v1.resolve_frame_why_authority` correctly resolves it to `skip`.

That decision only answered *"which WHY asset may serve this frame"*. It did not answer
*"may this frame exist as an active medical result at all"*. The final audit therefore found
the frame still:

- firing as an active signal,
- ranked in `report_v1.top_findings`,
- cited in intervention `activation_key_refs`,
- carrying the interpretation `Reflects methylation capacity and B-vitamin status.`

## 2. Canonical decision

A new module answers the wider question once:

```text
backend/core/knowledge/frame_runtime_authority_v1.py
```

| API | Purpose |
|---|---|
| `rejected_activation_keys()` | Cached set of activation keys whose governed `authority_state` is `REJECTED` |
| `is_frame_runtime_eligible(key)` | Canonical eligibility answer |
| `frame_runtime_exclusion_reason(key)` | `REJECTED_NOT_RUNTIME_ELIGIBLE` for audit surfaces |
| `filter_runtime_eligible_rows(rows)` | Drops rejected rows from signal-result-shaped rows (dict or `SignalResult`) |
| `runtime_ineligible_keys_present(rows)` | Reporting helper for gates |

Properties:

- **Single source of truth.** The register is the only input; no new medical rule is introduced.
- **Fail closed.** An unreadable register raises rather than admitting a rejected frame.
- **No over-reach.** Rows without an `activation_key` are out of the per-frame register's scope;
  identity enforcement for those remains a Package 1 concern.

## 3. Enforcement points (three, not per-consumer)

The prompt forbids scattering ad hoc rejection checks. Enforcement therefore sits at the three
distinct entry points into the medical pipeline:

| # | Surface | File | Effect |
|---:|---|---|---|
| 1 | Registry load | `backend/core/analytics/signal_evaluator.py` (`SignalRegistry._load`) | A rejected activation key never enters the registry, so it cannot be evaluated, fired, scored or ranked. Exclusions are recorded on `excluded_rejected_frames` for audit. |
| 2 | Evaluation output | `backend/core/analytics/signal_evaluator.py` (`SignalEvaluator.evaluate_all`) | Re-asserted after the collision policy, so any path that constructs rows differently still cannot emit a rejected frame. |
| 3 | Report assembly boundary | `backend/core/analytics/insight_graph_builder.py` (`build_insight_graph_v1`) | Replay/fixture rows never passed through evaluation, so they are filtered before ranking, domain scoring, narrative lead selection, interventions and report compilation. |

`build_insight_graph_v1` is the only caller of both `select_interventions_v1` and
`compile_report_v1`, so point 3 covers `top_findings` and intervention references without
adding checks to those consumers. This was verified by inspection rather than assumed, and a
redundant filter that had been added inside `select_interventions_v1` was reverted for that
reason.

## 4. Lifecycle trace (what the frame can no longer do)

| Capability | Blocked at | Evidence |
|---|---|---|
| Enter the active signal result set | 1 | `SignalRegistry._signals_by_activation_key` has no rejected key |
| Be marked fired | 1, 2 | Replay `fired activation keys` list excludes it |
| Participate in ranking / appear in `top_findings` | 1, 3 | Corrected replay `top_findings` has 7 rows, none rejected (baseline had 8, rank #3 rejected) |
| Contribute to domain scoring / narrative lead | 1, 3 | Rows are removed before graph assembly, which feeds both |
| Appear in intervention `signal_refs` / `activation_key_refs` | 3 | Corrected replay: no intervention cites the key (baseline: 2 interventions did) |
| Appear in consumer or clinician summaries | 1, 3 | Retired-wording fingerprint absent from assembled payload |
| Appear in replay as an active medical result | 3 | Injected-fixture regression test asserts absence from the graph payload |
| Act as a fallback for another frame | PKG3 + 1 | `resolve_frame_why_authority` → `skip`; frame absent from runtime set |
| Provide interpretation text | 1 | Its `signal_library.yaml` interpretation is unreachable at runtime |

Rejection stays visible only in the governed register, the package/spec files kept as audit
history, and `SignalRegistry.excluded_rejected_frames`.

## 5. Approved frames unaffected

The sibling homocysteine frames use different activation keys and are untouched:

- `…::inv_homocysteine_high_b_vitamin_related_methylation_impairment` — still fires, still
  compiles its two ratified hypotheses;
- `…::inv_homocysteine_high_renal_clearance_reduction` — unchanged;
- legacy `signal_homocysteine_elevation_context::inv_elevation_context` — unchanged routing.

No signal threshold, activation rule or ranking policy was modified.

## 6. STOP Gate A assessment

| Condition | Assessment |
|---|---|
| Exclusion requires changing approved medical activation rules | **No** — exclusion is keyed on the register, not on thresholds |
| Authority register unavailable at the required stage | **No** — it is loadable at registry-load time (cached YAML) |
| Unexplained ranking/report regressions | **No** — the only ranking change is the removal of the rejected row; all remaining ranks shift up by one |
| New clinical prioritisation rule required | **No** |

Gate A not triggered.

## 7. Tests and gate

- `backend/tests/regression/test_arch_conv_correct1_programme_closure.py` — fire attempt,
  upstream fixture exclusion, root-cause silence, intervention aggregation parity,
  non-over-reach on the MCV family.
- `backend/scripts/validate_arch_conv_correct1_gate.py` — WS1 block.
- `backend/scripts/replay_arch_conv_correct1_uat_case.py` — before/after evidence for the
  audited live analysis.
