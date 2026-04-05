import React from 'react';
import { render, screen } from '@testing-library/react';
import BiomarkerDials from '../../../app/components/biomarkers/BiomarkerDials';

describe('BiomarkerDials', () => {
  const mockBiomarkers = {
    glucose: {
      value: 100,
      unit: 'mg/dL',
      date: '2024-01-01',
      referenceRange: {
        min: 70,
        max: 100,
        unit: 'mg/dL',
      },
      status: 'normal',
    },
    hba1c: {
      value: 5.5,
      unit: '%',
      date: '2024-01-01',
      referenceRange: {
        min: 4.0,
        max: 5.7,
        unit: '%',
      },
      status: 'optimal',
    },
    total_cholesterol: {
      value: 220,
      unit: 'mg/dL',
      date: '2024-01-01',
      referenceRange: {
        min: 200,
        max: 240,
        unit: 'mg/dL',
      },
      status: 'elevated',
    },
  };

  it('renders section title and biomarker labels', () => {
    render(<BiomarkerDials biomarkers={mockBiomarkers} />);

    expect(screen.getByText('Your markers')).toBeInTheDocument();
    expect(screen.getByText('Glucose')).toBeInTheDocument();
    expect(screen.getByText('HbA1c')).toBeInTheDocument();
    expect(screen.getByText('Total Cholesterol')).toBeInTheDocument();
  });

  it('shows values and units', () => {
    render(<BiomarkerDials biomarkers={mockBiomarkers} />);

    expect(screen.getAllByText('100.0').length).toBeGreaterThan(0);
    expect(screen.getAllByText('mg/dL').length).toBeGreaterThan(0);
    expect(screen.getAllByText('5.5').length).toBeGreaterThan(0);
  });

  it('displays status badges', () => {
    render(<BiomarkerDials biomarkers={mockBiomarkers} />);

    expect(screen.getAllByText('Normal').length).toBeGreaterThan(0);
    expect(screen.getAllByText('Optimal').length).toBeGreaterThan(0);
    expect(screen.getAllByText('Elevated').length).toBeGreaterThan(0);
  });

  it('shows reference ranges in details mode', () => {
    render(<BiomarkerDials biomarkers={mockBiomarkers} showDetails />);

    expect(screen.getAllByText(/Range: 70-100 mg\/dL/).length).toBeGreaterThan(0);
    expect(screen.getAllByText(/Range: 4-5.7 %/).length).toBeGreaterThan(0);
  });

  it('renders dial svgs', () => {
    render(<BiomarkerDials biomarkers={mockBiomarkers} />);
    expect(document.querySelectorAll('svg').length).toBeGreaterThan(0);
  });

  it('shows date when showDetails and date set', () => {
    render(<BiomarkerDials biomarkers={mockBiomarkers} showDetails />);
    expect(screen.getAllByText('01/01/2024').length).toBeGreaterThan(0);
  });

  it('handles biomarkers without reference ranges', () => {
    render(
      <BiomarkerDials
        biomarkers={{
          glucose: { value: 100, unit: 'mg/dL', status: 'normal' },
        }}
      />,
    );
    expect(screen.getByText('Glucose')).toBeInTheDocument();
    expect(screen.getAllByText('100.0').length).toBeGreaterThan(0);
  });

  it('shows interpretation when showDetails and interpretation provided', () => {
    render(
      <BiomarkerDials
        biomarkers={{
          glucose: {
            value: 100,
            unit: 'mg/dL',
            status: 'normal',
            interpretation: 'Within expected range.',
          },
        }}
        showDetails
      />,
    );
    expect(screen.getByText('Within expected range.')).toBeInTheDocument();
  });

  it('shows empty state', () => {
    render(<BiomarkerDials biomarkers={{}} />);
    expect(screen.getByText('No biomarker data available.')).toBeInTheDocument();
  });

  it('respects custom section title', () => {
    render(<BiomarkerDials biomarkers={mockBiomarkers} sectionTitle="Markers (detail)" />);
    expect(screen.getByText('Markers (detail)')).toBeInTheDocument();
  });
});
