/**
 * LC-S4 — legacy `insights[]` (manifest_id legacy_v1) must not surface on consumer paths
 * unless NEXT_PUBLIC_HEALTHIQ_LEGACY_INSIGHTS is enabled for local/debug review.
 */

export function legacyInsightsDebugEnabled(): boolean {
  if (typeof process === 'undefined') return false;
  const v = process.env.NEXT_PUBLIC_HEALTHIQ_LEGACY_INSIGHTS;
  return v === '1' || v === 'true';
}

/** Backend default for older rows is legacy_v1; empty manifest_id is treated as legacy. */
export function isLegacyV1Insight(insight: { manifest_id?: string | null }): boolean {
  const mid = (insight.manifest_id ?? 'legacy_v1').trim();
  return mid === '' || mid === 'legacy_v1';
}

export function filterConsumerInsights<T extends { manifest_id?: string | null }>(
  insights: T[] | null | undefined
): T[] {
  if (!insights?.length) return [];
  if (legacyInsightsDebugEnabled()) return [...insights];
  return insights.filter((i) => !isLegacyV1Insight(i));
}

export function hasNonLegacyInsights(insights: { manifest_id?: string | null }[] | null | undefined): boolean {
  return filterConsumerInsights(insights).length > 0;
}
