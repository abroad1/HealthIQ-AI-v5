/**
 * Backend `compile_clinician_report_v1` may emit these strings as real `page1` fields.
 * They are implementation placeholders and must not be shown as user-facing prose.
 */
const PLACEHOLDER_TOP_HYPOTHESIS_LINES = new Set([
  'No hypothesis set available for this concern in v1.',
]);

export function sanitizeTopHypothesisLineForDisplay(raw: string | null | undefined): string {
  const t = (raw ?? '').trim();
  if (!t) return '';
  if (PLACEHOLDER_TOP_HYPOTHESIS_LINES.has(t)) return '';
  return t;
}
