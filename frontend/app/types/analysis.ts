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
  user_id?: string;  // Optional user ID for profile linking
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
  value: number | null;
  unit: string;
  score?: number | null;
  percentile?: number | null;
  status?: string | null;
  reference_range?: {
    min: number | null;
    max: number | null;
    unit: string;
    source: string | null;
  } | null;
  interpretation?: string | null;
}

export interface Insight {
  id: string;
  category: string;
  summary?: string;
  description?: string;
  confidence?: number;
  severity?: string;
  recommendations?: string[];
  biomarkers_involved?: string[];
}

export interface Cluster {
  id: string;
  category: string;
  summary?: string;
  biomarkers_involved?: string[];
  score?: number;
}

export interface AnalysisResult {
  analysis_id: string;
  biomarkers: BiomarkerResult[];
  clusters: Cluster[];
  insights: Insight[];
  overall_score: number | null;
  status: string;
  created_at?: string;
  completed_at?: string;
  result_version?: string;
  risk_assessment?: Record<string, any>;
  recommendations?: string[];
  meta?: Record<string, any>;
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
