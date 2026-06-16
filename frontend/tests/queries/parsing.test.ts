/**
 * @jest-environment jsdom
 */

import { renderHook, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import React from 'react';
import { useParseUpload, useValidateParsed } from '../../app/queries/parsing';

global.fetch = jest.fn();

function createWrapper() {
  const queryClient = new QueryClient({
    defaultOptions: {
      mutations: {
        retry: false,
      },
    },
  });
  return function Wrapper(props: { children: React.ReactNode }) {
    return React.createElement(QueryClientProvider, { client: queryClient }, props.children);
  };
}

describe('upload parsing hooks auth headers', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    localStorage.clear();
    document.cookie = 'healthiq_access_token=; Path=/; Max-Age=0';
  });

  it('useParseUpload sends Bearer when session token is present', async () => {
    localStorage.setItem('healthiq_auth_token', 'jwt-parse-test-token');

    (fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        success: true,
        message: 'ok',
        parsed_data: { biomarkers: [], metadata: {} },
        analysis_id: 'analysis_test',
        timestamp: new Date().toISOString(),
      }),
    });

    const { result } = renderHook(() => useParseUpload(), { wrapper: createWrapper() });
    result.current.mutate({ text: 'Glucose 5.2 mmol/L' });

    await waitFor(() => expect(result.current.isSuccess).toBe(true));

    expect(fetch).toHaveBeenCalledWith(
      'http://127.0.0.1:8000/api/upload/parse',
      expect.objectContaining({
        method: 'POST',
        headers: { Authorization: 'Bearer jwt-parse-test-token' },
      })
    );
  });

  it('useParseUpload omits Authorization when no session token is present', async () => {
    (fetch as jest.Mock).mockResolvedValueOnce({
      ok: false,
      status: 401,
      statusText: 'Unauthorized',
      json: async () => ({ detail: 'Authentication required' }),
    });

    const { result } = renderHook(() => useParseUpload(), { wrapper: createWrapper() });
    result.current.mutate({ text: 'Glucose 5.2 mmol/L' });

    await waitFor(() => expect(result.current.isError).toBe(true));

    const [, init] = (fetch as jest.Mock).mock.calls[0] as [string, RequestInit];
    expect(init.headers).toEqual({});
  });

  it('useValidateParsed sends Bearer when session token is present', async () => {
    localStorage.setItem('healthiq_auth_token', 'jwt-validate-test-token');

    (fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        valid: true,
        supported_formats: ['pdf', 'txt', 'json', 'csv'],
        max_file_size_mb: 10,
        detected_format: 'text/plain',
        file_size_bytes: 12,
        warnings: [],
        errors: [],
      }),
    });

    const { result } = renderHook(() => useValidateParsed(), { wrapper: createWrapper() });
    result.current.mutate({ text: 'Glucose 5.2 mmol/L' });

    await waitFor(() => expect(result.current.isSuccess).toBe(true));

    expect(fetch).toHaveBeenCalledWith(
      'http://127.0.0.1:8000/api/upload/validate',
      expect.objectContaining({
        method: 'POST',
        headers: { Authorization: 'Bearer jwt-validate-test-token' },
      })
    );
  });
});
