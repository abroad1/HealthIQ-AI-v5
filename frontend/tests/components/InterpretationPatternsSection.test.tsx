import React from 'react';
import { render, screen } from '@testing-library/react';
import {
  InterpretationPatternsSection,
  selectVisibleIdlRecords,
} from '@/components/results/InterpretationPatternsSection';
import type { InterpretationDisplayLayerBundleV1 } from '@/types/analysis';

jest.mock('@/components/ui/card', () => ({
  Card: ({ children, className, ...props }: any) => (
    <div className={className} data-testid="idl-card" {...props}>
      {children}
    </div>
  ),
  CardContent: ({ children, className }: any) => <div className={className}>{children}</div>,
  CardDescription: ({ children, className }: any) => <div className={className}>{children}</div>,
  CardHeader: ({ children, className }: any) => <div className={className}>{children}</div>,
  CardTitle: ({ children, className }: any) => <h3 className={className}>{children}</h3>,
}));

jest.mock('@/components/ui/badge', () => ({
  Badge: ({ children, className }: any) => <span className={className}>{children}</span>,
}));

const baseRecord = {
  internal_id: 'ph_test_a_v1',
  scientific_class: 'organ_pattern' as const,
  clinical_display_label: 'Clinical A',
  retail_display_label: 'Retail A',
  subtitle: 'Subtitle A',
  why_it_matters: 'Why A',
  severity_state: 'attention' as const,
  supporting_biomarkers_summary: 'Markers A',
  frontend_allowed_term: 'clinical_only' as const,
  display_order_priority: 2,
  enabled_for_frontend: true,
};

function makeBundle(overrides?: Partial<InterpretationDisplayLayerBundleV1>): InterpretationDisplayLayerBundleV1 {
  return {
    schema_version: '1.0.0',
    records: [
      {
        ...baseRecord,
        internal_id: 'ph_second_v1',
        retail_display_label: 'Second card',
        subtitle: 'Sub 2',
        why_it_matters: 'Why 2',
        supporting_biomarkers_summary: 'M2',
        display_order_priority: 10,
        enabled_for_frontend: false,
      },
      {
        ...baseRecord,
        internal_id: 'ph_first_v1',
        retail_display_label: 'First card',
        subtitle: 'Sub 1',
        why_it_matters: 'Why 1',
        supporting_biomarkers_summary: 'M1',
        display_order_priority: 1,
        enabled_for_frontend: true,
      },
      {
        ...baseRecord,
        internal_id: 'ph_third_v1',
        retail_display_label: 'Third card',
        display_order_priority: 3,
        enabled_for_frontend: true,
      },
    ],
    ...overrides,
  };
}

describe('selectVisibleIdlRecords', () => {
  it('filters to enabled_for_frontend and sorts by display_order_priority', () => {
    const bundle = makeBundle();
    const vis = selectVisibleIdlRecords(bundle);
    expect(vis).toHaveLength(2);
    expect(vis[0].retail_display_label).toBe('First card');
    expect(vis[1].retail_display_label).toBe('Third card');
  });

  it('returns empty for missing bundle', () => {
    expect(selectVisibleIdlRecords(undefined)).toEqual([]);
    expect(selectVisibleIdlRecords(null)).toEqual([]);
  });
});

describe('InterpretationPatternsSection', () => {
  it('renders nothing when no qualifying records', () => {
    const { container } = render(
      <InterpretationPatternsSection
        bundle={{ schema_version: '1.0.0', records: [{ ...baseRecord, enabled_for_frontend: false }] }}
      />
    );
    expect(container.firstChild).toBeNull();
  });

  it('renders section heading and IDL fields for visible cards', () => {
    const bundle = makeBundle();
    render(<InterpretationPatternsSection bundle={bundle} />);
    expect(screen.getByRole('heading', { name: /patterns across your body/i })).toBeInTheDocument();
    expect(screen.getByText('First card')).toBeInTheDocument();
    expect(screen.getByText('Third card')).toBeInTheDocument();
    expect(screen.queryByText('Second card')).not.toBeInTheDocument();
    expect(screen.getByText('Why 1')).toBeInTheDocument();
    expect(screen.getByText('M1')).toBeInTheDocument();
    // internal ids must not be surfaced
    expect(screen.queryByText(/ph_first_v1/)).not.toBeInTheDocument();
    expect(screen.queryByText(/phenotype/i)).not.toBeInTheDocument();
  });
});
