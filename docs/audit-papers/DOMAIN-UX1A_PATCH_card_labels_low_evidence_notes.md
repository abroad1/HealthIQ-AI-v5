# DOMAIN-UX1A-PATCH — Card Labels and Low-Evidence Notes

## 1. Preflight results

| Check | Result |
|---|---|
| Branch | `domain-ux/domain-ux1a-card-labels-low-evidence` |
| Stash | Empty |
| Kernel token | `DOMAIN-UX1A-PATCH` started and branch matched |
| Working tree before start | Governed by committing `latest_cursor_prompt.md` + `latest_prompt_hardening.json` |

## 2. Source documents reviewed

- `docs/planning-papers/DOMAIN_UX_health_systems_card_scaffold_sprint_plan_FINAL.md`
- `docs/discussion documents/healthiq_health_systems_card_discussion_FINAL.md`
- `docs/audit-papers/DOMAIN-UX1A_wave1_health_systems_card_scaffold_notes.md`
- `docs/audit-papers/DOMAIN-UX1_health_systems_card_codebase_reality_audit.md`
- `docs/governance/AUTOMATION_BUS_SOP_v1.3.1.md`

## 3. Exact visible issue confirmed

Confirmed from current UI + code baseline:

- Reliability rendered value-only (`Limited reliability`) with no visible `Score reliability` label.
- Evidence completeness rendered value-only (`Based on X of Y expected markers...`) with no visible `Evidence completeness` label.
- Zero-evidence cards rendered `0 / 100` and `Needs attention` as primary score state, creating misleading adverse framing for insufficient data.

## 4. Label hierarchy changes made

Collapsed card now renders explicit labels:

- `Score reliability`
- `Evidence completeness`

with corresponding values directly beneath each heading.

## 5. Low-evidence state rule implemented

Rule:

```text
if evidence_completeness_numerator === 0 and evidence_completeness_denominator > 0
```

then collapsed card now shows:

- `Not enough data`
- `This area needs more marker evidence before HealthIQ can score it meaningfully.`

and suppresses primary `score / 100` plus primary band chip in this state.

Partial-evidence cards (numerator > 0) continue to show score + band, with clear reliability and completeness labels.

## 6. Files changed

- `frontend/app/components/results/Wave1DomainCards.tsx`
- `frontend/app/lib/wave1HealthSystemCardDisplay.ts`
- `frontend/tests/components/Wave1DomainCards.test.tsx`
- `backend/tests/regression/test_domain_ux1a_wave1_health_systems_card_scaffold.py`
- `sentinel/packs/escaped_defects_v1.json`

## 7. Tests added/updated

- Updated `Wave1DomainCards` component tests for:
  - label + value hierarchy (`Score reliability`, `Evidence completeness`)
  - zero-evidence insufficient-data rendering
  - suppression of `0 / 100` and `Needs attention` in zero-evidence state
- Updated DOMAIN-UX1A regression sentinel test file for new label/zero-evidence defect classes.

## 8. Sentinel updates

Added active deterministic classes:

- `health_system_card_reliability_label_missing`
- `health_system_card_evidence_completeness_label_missing`
- `health_system_card_zero_evidence_shows_needs_attention`
- `health_system_card_zero_evidence_shows_primary_zero_score`

All point to `backend/tests/regression/test_domain_ux1a_wave1_health_systems_card_scaffold.py`.

## 9. Confirmation scoring logic unchanged

No scoring thresholds, band computation rules, confidence computation rules, signal logic, root-cause logic, IDL, or Knowledge Bus assets were changed.

Patch is presentation semantics only.

## 10. Residual gaps for DOMAIN-UX1B / DOMAIN-UX1C

- DOMAIN-UX1B: visual polish and richer card hierarchy/layout refinements.
- DOMAIN-UX1C: governed subsystem structures/chips and subsystem evidence model.

No subsystem grouping/chips were added in this patch.

## 11. Browser/UAT status

Browser verification required by sprint prompt; run against:

`http://localhost:3000/results?analysis_id=d7417288-7e11-48da-8716-d0f63f77c491`

to confirm:

- labels visible
- zero-evidence cards use insufficient-data state
- no `0 / 100 Needs attention` primary state for zero-evidence cards.

## 12. Recommendation for next sprint

Proceed with DOMAIN-UX1B after merge for card visual hierarchy refinement, then DOMAIN-UX1C for governed subsystem surfacing.
