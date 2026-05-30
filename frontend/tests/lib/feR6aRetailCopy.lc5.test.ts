import {
  biomarkerInterpretationForDetail,
  isMarkerNumericScoreInterpretation,
  sanitizeBiomarkerInterpretationForRetail,
} from '@/lib/feR6aRetailCopy';

describe('feR6aRetailCopy LC-5 marker score display', () => {
  it('hides Scored X/100 from default retail card sanitize', () => {
    expect(sanitizeBiomarkerInterpretationForRetail('Scored 30.5/100')).toBeNull();
    expect(sanitizeBiomarkerInterpretationForRetail('Scored 100.0/100')).toBeNull();
  });

  it('preserves Scored X/100 in detail expansion path', () => {
    expect(biomarkerInterpretationForDetail('Scored 30.5/100')).toBe('Scored 30.5/100');
  });

  it('detects numeric score interpretation lines', () => {
    expect(isMarkerNumericScoreInterpretation('Scored 30.5/100')).toBe(true);
    expect(isMarkerNumericScoreInterpretation('Elevated for your age group')).toBe(false);
  });
});
