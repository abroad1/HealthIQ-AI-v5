/**
 * Analysis Service Tests
 * Tests for frontend/app/services/analysis.ts
 */

import { AnalysisService } from '../../app/services/analysis';
import { BiomarkerData, UserProfile, AnalysisRequest } from '../../app/types/analysis';

// Mock fetch globally
global.fetch = jest.fn();

describe('AnalysisService', () => {
  beforeEach(() => {
    (fetch as jest.Mock).mockClear();
  });

  describe('startAnalysis', () => {
    it('should start analysis successfully', async () => {
      const mockResponse = {
        analysis_id: 'test-analysis-123',
      };

      (fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      });

      const request: AnalysisRequest = {
        biomarkers: {
          cholesterol: { value: 4.9, unit: 'mmol/L' },
          glucose: { value: 5.2, unit: 'mmol/L' },
        },
        user: { age: 35, sex: 'male' },
      };

      const result = await AnalysisService.startAnalysis(request);

      expect(result.success).toBe(true);
      expect(result.data).toEqual(mockResponse);
      expect(result.message).toBe('Analysis started successfully');
      expect(fetch).toHaveBeenCalledWith(
        'http://localhost:8000/api/analysis/start',
        expect.objectContaining({
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(request),
        })
      );
    });

    it('should handle API errors', async () => {
      (fetch as jest.Mock).mockResolvedValueOnce({
        ok: false,
        status: 500,
        statusText: 'Internal Server Error',
        json: async () => ({ detail: 'Server error' }),
      });

      const request: AnalysisRequest = {
        biomarkers: { cholesterol: { value: 4.9, unit: 'mmol/L' } },
        user: { age: 35, sex: 'male' },
      };

      const result = await AnalysisService.startAnalysis(request);

      expect(result.success).toBe(false);
      expect(result.error).toBe('Server error');
      expect(result.data).toBeNull();
    });

    it('should handle network errors', async () => {
      (fetch as jest.Mock).mockRejectedValueOnce(new Error('Network error'));

      const request: AnalysisRequest = {
        biomarkers: { cholesterol: { value: 4.9, unit: 'mmol/L' } },
        user: { age: 35, sex: 'male' },
      };

      const result = await AnalysisService.startAnalysis(request);

      expect(result.success).toBe(false);
      expect(result.error).toBe('Network error');
      expect(result.data).toBeNull();
    });
  });

  describe('getAnalysisResult', () => {
    it('should get analysis result successfully', async () => {
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
      expect(fetch).toHaveBeenCalledWith(
        'http://localhost:8000/api/analysis/result?analysis_id=test-analysis-123',
        expect.objectContaining({
          method: 'GET',
          headers: { 'Content-Type': 'application/json' },
        })
      );
    });

    it('should handle analysis not found', async () => {
      (fetch as jest.Mock).mockResolvedValueOnce({
        ok: false,
        status: 404,
        json: async () => ({ detail: 'Analysis not found' }),
      });

      const result = await AnalysisService.getAnalysisResult('nonexistent-id');

      expect(result.success).toBe(false);
      expect(result.error).toBe('Analysis not found');
    });
  });

  describe('subscribeToAnalysisEvents', () => {
    it('should create EventSource with correct URL', () => {
      const mockEventSource = {
        onmessage: jest.fn(),
        onerror: jest.fn(),
        addEventListener: jest.fn(),
        close: jest.fn(),
      };

      // Mock EventSource
      (global as any).EventSource = jest.fn(() => mockEventSource);

      const onEvent = jest.fn();
      const onError = jest.fn();
      const onComplete = jest.fn();

      AnalysisService.subscribeToAnalysisEvents('test-id', onEvent, onError, onComplete);

      expect(EventSource).toHaveBeenCalledWith(
        'http://localhost:8000/api/analysis/events?analysis_id=test-id'
      );
    });
  });

  describe('validateBiomarkerData', () => {
    it('should validate correct biomarker data', () => {
      const validData: BiomarkerData = {
        cholesterol: { value: 4.9, unit: 'mmol/L' },
        glucose: { value: 5.2, unit: 'mmol/L' },
      };

      const result = AnalysisService.validateBiomarkerData(validData);

      expect(result.valid).toBe(true);
      expect(result.errors).toHaveLength(0);
    });

    it('should reject invalid biomarker data', () => {
      const invalidData = {
        cholesterol: { value: -1, unit: 'mmol/L' }, // negative value
        glucose: { value: 5.2 }, // missing unit
      };

      const result = AnalysisService.validateBiomarkerData(invalidData as any);

      expect(result.valid).toBe(false);
      expect(result.errors.length).toBeGreaterThan(0);
      expect(result.errors).toContain('Biomarker cholesterol must have a positive numeric value');
      expect(result.errors).toContain('Biomarker glucose must have a valid unit');
    });

    it('should reject empty biomarker data', () => {
      const result = AnalysisService.validateBiomarkerData({});

      expect(result.valid).toBe(false);
      expect(result.errors).toContain('At least one biomarker is required');
    });

    it('should reject non-object biomarker data', () => {
      const result = AnalysisService.validateBiomarkerData(null as any);

      expect(result.valid).toBe(false);
      expect(result.errors).toContain('Biomarkers must be an object');
    });
  });

  describe('validateUserProfile', () => {
    it('should validate correct user profile', () => {
      const validProfile: UserProfile = {
        age: 35,
        sex: 'male',
        weight: 75,
        height: 180,
      };

      const result = AnalysisService.validateUserProfile(validProfile);

      expect(result.valid).toBe(true);
      expect(result.errors).toHaveLength(0);
    });

    it('should reject invalid age', () => {
      const invalidProfile = { age: -5, sex: 'male' as const };

      const result = AnalysisService.validateUserProfile(invalidProfile);

      expect(result.valid).toBe(false);
      expect(result.errors).toContain('Age must be a number between 0 and 150');
    });

    it('should reject invalid sex', () => {
      const invalidProfile = { age: 35, sex: 'invalid' as any };

      const result = AnalysisService.validateUserProfile(invalidProfile);

      expect(result.valid).toBe(false);
      expect(result.errors).toContain('Sex must be one of: male, female, other');
    });

    it('should reject negative weight', () => {
      const invalidProfile = { age: 35, sex: 'male' as const, weight: -10 };

      const result = AnalysisService.validateUserProfile(invalidProfile);

      expect(result.valid).toBe(false);
      expect(result.errors).toContain('Weight must be a positive number if provided');
    });

    it('should reject negative height', () => {
      const invalidProfile = { age: 35, sex: 'male' as const, height: -10 };

      const result = AnalysisService.validateUserProfile(invalidProfile);

      expect(result.valid).toBe(false);
      expect(result.errors).toContain('Height must be a positive number if provided');
    });
  });

  describe('getAnalysisHistory', () => {
    it('should return mock analysis history', async () => {
      const result = await AnalysisService.getAnalysisHistory();

      expect(result.success).toBe(true);
      expect(result.data).toBeDefined();
      expect(Array.isArray(result.data)).toBe(true);
      expect(result.message).toBe('Analysis history retrieved successfully');
    });
  });

  describe('cancelAnalysis', () => {
    it('should cancel analysis successfully', async () => {
      const result = await AnalysisService.cancelAnalysis('test-analysis-123');

      expect(result.success).toBe(true);
      expect(result.data).toEqual({ cancelled: true });
      expect(result.message).toBe('Analysis cancelled successfully');
    });
  });
});
