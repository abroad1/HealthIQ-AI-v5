'use client'

import React from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '../../ui/card'
import { Button } from '../../ui/button'
import { CheckCircle, Play, ArrowLeft } from 'lucide-react'
import { useHealthWizardStore } from '../../../state/healthWizard'
import { useAnalysisStore } from '../../../state/analysisStore'
import { useRouter } from 'next/navigation'

export default function AnalysisLaunchStep() {
  const { biomarkers, questionnaire, setCurrentStep } = useHealthWizardStore()
  const { startAnalysis, isLoading: isAnalyzing } = useAnalysisStore()
  const router = useRouter()
  const [isStarting, setIsStarting] = React.useState(false)
  const [isSuccess, setIsSuccess] = React.useState(false)
  const [analysisId, setAnalysisId] = React.useState<string | null>(null)

  const handleStartAnalysis = async () => {
    setIsStarting(true)
    
    try {
      console.log('AnalysisLaunchStep: Starting analysis with data:', {
        biomarkers: biomarkers.length,
        questionnaire: Object.keys(questionnaire).length
      })

      // Convert biomarkers to the format expected by the backend API
      const biomarkerData = biomarkers.reduce((acc, biomarker) => {
        acc[biomarker.name] = {
          value: typeof biomarker.value === 'number' ? biomarker.value : parseFloat(biomarker.value as string),
          unit: biomarker.unit
        }
        return acc
      }, {} as Record<string, { value: number; unit: string }>)

      // Extract user data from questionnaire
      const userData = {
        user_id: 'temp_user_' + Date.now(), // Temporary user ID
        age: calculateAge(questionnaire.date_of_birth) || 35,
        sex: questionnaire.biological_sex?.toLowerCase() || 'male',
        height: extractHeight(questionnaire.height) || 180,
        weight: parseFloat(questionnaire.weight) || 75,
        questionnaire: questionnaire
      }

      console.log('AnalysisLaunchStep: Prepared analysis payload:', {
        biomarkers: biomarkerData,
        user: userData
      })

      // Make direct API call to backend
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/analysis/start`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          biomarkers: biomarkerData,
          user: userData
        }),
      })

      console.log('AnalysisLaunchStep: API response status:', response.status)

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`)
      }

      const result = await response.json()
      console.log('AnalysisLaunchStep: Analysis started successfully:', result)
      
      // Show success message briefly before redirect
      if (result.analysis_id) {
        console.log('AnalysisLaunchStep: Redirecting to results page with analysis_id:', result.analysis_id)
        
        // Set success state
        setIsSuccess(true)
        setAnalysisId(result.analysis_id)
        setIsStarting(false)
        
        // Small delay to show success state before redirect
        setTimeout(() => {
          router.push(`/results?analysis_id=${result.analysis_id}`)
        }, 2000)
      } else {
        throw new Error('No analysis_id received from server')
      }
    } catch (error) {
      console.error('AnalysisLaunchStep: Failed to start analysis:', error)
      // You might want to show an error message to the user here
    } finally {
      setIsStarting(false)
    }
  }

  // Helper function to calculate age from date of birth
  const calculateAge = (dateOfBirth: string): number | null => {
    if (!dateOfBirth) return null
    const today = new Date()
    const birthDate = new Date(dateOfBirth)
    let age = today.getFullYear() - birthDate.getFullYear()
    const monthDiff = today.getMonth() - birthDate.getMonth()
    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
      age--
    }
    return age
  }

  // Helper function to extract height in cm from feet/inches
  const extractHeight = (heightData: any): number | null => {
    if (!heightData || typeof heightData !== 'object') return null
    const feet = parseFloat(heightData.Feet) || 0
    const inches = parseFloat(heightData.Inches) || 0
    if (feet === 0 && inches === 0) return null
    return Math.round((feet * 12 + inches) * 2.54) // Convert to cm
  }

  const hasBiomarkers = biomarkers.length > 0
  const hasQuestionnaire = Object.keys(questionnaire).length > 0

  return (
    <div className="space-y-6">
      <div className="text-center">
        <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <CheckCircle className="h-8 w-8 text-green-600" />
        </div>
        <h3 className="text-2xl font-bold text-gray-900 mb-2">
          Ready for Analysis!
        </h3>
        <p className="text-gray-600">
          Your health data is complete. Let&apos;s generate your personalized health insights.
        </p>
      </div>

      {/* Data Summary */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {hasBiomarkers && (
          <Card className="bg-blue-50 border-blue-200">
            <CardContent className="pt-6">
              <div className="flex items-center space-x-2 text-blue-800">
                <CheckCircle className="h-5 w-5" />
                <span className="font-medium">Biomarker Data</span>
              </div>
              <p className="text-sm text-blue-700 mt-1">
                {biomarkers.length} biomarkers confirmed and ready for analysis
              </p>
            </CardContent>
          </Card>
        )}

        {hasQuestionnaire && (
          <Card className="bg-green-50 border-green-200">
            <CardContent className="pt-6">
              <div className="flex items-center space-x-2 text-green-800">
                <CheckCircle className="h-5 w-5" />
                <span className="font-medium">Lifestyle Data</span>
              </div>
              <p className="text-sm text-green-700 mt-1">
                Health and lifestyle questionnaire completed
              </p>
            </CardContent>
          </Card>
        )}
      </div>

      {/* Analysis Preview */}
      <Card>
        <CardHeader>
          <CardTitle>What to Expect</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            <div className="flex items-start space-x-3">
              <div className="w-2 h-2 bg-blue-600 rounded-full mt-2"></div>
              <div>
                <p className="font-medium">Personalized Health Score</p>
                <p className="text-sm text-gray-600">Overall health assessment based on your biomarkers</p>
              </div>
            </div>
            <div className="flex items-start space-x-3">
              <div className="w-2 h-2 bg-green-600 rounded-full mt-2"></div>
              <div>
                <p className="font-medium">Risk Analysis</p>
                <p className="text-sm text-gray-600">Identification of potential health risks and patterns</p>
              </div>
            </div>
            <div className="flex items-start space-x-3">
              <div className="w-2 h-2 bg-purple-600 rounded-full mt-2"></div>
              <div>
                <p className="font-medium">Personalized Recommendations</p>
                <p className="text-sm text-gray-600">Actionable insights tailored to your health profile</p>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Action Buttons */}
      <div className="flex justify-center space-x-4">
        <Button 
          variant="outline" 
          onClick={() => setCurrentStep('questionnaire')}
          disabled={isStarting || isAnalyzing}
        >
          <ArrowLeft className="h-4 w-4 mr-2" />
          Back to Questionnaire
        </Button>

        <Button 
          onClick={handleStartAnalysis}
          disabled={isStarting || isAnalyzing || isSuccess}
          className="bg-blue-600 hover:bg-blue-700 min-w-[160px]"
        >
          {isSuccess ? (
            <>
              <CheckCircle className="h-4 w-4 mr-2" />
              Analysis Started!
            </>
          ) : isStarting || isAnalyzing ? (
            <>
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
              Starting Analysis...
            </>
          ) : (
            <>
              <Play className="h-4 w-4 mr-2" />
              Start Analysis
            </>
          )}
        </Button>
      </div>

      {/* Success Message */}
      {isSuccess && analysisId && (
        <Card className="bg-green-50 border-green-200">
          <CardContent className="pt-6">
            <div className="text-center">
              <CheckCircle className="h-12 w-12 text-green-600 mx-auto mb-4" />
              <h3 className="text-lg font-semibold text-green-800 mb-2">
                Analysis Started Successfully!
              </h3>
              <p className="text-sm text-green-700 mb-2">
                Your analysis is now processing. Redirecting to results page...
              </p>
              <p className="text-xs text-green-600 font-mono">
                Analysis ID: {analysisId}
              </p>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Processing Time Info */}
      <div className="text-center">
        <p className="text-sm text-gray-500">
          Your analysis will be ready in approximately 2-3 minutes
        </p>
      </div>
    </div>
  )
}
