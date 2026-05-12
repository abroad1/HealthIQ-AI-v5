import { filterConsumerInsights, isLegacyV1Insight, legacyInsightsDebugEnabled } from '@/lib/legacyInsightsVisibility';
import { buildActionCardModels } from '@/lib/resultsPageLayout';
import type { Cluster, Insight } from '@/types/analysis';

describe('legacyInsightsVisibility (LC-S4)', () => {
  const prev = process.env.NEXT_PUBLIC_HEALTHIQ_LEGACY_INSIGHTS;

  afterEach(() => {
    if (prev === undefined) {
      delete process.env.NEXT_PUBLIC_HEALTHIQ_LEGACY_INSIGHTS;
    } else {
      process.env.NEXT_PUBLIC_HEALTHIQ_LEGACY_INSIGHTS = prev;
    }
  });

  it('treats missing manifest_id as legacy_v1', () => {
    expect(isLegacyV1Insight({})).toBe(true);
    expect(isLegacyV1Insight({ manifest_id: 'legacy_v1' })).toBe(true);
    expect(isLegacyV1Insight({ manifest_id: 'production_v1' })).toBe(false);
  });

  it('filters legacy insights off the consumer path by default', () => {
    delete process.env.NEXT_PUBLIC_HEALTHIQ_LEGACY_INSIGHTS;
    const mixed: Insight[] = [
      { id: 'a', category: 'x', manifest_id: 'legacy_v1', recommendations: ['Old'] },
      { id: 'b', category: 'y', manifest_id: 'production_v1', recommendations: ['New'] },
    ];
    expect(filterConsumerInsights(mixed)).toHaveLength(1);
    expect(filterConsumerInsights(mixed)[0].id).toBe('b');
  });

  it('returns all insights when debug flag is set', () => {
    process.env.NEXT_PUBLIC_HEALTHIQ_LEGACY_INSIGHTS = 'true';
    expect(legacyInsightsDebugEnabled()).toBe(true);
    const legacy: Insight[] = [{ id: 'a', category: 'x', manifest_id: 'legacy_v1', recommendations: ['Old'] }];
    expect(filterConsumerInsights(legacy)).toHaveLength(1);
  });

  it('buildActionCardModels does not consume legacy insights when insights option is omitted', () => {
    const clusters: Cluster[] = [];
    const legacyOnly: Insight[] = [
      { id: 'a', category: 'x', manifest_id: 'legacy_v1', recommendations: ['Only legacy rec'] },
    ];
    const withLegacy = buildActionCardModels([], [], { maxItems: 5, insights: legacyOnly });
    const without = buildActionCardModels([], [], { maxItems: 5 });
    expect(withLegacy.length).toBeGreaterThan(0);
    expect(without.length).toBe(0);
  });
});
