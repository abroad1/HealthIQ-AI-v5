'use client'

import { useState, useEffect } from 'react'
import { Button } from '../ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card'
import { Input } from '../ui/input'
import { Label } from '../ui/label'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../ui/select'
import { Badge } from '../ui/badge'
import { X, Save, AlertCircle } from 'lucide-react'
import { ParsedBiomarker } from '../../types/parsed'

interface EditDialogProps {
  biomarker: ParsedBiomarker | null
  isOpen: boolean
  onSave: (biomarker: ParsedBiomarker) => void
  onCancel: () => void
}

const COMMON_UNITS = [
  'mg/dL',
  'mmol/L',
  'ng/mL',
  'pg/mL',
  'IU/mL',
  'U/L',
  'g/dL',
  '%',
  'cells/μL',
  'mg/L',
  'μg/dL',
  'mEq/L',
  'ng/dL',
  'pmol/L'
]

const COMMON_BIOMARKERS = [
  'Total Cholesterol',
  'HDL Cholesterol',
  'LDL Cholesterol',
  'Triglycerides',
  'Glucose',
  'HbA1c',
  'Insulin',
  'C-Reactive Protein',
  'ESR',
  'Ferritin',
  'Vitamin D',
  'B12',
  'Folate',
  'TSH',
  'T4',
  'T3',
  'Creatinine',
  'BUN',
  'ALT',
  'AST',
  'GGT',
  'ALP',
  'Bilirubin',
  'Albumin',
  'Hemoglobin',
  'Hematocrit',
  'WBC',
  'RBC',
  'Platelets',
  'Sodium',
  'Potassium',
  'Chloride',
  'CO2',
  'Calcium',
  'Phosphorus',
  'Magnesium'
]

export default function EditDialog({
  biomarker,
  isOpen,
  onSave,
  onCancel
}: EditDialogProps) {
  const [formData, setFormData] = useState({
    name: '',
    value: '',
    unit: '',
    status: 'edited' as ParsedBiomarker['status']
  })
  const [errors, setErrors] = useState<Record<string, string>>({})

  useEffect(() => {
    if (biomarker) {
      setFormData({
        name: biomarker.name,
        value: biomarker.value.toString(),
        unit: biomarker.unit,
        status: biomarker.status || 'edited'
      })
      setErrors({})
    }
  }, [biomarker])

  const validateForm = () => {
    const newErrors: Record<string, string> = {}

    if (!formData.name.trim()) {
      newErrors.name = 'Biomarker name is required'
    }

    if (!formData.value.trim()) {
      newErrors.value = 'Value is required'
    } else {
      const numValue = parseFloat(formData.value)
      if (isNaN(numValue)) {
        newErrors.value = 'Value must be a valid number'
      } else if (numValue < 0) {
        newErrors.value = 'Value must be positive'
      }
    }

    if (!formData.unit.trim()) {
      newErrors.unit = 'Unit is required'
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSave = () => {
    if (!validateForm()) {
      return
    }

    const numValue = parseFloat(formData.value)
    const editedBiomarker: ParsedBiomarker = {
      name: formData.name.trim(),
      value: isNaN(numValue) ? formData.value : numValue,
      unit: formData.unit.trim(),
      status: 'edited'
    }

    onSave(editedBiomarker)
  }

  const handleBiomarkerSelect = (biomarkerName: string) => {
    setFormData(prev => ({ ...prev, name: biomarkerName }))
  }

  if (!isOpen || !biomarker) {
    return null
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <Card className="w-full max-w-md max-h-[90vh] overflow-y-auto">
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-4">
          <CardTitle>Edit Biomarker</CardTitle>
          <Button
            variant="ghost"
            size="sm"
            onClick={onCancel}
          >
            <X className="h-4 w-4" />
          </Button>
        </CardHeader>
        
        <CardContent className="space-y-4">
          {/* Biomarker Name */}
          <div className="space-y-2">
            <Label htmlFor="name">Biomarker Name</Label>
            <div className="space-y-2">
              <Select onValueChange={handleBiomarkerSelect} value={formData.name}>
                <SelectTrigger>
                  <SelectValue placeholder="Select or type biomarker name" />
                </SelectTrigger>
                <SelectContent>
                  {COMMON_BIOMARKERS.map((biomarker) => (
                    <SelectItem key={biomarker} value={biomarker}>
                      {biomarker}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              <Input
                id="name"
                value={formData.name}
                onChange={(e) => setFormData(prev => ({ ...prev, name: e.target.value }))}
                placeholder="Enter biomarker name"
                className={errors.name ? 'border-red-500' : ''}
              />
            </div>
            {errors.name && (
              <div className="flex items-center space-x-1 text-destructive text-sm">
                <AlertCircle className="h-4 w-4" />
                <span>{errors.name}</span>
              </div>
            )}
          </div>

          {/* Value */}
          <div className="space-y-2">
            <Label htmlFor="value">Value</Label>
            <Input
              id="value"
              type="number"
              step="any"
              value={formData.value}
              onChange={(e) => setFormData(prev => ({ ...prev, value: e.target.value }))}
              placeholder="Enter value"
              className={errors.value ? 'border-red-500' : ''}
            />
            {errors.value && (
              <div className="flex items-center space-x-1 text-destructive text-sm">
                <AlertCircle className="h-4 w-4" />
                <span>{errors.value}</span>
              </div>
            )}
          </div>

          {/* Unit */}
          <div className="space-y-2">
            <Label htmlFor="unit">Unit</Label>
            <div className="space-y-2">
              <Select onValueChange={(value) => setFormData(prev => ({ ...prev, unit: value }))} value={formData.unit}>
                <SelectTrigger>
                  <SelectValue placeholder="Select unit" />
                </SelectTrigger>
                <SelectContent>
                  {COMMON_UNITS.map((unit) => (
                    <SelectItem key={unit} value={unit}>
                      {unit}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              <Input
                id="unit"
                value={formData.unit}
                onChange={(e) => setFormData(prev => ({ ...prev, unit: e.target.value }))}
                placeholder="Enter unit"
                className={errors.unit ? 'border-red-500' : ''}
              />
            </div>
            {errors.unit && (
              <div className="flex items-center space-x-1 text-destructive text-sm">
                <AlertCircle className="h-4 w-4" />
                <span>{errors.unit}</span>
              </div>
            )}
          </div>

          {/* Status */}
          <div className="space-y-2">
            <Label>Status</Label>
            <div className="flex items-center space-x-2">
              <Badge variant="default">Edited</Badge>
              <span className="text-sm text-muted-foreground">
                This biomarker has been modified from the original
              </span>
            </div>
          </div>

          {/* Actions */}
          <div className="flex space-x-2 pt-4">
            <Button
              onClick={handleSave}
              className="flex-1"
            >
              <Save className="h-4 w-4 mr-2" />
              Save Changes
            </Button>
            <Button
              onClick={onCancel}
              variant="outline"
              className="flex-1"
            >
              Cancel
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
