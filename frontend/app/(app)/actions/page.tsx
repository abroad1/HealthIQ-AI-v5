'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { ArrowRight, ListChecks, Loader2, Upload } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { AnalysisService } from '@/services/analysis';
import { buildActionCardModels, type ResultActionCardModel } from '@/lib/resultsPageLayout';
import { ActionHubCardList } from '@/components/actions/ActionHubCardList';

const DISCLAIMER =
  'HealthIQ is for information and education only. It is not a medical diagnosis and does not replace advice from a qualified clinician.';

type LoadState = 'loading' | 'ready' | 'empty' | 'error';
/** `no-recs` = completed analysis exists but no recommendation lines in DTO. */
type EmptyKind = 'no-completed' | 'no-recs' | null;

export default function ActionsPage() {
  const [loadState, setLoadState] = useState<LoadState>('loading');
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [actions, setActions] = useState<ResultActionCardModel[]>([]);
  const [contextLine, setContextLine] = useState<string | null>(null);
  const [emptyKind, setEmptyKind] = useState<EmptyKind>(null);

  useEffect(() => {
    let cancelled = false;

    (async () => {
      setLoadState('loading');
      setErrorMessage(null);

      const histRes = await AnalysisService.getAnalysisHistory(30, 0);
      if (cancelled) return;

      if (!histRes.success || !histRes.data) {
        setErrorMessage(histRes.error || 'Could not load your analysis history.');
        setLoadState('error');
        return;
      }

      const history = histRes.data.history || [];
      const completed = history.find((h) => h.status === 'completed');
      if (!completed) {
        setEmptyKind('no-completed');
        setLoadState('empty');
        return;
      }

      const resultRes = await AnalysisService.getAnalysisResult(completed.id);
      if (cancelled) return;

      if (!resultRes.success || !resultRes.data) {
        setErrorMessage(resultRes.error || 'Could not load that analysis.');
        setLoadState('error');
        return;
      }

      const data = resultRes.data;
      const models = buildActionCardModels(data.clusters || [], data.recommendations, {
        maxItems: 8,
      });

      const when = data.completed_at || data.created_at || completed.created_at;
      const dateLabel = when ? new Date(when).toLocaleDateString() : '';
      setContextLine(
        dateLabel
          ? `Based on your most recent completed analysis (${dateLabel}).`
          : 'Based on your most recent completed analysis.'
      );

      setActions(models);
      if (models.length > 0) {
        setEmptyKind(null);
        setLoadState('ready');
      } else {
        setEmptyKind('no-recs');
        setLoadState('empty');
      }
    })();

    return () => {
      cancelled = true;
    };
  }, []);

  return (
    <div className="container mx-auto max-w-5xl px-4 py-10">
      <div className="mb-8 flex flex-col gap-3 md:flex-row md:items-end md:justify-between">
        <div>
          <div className="flex items-center gap-2 text-indigo-700 mb-1">
            <ListChecks className="h-6 w-6" aria-hidden />
            <span className="text-sm font-semibold uppercase tracking-wide">Actions hub</span>
          </div>
          <h1 className="text-3xl font-bold text-slate-900">Recommended next steps</h1>
          <p className="text-slate-600 mt-2 max-w-2xl">
            Practical follow-ups derived from your latest completed blood test result—grouped for clarity, not a treatment
            plan.
          </p>
        </div>
        <Button asChild variant="outline" size="sm">
          <Link href="/results">
            Back to results
            <ArrowRight className="h-4 w-4 ml-2" />
          </Link>
        </Button>
      </div>

      {loadState === 'loading' ? (
        <div className="flex items-center gap-2 text-slate-600 py-12">
          <Loader2 className="h-5 w-5 animate-spin" aria-hidden />
          <span>Loading recommendations…</span>
        </div>
      ) : null}

      {loadState === 'error' ? (
        <Card className="border-amber-200 bg-amber-50/40">
          <CardHeader>
            <CardTitle className="text-lg">Something went wrong</CardTitle>
            <CardDescription>{errorMessage}</CardDescription>
          </CardHeader>
          <CardContent>
            <Button asChild variant="default">
              <Link href="/upload">Go to upload</Link>
            </Button>
          </CardContent>
        </Card>
      ) : null}

      {loadState === 'empty' ? (
        <Card className="border-slate-200">
          <CardHeader>
            <CardTitle className="text-lg">No actions to show yet</CardTitle>
            <CardDescription>
              {emptyKind === 'no-completed'
                ? 'Complete a blood test analysis first. When a run finishes, recommended follow-ups from that result can appear here.'
                : 'Your latest completed analysis did not include structured recommendation lines in the data we receive. Open your full results for narrative and system-level guidance.'}
            </CardDescription>
          </CardHeader>
          <CardContent className="flex flex-wrap gap-2">
            <Button asChild>
              <Link href="/upload">
                <Upload className="h-4 w-4 mr-2" />
                Upload a blood test
              </Link>
            </Button>
            <Button asChild variant="outline">
              <Link href="/results">Open results</Link>
            </Button>
          </CardContent>
        </Card>
      ) : null}

      {loadState === 'ready' ? (
        <>
          {contextLine ? <p className="text-sm text-slate-600 mb-4">{contextLine}</p> : null}
          <ActionHubCardList actions={actions} />
        </>
      ) : null}

      <p className="mt-10 text-xs text-slate-500 border-t border-slate-200 pt-4 max-w-3xl leading-relaxed">{DISCLAIMER}</p>
    </div>
  );
}
