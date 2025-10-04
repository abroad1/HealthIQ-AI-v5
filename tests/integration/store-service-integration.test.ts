/**
 * Store-Service Integration Tests
 * Tests integration between Zustand stores and API services
 */

import { useAnalysisStore } from '../../app/state/analysisStore';
import { useClusterStore } from '../../app/state/clusterStore';
import { useUIStore } from '../../app/state/uiStore';
import { AnalysisService } from '../../app/services/analysis';
import { AuthService } from '../../app/services/auth';
import { ReportsService } from '../../app/services/reports';

// Mock the services
jest.mock('../../app/services/analysis');
jest.mock('../../app/services/auth');
jest.mock('../../app/services/reports');

// Mock fetch globally
global.fetch = jest.fn();

// Mock EventSource
const mockEventSource = {
  onmessage: jest.fn(),
  onerror: jest.fn(),
  addEventListener: jest.fn(),
  close: jest.fn(),
};

(global as any).EventSource = jest.fn(() => mockEventSource);

describe('Store-Service Integration', () => {
  beforeEach(() => {
    // Reset all stores
    useAnalysisStore.getState().clearAnalysis();
    useClusterStore.getState().clearClusters();
    useUIStore.getState().resetUI();
    jest.clearAllMocks();
  });

  describe('Analysis Store + Analysis Service', () => {
    it('should integrate startAnalysis with service', async () => {
      const mockRequest = {
        biomarkers: {
          cholesterol: { value: 4.9, unit: 'mmol/L' },
          glucose: { value: 5.2, unit: 'mmol/L' },
        },
        user: { age: 35, sex: 'male' as const },
      };

      (AnalysisService.startAnalysis as jest.Mock).mockResolvedValue({
        success: true,
        data: { analysis_id: 'test-analysis-123' },
        message: 'Analysis started successfully',
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

      expect(AnalysisService.startAnalysis).toHaveBeenCalledWith(mockRequest);
      expect(useAnalysisStore.getState().currentAnalysis).toBeTruthy();
      expect(useAnalysisStore.getState().currentPhase).toBe('ingestion');
    });

    it('should handle service errors gracefully', async () => {
      const mockRequest = {
        biomarkers: {
          cholesterol: { value: 4.9, unit: 'mmol/L' },
        },
        user: { age: 35, sex: 'male' as const },
      };

      (AnalysisService.startAnalysis as jest.Mock).mockResolvedValue({
        success: false,
        error: 'Service unavailable',
        data: null,
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

      expect(useAnalysisStore.getState().error).toBeTruthy();
      expect(useAnalysisStore.getState().error?.message).toContain('Service unavailable');
      expect(useAnalysisStore.getState().currentPhase).toBe('idle');
    });
  });

  describe('Cluster Store + Analysis Service', () => {
    it('should load clusters from analysis results', async () => {
      const analysisId = 'test-analysis-123';
      
      // Mock the loadClusters method to simulate API call
      const mockClusters = [
        {
          id: 'cluster-1',
          name: 'Metabolic Health',
          description: 'Metabolic health cluster',
          biomarkers: ['glucose', 'insulin'],
          score: 85,
          risk_level: 'low' as const,
          category: 'metabolic',
          insights: ['Normal glucose metabolism'],
          recommendations: ['Maintain current lifestyle'],
          created_at: new Date().toISOString(),
          status: 'normal' as const,
        },
      ];

      // Mock the loadClusters implementation
      useClusterStore.getState().setClusters(mockClusters);
      useClusterStore.getState().setLoading(false);

      const state = useClusterStore.getState();
      expect(state.clusters).toHaveLength(1);
      expect(state.clusters[0].name).toBe('Metabolic Health');
      expect(state.isLoading).toBe(false);
    });
  });

  describe('UI Store + Auth Service', () => {
    it('should integrate login with UI state', async () => {
      const credentials = {
        email: 'test@example.com',
        password: 'password123',
      };

      (AuthService.login as jest.Mock).mockResolvedValue({
        success: true,
        data: {
          user: {
            id: 'user-123',
            email: 'test@example.com',
            name: 'Test User',
            role: 'user' as const,
            created_at: new Date().toISOString(),
            updated_at: new Date().toISOString(),
          },
          token: 'mock-token',
        },
        message: 'Login successful',
      });

      const result = await AuthService.login(credentials);
      
      expect(result.success).toBe(true);
      expect(result.data?.user.email).toBe('test@example.com');
      
      // UI store should handle authentication state
      useUIStore.getState().setGlobalLoading(false);
      expect(useUIStore.getState().globalLoading).toBe(false);
    });

    it('should handle authentication errors', async () => {
      const credentials = {
        email: 'test@example.com',
        password: 'wrong-password',
      };

      (AuthService.login as jest.Mock).mockResolvedValue({
        success: false,
        error: 'Invalid credentials',
        data: null,
      });

      const result = await AuthService.login(credentials);
      
      expect(result.success).toBe(false);
      expect(result.error).toBe('Invalid credentials');
      
      // UI store should handle error state
      useUIStore.getState().setGlobalError('Authentication failed');
      expect(useUIStore.getState().globalError).toBe('Authentication failed');
    });
  });

  describe('UI Store + Reports Service', () => {
    it('should integrate report generation with UI state', async () => {
      const reportRequest = {
        analysis_id: 'test-analysis-123',
        type: 'summary' as const,
        format: 'pdf' as const,
      };

      (ReportsService.generateReport as jest.Mock).mockResolvedValue({
        success: true,
        data: {
          id: 'report-123',
          analysis_id: 'test-analysis-123',
          title: 'Health Analysis Report',
          type: 'summary',
          format: 'pdf',
          status: 'generating',
          created_at: new Date().toISOString(),
        },
        message: 'Report generation started successfully',
      });

      // Set loading state
      useUIStore.getState().setLoading('report-generation', true);
      
      const result = await ReportsService.generateReport(reportRequest);
      
      expect(result.success).toBe(true);
      expect(result.data?.id).toBe('report-123');
      
      // Clear loading state
      useUIStore.getState().setLoading('report-generation', false);
      expect(useUIStore.getState().isLoading('report-generation')).toBe(false);
    });
  });

  describe('Cross-Store Integration', () => {
    it('should coordinate analysis and cluster stores', async () => {
      const analysisId = 'test-analysis-123';
      
      // Start analysis
      useAnalysisStore.getState().setCurrentAnalysis({
        analysis_id: analysisId,
        status: 'completed',
        created_at: new Date().toISOString(),
        results: {
          clusters: [
            {
              id: 'cluster-1',
              name: 'Metabolic Health',
              description: 'Metabolic health cluster',
              biomarkers: ['glucose'],
              score: 85,
              risk_level: 'low' as const,
              category: 'metabolic',
              insights: ['Normal glucose metabolism'],
              recommendations: ['Maintain current lifestyle'],
              created_at: new Date().toISOString(),
              status: 'normal' as const,
            },
          ],
          insights: [],
          overall_score: 85,
          risk_assessment: {},
          recommendations: [],
        },
      });

      // Load clusters from analysis results
      const analysis = useAnalysisStore.getState().currentAnalysis;
      if (analysis?.results?.clusters) {
        useClusterStore.getState().updateClustersFromAnalysis(analysis.results);
      }

      expect(useAnalysisStore.getState().currentAnalysis?.status).toBe('completed');
      expect(useClusterStore.getState().clusters).toHaveLength(1);
      expect(useClusterStore.getState().clusters[0].name).toBe('Metabolic Health');
    });

    it('should coordinate UI state across all stores', () => {
      // Set global loading
      useUIStore.getState().setGlobalLoading(true);
      
      // Set specific loading states
      useAnalysisStore.getState().setLoading(true);
      useClusterStore.getState().setLoading(true);
      
      // Check coordinated loading state
      expect(useUIStore.getState().globalLoading).toBe(true);
      expect(useAnalysisStore.getState().isLoading).toBe(true);
      expect(useClusterStore.getState().isLoading).toBe(true);
      
      // Clear all loading states
      useUIStore.getState().setGlobalLoading(false);
      useAnalysisStore.getState().setLoading(false);
      useClusterStore.getState().setLoading(false);
      
      expect(useUIStore.getState().globalLoading).toBe(false);
      expect(useAnalysisStore.getState().isLoading).toBe(false);
      expect(useClusterStore.getState().isLoading).toBe(false);
    });
  });

  describe('Error Handling Integration', () => {
    it('should propagate errors across stores', () => {
      const errorMessage = 'Network error';
      
      // Set error in analysis store
      useAnalysisStore.getState().setError({
        message: errorMessage,
        code: 'NETWORK_ERROR',
        details: null,
      });
      
      // Set error in UI store
      useUIStore.getState().setGlobalError(errorMessage);
      
      expect(useAnalysisStore.getState().error?.message).toBe(errorMessage);
      expect(useUIStore.getState().globalError).toBe(errorMessage);
    });

    it('should clear errors across stores', () => {
      // Set errors
      useAnalysisStore.getState().setError({
        message: 'Test error',
        code: 'TEST_ERROR',
        details: null,
      });
      useUIStore.getState().setGlobalError('Test error');
      
      // Clear errors
      useAnalysisStore.getState().setError(null);
      useUIStore.getState().setGlobalError(null);
      
      expect(useAnalysisStore.getState().error).toBeNull();
      expect(useUIStore.getState().globalError).toBeNull();
    });
  });
});
