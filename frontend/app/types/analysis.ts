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

export interface AnalysisResult {
  analysis_id: string;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  progress?: number;
  results?: {
    scoring?: {
      overall_score: number;
      confidence: string;
      health_system_scores: Record<string, any>;
      missing_biomarkers: string[];
      recommendations: string[];
      lifestyle_adjustments: string[];
    };
    clustering?: {
      clusters: ClusterData[];
      clustering_summary: ClusteringSummary;
    };
  };
  created_at: string;
  completed_at?: string;
}
