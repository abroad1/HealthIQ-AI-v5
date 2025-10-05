'use client'

import React, { useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '../../ui/card'
import { Button } from '../../ui/button'
import { FileUp, Edit3, CheckCircle } from 'lucide-react'
import FileDropzone from '../../upload/FileDropzone'
import PasteInput from '../../upload/PasteInput'
import BiomarkerForm from '../../forms/BiomarkerForm'
import { useHealthWizardStore } from '../../../state/healthWizard'
import { useParseUpload } from '../../../queries/parsing'
import { ParsedBiomarker } from '../../../types/parsed'

type InputMethod = 'upload' | 'manual' | null

export default function DataInputStep() {
  const [inputMethod, setInputMethod] = useState<InputMethod>(null)
  const { addBiomarkers, setCurrentStep, setError, clearError } = useHealthWizardStore()
  const parseUpload = useParseUpload()

  const handleFileUpload = async (file: File) => {
    clearError('upload')
    parseUpload.mutate({ file })
  }

  const handleTextPaste = async (text: string) => {
    clearError('paste')
    parseUpload.mutate({ text })
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
    setCurrentStep('review')
  }

  // Handle parse upload success
  React.useEffect(() => {
    if (parseUpload.isSuccess && parseUpload.data) {
      const { parsed_data } = parseUpload.data
      addBiomarkers(parsed_data.biomarkers)
      setCurrentStep('review')
    } else if (parseUpload.isError && parseUpload.error) {
      setError('upload', parseUpload.error.message || 'Failed to parse upload')
    }
  }, [parseUpload.isSuccess, parseUpload.isError, parseUpload.data, parseUpload.error, addBiomarkers, setCurrentStep, setError])

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
                onError={(error) => setError('upload', error)}
                disabled={parseUpload.isLoading}
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
                disabled={parseUpload.isLoading}
              />
            </CardContent>
          </Card>
        </div>

        {parseUpload.isLoading && (
          <div className="text-center py-8">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <p className="text-gray-600">Parsing your lab results...</p>
          </div>
        )}

        <div className="text-center">
          <Button 
            variant="outline" 
            onClick={() => setInputMethod(null)}
            disabled={parseUpload.isLoading}
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
              Upload a PDF or image of your lab results. We'll automatically extract and parse your biomarker values.
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
          Don't have your lab results? You can skip this step and complete the questionnaire only.
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
