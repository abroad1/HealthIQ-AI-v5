import { create } from 'zustand';
import { devtools } from 'zustand/middleware';
import { AnalysisService } from '../services/analysis';
import { BiomarkerValue, BiomarkerData, UserProfile, AnalysisRequest } from '../types/analysis';

export interface AnalysisResult {
  analysis_id: string;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  progress?: number;
  results?: {
    clusters: any[];
    insights: any[];
    overall_score?: number;
    risk_assessment: Record<string, any>;
    recommendations: string[];
  };
  created_at: string;
  completed_at?: string;
  processing_time_seconds?: number;
}

export interface AnalysisError {
  message: string;
  code: string;
  details?: any;
}

interface AnalysisState {
  // Current analysis state
  currentAnalysis: AnalysisResult | null;
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
  
  // SSE connection
  eventSource: EventSource | null;
  
  // Actions
  setCurrentAnalysis: (analysis: AnalysisResult | null) => void;
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
  completeAnalysis: (analysisId: string, results: AnalysisResult['results']) => void;
  failAnalysis: (analysisId: string, error: AnalysisError) => void;
  clearAnalysis: () => void;
  retryAnalysis: () => void;
  
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
      eventSource: null,

      // Basic setters
      setCurrentAnalysis: (analysis) => set({ currentAnalysis: analysis }),
      
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

      // Complex actions
      startAnalysis: async (request) => {
        // Validate input data
        const biomarkerValidation = AnalysisService.validateBiomarkerData(request.biomarkers);
        const userValidation = AnalysisService.validateUserProfile(request.user);

        if (!biomarkerValidation.valid || !userValidation.valid) {
          const errors = [...biomarkerValidation.errors, ...userValidation.errors];
          set({
            error: {
              message: `Validation failed: ${errors.join(', ')}`,
              code: 'VALIDATION_ERROR',
              details: { biomarkerErrors: biomarkerValidation.errors, userErrors: userValidation.errors },
            },
            isLoading: false,
          });
          return;
        }

        set({
          isLoading: true,
          error: null,
          currentPhase: 'ingestion',
          progress: 0,
          rawBiomarkers: request.biomarkers,
          userProfile: request.user,
          questionnaireResponses: request.questionnaire || {},
        });

        try {
          // Call the API service
          const response = await AnalysisService.startAnalysis(request);
          
          if (!response.success) {
            throw new Error(response.error || 'Failed to start analysis');
          }

          const analysisId = response.data.analysis_id;
          const analysis: AnalysisResult = {
            analysis_id: analysisId,
            status: 'pending',
            progress: 0,
            created_at: new Date().toISOString(),
          };

          set({
            currentAnalysis: analysis,
            isLoading: true,
            error: null,
            currentPhase: 'ingestion',
            progress: 0,
          });

          // Add to history
          get().addToHistory(analysis);

          // Start listening to SSE events
          const eventSource = AnalysisService.subscribeToAnalysisEvents(
            analysisId,
            (event) => {
              try {
                const data = JSON.parse(event.data);
                if (data.type === 'progress') {
                  get().updateAnalysisProgress(analysisId, data.progress, data.phase);
                } else if (data.type === 'complete') {
                  get().completeAnalysis(analysisId, data.results);
                } else if (data.type === 'error') {
                  get().failAnalysis(analysisId, {
                    message: data.message,
                    code: data.code,
                    details: data.details,
                  });
                }
              } catch (error) {
                console.error('Failed to parse SSE event:', error);
              }
            },
            (error) => {
              console.error('SSE connection error:', error);
              get().failAnalysis(analysisId, {
                message: 'Connection lost during analysis',
                code: 'CONNECTION_ERROR',
                details: error,
              });
            },
            () => {
              console.log('Analysis completed via SSE');
            }
          );

          // Store event source for cleanup
          set({ eventSource });

        } catch (error) {
          set({
            error: {
              message: error instanceof Error ? error.message : 'Failed to start analysis',
              code: 'API_ERROR',
              details: error,
            },
            isLoading: false,
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

      completeAnalysis: (analysisId, results) => {
        const state = get();
        if (state.currentAnalysis?.analysis_id === analysisId) {
          const completedAnalysis: AnalysisResult = {
            ...state.currentAnalysis,
            status: 'completed',
            progress: 100,
            results,
            completed_at: new Date().toISOString(),
          };

          set({
            currentAnalysis: completedAnalysis,
            isLoading: false,
            currentPhase: 'completed',
            progress: 100,
            error: null,
          });

          // Update in history
          get().addToHistory(completedAnalysis);
        }
      },

      failAnalysis: (analysisId, error) => {
        const state = get();
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
        }
      },

      clearAnalysis: () => {
        // Close any active SSE connection
        const state = get();
        if (state.eventSource) {
          state.eventSource.close();
        }
        
        set({
          currentAnalysis: null,
          isLoading: false,
          error: null,
          currentPhase: 'idle',
          progress: 0,
          rawBiomarkers: {},
          normalizedBiomarkers: {},
          unmappedBiomarkers: [],
          questionnaireResponses: {},
          questionnaireCompleted: false,
          eventSource: null,
        });
      },

      retryAnalysis: () => {
        const state = get();
        if (state.currentAnalysis && state.userProfile) {
          const request: AnalysisRequest = {
            biomarkers: state.rawBiomarkers,
            user: state.userProfile,
            questionnaire: state.questionnaireResponses,
          };
          get().startAnalysis(request);
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
          .map(a => a.results?.overall_score)
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
