'use client'

import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import type { ParsedBiomarker } from '../types/parsed'

// Questionnaire data type
export interface QuestionnaireData {
  [key: string]: any
}

interface HealthWizardStore {
  currentStep: 'input' | 'review' | 'questionnaire' | 'complete'
  biomarkers: ParsedBiomarker[]
  questionnaire: QuestionnaireData
  isLoading: boolean
  errors: Record<string, string>
  
  // Actions
  setCurrentStep: (step: HealthWizardStore['currentStep']) => void
  addBiomarkers: (biomarkers: ParsedBiomarker[]) => void
  updateBiomarker: (index: number, biomarker: ParsedBiomarker) => void
  setQuestionnaire: (questionnaire: QuestionnaireData) => void
  setLoading: (loading: boolean) => void
  setError: (key: string, error: string) => void
  clearError: (key: string) => void
  canProceed: () => boolean
  reset: () => void
}

export const useHealthWizardStore = create<HealthWizardStore>()(
  persist(
    (set, get) => ({
      currentStep: 'input',
      biomarkers: [],
      questionnaire: {
        full_name: '',
        email_address: '',
        phone_number: '',
        country: '',
        state_province: '',
        date_of_birth: '',
        biological_sex: '',
        height: { 'Feet': '', 'Inches': '' },
        weight: '',
        sleep_hours_nightly: '',
        sleep_quality_rating: 5,
        alcohol_drinks_weekly: '',
        tobacco_use: '',
        stress_level_rating: 5,
        vigorous_exercise_days: '',
        current_medications: '',
        long_term_medications: [],
        chronic_conditions: [],
        medical_conditions: [],
        current_symptoms: [],
        regular_migraines: '',
      },
      isLoading: false,
      errors: {},
      
      setCurrentStep: (step) => {
        console.debug('Health wizard: Setting step to', step)
        set({ currentStep: step })
      },
      
      addBiomarkers: (biomarkers) => {
        const existing = get().biomarkers
        const newBiomarkers = biomarkers.map(b => ({ 
          ...b, 
          status: 'raw' as const 
        }))
        console.debug('Health wizard: Adding biomarkers', {
          existing: existing.length,
          new: newBiomarkers.length,
          total: existing.length + newBiomarkers.length
        })
        set({ biomarkers: [...existing, ...newBiomarkers] })
      },
      
      updateBiomarker: (index, biomarker) => {
        const biomarkers = [...get().biomarkers]
        biomarkers[index] = { ...biomarker, status: 'edited' as const }
        console.debug('Health wizard: Updating biomarker', { index, name: biomarker.name })
        set({ biomarkers })
      },
      
      setQuestionnaire: (questionnaire) => {
        console.debug('Health wizard: Setting questionnaire data', {
          questionCount: Object.keys(questionnaire).length
        })
        set({ questionnaire })
      },
      
      setLoading: (loading) => set({ isLoading: loading }),
      
      setError: (key, error) => {
        const errors = { ...get().errors, [key]: error }
        set({ errors })
      },
      
      clearError: (key) => {
        const errors = { ...get().errors }
        delete errors[key]
        set({ errors })
      },
      
      canProceed: () => {
        const { currentStep, biomarkers, questionnaire } = get()
        
        switch (currentStep) {
          case 'input':
            return biomarkers.length > 0
          case 'review':
            return biomarkers.every(b => b.value && b.name)
          case 'questionnaire':
            // Check if all required fields are filled
            const requiredFields = [
              'full_name', 'email_address', 'phone_number', 'country', 
              'date_of_birth', 'biological_sex', 'height', 'weight',
              'sleep_hours_nightly', 'sleep_quality_rating', 'alcohol_drinks_weekly',
              'tobacco_use', 'stress_level_rating', 'vigorous_exercise_days',
              'current_medications', 'long_term_medications', 'chronic_conditions',
              'medical_conditions', 'current_symptoms', 'regular_migraines'
            ]
            
            return requiredFields.every(field => {
              const value = questionnaire[field]
              if (field === 'height') {
                return value && Object.values(value).some(v => v !== '' && v !== null && v !== undefined)
              } else if (['long_term_medications', 'chronic_conditions', 'medical_conditions', 'current_symptoms'].includes(field)) {
                return Array.isArray(value) && value.length > 0
              } else {
                return value !== '' && value !== null && value !== undefined
              }
            })
          case 'complete':
            return true
          default:
            return false
        }
      },
      
      reset: () => {
        console.debug('Health wizard: Resetting store')
        set({ 
          currentStep: 'input', 
          biomarkers: [], 
          questionnaire: {},
          errors: {}
        })
      }
    }),
    {
      name: 'health-wizard-store',
      partialize: (state) => ({
        currentStep: state.currentStep,
        biomarkers: state.biomarkers,
        questionnaire: state.questionnaire
      }),
      onRehydrateStorage: () => (state) => {
        console.debug('Health wizard: Store rehydrated', {
          step: state?.currentStep,
          biomarkerCount: state?.biomarkers?.length || 0,
          questionnaireKeys: Object.keys(state?.questionnaire || {}).length
        })
      }
    }
  )
)
