/**
 * @jest-environment jsdom
 */

import React from 'react';
import { render, screen } from '@testing-library/react';
import { ResultsInvestigationSpine } from '../../app/components/results/ResultsInvestigationSpine';

describe('ResultsInvestigationSpine (FE-R8C)', () => {
  it('renders directional bridge without main-focus duplicate', () => {
    render(<ResultsInvestigationSpine crossBodyPatternLabel="Vascular Inflammation Risk" />);
    expect(screen.getByTestId('results-investigation-spine')).toBeInTheDocument();
    expect(screen.getByText(/Primary finding/i)).toBeInTheDocument();
    expect(screen.getByText(/Vascular Inflammation Risk/)).toBeInTheDocument();
    expect(screen.queryByText(/Main focus/i)).not.toBeInTheDocument();
  });

  it('renders without IDL label when null', () => {
    render(<ResultsInvestigationSpine crossBodyPatternLabel={null} />);
    expect(screen.getByText(/Patterns across your body/i)).toBeInTheDocument();
  });
});
