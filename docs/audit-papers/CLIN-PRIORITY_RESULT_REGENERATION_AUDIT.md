# CLIN-PRIORITY-CORE-1 — Result Regeneration & Historic-Result Retention Audit

**Type:** Read-only repository audit (no implementation)
**Scope:** Result classification (current/stale/incompatible), historic-result retention rule, regeneration UX, interaction with `CLIN-PRIORITY-CORE-1`

## 1. Repository-verified facts

**F1. Result status is computed by two composed policies.**
`build_result_versioning_metadata()` (`backend/core/dto/result_versioning_policy_v1.py:135-174`) derives `result_status` from `assess_result_versioning()` (same file, lines 114-132), which merges:
- `assess_persisted_result_compatibility()` — `backend/core/dto/persisted_replay_contract_v1.py:64-105`
- `detect_launch_core_stale_reasons()` — `result_versioning_policy_v1.py:68-111`

Status logic (`result_versioning_policy_v1.py:142-145`):
```
status = "stale" if assessment.stale else "current"
if not assessment.base.compatible: status = "incompatible"
```

**F2. The stale/incompatible checks are an enumerated, closed list — they do not include any CLIN-PRIORITY-CORE-1 field.**
- `assess_persisted_result_compatibility` stale reasons: missing/mismatched `result_version` (line 74-78), missing/mismatched `replay_manifest` (80-88). `compatible` is false only if `PERSISTED_RENDER_REQUIRED_KEYS` or `FRONTEND_CONSUMED_ROOT_KEYS` are absent (`persisted_replay_contract_v1.py:17-29`, `frontend_contract_v1.py:13-38`, compatibility check at line 96).
- `detect_launch_core_stale_reasons` stale reasons: `completeness_policy_id` missing/mismatched vs `launch_core_1_subsystem_union_v1` (lines 72-76), card/subsystem completeness mismatch (78-93), legacy `wave1_subsystem_evidence_v1:` trace (98-100), legacy `total_bilirubin` false-missing (101-103), ARCH-CONV-PKGC-1 waist-unit remediation stamp/allowlist (105-109).

**Neither `PERSISTED_RENDER_REQUIRED_KEYS`, `FRONTEND_CONSUMED_ROOT_KEYS`, nor any `detect_launch_core_stale_reasons` check references `clinical_concern_set` or a CLIN-PRIORITY policy id.** Confirmed by direct read of `persisted_replay_contract_v1.py:17-29,64-105` and `frontend_contract_v1.py:13-38`.

**F3. `clinical_concern_set` is additive and Optional, stored one nesting level below anything the versioning contract inspects.**
`backend/core/models/results.py:461-464`:
```python
clinical_concern_set: Optional[ConsolidatedConcernSet] = Field(
    default=None,
    description="CLIN-PRIORITY-CORE-1: additive ConsolidatedConcernSet from concern construction",
)
```
Per the CLIN-PRIORITY-CORE-1 implementation report (`docs/architecture/CLIN-PRIORITY-CORE-1_implementation_and_verification_report.md:14-16`), the persisted location is `AnalysisResult.meta.insight_graph.clinical_concern_set` — nested under `meta`, which is itself only checked for *presence*, not for the presence of this sub-key, by both versioning contracts.

**F4. No completeness/versioning policy id was bumped by CLIN-PRIORITY-CORE-1.**
`CURRENT_COMPLETENESS_POLICY_ID = "launch_core_1_subsystem_union_v1"` and `CURRENT_RESULT_VERSIONING_POLICY_ID = "launch_core_3_immutable_snapshot_v1"` (`result_versioning_policy_v1.py:28-29`) are unchanged LAUNCH-CORE identifiers. `stamp_current_policy_meta()` (lines 177-182), which runs at persistence time for new analyses, stamps only these two fields — nothing tied to clinical-concern governance. Grep of `backend/core` for `clin_priority`/`CLIN_PRIORITY`/`clinical_concern_set` (see search log) shows no reference to these identifiers anywhere in the versioning/replay contract files.

**F5. Frontend gating is entirely dependent on `result_status` and raw-biomarker presence, both of which are indifferent to `clinical_concern_set`.**
`StaleResultBanner.tsx:21-24`: banner (and therefore the regeneration button) renders only when `versioning.result_status` is `'stale'` or `'incompatible'`. Regeneration button is additionally gated on `versioning.regeneration_available` (`StaleResultBanner.tsx:85`), which is computed by `assess_regeneration_available()` (`backend/core/dto/analysis_regeneration_v1.py:30-34`) — this checks only whether raw upload biomarkers were preserved (`stored_raw_biomarkers_sufficient`, lines 12-21). It has no dependency on clinical-concern-set presence or CLIN-PRIORITY-CORE-1 at all.

**F6. Frontend degrades silently, with no user-facing signal, when `clinical_concern_set` is absent.**
`frontend/app/lib/clinicalConcernSet.ts:7-17` — `getClinicalConcernSet()` returns `null` if the field is absent, malformed, or `findings` is not an array. `hasClinicalConcernAuthority()` (lines 19-24) returns `false` in that case. Per the implementation report (`CLIN-PRIORITY-CORE-1_implementation_and_verification_report.md:41`), `isCloseCallMode(..., { clinicalConcernAuthority: true })` only suppresses the legacy `technical_tiebreak_lead` framing when the concern set **is** present; when absent, the pre-CLIN-PRIORITY-CORE-1 "close-call"/`technical_tiebreak_lead` narrative path is retained as the silent fallback (`frontend/app/lib/leadUncertaintySection.ts:12-44`). No banner, warning, or `stale_reasons` entry accompanies this fallback.

**F7. The historic-result retention rule is a genuine, documented policy — not an accident.**
`docs/architecture/LAUNCH-CORE-3_result_versioning_replay_and_regeneration_policy.md:7-9`: "Generated client-result payloads … are immutable snapshots. The system must never silently overwrite, mutate, or refresh a stored result in place when engine, estate, or presentation policy changes." Lines 69-75 confirm the launch decision was to *warn*, not silently regenerate, and to make regeneration itself non-destructive (new `analysis_id`/version). This rule is intact and is not what this audit questions.

## 2. Findings

**Finding 1 — Confirmed gap: pre-CLIN-PRIORITY-CORE-1 analyses lacking `clinical_concern_set` are classified `current`, not `stale`.**
Given F1–F4, an analysis persisted before CLIN-PRIORITY-CORE-1 shipped, with a valid `result_version`, valid `replay_manifest`, and `meta.completeness_policy_id == "launch_core_1_subsystem_union_v1"`, will pass every existing stale/incompatible check and be reported `result_status: "current"` even though it has no `clinical_concern_set`. This is a straightforward logical consequence of the code as written, not an inference — the check list is closed and enumerable (F2).

**Finding 2 — This is a bounded defect (missing versioning trigger), not intentional policy.**
The LAUNCH-CORE-3 policy document (F7) predates CLIN-PRIORITY-CORE-1 and could not have anticipated it. The CLIN-PRIORITY-CORE-1 report (F3, F6) describes `clinical_concern_set` as governing *which clinical framing the user sees* — it demotes/suppresses the legacy `technical_tiebreak_lead` "close-call" language specifically because that framing was judged clinically inferior or potentially misleading when a governed concern set is available. Nowhere in the CLIN-PRIORITY-CORE-1 report, the LAUNCH-CORE-3 policy, or the versioning contract files is there a stated decision to treat "no clinical_concern_set" as an acceptable permanent state for `current` results. No `no_sop_invention`-class governance record authorises this as deliberate. The most defensible reading is: CLIN-PRIORITY-CORE-1 added a new governed field but did not add a corresponding stale-detection trigger for its absence — an omission consistent with a normal "add new field, forget to register it with the versioning contract" gap.

**Finding 3 — Consequence is silent, not just cosmetic.**
Because the frontend fallback (F6) is silent — no banner, no `stale_reasons`, no `user_message` — a user viewing a `current`-status legacy result sees the old, now-superseded close-call/tiebreak clinical framing with no indication that the platform's clinical-priority governance has since changed and no path to regenerate (the regenerate button never appears, since it is conditioned on `result_status !== 'current'`, F5). This is exactly the kind of divergence the LAUNCH-CORE-3 "warn, never silently diverge" principle (F7) was designed to prevent, applied to a policy surface (clinical concern governance) that didn't exist when that principle was written into code.

## 3. Recommendation (not implemented)

**Minimum safe correction:** add one new stale-reason check to `detect_launch_core_stale_reasons()` (`result_versioning_policy_v1.py:68-111`) — e.g. `clinical_concern_set_policy_missing` — fired when `meta.insight_graph.clinical_concern_set` is absent from a stored payload. This:
- Requires no change to the immutable-snapshot retention rule (F7) — old payloads are still never mutated, only re-labelled as `stale` at read time via the existing `result_status` derivation, exactly as `completeness_policy_id` mismatches already are (F2).
- Requires no change to prioritisation/clinical-concern policy itself — it only extends the *detection* surface that decides whether a warning banner is shown.
- Should reuse the existing `stale` (not `incompatible`) classification, since the payload still renders — it only carries a superseded clinical-framing decision, matching the treatment given to other "presentation policy changed" cases in the current design (F2, F7).
- Would need a corresponding `stamp_current_policy_meta()` update (or an equivalent CLIN-PRIORITY completeness-policy id) so *newly* persisted analyses record explicit clinical-concern-set policy version, giving the check something authoritative to compare against rather than a bare presence test — this determination is a design choice for the accountable engineering owner, not asserted here as the only valid shape.

This is scoped as a **CONTENT/BEHAVIOUR** classification question for whoever authors the follow-on work package; this audit does not assert `risk_level` or file a hardening spec.
