import React from 'react';
import { render, screen } from '@testing-library/react';
import fs from 'fs';
import path from 'path';
import { Wave1SubsystemEvidenceSection } from '../../app/components/results/Wave1SubsystemEvidenceSection';
import type { SubsystemEvidenceV1 } from '../../app/types/analysis';

describe('Wave1SubsystemEvidenceSection', () => {
  const sample: SubsystemEvidenceV1[] = [
    {
      subsystem_id: 'wave1_cv_vascular',
      subsystem_label: 'Vascular strain context',
      included_marker_ids: ['ldl_cholesterol'],
      missing_marker_ids: ['hs_crp'],
      included_markers: [{ id: 'ldl_cholesterol', display_label: 'LDL Cholesterol' }],
      missing_markers: [{ id: 'hs_crp', display_label: 'hs-CRP' }],
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
    expect(screen.getByText('LDL Cholesterol')).toBeInTheDocument();
    expect(screen.getByText('hs-CRP')).toBeInTheDocument();
    expect(screen.getByText('Not uploaded')).toBeInTheDocument();
  });

  it('does not render poor fallback labels when backend display labels are provided', () => {
    render(
      <Wave1SubsystemEvidenceSection
        subsystems={[
          {
            subsystem_id: 'wave1_met_glycaemic',
            subsystem_label: 'Glycaemic control',
            included_marker_ids: ['hba1c', 'crp', 'ldl_cholesterol'],
            missing_marker_ids: ['tc_hdl_ratio'],
            included_markers: [
              { id: 'hba1c', display_label: 'HbA1c' },
              { id: 'crp', display_label: 'CRP' },
              { id: 'ldl_cholesterol', display_label: 'LDL Cholesterol' },
            ],
            missing_markers: [{ id: 'tc_hdl_ratio', display_label: 'TC:HDL ratio' }],
            status_label: null,
            evidence_role: null,
            source_trace: 'Wave 1 governed subsystem map',
          },
        ]}
      />
    );

    expect(screen.getByText('HbA1c')).toBeInTheDocument();
    expect(screen.getByText('CRP')).toBeInTheDocument();
    expect(screen.getByText('LDL Cholesterol')).toBeInTheDocument();
    expect(screen.getByText('TC:HDL ratio')).toBeInTheDocument();
    expect(screen.queryByText('hba1c')).not.toBeInTheDocument();
    expect(screen.queryByText('crp')).not.toBeInTheDocument();
    expect(screen.queryByText('Ldl Cholesterol')).not.toBeInTheDocument();
    expect(screen.queryByText('Tc Hdl Ratio')).not.toBeInTheDocument();
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

  it('renders consumer-safe marker role chips from backend enum', () => {
    render(
      <Wave1SubsystemEvidenceSection
        subsystems={[
          {
            subsystem_id: 'wave1_cv_lipid',
            subsystem_label: 'Lipid transport',
            included_marker_ids: ['ldl_cholesterol'],
            missing_marker_ids: [],
            marker_evidence: [
              {
                marker_id: 'ldl_cholesterol',
                display_label: 'LDL cholesterol',
                marker_role: 'score_contributor',
                relationship_kind: 'direct_score_input',
                presence_policy: 'required_for_subsystem',
              },
            ],
            status_label: null,
            evidence_role: null,
            source_trace: 'Wave 1 governed subsystem map',
          },
        ]}
      />
    );
    expect(screen.getByText('Used in this score')).toBeInTheDocument();
    expect(screen.queryByText(/score contributor/i)).not.toBeInTheDocument();
  });

  it('renders from backend marker display labels, not local wave1Confidence map', () => {
    const sectionPath = path.join(process.cwd(), 'app/components/results/Wave1SubsystemEvidenceSection.tsx');
    const src = fs.readFileSync(sectionPath, 'utf8');
    expect(src).not.toContain('wave1ConfidenceMarkerDisplayLabel');
    expect(src).toContain('included_markers');
    expect(src).toContain('missing_markers');
  });
});
