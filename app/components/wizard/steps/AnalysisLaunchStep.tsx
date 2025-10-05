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

  const handleStartAnalysis = async () => {
    setIsStarting(true)
    
    try {
      // Convert biomarkers to the format expected by the analysis store
      const biomarkerData = biomarkers.reduce((acc, biomarker) => {
        acc[biomarker.name] = {
          value: typeof biomarker.value === 'number' ? biomarker.value : parseFloat(biomarker.value as string),
          unit: biomarker.unit
        }
        return acc
      }, {} as Record<string, { value: number; unit: string }>)

      // Start analysis with biomarker and questionnaire data
      await startAnalysis({
        biomarkers: biomarkerData,
        user: {
          age: 35, // Default age, could be made configurable
          sex: 'male' as const, // Default sex, could be made configurable
          height: 180, // Default height, could be made configurable
          weight: 75 // Default weight, could be made configurable
        },
        questionnaire: Object.keys(questionnaire).length > 0 ? questionnaire : null
      })
      
      // Redirect to results page
      router.push('/results')
    } catch (error) {
      console.error('Failed to start analysis:', error)
    } finally {
      setIsStarting(false)
    }
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
          Your health data is complete. Let's generate your personalized health insights.
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
          disabled={isStarting || isAnalyzing}
          className="bg-blue-600 hover:bg-blue-700 min-w-[160px]"
        >
          {isStarting || isAnalyzing ? (
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

      {/* Processing Time Info */}
      <div className="text-center">
        <p className="text-sm text-gray-500">
          Your analysis will be ready in approximately 2-3 minutes
        </p>
      </div>
    </div>
  )
}
