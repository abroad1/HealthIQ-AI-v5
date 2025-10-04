import { create } from 'zustand';
import { devtools } from 'zustand/middleware';
import { AnalysisService } from '../services/analysis';
import { BiomarkerValue, BiomarkerData, UserProfile, AnalysisRequest } from '../types/analysis';

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
  status: 'pending' | 'processing' | 'completed' | 'failed';
  progress?: number;
  results?: {
    biomarkers: BiomarkerResult[];
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
  
  // SSE connection
  eventSource: EventSource | null;
  
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
  completeAnalysis: (analysisId: string, results: AnalysisResult['results']) => Promise<void>;
  failAnalysis: (analysisId: string, error: AnalysisError) => void;
  clearAnalysis: () => void;
  retryAnalysis: () => void;
  
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
      eventSource: null,

      // Basic setters
      setCurrentAnalysis: (analysis) => set({ currentAnalysis: analysis }),
      
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
            currentPhase: 'idle',
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
            currentAnalysisId: analysisId,
            isLoading: false, // Set to false after successful start
            error: null,
            currentPhase: 'ingestion', // Move to ingestion phase
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
                console.log('SSE Event received:', data);
                
                // Handle analysis_status events
                if (data.phase && typeof data.progress === 'number') {
                  get().updateAnalysisProgress(analysisId, data.progress, data.phase);
                  
                  // Check if this is a completion event
                  if (data.phase === 'complete') {
                    get().completeAnalysis(analysisId, data.results);
                  }
                } else if (data.type === 'complete' || data.phase === 'complete') {
                  get().completeAnalysis(analysisId, data.results);
                } else if (data.type === 'error' || data.error) {
                  get().failAnalysis(analysisId, {
                    message: data.message || data.error || 'Analysis failed',
                    code: data.code || 'ANALYSIS_ERROR',
                    details: data.details,
                  });
                }
              } catch (error) {
                console.error('Failed to parse SSE event:', error);
              }
            },
            (error) => {
              console.error('SSE connection error:', error);
              // Only fail if analysis hasn't completed
              const state = get();
              if (state.currentPhase !== 'completed') {
                get().failAnalysis(analysisId, {
                  message: 'Connection lost during analysis',
                  code: 'CONNECTION_ERROR',
                  details: error,
                });
              } else {
                console.log('SSE error after completion - ignoring');
              }
            },
            () => {
              console.log('Analysis completed via SSE');
              get().completeAnalysis(analysisId, null);
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

      completeAnalysis: async (analysisId, results) => {
        const state = get();
        if (state.currentAnalysis?.analysis_id === analysisId) {
          try {
            // Fetch the full analysis results from the API
            const response = await AnalysisService.getAnalysisResult(analysisId);
            
            if (response.success && response.data) {
              const completedAnalysis: AnalysisResult = {
                ...state.currentAnalysis,
                ...response.data, // Use the properly mapped data from the service
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
            } else {
              // Fallback to the results passed in (if any)
              const completedAnalysis: AnalysisResult = {
                ...state.currentAnalysis,
                status: 'completed',
                progress: 100,
                results: results || {
                  biomarkers: [],
                  clusters: [],
                  insights: [],
                  risk_assessment: {},
                  recommendations: []
                },
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
          } catch (error) {
            console.error('Failed to fetch analysis results:', error);
            // Fallback to the results passed in (if any)
            const completedAnalysis: AnalysisResult = {
              ...state.currentAnalysis,
              status: 'completed',
              progress: 100,
              results: results || {
                biomarkers: [],
                clusters: [],
                insights: [],
                risk_assessment: {},
                recommendations: []
              },
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
        } else {
          // If no current analysis, just update the phase and progress
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
        // Close any active SSE connection
        const state = get();
        if (state.eventSource) {
          state.eventSource.close();
        }
        
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
