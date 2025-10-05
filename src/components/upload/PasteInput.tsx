'use client'

import { useState } from 'react'
import { Button } from '../ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card'
import { Textarea } from '../ui/textarea'
import { Copy, AlertCircle } from 'lucide-react'

interface PasteInputProps {
  onTextSubmit: (text: string) => void
  onError?: (error: string) => void
  disabled?: boolean
  placeholder?: string
}

export default function PasteInput({
  onTextSubmit,
  onError,
  disabled = false,
  placeholder = "Paste your lab results here...\n\nExample:\nTotal Cholesterol: 180 mg/dL\nHDL Cholesterol: 45 mg/dL\nLDL Cholesterol: 110 mg/dL\nTriglycerides: 125 mg/dL"
}: PasteInputProps) {
  const [text, setText] = useState('')
  const [error, setError] = useState<string | null>(null)

  const handleSubmit = () => {
    const trimmedText = text.trim()
    
    if (!trimmedText) {
      const errorMsg = 'Please paste some lab results text before submitting'
      setError(errorMsg)
      onError?.(errorMsg)
      return
    }

    if (trimmedText.length < 10) {
      const errorMsg = 'Text appears too short. Please paste more detailed lab results'
      setError(errorMsg)
      onError?.(errorMsg)
      return
    }

    setError(null)
    onTextSubmit(trimmedText)
  }

  const handleClear = () => {
    setText('')
    setError(null)
  }

  const handlePaste = async () => {
    try {
      const clipboardText = await navigator.clipboard.readText()
      setText(clipboardText)
      setError(null)
    } catch (err) {
      const errorMsg = 'Unable to access clipboard. Please paste manually'
      setError(errorMsg)
      onError?.(errorMsg)
    }
  }

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle className="flex items-center space-x-2">
          <Copy className="h-5 w-5" />
          <span>Paste Lab Results</span>
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="space-y-2">
          <Textarea
            value={text}
            onChange={(e) => {
              setText(e.target.value)
              setError(null)
            }}
            placeholder={placeholder}
            disabled={disabled}
            className="min-h-[200px] resize-none"
          />
          
          <div className="flex justify-between items-center text-xs text-muted-foreground">
            <span>{text.length} characters</span>
            <span>Minimum 10 characters required</span>
          </div>
        </div>

        {error && (
          <div className="flex items-center space-x-2 text-destructive text-sm">
            <AlertCircle className="h-4 w-4" />
            <span>{error}</span>
          </div>
        )}

        <div className="flex space-x-2">
          <Button
            onClick={handleSubmit}
            disabled={disabled || !text.trim()}
            className="flex-1"
          >
            Parse Lab Results
          </Button>
          
          <Button
            onClick={handlePaste}
            variant="outline"
            disabled={disabled}
          >
            Paste from Clipboard
          </Button>
          
          <Button
            onClick={handleClear}
            variant="outline"
            disabled={disabled || !text}
          >
            Clear
          </Button>
        </div>
      </CardContent>
    </Card>
  )
}
