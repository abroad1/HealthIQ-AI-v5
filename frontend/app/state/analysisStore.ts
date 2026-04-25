import { create } from 'zustand';
import { devtools } from 'zustand/middleware';
import { AnalysisService } from '../services/analysis';
import { emitWedgeEvent, emitWedgeEventOnce } from '../lib/wedgeAnalytics';
import {
  BiomarkerValue,
  BiomarkerData,
  UserProfile,
  AnalysisRequest,
  ClinicianReportV1,
  Cluster,
  type BiomarkerResult as ApiBiomarkerResult,
  type InterpretationDisplayLayerBundleV1,
  type NarrativeReportV1,
} from '../types/analysis';

/** Store row mirrors API BiomarkerResult (B1A/B1B explainer fields optional). */
export type BiomarkerResult = ApiBiomarkerResult;

export interface AnalysisResult {
  analysis_id: string;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  progress?: number;
  biomarkers: BiomarkerResult[];
  clusters: Cluster[];
  insights: any[];
  overall_score: number | null;
  recommendations?: string[];
  risk_assessment?: Record<string, any>;
  created_at?: string;
  completed_at?: string;
  processing_time_seconds?: number;
  result_version?: string;
  meta?: Record<string, any>;
  clinician_report_v1?: ClinicianReportV1 | null;
  balanced_systems_v1?: {
    intro_line: string;
    items: Array<{ system_topic: string; evidence_line: string; capacity_note?: string }>;
    context_line: string;
  } | null;
  interpretation_display_layer_v1?: InterpretationDisplayLayerBundleV1 | null;
  narrative_report_v1?: NarrativeReportV1 | null;
  primary_driver_system_id?: string;
  system_capacity_scores?: Record<string, unknown>;
  burden_hash?: string;
  derived_markers?: unknown;
  replay_manifest?: unknown;
}

export interface AnalysisError {
  message: string;
  code: string;
  details?: any;
}

interface AnalysisState {
  // Current analysis state
  currentAnalysis: AnalysisResult | null;
  currentAnalysisId: string | null;
  analysisHistory: AnalysisResult[];
  isLoading: boolean;
  error: AnalysisError | null;
  
  // Analysis workflow state
  currentPhase: 'idle' | 'ingestion' | 'normalization' | 'scoring' | 'clustering' | 'insights' | 'completed' | 'error';
  progress: number;
  
  // Biomarker data state
  rawBiomarkers: BiomarkerData;
  normalizedBiomarkers: BiomarkerData;
  unmappedBiomarkers: string[];
  
  // User context
  userProfile: UserProfile | null;
  
  // Questionnaire state
  questionnaireResponses: Record<string, any>;
  questionnaireCompleted: boolean;
  
  // Actions
  setCurrentAnalysis: (analysis: AnalysisResult | null) => void;
  setCurrentAnalysisId: (analysisId: string | null) => void;
  addToHistory: (analysis: AnalysisResult) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: AnalysisError | null) => void;
  setPhase: (phase: AnalysisState['currentPhase']) => void;
  setProgress: (progress: number) => void;
  setRawBiomarkers: (biomarkers: BiomarkerData) => void;
  setNormalizedBiomarkers: (biomarkers: BiomarkerData) => void;
  setUnmappedBiomarkers: (unmapped: string[]) => void;
  setUserProfile: (profile: UserProfile | null) => void;
  setQuestionnaireResponses: (responses: Record<string, any>) => void;
  setQuestionnaireCompleted: (completed: boolean) => void;
  
  // Complex actions
  startAnalysis: (request: AnalysisRequest) => Promise<void>;
  updateAnalysisProgress: (analysisId: string, progress: number, phase: string) => void;
  completeAnalysis: (analysisId: string) => Promise<void>;
  failAnalysis: (analysisId: string, error: AnalysisError) => void;
  clearAnalysis: () => void;
  retryAnalysis: () => Promise<void>;
  
  // Questionnaire actions
  setResponse: (id: string, value: any) => void;
  getResponse: (id: string) => any;
  resetResponses: () => void;
  
  // Utility actions
  getAnalysisById: (analysisId: string) => AnalysisResult | undefined;
  getRecentAnalyses: (limit?: number) => AnalysisResult[];
  isAnalysisComplete: () => boolean;
  getAnalysisSummary: () => {
    totalAnalyses: number;
    completedAnalyses: number;
    failedAnalyses: number;
    averageScore: number;
  };
}

export const useAnalysisStore = create<AnalysisState>()(
  devtools(
    (set, get) => ({
      // Initial state
      currentAnalysis: null,
      currentAnalysisId: null,
      analysisHistory: [],
      isLoading: false,
      error: null,
      currentPhase: 'idle',
      progress: 0,
      rawBiomarkers: {},
      normalizedBiomarkers: {},
      unmappedBiomarkers: [],
      userProfile: null,
      questionnaireResponses: {},
      questionnaireCompleted: false,

      // Basic setters
      setCurrentAnalysis: (analysis) => {
        console.debug('🔧 setCurrentAnalysis called with biomarkers count:', analysis?.biomarkers?.length);
        console.debug('🔧 setCurrentAnalysis biomarkers data:', analysis?.biomarkers);
        set({ currentAnalysis: analysis });
        const newState = get();
        console.debug('🔧 setCurrentAnalysis after update - biomarkers count:', newState.currentAnalysis?.biomarkers?.length);
      },
      
      setCurrentAnalysisId: (analysisId) => set({ currentAnalysisId: analysisId }),
      
      addToHistory: (analysis) => set((state) => ({
        analysisHistory: [analysis, ...state.analysisHistory.slice(0, 49)] // Keep last 50
      })),
      
      setLoading: (loading) => set({ isLoading: loading }),
      
      setError: (error) => set({ error }),
      
      setPhase: (phase) => set({ currentPhase: phase }),
      
      setProgress: (progress) => set({ progress: Math.max(0, Math.min(100, progress)) }),
      
      setRawBiomarkers: (biomarkers) => set({ rawBiomarkers: biomarkers }),
      
      setNormalizedBiomarkers: (biomarkers) => set({ normalizedBiomarkers: biomarkers }),
      
      setUnmappedBiomarkers: (unmapped) => set({ unmappedBiomarkers: unmapped }),
      
      setUserProfile: (profile) => set({ userProfile: profile }),
      
      setQuestionnaireResponses: (responses) => set({ questionnaireResponses: responses }),
      
      setQuestionnaireCompleted: (completed) => set({ questionnaireCompleted: completed }),

      // Questionnaire actions
      setResponse: (id, value) => set((state) => ({
        questionnaireResponses: { ...state.questionnaireResponses, [id]: value }
      })),
      
      getResponse: (id) => {
        const state = get();
        return state.questionnaireResponses[id];
      },
      
      resetResponses: () => set({ questionnaireResponses: {} }),

      // Complex actions
      startAnalysis: async (request) => {
        console.log("🔍 analysisStore.startAnalysis() called");
        
        // Validate input data
        const biomarkerValidation = AnalysisService.validateBiomarkerData(request.biomarkers);
        const userValidation = AnalysisService.validateUserProfile(request.user);
        
        console.log("🔍 Biomarker validation:", biomarkerValidation);
        console.log("🔍 User validation:", userValidation);

        if (!biomarkerValidation.valid || !userValidation.valid) {
          const errors = [...biomarkerValidation.errors, ...userValidation.errors];
          console.warn("⚠️ Validation failed in analysisStore:", errors);
          emitWedgeEvent({
            event_name: 'wedge_analysis_failed',
            timestamp: new Date().toISOString(),
            route: '/upload',
            error_class: 'validation',
          });
          set({
            error: {
              message: `Validation failed: ${errors.join(', ')}`,
              code: 'VALIDATION_ERROR',
              details: { biomarkerErrors: biomarkerValidation.errors, userErrors: userValidation.errors },
            },
            isLoading: false,
            currentPhase: 'idle',
          });
          return;
        }

        console.log("🔔 Phase changed to: ingestion");
        set({
          isLoading: true,
          error: null,
          currentPhase: 'ingestion',
          progress: 0,
          rawBiomarkers: request.biomarkers,
          userProfile: request.user,
          questionnaireResponses:
            (request.questionnaire_data ?? request.questionnaire ?? {}) as Record<string, unknown>,
        });

        try {
          // Call the API service
          const response = await AnalysisService.startAnalysis(request);

          if (!response.success || !response.data) {
            if (response.code === 'UPGRADE_REQUIRED') {
              emitWedgeEvent({
                event_name: 'wedge_analysis_paywall',
                timestamp: new Date().toISOString(),
                route: '/upload',
                error_class: 'upgrade_required',
              });
              set({
                error: {
                  message: response.error || 'Subscribe to run further analyses.',
                  code: 'UPGRADE_REQUIRED',
                },
                isLoading: false,
                currentPhase: 'idle',
              });
              return;
            }
            throw new Error(response.error || 'Failed to start analysis');
          }

          const analysisId = response.data.analysis_id;
          const analysis: AnalysisResult = {
            analysis_id: analysisId,
            status: 'processing',
            progress: 0,
            created_at: new Date().toISOString(),
            biomarkers: [],
            clusters: [],
            insights: [],
            overall_score: null,
          };

          set({
            currentAnalysis: analysis,
            currentAnalysisId: analysisId,
            isLoading: true,
            error: null,
            currentPhase: 'ingestion',
            progress: 0,
          });

          emitWedgeEvent({
            event_name: 'wedge_analysis_started',
            timestamp: new Date().toISOString(),
            route: '/upload',
            analysis_id: analysisId,
            phase: 'ingestion',
          });

          get().addToHistory(analysis);

          /** R-2A: pipeline runs in POST /start; no SSE. Hand off to useAnalysisResult → GET /result. */
          await get().completeAnalysis(analysisId);

        } catch (error) {
          emitWedgeEvent({
            event_name: 'wedge_analysis_failed',
            timestamp: new Date().toISOString(),
            route: '/upload',
            error_class: 'api_error',
          });
          set({
            error: {
              message: error instanceof Error ? error.message : 'Failed to start analysis',
              code: 'API_ERROR',
              details: error,
            },
            isLoading: false,
            currentPhase: 'idle', // Reset to idle on error
          });
        }
      },

      updateAnalysisProgress: (analysisId, progress, phase) => {
        const state = get();
        if (state.currentAnalysis?.analysis_id === analysisId) {
          set({
            currentAnalysis: {
              ...state.currentAnalysis,
              status: 'processing',
              progress,
            },
            progress,
            currentPhase: phase as AnalysisState['currentPhase'],
          });
        }
      },

      completeAnalysis: async (analysisId) => {
        const state = get();
        emitWedgeEventOnce(`wedge_completed:${analysisId}`, {
          event_name: 'wedge_analysis_completed',
          timestamp: new Date().toISOString(),
          route: '/results',
          analysis_id: analysisId,
          phase: 'completed',
        });
        if (state.currentAnalysis?.analysis_id === analysisId) {
          set({
            isLoading: false,
            currentPhase: 'completed',
            progress: 100,
            error: null,
          });
        } else {
          set({
            isLoading: false,
            currentPhase: 'completed',
            progress: 100,
            error: null,
          });
        }
      },

      failAnalysis: (analysisId, error) => {
        const state = get();
        const errClass = (error.code || 'analysis_error').toString().slice(0, 64);
        emitWedgeEventOnce(`wedge_failed:${analysisId}`, {
          event_name: 'wedge_analysis_failed',
          timestamp: new Date().toISOString(),
          route: '/results',
          analysis_id: analysisId,
          error_class: errClass,
        });
        if (state.currentAnalysis?.analysis_id === analysisId) {
          const failedAnalysis: AnalysisResult = {
            ...state.currentAnalysis,
            status: 'failed',
            completed_at: new Date().toISOString(),
          };

          set({
            currentAnalysis: failedAnalysis,
            isLoading: false,
            currentPhase: 'error',
            error,
          });

          // Update in history
          get().addToHistory(failedAnalysis);
        } else {
          // If no current analysis, just update the phase and error
          set({
            isLoading: false,
            currentPhase: 'error',
            error,
          });
        }
      },

      clearAnalysis: () => {
        set({
          currentAnalysis: null,
          currentAnalysisId: null,
          isLoading: false,
          error: null,
          currentPhase: 'idle',
          progress: 0,
          rawBiomarkers: {},
          normalizedBiomarkers: {},
          unmappedBiomarkers: [],
          questionnaireResponses: {},
          questionnaireCompleted: false,
        });
      },

      retryAnalysis: async () => {
        const state = get();
        if (state.currentAnalysis && state.userProfile) {
          const request: AnalysisRequest = {
            biomarkers: state.rawBiomarkers,
            user: state.userProfile,
            questionnaire_data: state.questionnaireResponses,
          };
          await get().startAnalysis(request);
        }
      },

      // Utility functions
      getAnalysisById: (analysisId) => {
        const state = get();
        return state.analysisHistory.find(analysis => analysis.analysis_id === analysisId);
      },

      getRecentAnalyses: (limit = 10) => {
        const state = get();
        return state.analysisHistory.slice(0, limit);
      },

      isAnalysisComplete: () => {
        const state = get();
        return state.currentAnalysis?.status === 'completed';
      },

      getAnalysisSummary: () => {
        const state = get();
        const analyses = state.analysisHistory;
        const completed = analyses.filter(a => a.status === 'completed');
        const failed = analyses.filter(a => a.status === 'failed');
        const scores = completed
          .map(a => a.overall_score)
          .filter(score => typeof score === 'number') as number[];
        
        return {
          totalAnalyses: analyses.length,
          completedAnalyses: completed.length,
          failedAnalyses: failed.length,
          averageScore: scores.length > 0 ? scores.reduce((a, b) => a + b, 0) / scores.length : 0,
        };
      },
    }),
    {
      name: 'analysis-store',
    }
  )
);
