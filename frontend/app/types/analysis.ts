import type { components } from './generated/openapi';

/** Regenerated from OpenAPI (`npm run generate-types`); use for request/response contract checks. */
export type ApiAnalysisStartRequest = components['schemas']['AnalysisStartRequest'];
export type ApiAnalysisStartResponse = components['schemas']['AnalysisStartResponse'];
export type ApiParseResponse = components['schemas']['ParseResponse'];

export interface BiomarkerValue {
  value: number;
  unit: string;
  timestamp?: string;
}

export interface BiomarkerData {
  [key: string]: BiomarkerValue;
}

/** Canonical analysis user context (CONTEXT-HARDENING-A). Server still accepts legacy aliases (age, height, weight, gender). */
export interface UserProfile {
  user_id?: string;
  chronological_age: number;
  sex: 'male' | 'female' | 'other';
  weight_kg: number;
  height_cm: number;
}

export interface AnalysisRequest {
  biomarkers: BiomarkerData;
  user: UserProfile;
  /** Canonical API field name; matches backend AnalysisStartRequest.questionnaire_data */
  questionnaire_data?: Record<string, unknown>;
  /** @deprecated use questionnaire_data — still serialized by some clients; prefer questionnaire_data */
  questionnaire?: Record<string, unknown>;
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

export interface BiomarkerReferenceRange {
  min: number | null;
  max: number | null;
  unit: string;
  source: string | null;
}

export interface BiomarkerResult {
  biomarker_name: string;
  value: number | null;
  unit: string;
  /** LC-S8G — customer-facing display (uploaded unit family when governed). */
  display_value?: number | null;
  display_unit?: string | null;
  display_reference_range?: BiomarkerReferenceRange | null;
  analytical_value?: number | null;
  analytical_unit?: string | null;
  analytical_reference_range?: BiomarkerReferenceRange | null;
  display_is_uploaded_unit?: boolean;
  /** LC-S8G — uploaded/source biomarker label when available (e.g. Hemoglobin vs Haemoglobin). */
  display_label?: string | null;
  analytical_transparency_unit?: string | null;
  score?: number | null;
  percentile?: number | null;
  status?: string | null;
  reference_range?: BiomarkerReferenceRange | null;
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
  /** Provenance — `legacy_v1` rows are gated off consumer surfaces (LC-S4). */
  manifest_id?: string;
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
      /** BE-W2-RQ2 — ranked runner-up from top_findings[1]; empty when not in close-call modes */
      runner_up_signal_id?: string;
      runner_up_topic_line?: string;
      runner_up_why_not_lead_line?: string;
    };
    root_cause: ClinicianRootCauseFindingV1 | null;
    confirmatory_tests: ClinicianConfirmatoryTestItem[];
  };
  suppressed_confirmatory_tests: string[];
}

/**
 * Backend `meta.narrative_runtime` — mirrors narrative_runtime_policy.narrative_runtime_meta_from_decision
 * plus optional `outcome` from synthesis when live call yields no validated insights.
 */
/** BE-IDL-1 / FE-R8 — mirrors backend/core/contracts/interpretation_display_layer_v1.py */
export type InterpretationScientificClassV1 =
  | 'phenotype'
  | 'risk_construct'
  | 'organ_pattern'
  | 'syndrome_state';

export type InterpretationFrontendAllowedTermV1 = 'phenotype_allowed' | 'clinical_only';

export type InterpretationSeverityStateV1 =
  | 'not_observed'
  | 'watch'
  | 'attention'
  | 'strong_signal';

export interface InterpretationDisplayRecordV1 {
  internal_id: string;
  scientific_class: InterpretationScientificClassV1;
  clinical_display_label: string;
  retail_display_label: string;
  subtitle: string;
  why_it_matters: string;
  severity_state: InterpretationSeverityStateV1;
  supporting_biomarkers_summary: string;
  frontend_allowed_term: InterpretationFrontendAllowedTermV1;
  display_order_priority: number;
  enabled_for_frontend: boolean;
  supporting_systems_summary?: string | null;
  user_safe_description?: string | null;
  future_commercial_domain?: string | null;
  display_caveat?: string | null;
}

export interface InterpretationDisplayLayerBundleV1 {
  schema_version: string;
  records: InterpretationDisplayRecordV1[];
}

/** N-8 / F-1 — mirrors backend `core/contracts/narrative_report_v1.py` (deterministic compiler output). */
export interface NarrativeReportV1 {
  narrative_report_version?: string;
  retail_summary: string;
  body_overview: string;
  lead_narrative: string;
  secondary_narratives: string;
  longitudinal_narrative: string;
  secondary_systems: string;
  next_steps_narrative: string;
  clinician_synthesis: string;
  meta?: Record<string, unknown>;
}

export interface NarrativeRuntimeMetaV1 {
  policy_version?: string;
  runtime_mode?: string;
  client_kind?: string;
  synthesizer_allow_llm_resolved?: boolean;
  master_switch_HEALTHIQ_NARRATIVE_LLM?: boolean;
  HEALTHIQ_ENABLE_LLM?: boolean;
  HEALTHIQ_MODE?: string;
  LLM_ENABLED?: boolean;
  policy_reason?: string;
  client_constructor_injected?: boolean;
  /** e.g. no_validated_insights_after_live_call — see backend core/insights/synthesis.py */
  outcome?: string;
}

/** D-6 — Wave 1 aligned drivers (from orchestrator `meta.wave1_aligned_drivers`) */
export interface Wave1AlignedDriversV1 {
  schema?: 'wave1_aligned_drivers_v1';
  biomarker_keys?: string[];
  by_domain?: Record<string, string[]>;
}

/** D-1/D-2/D-3 — Wave 1 customer domain card contract (mirrors Pydantic ConsumerDomainScoreV1) */
/** LC-S8D / FE-S8E — pre-arbitration upload row (Mode A fidelity). */
export interface UploadPanelObservation {
  value: number;
  unit: string;
}

/** LC-S8D — governed display policy metadata on analysis results (presentation only). */
export interface DisplayUnitPolicyBiomarkerEntry {
  uploaded_panel_fidelity?: {
    preserve_equivalent_rows?: boolean;
    equivalent_canonical_ids?: string[];
    legacy_input_units?: string[];
  };
}

export interface DisplayUnitPolicyMeta {
  display_unit_policy_version?: string;
  presentation_modes?: Record<string, unknown>;
  /** Present when backend embeds full policy; optional for older payloads. */
  biomarkers?: Record<string, DisplayUnitPolicyBiomarkerEntry>;
}

export interface AnalysisResultMetaV1 {
  upload_panel_observations?: Record<string, UploadPanelObservation | Record<string, unknown>>;
  display_unit_policy?: DisplayUnitPolicyMeta;
  [key: string]: unknown;
}

export interface ConsumerDomainScoreV1 {
  /** D-6 — bump when card assembly / narrative contract changes; current Wave 1 retail is 1.1 */
  card_schema_version?: string;
  domain_id: string;
  consumer_label: string;
  clinical_label: string;
  score: number;
  band_label: string;
  confidence_tier: 'high' | 'medium' | 'low';
  active_signal_ids: string[];
  primary_idl_record_id: string | null;
  missing_marker_ids: string[];
  source_track: string;
  caveat_flags: string[];
  contributing_system_keys: string[];
  raw_evidence_refs: Record<string, unknown>;
  headline_sentence: string;
  contributor_sentence: string;
  confidence_sentence: string;
  consequence_sentence: string;
  next_step_sentence: string;
  /** D-4: compact "based on" traceability line (collapsed card) */
  evidence_anchor_sentence?: string;
  /** DOMAIN-UX1A — plain-English descriptor (backend-emitted) */
  plain_english_descriptor?: string;
  evidence_completeness_numerator?: number;
  evidence_completeness_denominator?: number;
  subsystems?: unknown[] | null;
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
  /** Includes `narrative_runtime`, `upload_panel_observations`, `display_unit_policy` when present. */
  meta?: AnalysisResultMetaV1 & Record<string, unknown>;
  clinician_report_v1?: ClinicianReportV1 | null;
  /** BE-W2-RQ3 — deterministic balanced-system narrative; null when no stable systems to surface */
  balanced_systems_v1?: {
    intro_line: string;
    items: Array<{ system_topic: string; evidence_line: string; capacity_note?: string }>;
    context_line: string;
  } | null;
  /** FE-R8 — governed pattern cards (Section 5); sole retail display authority for this section */
  interpretation_display_layer_v1?: InterpretationDisplayLayerBundleV1 | null;
  /** N-8 — deterministic compiled narrative sections (F-1 surfaces in results journey) */
  narrative_report_v1?: NarrativeReportV1 | null;
  /** D-3 — Wave 1 three-domain consumer cards (retail; not clinician report) */
  consumer_domain_scores?: ConsumerDomainScoreV1[] | null;
  /** Passthrough from `build_analysis_result_dto` — cluster/engine context */
  primary_driver_system_id?: string;
  system_capacity_scores?: Record<string, unknown>;
  burden_hash?: string;
  derived_markers?: unknown;
  replay_manifest?: unknown;
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
