'use client'

import React from 'react'
import { Check } from 'lucide-react'

interface WizardProgressProps {
  currentStep: 'input' | 'review' | 'questionnaire' | 'complete'
}

export default function WizardProgress({ currentStep }: WizardProgressProps) {
  const steps = [
    { key: 'input', label: 'Data Input', number: 1 },
    { key: 'review', label: 'Review', number: 2 },
    { key: 'questionnaire', label: 'Questionnaire', number: 3 },
    { key: 'complete', label: 'Complete', number: 4 }
  ] as const

  const currentIndex = steps.findIndex(step => step.key === currentStep)

  return (
    <div className="flex items-center justify-center space-x-4 mb-8">
      {steps.map((step, index) => (
        <div key={step.key} className="flex items-center">
          {/* Step Circle */}
          <div className={`
            w-10 h-10 rounded-full flex items-center justify-center text-sm font-medium
            transition-colors duration-200
            ${index <= currentIndex 
              ? 'bg-blue-600 text-white' 
              : 'bg-gray-200 text-gray-600'
            }
          `}>
            {index < currentIndex ? (
              <Check className="h-5 w-5" />
            ) : (
              step.number
            )}
          </div>

          {/* Step Label */}
          <div className="ml-2 text-sm font-medium text-gray-700">
            {step.label}
          </div>

          {/* Connector Line */}
          {index < steps.length - 1 && (
            <div className={`
              w-16 h-0.5 mx-4 transition-colors duration-200
              ${index < currentIndex ? 'bg-blue-600' : 'bg-gray-200'}
            `} />
          )}
        </div>
      ))}
    </div>
  )
}
