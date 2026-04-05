/**
 * Analysis history — delegates to AnalysisService (persisted, Bearer-scoped).
 * userId parameters on legacy helpers are ignored; server uses JWT identity.
 */

import { AnalysisService } from './analysis';
import type { AnalysisHistoryItem, AnalysisHistoryResponse } from '../types/analysis';

export type { AnalysisHistoryItem };
/** @deprecated Use AnalysisHistoryResponse from types/analysis */
export type HistoryResponse = AnalysisHistoryResponse;

/**
 * @param userId Retained for call-site compatibility; not sent to the API.
 */
export async function getAnalysisHistory(
  userId: string,
  page: number = 1,
  limit: number = 10,
): Promise<HistoryResponse> {
  void userId;
  const offset = (page - 1) * limit;
  const res = await AnalysisService.getAnalysisHistory(limit, offset);
  if (!res.success || !res.data) {
    throw new Error(res.error || 'Failed to get analysis history');
  }
  return res.data;
}

/**
 * Minimal summary by id — uses persisted result fetch.
 */
export async function getAnalysisById(analysisId: string): Promise<AnalysisHistoryItem | null> {
  const res = await AnalysisService.getAnalysisResult(analysisId);
  if (!res.success || !res.data) {
    return null;
  }
  const d = res.data;
  return {
    id: d.analysis_id,
    analysis_id: d.analysis_id,
    created_at: d.created_at || '',
    status: 'completed',
    overall_score: d.overall_score ?? null,
  };
}
