/**
 * @jest-environment jsdom
 */

import { renderHook, act } from '@testing-library/react';
import { useHistory } from '../../app/hooks/useHistory';
import { AnalysisService } from '../../app/services/analysis';
import { AnalysisHistoryResponse } from '../../app/types/analysis';

jest.mock('../../app/services/analysis');

describe('useHistory', () => {
  const mockAnalysisService = AnalysisService as jest.Mocked<typeof AnalysisService>;

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('should initialize with empty state when autoFetch is off', () => {
    const { result } = renderHook(() => useHistory({ autoFetch: false }));

    expect(result.current.analyses).toEqual([]);
    expect(result.current.loading).toBe(false);
    expect(result.current.error).toBeNull();
    expect(result.current.total).toBe(0);
  });

  it('should load analyses successfully', async () => {
    const mockData: AnalysisHistoryResponse = {
      history: [
        {
          id: '123e4567-e89b-12d3-a456-426614174000',
          created_at: '2024-01-01T00:00:00Z',
          overall_score: 0.85,
          status: 'completed',
          processing_time_seconds: 5.0,
        },
        {
          id: '456e7890-e89b-12d3-a456-426614174001',
          created_at: '2024-01-02T00:00:00Z',
          overall_score: 0.92,
          status: 'completed',
          processing_time_seconds: 3.0,
        },
      ],
      total: 2,
      limit: 10,
      page: 1,
    };

    mockAnalysisService.getAnalysisHistory.mockResolvedValueOnce({
      success: true,
      data: mockData,
      message: 'ok',
    });

    const { result } = renderHook(() => useHistory({ autoFetch: false }));

    await act(async () => {
      await result.current.loadAnalyses();
    });

    expect(result.current.analyses).toEqual(mockData.history);
    expect(result.current.total).toBe(2);
    expect(result.current.loading).toBe(false);
    expect(result.current.error).toBeNull();
    expect(mockAnalysisService.getAnalysisHistory).toHaveBeenCalledWith(10, 0);
  });

  it('should handle loading state', async () => {
    let resolvePromise: (v: { success: true; data: AnalysisHistoryResponse; message: string }) => void;
    const promise = new Promise<{ success: true; data: AnalysisHistoryResponse; message: string }>(
      (resolve) => {
        resolvePromise = resolve;
      }
    );
    mockAnalysisService.getAnalysisHistory.mockReturnValueOnce(promise);

    const { result } = renderHook(() => useHistory({ autoFetch: false }));

    act(() => {
      void result.current.loadAnalyses();
    });

    expect(result.current.loading).toBe(true);

    await act(async () => {
      resolvePromise!({
        success: true,
        data: { history: [], total: 0, limit: 10, page: 1 },
        message: 'ok',
      });
    });

    expect(result.current.loading).toBe(false);
  });

  it('should handle errors from the service', async () => {
    mockAnalysisService.getAnalysisHistory.mockResolvedValueOnce({
      success: false,
      error: 'Failed to fetch analysis history',
      data: { history: [], total: 0, limit: 10, page: 1 },
    });

    const { result } = renderHook(() => useHistory({ autoFetch: false }));

    await act(async () => {
      await result.current.loadAnalyses();
    });

    expect(result.current.error).toBe('Failed to fetch analysis history');
    expect(result.current.loading).toBe(false);
    expect(result.current.analyses).toEqual([]);
  });

  it('should load another page when autoFetch is false', async () => {
    const first: AnalysisHistoryResponse = {
      history: [
        {
          id: '123e4567-e89b-12d3-a456-426614174000',
          created_at: '2024-01-01T00:00:00Z',
          overall_score: 0.85,
          status: 'completed',
        },
      ],
      total: 3,
      limit: 1,
      page: 1,
    };
    const second: AnalysisHistoryResponse = {
      history: [
        {
          id: '456e7890-e89b-12d3-a456-426614174001',
          created_at: '2024-01-02T00:00:00Z',
          overall_score: 0.92,
          status: 'completed',
        },
      ],
      total: 3,
      limit: 1,
      page: 2,
    };

    mockAnalysisService.getAnalysisHistory
      .mockResolvedValueOnce({ success: true, data: first, message: 'ok' })
      .mockResolvedValueOnce({ success: true, data: second, message: 'ok' });

    const { result } = renderHook(() => useHistory({ autoFetch: false, limit: 1 }));

    await act(async () => {
      await result.current.loadAnalyses(1);
    });
    await act(async () => {
      await result.current.loadAnalyses(2);
    });

    expect(result.current.analyses).toHaveLength(1);
    expect(result.current.analyses[0].id).toBe('456e7890-e89b-12d3-a456-426614174001');
    expect(mockAnalysisService.getAnalysisHistory).toHaveBeenCalledTimes(2);
    expect(mockAnalysisService.getAnalysisHistory).toHaveBeenNthCalledWith(1, 1, 0);
    expect(mockAnalysisService.getAnalysisHistory).toHaveBeenNthCalledWith(2, 1, 1);
  });

  it('should clear error when loading succeeds after a failure', async () => {
    mockAnalysisService.getAnalysisHistory
      .mockResolvedValueOnce({
        success: false,
        error: 'Previous error',
        data: { history: [], total: 0, limit: 10, page: 1 },
      })
      .mockResolvedValueOnce({
        success: true,
        data: { history: [], total: 0, limit: 10, page: 1 },
        message: 'ok',
      });

    const { result } = renderHook(() => useHistory({ autoFetch: false }));

    await act(async () => {
      await result.current.loadAnalyses();
    });
    expect(result.current.error).toBe('Previous error');

    await act(async () => {
      await result.current.loadAnalyses();
    });
    expect(result.current.error).toBeNull();
  });
});
