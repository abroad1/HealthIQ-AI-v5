'use client';

import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import Link from 'next/link';
import type { BiomarkerResult } from '@/types/analysis';
import { Download } from 'lucide-react';
import { humanizeStatus, oneLineMarkerInterpretation, type ResultActionCardModel } from '@/lib/resultsPageLayout';
import { cn } from '@/lib/utils';

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
  downloadDisabledReason?: string;
}

export function ResultsPrimaryHero({
  phenotypeLabel,
  summary,
  severityLabel,
  severityTone,
  downloadDisabledReason = 'PDF download is coming in a following release.',
}: ResultsPrimaryHeroProps) {
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
          <p className="text-base text-slate-800 leading-relaxed max-w-prose">{summary}</p>
          <div className="flex flex-wrap items-center gap-2">
            <Button type="button" size="sm" disabled className="gap-2" title={downloadDisabledReason}>
              <Download className="h-4 w-4" aria-hidden />
              Download report
            </Button>
            <p className="text-xs text-slate-500">{downloadDisabledReason}</p>
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
          <CardDescription>Top signals behind the main pattern, using the values returned for this run.</CardDescription>
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
                    <p className="font-medium text-slate-900">{b.biomarker_name}</p>
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
        No separate action list was included with this result. Your clinician interpretation and system groups below
        still describe what to discuss next.
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
