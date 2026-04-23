'use client';

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { BookOpen, ListChecks, Route, Stethoscope, TrendingUp } from 'lucide-react';
import type { NarrativeReportV1 } from '@/types/analysis';
import { cn } from '@/lib/utils';

function NarrativeProse({ text, className }: { text: string; className?: string }) {
  return <div className={cn('text-sm text-slate-800 leading-relaxed whitespace-pre-line', className)}>{text}</div>;
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
          <CardDescription>Plain-language overview from the deterministic narrative compiler.</CardDescription>
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
          <CardDescription>Deterministic explanation of the primary pattern and related context.</CardDescription>
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
  className = '',
}: {
  narrative?: NarrativeReportV1 | null;
  className?: string;
}) {
  const longitudinal = narrative?.longitudinal_narrative?.trim();
  const next = narrative?.next_steps_narrative?.trim();
  if (!longitudinal && !next) return null;

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
          {next ? (
            <div className={longitudinal ? 'border-t border-slate-100 pt-4' : ''}>
              <p className="text-xs font-semibold uppercase tracking-wide text-slate-500 mb-2 flex items-center gap-1">
                <ListChecks className="h-3.5 w-3.5" aria-hidden />
                Next steps
              </p>
              <NarrativeProse text={next} />
            </div>
          ) : null}
        </CardContent>
      </Card>
    </section>
  );
}
