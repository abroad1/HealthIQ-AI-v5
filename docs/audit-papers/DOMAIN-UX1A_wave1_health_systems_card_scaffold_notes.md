# DOMAIN-UX1A — Wave 1 Health Systems Card Scaffold Notes

## 1. Preflight

| Check | Result |
|---|---|
| Branch | `domain-ux/domain-ux1a-wave1-card-scaffold-contract` |
| Stash | Empty |
| Kernel | `DOMAIN-UX1A` STARTED after prompt front-matter fix + clean porcelain |
| Local scratch | Excluded via `.git/info/exclude` (not committed) |

## 2. Source documents reviewed

- `DOMAIN_UX_health_systems_card_scaffold_sprint_plan_FINAL.md`
- `healthiq_health_systems_card_discussion_FINAL.md`
- `User Health to Systems Map_FINAL.md`
- `DOMAIN-UX1_health_systems_card_codebase_reality_audit.md`
- `DOMAIN-R1_launch_core_health_domain_readiness_audit.md`

## 3. DTO fields added

On `ConsumerDomainScoreV1` (`results.py`), emitted by `domain_score_assembler.py`:

| Field | Purpose |
|---|---|
| `plain_english_descriptor` | Consumer descriptor per Wave 1 domain |
| `evidence_completeness_numerator` | Rail biomarkers scored on panel |
| `evidence_completeness_denominator` | Scored + missing (existing rail logic) |
| `subsystems` | `null` forward-compatible slot |

`card_schema_version` bumped to **1.2** for new contract fields.

## 4. Frontend components changed

| File | Change |
|---|---|
| `Wave1DomainCards.tsx` | Journey embed, descriptors, reliability/band/completeness display |
| `wave1HealthSystemCardDisplay.ts` | Presentational label maps only |
| `results/page.tsx` | Cards after “What’s working well”; removed closed disclosure duplicate |
| `analysis.ts` | Type mirror for new DTO fields |

## 5. Evidence completeness

Backend `_evidence_completeness_for_rail()`: `denominator = len(biomarker_scores) + len(missing_marker_ids)`, `numerator = len(biomarker_scores)`. Frontend displays backend values via `wave1EvidenceCompletenessLine()` — no frontend counting.

## 6. Card placement

Main retail journey: immediately after **What’s working well**, before **Primary finding and why**. `data-testid="fe-domain-ux1a-health-systems-cards"`. Removed duplicate from closed “Health domains” disclosure.

## 7. Label / wording changes

| Area | Mapping |
|---|---|
| Reliability | high → Good reliability; medium → Moderate reliability; low → Limited reliability |
| Band | review → Needs attention; watch → Worth watching |
| Section title | “Your health systems” |

## 8. Prose quality gate

Tightened `evidence_anchor_sentence` fallbacks in `domain_narrative_wave1.py` (removed repetitive “on this panel”). No scoring, IDL, or KB content changes.

## 9. No invented subsystems

`subsystems` is `null`; no subsystem chips, placeholder UI, or frontend marker groupings.

## 10. Tests

| File | Role |
|---|---|
| `test_domain_ux1a_wave1_health_systems_card_scaffold.py` | Contract + Sentinel static guards |
| `test_domain_score_assembler_v1.py` | Updated for 1.2 + completeness |
| `Wave1DomainCards.test.tsx` | Consumer field rendering |

## 11. Deferred to DOMAIN-UX1B / DOMAIN-UX1C

- Governed subsystem chips and per-subsystem biomarker grouping
- Compact biomarker card variant / domain dial
- Wave 2 domains (iron, thyroid, kidney)
- Greyed-out biomarker cards in domain context
- Full expanded reveal with subsystem evidence

## 12. Next sprint recommendation

**DOMAIN-UX1B:** subsystem evidence contract when backend-governed subsystem DTO exists. **Do not start KB-WAVE-1** from this sprint alone — mapping layer (MAP-R1A) is fixed; biomarker educational depth remains separate.
