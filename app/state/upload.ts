'use client'

import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import { ParsedBiomarker, ParseMetadata, UploadError, UploadState } from '../types/parsed'

interface UploadStore extends UploadState {
  // Actions
  setStatus: (status: UploadState['status']) => void
  setParsedData: (data: ParsedBiomarker[]) => void
  updateBiomarker: (index: number, biomarker: ParsedBiomarker) => void
  setError: (error: UploadError | null) => void
  setAnalysisId: (id: string | null) => void
  setSourceMetadata: (metadata: ParseMetadata | null) => void
  
  // Workflow actions
  startUpload: () => void
  startParsing: () => void
  setParsedResults: (biomarkers: ParsedBiomarker[], analysisId: string, metadata: ParseMetadata) => void
  confirmAll: () => void
  reset: () => void
  
  // Computed state
  hasUnconfirmedBiomarkers: () => boolean
  allBiomarkersConfirmed: () => boolean
}

export const useUploadStore = create<UploadStore>()(
  persist(
    (set, get) => ({
  // Initial state
  status: 'idle',
  parsedData: [],
  error: null,
  analysisId: null,
  sourceMetadata: null,

  // Basic setters
  setStatus: (status) => set({ status }),
  
  setParsedData: (parsedData) => set({ parsedData }),
  
  updateBiomarker: (index, biomarker) => {
    const { parsedData } = get()
    const updatedData = [...parsedData]
    updatedData[index] = biomarker
    set({ parsedData: updatedData })
  },
  
  setError: (error) => set({ error }),
  
  setAnalysisId: (analysisId) => set({ analysisId }),
  
  setSourceMetadata: (sourceMetadata) => set({ sourceMetadata }),

  // Workflow actions
  startUpload: () => set({ 
    status: 'uploading', 
    error: null 
  }),
  
  startParsing: () => set({ 
    status: 'parsing', 
    error: null 
  }),
  
  setParsedResults: (biomarkers, analysisId, metadata) => {
    // Store biomarkers exactly as received from backend
    set({
      parsedData: biomarkers,
      analysisId,
      sourceMetadata: metadata,
      status: 'ready',
      error: null
    })
  },
  
  confirmAll: () => {
    set({
      status: 'confirmed'
    })
  },
  
  reset: () => set({
    status: 'idle',
    parsedData: [],
    error: null,
    analysisId: null,
    sourceMetadata: null
  }),

  // Computed state
  hasUnconfirmedBiomarkers: () => {
    const { status } = get()
    return status !== 'confirmed'
  },
  
  allBiomarkersConfirmed: () => {
    const { status } = get()
    return status === 'confirmed'
  }
}),
    {
      name: 'upload-store',
      // Only persist parsed data and analysis ID, not error states
      partialize: (state) => ({
        parsedData: state.parsedData,
        analysisId: state.analysisId,
        sourceMetadata: state.sourceMetadata,
        status: state.status
      })
    }
  )
)

// Selector hooks for common state patterns
export const useUploadStatus = () => useUploadStore(state => state.status)
export const useParsedData = () => useUploadStore(state => state.parsedData)
export const useUploadError = () => useUploadStore(state => state.error)
export const useAnalysisId = () => useUploadStore(state => state.analysisId)

// Selector hooks for computed state
export const useHasUnconfirmedBiomarkers = () => useUploadStore(state => state.hasUnconfirmedBiomarkers())
export const useAllBiomarkersConfirmed = () => useUploadStore(state => state.allBiomarkersConfirmed())

// Selector hooks for actions
export const useUploadActions = () => useUploadStore(state => ({
  setStatus: state.setStatus,
  setParsedData: state.setParsedData,
  updateBiomarker: state.updateBiomarker,
  setError: state.setError,
  setAnalysisId: state.setAnalysisId,
  setSourceMetadata: state.setSourceMetadata,
  startUpload: state.startUpload,
  startParsing: state.startParsing,
  setParsedResults: state.setParsedResults,
  confirmAll: state.confirmAll,
  reset: state.reset
}))

// Persistence middleware (optional - for localStorage persistence)
export const useUploadStoreWithPersistence = create<UploadStore>()(
  (set, get) => ({
    ...useUploadStore.getInitialState(),
    
    // Override reset to also clear localStorage
    reset: () => {
      localStorage.removeItem('upload-store')
      useUploadStore.getState().reset()
    },
    
    // Override setParsedResults to also persist to localStorage
    setParsedResults: (biomarkers, analysisId, metadata) => {
      useUploadStore.getState().setParsedResults(biomarkers, analysisId, metadata)
      // Persist to localStorage
      const state = get()
      localStorage.setItem('upload-store', JSON.stringify({
        parsedData: state.parsedData,
        analysisId: state.analysisId,
        sourceMetadata: state.sourceMetadata,
        status: state.status
      }))
    }
  })
)
