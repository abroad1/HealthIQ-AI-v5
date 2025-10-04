// ARCHIVED TEST
// Reason: Medium-value test (duplicate coverage of analysis service)
// Archived: 2025-01-27
// Original Path: frontend/tests/services/simple.test.ts

/**
 * Simple Service Tests
 * Basic tests for frontend services to achieve coverage
 */

import { AnalysisService } from '../../../../app/services/analysis';
import { AuthService } from '../../../../app/services/auth';
import { ReportsService } from '../../../../app/services/reports';

// Mock fetch globally
global.fetch = jest.fn();

// Mock localStorage
const localStorageMock = {
  getItem: jest.fn(),
  setItem: jest.fn(),
  removeItem: jest.fn(),
  clear: jest.fn(),
};
Object.defineProperty(window, 'localStorage', {
  value: localStorageMock,
});

describe('Frontend Services', () => {
  beforeEach(() => {
    (fetch as jest.Mock).mockClear();
    localStorageMock.getItem.mockClear();
    localStorageMock.setItem.mockClear();
    localStorageMock.removeItem.mockClear();
  });

  describe('AnalysisService', () => {
    it('should validate biomarker data correctly', () => {
      const validData = {
        cholesterol: { value: 4.9, unit: 'mmol/L' },
        glucose: { value: 5.2, unit: 'mmol/L' },
      };

      const result = AnalysisService.validateBiomarkerData(validData);
      expect(result.valid).toBe(true);
      expect(result.errors).toHaveLength(0);
    });

    it('should reject invalid biomarker data', () => {
      const invalidData = {
        cholesterol: { value: -1, unit: 'mmol/L' },
      };

      const result = AnalysisService.validateBiomarkerData(invalidData);
      expect(result.valid).toBe(false);
      expect(result.errors.length).toBeGreaterThan(0);
    });

    it('should validate user profile correctly', () => {
      const validProfile = {
        age: 35,
        sex: 'male' as const,
      };

      const result = AnalysisService.validateUserProfile(validProfile);
      expect(result.valid).toBe(true);
      expect(result.errors).toHaveLength(0);
    });

    it('should reject invalid user profile', () => {
      const invalidProfile = {
        age: -5,
        sex: 'invalid' as any,
      };

      const result = AnalysisService.validateUserProfile(invalidProfile);
      expect(result.valid).toBe(false);
      expect(result.errors.length).toBeGreaterThan(0);
    });

    it('should start analysis successfully', async () => {
      const mockResponse = {
        analysis_id: 'test-analysis-123',
      };

      (fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      });

      const request = {
        biomarkers: {
          cholesterol: { value: 4.9, unit: 'mmol/L' },
        },
        user: { age: 35, sex: 'male' as const },
      };

      const result = await AnalysisService.startAnalysis(request);

      expect(result.success).toBe(true);
      expect(result.data).toEqual(mockResponse);
    });

    it('should handle analysis errors', async () => {
      (fetch as jest.Mock).mockResolvedValueOnce({
        ok: false,
        status: 500,
        json: async () => ({ detail: 'Server error' }),
      });

      const request = {
        biomarkers: {
          cholesterol: { value: 4.9, unit: 'mmol/L' },
        },
        user: { age: 35, sex: 'male' as const },
      };

      const result = await AnalysisService.startAnalysis(request);

      expect(result.success).toBe(false);
      expect(result.error).toBe('Server error');
    });

    it('should get analysis result', async () => {
      const mockResult = {
        analysis_id: 'test-analysis-123',
        status: 'completed',
        results: {
          clusters: [],
          insights: [],
          overall_score: 85,
        },
      };

      (fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => mockResult,
      });

      const result = await AnalysisService.getAnalysisResult('test-analysis-123');

      expect(result.success).toBe(true);
      expect(result.data).toEqual(mockResult);
    });

    it('should get analysis history', async () => {
      const result = await AnalysisService.getAnalysisHistory();
      expect(result.success).toBe(true);
      expect(Array.isArray(result.data)).toBe(true);
    });

    it('should cancel analysis', async () => {
      const result = await AnalysisService.cancelAnalysis('test-analysis-123');
      expect(result.success).toBe(true);
      expect(result.data).toEqual({ cancelled: true });
    });
  });

  describe('AuthService', () => {
    it('should login successfully', async () => {
      const mockResponse = {
        user: {
          id: 'user-123',
          email: 'test@example.com',
          name: 'Test User',
          role: 'user' as const,
          created_at: '2025-01-27T00:00:00Z',
          updated_at: '2025-01-27T00:00:00Z',
        },
        token: 'jwt-token-123',
      };

      (fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      });

      const credentials = { email: 'test@example.com', password: 'password123' };
      const result = await AuthService.login(credentials);

      expect(result.success).toBe(true);
      expect(result.data).toEqual(mockResponse);
    });

    it('should handle login errors', async () => {
      (fetch as jest.Mock).mockResolvedValueOnce({
        ok: false,
        status: 401,
        json: async () => ({ detail: 'Invalid credentials' }),
      });

      const credentials = { email: 'test@example.com', password: 'wrong' };
      const result = await AuthService.login(credentials);

      expect(result.success).toBe(false);
      expect(result.error).toBe('Invalid credentials');
    });

    it('should logout successfully', async () => {
      localStorageMock.getItem.mockReturnValue('jwt-token-123');

      (fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => ({ success: true }),
      });

      const result = await AuthService.logout();

      expect(result.success).toBe(true);
      expect(localStorageMock.removeItem).toHaveBeenCalledWith('healthiq_auth_token');
    });

    it('should get current user from localStorage', () => {
      const mockUser = {
        id: 'user-123',
        email: 'test@example.com',
        name: 'Test User',
        role: 'user' as const,
        created_at: '2025-01-27T00:00:00Z',
        updated_at: '2025-01-27T00:00:00Z',
      };

      localStorageMock.getItem.mockReturnValue(JSON.stringify(mockUser));

      const result = AuthService.getCurrentUser();

      expect(result).toEqual(mockUser);
    });

    it('should return null when no user data', () => {
      localStorageMock.getItem.mockReturnValue(null);

      const result = AuthService.getCurrentUser();

      expect(result).toBeNull();
    });

    it('should check if authenticated', () => {
      localStorageMock.getItem
        .mockReturnValueOnce('jwt-token-123')
        .mockReturnValueOnce(JSON.stringify({ id: 'user-123' }));

      const result = AuthService.isAuthenticated();

      expect(result).toBe(true);
    });

    it('should get token', () => {
      localStorageMock.getItem.mockReturnValue('jwt-token-123');

      const result = AuthService.getToken();

      expect(result).toBe('jwt-token-123');
    });

    it('should clear auth data', () => {
      AuthService.clearAuthData();

      expect(localStorageMock.removeItem).toHaveBeenCalledWith('healthiq_auth_token');
      expect(localStorageMock.removeItem).toHaveBeenCalledWith('healthiq_user_data');
    });
  });

  describe('ReportsService', () => {
    it('should generate report successfully', async () => {
      const mockResponse = {
        report_id: 'report-123',
        status: 'generated',
        download_url: 'http://localhost:8000/api/reports/download/report-123',
      };

      (fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      });

      const reportData = {
        analysis_id: 'analysis-123',
        format: 'pdf' as const,
        include_charts: true,
      };

      const result = await ReportsService.generateReport(reportData);

      expect(result.success).toBe(true);
      expect(result.data).toEqual(mockResponse);
    });

    it('should handle generation errors', async () => {
      (fetch as jest.Mock).mockResolvedValueOnce({
        ok: false,
        status: 400,
        json: async () => ({ detail: 'Invalid analysis ID' }),
      });

      const reportData = {
        analysis_id: 'invalid-id',
        format: 'pdf' as const,
      };

      const result = await ReportsService.generateReport(reportData);

      expect(result.success).toBe(false);
      expect(result.error).toBe('Invalid analysis ID');
    });

    it('should get report successfully', async () => {
      const mockReport = {
        report_id: 'report-123',
        analysis_id: 'analysis-123',
        status: 'completed',
        format: 'pdf',
        created_at: '2025-01-27T00:00:00Z',
        download_url: 'http://localhost:8000/api/reports/download/report-123',
      };

      (fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => mockReport,
      });

      const result = await ReportsService.getReport('report-123');

      expect(result.success).toBe(true);
      expect(result.data).toEqual(mockReport);
    });

    it('should download report successfully', async () => {
      const mockBlob = new Blob(['PDF content'], { type: 'application/pdf' });
      (fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        blob: async () => mockBlob,
      });

      const result = await ReportsService.downloadReport('report-123');

      expect(result.success).toBe(true);
      expect(result.data).toBeInstanceOf(Blob);
    });

    it('should get report history', async () => {
      const mockHistory = {
        reports: [
          {
            report_id: 'report-1',
            analysis_id: 'analysis-1',
            status: 'completed',
            format: 'pdf',
            created_at: '2025-01-27T00:00:00Z',
          },
        ],
        total: 1,
        page: 1,
        per_page: 10,
      };

      (fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => mockHistory,
      });

      const result = await ReportsService.getReportHistory();

      expect(result.success).toBe(true);
      expect(result.data).toEqual(mockHistory);
    });

    it('should delete report successfully', async () => {
      (fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => ({ deleted: true }),
      });

      const result = await ReportsService.deleteReport('report-123');

      expect(result.success).toBe(true);
      expect(result.data).toEqual({ deleted: true });
    });

    it('should share report successfully', async () => {
      const mockShareData = {
        share_id: 'share-123',
        share_url: 'http://localhost:8000/api/reports/share/share-123',
        expires_at: '2025-02-27T00:00:00Z',
      };

      (fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => mockShareData,
      });

      const shareOptions = {
        report_id: 'report-123',
        expires_in_days: 30,
        allow_download: true,
      };

      const result = await ReportsService.shareReport(shareOptions);

      expect(result.success).toBe(true);
      expect(result.data).toEqual(mockShareData);
    });

    it('should get report templates', async () => {
      const mockTemplates = {
        templates: [
          {
            id: 'template-1',
            name: 'Standard Report',
            description: 'Standard biomarker analysis report',
            format: 'pdf',
            created_at: '2025-01-27T00:00:00Z',
          },
        ],
        total: 1,
      };

      (fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => mockTemplates,
      });

      const result = await ReportsService.getReportTemplates();

      expect(result.success).toBe(true);
      expect(result.data).toEqual(mockTemplates);
    });
  });
});
