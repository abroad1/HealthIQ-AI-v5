'use client';

/**
 * Single source of truth for analysis result fetching.
 * Exactly one useQuery per analysis_id; no duplicate fetches.
 */
import { useEffect } from 'react';
import { useQuery } from '@tanstack/react-query';
import { AnalysisService } from '../services/analysis';
import { useAnalysisStore } from '../state/analysisStore';
import type { AnalysisResult } from '../types/analysis';

const QUERY_KEY_PREFIX = 'analysisResult' as const;

export function getAnalysisResultQueryKey(analysisId: string) {
  return [QUERY_KEY_PREFIX, analysisId] as const;
}

async function fetchAnalysisResult(analysisId: string) {
  const response = await AnalysisService.getAnalysisResult(analysisId);
  if (!response.success || !response.data) {
    throw new Error(response.error || 'Failed to fetch analysis result');
  }
  return response.data as AnalysisResult;
}

/**
 * Single hook that owns result retrieval for a given analysis_id.
 * - Enabled only when analysisId is truthy
 * - Fetches once per analysis_id; cached by TanStack Query
 * - Syncs result to analysis store when data arrives (for components using store)
 */
export function useAnalysisResult(analysisId: string | null) {
  const setCurrentAnalysis = useAnalysisStore((s) => s.setCurrentAnalysis);
  const addToHistory = useAnalysisStore((s) => s.addToHistory);

  const query = useQuery({
    queryKey: getAnalysisResultQueryKey(analysisId!),
    queryFn: () => fetchAnalysisResult(analysisId!),
    enabled: !!analysisId,
    staleTime: 60000,
    refetchOnWindowFocus: false,
    refetchOnMount: false,
    retry: 1,
  });

  // Sync to store when data arrives (single source: components read from store)
  useEffect(() => {
    if (query.data) {
      const analysisData = {
        ...query.data,
        status: 'completed' as const,
        progress: 100,
      };
      setCurrentAnalysis(analysisData);
      addToHistory(analysisData);
    }
  }, [query.data, setCurrentAnalysis, addToHistory]);

  return {
    data: query.data,
    error: query.error,
    isLoading: query.isFetching && query.isLoading,
    isSuccess: query.isSuccess,
    isError: query.isError,
    refetch: query.refetch,
  };
}
