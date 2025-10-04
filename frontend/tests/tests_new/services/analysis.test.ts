/**
 * @jest-environment jsdom
 */

import { AnalysisService } from '../../app/services/analysis';
import { AnalysisResult, AnalysisHistoryResponse, ExportRequest, ExportResponse } from '../../app/types/analysis';

// Mock fetch globally
global.fetch = jest.fn();

describe('AnalysisService', () => {
  beforeEach(() => {
    (fetch as jest.Mock).mockClear();
  });

  describe('getAnalysisResult', () => {
    it('should fetch analysis result and map to correct format', async () => {
      // Arrange
      const analysisId = '123e4567-e89b-12d3-a456-426614174000';
      const mockApiResponse = {
        analysis_id: analysisId,
        result_version: '1.0.0',
        biomarkers: [
          {
            biomarker_name: 'glucose',
            value: 95.0,
            unit: 'mg/dL',
            score: 0.75,
            percentile: 65.0,
            status: 'normal',
            reference_range: { min: 70, max: 100 },
            interpretation: 'Within normal range',
            confidence: 0.9,
            health_system: 'metabolic',
            critical_flag: false
          }
        ],
        clusters: [
          {
            id: '456e7890-e89b-12d3-a456-426614174001',
            name: 'metabolic',
            biomarkers: ['glucose'],
            description: 'Metabolic health cluster',
            severity: 'normal',
            confidence: 0.9
          }
        ],
        insights: [
          {
            id: '789e0123-e89b-12d3-a456-426614174002',
            title: 'Good glucose control',
            content: 'Your glucose levels are well controlled',
            category: 'metabolic',
            confidence: 0.9,
            severity: 'normal',
            biomarkers_involved: ['glucose'],
            recommendations: ['Continue current diet']
          }
        ],
        recommendations: ['Continue current diet'],
        overall_score: 0.85,
        meta: {
          result_version: '1.0.0',
          confidence_score: 0.9,
          processing_metadata: { test: 'data' }
        },
        created_at: '2024-01-01T00:00:00Z'
      };

      (fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => mockApiResponse,
      });

      // Act
      const result = await AnalysisService.getAnalysisResult(analysisId);

      // Assert
      expect(fetch).toHaveBeenCalledWith(
        `/api/analysis/result?analysis_id=${analysisId}`,
        {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
        }
      );

      expect(result).toEqual({
        analysis_id: analysisId,
        result_version: '1.0.0',
        biomarkers: [
          {
            biomarker_name: 'glucose',
            value: 95.0,
            unit: 'mg/dL',
            score: 0.75,
            percentile: 65.0,
            status: 'normal',
            reference_range: { min: 70, max: 100 },
            interpretation: 'Within normal range',
            confidence: 0.9,
            health_system: 'metabolic',
            critical_flag: false
          }
        ],
        clusters: [
          {
            id: '456e7890-e89b-12d3-a456-426614174001',
            name: 'metabolic',
            biomarkers: ['glucose'],
            description: 'Metabolic health cluster',
            severity: 'normal',
            confidence: 0.9
          }
        ],
        insights: [
          {
            id: '789e0123-e89b-12d3-a456-426614174002',
            title: 'Good glucose control',
            content: 'Your glucose levels are well controlled',
            category: 'metabolic',
            confidence: 0.9,
            severity: 'normal',
            biomarkers_involved: ['glucose'],
            recommendations: ['Continue current diet']
          }
        ],
        recommendations: ['Continue current diet'],
        overall_score: 0.85,
        meta: {
          result_version: '1.0.0',
          confidence_score: 0.9,
          processing_metadata: { test: 'data' }
        },
        created_at: '2024-01-01T00:00:00Z'
      });
    });

    it('should handle API errors', async () => {
      // Arrange
      const analysisId = '123e4567-e89b-12d3-a456-426614174000';
      (fetch as jest.Mock).mockResolvedValueOnce({
        ok: false,
        status: 404,
        statusText: 'Not Found',
      });

      // Act & Assert
      await expect(AnalysisService.getAnalysisResult(analysisId)).rejects.toThrow('Failed to fetch analysis result: 404 Not Found');
    });
  });

  describe('getAnalysisHistory', () => {
    it('should fetch analysis history with pagination', async () => {
      // Arrange
      const userId = '123e4567-e89b-12d3-a456-426614174000';
      const mockApiResponse: AnalysisHistoryResponse = {
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

      (fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => mockApiResponse,
      });

      // Act
      const result = await AnalysisService.getAnalysisHistory(userId, 10, 0);

      // Assert
      expect(fetch).toHaveBeenCalledWith(
        `/api/analysis/history?user_id=${userId}&limit=10&offset=0`,
        {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
        }
      );

      expect(result).toEqual(mockApiResponse);
    });

    it('should handle API errors for history', async () => {
      // Arrange
      const userId = '123e4567-e89b-12d3-a456-426614174000';
      (fetch as jest.Mock).mockResolvedValueOnce({
        ok: false,
        status: 500,
        statusText: 'Internal Server Error',
      });

      // Act & Assert
      await expect(AnalysisService.getAnalysisHistory(userId, 10, 0)).rejects.toThrow('Failed to fetch analysis history: 500 Internal Server Error');
    });
  });

  describe('exportAnalysis', () => {
    it('should trigger analysis export', async () => {
      // Arrange
      const analysisId = '123e4567-e89b-12d3-a456-426614174000';
      const userId = '456e7890-e89b-12d3-a456-426614174001';
      const format = 'pdf';
      
      const mockApiResponse: ExportResponse = {
        export_id: '789e0123-e89b-12d3-a456-426614174002',
        status: 'pending',
        message: 'Export request submitted successfully'
      };

      (fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => mockApiResponse,
      });

      // Act
      const result = await AnalysisService.exportAnalysis(analysisId, format, userId);

      // Assert
      expect(fetch).toHaveBeenCalledWith(
        '/api/analysis/export',
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            analysis_id: analysisId,
            format: format,
            user_id: userId
          }),
        }
      );

      expect(result).toEqual(mockApiResponse);
    });

    it('should handle API errors for export', async () => {
      // Arrange
      const analysisId = '123e4567-e89b-12d3-a456-426614174000';
      const userId = '456e7890-e89b-12d3-a456-426614174001';
      const format = 'pdf';
      
      (fetch as jest.Mock).mockResolvedValueOnce({
        ok: false,
        status: 400,
        statusText: 'Bad Request',
      });

      // Act & Assert
      await expect(AnalysisService.exportAnalysis(analysisId, format, userId)).rejects.toThrow('Failed to export analysis: 400 Bad Request');
    });
  });
});