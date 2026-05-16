import {
  buildUploadedPanelFidelityRows,
  normalizeUnitToken,
} from '../../app/lib/uploadPanelFidelity';
import type { BiomarkerResult } from '../../app/types/analysis';

const canonical: BiomarkerResult[] = [
  { biomarker_name: 'hba1c', value: 42, unit: 'mmol/mol' },
  { biomarker_name: 'hematocrit', value: 0.438, unit: 'L/L' },
  { biomarker_name: 'platelets', value: 225, unit: '10^9/L' },
  { biomarker_name: 'white_blood_cells', value: 6.4, unit: '10^9/L' },
  { biomarker_name: 'sodium', value: 140, unit: 'mmol/L' },
];

describe('uploadPanelFidelity', () => {
  it('normalizes unit tokens for comparison only', () => {
    expect(normalizeUnitToken('K/uL')).toBe('k/ul');
    expect(normalizeUnitToken('mEq/L')).toBe('meq/l');
    expect(normalizeUnitToken('10^9/L')).toBe('10^9/l');
  });

  it('includes equivalent hba1c_pct and unit-mismatch rows', () => {
    const upload = {
      hba1c: { value: 42, unit: 'mmol/mol' },
      hba1c_pct: { value: 6, unit: '%' },
      hematocrit: { value: 43.8, unit: '%' },
      platelets: { value: 225, unit: 'K/uL' },
      white_blood_cells: { value: 6.4, unit: 'K/uL' },
      sodium: { value: 140, unit: 'mEq/L' },
    };

    const rows = buildUploadedPanelFidelityRows(upload, {}, canonical);
    const keys = rows.map((r) => r.observationKey);

    expect(keys).toContain('hba1c_pct');
    expect(keys).toContain('hematocrit');
    expect(keys).toContain('platelets');
    expect(keys).toContain('white_blood_cells');
    expect(keys).toContain('sodium');
    expect(keys).not.toContain('hba1c');

    const hba1cPct = rows.find((r) => r.observationKey === 'hba1c_pct');
    expect(hba1cPct?.isEquivalentObservation).toBe(true);
    expect(hba1cPct?.linkedCanonicalId).toBe('hba1c');
    expect(hba1cPct?.value).toBe(6);
    expect(hba1cPct?.unit).toBe('%');
  });

  it('returns empty when upload panel is absent', () => {
    expect(buildUploadedPanelFidelityRows(undefined, {}, canonical)).toEqual([]);
  });
});
