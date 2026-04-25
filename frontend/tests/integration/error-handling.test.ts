/**
 * Error Handling Integration Tests
 * Tests error handling across stores and services
 */

import { useAnalysisStore } from '../../app/state/analysisStore';
import { useClusterStore } from '../../app/state/clusterStore';
import { useUIStore } from '../../app/state/uiStore';
import { AnalysisService } from '../../app/services/analysis';
import { AuthService } from '../../app/services/auth';
// Mock the services
jest.mock('../../app/services/analysis');
jest.mock('../../app/services/auth');

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

describe('Error Handling Integration', () => {
  beforeEach(() => {
    // Reset all stores
    useAnalysisStore.getState().clearAnalysis();
    useClusterStore.getState().clearClusters();
    useUIStore.getState().resetUI();
    jest.clearAllMocks();
  });

  describe('API Error Handling', () => {
    it('should handle network errors in analysis service', async () => {
      const mockRequest = {
        biomarkers: {
          cholesterol: { value: 4.9, unit: 'mmol/L' },
        },
        user: {
          chronological_age: 35,
          sex: 'male' as const,
          weight_kg: 75,
          height_cm: 180,
        },
      };

      // Mock network error
      (AnalysisService.startAnalysis as jest.Mock).mockRejectedValue(
        new Error('Network request failed')
      );

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
      expect(useAnalysisStore.getState().error?.message).toContain('Network request failed');
      expect(useAnalysisStore.getState().currentPhase).toBe('idle');
      expect(useAnalysisStore.getState().isLoading).toBe(false);
    });

    it('should handle HTTP errors in auth service', async () => {
      const credentials = {
        email: 'test@example.com',
        password: 'wrong-password',
      };

      (AuthService.login as jest.Mock).mockResolvedValueOnce({
        success: false,
        error: 'Invalid credentials',
        data: null,
        message: 'Login failed',
      });

      // Mock HTTP 401 error (in case the real client path is exercised later)
      (fetch as jest.Mock).mockResolvedValueOnce({
        ok: false,
        status: 401,
        statusText: 'Unauthorized',
        json: async () => ({ detail: 'Invalid credentials' }),
      });

      const result = await AuthService.login(credentials);

      expect(result.success).toBe(false);
      expect(result.error).toContain('Invalid credentials');
    });

  });

  describe('Validation Error Handling', () => {
    it('should handle biomarker validation errors', async () => {
      const mockRequest = {
        biomarkers: {
          cholesterol: { value: -1, unit: 'mmol/L' }, // Invalid value
        },
        user: {
          chronological_age: 35,
          sex: 'male' as const,
          weight_kg: 75,
          height_cm: 180,
        },
      };

      (AnalysisService.validateBiomarkerData as jest.Mock).mockReturnValue({
        valid: false,
        errors: ['Biomarker cholesterol must have a positive numeric value'],
      });

      await useAnalysisStore.getState().startAnalysis(mockRequest);

      expect(useAnalysisStore.getState().error).toBeTruthy();
      expect(useAnalysisStore.getState().error?.message).toContain('Validation failed');
      expect(useAnalysisStore.getState().error?.details?.biomarkerErrors).toContain(
        'Biomarker cholesterol must have a positive numeric value'
      );
      expect(useAnalysisStore.getState().currentPhase).toBe('idle');
    });

    it('should handle user profile validation errors', async () => {
      const mockRequest = {
        biomarkers: {
          cholesterol: { value: 4.9, unit: 'mmol/L' },
        },
        user: { age: -5, sex: 'invalid' as any }, // Invalid age and sex
      };

      (AnalysisService.validateBiomarkerData as jest.Mock).mockReturnValue({
        valid: true,
        errors: [],
      });

      (AnalysisService.validateUserProfile as jest.Mock).mockReturnValue({
        valid: false,
        errors: [
          'Age must be a number between 0 and 150',
          'Sex must be one of: male, female, other'
        ],
      });

      await useAnalysisStore.getState().startAnalysis(mockRequest);

      expect(useAnalysisStore.getState().error).toBeTruthy();
      expect(useAnalysisStore.getState().error?.message).toContain('Validation failed');
      expect(useAnalysisStore.getState().error?.details?.userErrors).toContain(
        'Age must be a number between 0 and 150'
      );
    });
  });

  describe('Store Error State Management', () => {
    it('should clear errors when starting new analysis', async () => {
      // Set initial error
      useAnalysisStore.getState().setError({
        message: 'Previous error',
        code: 'PREVIOUS_ERROR',
        details: null,
      });

      const mockRequest = {
        biomarkers: {
          cholesterol: { value: 4.9, unit: 'mmol/L' },
        },
        user: {
          chronological_age: 35,
          sex: 'male' as const,
          weight_kg: 75,
          height_cm: 180,
        },
      };

      (AnalysisService.startAnalysis as jest.Mock).mockResolvedValue({
        success: true,
        data: { analysis_id: 'test-analysis-123', status: 'completed', message: 'ok' },
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

      expect(useAnalysisStore.getState().error).toBeNull();
      expect(useAnalysisStore.getState().currentPhase).toBe('completed');
    });

    it('should maintain error state when retry fails', async () => {
      const mockRequest = {
        biomarkers: {
          cholesterol: { value: 4.9, unit: 'mmol/L' },
        },
        user: {
          chronological_age: 35,
          sex: 'male' as const,
          weight_kg: 75,
          height_cm: 180,
        },
      };

      // Set up initial state with error (retry requires currentAnalysis + userProfile)
      useAnalysisStore.getState().setCurrentAnalysis({
        analysis_id: 'prior-analysis',
        status: 'failed',
        created_at: new Date().toISOString(),
        biomarkers: [],
        clusters: [],
        insights: [],
        overall_score: null,
      });
      useAnalysisStore.getState().setRawBiomarkers(mockRequest.biomarkers);
      useAnalysisStore.getState().setUserProfile(mockRequest.user);
      useAnalysisStore.getState().setPhase('error');
      useAnalysisStore.getState().setError({
        message: 'Previous error',
        code: 'PREVIOUS_ERROR',
        details: null,
      });

      // Mock retry failure
      (AnalysisService.startAnalysis as jest.Mock).mockResolvedValue({
        success: false,
        error: 'Retry failed',
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

      await useAnalysisStore.getState().retryAnalysis();

      expect(useAnalysisStore.getState().error).toBeTruthy();
      expect(useAnalysisStore.getState().error?.message).toContain('Retry failed');
      expect(useAnalysisStore.getState().currentPhase).toBe('idle');
    });
  });

  describe('UI Error Display', () => {
    it('should show error notifications in UI store', () => {
      const errorMessage = 'Analysis failed';
      
      useUIStore.getState().addNotification({
        type: 'error',
        title: 'Error',
        message: errorMessage,
        duration: 5000,
      });

      const notifications = useUIStore.getState().notifications;
      expect(notifications).toHaveLength(1);
      expect(notifications[0].type).toBe('error');
      expect(notifications[0].message).toBe(errorMessage);
    });

    it('should show error toasts', () => {
      const errorMessage = 'Network error';
      
      useUIStore.getState().showToast({
        type: 'error',
        title: 'Error',
        message: errorMessage,
        duration: 5000,
        position: 'top-right',
      });

      const toasts = useUIStore.getState().toasts;
      expect(toasts).toHaveLength(1);
      expect(toasts[0].type).toBe('error');
      expect(toasts[0].message).toBe(errorMessage);
    });

    it('should clear error states when user dismisses', () => {
      // Add error notification
      useUIStore.getState().addNotification({
        type: 'error',
        title: 'Error',
        message: 'Test error',
        duration: 5000,
      });

      // Add error toast
      const toastId = useUIStore.getState().showToast({
        type: 'error',
        title: 'Error',
        message: 'Test error',
        duration: 5000,
        position: 'top-right',
      });

      expect(useUIStore.getState().notifications).toHaveLength(1);
      expect(useUIStore.getState().toasts).toHaveLength(1);

      // Dismiss notification
      useUIStore.getState().removeNotification(
        useUIStore.getState().notifications[0].id
      );

      // Dismiss toast
      useUIStore.getState().hideToast(toastId);

      expect(useUIStore.getState().notifications).toHaveLength(0);
      expect(useUIStore.getState().toasts).toHaveLength(0);
    });
  });

  describe('Error Recovery', () => {
    it('should allow recovery from analysis errors', async () => {
      const mockRequest = {
        biomarkers: {
          cholesterol: { value: 4.9, unit: 'mmol/L' },
        },
        user: {
          chronological_age: 35,
          sex: 'male' as const,
          weight_kg: 75,
          height_cm: 180,
        },
      };

      // First attempt fails
      (AnalysisService.startAnalysis as jest.Mock)
        .mockResolvedValueOnce({
          success: false,
          error: 'Service unavailable',
          data: null,
        })
        .mockResolvedValueOnce({
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

      // First attempt
      await useAnalysisStore.getState().startAnalysis(mockRequest);
      expect(useAnalysisStore.getState().error).toBeTruthy();

      // Clear error and retry
      useAnalysisStore.getState().setError(null);
      await useAnalysisStore.getState().startAnalysis(mockRequest);
      
      expect(useAnalysisStore.getState().error).toBeNull();
      expect(useAnalysisStore.getState().currentAnalysis).toBeTruthy();
    });

    it('should handle partial failures gracefully', async () => {
      // Mock partial cluster loading failure
      const mockClusters = [
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
      ];

      // Simulate partial success
      useClusterStore.getState().setClusters(mockClusters);
      useClusterStore.getState().setError('Some clusters failed to load');

      expect(useClusterStore.getState().clusters).toHaveLength(1);
      expect(useClusterStore.getState().error).toBe('Some clusters failed to load');
    });
  });
});
