import type { AnalysisResult, ConsolidatedConcernSetV1 } from '@/types/analysis';

/**
 * CLIN-PRIORITY-CORE-1 — read server-computed clinical_concern_set from insight graph meta.
 * Frontend must not recompute tier / urgency / lead.
 */
export function getClinicalConcernSet(
  analysis: AnalysisResult | null | undefined
): ConsolidatedConcernSetV1 | null {
  const meta = analysis?.meta as Record<string, unknown> | undefined;
  const graph = meta?.insight_graph as Record<string, unknown> | undefined;
  const raw = graph?.clinical_concern_set;
  if (!raw || typeof raw !== 'object') return null;
  const set = raw as ConsolidatedConcernSetV1;
  if (!Array.isArray(set.findings)) return null;
  return set;
}

export function hasClinicalConcernAuthority(
  analysis: AnalysisResult | null | undefined
): boolean {
  const set = getClinicalConcernSet(analysis);
  return Boolean(set && (set.findings.length > 0 || set.no_concern === true));
}
