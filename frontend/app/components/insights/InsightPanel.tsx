'use client';

import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Sparkles } from 'lucide-react';
import type { ClinicianReportV1, PrimaryConcernModeV1 } from '@/types/analysis';

export interface InsightPanelProps {
  report: ClinicianReportV1 | null | undefined;
  /** Retail label for the Primary Driver System Group — visual thread only */
  primaryDriverSystemGroupName?: string | null;
  className?: string;
}

function formatSignalIdForDisplay(signalId: string): string {
  const stripped = signalId.replace(/^signal_/, '').replace(/_/g, ' ');
  return stripped.replace(/\b\w/g, (c) => c.toUpperCase());
}

function modeLabel(mode: PrimaryConcernModeV1 | undefined): { label: string; variant: 'default' | 'secondary' | 'outline' | 'destructive' } {
  switch (mode) {
    case 'near_tie_ambiguity':
      return { label: 'Several top findings are close', variant: 'outline' };
    case 'technical_tiebreak_lead':
      return { label: 'Close call between top findings', variant: 'secondary' };
    case 'distinct_lead':
    default:
      return { label: 'Clear lead topic', variant: 'default' };
  }
}

function modeAudienceNote(mode: PrimaryConcernModeV1 | undefined): string | null {
  if (mode === 'near_tie_ambiguity') {
    return 'More than one pattern may be similarly important. The headline shows one first for clarity—not that the others are unimportant.';
  }
  if (mode === 'technical_tiebreak_lead') {
    return 'Two or more findings scored similarly; the summary picks a single lead so the story has a clear starting point.';
  }
  return null;
}

/**
 * Hero interpretation — locked to four copy blocks per FE-VISUALISATION-B2 / wireframe §2.
 * key_findings list is not rendered here; defer fuller lists to Advanced Analysis.
 */
export function InsightPanel({
  report,
  primaryDriverSystemGroupName,
  className = '',
}: InsightPanelProps) {
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
            A structured clinical summary is not available for this result yet. Use System Groups and markers below,
            or open Advanced analysis when present.
          </CardDescription>
        </CardHeader>
      </Card>
    );
  }

  const mode = page1.primary_concern_mode;
  const { label: modeText, variant: modeVariant } = modeLabel(mode);
  const ambiguityNote = modeAudienceNote(mode);
  const coPrimaries = page1.co_primary_signal_ids?.filter(Boolean) ?? [];

  const headline = (page1.primary_concern || '').trim();
  const interpretationParagraph = (page1.key_findings?.[0] || '').trim();
  const confidenceLine = (page1.confidence_and_missing_data || '').trim();
  const nextStepCue = (page1.top_hypothesis_line || '').trim();

  const showCoPrimaryRow =
    coPrimaries.length > 0 && (mode === 'near_tie_ambiguity' || mode === 'technical_tiebreak_lead');

  return (
    <Card
      className={`border-blue-100 shadow-md ${primaryDriverSystemGroupName ? 'border-l-4 border-l-blue-500' : ''} ${className}`}
    >
      <CardHeader className="pb-2">
        <div className="flex flex-wrap items-center gap-2 mb-2">
          <CardTitle className="flex items-center gap-2 text-2xl font-semibold tracking-tight text-gray-900 mr-auto">
            <Sparkles className="h-7 w-7 text-blue-600 flex-shrink-0" />
            Hero interpretation
          </CardTitle>
          <Badge variant={modeVariant}>{modeText}</Badge>
          {page1.ranking_policy_version ? (
            <span className="sr-only">Ranking policy reference: {page1.ranking_policy_version}</span>
          ) : null}
        </div>
        {primaryDriverSystemGroupName ? (
          <p className="text-xs font-medium text-blue-800 mb-1">
            Primary driver system group: <span className="font-semibold">{primaryDriverSystemGroupName}</span>
          </p>
        ) : null}
      </CardHeader>
      <CardContent className="space-y-4 pt-0">
        {showCoPrimaryRow ? (
          <p className="text-sm text-gray-600">
            <span className="font-medium text-gray-700">Also closely reviewed: </span>
            {coPrimaries.map((sid) => formatSignalIdForDisplay(sid)).join(' · ')}
          </p>
        ) : null}

        {ambiguityNote ? (
          <p className="text-sm text-gray-600 bg-slate-50 border border-slate-100 rounded-md px-3 py-2">{ambiguityNote}</p>
        ) : null}

        {/* 1 headline line */}
        <h2 className="text-xl font-semibold text-gray-900 leading-snug line-clamp-2 md:line-clamp-1" title={headline}>
          {headline || '—'}
        </h2>

        {/* 1 interpretation paragraph */}
        {interpretationParagraph ? (
          <p className="text-base text-gray-800 leading-relaxed">{interpretationParagraph}</p>
        ) : null}

        {/* 1 confidence qualifier line */}
        {confidenceLine ? (
          <p className="text-sm text-amber-900/90 leading-relaxed border-l-2 border-amber-200 pl-3">{confidenceLine}</p>
        ) : null}

        {/* 1 next-step cue max */}
        {nextStepCue ? (
          <p className="text-sm text-slate-800 leading-relaxed rounded-lg bg-slate-50 border border-slate-100 px-4 py-3">
            <span className="text-xs font-semibold uppercase tracking-wide text-slate-500 block mb-1">Next step</span>
            {nextStepCue}
          </p>
        ) : null}
      </CardContent>
    </Card>
  );
}
