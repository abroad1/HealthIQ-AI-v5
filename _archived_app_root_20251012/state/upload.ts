'use client'

import { create } from 'zustand'
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
  getBiomarkersByStatus: (status: ParsedBiomarker['status']) => ParsedBiomarker[]
}

export const useUploadStore = create<UploadStore>((set, get) => ({
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
    updatedData[index] = { ...biomarker, status: 'edited' }
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
    // Mark all biomarkers as 'raw' initially
    const processedBiomarkers = biomarkers.map(biomarker => ({
      ...biomarker,
      status: 'raw' as const
    }))
    
    set({
      parsedData: processedBiomarkers,
      analysisId,
      sourceMetadata: metadata,
      status: 'ready',
      error: null
    })
  },
  
  confirmAll: () => {
    const { parsedData } = get()
    const confirmedData = parsedData.map(biomarker => ({
      ...biomarker,
      status: 'confirmed' as const
    }))
    
    set({
      parsedData: confirmedData,
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
    const { parsedData } = get()
    return parsedData.some(biomarker => biomarker.status !== 'confirmed')
  },
  
  allBiomarkersConfirmed: () => {
    const { parsedData } = get()
    return parsedData.length > 0 && parsedData.every(biomarker => biomarker.status === 'confirmed')
  },
  
  getBiomarkersByStatus: (status) => {
    const { parsedData } = get()
    return parsedData.filter(biomarker => biomarker.status === status)
  }
}))

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
