'use client'

import { useState } from 'react'
import { Button } from '../ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card'
import { Badge } from '../ui/badge'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '../ui/table'
import { Edit, Check, X, AlertCircle } from 'lucide-react'
import { ParsedBiomarker } from '../../types/parsed'
import EditDialog from './EditDialog'

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

  const getStatusBadge = (status: ParsedBiomarker['status']) => {
    switch (status) {
      case 'raw':
        return <Badge variant="secondary">Raw</Badge>
      case 'edited':
        return <Badge variant="default">Edited</Badge>
      case 'confirmed':
        return <Badge variant="outline" className="text-green-600 border-green-600">Confirmed</Badge>
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
          <div className="flex items-center space-x-2 text-red-600">
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
        <CardContent className="p-6 text-center text-gray-500">
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
                <Badge variant="outline" className="text-orange-600 border-orange-600">
                  Review Required
                </Badge>
              )}
              {allConfirmed && (
                <Badge variant="outline" className="text-green-600 border-green-600">
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
                    <TableCell>
                      {typeof biomarker.value === 'number' 
                        ? biomarker.value.toFixed(2)
                        : biomarker.value
                      }
                    </TableCell>
                    <TableCell>{biomarker.unit}</TableCell>
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
