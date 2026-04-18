/**
 * @jest-environment jsdom
 */

import React from 'react';
import { render, screen, within } from '@testing-library/react';
import { SystemUnderstandingSection } from '../../app/components/results/SystemUnderstandingSection';

describe('SystemUnderstandingSection (FE-R8C example binding)', () => {
  const clusters = [
    {
      cluster_id: 'c1',
      name: 'Cardiovascular Health Pattern',
      biomarkers: ['ldl_cholesterol', 'hdl_cholesterol'],
      severity: 'high',
    },
  ];

  it('binds block C to IDL retail label when provided with primary driver', () => {
    render(
      <SystemUnderstandingSection
        balanced={{ intro_line: 'Intro', items: [], context_line: 'Ctx' }}
        clusters={clusters}
        primaryDriver={{ id: 'c1', name: 'Cardiovascular Health Pattern', biomarkers: ['ldl_cholesterol'] }}
        idlRetailLabel="Vascular Inflammation Risk"
      />
    );
    const blockC = screen.getByRole('heading', {
      name: 'How markers connect to the bigger picture',
    }).parentElement!;
    expect(within(blockC).getByText(/Vascular Inflammation Risk/)).toBeInTheDocument();
    expect(within(blockC).getByText(/Cardiovascular Health Pattern/)).toBeInTheDocument();
  });
});
