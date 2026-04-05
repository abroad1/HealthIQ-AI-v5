/**
 * Hook for authenticated persisted analysis history (FE-PERSISTENCE-B).
 */

import { useState, useEffect, useCallback } from 'react';
import { AnalysisService } from '../services/analysis';
import type { AnalysisHistoryItem } from '../types/analysis';

export interface UseHistoryOptions {
  page?: number;
  limit?: number;
  autoFetch?: boolean;
}

export interface UseHistoryReturn {
  analyses: AnalysisHistoryItem[];
  loading: boolean;
  error: string | null;
  total: number;
  page: number;
  limit: number;
  loadAnalyses: (userId: string, page?: number, limit?: number) => Promise<void>;
  refetch: () => Promise<void>;
  nextPage: () => void;
  prevPage: () => void;
}

/**
 * @param userId When truthy, enables fetch (e.g. current auth user id from /me). Not passed to API.
 */
export function useHistory(
  userId?: string,
  options: UseHistoryOptions = {},
): UseHistoryReturn {
  const { page = 1, limit = 10, autoFetch = true } = options;

  const [analyses, setAnalyses] = useState<AnalysisHistoryItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [total, setTotal] = useState(0);
  const [currentPage, setCurrentPage] = useState(page);

  const loadAnalyses = useCallback(
    async (userIdParam: string, pageParam?: number, limitParam?: number) => {
      if (!userIdParam) return;

      setLoading(true);
      setError(null);

      try {
        const pageNum = pageParam ?? currentPage;
        const lim = limitParam ?? limit;
        const offset = (pageNum - 1) * lim;
        const res = await AnalysisService.getAnalysisHistory(lim, offset);
        if (!res.success || !res.data) {
          throw new Error(res.error || 'Failed to fetch history');
        }
        setAnalyses(res.data.history);
        setTotal(res.data.total);
        if (pageParam !== undefined) {
          setCurrentPage(pageParam);
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch history');
      } finally {
        setLoading(false);
      }
    },
    [currentPage, limit],
  );

  const refetch = useCallback(async () => {
    if (userId) {
      await loadAnalyses(userId, currentPage, limit);
    }
  }, [userId, currentPage, limit, loadAnalyses]);

  useEffect(() => {
    if (autoFetch && userId) {
      void loadAnalyses(userId, currentPage, limit);
    }
  }, [userId, currentPage, limit, autoFetch, loadAnalyses]);

  const nextPage = () => {
    if (currentPage * limit < total) {
      setCurrentPage((prev) => prev + 1);
    }
  };

  const prevPage = () => {
    if (currentPage > 1) {
      setCurrentPage((prev) => prev - 1);
    }
  };

  return {
    analyses,
    loading,
    error,
    total,
    page: currentPage,
    limit,
    loadAnalyses,
    refetch,
    nextPage,
    prevPage,
  };
}
