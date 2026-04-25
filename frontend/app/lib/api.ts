// frontend/app/lib/api.ts
import { readAccessTokenCookie } from './auth-cookies';
import type { ApiAnalysisStartResponse } from '../types/analysis';

export const API_BASE = process.env.NEXT_PUBLIC_API_BASE || 'http://127.0.0.1:8000';

function analysisAuthHeaders(): Record<string, string> {
  if (typeof window === 'undefined') return {};
  const token =
    readAccessTokenCookie() ||
    (typeof localStorage !== 'undefined' ? localStorage.getItem('healthiq_auth_token') : null);
  if (!token) return {};
  return { Authorization: `Bearer ${token}` };
}

/** Bearer headers for authenticated API calls (wedge analytics, analysis, etc.). */
export function getApiAuthHeaders(): Record<string, string> {
  return analysisAuthHeaders();
}

export async function pingHealth(): Promise<any> {
  const res = await fetch(`${API_BASE}/api/health`, { credentials: 'omit' });
  return res.json();
}

// R-2A: /api/analysis/events is not used. Pipeline completes inside POST /api/analysis/start; load via GET /result.

export async function startAnalysis(payload: {
  biomarkers: Record<string, unknown>;
  user: Record<string, unknown>;
}): Promise<ApiAnalysisStartResponse> {
  const res = await fetch(`${API_BASE}/api/analysis/start`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', ...analysisAuthHeaders() },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error(`startAnalysis failed: ${res.status}`);
  return res.json() as Promise<ApiAnalysisStartResponse>;
}

export async function getAnalysisResult(analysisId: string): Promise<any> {
  const url = `${API_BASE}/api/analysis/result?analysis_id=${encodeURIComponent(analysisId)}`;
  const res = await fetch(url, {
    headers: { 'Content-Type': 'application/json', ...analysisAuthHeaders() },
  });
  if (!res.ok) throw new Error(`getAnalysisResult failed: ${res.status}`);
  return res.json();
}
