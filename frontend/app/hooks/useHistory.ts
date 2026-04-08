/**
 * Analysis history from the authenticated API (owner-scoped).
 */

import { useState, useEffect, useRef } from 'react';
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
  loadAnalyses: (pageParam?: number) => Promise<void>;
  refetch: () => Promise<void>;
  nextPage: () => void;
  prevPage: () => void;
}

export function useHistory(options: UseHistoryOptions = {}): UseHistoryReturn {
  const { page = 1, limit = 10, autoFetch = true } = options;

  const [analyses, setAnalyses] = useState<AnalysisHistoryItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [total, setTotal] = useState(0);
  const [currentPage, setCurrentPage] = useState(page);
  const pageRef = useRef(currentPage);
  const autoFetchRef = useRef(autoFetch);

  pageRef.current = currentPage;
  autoFetchRef.current = autoFetch;

  const runFetch = async (pageNum: number) => {
    setLoading(true);
    setError(null);
    try {
      const offset = (pageNum - 1) * limit;
      const response = await AnalysisService.getAnalysisHistory(limit, offset);
      if (response.success && response.data) {
        setAnalyses(response.data.history);
        setTotal(response.data.total);
      } else {
        setAnalyses([]);
        setTotal(0);
        setError(response.error ?? 'Failed to fetch history');
      }
    } catch (err) {
      setAnalyses([]);
      setTotal(0);
      setError(err instanceof Error ? err.message : 'Failed to fetch history');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (!autoFetch) return;
    void runFetch(currentPage);
    // eslint-disable-next-line react-hooks/exhaustive-deps -- run when page/limit/autoFetch change only
  }, [autoFetch, currentPage, limit]);

  const loadAnalyses = async (pageParam?: number) => {
    if (pageParam !== undefined) {
      setCurrentPage(pageParam);
      if (!autoFetchRef.current) {
        await runFetch(pageParam);
      }
      return;
    }
    await runFetch(pageRef.current);
  };

  const refetch = async () => {
    await runFetch(pageRef.current);
  };

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
