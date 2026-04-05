/**
 * @jest-environment jsdom
 */

import { renderHook, act } from '@testing-library/react';
import { useHistory } from '../../app/hooks/useHistory';
import { AnalysisService } from '../../app/services/analysis';
import type { AnalysisHistoryResponse } from '../../app/types/analysis';

jest.mock('../../app/services/analysis');

describe('useHistory', () => {
  const mockAnalysisService = AnalysisService as jest.Mocked<typeof AnalysisService>;

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('should initialize with empty state', () => {
    const { result } = renderHook(() => useHistory());

    expect(result.current.analyses).toEqual([]);
    expect(result.current.loading).toBe(false);
    expect(result.current.error).toBeNull();
    expect(result.current.total).toBe(0);
  });

  it('should load analyses successfully', async () => {
    const userId = '123e4567-e89b-12d3-a456-426614174000';
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
      page: 1,
      limit: 10,
    };

    mockAnalysisService.getAnalysisHistory.mockResolvedValueOnce({
      success: true,
      data: mockData,
      message: 'ok',
    });

    const { result } = renderHook(() => useHistory(userId, { autoFetch: false }));

    await act(async () => {
      await result.current.loadAnalyses(userId);
    });

    expect(result.current.analyses).toEqual(mockData.history);
    expect(result.current.total).toBe(2);
    expect(result.current.loading).toBe(false);
    expect(result.current.error).toBeNull();
    expect(mockAnalysisService.getAnalysisHistory).toHaveBeenCalledWith(10, 0);
  });

  it('should handle errors', async () => {
    const userId = '123e4567-e89b-12d3-a456-426614174000';
    mockAnalysisService.getAnalysisHistory.mockResolvedValueOnce({
      success: false,
      data: null,
      error: 'Failed to fetch analysis history',
      message: '',
    });

    const { result } = renderHook(() => useHistory(userId, { autoFetch: false }));

    await act(async () => {
      await result.current.loadAnalyses(userId);
    });

    expect(result.current.error).toBe('Failed to fetch analysis history');
    expect(result.current.analyses).toEqual([]);
  });
});
