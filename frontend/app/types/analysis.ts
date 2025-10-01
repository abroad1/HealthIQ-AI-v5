// TODO: Define analysis types
export interface BiomarkerValue {
  value: number;
  unit: string;
  timestamp?: string;
}

export interface BiomarkerData {
  [key: string]: BiomarkerValue;
}

export interface UserProfile {
  age: number;
  sex: 'male' | 'female' | 'other';
  weight?: number;
  height?: number;
}

export interface AnalysisRequest {
  biomarkers: BiomarkerData;
  user: UserProfile;
  questionnaire?: Record<string, any>;
}

export interface ClusterData {
  cluster_id: string;
  name: string;
  biomarkers: string[];
  description: string;
  severity: 'normal' | 'mild' | 'moderate' | 'high' | 'critical';
  confidence: number;
}

export interface ClusteringSummary {
  total_clusters: number;
  algorithm_used: string;
  confidence_score: number;
  processing_time_ms: number;
  validation_summary: {
    total_clusters: number;
    valid_clusters: number;
    is_valid: boolean;
  };
}

export interface BiomarkerResult {
  biomarker_name: string;
  value: number;
  unit: string;
  score: number;
  percentile?: number;
  status: 'optimal' | 'normal' | 'elevated' | 'low' | 'critical';
  reference_range?: {
    min: number;
    max: number;
    unit: string;
  };
  interpretation: string;
}

export interface AnalysisResult {
  analysis_id: string;
  result_version: string;
  biomarkers: BiomarkerResult[];
  clusters: ClusterData[];
  insights: InsightData[];
  recommendations: string[];
  overall_score: number | null;
  meta: {
    confidence_score?: number;
    processing_metadata?: Record<string, any>;
  };
  created_at: string;
}

export interface InsightData {
  insight_id: string;
  title: string;
  description: string;
  category: string;
  confidence: number;
  severity: string;
  biomarkers: string[];
  recommendations: string[];
}

export interface AnalysisHistoryItem {
  id: string;
  created_at: string;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  overall_score: number | null;
  processing_time_seconds?: number;
}

export interface AnalysisHistoryResponse {
  history: AnalysisHistoryItem[];
  total: number;
  page: number;
  limit: number;
}

export interface ExportRequest {
  analysis_id: string;
  export_type: 'pdf' | 'json' | 'csv';
  user_id?: string;
}

export interface ExportResponse {
  export_id: string;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  message?: string;
}
