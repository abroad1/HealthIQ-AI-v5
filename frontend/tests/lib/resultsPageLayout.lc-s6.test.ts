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
