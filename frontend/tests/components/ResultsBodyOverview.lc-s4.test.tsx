import { render, screen } from '@testing-library/react';
import { ResultsBodyOverview } from '@/components/results/ResultsBodyOverview';

describe('ResultsBodyOverview LC-S4', () => {
  it('prefers compiled body_overview from narrative_report_v1 when provided', () => {
    render(
      <ResultsBodyOverview
        clinicianReport={undefined}
        clusters={[]}
        compiledBodyOverview="Cross-system posture summarised for this panel."
      />,
    );
    expect(screen.getByTestId('results-body-overview')).toBeInTheDocument();
    expect(screen.getByText('Cross-system posture summarised for this panel.')).toBeInTheDocument();
  });
});
