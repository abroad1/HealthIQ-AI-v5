/**
 * @jest-environment node
 */
import {
  consumerMarkerRoleLabel,
  scrubKnownInternalPatternNames,
} from '@/lib/cardEvidenceConsumerCopy';

describe('cardEvidenceConsumerCopy LAUNCH-CORE-1', () => {
  it('maps marker roles to consumer-safe labels', () => {
    expect(consumerMarkerRoleLabel('score_contributor')).toBe('Used in this score');
    expect(consumerMarkerRoleLabel('confidence_contributor')).toBe('Supports confidence');
    expect(consumerMarkerRoleLabel('contextual_marker')).toBe('Context marker');
  });

  it('does not echo raw enum vocabulary', () => {
    expect(consumerMarkerRoleLabel('score_contributor')).not.toContain('score_contributor');
  });

  it('scrubs homocysteine elevation context display name', () => {
    expect(scrubKnownInternalPatternNames('Homocysteine Elevation Context: warrants attention')).toBe(
      'Raised homocysteine pattern: warrants attention'
    );
  });
});
