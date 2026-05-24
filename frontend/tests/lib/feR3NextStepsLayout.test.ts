/**
 * @jest-environment node
 */
import {
  dedupeActionCardsAgainstNarrative,
  normalizeFeR3DedupeKey,
} from '@/lib/feR3NextStepsLayout';
import type { ResultActionCardModel } from '@/lib/resultsPageLayout';

describe('feR3NextStepsLayout', () => {
  it('dedupes action cards that repeat narrative next-step paragraphs', () => {
    const paragraph = 'Repeat fasting glucose and discuss results with your clinician.';
    const cards: ResultActionCardModel[] = [
      {
        heading: 'Repeat fasting glucose',
        paragraph,
        sourceLabel: 'Panel summary',
        categoryLabel: 'Follow-up',
        evidenceLevelLabel: 'Panel-level note',
      },
      {
        heading: 'Different action',
        paragraph: 'Book a follow-up review within three months.',
        sourceLabel: 'Panel summary',
        categoryLabel: 'Follow-up',
        evidenceLevelLabel: 'Panel-level note',
      },
    ];
    const narrative = `- ${paragraph}`;
    const out = dedupeActionCardsAgainstNarrative(cards, narrative);
    expect(out).toHaveLength(1);
    expect(out[0].paragraph).toContain('three months');
  });

  it('normalizeFeR3DedupeKey is stable for punctuation', () => {
    const a = normalizeFeR3DedupeKey('Hello, world!');
    const b = normalizeFeR3DedupeKey('hello world');
    expect(a).toBe(b);
  });
});
