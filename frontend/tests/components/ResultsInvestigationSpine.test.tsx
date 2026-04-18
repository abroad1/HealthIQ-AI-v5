/**
 * @jest-environment jsdom
 */

import React from 'react';
import { render, screen } from '@testing-library/react';
import { ResultsInvestigationSpine } from '../../app/components/results/ResultsInvestigationSpine';

describe('ResultsInvestigationSpine', () => {
  it('renders nothing when no props', () => {
    const { container } = render(
      <ResultsInvestigationSpine focusLine={null} idlRetailLabel={null} idlSubtitle={null} />
    );
    expect(container.firstChild).toBeNull();
  });

  it('renders focus and IDL lines from governed strings', () => {
    render(
      <ResultsInvestigationSpine
        focusLine="Lead topic."
        idlRetailLabel="Vascular pattern"
        idlSubtitle="Inflammation and lipids"
      />
    );
    expect(screen.getByText('Lead topic.')).toBeInTheDocument();
    expect(screen.getByText('Vascular pattern')).toBeInTheDocument();
    expect(screen.getByText('Inflammation and lipids')).toBeInTheDocument();
  });
});
