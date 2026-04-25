/**
 * Analysis API Service — POST /api/analysis/start (synchronous pipeline) + GET /api/analysis/result.
 * R-2A: do not use /api/analysis/events; progress is not streamed.
 */

import { 
  AnalysisRequest, 
  BiomarkerData, 
  UserProfile, 
  AnalysisResult, 
  AnalysisHistoryResponse,
  ExportRequest,
  ExportResponse,
  type ApiAnalysisStartResponse,
} from '../types/analysis';
import { ApiResponse, ApiError } from '../types/api';
import { readAccessTokenCookie } from '../lib/auth-cookies';
import { API_BASE } from '../lib/api';

/** FastAPI routes live under `/api/...`. `NEXT_PUBLIC_API_BASE` is the origin only (see env.local.example). */
function analysisApiRoot(): string {
  const base = API_BASE.replace(/\/$/, '');
  return base.endsWith('/api') ? base : `${base}/api`;
}

const API_URL = analysisApiRoot();

/**
 * Maps GET /api/analysis/result JSON into `AnalysisResult` without dropping backend fields (FE-R8A).
 * Spreads the server payload and normalizes array/meta/risk + required frontend aliases.
 */
export function normalizeAnalysisResultPayload(raw: unknown): AnalysisResult {
  if (raw === null || typeof raw !== 'object' || Array.isArray(raw)) {
    throw new Error('Invalid analysis result payload');
  }
  const r = raw as Record<string, unknown>;

  const biomarkers = Array.isArray(r.biomarkers) ? r.biomarkers : [];
  const clusters = Array.isArray(r.clusters) ? r.clusters : [];
  const insights = Array.isArray(r.insights) ? r.insights : [];
  const recommendations = Array.isArray(r.recommendations) ? r.recommendations : [];
  const meta =
    r.meta && typeof r.meta === 'object' && !Array.isArray(r.meta)
      ? (r.meta as Record<string, unknown>)
      : {};

  const riskRaw = r.risk_assessment;
  const risk_assessment =
    riskRaw === undefined || riskRaw === null
      ? {}
      : typeof riskRaw === 'object' && !Array.isArray(riskRaw)
        ? (riskRaw as Record<string, unknown>)
        : {};

  return {
    ...r,
    analysis_id: String(r.analysis_id ?? ''),
    biomarkers: biomarkers as AnalysisResult['biomarkers'],
    clusters: clusters as AnalysisResult['clusters'],
    insights: insights as AnalysisResult['insights'],
    recommendations,
    meta,
    risk_assessment,
    status: 'completed',
    clinician_report_v1: (r.clinician_report_v1 ?? null) as AnalysisResult['clinician_report_v1'],
    balanced_systems_v1: (r.balanced_systems_v1 ?? null) as AnalysisResult['balanced_systems_v1'],
    interpretation_display_layer_v1: (r.interpretation_display_layer_v1 ??
      null) as AnalysisResult['interpretation_display_layer_v1'],
    narrative_report_v1: (r.narrative_report_v1 ?? null) as AnalysisResult['narrative_report_v1'],
    overall_score:
      typeof r.overall_score === 'number'
        ? r.overall_score
        : r.overall_score === null
          ? null
          : null,
    result_version: typeof r.result_version === 'string' ? r.result_version : undefined,
    created_at: typeof r.created_at === 'string' ? r.created_at : undefined,
    completed_at: typeof r.completed_at === 'string' ? r.completed_at : undefined,
  } as AnalysisResult;
}

function analysisAuthHeaders(): Record<string, string> {
  if (typeof window === 'undefined') return {};
  const token =
    readAccessTokenCookie() ||
    (typeof localStorage !== 'undefined' ? localStorage.getItem('healthiq_auth_token') : null);
  if (!token) return {};
  return { Authorization: `Bearer ${token}` };
}

export class AnalysisService {
  /**
   * Start a new biomarker analysis
   */
  static async startAnalysis(data: AnalysisRequest): Promise<ApiResponse<ApiAnalysisStartResponse>> {
    console.log("📤 AnalysisService.startAnalysis() called with payload:", data);
    console.log("📤 Biomarkers count:", Object.keys(data.biomarkers).length);
    console.log("📤 User data:", data.user);
    
    try {
      const url = `${API_URL}/analysis/start`;
      console.log("🌐 POST /api/analysis/start →", url);
      console.log("📨 Request body:", JSON.stringify(data, null, 2));
      console.log("Outgoing payload:", data);
      
      // === BEGIN DEBUG LOGGING FOR OUTGOING ANALYSIS PAYLOAD ===
      try {
        console.group("[TRACE] Outgoing Analysis Payload");
        console.log("Payload keys:", Object.keys(data || {}));
        console.log("Biomarker count:", Object.keys(data?.biomarkers || {}).length);
        console.log("Sample biomarker keys:", Object.keys(data?.biomarkers || {}).slice(0, 5));
        console.log("User object:", data?.user || {});
        console.log(
          "[TRACE] Full Payload JSON:\n",
          JSON.stringify(data, null, 2)
        );
        console.groupEnd();
      } catch (err) {
        console.warn("[WARN] Failed to log outgoing payload:", err);
      }
      // === END DEBUG LOGGING ===
      
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...analysisAuthHeaders(),
        },
        body: JSON.stringify(data),
      });

      console.log("📥 Response status:", response.status, response.statusText);
      
      if (!response.ok) {
        const errorText = await response.clone().text();
        console.error("❌ Response error body:", errorText);
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`);
      }

      const result = (await response.json()) as ApiAnalysisStartResponse;
      console.log("✅ Response data:", result);

      if (result.status !== "completed") {
        return {
          data: null,
          success: false,
          error: result.message || "Analysis did not complete successfully",
        };
      }
      
      return {
        data: {
          analysis_id: result.analysis_id,
          status: result.status,
          message: result.message,
        },
        success: true,
        message: "Analysis started successfully",
      };
    } catch (error) {
      console.error("❌ AnalysisService.startAnalysis() error:", error);
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
      const response = await fetch(`${API_URL}/analysis/result?analysis_id=${encodeURIComponent(analysisId)}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          ...analysisAuthHeaders(),
        },
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`);
      }

      const result = await response.json();
      const analysisResult = normalizeAnalysisResultPayload(result);

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

    const age = user.chronological_age;
    if (typeof age !== 'number' || age < 0 || age > 150) {
      errors.push('chronological_age must be a number between 0 and 150');
    }

    if (!['male', 'female', 'other'].includes(user.sex)) {
      errors.push('Sex must be one of: male, female, other');
    }

    if (typeof user.weight_kg !== 'number' || user.weight_kg <= 0) {
      errors.push('weight_kg must be a positive number');
    }

    if (typeof user.height_cm !== 'number' || user.height_cm <= 0) {
      errors.push('height_cm must be a positive number');
    }

    return {
      valid: errors.length === 0,
      errors,
    };
  }

  /**
   * Get analysis history for the authenticated user (owner-scoped).
   */
  static async getAnalysisHistory(
    limit: number = 10,
    offset: number = 0
  ): Promise<ApiResponse<AnalysisHistoryResponse>> {
    try {
      const response = await fetch(
        `${API_URL}/analysis/history?limit=${limit}&offset=${offset}`,
        {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            ...analysisAuthHeaders(),
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
   * Download PDF summary (GET /api/analysis/export/pdf) — Sprint 4 retail summary; requires auth when DB is used.
   */
  static async downloadSummaryPdf(
    analysisId: string
  ): Promise<{ blob: Blob; filename: string } | { error: string }> {
    try {
      const url = `${API_URL}/analysis/export/pdf?analysis_id=${encodeURIComponent(analysisId)}`;
      const response = await fetch(url, {
        method: 'GET',
        headers: {
          ...analysisAuthHeaders(),
        },
      });
      if (!response.ok) {
        const errBody = await response.json().catch(() => ({}));
        const detail =
          typeof (errBody as { detail?: unknown }).detail === 'string'
            ? (errBody as { detail: string }).detail
            : `HTTP ${response.status}`;
        return { error: detail };
      }
      const cd = response.headers.get('Content-Disposition');
      let filename = `healthiq-summary-${analysisId.slice(0, 8)}.pdf`;
      if (cd) {
        const m = cd.match(/filename="?([^";\n]+)"?/i);
        if (m?.[1]) filename = m[1].trim();
      }
      const blob = await response.blob();
      if (!blob.size) {
        return { error: 'Empty PDF response' };
      }
      return { blob, filename };
    } catch (e) {
      return { error: e instanceof Error ? e.message : 'Failed to download PDF' };
    }
  }

  /**
   * Export analysis results (legacy JSON contract; not used for Sprint 4 PDF).
   */
  static async exportAnalysis(
    analysisId: string, 
    format: 'pdf' | 'json' | 'csv' = 'json',
    userId?: string
  ): Promise<ApiResponse<ExportResponse>> {
    try {
      const response = await fetch(`${API_URL}/analysis/export`, {
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