'use client'

import React from 'react'
import { useHealthWizardStore } from '../../state/healthWizard'
import WizardProgress from './WizardProgress'
import WizardNavigation from './WizardNavigation'
import DataInputStep from './steps/DataInputStep'
import DataReviewStep from './steps/DataReviewStep'
import QuestionnaireStep from './steps/QuestionnaireStep'
import AnalysisLaunchStep from './steps/AnalysisLaunchStep'
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card'
import { Alert, AlertDescription } from '../ui/alert'
import { AlertCircle } from 'lucide-react'

export default function HealthWizard() {
  const { currentStep, errors, isLoading } = useHealthWizardStore()

  const renderStep = () => {
    switch (currentStep) {
      case 'input':
        return <DataInputStep />
      case 'review':
        return <DataReviewStep />
      case 'questionnaire':
        return <QuestionnaireStep />
      case 'complete':
        return <AnalysisLaunchStep />
      default:
        return <DataInputStep />
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            🩺 Health Analysis Setup
          </h1>
          <p className="text-lg text-gray-600">
            Get personalized health insights from your lab results
          </p>
        </div>

        {/* Progress Indicator */}
        <WizardProgress currentStep={currentStep} />

        {/* Main Content */}
        <Card className="mb-6">
          <CardHeader>
            <CardTitle className="text-center">
              {currentStep === 'input' && 'Step 1: Your Health Data'}
              {currentStep === 'review' && 'Step 2: Review Your Data'}
              {currentStep === 'questionnaire' && 'Step 3: Lifestyle & Health Habits'}
              {currentStep === 'complete' && 'Ready for Analysis!'}
            </CardTitle>
          </CardHeader>
          <CardContent>
            {/* Error Display */}
            {Object.keys(errors).length > 0 && (
              <div className="mb-6 space-y-2">
                {Object.entries(errors).map(([key, error]) => (
                  <Alert key={key} className="border-red-200 bg-red-50">
                    <AlertCircle className="h-4 w-4 text-red-600" />
                    <AlertDescription className="text-red-800">
                      {error}
                    </AlertDescription>
                  </Alert>
                ))}
              </div>
            )}

            {/* Step Content */}
            {renderStep()}
          </CardContent>
        </Card>

        {/* Navigation */}
        <WizardNavigation isLoading={isLoading} />
      </div>
    </div>
  )
}
