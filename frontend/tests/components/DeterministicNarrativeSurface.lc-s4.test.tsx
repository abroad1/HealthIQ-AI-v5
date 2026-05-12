/**
 * LC-S4 — governed narrative carriage on deterministic surfaces.
 */
import { render, screen } from '@testing-library/react';
import { NarrativeRetailSummaryCard } from '@/components/results/DeterministicNarrativeSurface';
import type { NarrativeReportV1 } from '@/types/analysis';

const minimalNarrative = (over: Partial<NarrativeReportV1> = {}): NarrativeReportV1 => ({
  retail_summary: '',
  body_overview: '',
  lead_narrative: '',
  secondary_narratives: '',
  longitudinal_narrative: '',
  secondary_systems: '',
  next_steps_narrative: '',
  clinician_synthesis: '',
  ...over,
});

describe('DeterministicNarrativeSurface LC-S4', () => {
  it('renders retail_summary from the full narrative object (IDL-independent)', () => {
    render(
      <NarrativeRetailSummaryCard
        narrative={minimalNarrative({
          retail_summary: 'Governed retail line for this panel.',
        })}
      />,
    );
    expect(screen.getByTestId('narrative-retail-summary')).toBeInTheDocument();
    expect(screen.getByText('Governed retail line for this panel.')).toBeInTheDocument();
  });
});
