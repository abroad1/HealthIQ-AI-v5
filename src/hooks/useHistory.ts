/**
 * Custom hook for managing analysis history.
 * TODO: Implement actual Supabase integration in Sprint 9b.
 */

import { useState, useEffect, useCallback } from 'react';
import { getAnalysisHistory, AnalysisHistoryItem, HistoryResponse } from '../services/history';

export interface UseHistoryOptions {
  page?: number;
  limit?: number;
  autoFetch?: boolean;
}

export interface UseHistoryReturn {
  history: AnalysisHistoryItem[];
  loading: boolean;
  error: string | null;
  total: number;
  page: number;
  limit: number;
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
  userId: string,
  options: UseHistoryOptions = {}
): UseHistoryReturn {
  const { page = 1, limit = 10, autoFetch = true } = options;
  
  const [history, setHistory] = useState<AnalysisHistoryItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [total, setTotal] = useState(0);
  const [currentPage, setCurrentPage] = useState(page);

  const fetchHistory = useCallback(async () => {
    if (!userId) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const response = await getAnalysisHistory(userId, currentPage, limit);
      setHistory(response.history);
      setTotal(response.total);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch history');
    } finally {
      setLoading(false);
    }
  }, [userId, currentPage, limit]);

  useEffect(() => {
    if (autoFetch) {
      fetchHistory();
    }
  }, [autoFetch, fetchHistory]);

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
    history,
    loading,
    error,
    total,
    page: currentPage,
    limit,
    refetch: fetchHistory,
    nextPage,
    prevPage
  };
}
