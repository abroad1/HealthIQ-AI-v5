'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import type { Cluster } from '@/types/analysis';
import type { BalancedSystemsV1 } from '@/components/results/BalancedSystemsSummary';

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
 * Deterministic; uses only props from the results page (no new DTO fields).
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

  // Block A — example system + 1–2 markers (deterministic: primary driver first, else first cluster)
  let blockA: string;
  if (primaryDriver && leadName) {
    const keys = (primaryDriver.biomarkers || []).slice(0, 2);
    const labels = keys.map(formatMarkerLabel).filter(Boolean);
    if (labels.length >= 2) {
      blockA = `We organise markers into body systems so related results read together instead of in isolation. ${leadName} brings together markers such as ${labels[0]} and ${labels[1]}, in the same neighbourhood as the headline pattern above.`;
    } else if (labels.length === 1) {
      blockA = `We organise markers into body systems so related results read together instead of in isolation. ${leadName} combines markers such as ${labels[0]}—near the headline pattern above.`;
    } else {
      const match = clusterById(clusters, primaryDriver.id);
      const altKeys = (match?.biomarkers || match?.biomarkers_involved || []).slice(0, 2);
      const altLabels = altKeys.map(formatMarkerLabel).filter(Boolean);
      if (altLabels.length >= 2) {
        blockA = `We organise markers into body systems so related results read together instead of in isolation. ${leadName} brings together markers such as ${altLabels[0]} and ${altLabels[1]}, in the same neighbourhood as the headline pattern above.`;
      } else if (altLabels.length === 1) {
        blockA = `We organise markers into body systems so related results read together instead of in isolation. ${leadName} combines markers such as ${altLabels[0]}—near the headline pattern above.`;
      } else {
        blockA = `We organise markers into body systems so related results read together. ${leadName} is one of the bundles we use to connect markers to the headline pattern above.`;
      }
    }
  } else if (clusters.length > 0) {
    const c0 = clusters[0];
    const name = clusterLabel(c0) || 'Health pattern';
    const raw = (c0.biomarkers || c0.biomarkers_involved || []).slice(0, 2);
    const labels = raw.map(formatMarkerLabel).filter(Boolean);
    if (labels.length >= 2) {
      blockA = `We organise markers into body systems so related results read together. ${name} is one example: it combines markers such as ${labels[0]} and ${labels[1]}.`;
    } else if (labels.length === 1) {
      blockA = `We organise markers into body systems so related results read together. ${name} combines markers such as ${labels[0]}.`;
    } else {
      blockA = `We organise markers into body systems so related results read together. ${name} is one of the groups we use to structure what you see on this page.`;
    }
  } else {
    blockA =
      'We group markers into body systems so related results read as connected signals, not scattered numbers. That structure is what lets a clear headline pattern emerge from the panel.';
  }

  // Block B — stable vs strain (ground in balanced_systems when present)
  let blockB: string;
  if (stableFirstTopic && leadName) {
    blockB = `Stable means a system looks broadly within range here; strain means several markers line up and need attention—not a diagnosis on its own. ${stableFirstTopic} appears among the stable systems named earlier, while ${leadName} is often where we focus when strain drives the view.`;
  } else if (stableFirstTopic) {
    blockB = `Stable means broadly within range for this snapshot; strain means several markers align and need attention—not a diagnosis on its own. ${stableFirstTopic} is one of the stable systems named earlier.`;
  } else if (leadName) {
    blockB = `Here, stable means a system looks broadly within range for this snapshot. Strain means several markers align in the same direction—often where ${leadName} leads—and that is where we narrow attention, without implying a diagnosis on its own.`;
  } else {
    blockB =
      'Stable systems are broadly within range for this snapshot. Where we describe strain, several markers are moving together in a way that deserves attention—that is where interpretation tightens, not a diagnosis on its own.';
  }

  // Block C — markers → bigger picture (do not reuse Section 3 sentences)
  let blockC: string;
  if (leadName && idlLabel) {
    blockC = `Individual markers are single signals; the useful story is how they combine across systems. ${leadName} organises markers for comparison, while the cross-body read “${idlLabel}” summarises how related signals line up across the panel—both are on this page, answering different layers of the same investigation.`;
  } else if (leadName) {
    blockC = `Individual markers are single signals; the useful story is how they combine across systems. When the evidence lines up, a pattern such as ${leadName} can sit at the top—without resting on any one number in isolation.`;
  } else {
    blockC =
      'Individual markers are single signals; the useful story is how they combine across systems. That layered reading is what produces the headline you see first on this page.';
  }

  return (
    <Card className="border-slate-200 bg-white shadow-sm" data-testid="system-understanding-section">
      <CardHeader className="pb-2">
        <CardTitle className="text-lg font-semibold text-gray-900">How to understand your results</CardTitle>
      </CardHeader>
      <CardContent className="space-y-6 text-sm text-gray-800 leading-relaxed">
        <div>
          <h3 className="text-sm font-semibold text-gray-900 mb-1.5">Why your results are grouped</h3>
          <p>{blockA}</p>
        </div>
        <div>
          <h3 className="text-sm font-semibold text-gray-900 mb-1.5">What “stable” and “strain” mean here</h3>
          <p>{blockB}</p>
        </div>
        <div>
          <h3 className="text-sm font-semibold text-gray-900 mb-1.5">How markers connect to the bigger picture</h3>
          <p>{blockC}</p>
        </div>
      </CardContent>
    </Card>
  );
}
