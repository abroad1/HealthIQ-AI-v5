/**
 * @jest-environment node
 */

import { buildSection3LeadStatement, buildWhatThisMeansBlock } from '../../app/lib/primaryFindingShaping';

const PLACEHOLDER_HYP = 'No hypothesis set available for this concern in v1.';

describe('primaryFindingShaping — compiler placeholder suppression', () => {
  const page1Base = {
    primary_concern: 'Lh High: is outside the optimal range on this panel.',
    key_findings: ['Lh High is outside the optimal range on this panel.'],
    chains: [] as string[],
  };

  it('buildWhatThisMeansBlock drops placeholder top_hypothesis_line and uses key findings', () => {
    const out = buildWhatThisMeansBlock({
      ...page1Base,
      top_hypothesis_line: PLACEHOLDER_HYP,
    });
    expect(out).not.toContain('No hypothesis set available');
    expect(out).toContain('Lh High');
  });

  it('buildSection3LeadStatement does not prefix Leading explanation with placeholder', () => {
    const out = buildSection3LeadStatement({
      ...page1Base,
      top_hypothesis_line: PLACEHOLDER_HYP,
    });
    expect(out).not.toContain('No hypothesis set available');
    expect(out).toContain('Main finding for this panel');
    expect(out).not.toMatch(/Leading explanation:\s*No hypothesis/i);
  });
});
