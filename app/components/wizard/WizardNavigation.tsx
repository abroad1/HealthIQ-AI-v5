'use client'

import React, { useState, useEffect } from 'react'
import { Button } from '../ui/button'
import { useHealthWizardStore } from '../../state/healthWizard'

interface WizardNavigationProps {
  isLoading?: boolean
}

export default function WizardNavigation({ isLoading = false }: WizardNavigationProps) {
  const { currentStep, canProceed, setCurrentStep } = useHealthWizardStore()
  const [isClient, setIsClient] = useState(false)

  useEffect(() => {
    setIsClient(true)
  }, [])

  const getNextStep = (current: string) => {
    switch (current) {
      case 'input': return 'review'
      case 'review': return 'questionnaire'
      case 'questionnaire': return 'complete'
      default: return null
    }
  }

  const getPrevStep = (current: string) => {
    switch (current) {
      case 'review': return 'input'
      case 'questionnaire': return 'review'
      case 'complete': return 'questionnaire'
      default: return null
    }
  }

  const handleNext = () => {
    const nextStep = getNextStep(currentStep)
    if (nextStep) {
      setCurrentStep(nextStep as any)
    }
  }

  const handleBack = () => {
    const prevStep = getPrevStep(currentStep)
    if (prevStep) {
      setCurrentStep(prevStep as any)
    }
  }

  const canGoBack = currentStep !== 'input'
  const isLastStep = currentStep === 'complete'

  return (
    <div className="flex justify-between items-center">
      <Button 
        variant="outline" 
        onClick={handleBack}
        disabled={!canGoBack || isLoading}
        className="min-w-[100px]"
      >
        Back
      </Button>

      <div className="text-sm text-gray-500">
        {currentStep === 'input' && 'Upload or enter your lab results to continue'}
        {currentStep === 'review' && 'Review and confirm your biomarker data'}
        {currentStep === 'questionnaire' && 'Complete the lifestyle questionnaire'}
        {currentStep === 'complete' && 'Ready to start your health analysis'}
      </div>

      <Button 
        onClick={handleNext}
        disabled={!isClient || !canProceed() || isLoading}
        className="min-w-[120px] bg-blue-600 hover:bg-blue-700"
      >
        {isLoading ? (
          <>
            <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
            Processing...
          </>
        ) : isLastStep ? (
          'Start Analysis'
        ) : (
          'Continue'
        )}
      </Button>
    </div>
  )
}
