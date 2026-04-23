'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { LayoutGrid } from 'lucide-react';
import type { ClinicianReportV1 } from '@/types/analysis';
import {
  BODY_OVERVIEW_FALLBACK_PRIMARY,
  buildBodyOverviewPrimarySentence,
  summarizeClusterPatternBuckets,
} from '@/lib/bodyOverviewPrimarySentence';

export interface ResultsBodyOverviewProps {
  clinicianReport: ClinicianReportV1 | null | undefined;
  /** Cluster rows from analysis (severity used only for bucket counts). */
  clusters: { severity?: string | null }[];
  /** F-1 — when set, replaces heuristic primary sentence with backend `narrative_report_v1.body_overview`. */
  compiledBodyOverview?: string | null;
  className?: string;
}

/**
 * FE-R1 Section 1 — Body overview: one primary sentence, quick pattern scan, micro-framing only.
 */
export function ResultsBodyOverview({
  clinicianReport,
  clusters,
  compiledBodyOverview,
  className = '',
}: ResultsBodyOverviewProps) {
  const page1 = clinicianReport?.sections?.page1;
  const compiled = (compiledBodyOverview ?? '').trim();
  const primary =
    compiled ||
    (page1 && (page1.primary_concern || page1.top_hypothesis_line || page1.key_findings?.[0])
      ? buildBodyOverviewPrimarySentence(page1)
      : BODY_OVERVIEW_FALLBACK_PRIMARY);

  const buckets = summarizeClusterPatternBuckets(clusters);
  const totalPatterns = clusters.length;
  const hasBuckets = totalPatterns > 0;

  return (
    <section className={className} aria-labelledby="body-overview-heading" data-testid="results-body-overview">
      <Card className="border-slate-200 shadow-sm">
        <CardHeader className="pb-2">
          <CardTitle id="body-overview-heading" className="text-xl font-semibold text-gray-900 flex items-center gap-2">
            <LayoutGrid className="h-6 w-6 text-slate-600 shrink-0" aria-hidden />
            Body overview
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4 pt-0">
          <p className="text-lg font-medium text-gray-900 leading-snug">{primary}</p>

          {hasBuckets ? (
            <div className="rounded-lg border border-slate-100 bg-slate-50/80 p-4">
              <p className="text-xs font-semibold uppercase tracking-wide text-slate-500 mb-3">Pattern groups on this panel</p>
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 text-sm">
                <div className="rounded-md bg-white border border-amber-100 px-3 py-2">
                  <p className="text-xs text-amber-800 font-medium">Needs attention</p>
                  <p className="text-2xl font-semibold text-amber-950">{buckets.needs_attention}</p>
                </div>
                <div className="rounded-md bg-white border border-slate-200 px-3 py-2">
                  <p className="text-xs text-slate-600 font-medium">Explore further</p>
                  <p className="text-2xl font-semibold text-slate-900">{buckets.explore_further}</p>
                </div>
                <div className="rounded-md bg-white border border-emerald-100 px-3 py-2">
                  <p className="text-xs text-emerald-800 font-medium">Stable on this panel</p>
                  <p className="text-2xl font-semibold text-emerald-950">{buckets.stable}</p>
                </div>
              </div>
              <p className="text-xs text-slate-500 mt-2">{totalPatterns} pattern group{totalPatterns === 1 ? '' : 's'} in this run.</p>
            </div>
          ) : (
            <p className="text-sm text-slate-600 border border-dashed border-slate-200 rounded-md px-3 py-2 bg-white">
              Pattern groups are not available for this result yet — the sections below still walk through your markers
              and findings.
            </p>
          )}
        </CardContent>
      </Card>
    </section>
  );
}
