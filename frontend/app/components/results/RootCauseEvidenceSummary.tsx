'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import type { ClinicianReportV1 } from '@/types/analysis';

function formatMarkerRef(id: string): string {
  return id.replace(/_/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase());
}

function formatSignalIdForDisplay(signalId: string): string {
  const stripped = signalId.replace(/^signal_/, '').replace(/_/g, ' ');
  return stripped.replace(/\b\w/g, (c) => c.toUpperCase());
}

function stateConsumerPhrase(state: string): string {
  const key = (state || '').trim().toLowerCase();
  const phrases: Record<string, string> = {
    at_risk: 'warrants attention on this panel',
    suboptimal: 'is outside the optimal range on this panel',
    optimal: 'looks favourable on this panel',
    unknown: 'is not fully characterised from this panel alone',
  };
  return phrases[key] ?? `is described as ${key.replace(/_/g, ' ')} on this panel`;
}

interface RootCauseEvidenceSummaryProps {
  report: ClinicianReportV1 | null | undefined;
}

/**
 * Surfaces supporting / contradictory / missing structured evidence for the top hypothesis
 * (deterministic compiler output — no extra medical claims).
 */
export function RootCauseEvidenceSummary({ report }: RootCauseEvidenceSummaryProps) {
  const rc = report?.sections?.root_cause;
  const top = rc?.hypotheses?.[0];
  if (!top) return null;

  const supporting = top.evidence_for ?? [];
  const opposing = top.evidence_against ?? [];
  const gaps = top.missing_data ?? [];

  const summaryText = (top.summary || '').trim();
  const rankingText = (top.ranking_rationale || '').trim();
  const patternLine = rc
    ? `${formatSignalIdForDisplay(rc.signal_id)} ${stateConsumerPhrase(rc.signal_state)}` +
      (rc.primary_metric
        ? ` Your main lab anchor on this thread is ${formatMarkerRef(rc.primary_metric)}.`
        : '')
    : '';

  if (
    supporting.length === 0 &&
    opposing.length === 0 &&
    gaps.length === 0 &&
    !summaryText &&
    !rankingText &&
    !patternLine
  ) {
    return null;
  }

  return (
    <Card className="border-slate-200 bg-white shadow-sm" data-testid="root-cause-evidence-summary">
      <CardHeader className="pb-2">
        <CardTitle className="text-base font-semibold text-gray-900">Why this hypothesis leads</CardTitle>
        <p className="text-sm text-gray-600">
          A concise walkthrough of the lead interpretation —{' '}
          <span className="font-medium text-gray-800">{top.title}</span> — using the same structured evidence as the
          clinician report (deterministic compiler output).
        </p>
      </CardHeader>
      <CardContent className="space-y-4 text-sm text-gray-800">
        {patternLine ? (
          <div className="rounded-md border border-slate-100 bg-slate-50/80 px-3 py-2 space-y-1">
            <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">Pattern</p>
            <p>{patternLine}</p>
          </div>
        ) : null}

        {summaryText ? (
          <div className="space-y-1">
            <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">What this means</p>
            <p className="leading-relaxed">{summaryText}</p>
          </div>
        ) : null}

        {rankingText ? (
          <div className="rounded-md border border-indigo-100 bg-indigo-50/50 px-3 py-2 space-y-1">
            <p className="text-xs font-semibold uppercase tracking-wide text-indigo-800">How this ranks on this panel</p>
            <p className="text-indigo-950 leading-relaxed">{rankingText}</p>
          </div>
        ) : null}

        {supporting.length > 0 ? (
          <div>
            <p className="font-medium text-green-900 mb-1">Supports this interpretation</p>
            <ul className="list-disc pl-5 space-y-1">
              {supporting.map((ev, i) => (
                <li key={`f-${i}`}>
                  {ev.item}
                  {ev.marker_refs && ev.marker_refs.length > 0 ? (
                    <span className="text-gray-600">
                      {' '}
                      (markers: {ev.marker_refs.map(formatMarkerRef).join(', ')})
                    </span>
                  ) : null}
                </li>
              ))}
            </ul>
          </div>
        ) : null}

        {opposing.length > 0 ? (
          <div>
            <p className="font-medium text-amber-900 mb-1">Pulls against or complicates it</p>
            <ul className="list-disc pl-5 space-y-1">
              {opposing.map((ev, i) => (
                <li key={`a-${i}`}>
                  {ev.item}
                  {ev.marker_refs && ev.marker_refs.length > 0 ? (
                    <span className="text-gray-600">
                      {' '}
                      (markers: {ev.marker_refs.map(formatMarkerRef).join(', ')})
                    </span>
                  ) : null}
                </li>
              ))}
            </ul>
          </div>
        ) : null}

        {gaps.length > 0 ? (
          <div>
            <p className="font-medium text-slate-800 mb-1">Not on this panel (limits confidence)</p>
            <ul className="list-disc pl-5 space-y-1">
              {gaps.map((m, i) => (
                <li key={`m-${i}`}>
                  <span className="font-medium">{formatMarkerRef(m.marker_id)}:</span> {m.reason}
                </li>
              ))}
            </ul>
          </div>
        ) : null}
      </CardContent>
    </Card>
  );
}
