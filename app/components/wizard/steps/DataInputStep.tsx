'use client'

import React, { useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '../../ui/card'
import { Button } from '../../ui/button'
import { FileUp, Edit3, CheckCircle } from 'lucide-react'
import FileDropzone from '../../upload/FileDropzone'
import PasteInput from '../../upload/PasteInput'
import BiomarkerForm from '../../forms/BiomarkerForm'
import { useHealthWizardStore } from '../../../state/healthWizard'
import { ParsedBiomarker } from '../../../types/parsed'

// API configuration
const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

type InputMethod = 'upload' | 'manual' | null

export default function DataInputStep() {
  const [inputMethod, setInputMethod] = useState<InputMethod>(null)
  const { addBiomarkers, setCurrentStep, setError, clearError, currentStep } = useHealthWizardStore()
  const [isParsing, setIsParsing] = useState(false)

  const handleFileUpload = async (file: File) => {
    clearError('upload')
    console.log('DataInputStep: File upload received:', {
      name: file.name,
      type: file.type,
      size: file.size
    })
    
    // File is now stored in FileDropzone component state
    // User can see the file preview with Remove and Parse buttons
    // No automatic progression - let user decide when to proceed
  }

  const handleFileRemove = () => {
    clearError('upload')
    console.log('DataInputStep: File removed')
    // File removal is handled by the FileDropzone component's internal state
  }

  const handleFileParse = async (file: File) => {
    clearError('upload')
    console.log('DataInputStep: Parsing file:', {
      name: file.name,
      type: file.type,
      size: file.size
    })
    
    setIsParsing(true)
    
    try {
      console.log('DataInputStep: Sending file to backend for Gemini parsing')
      
      // Create FormData for file upload
      const formData = new FormData()
      formData.append('file', file)
      
      // Send file to backend for real Gemini parsing
      const response = await fetch(`${API_BASE}/api/upload/parse`, {
        method: 'POST',
        body: formData,
      })
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`)
      }
      
      const data = await response.json()
      console.log('DataInputStep: Parsing successful:', data)
      
      if (!data.success) {
        throw new Error(data.message || 'Parsing failed')
      }
      
      // Extract biomarkers from the response
      const biomarkers = data.parsed_data.biomarkers.map((biomarker: any) => ({
        ...biomarker,
        status: 'raw' as const
      }))
      
      console.log('DataInputStep: Extracted biomarkers:', biomarkers)
      
      // Add real biomarkers to store
      addBiomarkers(biomarkers)
      
      // Proceed to review step
      console.log('DataInputStep: Proceeding to review step')
      setCurrentStep('review')
      
    } catch (error) {
      console.error('DataInputStep: Error during parsing:', error)
      setError('upload', `Error during parsing: ${error instanceof Error ? error.message : 'Unknown error'}`)
    } finally {
      setIsParsing(false)
    }
  }

  const handleTextPaste = async (text: string) => {
    clearError('paste')
    // TODO: Implement text parsing
    console.log('Text paste:', text)
  }

  const handleBiomarkerSubmit = (biomarkerData: any) => {
    // Convert biomarker form data to ParsedBiomarker format
    const biomarkers: ParsedBiomarker[] = Object.entries(biomarkerData).map(([name, value]) => ({
      name,
      value: value as number,
      unit: 'mg/dL', // Default unit, could be made configurable
      status: 'raw' as const
    }))
    
    addBiomarkers(biomarkers)
    // Use setTimeout to avoid state update during render
    setTimeout(() => {
      setCurrentStep('review')
    }, 0)
  }

  // TODO: Add parse upload success handling

  if (inputMethod === 'upload') {
    return (
      <div className="space-y-6">
        <div className="text-center">
          <h3 className="text-lg font-semibold mb-2">Upload Your Lab Report</h3>
          <p className="text-gray-600">Upload a PDF or image of your lab results</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <FileUp className="h-5 w-5" />
                Upload File
              </CardTitle>
            </CardHeader>
            <CardContent>
              <FileDropzone
                onFileSelect={handleFileUpload}
                onFileRemove={handleFileRemove}
                onFileParse={handleFileParse}
                onError={(error) => setError('upload', error)}
              />
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Edit3 className="h-5 w-5" />
                Paste Results
              </CardTitle>
            </CardHeader>
            <CardContent>
              <PasteInput
                onTextSubmit={handleTextPaste}
                onError={(error) => setError('paste', error)}
              />
            </CardContent>
          </Card>
        </div>

        {/* Loading state for file parsing */}
        {isParsing && (
          <div className="text-center p-4">
            <div className="inline-flex items-center space-x-2">
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-primary"></div>
              <span className="text-sm text-muted-foreground">Parsing file with Gemini AI...</span>
            </div>
          </div>
        )}

        <div className="text-center">
          <Button 
            variant="outline" 
            onClick={() => setInputMethod(null)}
          >
            Back to Options
          </Button>
        </div>
      </div>
    )
  }

  if (inputMethod === 'manual') {
    return (
      <div className="space-y-6">
        <div className="text-center">
          <h3 className="text-lg font-semibold mb-2">Manual Biomarker Entry</h3>
          <p className="text-gray-600">Enter your biomarker values directly</p>
        </div>

        <BiomarkerForm
          onSubmit={handleBiomarkerSubmit}
          isLoading={false}
          showSubmitButton={true}
        />

        <div className="text-center">
          <Button 
            variant="outline" 
            onClick={() => setInputMethod(null)}
          >
            Back to Options
          </Button>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-8">
      <div className="text-center">
        <h3 className="text-lg font-semibold mb-2">How would you like to provide your health data?</h3>
        <p className="text-gray-600">Choose the method that works best for you</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card 
          className="cursor-pointer hover:shadow-lg transition-shadow"
          onClick={() => setInputMethod('upload')}
        >
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <FileUp className="h-6 w-6 text-blue-600" />
              Upload Lab Report
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-gray-600 mb-4">
              Upload a PDF or image of your lab results. We&apos;ll automatically extract and parse your biomarker values.
            </p>
            <div className="flex items-center text-sm text-green-600">
              <CheckCircle className="h-4 w-4 mr-1" />
              Fastest option
            </div>
          </CardContent>
        </Card>

        <Card 
          className="cursor-pointer hover:shadow-lg transition-shadow"
          onClick={() => setInputMethod('manual')}
        >
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Edit3 className="h-6 w-6 text-green-600" />
              Manual Entry
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-gray-600 mb-4">
              Enter your biomarker values manually. Perfect if you have your results in a different format.
            </p>
            <div className="flex items-center text-sm text-blue-600">
              <CheckCircle className="h-4 w-4 mr-1" />
              Full control
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="text-center">
        <p className="text-sm text-gray-500">
          Don&apos;t have your lab results? You can skip this step and complete the questionnaire only.
        </p>
        <Button 
          variant="ghost" 
          onClick={() => setCurrentStep('questionnaire')}
          className="mt-2"
        >
          Skip to Questionnaire
        </Button>
      </div>
    </div>
  )
}
