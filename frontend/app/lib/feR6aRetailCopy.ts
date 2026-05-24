/**
 * FE-R6A — retail-surface copy guards (presentation only; no clinical logic).
 */

const SCORING_ONLY_INTERPRETATION_RE =
  /^(Scored using|Not scored\b|Insufficient numeric bounds)/i;

const RAW_SCORING_ERROR_RE =
  /^Not scored\s*[-–—]\s*result unit and lab reference range unit cannot be aligned/i;

export const BIOMARKER_LIMITED_STATE_MESSAGE =
  'More interpretive detail for this marker is not available on this panel yet. Your clinician can help place this value in context.';

export const BIOMARKER_UNSCORED_CONSUMER_MESSAGE =
  'This result is shown for reference, but HealthIQ could not score it reliably because the units or reference range need review.';

export function isScoringMechanicsInterpretation(text: string | null | undefined): boolean {
  const t = (text || '').trim();
  if (!t.length) return false;
  return SCORING_ONLY_INTERPRETATION_RE.test(t) || RAW_SCORING_ERROR_RE.test(t);
}

export function sanitizeBiomarkerInterpretationForRetail(text: string | null | undefined): string | null {
  const t = (text || '').trim();
  if (!t.length) return null;
  if (RAW_SCORING_ERROR_RE.test(t)) return BIOMARKER_UNSCORED_CONSUMER_MESSAGE;
  if (isScoringMechanicsInterpretation(t)) return null;
  return t;
}

export function retailInterpretationForExpansion(
  interpretation: string | null | undefined,
  hasDeeperLayers: boolean
): { showInterpretationBlock: boolean; interpretationText: string | null; showLimitedState: boolean } {
  const sanitized = sanitizeBiomarkerInterpretationForRetail(interpretation);
  if (sanitized) {
    return { showInterpretationBlock: true, interpretationText: sanitized, showLimitedState: false };
  }
  if (!hasDeeperLayers) {
    return {
      showInterpretationBlock: false,
      interpretationText: null,
      showLimitedState: true,
    };
  }
  return { showInterpretationBlock: false, interpretationText: null, showLimitedState: false };
}

export function scrubBalancedSystemsEvidenceLine(line: string): string {
  let s = line;
  s = s.replace(/\s*\(interpretation confidence for this read:[^)]*\)/gi, '');
  s = s.replace(/\s*interpretation confidence for this read:\s*[^\s.)]+/gi, '');
  return s.replace(/\s{2,}/g, ' ').trim();
}

export function stripDanglingNextStepsLabels(text: string): string {
  return text
    .replace(/Suggested follow-up themes:\s*$/gim, '')
    .replace(/Suggested follow-up themes:\s*\n/gi, '\n')
    .trim();
}

export function filterNarrativeNextStepsForConfirmatoryDedup(
  paragraphs: string[],
  confirmatoryDisplayNames: string[]
): string[] {
  if (!confirmatoryDisplayNames.length) return paragraphs;
  const needles = confirmatoryDisplayNames.map((n) => n.toLowerCase().trim()).filter(Boolean);
  return paragraphs.filter((p) => {
    const low = p.toLowerCase();
    return !needles.some((name) => name.length > 4 && low.includes(name));
  });
}
