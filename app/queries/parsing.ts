'use client'

import { useMutation } from '@tanstack/react-query'
import { ParseResponse, ValidationResponse, UseParseUploadResult, UseValidateParsedResult } from '../types/parsed'

/**
 * Base API URL for parsing endpoints
 */
const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

/**
 * Parse upload hook - calls backend /api/upload/parse
 * Handles both file uploads and text content parsing
 */
export function useParseUpload(): UseParseUploadResult {
  const mutation = useMutation({
    mutationFn: async ({ file, text }: { file?: File; text?: string }): Promise<ParseResponse> => {
      if (!file && !text) {
        throw new Error('Either file or text must be provided')
      }

      const formData = new FormData()
      
      if (file) {
        formData.append('file', file)
      }
      
      if (text) {
        formData.append('text_content', text)
      }

      const response = await fetch(`${API_BASE}/api/upload/parse`, {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`)
      }

      const data: ParseResponse = await response.json()
      
      if (!data.success) {
        throw new Error(data.message || 'Parsing failed')
      }

      return data
    },
    onError: (error) => {
      console.error('Parse upload error:', error)
    }
  })

  return {
    data: mutation.data,
    error: mutation.error,
    isLoading: mutation.isPending,
    isSuccess: mutation.isSuccess,
    isError: mutation.isError,
    mutate: mutation.mutate,
    reset: mutation.reset
  }
}

/**
 * Validate parsed content hook - calls backend /api/upload/validate
 * Validates file format and content before parsing
 */
export function useValidateParsed(): UseValidateParsedResult {
  const mutation = useMutation({
    mutationFn: async ({ file, text }: { file?: File; text?: string }): Promise<ValidationResponse> => {
      if (!file && !text) {
        throw new Error('Either file or text must be provided')
      }

      const formData = new FormData()
      
      if (file) {
        formData.append('file', file)
      }
      
      if (text) {
        formData.append('text_content', text)
      }

      const response = await fetch(`${API_BASE}/api/upload/validate`, {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`)
      }

      const data: ValidationResponse = await response.json()
      return data
    },
    onError: (error) => {
      console.error('Validation error:', error)
    }
  })

  return {
    data: mutation.data,
    error: mutation.error,
    isLoading: mutation.isPending,
    isSuccess: mutation.isSuccess,
    isError: mutation.isError,
    mutate: mutation.mutate,
    reset: mutation.reset
  }
}

/**
 * Combined parsing workflow hook
 * Validates first, then parses if validation succeeds
 */
export function useParsingWorkflow() {
  const validation = useValidateParsed()
  const parsing = useParseUpload()

  const validateAndParse = async ({ file, text }: { file?: File; text?: string }) => {
    try {
      // First validate
      validation.mutate({ file, text })
      
      // Wait for validation to complete
      if (validation.isSuccess && validation.data?.valid) {
        // Then parse
        parsing.mutate({ file, text })
      } else if (validation.isError) {
        throw validation.error
      }
    } catch (error) {
      console.error('Parsing workflow error:', error)
    }
  }

  return {
    validateAndParse,
    isValidationLoading: validation.isLoading,
    isParsingLoading: parsing.isLoading,
    isValidationSuccess: validation.isSuccess,
    isParsingSuccess: parsing.isSuccess,
    validationError: validation.error,
    parsingError: parsing.error,
    validationData: validation.data,
    parsingData: parsing.data,
    reset: () => {
      validation.reset()
      parsing.reset()
    }
  }
}

/**
 * Utility function to extract biomarkers from parse response
 */
export function extractBiomarkersFromResponse(response: ParseResponse) {
  return response.parsed_data.biomarkers.map(biomarker => ({
    ...biomarker,
    status: 'raw' as const
  }))
}

/**
 * Utility function to check if parsed data is ready for confirmation
 */
export function isParsedDataReady(biomarkers: any[]): boolean {
  return biomarkers.length > 0 && biomarkers.every(b => 
    b.name && b.value !== undefined && b.unit
  )
}
