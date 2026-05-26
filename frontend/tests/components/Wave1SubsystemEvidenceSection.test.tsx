import React from 'react';
import { render, screen } from '@testing-library/react';
import { Wave1SubsystemEvidenceSection } from '../../app/components/results/Wave1SubsystemEvidenceSection';
import type { SubsystemEvidenceV1 } from '../../app/types/analysis';

describe('Wave1SubsystemEvidenceSection', () => {
  const sample: SubsystemEvidenceV1[] = [
    {
      subsystem_id: 'wave1_cv_vascular',
      subsystem_label: 'Vascular strain context',
      included_marker_ids: ['ldl_cholesterol'],
      missing_marker_ids: ['hs_crp'],
      status_label: 'Limited evidence',
      evidence_role: null,
      source_trace: 'Wave 1 governed subsystem map',
    },
  ];

  it('renders subsystem id hooks and backend labels', () => {
    render(<Wave1SubsystemEvidenceSection subsystems={sample} />);
    expect(screen.getByTestId('wave1-subsystem-wave1_cv_vascular')).toBeInTheDocument();
    expect(screen.getByText('Vascular strain context')).toBeInTheDocument();
  });

  it('shows included and missing markers with missing markers tagged as not uploaded', () => {
    render(<Wave1SubsystemEvidenceSection subsystems={sample} />);
    expect(screen.getByText('Ldl Cholesterol')).toBeInTheDocument();
    expect(screen.getByText('Hs Crp')).toBeInTheDocument();
    expect(screen.getByText('Not uploaded')).toBeInTheDocument();
  });

  it('hides non consumer-safe source trace strings', () => {
    render(
      <Wave1SubsystemEvidenceSection
        subsystems={[
          {
            ...sample[0],
            source_trace: 'internal_signal_map/v1',
          },
        ]}
      />
    );

    expect(screen.queryByTestId('wave1-subsystem-source-trace')).not.toBeInTheDocument();
  });
});
