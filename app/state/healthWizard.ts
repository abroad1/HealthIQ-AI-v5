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
      questionnaire: {},
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
            return Object.keys(questionnaire).length > 0
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
