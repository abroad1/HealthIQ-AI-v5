/**
 * @jest-environment node
 */

import {
  buildBodyOverviewPrimarySentence,
  ensureTerminalPunctuation,
  extractFirstSentence,
} from '../../app/lib/bodyOverviewPrimarySentence';

describe('bodyOverviewPrimarySentence (FE-R8B)', () => {
  describe('ensureTerminalPunctuation', () => {
    it('adds a period when the clause has no terminal punctuation', () => {
      expect(ensureTerminalPunctuation('Homocysteine context warrants attention on this panel')).toBe(
        'Homocysteine context warrants attention on this panel.'
      );
    });
    it('does not double punctuate when already present', () => {
      expect(ensureTerminalPunctuation('Already done.')).toBe('Already done.');
    });
  });

  describe('buildBodyOverviewPrimarySentence', () => {
    it('joins tie-mode rider with a proper boundary after the lead clause', () => {
      const page1 = {
        primary_concern: 'Homocysteine Elevation Context: warrants attention on this panel',
        primary_concern_mode: 'near_tie_ambiguity' as const,
        key_findings: [],
        chains: [],
      };
      const out = buildBodyOverviewPrimarySentence(page1);
      expect(out).toContain('Homocysteine Elevation Context: warrants attention on this panel.');
      expect(out).toContain('More than one pattern is close');
      expect(out.indexOf('panel.')).toBeLessThan(out.indexOf('More than'));
    });

    it('ignores compiler placeholder top_hypothesis_line when primary_concern is empty', () => {
      const page1 = {
        primary_concern: '',
        top_hypothesis_line: 'No hypothesis set available for this concern in v1.',
        key_findings: ['Marker X is elevated on this panel.'],
        chains: [],
      };
      const out = buildBodyOverviewPrimarySentence(page1);
      expect(out).not.toContain('No hypothesis set available');
      expect(out).toContain('Marker X is elevated');
    });
  });

  describe('extractFirstSentence', () => {
    it('returns first sentence when delimited', () => {
      expect(extractFirstSentence('First bit. Second bit.')).toBe('First bit.');
    });
  });
});
