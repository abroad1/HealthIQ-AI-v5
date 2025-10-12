import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import BiomarkerDials from '../../app/components/biomarkers/BiomarkerDials';

// Mock the UI components
jest.mock('@/components/ui/card', () => ({
  Card: ({ children, className }: any) => <div className={className}>{children}</div>,
  CardContent: ({ children, className }: any) => <div className={className}>{children}</div>,
  CardDescription: ({ children, className }: any) => <div className={className}>{children}</div>,
  CardHeader: ({ children, className }: any) => <div className={className}>{children}</div>,
  CardTitle: ({ children, className }: any) => <h3 className={className}>{children}</h3>,
}));

jest.mock('@/components/ui/badge', () => ({
  Badge: ({ children, className }: any) => <span className={className}>{children}</span>,
}));

jest.mock('@/components/ui/button', () => ({
  Button: ({ children, onClick, className }: any) => (
    <button onClick={onClick} className={className}>{children}</button>
  ),
}));

jest.mock('@/components/ui/tabs', () => ({
  Tabs: ({ children, value, onValueChange }: any) => (
    <div data-testid="tabs" data-value={value} data-onchange={onValueChange}>
      {children}
    </div>
  ),
  TabsContent: ({ children, value }: any) => (
    <div data-testid={`tab-content-${value}`}>{children}</div>
  ),
  TabsList: ({ children, className }: any) => (
    <div className={className} data-testid="tabs-list">{children}</div>
  ),
  TabsTrigger: ({ children, value, className }: any) => (
    <button data-testid={`tab-trigger-${value}`} className={className}>
      {children}
    </button>
  ),
}));

describe('BiomarkerDials', () => {
  const mockBiomarkers = {
    glucose: {
      value: 100,
      unit: 'mg/dL',
      date: '2024-01-01',
      referenceRange: {
        min: 70,
        max: 100,
        unit: 'mg/dL'
      },
      status: 'normal'
    },
    hba1c: {
      value: 5.5,
      unit: '%',
      date: '2024-01-01',
      referenceRange: {
        min: 4.0,
        max: 5.7,
        unit: '%'
      },
      status: 'optimal'
    },
    total_cholesterol: {
      value: 220,
      unit: 'mg/dL',
      date: '2024-01-01',
      referenceRange: {
        min: 200,
        max: 240,
        unit: 'mg/dL'
      },
      status: 'elevated'
    }
  };

  it('renders biomarker dials with correct data', () => {
    render(<BiomarkerDials biomarkers={mockBiomarkers} />);
    
    expect(screen.getByText('Biomarker Analysis')).toBeInTheDocument();
    expect(screen.getByText('Glucose')).toBeInTheDocument();
    expect(screen.getByText('HbA1c')).toBeInTheDocument();
    expect(screen.getByText('Total Cholesterol')).toBeInTheDocument();
  });

  it('shows correct biomarker values and units', () => {
    render(<BiomarkerDials biomarkers={mockBiomarkers} />);
    
    expect(screen.getByText('100.0')).toBeInTheDocument();
    expect(screen.getByText('mg/dL')).toBeInTheDocument();
    expect(screen.getByText('5.5')).toBeInTheDocument();
    expect(screen.getByText('%')).toBeInTheDocument();
  });

  it('displays status badges correctly', () => {
    render(<BiomarkerDials biomarkers={mockBiomarkers} />);
    
    expect(screen.getByText('Normal')).toBeInTheDocument();
    expect(screen.getByText('Optimal')).toBeInTheDocument();
    expect(screen.getByText('Elevated')).toBeInTheDocument();
  });

  it('shows reference ranges when showDetails is true', () => {
    render(<BiomarkerDials biomarkers={mockBiomarkers} showDetails={true} />);
    
    expect(screen.getByText('Range: 70-100 mg/dL')).toBeInTheDocument();
    expect(screen.getByText('Range: 4.0-5.7 %')).toBeInTheDocument();
  });

  it('groups biomarkers by category', () => {
    render(<BiomarkerDials biomarkers={mockBiomarkers} />);
    
    expect(screen.getByText('Metabolic Health')).toBeInTheDocument();
    expect(screen.getByText('Cardiovascular Health')).toBeInTheDocument();
  });

  it('allows expanding and collapsing categories', async () => {
    const user = userEvent.setup();
    render(<BiomarkerDials biomarkers={mockBiomarkers} />);
    
    // Initially categories should be collapsed
    expect(screen.queryByText('Glucose')).not.toBeInTheDocument();
    
    // Click to expand metabolic category
    const expandButton = screen.getByRole('button', { name: /chevron/i });
    await user.click(expandButton);
    
    // Should now show biomarkers
    expect(screen.getByText('Glucose')).toBeInTheDocument();
  });

  it('filters biomarkers by category', async () => {
    const user = userEvent.setup();
    render(<BiomarkerDials biomarkers={mockBiomarkers} />);
    
    // Click on cardiovascular tab
    const cardiovascularTab = screen.getByText('Cardiovascular Health');
    await user.click(cardiovascularTab);
    
    // Should only show cardiovascular biomarkers
    expect(screen.getByText('Total Cholesterol')).toBeInTheDocument();
    expect(screen.queryByText('Glucose')).not.toBeInTheDocument();
  });

  it('shows empty state when no biomarkers provided', () => {
    render(<BiomarkerDials biomarkers={{}} />);
    
    expect(screen.getByText('No biomarker data available.')).toBeInTheDocument();
    expect(screen.getByText('Complete an analysis to view your biomarker results.')).toBeInTheDocument();
  });

  it('renders dials with correct values', () => {
    render(<BiomarkerDials biomarkers={mockBiomarkers} />);
    
    // Check that dial elements are rendered (they would be SVG circles)
    const svgElements = screen.getAllByRole('img', { hidden: true });
    expect(svgElements.length).toBeGreaterThan(0);
  });

  it('shows date information when available', () => {
    render(<BiomarkerDials biomarkers={mockBiomarkers} showDetails={true} />);
    
    expect(screen.getByText('1/1/2024')).toBeInTheDocument();
  });

  it('handles biomarkers without reference ranges', () => {
    const biomarkersWithoutRanges = {
      glucose: {
        value: 100,
        unit: 'mg/dL',
        status: 'normal'
      }
    };
    
    render(<BiomarkerDials biomarkers={biomarkersWithoutRanges} />);
    
    expect(screen.getByText('Glucose')).toBeInTheDocument();
    expect(screen.getByText('100.0')).toBeInTheDocument();
  });

  it('shows progress bars in details view', () => {
    render(<BiomarkerDials biomarkers={mockBiomarkers} showDetails={true} />);
    
    // Should show progress bars for reference ranges
    const progressBars = screen.getAllByRole('progressbar', { hidden: true });
    expect(progressBars.length).toBeGreaterThan(0);
  });

  it('calculates dial values correctly based on reference ranges', () => {
    render(<BiomarkerDials biomarkers={mockBiomarkers} />);
    
    // Glucose is at the upper limit (100 out of 70-100 range)
    // This should result in a dial value close to 100
    const glucoseValue = screen.getByText('100.0');
    expect(glucoseValue).toBeInTheDocument();
  });

  it('handles different status types correctly', () => {
    const biomarkersWithDifferentStatuses = {
      optimal: { value: 5.0, unit: '%', status: 'optimal' as const },
      normal: { value: 5.5, unit: '%', status: 'normal' as const },
      elevated: { value: 6.5, unit: '%', status: 'elevated' as const },
      low: { value: 3.5, unit: '%', status: 'low' as const },
      critical: { value: 8.0, unit: '%', status: 'critical' as const }
    };
    
    render(<BiomarkerDials biomarkers={biomarkersWithDifferentStatuses} />);
    
    expect(screen.getByText('Optimal')).toBeInTheDocument();
    expect(screen.getByText('Normal')).toBeInTheDocument();
    expect(screen.getByText('Elevated')).toBeInTheDocument();
    expect(screen.getByText('Low')).toBeInTheDocument();
    expect(screen.getByText('Critical')).toBeInTheDocument();
  });

  it('should render biomarkers from backend API response format', () => {
    const backendBiomarkers = {
      glucose: {
        value: 95.0,
        unit: 'mg/dL',
        status: 'normal',
        referenceRange: {
          min: 70,
          max: 100,
          unit: 'mg/dL'
        },
        date: '2024-01-01'
      },
      total_cholesterol: {
        value: 180.0,
        unit: 'mg/dL',
        status: 'optimal',
        referenceRange: {
          min: 150,
          max: 200,
          unit: 'mg/dL'
        },
        date: '2024-01-01'
      }
    };

    render(<BiomarkerDials biomarkers={backendBiomarkers} showDetails={false} />);
    
    // Should not show "No biomarker data available"
    expect(screen.queryByText('No biomarker data available.')).not.toBeInTheDocument();
    
    // Should show biomarker names
    expect(screen.getByText('Glucose')).toBeInTheDocument();
    expect(screen.getByText('Total Cholesterol')).toBeInTheDocument();
    
    // Should show values
    expect(screen.getByText('95.0')).toBeInTheDocument();
    expect(screen.getByText('180.0')).toBeInTheDocument();
    
    // Should show status badges
    expect(screen.getByText('Normal')).toBeInTheDocument();
    expect(screen.getByText('Optimal')).toBeInTheDocument();
  });
});
