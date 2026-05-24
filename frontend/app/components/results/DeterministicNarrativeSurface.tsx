'use client';

import { useMemo } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { BookOpen, ListChecks, Route, Stethoscope, TrendingUp } from 'lucide-react';
import type { NarrativeReportV1 } from '@/types/analysis';
import { cn } from '@/lib/utils';
import { scrubConsumerRetailNarrative } from '@/lib/retailNarrativeSanitize';
import { parseNarrativeNextStepParagraphs } from '@/lib/resultsPageLayout';
import { stripDanglingNextStepsLabels } from '@/lib/feR6aRetailCopy';

function NarrativeProse({
  text,
  className,
}: {
  text: string;
  className?: string;
}) {
  const safe = useMemo(() => scrubConsumerRetailNarrative(text), [text]);
  return <div className={cn('text-sm text-slate-800 leading-relaxed whitespace-pre-line', className)}>{safe}</div>;
}

export function hasDeterministicNarrativeContent(n: NarrativeReportV1 | null | undefined): boolean {
  if (!n) return false;
  const fields = [
    n.retail_summary,
    n.body_overview,
    n.lead_narrative,
    n.secondary_narratives,
    n.longitudinal_narrative,
    n.secondary_systems,
    n.next_steps_narrative,
    n.clinician_synthesis,
  ];
  return fields.some((f) => typeof f === 'string' && f.trim().length > 0);
}

/** F-1 — Top-of-journey lay summary from `narrative_report_v1.retail_summary` (backend-compiled only). */
export function NarrativeRetailSummaryCard({
  narrative,
  className = '',
}: {
  narrative?: NarrativeReportV1 | null;
  className?: string;
}) {
  const text = narrative?.retail_summary?.trim();
  if (!text) return null;
  return (
    <section aria-labelledby="deterministic-retail-summary-heading" className={className}>
      <Card className="border-indigo-100 bg-indigo-50/25 shadow-sm" data-testid="narrative-retail-summary">
        <CardHeader className="pb-2">
          <CardTitle
            id="deterministic-retail-summary-heading"
            className="text-lg font-semibold text-slate-900 flex items-center gap-2"
          >
            <BookOpen className="h-5 w-5 text-indigo-600 shrink-0" aria-hidden />
            Summary
          </CardTitle>
          <CardDescription>A plain-language summary of the main pattern in your results.</CardDescription>
        </CardHeader>
        <CardContent className="pt-0">
          <NarrativeProse text={text} className="text-base text-slate-900" />
        </CardContent>
      </Card>
    </section>
  );
}

/** F-1 — Lead / secondary / other systems blocks (compiler text only; hierarchy preserved). */
export function NarrativeLeadAndSupportingSections({
  narrative,
  className = '',
}: {
  narrative?: NarrativeReportV1 | null;
  className?: string;
}) {
  const lead = narrative?.lead_narrative?.trim();
  const secondary = narrative?.secondary_narratives?.trim();
  const otherSystems = narrative?.secondary_systems?.trim();
  if (!lead && !secondary && !otherSystems) return null;

  return (
    <section aria-labelledby="deterministic-lead-narrative-heading" className={className} data-testid="narrative-lead-stack">
      <Card className="border-slate-200 shadow-sm">
        <CardHeader className="pb-2">
          <CardTitle
            id="deterministic-lead-narrative-heading"
            className="text-xl font-semibold text-gray-900 flex items-center gap-2"
          >
            <Stethoscope className="h-6 w-6 text-slate-600 shrink-0" aria-hidden />
            What this means
          </CardTitle>
          <CardDescription>
            How the main pattern fits with the rest of your markers — written in plain language, with appropriate
            caution.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6 pt-0">
          {lead ? (
            <div>
              <p className="text-xs font-semibold uppercase tracking-wide text-slate-500 mb-2">Primary focus</p>
              <NarrativeProse text={lead} className="text-base text-slate-900" />
            </div>
          ) : null}
          {secondary ? (
            <div className="border-t border-slate-100 pt-4">
              <p className="text-xs font-semibold uppercase tracking-wide text-slate-500 mb-2">Secondary patterns</p>
              <NarrativeProse text={secondary} className="text-slate-700" />
            </div>
          ) : null}
          {otherSystems ? (
            <div className="border-t border-slate-100 pt-4">
              <p className="text-xs font-semibold uppercase tracking-wide text-slate-500 mb-2">Other systems</p>
              <NarrativeProse text={otherSystems} className="text-slate-700" />
            </div>
          ) : null}
        </CardContent>
      </Card>
    </section>
  );
}

/** F-1 — Longitudinal direction + prioritised next steps. */
export function NarrativeLongitudinalAndNextSteps({
  narrative,
  nextStepsParagraphs,
  className = '',
}: {
  narrative?: NarrativeReportV1 | null;
  /** FE-R6A — pre-parsed/deduped lines; overrides raw narrative next_steps when set. */
  nextStepsParagraphs?: string[] | null;
  className?: string;
}) {
  const longitudinal = narrative?.longitudinal_narrative?.trim();
  const nextRaw = narrative?.next_steps_narrative?.trim();
  const nextLines =
    nextStepsParagraphs && nextStepsParagraphs.length > 0
      ? nextStepsParagraphs
      : nextRaw
        ? parseNarrativeNextStepParagraphs(stripDanglingNextStepsLabels(nextRaw))
        : [];
  if (!longitudinal && nextLines.length === 0) return null;

  return (
    <section className={className} aria-labelledby="deterministic-longitudinal-heading" data-testid="narrative-trend-next">
      <Card className="border-slate-200 shadow-sm">
        <CardHeader className="pb-2">
          <CardTitle
            id="deterministic-longitudinal-heading"
            className="text-xl font-semibold text-gray-900 flex items-center gap-2"
          >
            <Route className="h-6 w-6 text-slate-600 shrink-0" aria-hidden />
            Direction and follow-up
          </CardTitle>
          <CardDescription>How markers moved relative to prior data when available, and suggested next actions.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-6 pt-0">
          {longitudinal ? (
            <div>
              <p className="text-xs font-semibold uppercase tracking-wide text-slate-500 mb-2 flex items-center gap-1">
                <TrendingUp className="h-3.5 w-3.5" aria-hidden />
                Trends
              </p>
              <NarrativeProse text={longitudinal} />
            </div>
          ) : null}
          {nextLines.length > 0 ? (
            <div className={longitudinal ? 'border-t border-slate-100 pt-4' : ''}>
              <p className="text-xs font-semibold uppercase tracking-wide text-slate-500 mb-2 flex items-center gap-1">
                <ListChecks className="h-3.5 w-3.5" aria-hidden />
                Next steps
              </p>
              <ul
                className="list-disc pl-5 space-y-2 text-sm text-slate-800 leading-relaxed"
                data-testid="narrative-next-steps-list"
              >
                {nextLines.map((line, i) => (
                  <li key={i}>{scrubConsumerRetailNarrative(line)}</li>
                ))}
              </ul>
            </div>
          ) : null}
        </CardContent>
      </Card>
    </section>
  );
}
