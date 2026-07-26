'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import type { Cluster } from '@/types/analysis';
import type { BalancedSystemsV1 } from '@/components/results/BalancedSystemsSummary';
import {
  SYSTEM_UNDERSTANDING_HEADINGS,
  biggerPictureCopy,
  groupingCopy,
  stableStrainCopy,
} from '@/lib/systemUnderstandingCopy';

export interface SystemUnderstandingPrimaryDriver {
  id: string;
  name: string;
  biomarkers: string[];
}

export interface SystemUnderstandingSectionProps {
  balanced: BalancedSystemsV1 | null | undefined;
  clusters: Cluster[];
  primaryDriver: SystemUnderstandingPrimaryDriver | null;
  /** FE-R8C — first visible IDL retail label; example binding only, no new inference */
  idlRetailLabel?: string | null;
}

/** Human-readable label from a marker key — avoids displaying raw snake_case identifiers. */
function formatMarkerLabel(raw: string): string {
  const s = raw.trim();
  if (!s) return '';
  return s
    .split(/[_\s]+/)
    .filter(Boolean)
    .map((w) => w.charAt(0).toUpperCase() + w.slice(1).toLowerCase())
    .join(' ');
}

function clusterLabel(c: Cluster | undefined): string | null {
  if (!c) return null;
  const n = c.name?.trim();
  return n || null;
}

function clusterById(clusters: Cluster[], id: string): Cluster | undefined {
  return clusters.find((c) => String(c.cluster_id || c.id || '') === id);
}

/**
 * FE-R5 — Section 5: three short blocks (grouping, stable vs strain, markers → pattern).
 *
 * ARCH-CONV-CORRECT-1 — all prose comes from the governed copy module in
 * `@/lib/systemUnderstandingCopy`; this component only selects which governed names to
 * interpolate and never authors medical wording.
 */
export function SystemUnderstandingSection({
  balanced,
  clusters,
  primaryDriver,
  idlRetailLabel,
}: SystemUnderstandingSectionProps) {
  const leadName = primaryDriver?.name?.trim() || null;
  const stableFirstTopic = balanced?.items?.[0]?.system_topic?.trim() || null;
  const idlLabel = idlRetailLabel?.trim() || null;

  const groupingSubject = ((): { systemName: string | null; markerLabels: string[] } => {
    if (primaryDriver && leadName) {
      const own = (primaryDriver.biomarkers || []).slice(0, 2).map(formatMarkerLabel).filter(Boolean);
      if (own.length > 0) return { systemName: leadName, markerLabels: own };
      const match = clusterById(clusters, primaryDriver.id);
      const fromCluster = (match?.biomarkers || match?.biomarkers_involved || [])
        .slice(0, 2)
        .map(formatMarkerLabel)
        .filter(Boolean);
      return { systemName: leadName, markerLabels: fromCluster };
    }
    if (clusters.length > 0) {
      const c0 = clusters[0];
      return {
        systemName: clusterLabel(c0) || 'Health pattern',
        markerLabels: (c0.biomarkers || c0.biomarkers_involved || [])
          .slice(0, 2)
          .map(formatMarkerLabel)
          .filter(Boolean),
      };
    }
    return { systemName: null, markerLabels: [] };
  })();

  const blockA = groupingCopy(groupingSubject);
  const blockB = stableStrainCopy({ stableTopic: stableFirstTopic, leadName });
  const blockC = biggerPictureCopy({ leadName, idlRetailLabel: idlLabel });

  return (
    <Card className="border-slate-200 bg-white shadow-sm" data-testid="system-understanding-section">
      <CardHeader className="pb-2">
        <CardTitle className="text-lg font-semibold text-gray-900">
          {SYSTEM_UNDERSTANDING_HEADINGS.section}
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-6 text-sm text-gray-800 leading-relaxed">
        <div>
          <h3 className="text-sm font-semibold text-gray-900 mb-1.5">
            {SYSTEM_UNDERSTANDING_HEADINGS.grouping}
          </h3>
          <p>{blockA}</p>
        </div>
        <div>
          <h3 className="text-sm font-semibold text-gray-900 mb-1.5">
            {SYSTEM_UNDERSTANDING_HEADINGS.stableStrain}
          </h3>
          <p>{blockB}</p>
        </div>
        <div>
          <h3 className="text-sm font-semibold text-gray-900 mb-1.5">
            {SYSTEM_UNDERSTANDING_HEADINGS.biggerPicture}
          </h3>
          <p>{blockC}</p>
        </div>
      </CardContent>
    </Card>
  );
}
