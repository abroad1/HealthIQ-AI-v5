/**
 * Frontend-only narrowing of `meta.insight_graph.layer_c_features` (InsightGraphV1).
 * Mirrors backend LayerCFeatureBundleV1 — not a new API field.
 * @see backend/core/contracts/insight_graph_v1.py
 */

export interface MetabolicAgeFeatureV1 {
  metabolic_age: number;
  age_delta_years: number;
  homa_ir: number;
  severity: string;
  confidence: number;
  risk_flags: string[];
}

export interface HeartFeatureV1 {
  heart_resilience_score: number;
  severity: string;
  confidence: number;
  risk_factors: string[];
  ldl_hdl_ratio: number | null;
  tc_hdl_ratio: number | null;
  tg_hdl_ratio: number | null;
}

export interface InflammationFeatureV1 {
  inflammation_burden_score: number;
  severity: string;
  confidence: number;
  risk_factors: string[];
  nlr: number | null;
}

export interface FatigueFeatureV1 {
  severity: string;
  confidence: number;
  root_causes: string[];
  iron_status: string;
  thyroid_status: string;
  vitamin_status: string;
  inflammation_status: string;
  cortisol_status: string;
}

export interface DetoxFeatureV1 {
  detox_filtration_score: number;
  liver_score: number;
  kidney_score: number;
  severity: string;
  confidence: number;
  risk_factors: string[];
  egfr: number | null;
  egfr_source: string;
}

export interface LayerCFeatureBundleV1 {
  metabolic_age: MetabolicAgeFeatureV1;
  heart_insight: HeartFeatureV1;
  inflammation: InflammationFeatureV1;
  fatigue_root_cause: FatigueFeatureV1;
  detox_filtration: DetoxFeatureV1;
}
