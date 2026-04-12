'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import type { ClinicianReportV1 } from '@/types/analysis';

function formatMarkerRef(id: string): string {
  return id.replace(/_/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase());
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

  if (supporting.length === 0 && opposing.length === 0 && gaps.length === 0) {
    return null;
  }

  return (
    <Card className="border-slate-200 bg-white shadow-sm">
      <CardHeader className="pb-2">
        <CardTitle className="text-base font-semibold text-gray-900">Evidence for the lead hypothesis</CardTitle>
        <p className="text-sm text-gray-600">
          Based on <span className="font-medium text-gray-800">{top.title}</span> — how markers on this panel line
          up, and what is not measured here.
        </p>
      </CardHeader>
      <CardContent className="space-y-4 text-sm text-gray-800">
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
