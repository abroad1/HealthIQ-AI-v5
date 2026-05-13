/**
 * @jest-environment node
 */
import { buildActionCardModels, parseNarrativeNextStepParagraphs } from '@/lib/resultsPageLayout';

describe('resultsPageLayout LC-S6', () => {
  it('parseNarrativeNextStepParagraphs normalises bullet lines', () => {
    const lines = parseNarrativeNextStepParagraphs(
      '- Discuss these results with your clinician.\n- Consider repeating key markers on advice.',
    );
    expect(lines.length).toBe(2);
    expect(lines[0]).toContain('Discuss these results');
  });

  it('buildActionCardModels falls back to narrative next steps when nothing else is present', () => {
    const models = buildActionCardModels([], [], {
      narrativeNextStepsNarrative:
        '- Discuss these results with your clinician.\n- Arrange follow-up testing as advised.',
    });
    expect(models.length).toBeGreaterThan(0);
    expect(models[0].sourceLabel).toBe('Report next steps');
  });

  it('does not append narrative cards when cluster recommendations exist', () => {
    const models = buildActionCardModels(
      [
        {
          cluster_id: '1',
          name: 'Metabolic',
          severity: 'moderate',
          biomarkers: [],
          recommendations: ['Eat more vegetables daily for fibre.'],
        },
      ],
      [],
      {
        narrativeNextStepsNarrative: '- This narrative line should not appear when cluster recs exist.',
      },
    );
    expect(models).toHaveLength(1);
    expect(models[0].paragraph).toContain('vegetables');
  });
});

describe('resultsPageLayout LC-S7', () => {
  it('parseNarrativeNextStepParagraphs drops Safe next-step framing preamble line', () => {
    const lines = parseNarrativeNextStepParagraphs(
      'Safe next-step framing (Layer C, bounded):\n• Discuss these findings with a clinician.',
    );
    expect(lines.some((l) => /safe\s+next-?step\s+framing/i.test(l))).toBe(false);
    expect(lines.length).toBeGreaterThan(0);
  });

  it('buildActionCardModels omits narrative fallback when omitNarrativeNextStepsFromCards is true', () => {
    const models = buildActionCardModels([], [], {
      narrativeNextStepsNarrative: '- Discuss these results with your clinician.',
      omitNarrativeNextStepsFromCards: true,
    });
    expect(models).toHaveLength(0);
  });

  it('buildActionCardModels dedupes identical paragraphs from different clusters', () => {
    const models = buildActionCardModels(
      [
        {
          cluster_id: '1',
          name: 'A',
          severity: 'moderate',
          biomarkers: [],
          recommendations: ['Same follow-up sentence for fibre and movement daily.'],
        },
        {
          cluster_id: '2',
          name: 'B',
          severity: 'moderate',
          biomarkers: [],
          recommendations: ['Same follow-up sentence for fibre and movement daily.'],
        },
      ],
      [],
      {},
    );
    expect(models).toHaveLength(1);
  });
});
