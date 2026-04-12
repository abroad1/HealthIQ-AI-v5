'use client'

import { useState, useEffect } from 'react'
import { Button } from '../ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card'
import { Input } from '../ui/input'
import { Label } from '../ui/label'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../ui/select'
import { Badge } from '../ui/badge'
import { X, Save, AlertCircle, Copy } from 'lucide-react'
import { ParsedBiomarker } from '../../types/parsed'
import { Textarea } from '../ui/textarea'
import { parseBiomarkerValueForReview } from '@/lib/uploadReferenceRange'

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
  'pmol/L',
  'ratio',
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
  'Magnesium',
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
    refMin: '',
    refMax: '',
    refUnit: '',
    referenceText: '',
    status: 'edited' as ParsedBiomarker['status']
  })
  const [errors, setErrors] = useState<Record<string, string>>({})
  const [referenceTextUnlocked, setReferenceTextUnlocked] = useState(false)

  useEffect(() => {
    if (biomarker) {
      const r = biomarker.referenceRange
      setFormData({
        name: biomarker.name,
        value: biomarker.value.toString(),
        unit: biomarker.unit,
        refMin: r?.min != null && Number.isFinite(r.min) ? String(r.min) : '',
        refMax: r?.max != null && Number.isFinite(r.max) ? String(r.max) : '',
        refUnit: r?.unit ?? biomarker.unit ?? '',
        referenceText: biomarker.referenceText ?? '',
        status: biomarker.status || 'edited'
      })
      setErrors({})
      setReferenceTextUnlocked(false)
    }
  }, [biomarker])

  const validateForm = () => {
    const newErrors: Record<string, string> = {}

    if (!formData.name.trim()) {
      newErrors.name = 'Biomarker name is required'
    }

    const parsedVal = parseBiomarkerValueForReview(formData.value)
    if (parsedVal.ok === false) {
      newErrors.value = parsedVal.message
    }

    if (!formData.unit.trim()) {
      newErrors.unit = 'Unit is required'
    }

    const refMinN = formData.refMin.trim() === '' ? NaN : parseFloat(formData.refMin)
    const refMaxN = formData.refMax.trim() === '' ? NaN : parseFloat(formData.refMax)
    if (formData.refMin.trim() !== '' && !Number.isFinite(refMinN)) {
      newErrors.refMin = 'Enter a valid number or leave empty'
    }
    if (formData.refMax.trim() !== '' && !Number.isFinite(refMaxN)) {
      newErrors.refMax = 'Enter a valid number or leave empty'
    }
    if (
      Number.isFinite(refMinN) &&
      Number.isFinite(refMaxN) &&
      refMinN >= refMaxN
    ) {
      newErrors.refMax = 'Max must be greater than min when both are set'
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSave = () => {
    if (!validateForm() || !biomarker) {
      return
    }

    const parsedVal = parseBiomarkerValueForReview(formData.value)
    if (parsedVal.ok === false) return

    const refMinN = formData.refMin.trim() === '' ? undefined : parseFloat(formData.refMin)
    const refMaxN = formData.refMax.trim() === '' ? undefined : parseFloat(formData.refMax)
    const hasMin = refMinN !== undefined && Number.isFinite(refMinN)
    const hasMax = refMaxN !== undefined && Number.isFinite(refMaxN)
    const refUnit = (formData.refUnit.trim() || formData.unit.trim()).trim()

    let referenceRange: ParsedBiomarker['referenceRange'] = undefined
    if (hasMin || hasMax) {
      referenceRange = {
        min: hasMin ? refMinN : undefined,
        max: hasMax ? refMaxN : undefined,
        unit: refUnit,
      }
    }

    const editedBiomarker: ParsedBiomarker = {
      ...biomarker,
      name: formData.name.trim(),
      value: parsedVal.display,
      unit: formData.unit.trim(),
      referenceRange,
      referenceText: formData.referenceText.trim() || undefined,
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
      <Card className="w-full max-w-lg max-h-[90vh] overflow-y-auto">
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
              type="text"
              inputMode="decimal"
              autoComplete="off"
              value={formData.value}
              onChange={(e) => setFormData(prev => ({ ...prev, value: e.target.value }))}
              placeholder={'e.g. 5.2 or <0.05'}
              className={`font-mono text-sm ${errors.value ? 'border-red-500' : ''}`}
            />
            <p className="text-xs text-muted-foreground">
              Enter a number, or an inequality plus a number if your lab reported it that way (e.g. &lt;0.05).
            </p>
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

          {/* Reference range (manual correction) */}
          <div className="rounded-md border border-dashed p-3 space-y-3 bg-muted/30">
            <div className="flex items-center justify-between">
              <Label className="text-base">Reference range (lab)</Label>
              <Badge variant="outline" className="text-xs font-normal">Optional</Badge>
            </div>
            <p className="text-xs text-muted-foreground">
              Add or edit min and/or max if the parser missed your lab&apos;s interval. Leave one side empty when the
              lab only gives an upper or lower bound — both are not required.
            </p>
            <div className="grid grid-cols-2 gap-2">
              <div className="space-y-1">
                <Label htmlFor="refMin" className="text-xs">Min</Label>
                <Input
                  id="refMin"
                  type="number"
                  step="any"
                  value={formData.refMin}
                  onChange={(e) => setFormData(prev => ({ ...prev, refMin: e.target.value }))}
                  placeholder="—"
                  className={errors.refMin ? 'border-red-500' : ''}
                />
                {errors.refMin && <span className="text-xs text-destructive">{errors.refMin}</span>}
              </div>
              <div className="space-y-1">
                <Label htmlFor="refMax" className="text-xs">Max</Label>
                <Input
                  id="refMax"
                  type="number"
                  step="any"
                  value={formData.refMax}
                  onChange={(e) => setFormData(prev => ({ ...prev, refMax: e.target.value }))}
                  placeholder="—"
                  className={errors.refMax ? 'border-red-500' : ''}
                />
                {errors.refMax && <span className="text-xs text-destructive">{errors.refMax}</span>}
              </div>
            </div>
            <div className="space-y-2">
              <Label htmlFor="refUnit">Range unit</Label>
              <Input
                id="refUnit"
                value={formData.refUnit}
                onChange={(e) => setFormData(prev => ({ ...prev, refUnit: e.target.value }))}
                placeholder="Defaults to value unit if left blank when you save"
              />
            </div>
            <div className="space-y-2">
              <div className="flex items-center justify-between gap-2">
                <Label className="text-xs">Lab reference text (from your file)</Label>
                <div className="flex gap-1 shrink-0">
                  {formData.referenceText.trim() ? (
                    <Button
                      type="button"
                      variant="outline"
                      size="sm"
                      className="h-7 text-xs"
                      onClick={() => {
                        void navigator.clipboard?.writeText(formData.referenceText).catch(() => undefined)
                      }}
                    >
                      <Copy className="h-3 w-3 mr-1" />
                      Copy
                    </Button>
                  ) : null}
                  {!referenceTextUnlocked && (
                    <Button
                      type="button"
                      variant="ghost"
                      size="sm"
                      className="h-7 text-xs"
                      onClick={() => setReferenceTextUnlocked(true)}
                    >
                      {formData.referenceText.trim() ? 'Edit text' : 'Add text'}
                    </Button>
                  )}
                </div>
              </div>
              <p className="text-xs text-muted-foreground">
                Preserved from parsing for context. Analysis uses the numeric min/max fields above when set — not a
                substitute for correcting those bounds.
              </p>
              {referenceTextUnlocked ? (
                <Textarea
                  id="referenceText"
                  value={formData.referenceText}
                  onChange={(e) => setFormData(prev => ({ ...prev, referenceText: e.target.value }))}
                  placeholder="e.g. multi-line lab footnotes"
                  rows={5}
                  className="text-sm font-mono min-h-[120px]"
                />
              ) : (
                <div
                  className="rounded-md border bg-background px-3 py-2 text-sm font-mono whitespace-pre-wrap break-words max-h-48 overflow-y-auto select-all"
                  aria-readonly="true"
                >
                  {formData.referenceText.trim() ? formData.referenceText : '—'}
                </div>
              )}
            </div>
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
