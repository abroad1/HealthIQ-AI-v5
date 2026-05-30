import { scrubKnownInternalPatternNames } from '@/lib/cardEvidenceConsumerCopy';

/**
 * Backend `compile_clinician_report_v1` may emit these strings as real `page1` fields.
 * They are implementation placeholders and must not be shown as user-facing prose.
 */
const PLACEHOLDER_TOP_HYPOTHESIS_LINES = new Set([
  'No hypothesis set available for this concern in v1.',
]);

const INTERNAL_WHY_FALLBACK_RE = /^no governed why for signal_/i;

export function sanitizeTopHypothesisLineForDisplay(raw: string | null | undefined): string {
  const t = (raw ?? '').trim();
  if (!t) return '';
  if (PLACEHOLDER_TOP_HYPOTHESIS_LINES.has(t)) return '';
  if (INTERNAL_WHY_FALLBACK_RE.test(t)) return '';
  if (t.startsWith('Top hypothesis: ') && INTERNAL_WHY_FALLBACK_RE.test(t)) return '';
  return t;
}

/** Strip legacy internal WHY fallback titles from consumer primary-concern lines. */
export function sanitizePrimaryConcernForDisplay(raw: string | null | undefined): string {
  const t = (raw ?? '').trim();
  if (!t) return '';
  if (INTERNAL_WHY_FALLBACK_RE.test(t)) {
    return 'A lead pattern was identified, but a deeper causal explanation is not yet available on this panel.';
  }
  return scrubKnownInternalPatternNames(t);
}
