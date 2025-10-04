'use client'

import { useState, useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import { Button } from '../ui/button'
import { Card, CardContent } from '../ui/card'
import { Upload, FileText, AlertCircle } from 'lucide-react'

interface FileDropzoneProps {
  onFileSelect: (file: File) => void
  onError?: (error: string) => void
  maxSize?: number // in bytes
  acceptedTypes?: string[]
  disabled?: boolean
}

export default function FileDropzone({
  onFileSelect,
  onError,
  maxSize = 10 * 1024 * 1024, // 10MB default
  acceptedTypes = ['.pdf', '.txt', '.json', '.csv'],
  disabled = false
}: FileDropzoneProps) {
  const [isDragActive, setIsDragActive] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const onDrop = useCallback((acceptedFiles: File[]) => {
    const file = acceptedFiles[0]
    if (file) {
      setError(null)
      onFileSelect(file)
    }
  }, [onFileSelect])

  const onDropRejected = useCallback((rejectedFiles: any[]) => {
    const rejection = rejectedFiles[0]
    if (rejection.errors[0]?.code === 'file-too-large') {
      const errorMsg = `File too large. Maximum size is ${Math.round(maxSize / 1024 / 1024)}MB`
      setError(errorMsg)
      onError?.(errorMsg)
    } else if (rejection.errors[0]?.code === 'file-invalid-type') {
      const errorMsg = `Invalid file type. Accepted types: ${acceptedTypes.join(', ')}`
      setError(errorMsg)
      onError?.(errorMsg)
    }
  }, [maxSize, acceptedTypes, onError])

  const { getRootProps, getInputProps, isDragReject } = useDropzone({
    onDrop,
    onDropRejected,
    accept: acceptedTypes.reduce((acc, type) => {
      acc[type] = []
      return acc
    }, {} as Record<string, string[]>),
    maxSize,
    multiple: false,
    disabled
  })

  return (
    <Card className="w-full">
      <CardContent className="p-6">
        <div
          {...getRootProps()}
          className={`
            border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors
            ${isDragActive ? 'border-blue-500 bg-blue-50' : 'border-gray-300 hover:border-gray-400'}
            ${isDragReject ? 'border-red-500 bg-red-50' : ''}
            ${disabled ? 'opacity-50 cursor-not-allowed' : ''}
          `}
          onMouseEnter={() => setIsDragActive(true)}
          onMouseLeave={() => setIsDragActive(false)}
        >
          <input {...getInputProps()} />
          
          <div className="flex flex-col items-center space-y-4">
            <div className="p-3 bg-blue-100 rounded-full">
              <Upload className="h-8 w-8 text-blue-600" />
            </div>
            
            <div>
              <h3 className="text-lg font-semibold text-gray-900">
                Drop your lab report here
              </h3>
              <p className="text-sm text-gray-500 mt-1">
                or click to browse files
              </p>
            </div>
            
            <div className="flex items-center space-x-2 text-xs text-gray-400">
              <FileText className="h-4 w-4" />
              <span>PDF, TXT, JSON, CSV up to {Math.round(maxSize / 1024 / 1024)}MB</span>
            </div>
          </div>
        </div>
        
        {error && (
          <div className="mt-4 flex items-center space-x-2 text-red-600 text-sm">
            <AlertCircle className="h-4 w-4" />
            <span>{error}</span>
          </div>
        )}
      </CardContent>
    </Card>
  )
}
