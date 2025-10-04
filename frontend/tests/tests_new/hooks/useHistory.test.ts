/**
 * @jest-environment jsdom
 */

import { renderHook, act } from '@testing-library/react';
import { useHistory } from '../../app/hooks/useHistory';
import { AnalysisService } from '../../app/services/analysis';
import { AnalysisHistoryResponse } from '../../app/types/analysis';

// Mock the AnalysisService
jest.mock('../../app/services/analysis');

describe('useHistory', () => {
  const mockAnalysisService = AnalysisService as jest.Mocked<typeof AnalysisService>;

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('should initialize with empty state', () => {
    // Act
    const { result } = renderHook(() => useHistory());

    // Assert
    expect(result.current.analyses).toEqual([]);
    expect(result.current.loading).toBe(false);
    expect(result.current.error).toBeNull();
    expect(result.current.total).toBe(0);
  });

  it('should load analyses successfully', async () => {
    // Arrange
    const userId = '123e4567-e89b-12d3-a456-426614174000';
    const mockResponse: AnalysisHistoryResponse = {
      analyses: [
        {
          analysis_id: '123e4567-e89b-12d3-a456-426614174000',
          created_at: '2024-01-01T00:00:00Z',
          overall_score: 0.85,
          status: 'completed',
          processing_time_seconds: 5.0
        },
        {
          analysis_id: '456e7890-e89b-12d3-a456-426614174001',
          created_at: '2024-01-02T00:00:00Z',
          overall_score: 0.92,
          status: 'completed',
          processing_time_seconds: 3.0
        }
      ],
      total: 2,
      limit: 10,
      offset: 0
    };

    mockAnalysisService.getAnalysisHistory.mockResolvedValueOnce(mockResponse);

    // Act
    const { result } = renderHook(() => useHistory());

    await act(async () => {
      await result.current.loadAnalyses(userId);
    });

    // Assert
    expect(result.current.analyses).toEqual(mockResponse.analyses);
    expect(result.current.total).toBe(2);
    expect(result.current.loading).toBe(false);
    expect(result.current.error).toBeNull();
    expect(mockAnalysisService.getAnalysisHistory).toHaveBeenCalledWith(userId, 10, 0);
  });

  it('should handle loading state', async () => {
    // Arrange
    const userId = '123e4567-e89b-12d3-a456-426614174000';
    let resolvePromise: (value: AnalysisHistoryResponse) => void;
    const promise = new Promise<AnalysisHistoryResponse>((resolve) => {
      resolvePromise = resolve;
    });
    mockAnalysisService.getAnalysisHistory.mockReturnValueOnce(promise);

    // Act
    const { result } = renderHook(() => useHistory());

    act(() => {
      result.current.loadAnalyses(userId);
    });

    // Assert - loading state
    expect(result.current.loading).toBe(true);
    expect(result.current.analyses).toEqual([]);

    // Act - resolve promise
    await act(async () => {
      resolvePromise!({
        analyses: [],
        total: 0,
        limit: 10,
        offset: 0
      });
    });

    // Assert - loading completed
    expect(result.current.loading).toBe(false);
  });

  it('should handle errors', async () => {
    // Arrange
    const userId = '123e4567-e89b-12d3-a456-426614174000';
    const error = new Error('Failed to fetch analysis history');
    mockAnalysisService.getAnalysisHistory.mockRejectedValueOnce(error);

    // Act
    const { result } = renderHook(() => useHistory());

    await act(async () => {
      await result.current.loadAnalyses(userId);
    });

    // Assert
    expect(result.current.error).toBe('Failed to fetch analysis history');
    expect(result.current.loading).toBe(false);
    expect(result.current.analyses).toEqual([]);
  });

  it('should load more analyses with pagination', async () => {
    // Arrange
    const userId = '123e4567-e89b-12d3-a456-426614174000';
    const initialResponse: AnalysisHistoryResponse = {
      analyses: [
        {
          analysis_id: '123e4567-e89b-12d3-a456-426614174000',
          created_at: '2024-01-01T00:00:00Z',
          overall_score: 0.85,
          status: 'completed',
          processing_time_seconds: 5.0
        }
      ],
      total: 3,
      limit: 1,
      offset: 0
    };

    const moreResponse: AnalysisHistoryResponse = {
      analyses: [
        {
          analysis_id: '456e7890-e89b-12d3-a456-426614174001',
          created_at: '2024-01-02T00:00:00Z',
          overall_score: 0.92,
          status: 'completed',
          processing_time_seconds: 3.0
        }
      ],
      total: 3,
      limit: 1,
      offset: 1
    };

    mockAnalysisService.getAnalysisHistory
      .mockResolvedValueOnce(initialResponse)
      .mockResolvedValueOnce(moreResponse);

    // Act
    const { result } = renderHook(() => useHistory());

    // Load initial analyses
    await act(async () => {
      await result.current.loadAnalyses(userId, 1, 0);
    });

    // Load more analyses
    await act(async () => {
      await result.current.loadMore(userId, 1, 1);
    });

    // Assert
    expect(result.current.analyses).toHaveLength(2);
    expect(result.current.total).toBe(3);
    expect(mockAnalysisService.getAnalysisHistory).toHaveBeenCalledTimes(2);
    expect(mockAnalysisService.getAnalysisHistory).toHaveBeenNthCalledWith(1, userId, 1, 0);
    expect(mockAnalysisService.getAnalysisHistory).toHaveBeenNthCalledWith(2, userId, 1, 1);
  });

  it('should clear error when loading new analyses', async () => {
    // Arrange
    const userId = '123e4567-e89b-12d3-a456-426614174000';
    const error = new Error('Previous error');
    const mockResponse: AnalysisHistoryResponse = {
      analyses: [],
      total: 0,
      limit: 10,
      offset: 0
    };

    mockAnalysisService.getAnalysisHistory
      .mockRejectedValueOnce(error)
      .mockResolvedValueOnce(mockResponse);

    // Act
    const { result } = renderHook(() => useHistory());

    // First call fails
    await act(async () => {
      await result.current.loadAnalyses(userId);
    });

    expect(result.current.error).toBe('Previous error');

    // Second call succeeds
    await act(async () => {
      await result.current.loadAnalyses(userId);
    });

    // Assert
    expect(result.current.error).toBeNull();
    expect(result.current.analyses).toEqual([]);
  });

  it('should handle empty response', async () => {
    // Arrange
    const userId = '123e4567-e89b-12d3-a456-426614174000';
    const mockResponse: AnalysisHistoryResponse = {
      analyses: [],
      total: 0,
      limit: 10,
      offset: 0
    };

    mockAnalysisService.getAnalysisHistory.mockResolvedValueOnce(mockResponse);

    // Act
    const { result } = renderHook(() => useHistory());

    await act(async () => {
      await result.current.loadAnalyses(userId);
    });

    // Assert
    expect(result.current.analyses).toEqual([]);
    expect(result.current.total).toBe(0);
    expect(result.current.loading).toBe(false);
    expect(result.current.error).toBeNull();
  });
});