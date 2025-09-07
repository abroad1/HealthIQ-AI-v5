// frontend/src/lib/api.ts
export const API_BASE =
  (import.meta as any).env?.VITE_API_BASE || 'http://127.0.0.1:8000';

export async function pingHealth(): Promise<any> {
  const res = await fetch(`${API_BASE}/api/health`, { credentials: 'omit' });
  return res.json();
}

export function openAnalysisSSE(analysisId: string): EventSource {
  const url = `${API_BASE}/api/analysis/events?analysis_id=${encodeURIComponent(
    analysisId
  )}`;
  return new EventSource(url);
}
