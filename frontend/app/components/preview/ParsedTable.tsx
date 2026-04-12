'use client'

import { useState } from 'react'
import { Button } from '../ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card'
import { Badge } from '../ui/badge'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '../ui/table'
import { Edit, Check, AlertCircle, AlertTriangle } from 'lucide-react'
import { ParsedBiomarker } from '../../types/parsed'
import EditDialog from './EditDialog'
import {
  formatReferenceRangeDisplay,
  rangeAttentionLevel,
} from '@/lib/uploadReferenceRange'

interface ParsedTableProps {
  biomarkers: ParsedBiomarker[]
  onBiomarkerEdit: (index: number, biomarker: ParsedBiomarker) => void
  onConfirmAll: () => void
  isLoading?: boolean
  error?: string | null
}

export default function ParsedTable({
  biomarkers,
  onBiomarkerEdit,
  onConfirmAll,
  isLoading = false,
  error = null
}: ParsedTableProps) {
  const [editingIndex, setEditingIndex] = useState<number | null>(null)

  const rangeBadge = (b: ParsedBiomarker) => {
    const att = rangeAttentionLevel({
      unit: b.unit,
      referenceRange: b.referenceRange,
      referenceText: b.referenceText,
      contextRangeOptions: b.contextRangeOptions,
      referenceType: b.referenceType,
      matchedLabelledBand: b.matchedLabelledBand,
    })
    const noUnit = !b.unit?.trim()
    if (noUnit) {
      return (
        <Badge variant="destructive" className="gap-1 font-normal">
          <AlertCircle className="h-3 w-3" />
          Unit required
        </Badge>
      )
    }
    if (att === 'no-lab-range-supplied') {
      return (
        <Badge variant="outline" className="gap-1 font-normal border-slate-300 text-slate-800 bg-slate-100">
          No lab range
        </Badge>
      )
    }
    if (att === 'incomplete-or-ambiguous') {
      return (
        <Badge variant="outline" className="gap-1 font-normal border-amber-500 text-amber-950 bg-amber-50">
          <AlertTriangle className="h-3 w-3" />
          Needs clarification
        </Badge>
      )
    }
    if (att === 'labelled-bands-resolved') {
      return (
        <Badge variant="outline" className="gap-1 font-normal border-emerald-400 text-emerald-950 bg-emerald-50">
          Interpretive match
        </Badge>
      )
    }
    if (att === 'context-selection-required') {
      return (
        <Badge variant="outline" className="gap-1 font-normal border-violet-400 text-violet-950 bg-violet-50">
          <AlertTriangle className="h-3 w-3" />
          Choose reference band
        </Badge>
      )
    }
    if (att === 'missing') {
      return (
        <Badge variant="secondary" className="gap-1 font-normal border-amber-500/60 text-amber-900 bg-amber-50">
          <AlertTriangle className="h-3 w-3" />
          Range needed
        </Badge>
      )
    }
    if (att === 'one-sided') {
      return (
        <Badge variant="outline" className="gap-1 font-normal border-slate-300 text-slate-800 bg-slate-50">
          One-sided range
        </Badge>
      )
    }
    if (att === 'partial') {
      return (
        <Badge variant="outline" className="gap-1 font-normal border-amber-400 text-amber-900">
          <AlertTriangle className="h-3 w-3" />
          Context / incomplete range
        </Badge>
      )
    }
    return null
  }

  const getStatusBadge = (status: ParsedBiomarker['status']) => {
    switch (status) {
      case 'raw':
        return <Badge variant="secondary">Raw</Badge>
      case 'edited':
        return <Badge variant="default">Edited</Badge>
      case 'confirmed':
        return <Badge variant="outline" className="text-[hsl(var(--status-excellent))] border-[hsl(var(--status-excellent))]">Confirmed</Badge>
      default:
        return <Badge variant="secondary">Raw</Badge>
    }
  }

  const handleEdit = (index: number) => {
    setEditingIndex(index)
  }

  const handleSaveEdit = (editedBiomarker: ParsedBiomarker) => {
    if (editingIndex !== null) {
      onBiomarkerEdit(editingIndex, editedBiomarker)
      setEditingIndex(null)
    }
  }

  const handleCancelEdit = () => {
    setEditingIndex(null)
  }

  const allConfirmed = biomarkers.every(b => b.status === 'confirmed')
  const hasUnconfirmed = biomarkers.some(b => b.status !== 'confirmed')

  if (error) {
    return (
      <Card className="w-full">
        <CardContent className="p-6">
          <div className="flex items-center space-x-2 text-destructive">
            <AlertCircle className="h-5 w-5" />
            <span>{error}</span>
          </div>
        </CardContent>
      </Card>
    )
  }

  if (biomarkers.length === 0) {
    return (
      <Card className="w-full">
        <CardContent className="p-6 text-center text-muted-foreground">
          No biomarkers found. Please upload or paste lab results to get started.
        </CardContent>
      </Card>
    )
  }

  return (
    <>
      <Card className="w-full">
        <CardHeader>
          <CardTitle className="flex items-center justify-between">
            <span>Parsed Biomarkers ({biomarkers.length})</span>
            <div className="flex items-center space-x-2">
              {hasUnconfirmed && (
                <Badge variant="outline" className="text-[hsl(var(--status-fair))] border-[hsl(var(--status-fair))]">
                  Review Required
                </Badge>
              )}
              {allConfirmed && (
                <Badge variant="outline" className="text-[hsl(var(--status-excellent))] border-[hsl(var(--status-excellent))]">
                  All Confirmed
                </Badge>
              )}
            </div>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="rounded-md border">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Biomarker</TableHead>
                  <TableHead>Value</TableHead>
                  <TableHead>Unit</TableHead>
                  <TableHead>Range</TableHead>
                  <TableHead>Attention</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead className="w-[100px]">Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {biomarkers.map((biomarker, index) => (
                  <TableRow key={index}>
                    <TableCell className="font-medium">
                      {biomarker.name}
                    </TableCell>
                    <TableCell className="font-mono text-sm max-w-[140px] break-all">
                      {typeof biomarker.value === 'number'
                        ? biomarker.value.toFixed(2)
                        : String(biomarker.value)}
                    </TableCell>
                    <TableCell>{biomarker.unit}</TableCell>
                    <TableCell className="max-w-md min-w-[200px] align-top text-sm whitespace-pre-wrap break-words">
                      {formatReferenceRangeDisplay(biomarker)}
                    </TableCell>
                    <TableCell>{rangeBadge(biomarker)}</TableCell>
                    <TableCell>
                      {getStatusBadge(biomarker.status)}
                    </TableCell>
                    <TableCell>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => handleEdit(index)}
                        disabled={isLoading}
                      >
                        <Edit className="h-4 w-4" />
                      </Button>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
          
          <div className="mt-4 flex justify-end">
            <Button
              onClick={onConfirmAll}
              disabled={isLoading || biomarkers.length === 0}
              className="min-w-[120px]"
            >
              {isLoading ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                  Processing...
                </>
              ) : (
                <>
                  <Check className="h-4 w-4 mr-2" />
                  Confirm All
                </>
              )}
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Edit Dialog */}
      <EditDialog
        biomarker={editingIndex !== null ? biomarkers[editingIndex] : null}
        isOpen={editingIndex !== null}
        onSave={handleSaveEdit}
        onCancel={handleCancelEdit}
      />
    </>
  )
}
