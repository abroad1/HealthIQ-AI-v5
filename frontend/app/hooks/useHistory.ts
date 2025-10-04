/**
 * Custom hook for managing analysis history.
 * TODO: Implement actual Supabase integration in Sprint 9b.
 */

import { useState, useEffect } from 'react';
import { getAnalysisHistory, AnalysisHistoryItem, HistoryResponse } from '../services/history';

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
 * Hook for managing analysis history.
 * @param userId - User ID
 * @param options - Hook options
 * @returns UseHistoryReturn
 */
export function useHistory(
  userId?: string,
  options: UseHistoryOptions = {}
): UseHistoryReturn {
  const { page = 1, limit = 10, autoFetch = true } = options;
  
  const [analyses, setAnalyses] = useState<AnalysisHistoryItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [total, setTotal] = useState(0);
  const [currentPage, setCurrentPage] = useState(page);

  const loadAnalyses = async (userIdParam: string, pageParam?: number, limitParam?: number) => {
    if (!userIdParam) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const response = await getAnalysisHistory(userIdParam, pageParam || currentPage, limitParam || limit);
      setAnalyses(response.history);
      setTotal(response.total);
      if (pageParam) {
        setCurrentPage(pageParam);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch history');
    } finally {
      setLoading(false);
    }
  };

  const fetchHistory = async () => {
    if (userId) {
      await loadAnalyses(userId, currentPage, limit);
    }
  };

  useEffect(() => {
    if (autoFetch && userId) {
      fetchHistory();
    }
  }, [userId, currentPage, limit, autoFetch]);

  const nextPage = () => {
    if (currentPage * limit < total) {
      setCurrentPage(prev => prev + 1);
    }
  };

  const prevPage = () => {
    if (currentPage > 1) {
      setCurrentPage(prev => prev - 1);
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
    refetch: fetchHistory,
    nextPage,
    prevPage
  };
}
