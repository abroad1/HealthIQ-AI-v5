import {
  analysisBiomarkerKey,
  buildReferenceRangeFromParserRow,
  formatReferenceRangeDisplay,
  rangeAttentionLevel,
  referenceRangeToPayload,
} from '@/lib/uploadReferenceRange';

describe('buildReferenceRangeFromParserRow', () => {
  it('preserves one-sided ref_high only', () => {
    const out = buildReferenceRangeFromParserRow({
      unit: 'mg/dL',
      ref_low: null,
      ref_high: 100,
      value: 80,
    });
    expect(out.referenceRange).toEqual({ min: undefined, max: 100, unit: 'mg/dL' });
  });

  it('preserves one-sided ref_low only', () => {
    const out = buildReferenceRangeFromParserRow({
      unit: '%',
      ref_low: 4.0,
      ref_high: null,
      value: 5.2,
    });
    expect(out.referenceRange).toEqual({ min: 4, max: undefined, unit: '%' });
  });

  it('merges raw reference string when present', () => {
    const out = buildReferenceRangeFromParserRow({
      unit: 'mmol/L',
      reference: '3.5–5.5',
      ref_low: null,
      ref_high: null,
    });
    expect(out.referenceText).toContain('3.5');
    expect(out.referenceRange).toBeUndefined();
  });
});

describe('referenceRangeToPayload', () => {
  it('returns null when no bounds', () => {
    expect(referenceRangeToPayload(undefined)).toBeNull();
    expect(referenceRangeToPayload({ unit: 'mg/dL' } as any)).toBeNull();
  });

  it('serializes nullable sides for backend', () => {
    expect(referenceRangeToPayload({ min: 40, unit: 'mg/dL' })).toEqual({
      min: 40,
      max: null,
      unit: 'mg/dL',
      source: 'lab',
    });
  });
});

describe('rangeAttentionLevel', () => {
  it('flags missing when no bounds and no text', () => {
    expect(rangeAttentionLevel({ unit: 'mg/dL' })).toBe('missing');
  });

  it('none when both bounds', () => {
    expect(
      rangeAttentionLevel({
        unit: 'mg/dL',
        referenceRange: { min: 0, max: 100, unit: 'mg/dL' },
      })
    ).toBe('none');
  });

  it('partial for one-sided', () => {
    expect(
      rangeAttentionLevel({
        unit: 'mg/dL',
        referenceRange: { max: 100, unit: 'mg/dL' },
      })
    ).toBe('partial');
  });
});

describe('analysisBiomarkerKey', () => {
  it('maps apolipoprotein venous slug variants to canonical apob_apoa1_ratio', () => {
    expect(analysisBiomarkerKey('Apolipoprotein ratio (Venous)')).toBe('apob_apoa1_ratio');
    expect(analysisBiomarkerKey('apolipoprotein_ratio_venous')).toBe('apob_apoa1_ratio');
  });
});

describe('formatReferenceRangeDisplay', () => {
  it('formats one-sided max', () => {
    expect(
      formatReferenceRangeDisplay({
        referenceRange: { max: 5.6, unit: '%' },
      })
    ).toMatch(/≤ 5\.6/);
  });
});
