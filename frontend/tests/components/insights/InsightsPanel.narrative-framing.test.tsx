/**
 * FE-S2A — narrative presentation framing (translation layer copy).
 */
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { InsightsPanel } from '@/components/insights/InsightsPanel';

describe('InsightsPanel narrative framing (FE-S2A)', () => {
  it('frames empty state as narrative summaries, not generic health insights', () => {
    render(<InsightsPanel insights={[]} />);
    expect(screen.getByText('Narrative summaries')).toBeInTheDocument();
    expect(screen.getByText(/Plain-language summaries derived from your structured analysis/i)).toBeInTheDocument();
    expect(screen.queryByText('Health Insights')).not.toBeInTheDocument();
    expect(screen.getByText(/No narrative summaries on this result/i)).toBeInTheDocument();
  });

  it('FE-S2B: shows runtime-aware copy when narrative is disabled by policy', () => {
    render(
      <InsightsPanel
        insights={[]}
        narrativeRuntime={{
          synthesizer_allow_llm_resolved: false,
          policy_reason: 'HEALTHIQ_NARRATIVE_LLM_not_set_default_off',
        }}
      />
    );
    expect(screen.getByText('Narrative summaries not generated for this run')).toBeInTheDocument();
    expect(screen.getByText(/not enabled in this environment/i)).toBeInTheDocument();
  });

  it('keeps narrative framing when summaries exist', async () => {
    const user = userEvent.setup();
    render(
      <InsightsPanel
        insights={[
          {
            id: 'n1',
            category: 'metabolic',
            summary: 'Example narrative line',
            severity: 'info',
            confidence: 0.85,
          },
        ]}
      />
    );
    expect(screen.getByText('Narrative summaries')).toBeInTheDocument();
    expect(screen.getByText(/Readable summaries from structured results/i)).toBeInTheDocument();
    expect(screen.getByText('1 summaries')).toBeInTheDocument();
    expect(screen.getByText('Total summaries')).toBeInTheDocument();
    expect(screen.queryByText('Health Insights')).not.toBeInTheDocument();
    const metabolicButtons = screen.getAllByRole('button', { name: /Metabolic Health/i });
    await user.click(metabolicButtons[metabolicButtons.length - 1]);
    expect(screen.getByText('Example narrative line')).toBeInTheDocument();
  });
});
