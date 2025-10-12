/**
 * Supabase client configuration for HealthIQ AI v5.
 * TODO: Implement actual Supabase integration in Sprint 9b.
 */

import { createClient } from '@supabase/supabase-js';

// Environment variables (must be prefixed with NEXT_PUBLIC_)
const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

if (!supabaseUrl || !supabaseAnonKey) {
  throw new Error(
    'Missing Supabase environment variables. Please check your .env.local file.'
  );
}

// Create Supabase client
export const supabase = createClient(supabaseUrl, supabaseAnonKey, {
  auth: {
    autoRefreshToken: true,
    persistSession: true,
    detectSessionInUrl: true
  }
});

// Database types (to be defined in Sprint 9b)
export interface Database {
  public: {
    Tables: {
      profiles: {
        Row: {
          id: string;
          email: string;
          demographics: any;
          created_at: string;
          updated_at: string;
        };
        Insert: {
          id: string;
          email: string;
          demographics?: any;
          created_at?: string;
          updated_at?: string;
        };
        Update: {
          id?: string;
          email?: string;
          demographics?: any;
          created_at?: string;
          updated_at?: string;
        };
      };
      analyses: {
        Row: {
          id: string;
          user_id: string;
          status: 'pending' | 'processing' | 'completed' | 'failed';
          raw_biomarkers: any;
          questionnaire_data: any;
          created_at: string;
          updated_at: string;
          processing_time_seconds?: number;
        };
        Insert: {
          id: string;
          user_id: string;
          status: 'pending' | 'processing' | 'completed' | 'failed';
          raw_biomarkers?: any;
          questionnaire_data?: any;
          created_at?: string;
          updated_at?: string;
          processing_time_seconds?: number;
        };
        Update: {
          id?: string;
          user_id?: string;
          status?: 'pending' | 'processing' | 'completed' | 'failed';
          raw_biomarkers?: any;
          questionnaire_data?: any;
          created_at?: string;
          updated_at?: string;
          processing_time_seconds?: number;
        };
      };
      analysis_results: {
        Row: {
          id: string;
          analysis_id: string;
          biomarkers: any;
          clusters: any;
          insights: any;
          overall_score: number;
          risk_assessment: any;
          recommendations: string[];
          created_at: string;
        };
        Insert: {
          id: string;
          analysis_id: string;
          biomarkers?: any;
          clusters?: any;
          insights?: any;
          overall_score?: number;
          risk_assessment?: any;
          recommendations?: string[];
          created_at?: string;
        };
        Update: {
          id?: string;
          analysis_id?: string;
          biomarkers?: any;
          clusters?: any;
          insights?: any;
          overall_score?: number;
          risk_assessment?: any;
          recommendations?: string[];
          created_at?: string;
        };
      };
    };
  };
}

// Helper functions (to be implemented in Sprint 9b)
export const supabaseHelpers = {
  /**
   * Get user profile by ID.
   * TODO: Implement in Sprint 9b.
   */
  async getUserProfile(userId: string) {
    console.log(`Mock: Getting user profile for ${userId}`);
    return null;
  },

  /**
   * Save analysis result to database.
   * TODO: Implement in Sprint 9b.
   */
  async saveAnalysisResult(analysisId: string, result: any) {
    console.log(`Mock: Saving analysis result for ${analysisId}`);
    return null;
  },

  /**
   * Get analysis history for user.
   * TODO: Implement in Sprint 9b.
   */
  async getAnalysisHistory(userId: string, page: number = 1, limit: number = 10) {
    console.log(`Mock: Getting analysis history for user ${userId}`);
    return { data: [], count: 0 };
  }
};
