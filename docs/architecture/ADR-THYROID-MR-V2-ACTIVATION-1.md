# ADR-THYROID-MR-V2-ACTIVATION-1 — Thyroid MR-v2 Activation Completion

## Status

Accepted — P1-25 authority decision.

## Date

2026-06-23

## Context

P1-23 activated TSH directional signal intelligence and the `wave1_thy_hormonal_axis` compiled card. FT3-low (`signal_free_t3_low`) remained excluded from the thyroid domain allowlist per `ADR-THYROID-TSH-SIGNAL-INTELLIGENCE-ACTIVATION-1` Decision 3. kb59 thyroid antibody packages remained inactive per `ADR-THYROID-FT3-AUTHORITY-RECONCILIATION-1`.

Medical Research Activation Review Deferred Wave 1 Items v2 (MR-v2, dated 2026-06-23) clears:

- FT3-low / reduced peripheral T3 availability context with strict gates.
- TPOAb-high / autoimmune thyroid context supporting hypothyroid biochemistry with strict gates.

TPOAb euthyroid context and TgAb packages remain deferred post-launch.

## Medical authority

MR-v2 dated 2026-06-23 is the current medical activation authority for this sprint.

## Decision

1. Activate `signal_free_t3_low` on the thyroid launch allowlist with:
   - lab-range low FT3 activation;
   - mandatory runtime context requirements (TSH, FT4, medication, illness/recovery, calorie restriction, fasting, pregnancy safety);
   - mandatory pre-emission gate requiring TSH not below the lab-provided minimum;
   - fail-closed behaviour when questionnaire context fields are absent in production.

2. Activate `signal_tpo_ab_high` on the thyroid launch allowlist with:
   - lab-range high TPOAb activation;
   - mandatory TSH and FT4 biomarker presence;
   - thyroid medication and pregnancy context requirements;
   - mandatory pre-emission gate requiring TSH above the lab-provided maximum;
   - no emission in euthyroid biochemistry.

3. Keep excluded: `signal_thyroid_tsh_context`.

4. Keep deferred: TPOAb euthyroid context (`pkg_kb59_tpo_ab_high_euthyroid_autoimmune_risk`), TgAb packages.

5. No changes to `signal_evaluator.py`, `scoring_policy.yaml`, `biomarkers.yaml`, or `questionnaire.json` in this sprint.

## Supersession

- Supersedes Decision 3 in `ADR-THYROID-TSH-SIGNAL-INTELLIGENCE-ACTIVATION-1` regarding FT3-low exclusion.
- Partially supersedes the thyroid antibody deferral in `ADR-THYROID-FT3-AUTHORITY-RECONCILIATION-1` for the TPOAb hypothyroid biochemistry frame only.

Existing ADRs are not amended; this ADR records the new authority position.

## Non-negotiable constraints

- No hypothyroidism diagnosis from FT3-low alone.
- No Hashimoto's disease, autoimmune thyroid disease, or hypothyroidism diagnosis from TPOAb alone.
- No “immune system attacking thyroid” or “thyroid will fail” consumer wording.
- No permissive activation without mandatory pre-emission gates.

## Consequences

- P1-22 carry-forward cf_002 (FT3 low deferred) closed when gates pass validation.
- P1-22 carry-forward cf_003 (thyroid antibodies) partially closed for TPOAb hypothyroid frame.
- `wave1_thy_hormonal_axis` enriched with FT3-low and TPOAb source-spec depth.
- Questionnaire alignment for FT3-low context fields remains a product carry-forward; fail-closed behaviour preserved.

## References

- `docs/Medical Research Documents/Medical_Research_Activation_Review_Deferred_Wave_1_Items_v2.md`
- `docs/architecture/ADR-THYROID-TSH-SIGNAL-INTELLIGENCE-ACTIVATION-1.md`
- `docs/architecture/ADR-THYROID-FT3-AUTHORITY-RECONCILIATION-1.md`
- `knowledge_bus/packages/pkg_kb47_free_t3_low_low_t3_syndrome/`
- `knowledge_bus/packages/pkg_kb59_tpo_ab_high_autoimmune_hypothyroid_pattern/`
