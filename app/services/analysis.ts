/**
 * Analysis API Service
 * Handles biomarker analysis operations and SSE streaming
 */

import { 
  AnalysisRequest, 
  BiomarkerData, 
  UserProfile, 
  AnalysisResult, 
  AnalysisHistoryResponse,
  ExportRequest,
  ExportResponse
} from '../types/analysis';
import { ApiResponse, ApiError } from '../types/api';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

export class AnalysisService {
  /**
   * Start a new biomarker analysis
   */
  static async startAnalysis(data: AnalysisRequest): Promise<ApiResponse<{ analysis_id: string }>> {
    try {
      const response = await fetch(`${API_BASE_URL}/analysis/start`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`);
      }

      const result = await response.json();
      return {
        data: result,
        success: true,
        message: 'Analysis started successfully',
      };
    } catch (error) {
      return {
        data: null,
        success: false,
        error: error instanceof Error ? error.message : 'Failed to start analysis',
      };
    }
  }

  /**
   * Get analysis result by ID
   */
  static async getAnalysisResult(analysisId: string): Promise<ApiResponse<AnalysisResult>> {
    try {
      const response = await fetch(`${API_BASE_URL}/analysis/result?analysis_id=${encodeURIComponent(analysisId)}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`);
      }

      const result = await response.json();
      
      // Map API response to frontend AnalysisResult format (Sprint 9b DTO parity)
      const analysisResult: AnalysisResult = {
        analysis_id: result.analysis_id,
        result_version: result.result_version,
        biomarkers: result.biomarkers || [],
        clusters: result.clusters || [],
        insights: result.insights || [],
        recommendations: result.recommendations || [],
        overall_score: result.overall_score,
        meta: result.meta || {},
        created_at: result.created_at
      };
      
      return {
        data: analysisResult,
        success: true,
        message: 'Analysis result retrieved successfully',
      };
    } catch (error) {
      return {
        data: null,
        success: false,
        error: error instanceof Error ? error.message : 'Failed to get analysis result',
      };
    }
  }

  /**
   * Subscribe to analysis events via Server-Sent Events
   */
  static subscribeToAnalysisEvents(
    analysisId: string,
    onEvent: (event: MessageEvent) => void,
    onError?: (error: Event) => void,
    onComplete?: () => void
  ): EventSource {
    const eventSource = new EventSource(
      `${API_BASE_URL}/analysis/events?analysis_id=${encodeURIComponent(analysisId)}`
    );

    let isCompleted = false;

    eventSource.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        onEvent(event);
      } catch (error) {
        console.error('Failed to parse SSE event data:', error);
        onError?.(error as Event);
      }
    };

    eventSource.onerror = (error) => {
      console.error('SSE connection error:', error);
      // Only call onError if not completed - this prevents false error states
      if (!isCompleted) {
        onError?.(error);
      } else {
        console.log('SSE closed gracefully after completion');
      }
    };

    // Listen for specific event types
    eventSource.addEventListener('analysis_status', (event) => {
      try {
        const data = JSON.parse(event.data);
        onEvent(event);
        
        // Check if this is a completion event
        if (data.phase === 'complete') {
          isCompleted = true;
          eventSource.close(); // Close cleanly
          console.log('SSE closed gracefully after completion');
          onComplete?.();
        }
      } catch (error) {
        console.error('Failed to parse analysis_status event:', error);
        onError?.(error as Event);
      }
    });

    eventSource.addEventListener('complete', () => {
      isCompleted = true;
      eventSource.close();
      onComplete?.();
    });

    return eventSource;
  }

  /**
   * Validate biomarker data before analysis
   */
  static validateBiomarkerData(biomarkers: BiomarkerData): { valid: boolean; errors: string[] } {
    const errors: string[] = [];

    if (!biomarkers || typeof biomarkers !== 'object') {
      errors.push('Biomarkers must be an object');
      return { valid: false, errors };
    }

    const biomarkerEntries = Object.entries(biomarkers);
    
    if (biomarkerEntries.length === 0) {
      errors.push('At least one biomarker is required');
    }

    for (const [key, value] of biomarkerEntries) {
      if (!value || typeof value !== 'object') {
        errors.push(`Biomarker ${key} must be an object`);
        continue;
      }

      if (typeof value.value !== 'number' || value.value <= 0) {
        errors.push(`Biomarker ${key} must have a positive numeric value`);
      }

      if (!value.unit || typeof value.unit !== 'string') {
        errors.push(`Biomarker ${key} must have a valid unit`);
      }
    }

    return {
      valid: errors.length === 0,
      errors,
    };
  }

  /**
   * Validate user profile data
   */
  static validateUserProfile(user: UserProfile): { valid: boolean; errors: string[] } {
    const errors: string[] = [];

    if (!user || typeof user !== 'object') {
      errors.push('User profile must be an object');
      return { valid: false, errors };
    }

    if (typeof user.age !== 'number' || user.age < 0 || user.age > 150) {
      errors.push('Age must be a number between 0 and 150');
    }

    if (!['male', 'female', 'other'].includes(user.sex)) {
      errors.push('Sex must be one of: male, female, other');
    }

    if (user.weight !== undefined && (typeof user.weight !== 'number' || user.weight <= 0)) {
      errors.push('Weight must be a positive number if provided');
    }

    if (user.height !== undefined && (typeof user.height !== 'number' || user.height <= 0)) {
      errors.push('Height must be a positive number if provided');
    }

    return {
      valid: errors.length === 0,
      errors,
    };
  }

  /**
   * Get analysis history for a user
   */
  static async getAnalysisHistory(
    userId: string, 
    limit: number = 10, 
    offset: number = 0
  ): Promise<ApiResponse<AnalysisHistoryResponse>> {
    try {
      const response = await fetch(
        `${API_BASE_URL}/analysis/history?user_id=${encodeURIComponent(userId)}&limit=${limit}&offset=${offset}`,
        {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
        }
      );

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`);
      }

      const result = await response.json();

      return {
        data: result,
        success: true,
        message: 'Analysis history retrieved successfully',
      };
    } catch (error) {
      return {
        data: { history: [], total: 0, page: 1, limit },
        success: false,
        error: error instanceof Error ? error.message : 'Failed to get analysis history',
      };
    }
  }

  /**
   * Export analysis results
   */
  static async exportAnalysis(
    analysisId: string, 
    format: 'pdf' | 'json' | 'csv' = 'json',
    userId?: string
  ): Promise<ApiResponse<ExportResponse>> {
    try {
      const response = await fetch(`${API_BASE_URL}/analysis/export`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          analysis_id: analysisId,
          format,
          user_id: userId
        }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`);
      }

      const result = await response.json();

      return {
        data: result,
        success: true,
        message: 'Export request created successfully',
      };
    } catch (error) {
      return {
        data: { export_id: '', status: 'failed' as const },
        success: false,
        error: error instanceof Error ? error.message : 'Failed to export analysis',
      };
    }
  }

  /**
   * Cancel an ongoing analysis
   * TODO: Implement when backend endpoint is available
   */
  static async cancelAnalysis(analysisId: string): Promise<ApiResponse<{ cancelled: boolean }>> {
    try {
      // Mock implementation - replace with actual API call
      return {
        data: { cancelled: true },
        success: true,
        message: 'Analysis cancelled successfully',
      };
    } catch (error) {
      return {
        data: { cancelled: false },
        success: false,
        error: error instanceof Error ? error.message : 'Failed to cancel analysis',
      };
    }
  }
}