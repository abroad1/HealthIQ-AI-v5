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
        `http://127.0.0.1:8000/api/analysis/result?analysis_id=${analysisId}`,
        expect.objectContaining({
          method: 'GET',
          headers: expect.objectContaining({
            'Content-Type': 'application/json',
          }),
        })
      );

      expect(result).toEqual({
        success: true,
        message: 'Analysis result retrieved successfully',
        data: {
          analysis_id: analysisId,
          result_version: '1.0.0',
          status: 'completed',
          balanced_systems_v1: null,
          interpretation_display_layer_v1: null,
          risk_assessment: {},
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
        clinician_report_v1: null,
        created_at: '2024-01-01T00:00:00Z',
        completed_at: undefined,
        narrative_report_v1: null,
        }
      });
    });

    it('should preserve balanced_systems_v1, interpretation_display_layer_v1, and risk_assessment from API', async () => {
      const analysisId = '123e4567-e89b-12d3-a456-426614174000';
      const idlStub = {
        schema_version: '1.0',
        records: [
          {
            internal_id: 't1',
            scientific_class: 'phenotype',
            clinical_display_label: 'Clinical',
            retail_display_label: 'Retail',
            subtitle: 'Sub',
            why_it_matters: 'Because',
            severity_state: 'watch',
            supporting_biomarkers_summary: 'A, B',
            frontend_allowed_term: 'phenotype_allowed',
            display_order_priority: 1,
            enabled_for_frontend: true,
          },
        ],
      };
      const balancedStub = {
        intro_line: 'Intro',
        items: [{ system_topic: 'Liver', evidence_line: 'Looks stable', capacity_note: '' }],
        context_line: 'Context',
      };
      const mockApiResponse = {
        analysis_id: analysisId,
        result_version: '1.0.0',
        biomarkers: [],
        clusters: [],
        insights: [],
        recommendations: [],
        overall_score: null,
        meta: {},
        created_at: '2024-01-01T00:00:00Z',
        clinician_report_v1: null,
        balanced_systems_v1: balancedStub,
        interpretation_display_layer_v1: idlStub,
        risk_assessment: { metabolic_strain: 12 },
        primary_driver_system_id: 'metabolic',
      };

      (fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => mockApiResponse,
      });

      const result = await AnalysisService.getAnalysisResult(analysisId);

      expect(result.success).toBe(true);
      expect(result.data?.balanced_systems_v1).toEqual(balancedStub);
      expect(result.data?.interpretation_display_layer_v1).toEqual(idlStub);
      expect(result.data?.risk_assessment).toEqual({ metabolic_strain: 12 });
      expect(result.data?.primary_driver_system_id).toBe('metabolic');
    });

    it('should handle API errors', async () => {
      // Arrange
      const analysisId = '123e4567-e89b-12d3-a456-426614174000';
      (fetch as jest.Mock).mockResolvedValueOnce({
        ok: false,
        status: 404,
        statusText: 'Not Found',
        json: jest.fn().mockRejectedValue(new Error('response.json is not a function')),
      });

      // Act
      const result = await AnalysisService.getAnalysisResult(analysisId);

      // Assert - service returns error response instead of throwing
      expect(result.success).toBe(false);
      expect(result.error).toBe('HTTP 404: Not Found');
      expect(result.data).toBeNull();
    });
  });

  describe('getAnalysisHistory', () => {
    it('should fetch analysis history with pagination', async () => {
      // Arrange
      const mockApiResponse: AnalysisHistoryResponse = {
        history: [
          {
            id: '123e4567-e89b-12d3-a456-426614174000',
            created_at: '2024-01-01T00:00:00Z',
            overall_score: 0.85,
            status: 'completed',
            processing_time_seconds: 5.0
          },
          {
            id: '456e7890-e89b-12d3-a456-426614174001',
            created_at: '2024-01-02T00:00:00Z',
            overall_score: 0.92,
            status: 'completed',
            processing_time_seconds: 3.0
          }
        ],
        total: 2,
        limit: 10,
        page: 1
      };

      (fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => mockApiResponse,
      });

      // Act
      const result = await AnalysisService.getAnalysisHistory(10, 0);

      // Assert
      expect(fetch).toHaveBeenCalledWith(
        `http://127.0.0.1:8000/api/analysis/history?limit=10&offset=0`,
        expect.objectContaining({
          method: 'GET',
          headers: expect.objectContaining({
            'Content-Type': 'application/json',
          }),
        })
      );

      expect(result).toEqual({
        success: true,
        message: 'Analysis history retrieved successfully',
        data: mockApiResponse
      });
    });

    it('should handle API errors for history', async () => {
      // Arrange
      (fetch as jest.Mock).mockResolvedValueOnce({
        ok: false,
        status: 500,
        statusText: 'Internal Server Error',
        json: jest.fn().mockRejectedValue(new Error('response.json is not a function')),
      });

      // Act
      const result = await AnalysisService.getAnalysisHistory(10, 0);

      // Assert - service returns error response instead of throwing
      expect(result.success).toBe(false);
      expect(result.error).toBe('HTTP 500: Internal Server Error');
      expect(result.data).toEqual({ history: [], limit: 10, page: 1, total: 0 });
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
        'http://127.0.0.1:8000/api/analysis/export',
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

      expect(result).toEqual({
        success: true,
        message: 'Export request created successfully',
        data: mockApiResponse
      });
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
        json: jest.fn().mockRejectedValue(new Error('response.json is not a function')),
      });

      // Act
      const result = await AnalysisService.exportAnalysis(analysisId, format, userId);

      // Assert - service returns error response instead of throwing
      expect(result.success).toBe(false);
      expect(result.error).toBe('HTTP 400: Bad Request');
      expect(result.data).toEqual({ export_id: '', status: 'failed' });
    });
  });
});