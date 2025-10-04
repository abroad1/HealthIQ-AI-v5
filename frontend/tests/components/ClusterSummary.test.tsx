import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import ClusterSummary from '../../app/components/clusters/ClusterSummary';

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
  Button: ({ children, onClick, disabled, className }: any) => (
    <button onClick={onClick} disabled={disabled} className={className}>{children}</button>
  ),
}));

jest.mock('@/components/ui/alert', () => ({
  Alert: ({ children, className }: any) => <div className={className}>{children}</div>,
  AlertDescription: ({ children, className }: any) => <div className={className}>{children}</div>,
}));

const mockClusters = [
  {
    id: 'metabolic-1',
    name: 'Metabolic Health Cluster',
    category: 'metabolic',
    score: 75,
    confidence: 0.85,
    biomarkers: ['glucose', 'hba1c', 'insulin'],
    description: 'Your metabolic health shows good overall patterns with some areas for improvement.',
    recommendations: [
      'Increase physical activity to at least 150 minutes per week',
      'Consider reducing refined carbohydrate intake'
    ],
    severity: 'moderate' as const,
    trend: 'improving' as const
  },
  {
    id: 'cardiovascular-1',
    name: 'Cardiovascular Risk Cluster',
    category: 'cardiovascular',
    score: 45,
    confidence: 0.92,
    biomarkers: ['total_cholesterol', 'ldl_cholesterol', 'hdl_cholesterol'],
    description: 'Elevated cardiovascular risk factors detected requiring attention.',
    recommendations: [
      'Focus on heart-healthy diet with reduced saturated fats',
      'Consider discussing statin therapy with your healthcare provider'
    ],
    severity: 'high' as const,
    trend: 'stable' as const
  },
  {
    id: 'inflammatory-1',
    name: 'Inflammatory Markers Cluster',
    category: 'inflammatory',
    score: 60,
    confidence: 0.78,
    biomarkers: ['crp', 'esr'],
    description: 'Mild inflammatory markers present, likely lifestyle-related.',
    recommendations: [
      'Implement stress management techniques',
      'Improve sleep quality and duration'
    ],
    severity: 'low' as const,
    trend: 'declining' as const
  }
];

describe('ClusterSummary', () => {
  it('renders cluster summary with correct data', () => {
    render(<ClusterSummary clusters={mockClusters} />);
    
    expect(screen.getByText('Metabolic Health Cluster')).toBeInTheDocument();
    expect(screen.getByText('Cardiovascular Risk Cluster')).toBeInTheDocument();
    expect(screen.getByText('Inflammatory Markers Cluster')).toBeInTheDocument();
  });

  it('shows summary statistics', () => {
    render(<ClusterSummary clusters={mockClusters} />);
    
    expect(screen.getByText('3')).toBeInTheDocument(); // Total clusters
    expect(screen.getByText('60')).toBeInTheDocument(); // Average score
    expect(screen.getByText('1')).toBeInTheDocument(); // Critical issues
    expect(screen.getByText('1')).toBeInTheDocument(); // High priority
  });

  it('displays cluster scores and confidence levels', () => {
    render(<ClusterSummary clusters={mockClusters} />);
    
    expect(screen.getByText('75/100')).toBeInTheDocument();
    expect(screen.getByText('45/100')).toBeInTheDocument();
    expect(screen.getByText('60/100')).toBeInTheDocument();
    expect(screen.getByText('85%')).toBeInTheDocument();
    expect(screen.getByText('92%')).toBeInTheDocument();
    expect(screen.getByText('78%')).toBeInTheDocument();
  });

  it('shows severity badges correctly', () => {
    render(<ClusterSummary clusters={mockClusters} />);
    
    expect(screen.getByText('Moderate')).toBeInTheDocument();
    expect(screen.getByText('High')).toBeInTheDocument();
    expect(screen.getByText('Low')).toBeInTheDocument();
  });

  it('displays trend indicators', () => {
    render(<ClusterSummary clusters={mockClusters} />);
    
    expect(screen.getByText('Improving')).toBeInTheDocument();
    expect(screen.getByText('Stable')).toBeInTheDocument();
    expect(screen.getByText('Declining')).toBeInTheDocument();
  });

  it('allows expanding cluster details', async () => {
    const user = userEvent.setup();
    render(<ClusterSummary clusters={mockClusters} />);
    
    // Initially details should be hidden
    expect(screen.queryByText('Biomarkers Analyzed')).not.toBeInTheDocument();
    
    // Click to expand first cluster
    const expandButtons = screen.getAllByRole('button', { name: /chevron/i });
    await user.click(expandButtons[0]);
    
    // Should now show details
    expect(screen.getByText('Biomarkers Analyzed')).toBeInTheDocument();
    expect(screen.getByText('Recommendations')).toBeInTheDocument();
  });

  it('shows biomarker list when expanded', async () => {
    const user = userEvent.setup();
    render(<ClusterSummary clusters={mockClusters} />);
    
    const expandButtons = screen.getAllByRole('button', { name: /chevron/i });
    await user.click(expandButtons[0]);
    
    expect(screen.getByText('Glucose')).toBeInTheDocument();
    expect(screen.getByText('HbA1c')).toBeInTheDocument();
    expect(screen.getByText('Insulin')).toBeInTheDocument();
  });

  it('shows recommendations when expanded', async () => {
    const user = userEvent.setup();
    render(<ClusterSummary clusters={mockClusters} />);
    
    const expandButtons = screen.getAllByRole('button', { name: /chevron/i });
    await user.click(expandButtons[0]);
    
    expect(screen.getByText('Increase physical activity to at least 150 minutes per week')).toBeInTheDocument();
    expect(screen.getByText('Consider reducing refined carbohydrate intake')).toBeInTheDocument();
  });

  it('filters clusters by severity', async () => {
    const user = userEvent.setup();
    render(<ClusterSummary clusters={mockClusters} />);
    
    // Click on high severity filter
    const highFilter = screen.getByText('High (1)');
    await user.click(highFilter);
    
    // Should only show high severity clusters
    expect(screen.getByText('Cardiovascular Risk Cluster')).toBeInTheDocument();
    expect(screen.queryByText('Metabolic Health Cluster')).not.toBeInTheDocument();
    expect(screen.queryByText('Inflammatory Markers Cluster')).not.toBeInTheDocument();
  });

  it('shows all clusters when "All" filter is selected', async () => {
    const user = userEvent.setup();
    render(<ClusterSummary clusters={mockClusters} />);
    
    // First filter by high severity
    const highFilter = screen.getByText('High (1)');
    await user.click(highFilter);
    
    // Then click "All" to show all clusters
    const allFilter = screen.getByText('All (3)');
    await user.click(allFilter);
    
    // Should show all clusters again
    expect(screen.getByText('Metabolic Health Cluster')).toBeInTheDocument();
    expect(screen.getByText('Cardiovascular Risk Cluster')).toBeInTheDocument();
    expect(screen.getByText('Inflammatory Markers Cluster')).toBeInTheDocument();
  });

  it('shows empty state when no clusters match filter', async () => {
    const user = userEvent.setup();
    render(<ClusterSummary clusters={mockClusters} />);
    
    // Filter by critical severity (none exist)
    const criticalFilter = screen.getByText('Critical (0)');
    await user.click(criticalFilter);
    
    expect(screen.getByText('No clusters found for the selected severity level.')).toBeInTheDocument();
    expect(screen.getByText('Show All Clusters')).toBeInTheDocument();
  });

  it('shows loading state', () => {
    render(<ClusterSummary clusters={[]} isLoading={true} />);
    
    expect(screen.getByText('Loading health clusters...')).toBeInTheDocument();
  });

  it('shows empty state when no clusters provided', () => {
    render(<ClusterSummary clusters={[]} />);
    
    expect(screen.getByText('No health clusters available.')).toBeInTheDocument();
    expect(screen.getByText('Complete an analysis to view your health cluster analysis.')).toBeInTheDocument();
  });

  it('shows category information when expanded', async () => {
    const user = userEvent.setup();
    render(<ClusterSummary clusters={mockClusters} />);
    
    const expandButtons = screen.getAllByRole('button', { name: /chevron/i });
    await user.click(expandButtons[0]);
    
    expect(screen.getByText('Category')).toBeInTheDocument();
    expect(screen.getByText('Metabolic')).toBeInTheDocument();
  });

  it('displays progress bars for cluster scores', () => {
    render(<ClusterSummary clusters={mockClusters} />);
    
    // Should have progress bars for each cluster
    const progressBars = screen.getAllByRole('progressbar', { hidden: true });
    expect(progressBars.length).toBeGreaterThan(0);
  });

  it('handles clusters without recommendations', () => {
    const clustersWithoutRecommendations = [
      {
        ...mockClusters[0],
        recommendations: []
      }
    ];
    
    render(<ClusterSummary clusters={clustersWithoutRecommendations} />);
    
    expect(screen.getByText('Metabolic Health Cluster')).toBeInTheDocument();
  });

  it('handles clusters without trend information', () => {
    const clustersWithoutTrend = [
      {
        ...mockClusters[0],
        trend: undefined
      }
    ];
    
    render(<ClusterSummary clusters={clustersWithoutTrend} />);
    
    expect(screen.getByText('Metabolic Health Cluster')).toBeInTheDocument();
  });

  it('shows correct biomarker count for each cluster', () => {
    render(<ClusterSummary clusters={mockClusters} />);
    
    expect(screen.getByText('3')).toBeInTheDocument(); // Metabolic cluster has 3 biomarkers
    expect(screen.getByText('3')).toBeInTheDocument(); // Cardiovascular cluster has 3 biomarkers
    expect(screen.getByText('2')).toBeInTheDocument(); // Inflammatory cluster has 2 biomarkers
  });
});
