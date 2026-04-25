/**
 * Loads the two most recent completed analyses and builds longitudinal biomarker rows.
 */

import { useState, useEffect } from 'react';
import { AnalysisService } from '@/services/analysis';
import type { AnalysisHistoryItem, AnalysisResult } from '@/types/analysis';
import {
  buildBiomarkerTrendRows,
  sortCompletedHistoryNewestFirst,
  type BiomarkerTrendRow,
} from '@/lib/trendComparison';

export type TrendDataState =
  | { status: 'loading' }
  | { status: 'error'; message: string }
  | { status: 'insufficient'; completedCount: number }
  | {
      status: 'ready';
      rows: BiomarkerTrendRow[];
      recent: AnalysisResult;
      previous: AnalysisResult;
      recentItem: AnalysisHistoryItem;
      previousItem: AnalysisHistoryItem;
      completedCount: number;
    };

const HISTORY_LIMIT = 50;

export function useTrendData(enabled = true): TrendDataState {
  const [state, setState] = useState<TrendDataState>({ status: 'loading' });

  useEffect(() => {
    if (!enabled) {
      setState({ status: 'insufficient', completedCount: 0 });
      return;
    }

    let cancelled = false;

    (async () => {
      setState({ status: 'loading' });

      const histRes = await AnalysisService.getAnalysisHistory(HISTORY_LIMIT, 0);
      if (cancelled) return;

      if (!histRes.success || !histRes.data) {
        setState({
          status: 'error',
          message: histRes.error || 'Could not load your analysis history.',
        });
        return;
      }

      const completed = sortCompletedHistoryNewestFirst(histRes.data.history || []);

      if (completed.length < 2) {
        setState({ status: 'insufficient', completedCount: completed.length });
        return;
      }

      const recentItem = completed[0];
      const previousItem = completed[1];

      const [recentRes, previousRes] = await Promise.all([
        AnalysisService.getAnalysisResult(recentItem.id),
        AnalysisService.getAnalysisResult(previousItem.id),
      ]);

      if (cancelled) return;

      if (!recentRes.success || !recentRes.data) {
        setState({
          status: 'error',
          message: recentRes.error || 'Could not load your latest analysis result.',
        });
        return;
      }
      if (!previousRes.success || !previousRes.data) {
        setState({
          status: 'error',
          message: previousRes.error || 'Could not load your previous analysis result.',
        });
        return;
      }

      const rows = buildBiomarkerTrendRows(recentRes.data, previousRes.data);

      setState({
        status: 'ready',
        rows,
        recent: recentRes.data,
        previous: previousRes.data,
        recentItem,
        previousItem,
        completedCount: completed.length,
      });
    })();

    return () => {
      cancelled = true;
    };
  }, [enabled]);

  return state;
}
