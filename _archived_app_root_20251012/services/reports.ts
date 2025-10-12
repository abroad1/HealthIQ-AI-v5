/**
 * Reports API Service
 * Handles report generation, download, and management
 */

import { AnalysisResult } from '../types/analysis';
import { ApiResponse, PaginatedResponse } from '../types/api';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

export interface Report {
  id: string;
  analysis_id: string;
  title: string;
  type: 'summary' | 'detailed' | 'executive' | 'clinical';
  format: 'pdf' | 'html' | 'json';
  status: 'generating' | 'ready' | 'failed';
  created_at: string;
  completed_at?: string;
  download_url?: string;
  file_size?: number;
}

export interface ReportTemplate {
  id: string;
  name: string;
  description: string;
  type: 'summary' | 'detailed' | 'executive' | 'clinical';
  sections: string[];
  is_default: boolean;
}

export interface ReportGenerationRequest {
  analysis_id: string;
  template_id?: string;
  type: 'summary' | 'detailed' | 'executive' | 'clinical';
  format: 'pdf' | 'html' | 'json';
  include_charts?: boolean;
  include_recommendations?: boolean;
  custom_sections?: string[];
}

export class ReportsService {
  /**
   * Generate a new report
   */
  static async generateReport(request: ReportGenerationRequest): Promise<ApiResponse<Report>> {
    try {
      const response = await fetch(`${API_BASE_URL}/reports/generate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.getAuthToken()}`,
        },
        body: JSON.stringify(request),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`);
      }

      const result = await response.json();
      return {
        data: result,
        success: true,
        message: 'Report generation started successfully',
      };
    } catch (error) {
      return {
        data: null,
        success: false,
        error: error instanceof Error ? error.message : 'Failed to generate report',
      };
    }
  }

  /**
   * Get report by ID
   */
  static async getReport(reportId: string): Promise<ApiResponse<Report>> {
    try {
      const response = await fetch(`${API_BASE_URL}/reports/${encodeURIComponent(reportId)}`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${this.getAuthToken()}`,
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`);
      }

      const result = await response.json();
      return {
        data: result,
        success: true,
        message: 'Report retrieved successfully',
      };
    } catch (error) {
      return {
        data: null,
        success: false,
        error: error instanceof Error ? error.message : 'Failed to get report',
      };
    }
  }

  /**
   * Download report file
   */
  static async downloadReport(reportId: string): Promise<ApiResponse<Blob>> {
    try {
      const response = await fetch(`${API_BASE_URL}/reports/${encodeURIComponent(reportId)}/download`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${this.getAuthToken()}`,
        },
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`);
      }

      const blob = await response.blob();
      return {
        data: blob,
        success: true,
        message: 'Report downloaded successfully',
      };
    } catch (error) {
      return {
        data: null,
        success: false,
        error: error instanceof Error ? error.message : 'Failed to download report',
      };
    }
  }

  /**
   * Get report history with pagination
   */
  static async getReportHistory(params?: {
    page?: number;
    limit?: number;
    type?: string;
    status?: string;
  }): Promise<PaginatedResponse<Report>> {
    try {
      const searchParams = new URLSearchParams();
      if (params?.page) searchParams.set('page', params.page.toString());
      if (params?.limit) searchParams.set('limit', params.limit.toString());
      if (params?.type) searchParams.set('type', params.type);
      if (params?.status) searchParams.set('status', params.status);

      const response = await fetch(`${API_BASE_URL}/reports?${searchParams.toString()}`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${this.getAuthToken()}`,
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`);
      }

      const result = await response.json();
      return {
        data: result.data || result,
        success: true,
        message: 'Report history retrieved successfully',
        pagination: result.pagination || {
          page: 1,
          limit: 10,
          total: 0,
          totalPages: 0,
        },
      };
    } catch (error) {
      return {
        data: [],
        success: false,
        error: error instanceof Error ? error.message : 'Failed to get report history',
        pagination: {
          page: 1,
          limit: 10,
          total: 0,
          totalPages: 0,
        },
      };
    }
  }

  /**
   * Get available report templates
   */
  static async getReportTemplates(): Promise<ApiResponse<ReportTemplate[]>> {
    try {
      const response = await fetch(`${API_BASE_URL}/reports/templates`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${this.getAuthToken()}`,
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`);
      }

      const result = await response.json();
      return {
        data: result,
        success: true,
        message: 'Report templates retrieved successfully',
      };
    } catch (error) {
      return {
        data: [],
        success: false,
        error: error instanceof Error ? error.message : 'Failed to get report templates',
      };
    }
  }

  /**
   * Delete a report
   */
  static async deleteReport(reportId: string): Promise<ApiResponse<{ deleted: boolean }>> {
    try {
      const response = await fetch(`${API_BASE_URL}/reports/${encodeURIComponent(reportId)}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${this.getAuthToken()}`,
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`);
      }

      const result = await response.json();
      return {
        data: result,
        success: true,
        message: 'Report deleted successfully',
      };
    } catch (error) {
      return {
        data: { deleted: false },
        success: false,
        error: error instanceof Error ? error.message : 'Failed to delete report',
      };
    }
  }

  /**
   * Get report status
   */
  static async getReportStatus(reportId: string): Promise<ApiResponse<{ status: string; progress?: number }>> {
    try {
      const response = await fetch(`${API_BASE_URL}/reports/${encodeURIComponent(reportId)}/status`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${this.getAuthToken()}`,
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`);
      }

      const result = await response.json();
      return {
        data: result,
        success: true,
        message: 'Report status retrieved successfully',
      };
    } catch (error) {
      return {
        data: { status: 'unknown' },
        success: false,
        error: error instanceof Error ? error.message : 'Failed to get report status',
      };
    }
  }

  /**
   * Create a shareable link for a report
   */
  static async createShareableLink(reportId: string, expiresIn?: number): Promise<ApiResponse<{ share_url: string; expires_at: string }>> {
    try {
      const response = await fetch(`${API_BASE_URL}/reports/${encodeURIComponent(reportId)}/share`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${this.getAuthToken()}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ expires_in: expiresIn }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`);
      }

      const result = await response.json();
      return {
        data: result,
        success: true,
        message: 'Shareable link created successfully',
      };
    } catch (error) {
      return {
        data: null,
        success: false,
        error: error instanceof Error ? error.message : 'Failed to create shareable link',
      };
    }
  }

  /**
   * Get authentication token
   */
  private static getAuthToken(): string {
    return localStorage.getItem('healthiq_auth_token') || '';
  }

  /**
   * Trigger file download in browser
   */
  static triggerDownload(blob: Blob, filename: string): void {
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
  }

  /**
   * Get report statistics
   */
  static async getReportStatistics(): Promise<ApiResponse<{
    total_reports: number;
    reports_by_type: Record<string, number>;
    reports_by_status: Record<string, number>;
    total_size: number;
    last_generated?: string;
  }>> {
    try {
      const response = await fetch(`${API_BASE_URL}/reports/statistics`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${this.getAuthToken()}`,
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`);
      }

      const result = await response.json();
      return {
        data: result,
        success: true,
        message: 'Report statistics retrieved successfully',
      };
    } catch (error) {
      return {
        data: {
          total_reports: 0,
          reports_by_type: {},
          reports_by_status: {},
          total_size: 0,
        },
        success: false,
        error: error instanceof Error ? error.message : 'Failed to get report statistics',
      };
    }
  }
}