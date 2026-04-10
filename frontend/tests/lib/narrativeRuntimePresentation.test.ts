import {
  extractNarrativeRuntimeMeta,
  narrativeEmptyPresentation,
} from '@/lib/narrativeRuntimePresentation';
import type { NarrativeRuntimeMetaV1 } from '@/types/analysis';

describe('extractNarrativeRuntimeMeta', () => {
  it('returns undefined when meta is missing', () => {
    expect(extractNarrativeRuntimeMeta(undefined)).toBeUndefined();
    expect(extractNarrativeRuntimeMeta(null)).toBeUndefined();
  });

  it('returns undefined when narrative_runtime absent', () => {
    expect(extractNarrativeRuntimeMeta({ burden_vector: {} })).toBeUndefined();
  });

  it('returns typed object when narrative_runtime present', () => {
    const nr: NarrativeRuntimeMetaV1 = {
      policy_version: '1.0.0',
      synthesizer_allow_llm_resolved: false,
      policy_reason: 'HEALTHIQ_NARRATIVE_LLM_not_set_default_off',
    };
    expect(extractNarrativeRuntimeMeta({ narrative_runtime: nr })).toEqual(nr);
  });
});

describe('narrativeEmptyPresentation', () => {
  it('returns populated when insights exist', () => {
    expect(narrativeEmptyPresentation(1, undefined)).toEqual({ variant: 'populated' });
  });

  it('legacy / no metadata — calm, non-alarmist', () => {
    const p = narrativeEmptyPresentation(0, undefined);
    expect(p.variant).toBe('empty');
    if (p.variant === 'empty') {
      expect(p.title).toMatch(/No narrative summaries on this result/i);
      expect(p.detail).toMatch(/older results|not recorded/i);
    }
  });

  it('no validated insights after live call', () => {
    const nr: NarrativeRuntimeMetaV1 = {
      synthesizer_allow_llm_resolved: true,
      runtime_mode: 'live_gemini',
      outcome: 'no_validated_insights_after_live_call',
    };
    const p = narrativeEmptyPresentation(0, nr);
    expect(p.variant).toBe('empty');
    if (p.variant === 'empty') {
      expect(p.title).toMatch(/quality checks/i);
      expect(p.detail).toMatch(/acceptance checks/i);
    }
  });

  it('policy disabled — uses known policy_reason copy', () => {
    const nr: NarrativeRuntimeMetaV1 = {
      synthesizer_allow_llm_resolved: false,
      policy_reason: 'HEALTHIQ_NARRATIVE_LLM_not_set_default_off',
    };
    const p = narrativeEmptyPresentation(0, nr);
    expect(p.variant).toBe('empty');
    if (p.variant === 'empty') {
      expect(p.detail).toMatch(/not enabled in this environment/i);
    }
  });

  it('allow_llm true, no outcome, zero insights — generic truthful copy', () => {
    const nr: NarrativeRuntimeMetaV1 = {
      synthesizer_allow_llm_resolved: true,
      runtime_mode: 'deterministic_mock',
      policy_reason: 'api_path_double_opt_in_passed',
    };
    const p = narrativeEmptyPresentation(0, nr);
    expect(p.variant).toBe('empty');
    if (p.variant === 'empty') {
      expect(p.detail).toMatch(/primary view/i);
    }
  });
});
