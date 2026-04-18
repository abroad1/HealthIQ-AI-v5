'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Route } from 'lucide-react';

export interface ResultsInvestigationSpineProps {
  /** First clause of lead topic — same source as body overview lead, without tie-break rider. */
  focusLine: string | null;
  /** First governed IDL record (retail + subtitle) — backend strings only. */
  idlRetailLabel: string | null;
  idlSubtitle: string | null;
  className?: string;
}

/**
 * FE-R8B — Above-the-fold investigation spine: connects lead topic to cross-body IDL read
 * using deterministic strings already on the result payload (no new clinical claims).
 */
export function ResultsInvestigationSpine({
  focusLine,
  idlRetailLabel,
  idlSubtitle,
  className = '',
}: ResultsInvestigationSpineProps) {
  const hasIdl = Boolean(idlRetailLabel?.trim() || idlSubtitle?.trim());
  if (!focusLine && !hasIdl) return null;

  return (
    <section
      aria-labelledby="investigation-spine-heading"
      className={className}
      data-testid="results-investigation-spine"
    >
      <Card className="border-indigo-100 bg-gradient-to-b from-indigo-50/50 to-white shadow-sm">
        <CardHeader className="pb-2">
          <CardTitle
            id="investigation-spine-heading"
            className="text-lg font-semibold text-indigo-950 flex items-center gap-2"
          >
            <Route className="h-5 w-5 text-indigo-600 shrink-0" aria-hidden />
            Your investigation path
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4 text-sm text-slate-800 pt-0">
          {focusLine ? (
            <div>
              <p className="text-xs font-semibold uppercase tracking-wide text-indigo-900/85 mb-1">Main focus</p>
              <p className="leading-snug text-base text-slate-900">{focusLine}</p>
            </div>
          ) : null}
          {hasIdl ? (
            <div className="border-t border-indigo-100 pt-3">
              <p className="text-xs font-semibold uppercase tracking-wide text-slate-600 mb-1">
                Pattern read across the body
              </p>
              <p className="leading-snug">
                {idlRetailLabel ? (
                  <span className="font-semibold text-slate-900">{idlRetailLabel.trim()}</span>
                ) : null}
                {idlRetailLabel && idlSubtitle ? <span className="text-slate-500"> — </span> : null}
                {idlSubtitle ? <span className="text-slate-700">{idlSubtitle.trim()}</span> : null}
              </p>
              <p className="text-xs text-slate-500 mt-2">
                The sections below connect this cross-body pattern to your lead finding, stable systems, and markers.
              </p>
            </div>
          ) : null}
        </CardContent>
      </Card>
    </section>
  );
}
