/**
 * Regression safeguard: ensure analysis result is fetched at most once per analysis_id.
 */
import { renderHook, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import React from 'react';
import { useAnalysisResult } from '../../app/queries/analysisResult';
import { AnalysisService } from '../../app/services/analysis';

jest.mock('../../app/services/analysis', () => ({
  AnalysisService: {
    getAnalysisResult: jest.fn(),
  },
}));

const mockGetAnalysisResult = AnalysisService.getAnalysisResult as jest.MockedFunction<
  typeof AnalysisService.getAnalysisResult
>;

function createWrapper() {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: {
        retry: false,
        gcTime: 0,
      },
    },
  });
  return function Wrapper(props: { children: React.ReactNode }) {
    return React.createElement(
      QueryClientProvider,
      { client: queryClient },
      props.children
    );
  };
}

describe('useAnalysisResult', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    mockGetAnalysisResult.mockResolvedValue({
      success: true,
      data: {
        analysis_id: 'test-123',
        status: 'completed',
        biomarkers: [],
        clusters: [],
        insights: [],
        overall_score: 85,
      },
      message: 'OK',
    });
  });

  it('fetches result exactly once per analysis_id', async () => {
    const Wrapper = createWrapper();
    const { result } = renderHook(
      () => useAnalysisResult('test-123'),
      { wrapper: Wrapper }
    );

    await waitFor(() => {
      expect(result.current.isSuccess).toBe(true);
    });

    expect(mockGetAnalysisResult).toHaveBeenCalledTimes(1);
    expect(mockGetAnalysisResult).toHaveBeenCalledWith('test-123');
  });

  it('does not fetch when analysisId is null', async () => {
    const Wrapper = createWrapper();
    renderHook(() => useAnalysisResult(null), { wrapper: Wrapper });

    await waitFor(() => {});

    expect(mockGetAnalysisResult).not.toHaveBeenCalled();
  });
});
