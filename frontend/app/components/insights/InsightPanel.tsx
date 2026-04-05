'use client';

import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Sparkles, ListOrdered, Microscope } from 'lucide-react';
import type { ClinicianReportV1, PrimaryConcernModeV1 } from '@/types/analysis';

export interface InsightPanelProps {
  report: ClinicianReportV1 | null | undefined;
  className?: string;
}

function formatSignalIdForDisplay(signalId: string): string {
  const stripped = signalId.replace(/^signal_/, '').replace(/_/g, ' ');
  return stripped.replace(/\b\w/g, (c) => c.toUpperCase());
}

function modeLabel(mode: PrimaryConcernModeV1 | undefined): { label: string; variant: 'default' | 'secondary' | 'outline' | 'destructive' } {
  switch (mode) {
    case 'near_tie_ambiguity':
      return { label: 'Several findings are closely ranked', variant: 'outline' };
    case 'technical_tiebreak_lead':
      return { label: 'Lead concern uses a technical tie-break', variant: 'secondary' };
    case 'distinct_lead':
    default:
      return { label: 'Clear lead concern', variant: 'default' };
  }
}

function modeAudienceNote(mode: PrimaryConcernModeV1 | undefined): string | null {
  if (mode === 'near_tie_ambiguity') {
    return 'More than one pattern may be similarly important. The headline reflects the current ranking, not certainty that other findings are less relevant.';
  }
  if (mode === 'technical_tiebreak_lead') {
    return 'Two or more findings had similar scores; governance selected the lead concern with a technical rule.';
  }
  return null;
}

/**
 * Policy-aligned hero: primary interpretation from clinician_report_v1.sections.page1.
 * Does not invent medical content when the report is absent.
 */
export function InsightPanel({ report, className = '' }: InsightPanelProps) {
  const page1 = report?.sections?.page1;

  if (!page1) {
    return (
      <Card className={`border-blue-100 shadow-sm ${className}`}>
        <CardHeader className="pb-2">
          <CardTitle className="flex items-center gap-2 text-xl">
            <Sparkles className="h-6 w-6 text-blue-600" />
            Interpretation
          </CardTitle>
          <CardDescription>
            A structured clinical summary is not available for this result yet. Use scores and markers below,
            or open the clinician report in Additional detail when present.
          </CardDescription>
        </CardHeader>
      </Card>
    );
  }

  const mode = page1.primary_concern_mode;
  const { label: modeText, variant: modeVariant } = modeLabel(mode);
  const ambiguityNote = modeAudienceNote(mode);
  const coPrimaries = page1.co_primary_signal_ids?.filter(Boolean) ?? [];

  return (
    <Card className={`border-blue-100 shadow-md ${className}`}>
      <CardHeader className="pb-2">
        <div className="flex flex-wrap items-center gap-2 mb-2">
          <CardTitle className="flex items-center gap-2 text-2xl font-semibold tracking-tight text-gray-900 mr-auto">
            <Sparkles className="h-7 w-7 text-blue-600 flex-shrink-0" />
            What matters most
          </CardTitle>
          <Badge variant={modeVariant}>{modeText}</Badge>
          {page1.ranking_policy_version ? (
            <Badge variant="outline" className="text-xs font-normal text-gray-600">
              Policy v{page1.ranking_policy_version}
            </Badge>
          ) : null}
        </div>
        <p className="text-lg text-gray-800 leading-relaxed font-medium mt-1">
          {page1.primary_concern}
        </p>
      </CardHeader>
      <CardContent className="space-y-6">
        {ambiguityNote ? (
          <Alert>
            <AlertDescription>{ambiguityNote}</AlertDescription>
          </Alert>
        ) : null}

        {coPrimaries.length > 0 && (mode === 'near_tie_ambiguity' || mode === 'technical_tiebreak_lead') ? (
          <div>
            <h3 className="text-sm font-semibold text-gray-700 mb-2 flex items-center gap-2">
              <Microscope className="h-4 w-4" />
              Closely related signals
            </h3>
            <ul className="flex flex-wrap gap-2 list-none p-0 m-0">
              {coPrimaries.map((sid) => (
                <li key={sid}>
                  <Badge variant="outline" className="font-normal text-gray-700">
                    {formatSignalIdForDisplay(sid)}
                  </Badge>
                </li>
              ))}
            </ul>
          </div>
        ) : null}

        {page1.key_findings?.length ? (
          <div>
            <h3 className="text-sm font-semibold text-gray-700 mb-2 flex items-center gap-2">
              <ListOrdered className="h-4 w-4" />
              Key findings
            </h3>
            <ul className="space-y-2">
              {page1.key_findings.map((line, i) => (
                <li key={i} className="text-gray-700 text-sm leading-relaxed pl-1 border-l-2 border-blue-200 pl-3">
                  {line}
                </li>
              ))}
            </ul>
          </div>
        ) : null}

        {page1.top_hypothesis_line ? (
          <div className="rounded-lg bg-slate-50 border border-slate-100 px-4 py-3">
            <h3 className="text-xs font-semibold uppercase tracking-wide text-slate-500 mb-1">Hypothesis & next steps</h3>
            <p className="text-sm text-slate-800 leading-relaxed">{page1.top_hypothesis_line}</p>
          </div>
        ) : null}

        {page1.confidence_and_missing_data ? (
          <div className="rounded-lg bg-amber-50/60 border border-amber-100 px-4 py-3">
            <h3 className="text-xs font-semibold uppercase tracking-wide text-amber-800/90 mb-1">Confidence & gaps</h3>
            <p className="text-sm text-amber-950/90 leading-relaxed whitespace-pre-wrap">
              {page1.confidence_and_missing_data}
            </p>
          </div>
        ) : null}
      </CardContent>
    </Card>
  );
}
