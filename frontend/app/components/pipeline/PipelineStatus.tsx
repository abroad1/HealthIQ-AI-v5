'use client';

import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Button } from '@/components/ui/button';
import { CheckCircle2, AlertTriangle, ClipboardList, ChevronDown, ChevronUp } from 'lucide-react';
import type { ClinicianConfirmatoryTestItem, ClinicianReportV1 } from '@/types/analysis';

export interface PipelineStatusProps {
  dataQuality: ClinicianReportV1['data_quality'] | null | undefined;
  confirmatoryTests?: ClinicianConfirmatoryTestItem[] | null;
  /** Line 2 cue only when Missing Chapter threshold met (computed by results page) */
  missingChapterLine?: string | null;
  className?: string;
}

function truncateText(text: string, maxLen: number): string {
  const t = text.trim();
  if (t.length <= maxLen) return t;
  return `${t.slice(0, maxLen - 1)}…`;
}

/**
 * Trust strip — max 2 plain-language lines by default; detail behind reveal (wireframe §3).
 */
export default function PipelineStatus({
  dataQuality,
  confirmatoryTests,
  missingChapterLine,
  className = '',
}: PipelineStatusProps) {
  const [revealed, setRevealed] = useState(false);

  if (!dataQuality) {
    return (
      <Card className={`border-slate-200 ${className}`}>
        <CardHeader className="pb-2">
          <CardTitle className="text-base">Trust strip</CardTitle>
          <CardDescription>No data-quality summary was returned for this analysis.</CardDescription>
        </CardHeader>
      </Card>
    );
  }

  const present = dataQuality.panel_completeness_present ?? 0;
  const expected = dataQuality.panel_completeness_expected ?? 0;
  const checksPassed = dataQuality.data_quality_passed === true;
  const labQuality = dataQuality.lab_range_quality_by_primary_metric ?? [];
  const tests = confirmatoryTests ?? [];
  const caveat = (dataQuality.confidence_caveat || '').trim();

  const line1 =
    expected > 0
      ? `We received ${present} of ${expected} expected markers for this interpretation.${
          checksPassed ? ' Core quality checks passed.' : ' Review the notes below before relying on the headline.'
        }`
      : 'Panel completeness was not scored for this result.';

  const line2 =
    (missingChapterLine && missingChapterLine.trim()) ||
    (!checksPassed && caveat ? truncateText(caveat, 160) : null);

  return (
    <Card className={`border-slate-200 shadow-sm ${className}`}>
      <CardHeader className="pb-2">
        <div className="flex flex-wrap items-center gap-2">
          <CardTitle className="text-lg">Trust strip</CardTitle>
          <Badge variant={checksPassed ? 'default' : 'destructive'} className="font-normal">
            {checksPassed ? 'Quality checks passed' : 'Review quality notes'}
          </Badge>
        </div>
        <CardDescription className="text-gray-700">{line1}</CardDescription>
      </CardHeader>
      <CardContent className="space-y-3">
        {line2 ? (
          <p className="text-sm text-gray-800 leading-relaxed border-l-2 border-amber-200 pl-3">{line2}</p>
        ) : null}

        <div className="flex flex-wrap items-center gap-2">
          <Button
            type="button"
            variant="ghost"
            size="sm"
            className="text-blue-700 -ml-2"
            onClick={() => setRevealed((r) => !r)}
            aria-expanded={revealed}
          >
            {revealed ? (
              <>
                <ChevronUp className="h-4 w-4 mr-1" /> Less detail
              </>
            ) : (
              <>
                <ChevronDown className="h-4 w-4 mr-1" /> More detail
              </>
            )}
          </Button>
        </div>

        {revealed ? (
          <div className="space-y-4 pt-2 border-t border-slate-100">
            {caveat && (!line2 || caveat !== missingChapterLine) ? (
              <p className="text-sm text-gray-700 leading-relaxed whitespace-pre-wrap">{caveat}</p>
            ) : null}

            {missingChapterLine && line2 !== missingChapterLine.trim() ? (
              <div className="rounded-md bg-amber-50/80 border border-amber-100 px-3 py-2 text-sm text-amber-950">
                <span className="font-semibold">Missing chapter:</span> {missingChapterLine}
              </div>
            ) : null}

            {labQuality.length > 0 ? (
              <div>
                <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">
                  Lab-range coverage (primary metrics)
                </h3>
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
                  {tests.slice(0, 8).map((t) => (
                    <li key={t.test_id} className="text-sm border border-gray-100 rounded-md p-3 bg-gray-50/80">
                      <div className="font-medium text-gray-900">{t.display_name}</div>
                      <p className="text-gray-600 mt-1 leading-relaxed">{t.rationale}</p>
                    </li>
                  ))}
                </ul>
                {tests.length > 8 ? (
                  <p className="text-xs text-gray-500 mt-2">Additional tests are listed in the clinician report inside Advanced analysis.</p>
                ) : null}
              </div>
            ) : null}
          </div>
        ) : null}
      </CardContent>
    </Card>
  );
}
