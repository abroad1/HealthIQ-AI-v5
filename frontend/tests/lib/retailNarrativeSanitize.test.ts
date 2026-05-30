/**
 * @jest-environment node
 */
import { scrubConsumerRetailNarrative, scrubMojibakeArtifacts, stripSimpleMarkdownDecorators } from '@/lib/retailNarrativeSanitize';

describe('retailNarrativeSanitize LC-S6', () => {
  it('stripSimpleMarkdownDecorators removes bold markers', () => {
    expect(stripSimpleMarkdownDecorators('**Homocysteine** context')).toBe('Homocysteine context');
  });

  it('scrubConsumerRetailNarrative removes internal vocabulary', () => {
    const s = scrubConsumerRetailNarrative('Layer B and Layer C appear in the deterministic narrative compiler output.');
    expect(s).not.toMatch(/Layer B/i);
    expect(s).not.toMatch(/Layer C/i);
    expect(s).not.toMatch(/deterministic narrative compiler/i);
  });

  it('scrubConsumerRetailNarrative maps known signal tokens (LC-S7)', () => {
    const s = scrubConsumerRetailNarrative('Discuss signal_homocysteine_elevation_context with your clinician.');
    expect(s).toContain('homocysteine-related pattern');
    expect(s).not.toContain('signal_homocysteine_elevation_context');
  });

  it('scrubConsumerRetailNarrative replaces homocysteine elevation context title', () => {
    const s = scrubConsumerRetailNarrative('Homocysteine Elevation Context: warrants attention on this panel');
    expect(s).toContain('Raised homocysteine pattern');
    expect(s).not.toMatch(/Homocysteine Elevation Context/i);
  });

  it('scrubMojibakeArtifacts repairs common dash mojibake', () => {
    expect(scrubMojibakeArtifacts('Marker Aâ€”Marker B')).toBe('Marker A—Marker B');
  });
});
