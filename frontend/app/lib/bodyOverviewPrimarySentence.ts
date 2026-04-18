import type { ClinicianReportV1, PrimaryConcernModeV1 } from '@/types/analysis';

/** Safe copy when `page1` is missing or insufficient — sprint FE-R1 fallback. */
export const BODY_OVERVIEW_FALLBACK_PRIMARY =
  "We've analysed your results and will guide you through the key findings below.";

/** First sentence or bounded excerpt — used for overview and investigation spine (FE-R8B). */
export function extractFirstSentence(text: string): string {
  const t = text.trim();
  if (!t) return '';
  const cut = t.match(/^(.+?[.!?])(\s|$)/);
  if (cut) return cut[1].trim();
  if (t.length <= 280) return t;
  return `${t.slice(0, 277).trim()}…`;
}

/** Ensures a clause ends with `.` `!` or `?` before appending another sentence (FE-R8B). */
export function ensureTerminalPunctuation(s: string): string {
  const t = s.trim();
  if (!t) return t;
  return /[.!?]$/.test(t) ? t : `${t}.`;
}

/**
 * Single primary line for Section 1 — grounded in `clinician_report_v1.sections.page1` only.
 * Not a raw concatenation of all page1 fields; shapes one scannable sentence (+ optional clause for tie modes).
 */
export function buildBodyOverviewPrimarySentence(
  page1: ClinicianReportV1['sections']['page1'] | undefined
): string {
  if (!page1) return BODY_OVERVIEW_FALLBACK_PRIMARY;

  const concern = (page1.primary_concern || '').trim();
  const topHyp = (page1.top_hypothesis_line || '').trim();
  const kf0 = (page1.key_findings?.[0] || '').trim();
  const mode: PrimaryConcernModeV1 | undefined = page1.primary_concern_mode;

  if (!concern && !topHyp && !kf0) {
    return BODY_OVERVIEW_FALLBACK_PRIMARY;
  }

  const leadSource = concern || topHyp || kf0;
  const lead = ensureTerminalPunctuation(extractFirstSentence(leadSource));

  const wider =
    mode === 'near_tie_ambiguity' || mode === 'technical_tiebreak_lead'
      ? ' More than one pattern is close; the sections below show how we set focus.'
      : " We'll show how this fits the wider picture as you go.";

  return `${lead}${wider}`;
}

export type PatternBucketKey = 'needs_attention' | 'explore_further' | 'stable';

/** Quick-scan counts from cluster severity — no forbidden DTO fields. */
export function summarizeClusterPatternBuckets(clusters: { severity?: string | null }[]): Record<
  PatternBucketKey,
  number
> {
  let needs_attention = 0;
  let explore_further = 0;
  let stable = 0;
  for (const c of clusters) {
    const raw = String(c.severity || 'moderate').toLowerCase();
    if (raw === 'critical' || raw === 'high') needs_attention += 1;
    else if (raw === 'normal' || raw === 'mild' || raw === 'low') stable += 1;
    else explore_further += 1;
  }
  return { needs_attention, explore_further, stable };
}
