// ARCHIVED TEST
// Reason: Medium-value test (API mock, not critical path)
// Archived: 2025-01-27
// Original Path: frontend/tests/services/reports.test.ts

/**
 * Reports Service Tests
 * Tests for frontend/app/services/reports.ts
 */

import { ReportsService } from '../../../../app/services/reports';

// Mock fetch globally
global.fetch = jest.fn();

describe('ReportsService', () => {
  beforeEach(() => {
    (fetch as jest.Mock).mockClear();
  });

  describe('generateReport', () => {
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
      expect(result.message).toBe('Report generated successfully');
      expect(fetch).toHaveBeenCalledWith(
        'http://localhost:8000/api/reports/generate',
        expect.objectContaining({
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(reportData),
        })
      );
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

    it('should handle network errors', async () => {
      (fetch as jest.Mock).mockRejectedValueOnce(new Error('Network error'));

      const reportData = {
        analysis_id: 'analysis-123',
        format: 'pdf' as const,
      };

      const result = await ReportsService.generateReport(reportData);

      expect(result.success).toBe(false);
      expect(result.error).toBe('Network error');
    });
  });

  describe('getReport', () => {
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
      expect(fetch).toHaveBeenCalledWith(
        'http://localhost:8000/api/reports/report-123',
        expect.objectContaining({
          method: 'GET',
          headers: { 'Content-Type': 'application/json' },
        })
      );
    });

    it('should handle report not found', async () => {
      (fetch as jest.Mock).mockResolvedValueOnce({
        ok: false,
        status: 404,
        json: async () => ({ detail: 'Report not found' }),
      });

      const result = await ReportsService.getReport('nonexistent-id');

      expect(result.success).toBe(false);
      expect(result.error).toBe('Report not found');
    });
  });

  describe('downloadReport', () => {
    it('should download report successfully', async () => {
      const mockBlob = new Blob(['PDF content'], { type: 'application/pdf' });
      (fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        blob: async () => mockBlob,
      });

      const result = await ReportsService.downloadReport('report-123');

      expect(result.success).toBe(true);
      expect(result.data).toBeInstanceOf(Blob);
      expect(fetch).toHaveBeenCalledWith(
        'http://localhost:8000/api/reports/download/report-123',
        expect.objectContaining({
          method: 'GET',
        })
      );
    });

    it('should handle download errors', async () => {
      (fetch as jest.Mock).mockResolvedValueOnce({
        ok: false,
        status: 404,
        json: async () => ({ detail: 'Report not found' }),
      });

      const result = await ReportsService.downloadReport('nonexistent-id');

      expect(result.success).toBe(false);
      expect(result.error).toBe('Report not found');
    });
  });

  describe('getReportHistory', () => {
    it('should get report history successfully', async () => {
      const mockHistory = {
        reports: [
          {
            report_id: 'report-1',
            analysis_id: 'analysis-1',
            status: 'completed',
            format: 'pdf',
            created_at: '2025-01-27T00:00:00Z',
          },
          {
            report_id: 'report-2',
            analysis_id: 'analysis-2',
            status: 'completed',
            format: 'json',
            created_at: '2025-01-26T00:00:00Z',
          },
        ],
        total: 2,
        page: 1,
        per_page: 10,
      };

      (fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => mockHistory,
      });

      const result = await ReportsService.getReportHistory({ page: 1, per_page: 10 });

      expect(result.success).toBe(true);
      expect(result.data).toEqual(mockHistory);
      expect(fetch).toHaveBeenCalledWith(
        'http://localhost:8000/api/reports/history?page=1&per_page=10',
        expect.objectContaining({
          method: 'GET',
          headers: { 'Content-Type': 'application/json' },
        })
      );
    });

    it('should get report history with default pagination', async () => {
      const mockHistory = { reports: [], total: 0, page: 1, per_page: 20 };

      (fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => mockHistory,
      });

      const result = await ReportsService.getReportHistory();

      expect(result.success).toBe(true);
      expect(fetch).toHaveBeenCalledWith(
        'http://localhost:8000/api/reports/history?page=1&per_page=20',
        expect.any(Object)
      );
    });

    it('should handle history errors', async () => {
      (fetch as jest.Mock).mockResolvedValueOnce({
        ok: false,
        status: 500,
        json: async () => ({ detail: 'Server error' }),
      });

      const result = await ReportsService.getReportHistory();

      expect(result.success).toBe(false);
      expect(result.error).toBe('Server error');
    });
  });

  describe('deleteReport', () => {
    it('should delete report successfully', async () => {
      (fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => ({ deleted: true }),
      });

      const result = await ReportsService.deleteReport('report-123');

      expect(result.success).toBe(true);
      expect(result.data).toEqual({ deleted: true });
      expect(result.message).toBe('Report deleted successfully');
      expect(fetch).toHaveBeenCalledWith(
        'http://localhost:8000/api/reports/report-123',
        expect.objectContaining({
          method: 'DELETE',
          headers: { 'Content-Type': 'application/json' },
        })
      );
    });

    it('should handle delete errors', async () => {
      (fetch as jest.Mock).mockResolvedValueOnce({
        ok: false,
        status: 404,
        json: async () => ({ detail: 'Report not found' }),
      });

      const result = await ReportsService.deleteReport('nonexistent-id');

      expect(result.success).toBe(false);
      expect(result.error).toBe('Report not found');
    });
  });

  describe('shareReport', () => {
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
      expect(fetch).toHaveBeenCalledWith(
        'http://localhost:8000/api/reports/share',
        expect.objectContaining({
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(shareOptions),
        })
      );
    });

    it('should handle share errors', async () => {
      (fetch as jest.Mock).mockResolvedValueOnce({
        ok: false,
        status: 400,
        json: async () => ({ detail: 'Invalid share options' }),
      });

      const result = await ReportsService.shareReport({
        report_id: 'report-123',
        expires_in_days: -1,
      });

      expect(result.success).toBe(false);
      expect(result.error).toBe('Invalid share options');
    });
  });

  describe('getReportTemplates', () => {
    it('should get report templates successfully', async () => {
      const mockTemplates = {
        templates: [
          {
            id: 'template-1',
            name: 'Standard Report',
            description: 'Standard biomarker analysis report',
            format: 'pdf',
            created_at: '2025-01-27T00:00:00Z',
          },
          {
            id: 'template-2',
            name: 'Detailed Report',
            description: 'Comprehensive biomarker analysis report',
            format: 'pdf',
            created_at: '2025-01-26T00:00:00Z',
          },
        ],
        total: 2,
      };

      (fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => mockTemplates,
      });

      const result = await ReportsService.getReportTemplates();

      expect(result.success).toBe(true);
      expect(result.data).toEqual(mockTemplates);
      expect(fetch).toHaveBeenCalledWith(
        'http://localhost:8000/api/reports/templates',
        expect.objectContaining({
          method: 'GET',
          headers: { 'Content-Type': 'application/json' },
        })
      );
    });

    it('should handle template errors', async () => {
      (fetch as jest.Mock).mockResolvedValueOnce({
        ok: false,
        status: 500,
        json: async () => ({ detail: 'Server error' }),
      });

      const result = await ReportsService.getReportTemplates();

      expect(result.success).toBe(false);
      expect(result.error).toBe('Server error');
    });
  });

  describe('createReportTemplate', () => {
    it('should create report template successfully', async () => {
      const mockTemplate = {
        id: 'template-123',
        name: 'Custom Template',
        description: 'User-created template',
        format: 'pdf',
        created_at: '2025-01-27T00:00:00Z',
      };

      (fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => mockTemplate,
      });

      const templateData = {
        name: 'Custom Template',
        description: 'User-created template',
        format: 'pdf' as const,
        sections: ['overview', 'biomarkers', 'recommendations'],
      };

      const result = await ReportsService.createReportTemplate(templateData);

      expect(result.success).toBe(true);
      expect(result.data).toEqual(mockTemplate);
      expect(fetch).toHaveBeenCalledWith(
        'http://localhost:8000/api/reports/templates',
        expect.objectContaining({
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(templateData),
        })
      );
    });

    it('should handle creation errors', async () => {
      (fetch as jest.Mock).mockResolvedValueOnce({
        ok: false,
        status: 400,
        json: async () => ({ detail: 'Invalid template data' }),
      });

      const result = await ReportsService.createReportTemplate({
        name: '',
        description: 'Invalid template',
        format: 'pdf' as const,
      });

      expect(result.success).toBe(false);
      expect(result.error).toBe('Invalid template data');
    });
  });

  describe('updateReportTemplate', () => {
    it('should update report template successfully', async () => {
      const mockTemplate = {
        id: 'template-123',
        name: 'Updated Template',
        description: 'Updated description',
        format: 'pdf',
        updated_at: '2025-01-27T00:00:00Z',
      };

      (fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => mockTemplate,
      });

      const templateData = {
        name: 'Updated Template',
        description: 'Updated description',
      };

      const result = await ReportsService.updateReportTemplate('template-123', templateData);

      expect(result.success).toBe(true);
      expect(result.data).toEqual(mockTemplate);
      expect(fetch).toHaveBeenCalledWith(
        'http://localhost:8000/api/reports/templates/template-123',
        expect.objectContaining({
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(templateData),
        })
      );
    });

    it('should handle update errors', async () => {
      (fetch as jest.Mock).mockResolvedValueOnce({
        ok: false,
        status: 404,
        json: async () => ({ detail: 'Template not found' }),
      });

      const result = await ReportsService.updateReportTemplate('nonexistent-id', {
        name: 'Updated',
      });

      expect(result.success).toBe(false);
      expect(result.error).toBe('Template not found');
    });
  });

  describe('deleteReportTemplate', () => {
    it('should delete report template successfully', async () => {
      (fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => ({ deleted: true }),
      });

      const result = await ReportsService.deleteReportTemplate('template-123');

      expect(result.success).toBe(true);
      expect(result.data).toEqual({ deleted: true });
      expect(fetch).toHaveBeenCalledWith(
        'http://localhost:8000/api/reports/templates/template-123',
        expect.objectContaining({
          method: 'DELETE',
          headers: { 'Content-Type': 'application/json' },
        })
      );
    });

    it('should handle delete errors', async () => {
      (fetch as jest.Mock).mockResolvedValueOnce({
        ok: false,
        status: 404,
        json: async () => ({ detail: 'Template not found' }),
      });

      const result = await ReportsService.deleteReportTemplate('nonexistent-id');

      expect(result.success).toBe(false);
      expect(result.error).toBe('Template not found');
    });
  });
});
