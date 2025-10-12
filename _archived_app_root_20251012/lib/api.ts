// frontend/app/lib/api.ts
export const API_BASE = process.env.NEXT_PUBLIC_API_BASE || 'http://127.0.0.1:8000';

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

export async function startAnalysis(payload: {
  biomarkers: Record<string, any>;
  user: Record<string, any>;
}): Promise<{ analysis_id: string }> {
  const res = await fetch(`${API_BASE}/api/analysis/start`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error(`startAnalysis failed: ${res.status}`);
  return res.json();
}

export async function getAnalysisResult(analysisId: string): Promise<any> {
  const url = `${API_BASE}/api/analysis/result?analysis_id=${encodeURIComponent(analysisId)}`;
  const res = await fetch(url);
  if (!res.ok) throw new Error(`getAnalysisResult failed: ${res.status}`);
  return res.json();
}
