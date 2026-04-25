import {
  biomarkerTrendKey,
  buildBiomarkerTrendRows,
  sortCompletedHistoryNewestFirst,
  topMovementRows,
} from '@/lib/trendComparison';
import type { AnalysisHistoryItem, AnalysisResult } from '@/types/analysis';

function resultWithBiomarkers(
  biomarkers: AnalysisResult['biomarkers'],
  id = 'a1'
): AnalysisResult {
  return {
    analysis_id: id,
    biomarkers,
    clusters: [],
    insights: [],
    overall_score: null,
    status: 'completed',
  };
}

describe('trendComparison', () => {
  it('biomarkerTrendKey normalizes', () => {
    expect(biomarkerTrendKey('  LDL Cholesterol ')).toBe('ldl cholesterol');
  });

  it('sortCompletedHistoryNewestFirst keeps only completed and orders by date', () => {
    const items: AnalysisHistoryItem[] = [
      { id: 'old', created_at: '2024-01-01T00:00:00Z', status: 'completed', overall_score: 0.5 },
      { id: 'mid', created_at: '2024-06-01T00:00:00Z', status: 'failed', overall_score: null },
      { id: 'new', created_at: '2025-01-01T00:00:00Z', status: 'completed', overall_score: 0.6 },
    ];
    const sorted = sortCompletedHistoryNewestFirst(items);
    expect(sorted.map((x) => x.id)).toEqual(['new', 'old']);
  });

  it('buildBiomarkerTrendRows sorts by absolute delta descending', () => {
    const recent = resultWithBiomarkers(
      [
        {
          biomarker_name: 'Glucose',
          value: 5.2,
          unit: 'mmol/L',
          status: 'normal',
        },
        {
          biomarker_name: 'Ferritin',
          value: 100,
          unit: 'µg/L',
          status: 'high',
        },
      ],
      'r1'
    );
    const previous = resultWithBiomarkers(
      [
        {
          biomarker_name: 'Glucose',
          value: 5.0,
          unit: 'mmol/L',
          status: 'normal',
        },
        {
          biomarker_name: 'Ferritin',
          value: 40,
          unit: 'µg/L',
          status: 'low',
        },
      ],
      'r0'
    );
    const rows = buildBiomarkerTrendRows(recent, previous);
    expect(rows[0].biomarkerName).toBe('Ferritin');
    expect(rows[0].deltaDisplay).toMatch(/^\+60/);
    expect(rows[0].arrow).toBe('up');
    expect(rows[1].biomarkerName).toBe('Glucose');
    expect(rows[1].arrow).toBe('up');
    expect(rows[1].hasComparableDelta).toBe(true);
  });

  it('handles marker only in previous run', () => {
    const recent = resultWithBiomarkers(
      [{ biomarker_name: 'A', value: 1, unit: 'u', status: 'normal' }],
      'r1'
    );
    const previous = resultWithBiomarkers(
      [
        { biomarker_name: 'A', value: 2, unit: 'u', status: 'normal' },
        { biomarker_name: 'B', value: 3, unit: 'u', status: 'low' },
      ],
      'r0'
    );
    const rows = buildBiomarkerTrendRows(recent, previous);
    const b = rows.find((r) => r.biomarkerName === 'B');
    expect(b).toBeDefined();
    expect(b!.recentDisplay).toBe('—');
    expect(b!.previousDisplay).toBe('3 u');
    expect(b!.rangeStatusLabel).toBe('—');
    expect(b!.hasComparableDelta).toBe(false);
  });

  it('topMovementRows returns up to n comparable rows', () => {
    const recent = resultWithBiomarkers(
      [
        { biomarker_name: 'X', value: 10, unit: '', status: null },
        { biomarker_name: 'Y', value: 1, unit: '', status: null },
      ],
      'r1'
    );
    const previous = resultWithBiomarkers(
      [
        { biomarker_name: 'X', value: 7, unit: '', status: null },
        { biomarker_name: 'Y', value: 0, unit: '', status: null },
      ],
      'r0'
    );
    const rows = buildBiomarkerTrendRows(recent, previous);
    const top = topMovementRows(rows, 1);
    expect(top).toHaveLength(1);
    expect(top[0].biomarkerName).toBe('X');
  });
});
