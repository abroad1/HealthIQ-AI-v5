// frontend/app/lib/api.ts
import { readAccessTokenCookie } from './auth-cookies';

export const API_BASE = process.env.NEXT_PUBLIC_API_BASE || 'http://127.0.0.1:8000';

function analysisAuthHeaders(): Record<string, string> {
  if (typeof window === 'undefined') return {};
  const token =
    readAccessTokenCookie() ||
    (typeof localStorage !== 'undefined' ? localStorage.getItem('healthiq_auth_token') : null);
  if (!token) return {};
  return { Authorization: `Bearer ${token}` };
}

export async function pingHealth(): Promise<any> {
  const res = await fetch(`${API_BASE}/api/health`, { credentials: 'omit' });
  return res.json();
}

// DEPRECATED: This function has no cleanup and is not used in production flow
// EventSource connections should be managed through AnalysisService.subscribeToAnalysisEvents()
// which includes proper cleanup and error handling
//
// export function openAnalysisSSE(analysisId: string): EventSource {
//   const url = `${API_BASE}/api/analysis/events?analysis_id=${encodeURIComponent(
//     analysisId
//   )}`;
//   return new EventSource(url);
// }

export async function startAnalysis(payload: {
  biomarkers: Record<string, any>;
  user: Record<string, any>;
}): Promise<{ analysis_id: string }> {
  const res = await fetch(`${API_BASE}/api/analysis/start`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', ...analysisAuthHeaders() },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error(`startAnalysis failed: ${res.status}`);
  return res.json();
}

export async function getAnalysisResult(analysisId: string): Promise<any> {
  const url = `${API_BASE}/api/analysis/result?analysis_id=${encodeURIComponent(analysisId)}`;
  const res = await fetch(url, {
    headers: { 'Content-Type': 'application/json', ...analysisAuthHeaders() },
  });
  if (!res.ok) throw new Error(`getAnalysisResult failed: ${res.status}`);
  return res.json();
}
