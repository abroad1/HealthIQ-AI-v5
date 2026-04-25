'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Route } from 'lucide-react';

export interface ResultsInvestigationSpineProps {
  /**
   * FE-R8C — Optional first visible IDL retail label: named once as a pointer to Section 5
   * (no subtitle/body duplicate here).
   */
  crossBodyPatternLabel: string | null;
  className?: string;
}

/**
 * FE-R8B / FE-R8C — Directional bridge only: orients the scroll order without restating
 * the lead sentence (Body overview + Primary finding own that thread).
 */
export function ResultsInvestigationSpine({
  crossBodyPatternLabel,
  className = '',
}: ResultsInvestigationSpineProps) {
  return (
    <section
      aria-labelledby="investigation-spine-heading"
      className={className}
      data-testid="results-investigation-spine"
    >
      <Card className="border-slate-200 bg-slate-50/40 shadow-sm">
        <CardHeader className="pb-2">
          <CardTitle
            id="investigation-spine-heading"
            className="text-base font-semibold text-slate-900 flex items-center gap-2"
          >
            <Route className="h-5 w-5 text-slate-600 shrink-0" aria-hidden />
            Your investigation path
          </CardTitle>
        </CardHeader>
        <CardContent className="pt-0">
          <p className="text-sm text-slate-700 leading-relaxed">
            <span className="font-medium text-slate-900">Primary finding</span> states the headline read for this
            panel. Next: what looks stable, the lead finding and evidence, why that lead ranked, then{' '}
            <span className="font-medium text-slate-900">Patterns across your body</span>
            {crossBodyPatternLabel ? (
              <>
                {' '}
                (including <span className="font-medium text-slate-900">{crossBodyPatternLabel}</span>)
              </>
            ) : null}
            , then deeper evidence—each block adds detail instead of repeating the same headline.
          </p>
        </CardContent>
      </Card>
    </section>
  );
}
