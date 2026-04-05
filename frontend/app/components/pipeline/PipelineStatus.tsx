'use client';

import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { CheckCircle2, AlertTriangle, ClipboardList } from 'lucide-react';
import type { ClinicianConfirmatoryTestItem, ClinicianReportV1 } from '@/types/analysis';

export interface PipelineStatusProps {
  dataQuality: ClinicianReportV1['data_quality'] | null | undefined;
  confirmatoryTests?: ClinicianConfirmatoryTestItem[] | null;
  className?: string;
}

/**
 * User-facing trust layer from backend data_quality + confirmatory cues.
 * Not raw pipeline plumbing — copy explains completeness and caveats in plain language.
 */
export default function PipelineStatus({
  dataQuality,
  confirmatoryTests,
  className = '',
}: PipelineStatusProps) {
  if (!dataQuality) {
    return (
      <Card className={`border-slate-200 ${className}`}>
        <CardHeader className="pb-2">
          <CardTitle className="text-base">Data quality</CardTitle>
          <CardDescription>No data-quality summary was returned for this analysis.</CardDescription>
        </CardHeader>
      </Card>
    );
  }

  const present = dataQuality.panel_completeness_present ?? 0;
  const expected = dataQuality.panel_completeness_expected ?? 0;
  const completenessLabel =
    expected > 0
      ? `We received ${present} of ${expected} expected panel markers for this interpretation.`
      : 'Panel completeness was not scored for this result.';

  const checksPassed = dataQuality.data_quality_passed === true;
  const labQuality = dataQuality.lab_range_quality_by_primary_metric ?? [];
  const tests = confirmatoryTests ?? [];

  return (
    <Card className={`border-slate-200 shadow-sm ${className}`}>
      <CardHeader className="pb-2">
        <div className="flex flex-wrap items-center gap-2">
          <CardTitle className="text-lg">Trust &amp; data quality</CardTitle>
          <Badge variant={checksPassed ? 'default' : 'destructive'} className="font-normal">
            {checksPassed ? 'Quality checks passed' : 'Review quality notes'}
          </Badge>
        </div>
        <CardDescription>{completenessLabel}</CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        {dataQuality.confidence_caveat ? (
          <p className="text-sm text-gray-700 leading-relaxed">{dataQuality.confidence_caveat}</p>
        ) : null}

        {labQuality.length > 0 ? (
          <div>
            <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">Lab-range coverage (primary metrics)</h3>
            <ul className="text-sm text-gray-700 space-y-1 list-disc pl-5">
              {labQuality.map((line, i) => (
                <li key={i}>{line}</li>
              ))}
            </ul>
          </div>
        ) : null}

        {!checksPassed ? (
          <Alert variant="destructive">
            <AlertTriangle className="h-4 w-4" />
            <AlertDescription>
              Some data-quality checks did not pass. Treat the interpretation cautiously and consider repeating
              labs or supplying missing markers if your clinician agrees.
            </AlertDescription>
          </Alert>
        ) : (
          <div className="flex items-start gap-2 text-sm text-green-800 bg-green-50 border border-green-100 rounded-md p-3">
            <CheckCircle2 className="h-5 w-5 flex-shrink-0 mt-0.5" />
            <span>Core data-quality checks passed for this run.</span>
          </div>
        )}

        {tests.length > 0 ? (
          <div>
            <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2 flex items-center gap-2">
              <ClipboardList className="h-4 w-4" />
              Confirmatory tests to discuss with your clinician
            </h3>
            <ul className="space-y-3">
              {tests.slice(0, 5).map((t) => (
                <li key={t.test_id} className="text-sm border border-gray-100 rounded-md p-3 bg-gray-50/80">
                  <div className="font-medium text-gray-900">{t.display_name}</div>
                  <p className="text-gray-600 mt-1 leading-relaxed">{t.rationale}</p>
                </li>
              ))}
            </ul>
            {tests.length > 5 ? (
              <p className="text-xs text-gray-500 mt-2">Additional tests are listed in the full clinician report.</p>
            ) : null}
          </div>
        ) : null}
      </CardContent>
    </Card>
  );
}
