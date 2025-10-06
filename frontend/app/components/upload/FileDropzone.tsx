'use client'

import { useState, useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import { Button } from '../ui/button'
import { Card, CardContent } from '../ui/card'
import { Upload, FileText, AlertCircle, X, Play } from 'lucide-react'

interface FileDropzoneProps {
  onFileParse: (file: File) => void
  onError?: (error: string) => void
  maxSize?: number // in bytes
  acceptedTypes?: string[]
  disabled?: boolean
  isParsing?: boolean
}

export default function FileDropzone({
  onFileParse,
  onError,
  maxSize = 10 * 1024 * 1024, // 10MB default
  acceptedTypes = ['application/pdf', 'text/plain', 'application/json', 'text/csv'],
  disabled = false,
  isParsing = false
}: FileDropzoneProps) {
  const [isDragActive, setIsDragActive] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [selectedFile, setSelectedFile] = useState<File | null>(null)

  const onDrop = useCallback((acceptedFiles: File[]) => {
    const file = acceptedFiles[0]
    if (file) {
      setError(null)
      setSelectedFile(file)
    }
  }, [])

  const handleParse = () => {
    if (selectedFile) {
      onFileParse(selectedFile)
    }
  }

  const handleRemove = () => {
    setSelectedFile(null)
    setError(null)
  }

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
    accept: {
      'application/pdf': ['.pdf'],
      'text/plain': ['.txt'],
      'text/csv': ['.csv'],
      'application/json': ['.json'],
    },
    maxSize,
    multiple: false,
    disabled: disabled || isParsing
  })

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
  }

  return (
    <Card className="w-full">
      <CardContent className="p-6">
        {!selectedFile ? (
          <div
            {...getRootProps()}
            className={`
              border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors
              ${isDragActive ? 'border-primary bg-primary/5' : 'border-border hover:border-primary/50'}
              ${isDragReject ? 'border-destructive bg-destructive/5' : ''}
              ${disabled || isParsing ? 'opacity-50 cursor-not-allowed' : ''}
            `}
            onMouseEnter={() => setIsDragActive(true)}
            onMouseLeave={() => setIsDragActive(false)}
          >
            <input {...getInputProps()} />
            
            <div className="flex flex-col items-center space-y-4">
              <div className="p-3 bg-primary/10 rounded-full">
                <Upload className="h-8 w-8 text-primary" />
              </div>
              
              <div>
                <h3 className="text-lg font-semibold text-foreground">
                  Drop your lab report here
                </h3>
                <p className="text-sm text-muted-foreground mt-1">
                  or click to browse files
                </p>
              </div>
              
              <div className="flex items-center space-x-2 text-xs text-muted-foreground">
                <FileText className="h-4 w-4" />
                <span>PDF, TXT, JSON, CSV up to {Math.round(maxSize / 1024 / 1024)}MB</span>
              </div>
            </div>
          </div>
        ) : (
          <div className="space-y-4">
            {/* Selected File Display */}
            <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg border">
              <div className="flex items-center space-x-3">
                <div className="p-2 bg-blue-100 rounded">
                  <FileText className="h-5 w-5 text-blue-600" />
                </div>
                <div>
                  <p className="font-medium text-gray-900">{selectedFile.name}</p>
                  <p className="text-sm text-gray-500">{formatFileSize(selectedFile.size)}</p>
                </div>
              </div>
              <Button
                variant="ghost"
                size="sm"
                onClick={handleRemove}
                disabled={isParsing}
                className="text-gray-400 hover:text-gray-600"
              >
                <X className="h-4 w-4" />
              </Button>
            </div>

            {/* Action Buttons */}
            <div className="flex space-x-3">
              <Button
                onClick={handleParse}
                disabled={isParsing}
                className="flex-1"
              >
                {isParsing ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                    Parsing...
                  </>
                ) : (
                  <>
                    <Play className="h-4 w-4 mr-2" />
                    Parse File
                  </>
                )}
              </Button>
              <Button
                variant="outline"
                onClick={handleRemove}
                disabled={isParsing}
              >
                <X className="h-4 w-4 mr-2" />
                Remove
              </Button>
            </div>
          </div>
        )}
        
        {error && (
          <div className="mt-4 flex items-center space-x-2 text-destructive text-sm">
            <AlertCircle className="h-4 w-4" />
            <span>{error}</span>
          </div>
        )}
      </CardContent>
    </Card>
  )
}
