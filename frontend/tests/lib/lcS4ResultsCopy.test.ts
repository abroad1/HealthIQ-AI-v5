import { LC_S4_MOCK_MODE_HONESTY_DISCLOSURE } from '@/lib/lcS4ResultsCopy';

describe('lcS4ResultsCopy', () => {
  it('retains sprint-approved mock-mode honesty wording', () => {
    expect(LC_S4_MOCK_MODE_HONESTY_DISCLOSURE).toBe(
      'Your report is built from governed clinical rules applied to your lab data. AI-personalised narrative is not active in this view.',
    );
  });
});
