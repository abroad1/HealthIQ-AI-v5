'use client'

import React from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '../../ui/card'
import { Button } from '../../ui/button'
import { CheckCircle, ArrowLeft } from 'lucide-react'
import QuestionnaireForm from '../../forms/QuestionnaireForm'
import { useHealthWizardStore } from '../../../state/healthWizard'

export default function QuestionnaireStep() {
  const { questionnaire, setQuestionnaire, setCurrentStep, biomarkers } = useHealthWizardStore()
  const [isSubmitting, setIsSubmitting] = React.useState(false)

  const handleQuestionnaireSubmit = async (questionnaireData: any) => {
    setIsSubmitting(true)
    
    try {
      setQuestionnaire(questionnaireData)
      // Use setTimeout to avoid state update during render
      setTimeout(() => {
        setCurrentStep('complete')
      }, 0)
    } catch (error) {
      console.error('Failed to save questionnaire:', error)
    } finally {
      setIsSubmitting(false)
    }
  }

  const hasBiomarkers = biomarkers.length > 0

  return (
    <div className="space-y-6">
      <div className="text-center">
        <h3 className="text-lg font-semibold mb-2">
          Lifestyle & Health Habits
        </h3>
        <p className="text-gray-600">
          Help us understand your lifestyle for more personalized health insights
        </p>
      </div>

      {/* Summary of what we have so far */}
      {hasBiomarkers && (
        <Card className="bg-green-50 border-green-200">
          <CardContent className="pt-6">
            <div className="flex items-center space-x-2 text-green-800">
              <CheckCircle className="h-5 w-5" />
              <span className="font-medium">
                {biomarkers.length} biomarkers confirmed
              </span>
            </div>
            <p className="text-sm text-green-700 mt-1">
              Your biomarker data is ready. Now let&apos;s learn about your lifestyle to provide better insights.
            </p>
          </CardContent>
        </Card>
      )}

      {/* Questionnaire Form */}
      <Card>
        <CardHeader>
          <CardTitle>Health & Lifestyle Questionnaire</CardTitle>
        </CardHeader>
        <CardContent>
          <QuestionnaireForm
            onSubmit={handleQuestionnaireSubmit}
            onCancel={() => setCurrentStep('review')}
            initialData={questionnaire}
            isLoading={isSubmitting}
          />
        </CardContent>
      </Card>

      {/* Back to Review Option */}
      {hasBiomarkers && (
        <div className="text-center">
          <Button 
            variant="outline" 
            onClick={() => setCurrentStep('review')}
            className="mr-4"
          >
            <ArrowLeft className="h-4 w-4 mr-2" />
            Back to Biomarker Review
          </Button>
        </div>
      )}

      {/* Skip Option */}
      <div className="text-center pt-4 border-t">
        <p className="text-sm text-gray-500 mb-2">
          Want to proceed with just your biomarker data? You can skip the questionnaire.
        </p>
        <Button 
          variant="ghost" 
          onClick={() => setCurrentStep('complete')}
          disabled={isSubmitting}
        >
          Skip Questionnaire
        </Button>
      </div>
    </div>
  )
}
