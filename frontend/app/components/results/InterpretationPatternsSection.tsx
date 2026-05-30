'use client';

import React, { useMemo } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import type { InterpretationDisplayLayerBundleV1, InterpretationDisplayRecordV1 } from '@/types/analysis';
import {
  formatScientificClassChipLabel,
  isGenericIdlSupportingSummary,
  selectSafeIdlPatternRecords,
} from '@/lib/feR5aIdlPatternGuards';
import { formatConsumerSeverityLabel } from '@/lib/resultsPageLayout';

/** @deprecated Use selectSafeIdlPatternRecords — retained for tests importing this symbol. */
export function selectVisibleIdlRecords(
  bundle: InterpretationDisplayLayerBundleV1 | null | undefined
): InterpretationDisplayRecordV1[] {
  return selectSafeIdlPatternRecords(bundle?.records);
}

function severityBadgeClass(severity: InterpretationDisplayRecordV1['severity_state']): string {
  switch (severity) {
    case 'strong_signal':
      return 'border-rose-200 bg-rose-50 text-rose-900';
    case 'attention':
      return 'border-amber-200 bg-amber-50 text-amber-950';
    case 'watch':
      return 'border-sky-200 bg-sky-50 text-sky-950';
    case 'not_observed':
    default:
      return 'border-slate-200 bg-slate-50 text-slate-800';
  }
}

function formatSeverityLabel(severity: InterpretationDisplayRecordV1['severity_state']): string {
  return formatConsumerSeverityLabel(severity);
}

export interface InterpretationPatternsSectionProps {
  bundle: InterpretationDisplayLayerBundleV1 | null | undefined;
  /** When true, omit outer section heading (parent journey section owns it). */
  embedInJourney?: boolean;
}

/**
 * FE-R5A — Section 5 “Patterns across your body” (governed display records only).
 */
export function InterpretationPatternsSection({
  bundle,
  embedInJourney = false,
}: InterpretationPatternsSectionProps) {
  const rows = useMemo(() => selectSafeIdlPatternRecords(bundle?.records), [bundle]);

  if (!rows.length) {
    return null;
  }

  const cards = (
    <div className="grid gap-4 md:grid-cols-1">
      {rows.map((rec) => {
        const classChip = formatScientificClassChipLabel(rec.scientific_class);
        const showSupporting =
          !!rec.supporting_biomarkers_summary?.trim() &&
          !isGenericIdlSupportingSummary(rec.supporting_biomarkers_summary);

        return (
          <Card
            key={`${rec.internal_id}-${rec.display_order_priority}`}
            className="border-slate-200 shadow-sm"
            data-testid={`idl-pattern-card-${rec.display_order_priority}`}
          >
            <CardHeader className="pb-2 space-y-2">
              <div className="flex flex-wrap items-start justify-between gap-2">
                <div>
                  <CardTitle className="text-lg font-semibold text-gray-900 leading-snug">
                    {rec.retail_display_label}
                  </CardTitle>
                  <CardDescription className="text-sm text-gray-600 mt-1">{rec.subtitle}</CardDescription>
                </div>
                <div className="flex flex-wrap gap-2 shrink-0">
                  {classChip ? (
                    <Badge
                      variant="outline"
                      className="font-normal border-slate-200 bg-slate-50 text-slate-800"
                      data-testid="idl-scientific-class-chip"
                    >
                      {classChip}
                    </Badge>
                  ) : null}
                  <Badge
                    variant="outline"
                    className={`font-normal ${severityBadgeClass(rec.severity_state)}`}
                    data-testid="idl-severity-chip"
                  >
                    {formatSeverityLabel(rec.severity_state)}
                  </Badge>
                </div>
              </div>
            </CardHeader>
            <CardContent className="space-y-3 text-sm text-gray-800">
              <p>
                <span className="text-gray-500 block text-xs uppercase tracking-wide mb-0.5">
                  Why this matters
                </span>
                {rec.why_it_matters}
              </p>
              {showSupporting ? (
                <p data-testid="idl-supporting-markers">
                  <span className="text-gray-500 block text-xs uppercase tracking-wide mb-0.5">
                    Supporting markers
                  </span>
                  {rec.supporting_biomarkers_summary}
                </p>
              ) : null}
              {rec.supporting_systems_summary ? (
                <p>
                  <span className="text-gray-500 block text-xs uppercase tracking-wide mb-0.5">
                    Systems context
                  </span>
                  {rec.supporting_systems_summary}
                </p>
              ) : null}
              {rec.display_caveat ? (
                <p className="text-xs text-gray-600 border-t border-dashed border-slate-200 pt-2">
                  {rec.display_caveat}
                </p>
              ) : null}
              {rec.user_safe_description ? (
                <details className="rounded-md border border-slate-100 bg-slate-50/60 px-3 py-2">
                  <summary className="cursor-pointer text-sm font-medium text-gray-800 outline-none">
                    Read more
                  </summary>
                  <p className="mt-2 text-sm text-gray-700 leading-relaxed">{rec.user_safe_description}</p>
                </details>
              ) : null}
            </CardContent>
          </Card>
        );
      })}
    </div>
  );

  if (embedInJourney) {
    return (
      <div className="space-y-4" data-testid="interpretation-patterns-section">
        <p className="text-sm text-gray-600 leading-relaxed">
          These patterns summarise how related markers group together on your panel. They support the story above — they
          are not a diagnosis on their own.
        </p>
        {cards}
      </div>
    );
  }

  return (
    <section
      className="space-y-4"
      aria-labelledby="patterns-across-body-heading"
      data-testid="interpretation-patterns-section"
    >
      <h2 id="patterns-across-body-heading" className="text-xl font-semibold text-gray-900">
        Patterns across your body
      </h2>
      <p className="text-sm text-gray-600 leading-relaxed">
        These patterns summarise how related markers group together on your panel. They support the story above — they are
        not a diagnosis on their own.
      </p>
      {cards}
    </section>
  );
}
