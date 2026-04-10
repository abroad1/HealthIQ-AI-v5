import {
  friendlyHistoryError,
  savedAnalysisPrimaryLabel,
} from '@/lib/historyErrors';

describe('historyErrors (FE-LAUNCH-INTEGRATION-B)', () => {
  it('friendlyHistoryError maps common HTTP-style messages', () => {
    expect(friendlyHistoryError('HTTP 401: Unauthorized')).toMatch(/session/i);
    expect(friendlyHistoryError('503 Service Unavailable')).toMatch(/temporarily unavailable/i);
    expect(friendlyHistoryError('something obscure')).toMatch(/try again/i);
  });

  it('savedAnalysisPrimaryLabel shortens long ids consistently', () => {
    const id = '550e8400-e29b-41d4-a716-446655440000';
    expect(savedAnalysisPrimaryLabel(id).line).toBe('Analysis 550e8400…');
    expect(savedAnalysisPrimaryLabel(id).fullId).toBe(id);
    expect(savedAnalysisPrimaryLabel('short-id').line).toBe('Analysis short-id');
  });
});
