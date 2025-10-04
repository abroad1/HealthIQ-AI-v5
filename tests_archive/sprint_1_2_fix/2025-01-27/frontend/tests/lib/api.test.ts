// ARCHIVED TEST
// Reason: Medium-value test (infrastructure test, not user-facing)
// Archived: 2025-01-27
// Original Path: frontend/tests/lib/api.test.ts

/**
 * API Utility Tests
 * Tests for frontend/app/lib/api.ts
 */

import { API_BASE_URL, API_ENDPOINTS, buildApiUrl, handleApiResponse } from '../../../../app/lib/api';

describe('API Utility', () => {
  describe('API_BASE_URL', () => {
    it('should have correct base URL', () => {
      expect(API_BASE_URL).toBe('http://localhost:8000');
    });
  });

  describe('API_ENDPOINTS', () => {
    it('should have analysis endpoints', () => {
      expect(API_ENDPOINTS.ANALYSIS.START).toBe('/api/analysis/start');
      expect(API_ENDPOINTS.ANALYSIS.RESULT).toBe('/api/analysis/result');
      expect(API_ENDPOINTS.ANALYSIS.EVENTS).toBe('/api/analysis/events');
      expect(API_ENDPOINTS.ANALYSIS.HISTORY).toBe('/api/analysis/history');
      expect(API_ENDPOINTS.ANALYSIS.CANCEL).toBe('/api/analysis/cancel');
    });

    it('should have auth endpoints', () => {
      expect(API_ENDPOINTS.AUTH.LOGIN).toBe('/api/auth/login');
      expect(API_ENDPOINTS.AUTH.LOGOUT).toBe('/api/auth/logout');
      expect(API_ENDPOINTS.AUTH.REGISTER).toBe('/api/auth/register');
      expect(API_ENDPOINTS.AUTH.PROFILE).toBe('/api/auth/profile');
      expect(API_ENDPOINTS.AUTH.REFRESH).toBe('/api/auth/refresh');
      expect(API_ENDPOINTS.AUTH.RESET_PASSWORD).toBe('/api/auth/reset-password');
    });

    it('should have reports endpoints', () => {
      expect(API_ENDPOINTS.REPORTS.GENERATE).toBe('/api/reports/generate');
      expect(API_ENDPOINTS.REPORTS.GET).toBe('/api/reports');
      expect(API_ENDPOINTS.REPORTS.DOWNLOAD).toBe('/api/reports/download');
      expect(API_ENDPOINTS.REPORTS.HISTORY).toBe('/api/reports/history');
      expect(API_ENDPOINTS.REPORTS.DELETE).toBe('/api/reports');
      expect(API_ENDPOINTS.REPORTS.SHARE).toBe('/api/reports/share');
      expect(API_ENDPOINTS.REPORTS.TEMPLATES).toBe('/api/reports/templates');
    });
  });

  describe('buildApiUrl', () => {
    it('should build correct URL for analysis start', () => {
      const url = buildApiUrl(API_ENDPOINTS.ANALYSIS.START);
      expect(url).toBe('http://localhost:8000/api/analysis/start');
    });

    it('should build correct URL for auth login', () => {
      const url = buildApiUrl(API_ENDPOINTS.AUTH.LOGIN);
      expect(url).toBe('http://localhost:8000/api/auth/login');
    });

    it('should build correct URL for reports generate', () => {
      const url = buildApiUrl(API_ENDPOINTS.REPORTS.GENERATE);
      expect(url).toBe('http://localhost:8000/api/reports/generate');
    });
  });

  describe('handleApiResponse', () => {
    it('should handle successful response', async () => {
      const mockResponse = {
        ok: true,
        json: async () => ({ data: 'test' }),
      };

      const result = await handleApiResponse(mockResponse as Response);
      expect(result.success).toBe(true);
      expect(result.data).toEqual({ data: 'test' });
    });

    it('should handle error response', async () => {
      const mockResponse = {
        ok: false,
        status: 400,
        json: async () => ({ detail: 'Bad request' }),
      };

      const result = await handleApiResponse(mockResponse as Response);
      expect(result.success).toBe(false);
      expect(result.error).toBe('Bad request');
    });

    it('should handle network error', async () => {
      const mockResponse = {
        ok: false,
        status: 500,
        json: async () => { throw new Error('Network error'); },
      };

      const result = await handleApiResponse(mockResponse as Response);
      expect(result.success).toBe(false);
      expect(result.error).toBe('Network error');
    });
  });
});
