import {
  analysisBiomarkerKey,
  stripAbnormalLabMarkerSuffix,
  buildReferenceRangeFromParserRow,
  deriveReviewReferenceType,
  formatReferenceRangeDisplay,
  inferComparatorFromSnippet,
  matchLabelledBandFromValue,
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
    expect(out.referenceRange).toEqual({
      min: undefined,
      max: 100,
      unit: 'mg/dL',
      upperComparator: '≤',
    });
  });

  it('preserves one-sided ref_low only', () => {
    const out = buildReferenceRangeFromParserRow({
      unit: '%',
      ref_low: 4.0,
      ref_high: null,
      value: 5.2,
    });
    expect(out.referenceRange).toEqual({
      min: 4,
      max: undefined,
      unit: '%',
      lowerComparator: '≥',
    });
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

  it('no-lab-range-supplied when referenceType says so', () => {
    expect(
      rangeAttentionLevel({
        unit: 'ratio',
        referenceType: 'no_lab_range_supplied',
      })
    ).toBe('no-lab-range-supplied');
  });

  it('incomplete-or-ambiguous when referenceType says so', () => {
    expect(
      rangeAttentionLevel({
        unit: 'U/L',
        referenceType: 'incomplete_or_ambiguous',
        referenceText: 'unclear',
      })
    ).toBe('incomplete-or-ambiguous');
  });

  it('labelled-bands-resolved when matched label present', () => {
    expect(
      rangeAttentionLevel({
        unit: 'ng/mL',
        referenceType: 'labelled_bands',
        matchedLabelledBand: 'Normal',
        referenceRange: { min: 3, max: 5, unit: 'ng/mL' },
      })
    ).toBe('labelled-bands-resolved');
  });
});

describe('deriveReviewReferenceType', () => {
  it('infers bounded_range from two-sided numeric range', () => {
    expect(
      deriveReviewReferenceType(undefined, {
        referenceRange: { min: 1, max: 10, unit: 'mg/dL' },
      })
    ).toBe('bounded_range');
  });

  it('infers labelled_bands when bands present without parser type', () => {
    expect(
      deriveReviewReferenceType(undefined, {
        labelledBands: [{ bandLabel: 'A', min: 0, max: 1, unit: 'x' }],
      })
    ).toBe('labelled_bands');
  });
});

describe('matchLabelledBandFromValue', () => {
  it('matches inclusive closed band', () => {
    const b = matchLabelledBandFromValue(3.5, [
      { bandLabel: 'Low', min: 0, max: 3.37, unit: 'ng/mL' },
      { bandLabel: 'Mid', min: 3.38, max: 5.38, unit: 'ng/mL' },
    ]);
    expect(b?.bandLabel).toBe('Mid');
  });
});

describe('inferComparatorFromSnippet', () => {
  it('reads strict upper comparator from band snippet', () => {
    expect(inferComparatorFromSnippet('Normal < 39', 'upper')).toBe('<');
    expect(inferComparatorFromSnippet('Normal ≤ 39', 'upper')).toBe('≤');
  });
});

describe('buildReferenceRangeFromParserRow no-range heuristic', () => {
  it('infers no_lab_range_supplied when there is no range text or structure', () => {
    const out = buildReferenceRangeFromParserRow({
      unit: '%',
      value: 42.1,
      ref_low: null,
      ref_high: null,
    });
    expect(out.referenceType).toBe('no_lab_range_supplied');
  });

  it('does not override incomplete_or_ambiguous', () => {
    const out = buildReferenceRangeFromParserRow({
      unit: 'U/L',
      value: 50,
      referenceType: 'incomplete_or_ambiguous',
      ref_low: null,
      ref_high: null,
    });
    expect(out.referenceType).toBe('incomplete_or_ambiguous');
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

  it('strips trailing star abnormal markers before key normalisation (MAP-R1A)', () => {
    expect(analysisBiomarkerKey('Homocysteine (venous)*')).toBe('homocysteine_(venous)');
    expect(analysisBiomarkerKey('Apolipoprotein B (venous)*')).toBe('apolipoprotein_b_(venous)');
    expect(analysisBiomarkerKey('Apolipoprotein A1 (venous)*')).toBe('apolipoprotein_a1_(venous)');
    expect(analysisBiomarkerKey('Lipoprotein (a) (venous)*')).toBe('lipoprotein_(a)_(venous)');
    expect(analysisBiomarkerKey('Corrected Calcium (venous)*')).toBe('corrected_calcium_(venous)');
  });

  it('leaves clean labels unchanged aside from normal slugs', () => {
    expect(analysisBiomarkerKey('Homocysteine (venous)')).toBe('homocysteine_(venous)');
    expect(analysisBiomarkerKey('Creatinine (venous)')).toBe('creatinine_(venous)');
  });
});

describe('stripAbnormalLabMarkerSuffix', () => {
  it('removes trailing star and dagger markers', () => {
    expect(stripAbnormalLabMarkerSuffix('Homocysteine (venous)*')).toBe('Homocysteine (venous)');
    expect(stripAbnormalLabMarkerSuffix('TSH (venous)†')).toBe('TSH (venous)');
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

  it('shows matched interpretive label in parentheses without em dash separator', () => {
    const s = formatReferenceRangeDisplay({
      referenceRange: { max: 39, unit: 'pg/mL', upperComparator: '<' },
      matchedLabelledBand: 'Normal',
    });
    expect(s).toContain('< 39');
    expect(s).toContain('(Normal)');
    expect(s).not.toMatch(/\s—\sNormal/);
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
