/**
 * Analysis history service for retrieving user's past analyses.
 * TODO: Implement actual Supabase integration in Sprint 9b.
 */

export interface AnalysisHistoryItem {
  id: string;
  created_at: string;
  status: 'completed' | 'failed' | 'processing';
  biomarkers_count: number;
  overall_score?: number;
}

export interface HistoryResponse {
  history: AnalysisHistoryItem[];
  total: number;
  page: number;
  limit: number;
}

/**
 * Get analysis history for a user.
 * @param userId - User ID
 * @param page - Page number (default: 1)
 * @param limit - Items per page (default: 10)
 * @returns Promise<HistoryResponse>
 */
export async function getAnalysisHistory(
  userId: string,
  page: number = 1,
  limit: number = 10
): Promise<HistoryResponse> {
  // TODO: Implement actual Supabase query in Sprint 9b
  console.log(`Mock: Getting history for user ${userId}, page ${page}, limit ${limit}`);
  
  // Return mock data for now
  return {
    history: [],
    total: 0,
    page,
    limit
  };
}

/**
 * Get a specific analysis by ID.
 * @param analysisId - Analysis ID
 * @returns Promise<AnalysisHistoryItem | null>
 */
export async function getAnalysisById(analysisId: string): Promise<AnalysisHistoryItem | null> {
  // TODO: Implement actual Supabase query in Sprint 9b
  console.log(`Mock: Getting analysis ${analysisId}`);
  
  return null;
}
