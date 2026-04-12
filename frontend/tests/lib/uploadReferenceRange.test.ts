import {
  analysisBiomarkerKey,
  buildReferenceRangeFromParserRow,
  formatReferenceRangeDisplay,
  numericPartForAnalysisPayload,
  parseBiomarkerValueForReview,
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

  it('returns multiple contextRangeOptions without numeric range when parser omits bounds', () => {
    const out = buildReferenceRangeFromParserRow({
      unit: 'mIU/L',
      ref_low: null,
      ref_high: null,
      rawReferenceText: 'Males: 2–18\nFemales: 2–29',
      contextRangeOptions: [
        { contextLabel: 'Male', min: 2, max: 18, unit: 'mIU/L', sourceSnippet: 'Males: 2–18' },
        { contextLabel: 'Female', min: 2, max: 29, unit: 'mIU/L', sourceSnippet: 'Females: 2–29' },
      ],
    });
    expect(out.contextRangeOptions).toHaveLength(2);
    expect(out.referenceRange).toBeUndefined();
    expect(out.referenceText).toMatch(/Males/);
  });

  it('auto-fills reference range from a single context option when bounds exist', () => {
    const out = buildReferenceRangeFromParserRow({
      unit: 'mIU/L',
      ref_low: null,
      ref_high: null,
      contextRangeOptions: [{ contextLabel: 'Adult', min: 2, max: 18, unit: 'mIU/L' }],
    });
    expect(out.referenceRange).toEqual({ min: 2, max: 18, unit: 'mIU/L' });
    expect(out.contextRangeOptions).toHaveLength(1);
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

  it('one-sided when only max bound', () => {
    expect(
      rangeAttentionLevel({
        unit: 'mg/dL',
        referenceRange: { max: 100, unit: 'mg/dL' },
      })
    ).toBe('one-sided');
  });

  it('one-sided when only min bound', () => {
    expect(
      rangeAttentionLevel({
        unit: 'mg/dL',
        referenceRange: { min: 40, unit: 'mg/dL' },
      })
    ).toBe('one-sided');
  });

  it('partial when only contextual text and no numeric bounds', () => {
    expect(
      rangeAttentionLevel({
        unit: 'mg/dL',
        referenceText: 'See pregnancy table on page 2',
      })
    ).toBe('partial');
  });

  it('context-selection-required when multiple bands and no numeric bounds yet', () => {
    expect(
      rangeAttentionLevel({
        unit: 'mIU/L',
        referenceText: 'Males / Females',
        contextRangeOptions: [
          { contextLabel: 'Male', min: 2, max: 18, unit: 'mIU/L' },
          { contextLabel: 'Female', min: 2, max: 29, unit: 'mIU/L' },
        ],
      })
    ).toBe('context-selection-required');
  });

  it('clears context-selection-required once any bound is set', () => {
    expect(
      rangeAttentionLevel({
        unit: 'mIU/L',
        referenceRange: { min: 2, unit: 'mIU/L' },
        contextRangeOptions: [
          { contextLabel: 'Male', min: 2, max: 18, unit: 'mIU/L' },
          { contextLabel: 'Female', min: 2, max: 29, unit: 'mIU/L' },
        ],
      })
    ).toBe('one-sided');
  });
});

describe('buildReferenceRangeFromParserRow rawReferenceText', () => {
  it('prepends rawReferenceText before referenceRange string', () => {
    const out = buildReferenceRangeFromParserRow({
      unit: 'mIU/L',
      rawReferenceText: 'Males: 2–18\nFemales: 2–29',
      referenceRange: '< 25',
      ref_low: null,
      ref_high: 25,
    });
    expect(out.referenceText).toMatch(/Males: 2–18/);
    expect(out.referenceText).toMatch(/< 25/);
    expect(out.referenceRange?.max).toBe(25);
  });
});

describe('analysisBiomarkerKey', () => {
  it('maps apolipoprotein venous slug variants to canonical apob_apoa1_ratio', () => {
    expect(analysisBiomarkerKey('Apolipoprotein ratio (Venous)')).toBe('apob_apoa1_ratio');
    expect(analysisBiomarkerKey('apolipoprotein_ratio_venous')).toBe('apob_apoa1_ratio');
  });
});

describe('formatReferenceRangeDisplay', () => {
  it('formats one-sided max with ≤ when reference text does not show strict bound', () => {
    expect(
      formatReferenceRangeDisplay({
        referenceRange: { max: 5.6, unit: '%' },
      })
    ).toMatch(/≤ 5\.6/);
  });

  it('uses < when reference text shows strict upper bound before the number', () => {
    expect(
      formatReferenceRangeDisplay({
        referenceRange: { max: 200, unit: 'mg/dL' },
        referenceText: 'Reference interval: < 200 mg/dL',
      })
    ).toBe('< 200 mg/dL');
  });

  it('preserves multi-line reference text when no numeric bounds', () => {
    const multi = 'Line 1\nLine 2\nSee footnote';
    expect(
      formatReferenceRangeDisplay({
        referenceText: multi,
      })
    ).toBe(multi);
  });
});

describe('parseBiomarkerValueForReview', () => {
  it('accepts plain numbers', () => {
    const p = parseBiomarkerValueForReview('5.2');
    expect(p.ok && p.display).toBe(5.2);
    expect(p.ok && p.numericForPayload).toBe(5.2);
  });

  it('accepts inequality-prefixed values and keeps display string', () => {
    const p = parseBiomarkerValueForReview('<0.05');
    expect(p.ok).toBe(true);
    if (p.ok) {
      expect(p.display).toBe('<0.05');
      expect(p.numericForPayload).toBe(0.05);
    }
  });

  it('rejects garbage', () => {
    const p = parseBiomarkerValueForReview('not a value');
    expect(p.ok).toBe(false);
  });
});

describe('numericPartForAnalysisPayload', () => {
  it('extracts numeric part from inequality string', () => {
    expect(numericPartForAnalysisPayload('< 12.5')).toBe(12.5);
  });

  it('passes through finite numbers', () => {
    expect(numericPartForAnalysisPayload(4)).toBe(4);
  });
});
