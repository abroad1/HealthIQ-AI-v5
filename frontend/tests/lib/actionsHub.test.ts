/**
 * @jest-environment node
 */
import { twoSentenceExcerpt } from '../../app/lib/actionsHub';

describe('actionsHub', () => {
  it('twoSentenceExcerpt returns at most two sentences', () => {
    const t = 'First sentence here. Second sentence there. Third ignored.';
    const out = twoSentenceExcerpt(t);
    expect(out).toContain('First sentence here');
    expect(out).toContain('Second sentence there');
    expect(out).not.toContain('Third');
  });
});
