'use client';

import { Badge } from '@/components/ui/badge';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import type { ResultActionCardModel } from '@/lib/resultsPageLayout';
import { twoSentenceExcerpt } from '@/lib/actionsHub';

export function ActionHubCardList({ actions }: { actions: ResultActionCardModel[] }) {
  return (
    <ul className="grid gap-4 md:grid-cols-1 lg:grid-cols-2" data-testid="actions-hub-cards">
      {actions.map((a, i) => (
        <li key={`${a.heading}-${i}`}>
          <Card className="border-slate-200 h-full shadow-sm">
            <CardHeader className="pb-2 space-y-2">
              <div className="flex flex-wrap items-start justify-between gap-2">
                <CardTitle className="text-base font-semibold text-slate-900 leading-snug pr-2">{a.heading}</CardTitle>
                <Badge variant="secondary" className="shrink-0 font-normal text-xs">
                  {a.categoryLabel}
                </Badge>
              </div>
              <CardDescription className="text-xs font-medium text-slate-600">Evidence: {a.evidenceLevelLabel}</CardDescription>
            </CardHeader>
            <CardContent className="space-y-2 pt-0">
              <p className="text-sm text-slate-700 leading-relaxed">{twoSentenceExcerpt(a.paragraph)}</p>
              <p className="text-xs text-slate-500 border-t border-slate-100 pt-2">
                Source: {a.sourceLabel}
              </p>
            </CardContent>
          </Card>
        </li>
      ))}
    </ul>
  );
}
