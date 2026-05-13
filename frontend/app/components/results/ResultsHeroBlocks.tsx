'use client';

import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import Link from 'next/link';
import type { BiomarkerResult } from '@/types/analysis';
import { Download } from 'lucide-react';
import { humanizeStatus, oneLineMarkerInterpretation, type ResultActionCardModel, formatBiomarkerDisplayName } from '@/lib/resultsPageLayout';
import { cn } from '@/lib/utils';
import { scrubConsumerRetailNarrative } from '@/lib/retailNarrativeSanitize';

function severityBadgeClass(tone: 'rose' | 'amber' | 'slate' | 'emerald'): string {
  switch (tone) {
    case 'rose':
      return 'border-rose-200 bg-rose-50 text-rose-950';
    case 'amber':
      return 'border-amber-200 bg-amber-50 text-amber-950';
    case 'emerald':
      return 'border-emerald-200 bg-emerald-50 text-emerald-950';
    default:
      return 'border-slate-200 bg-slate-50 text-slate-800';
  }
}

export interface ResultsPrimaryHeroProps {
  phenotypeLabel: string;
  summary: string;
  severityLabel: string;
  severityTone: 'rose' | 'amber' | 'slate' | 'emerald';
  /**
   * When the clinician-ranked lead differs from the pattern-led hero title (IDL present),
   * show it only as explicit secondary copy — not as the main hero paragraph.
   */
  rankedSignalSecondaryLine?: string | null;
  /** LC-S6 — e.g. "Main system context: …" when hero title is the ranked lead pattern. */
  systemContextLine?: string | null;
  /** When set, enables the button and runs this handler (Sprint 4 PDF). */
  onDownloadReport?: () => void | Promise<void>;
  downloadPending?: boolean;
  downloadError?: string | null;
  downloadDisabledReason?: string;
}

function triggerBrowserDownload(blob: Blob, filename: string) {
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  a.rel = 'noopener';
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(url);
}

export { triggerBrowserDownload };

export function ResultsPrimaryHero({
  phenotypeLabel,
  summary,
  severityLabel,
  severityTone,
  rankedSignalSecondaryLine = null,
  systemContextLine = null,
  onDownloadReport,
  downloadPending = false,
  downloadError = null,
  downloadDisabledReason = 'Sign in to download your report.',
}: ResultsPrimaryHeroProps) {
  const safeSummary = scrubConsumerRetailNarrative(summary);
  const safeSecondary = rankedSignalSecondaryLine ? scrubConsumerRetailNarrative(rankedSignalSecondaryLine) : null;
  const safeSystemContext = systemContextLine ? scrubConsumerRetailNarrative(systemContextLine) : null;

  return (
    <section aria-labelledby="primary-finding-hero" data-testid="results-primary-hero">
      <Card className="border-indigo-100 bg-gradient-to-b from-indigo-50/40 to-white shadow-sm">
        <CardHeader className="pb-2">
          <div className="flex flex-wrap items-start justify-between gap-3">
            <div className="space-y-1">
              <p className="text-xs font-semibold uppercase tracking-wide text-indigo-800/90">Primary finding</p>
              <CardTitle id="primary-finding-hero" className="text-2xl font-semibold text-slate-900 leading-snug max-w-2xl">
                {phenotypeLabel}
              </CardTitle>
              {systemContextLine ? (
                <p className="text-sm text-slate-600 leading-snug max-w-2xl mt-1">{safeSystemContext}</p>
              ) : null}
            </div>
            <Badge
              variant="outline"
              className={cn('shrink-0 font-medium', severityBadgeClass(severityTone))}
              data-testid="primary-severity-badge"
            >
              {severityLabel}
            </Badge>
          </div>
        </CardHeader>
        <CardContent className="space-y-4">
          <p className="text-base text-slate-800 leading-relaxed max-w-prose">{safeSummary}</p>
          {safeSecondary ? (
            <p className="text-sm text-slate-600 leading-relaxed max-w-prose border-l-2 border-slate-200 pl-3">
              {safeSecondary}
            </p>
          ) : null}
          <div className="flex flex-col gap-1 sm:flex-row sm:flex-wrap sm:items-center sm:gap-2">
            <Button
              type="button"
              size="sm"
              className="gap-2"
              disabled={!onDownloadReport || downloadPending}
              title={onDownloadReport ? 'Download a PDF summary' : downloadDisabledReason}
              onClick={() => void onDownloadReport?.()}
            >
              <Download className="h-4 w-4" aria-hidden />
              {downloadPending ? 'Preparing PDF…' : 'Download report'}
            </Button>
            {onDownloadReport ? null : (
              <p className="text-xs text-slate-500">{downloadDisabledReason}</p>
            )}
            {downloadError ? (
              <p className="text-xs text-red-600" role="alert">
                {downloadError}
              </p>
            ) : null}
          </div>
        </CardContent>
      </Card>
    </section>
  );
}

export interface ResultsDrivingSignalsProps {
  markers: BiomarkerResult[];
  biomarkerSectionId: string;
}

export function ResultsDrivingSignals({ markers, biomarkerSectionId }: ResultsDrivingSignalsProps) {
  return (
    <section aria-labelledby="driving-signals-heading" data-testid="results-driving-signals">
      <Card className="border-slate-200 shadow-sm">
        <CardHeader className="pb-2">
          <CardTitle id="driving-signals-heading" className="text-lg">
            What&apos;s driving this
          </CardTitle>
          <CardDescription>Key markers behind the main pattern, using the values returned for this run.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-3">
          {markers.length === 0 ? (
            <p className="text-sm text-slate-600">No individual marker rows were returned for the primary driver set.</p>
          ) : (
            <ul className="space-y-3">
              {markers.map((b) => (
                <li
                  key={b.biomarker_name}
                  className="rounded-lg border border-slate-100 bg-slate-50/60 px-3 py-3"
                >
                  <div className="flex flex-wrap items-baseline justify-between gap-2">
                    <p className="font-medium text-slate-900">{formatBiomarkerDisplayName(b.biomarker_name)}</p>
                    <p className="text-sm text-slate-700 tabular-nums">
                      {b.value} {b.unit}
                      <span className="text-slate-500"> · {humanizeStatus(b.status)}</span>
                    </p>
                  </div>
                  <p className="text-sm text-slate-600 mt-1 leading-relaxed">{oneLineMarkerInterpretation(b)}</p>
                </li>
              ))}
            </ul>
          )}
          <p>
            <Link
              href={`#${biomarkerSectionId}`}
              className="text-sm font-medium text-indigo-700 hover:text-indigo-900 underline-offset-2 hover:underline"
            >
              See all markers
            </Link>
          </p>
        </CardContent>
      </Card>
    </section>
  );
}

export function ResultsActionCardsBlock({ actions }: { actions: ResultActionCardModel[] }) {
  if (actions.length === 0) {
    return (
      <p className="text-sm text-slate-600 border border-dashed border-slate-200 rounded-md px-3 py-3 bg-slate-50/50">
        No separate checklist of follow-up lines was packaged with this result. The sections below still describe what to discuss next.
      </p>
    );
  }
  return (
    <ul className="space-y-3" data-testid="results-action-cards">
      {actions.map((a, i) => (
        <li key={`${a.heading}-${i}`} className="rounded-lg border border-slate-200 bg-white px-3 py-3 shadow-sm">
          <div className="flex flex-wrap items-start justify-between gap-2">
            <p className="font-medium text-slate-900 pr-2">{a.heading}</p>
            <div className="flex flex-wrap gap-2">
              <Badge variant="secondary" className="font-normal text-xs">
                {a.categoryLabel}
              </Badge>
              <Badge variant="outline" className="font-normal text-xs">
                {a.evidenceLevelLabel}
              </Badge>
            </div>
          </div>
          <p className="text-sm text-slate-700 mt-2 leading-relaxed">{a.paragraph}</p>
          <p className="text-xs text-slate-500 mt-2">Source: {a.sourceLabel}</p>
        </li>
      ))}
    </ul>
  );
}
