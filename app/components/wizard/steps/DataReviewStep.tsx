'use client'

import React from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '../../ui/card'
import { Button } from '../../ui/button'
import { Plus, CheckCircle } from 'lucide-react'
import ParsedTable from '../../preview/ParsedTable'
import BiomarkerForm from '../../forms/BiomarkerForm'
import { useHealthWizardStore } from '../../../state/healthWizard'
import { ParsedBiomarker } from '../../../types/parsed'

export default function DataReviewStep() {
  const { biomarkers, updateBiomarker, addBiomarkers, setCurrentStep } = useHealthWizardStore()
  const [showAddForm, setShowAddForm] = React.useState(false)

  const handleBiomarkerEdit = (index: number, biomarker: ParsedBiomarker) => {
    updateBiomarker(index, biomarker)
  }

  const handleAddBiomarkers = (biomarkerData: any) => {
    // Convert biomarker form data to ParsedBiomarker format
    const newBiomarkers: ParsedBiomarker[] = Object.entries(biomarkerData).map(([name, value]) => ({
      name,
      value: value as number,
      unit: 'mg/dL', // Default unit, could be made configurable
      status: 'raw' as const
    }))
    
    addBiomarkers(newBiomarkers)
    setShowAddForm(false)
  }

  const handleConfirmAll = () => {
    // Mark all biomarkers as confirmed and proceed
    biomarkers.forEach((biomarker, index) => {
      if (biomarker.status !== 'confirmed') {
        updateBiomarker(index, { ...biomarker, status: 'confirmed' })
      }
    })
    setCurrentStep('questionnaire')
  }

  if (biomarkers.length === 0) {
    return (
      <div className="space-y-6">
        <div className="text-center py-8">
          <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <Plus className="h-8 w-8 text-gray-400" />
          </div>
          <h3 className="text-lg font-semibold text-gray-900 mb-2">No biomarkers found</h3>
          <p className="text-gray-600 mb-6">
            It looks like no biomarkers were detected. You can add them manually or proceed to the questionnaire.
          </p>
          
          <div className="space-x-4">
            <Button onClick={() => setShowAddForm(true)}>
              <Plus className="h-4 w-4 mr-2" />
              Add Biomarkers
            </Button>
            <Button 
              variant="outline" 
              onClick={() => setCurrentStep('questionnaire')}
            >
              Skip to Questionnaire
            </Button>
          </div>
        </div>

        {showAddForm && (
          <Card>
            <CardHeader>
              <CardTitle>Add Biomarkers</CardTitle>
            </CardHeader>
            <CardContent>
              <BiomarkerForm
                onSubmit={handleAddBiomarkers}
                isLoading={false}
                showSubmitButton={true}
              />
              <div className="mt-4">
                <Button 
                  variant="outline" 
                  onClick={() => setShowAddForm(false)}
                >
                  Cancel
                </Button>
              </div>
            </CardContent>
          </Card>
        )}
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="text-center">
        <h3 className="text-lg font-semibold mb-2">
          Review Your Biomarker Data
        </h3>
        <p className="text-gray-600">
          Found {biomarkers.length} biomarkers. Review and edit as needed, then confirm to continue.
        </p>
      </div>

      {/* Biomarker Table */}
      <ParsedTable
        biomarkers={biomarkers}
        onBiomarkerEdit={handleBiomarkerEdit}
        onConfirmAll={handleConfirmAll}
        isLoading={false}
        error={null}
      />

      {/* Add More Biomarkers */}
      <div className="text-center">
        <Button 
          variant="outline" 
          onClick={() => setShowAddForm(true)}
          className="mr-4"
        >
          <Plus className="h-4 w-4 mr-2" />
          Add More Biomarkers
        </Button>
        
        <Button 
          onClick={handleConfirmAll}
          className="bg-green-600 hover:bg-green-700"
        >
          <CheckCircle className="h-4 w-4 mr-2" />
          Confirm All & Continue
        </Button>
      </div>

      {/* Add Form Modal */}
      {showAddForm && (
        <Card className="mt-6">
          <CardHeader>
            <CardTitle>Add Additional Biomarkers</CardTitle>
          </CardHeader>
          <CardContent>
            <BiomarkerForm
              onSubmit={handleAddBiomarkers}
              isLoading={false}
              showSubmitButton={true}
            />
            <div className="mt-4">
              <Button 
                variant="outline" 
                onClick={() => setShowAddForm(false)}
              >
                Cancel
              </Button>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Skip Option */}
      <div className="text-center pt-4 border-t">
        <p className="text-sm text-gray-500 mb-2">
          Don't want to review biomarkers? You can skip to the questionnaire.
        </p>
        <Button 
          variant="ghost" 
          onClick={() => setCurrentStep('questionnaire')}
        >
          Skip to Questionnaire
        </Button>
      </div>
    </div>
  )
}
