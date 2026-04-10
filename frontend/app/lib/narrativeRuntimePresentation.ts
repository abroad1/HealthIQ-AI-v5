/**
 * Presentation-only mapping for backend `meta.narrative_runtime` (BE-S1B / orchestrator).
 * Does not infer backend states beyond fields actually supplied.
 */

import type { NarrativeRuntimeMetaV1 } from '@/types/analysis';

export function extractNarrativeRuntimeMeta(
  meta: Record<string, any> | undefined | null
): NarrativeRuntimeMetaV1 | undefined {
  if (!meta || typeof meta !== 'object') return undefined;
  const nr = meta['narrative_runtime'];
  if (!nr || typeof nr !== 'object') return undefined;
  return nr as NarrativeRuntimeMetaV1;
}

export type NarrativeEmptyPresentation =
  | { variant: 'populated' }
  | { variant: 'empty'; title: string; detail: string };

/** Known backend policy_reason strings — backend/core/insights/narrative_runtime_policy.py */
const POLICY_REASON_DETAIL: Partial<Record<string, string>> = {
  orchestrator_explicit_false:
    'Narrative generation was turned off for this analysis run. Your structured interpretation and clinician report are unchanged.',
  test_mode_forces_mock:
    'This run used test mode, so live narrative generation is not used. Your structured results above are unchanged.',
  fixture_or_test_mode_uses_mock:
    'This run used fixture mode, so live narrative generation is not used. Your structured results above are unchanged.',
  HEALTHIQ_NARRATIVE_LLM_not_set_default_off:
    'Short narrative summaries are not enabled in this environment (narrative layer switch). Your structured results above are unchanged.',
  HEALTHIQ_ENABLE_LLM_required_with_narrative_master:
    'Narrative summaries require the network model path to be enabled alongside the narrative switch. Your structured results above are unchanged.',
  LLM_ENABLED_false:
    'Narrative summaries are off in configuration for this run. Your structured results above are unchanged.',
  api_path_double_opt_in_passed: '',
};

const GENERIC_NOT_ACTIVE =
  'Narrative generation was not active for this analysis run. Your biomarker interpretation and clinician report are unchanged.';

/**
 * User-facing empty-state copy when `insights.length === 0`.
 * If insights exist, caller should not use empty copy.
 */
export function narrativeEmptyPresentation(
  insightCount: number,
  nr: NarrativeRuntimeMetaV1 | undefined
): NarrativeEmptyPresentation {
  if (insightCount > 0) {
    return { variant: 'populated' };
  }

  if (!nr) {
    return {
      variant: 'empty',
      title: 'No narrative summaries on this result',
      detail:
        'Short narrative summaries may not be available for older results or when runtime details were not recorded. Your hero interpretation and clinician report above remain the primary structured analysis.',
    };
  }

  if (nr.outcome === 'no_validated_insights_after_live_call') {
    return {
      variant: 'empty',
      title: 'No narrative summaries passed quality checks',
      detail:
        'A narrative pass ran for this result, but no short summaries met acceptance checks. This does not change your structured results — use the hero interpretation and clinician report for the main findings.',
    };
  }

  if (nr.synthesizer_allow_llm_resolved === false) {
    const reason = (nr.policy_reason ?? '').trim();
    const mapped = reason ? POLICY_REASON_DETAIL[reason] : undefined;
    const detail = mapped && mapped.length > 0 ? mapped : GENERIC_NOT_ACTIVE;
    return {
      variant: 'empty',
      title: 'Narrative summaries not generated for this run',
      detail,
    };
  }

  return {
    variant: 'empty',
    title: 'No narrative summaries for this result',
    detail:
      'No short summaries were produced for this run. Your hero interpretation and clinician report above remain the primary view.',
  };
}
