'use client'

import { useState, useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import { Button } from '../ui/button'
import { Card, CardContent } from '../ui/card'
import { Upload, FileText, AlertCircle, X, File } from 'lucide-react'

interface FileDropzoneProps {
  onFileSelect: (file: File) => void
  onFileRemove?: () => void
  onFileParse?: (file: File) => void
  onError?: (error: string) => void
  maxSize?: number // in bytes
  acceptedTypes?: string[]
  disabled?: boolean
}

export default function FileDropzone({
  onFileSelect,
  onFileRemove,
  onFileParse,
  onError,
  maxSize = 10 * 1024 * 1024, // 10MB default
  acceptedTypes = ['.pdf', '.txt', '.json', '.csv'],
  disabled = false
}: FileDropzoneProps) {
  const [isDragActive, setIsDragActive] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [selectedFile, setSelectedFile] = useState<File | null>(null)

  const onDrop = useCallback((acceptedFiles: File[]) => {
    const file = acceptedFiles[0]
    if (file) {
      setError(null)
      setSelectedFile(file)
      console.log('FileDropzone: Accepted file:', {
        name: file.name,
        type: file.type,
        size: file.size
      })
      onFileSelect(file)
    }
  }, [onFileSelect])

  const handleRemoveFile = useCallback(() => {
    setSelectedFile(null)
    onFileRemove?.()
  }, [onFileRemove])

  const handleParseFile = useCallback(() => {
    if (selectedFile) {
      onFileParse?.(selectedFile)
    }
  }, [selectedFile, onFileParse])

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
    disabled
  })

  return (
    <Card className="w-full">
      <CardContent className="p-6">
        <div
          {...getRootProps()}
          className={`
            border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors
            ${isDragActive ? 'border-primary bg-primary/5' : 'border-border hover:border-primary/50'}
            ${isDragReject ? 'border-destructive bg-destructive/5' : ''}
            ${disabled ? 'opacity-50 cursor-not-allowed' : ''}
          `}
          onMouseEnter={() => setIsDragActive(true)}
          onMouseLeave={() => setIsDragActive(false)}
        >
          <input 
            {...getInputProps()} 
            id="file-upload"
            name="file"
            autoComplete="off"
          />
          
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
        
        {error && (
          <div className="mt-4 flex items-center space-x-2 text-destructive text-sm">
            <AlertCircle className="h-4 w-4" />
            <span>{error}</span>
          </div>
        )}

        {/* File Preview Section */}
        {selectedFile && (
          <div className="mt-4 p-4 border border-border rounded-lg bg-muted/50">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <div className="p-2 bg-primary/10 rounded-full">
                  <File className="h-5 w-5 text-primary" />
                </div>
                <div>
                  <p className="font-medium text-foreground">{selectedFile.name}</p>
                  <p className="text-sm text-muted-foreground">
                    {selectedFile.type} • {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                  </p>
                </div>
              </div>
              <div className="flex items-center space-x-2">
                {selectedFile.type === 'application/pdf' && (
                  <Button
                    onClick={handleParseFile}
                    size="sm"
                    className="bg-primary hover:bg-primary/90"
                  >
                    Parse
                  </Button>
                )}
                <Button
                  onClick={handleRemoveFile}
                  variant="outline"
                  size="sm"
                  className="text-destructive hover:text-destructive hover:bg-destructive/10"
                >
                  <X className="h-4 w-4 mr-1" />
                  Remove
                </Button>
              </div>
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  )
}
