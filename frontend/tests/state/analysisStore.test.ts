/**
 * Analysis Store Tests
 * Tests for frontend/app/state/analysisStore.ts
 */

import { useAnalysisStore } from '../../app/state/analysisStore';
import { AnalysisService } from '../../app/services/analysis';
import { BiomarkerData, UserProfile, AnalysisRequest } from '../../app/types/analysis';

// Mock the AnalysisService
jest.mock('../../app/services/analysis', () => ({
  AnalysisService: {
    startAnalysis: jest.fn(),
    getAnalysisResult: jest.fn(),
    subscribeToAnalysisEvents: jest.fn(),
    validateBiomarkerData: jest.fn(),
    validateUserProfile: jest.fn(),
  },
}));

// Mock EventSource
const mockEventSource = {
  onmessage: jest.fn(),
  onerror: jest.fn(),
  addEventListener: jest.fn(),
  close: jest.fn(),
};

(global as any).EventSource = jest.fn(() => mockEventSource);

describe('AnalysisStore', () => {
  beforeEach(() => {
    // Reset store state
    useAnalysisStore.getState().clearAnalysis();
    jest.clearAllMocks();
  });

  describe('Initial State', () => {
    it('should have correct initial state', () => {
      const state = useAnalysisStore.getState();

      expect(state.currentAnalysis).toBeNull();
      expect(state.analysisHistory).toEqual([]);
      expect(state.isLoading).toBe(false);
      expect(state.error).toBeNull();
      expect(state.currentPhase).toBe('idle');
      expect(state.progress).toBe(0);
      expect(state.rawBiomarkers).toEqual({});
      expect(state.normalizedBiomarkers).toEqual({});
      expect(state.userProfile).toBeNull();
      expect(state.eventSource).toBeNull();
    });
  });

  describe('Basic Setters', () => {
    it('should set current analysis', () => {
      const analysis = { id: 'test-123', status: 'completed' };
      useAnalysisStore.getState().setCurrentAnalysis(analysis);

      expect(useAnalysisStore.getState().currentAnalysis).toEqual(analysis);
    });

    it('should set loading state', () => {
      useAnalysisStore.getState().setLoading(true);
      expect(useAnalysisStore.getState().isLoading).toBe(true);

      useAnalysisStore.getState().setLoading(false);
      expect(useAnalysisStore.getState().isLoading).toBe(false);
    });

    it('should set error', () => {
      const error = 'Test error';
      useAnalysisStore.getState().setError(error);
      expect(useAnalysisStore.getState().error).toBe(error);
    });

    it('should set workflow phase', () => {
      useAnalysisStore.getState().setPhase('processing');
      expect(useAnalysisStore.getState().currentPhase).toBe('processing');
    });

    it('should set progress', () => {
      useAnalysisStore.getState().setProgress(50);
      expect(useAnalysisStore.getState().progress).toBe(50);
    });

    it('should set raw biomarkers', () => {
      const biomarkers: BiomarkerData = {
        cholesterol: { value: 4.9, unit: 'mmol/L' },
        glucose: { value: 5.2, unit: 'mmol/L' },
      };
      useAnalysisStore.getState().setRawBiomarkers(biomarkers);
      expect(useAnalysisStore.getState().rawBiomarkers).toEqual(biomarkers);
    });

    it('should set normalized biomarkers', () => {
      const biomarkers: BiomarkerData = {
        cholesterol: { value: 4.9, unit: 'mmol/L' },
        glucose: { value: 5.2, unit: 'mmol/L' },
      };
      useAnalysisStore.getState().setNormalizedBiomarkers(biomarkers);
      expect(useAnalysisStore.getState().normalizedBiomarkers).toEqual(biomarkers);
    });

    it('should set user profile', () => {
      const profile: UserProfile = {
        age: 35,
        sex: 'male',
        weight: 75,
        height: 180,
      };
      useAnalysisStore.getState().setUserProfile(profile);
      expect(useAnalysisStore.getState().userProfile).toEqual(profile);
    });
  });

  describe('startAnalysis', () => {
    it('should start analysis successfully', async () => {
      const mockAnalysisId = 'analysis-123';
      const mockRequest: AnalysisRequest = {
        biomarkers: { cholesterol: { value: 4.9, unit: 'mmol/L' } },
        user: { age: 35, sex: 'male' },
      };

      (AnalysisService.startAnalysis as jest.Mock).mockResolvedValue({
        success: true,
        data: { analysis_id: mockAnalysisId },
        message: 'Analysis started',
      });

      (AnalysisService.validateBiomarkerData as jest.Mock).mockReturnValue({
        valid: true,
        errors: [],
      });

      (AnalysisService.validateUserProfile as jest.Mock).mockReturnValue({
        valid: true,
        errors: [],
      });

      await useAnalysisStore.getState().startAnalysis(mockRequest);

      const state = useAnalysisStore.getState();
      expect(state.isLoading).toBe(false);
      expect(state.error).toBeNull();
      expect(state.currentPhase).toBe('processing');
      expect(state.currentAnalysis).toEqual({ analysis_id: mockAnalysisId });
      expect(AnalysisService.startAnalysis).toHaveBeenCalledWith(mockRequest);
    });

    it('should handle validation errors', async () => {
      const mockRequest: AnalysisRequest = {
        biomarkers: { cholesterol: { value: -1, unit: 'mmol/L' } },
        user: { age: 35, sex: 'male' },
      };

      (AnalysisService.validateBiomarkerData as jest.Mock).mockReturnValue({
        valid: false,
        errors: ['Invalid biomarker value'],
      });

      await useAnalysisStore.getState().startAnalysis(mockRequest);

      const state = useAnalysisStore.getState();
      expect(state.isLoading).toBe(false);
      expect(state.error?.message).toContain('Invalid biomarker value');
      expect(state.currentPhase).toBe('idle');
    });

    it('should handle API errors', async () => {
      const mockRequest: AnalysisRequest = {
        biomarkers: { cholesterol: { value: 4.9, unit: 'mmol/L' } },
        user: { age: 35, sex: 'male' },
      };

      (AnalysisService.validateBiomarkerData as jest.Mock).mockReturnValue({
        valid: true,
        errors: [],
      });

      (AnalysisService.validateUserProfile as jest.Mock).mockReturnValue({
        valid: true,
        errors: [],
      });

      (AnalysisService.startAnalysis as jest.Mock).mockResolvedValue({
        success: false,
        error: 'API Error',
        data: null,
      });

      await useAnalysisStore.getState().startAnalysis(mockRequest);

      const state = useAnalysisStore.getState();
      expect(state.isLoading).toBe(false);
      expect(state.error?.message).toContain('API Error');
      expect(state.currentPhase).toBe('idle');
    });
  });

  describe('updateAnalysisProgress', () => {
    it('should update progress and phase', () => {
      useAnalysisStore.getState().updateAnalysisProgress('analysis-123', 50, 'processing');
      
      const state = useAnalysisStore.getState();
      expect(state.progress).toBe(50);
      expect(state.currentPhase).toBe('processing');
    });
  });

  describe('completeAnalysis', () => {
    it('should complete analysis successfully', () => {
      const mockResults = {
        clusters: [],
        insights: [],
        overall_score: 85,
        risk_assessment: {},
        recommendations: [],
      };

      useAnalysisStore.getState().completeAnalysis('analysis-123', mockResults);

      const state = useAnalysisStore.getState();
      expect(state.currentPhase).toBe('completed');
      expect(state.progress).toBe(100);
      expect(state.isLoading).toBe(false);
      expect(state.error).toBeNull();
    });
  });

  describe('failAnalysis', () => {
    it('should fail analysis with error', () => {
      const error = {
        message: 'Analysis failed',
        code: 'ANALYSIS_ERROR',
        details: null,
      };
      useAnalysisStore.getState().failAnalysis('analysis-123', error);

      const state = useAnalysisStore.getState();
      expect(state.currentPhase).toBe('error');
      expect(state.isLoading).toBe(false);
      expect(state.error).toEqual(error);
    });
  });

  describe('clearAnalysis', () => {
    it('should clear all analysis data', () => {
      // Set some data first
      useAnalysisStore.getState().setCurrentAnalysis({
        analysis_id: 'test',
        status: 'processing',
        created_at: '2025-01-27T00:00:00Z',
      });
      useAnalysisStore.getState().setLoading(true);
      useAnalysisStore.getState().setError({
        message: 'test error',
        code: 'TEST_ERROR',
        details: null,
      });
      useAnalysisStore.getState().setPhase('processing');
      useAnalysisStore.getState().setProgress(50);

      useAnalysisStore.getState().clearAnalysis();

      const state = useAnalysisStore.getState();
      expect(state.currentAnalysis).toBeNull();
      expect(state.isLoading).toBe(false);
      expect(state.error).toBeNull();
      expect(state.currentPhase).toBe('idle');
      expect(state.progress).toBe(0);
      expect(state.eventSource).toBeNull();
    });
  });

  describe('retryAnalysis', () => {
    it('should retry analysis with same data', async () => {
      const mockRequest: AnalysisRequest = {
        biomarkers: { cholesterol: { value: 4.9, unit: 'mmol/L' } },
        user: { age: 35, sex: 'male' },
      };

      // Set up initial state
      useAnalysisStore.getState().setRawBiomarkers(mockRequest.biomarkers);
      useAnalysisStore.getState().setUserProfile(mockRequest.user);
      useAnalysisStore.getState().setPhase('error');
      useAnalysisStore.getState().setError({
        message: 'Previous error',
        code: 'PREVIOUS_ERROR',
        details: null,
      });

      (AnalysisService.validateBiomarkerData as jest.Mock).mockReturnValue({
        valid: true,
        errors: [],
      });

      (AnalysisService.validateUserProfile as jest.Mock).mockReturnValue({
        valid: true,
        errors: [],
      });

      (AnalysisService.startAnalysis as jest.Mock).mockResolvedValue({
        success: true,
        data: { analysis_id: 'retry-123' },
        message: 'Analysis started',
      });

      await useAnalysisStore.getState().retryAnalysis();

      const state = useAnalysisStore.getState();
      expect(state.currentPhase).toBe('processing');
      expect(state.error).toBeNull();
      expect(AnalysisService.startAnalysis).toHaveBeenCalledWith(mockRequest);
    });

    it('should not retry if no previous data', async () => {
      useAnalysisStore.getState().retryAnalysis();

      expect(AnalysisService.startAnalysis).not.toHaveBeenCalled();
    });
  });

  describe('addToHistory', () => {
    it('should add analysis to history', () => {
      const analysis = {
        analysis_id: 'test-123',
        status: 'completed' as const,
        created_at: '2025-01-27T00:00:00Z',
        results: { 
          overall_score: 85,
          clusters: [],
          insights: [],
          risk_assessment: {},
          recommendations: [],
        },
      };

      useAnalysisStore.getState().addToHistory(analysis);

      const state = useAnalysisStore.getState();
      expect(state.analysisHistory).toHaveLength(1);
      expect(state.analysisHistory[0]).toEqual(analysis);
    });

    it('should limit history to max items', () => {
      const store = useAnalysisStore.getState();
      
      // Add more than MAX_HISTORY items
      for (let i = 0; i < 15; i++) {
        store.addToHistory({
          id: `test-${i}`,
          timestamp: '2025-01-27T00:00:00Z',
          status: 'completed' as const,
          results: { overall_score: 85 },
        });
      }

      expect(store.analysisHistory).toHaveLength(10); // MAX_HISTORY = 10
    });
  });

  describe('getAnalysisSummary', () => {
    it('should return analysis summary', () => {
      const analysis = {
        analysis_id: 'test-123',
        status: 'completed' as const,
        created_at: '2025-01-27T00:00:00Z',
        results: { 
          overall_score: 85,
          clusters: [],
          insights: [],
          risk_assessment: {},
          recommendations: [],
        },
      };

      useAnalysisStore.getState().setCurrentAnalysis(analysis);
      const summary = useAnalysisStore.getState().getAnalysisSummary();

      expect(summary).toEqual({
        totalAnalyses: 1,
        completedAnalyses: 1,
        failedAnalyses: 0,
        averageScore: 85,
      });
    });

    it('should return summary even if no current analysis', () => {
      const summary = useAnalysisStore.getState().getAnalysisSummary();
      expect(summary).toEqual({
        totalAnalyses: 0,
        completedAnalyses: 0,
        failedAnalyses: 0,
        averageScore: 0,
      });
    });
  });
});
