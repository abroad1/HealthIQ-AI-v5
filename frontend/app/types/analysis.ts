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

/** FE-VISUALISATION-B1A — governed retail explainer payloads (optional on API). */
export interface BiomarkerEducationalExplainerV1 {
  schema_version: string;
  content_class: 'biomarker_education';
  biomarker_id: string;
  title: string;
  body: string;
}

export interface SystemEducationalExplainerV1 {
  schema_version: string;
  content_class: 'system_education';
  system_key: string;
  title: string;
  body: string;
}

export interface ContributionContextV1 {
  schema_version: string;
  content_class: 'contribution_context';
  relationship_kind: 'cluster_membership';
  factual_statement: string;
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
  /** Engine/lab mechanics — not retail educational explainer text */
  interpretation?: string | null;
  biomarker_educational_explainer?: BiomarkerEducationalExplainerV1 | null;
  contribution_context?: ContributionContextV1 | null;
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

/** Cluster objects returned on analysis results (cluster engine / API). */
export interface Cluster {
  id?: string;
  cluster_id?: string;
  name?: string;
  category?: string;
  summary?: string;
  description?: string;
  biomarkers?: string[];
  biomarkers_involved?: string[];
  score?: number;
  confidence?: number;
  severity?: string;
  recommendations?: string[];
  system_educational_explainer?: SystemEducationalExplainerV1 | null;
}

export interface ClinicianEvidenceItem {
  item: string;
  marker_refs: string[];
}

export interface ClinicianMissingDataItem {
  marker_id: string;
  reason: string;
}

export interface ClinicianConfirmatoryTestItem {
  test_id: string;
  display_name: string;
  rationale: string;
}

export interface ClinicianHypothesisV1 {
  hypothesis_id: string;
  title: string;
  summary: string;
  hypothesis_confidence: number;
  ranking_rationale: string;
  evidence_for: ClinicianEvidenceItem[];
  evidence_against: ClinicianEvidenceItem[];
  missing_data: ClinicianMissingDataItem[];
  confirmatory_tests: ClinicianConfirmatoryTestItem[];
  safety_class: 'monitoring' | 'clinician_referral' | 'lifestyle';
}

export interface ClinicianRootCauseFindingV1 {
  signal_id: string;
  signal_state: string;
  signal_confidence: number;
  primary_metric: string;
  hypotheses: ClinicianHypothesisV1[];
}

/** KB-S54B-FE — mirrors backend Page1SummaryBlockV1.primary_concern_mode */
export type PrimaryConcernModeV1 =
  | 'distinct_lead'
  | 'near_tie_ambiguity'
  | 'technical_tiebreak_lead';

export interface ClinicianReportV1 {
  header: {
    report_version: 'v1';
    disclaimer_top: string;
    footer_line: string;
  };
  data_quality: {
    panel_completeness_present: number;
    panel_completeness_expected: number;
    lab_range_quality_by_primary_metric: string[];
    confidence_caveat: string;
    data_quality_passed: boolean;
  };
  sections: {
    page1: {
      primary_concern: string;
      key_findings: string[];
      chains: string[];
      top_hypothesis_line: string;
      confidence_and_missing_data: string;
      /** Optional for older API payloads; defaults interpreted in renderer. */
      primary_concern_mode?: PrimaryConcernModeV1;
      co_primary_signal_ids?: string[];
      ranking_policy_version?: string;
    };
    root_cause: ClinicianRootCauseFindingV1 | null;
    confirmatory_tests: ClinicianConfirmatoryTestItem[];
  };
  suppressed_confirmatory_tests: string[];
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
  clinician_report_v1?: ClinicianReportV1 | null;
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
