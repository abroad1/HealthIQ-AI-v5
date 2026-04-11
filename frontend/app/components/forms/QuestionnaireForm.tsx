'use client';

import React, { useState, useEffect, useCallback } from 'react';
import { Button } from '../ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card';
import { Input } from '../ui/input';
import { Label } from '../ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../ui/select';
import { Slider } from '../ui/slider';
import { Checkbox } from '../ui/checkbox';
import { Textarea } from '../ui/textarea';
import { Progress } from '../ui/progress';
import { Alert, AlertDescription } from '../ui/alert';
import { Loader2, CheckCircle, AlertCircle } from 'lucide-react';
import {
  fetchQuestionnaireSchema,
  type QuestionnaireQuestion,
} from '@/lib/questionnaireSchema';

interface QuestionnaireFormProps {
  onSubmit: (responses: Record<string, any>) => void;
  onCancel?: () => void;
  initialData?: Record<string, any>;
  isLoading?: boolean;
}

export default function QuestionnaireForm({ 
  onSubmit, 
  onCancel, 
  initialData = {}, 
  isLoading = false 
}: QuestionnaireFormProps) {
  const [questions, setQuestions] = useState<QuestionnaireQuestion[]>([]);
  const [responses, setResponses] = useState<Record<string, any>>(initialData);
  const [currentStep, setCurrentStep] = useState(0);
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [loadingQuestions, setLoadingQuestions] = useState(true);
  const [schemaLoadError, setSchemaLoadError] = useState<string | null>(null);

  const questionsPerStep = 5; // Show 5 questions per step
  const totalSteps = Math.max(1, Math.ceil(questions.length / questionsPerStep));

  const loadQuestions = useCallback(async () => {
    setSchemaLoadError(null);
    setLoadingQuestions(true);
    try {
      const schema = await fetchQuestionnaireSchema();
      setQuestions(schema);
    } catch (error) {
      const message =
        error instanceof Error ? error.message : 'Failed to load questionnaire schema';
      console.error('Questionnaire schema load failed:', error);
      setSchemaLoadError(message);
      setQuestions([]);
    } finally {
      setLoadingQuestions(false);
    }
  }, []);

  useEffect(() => {
    loadQuestions();
  }, [loadQuestions]);

  /** Dev/test only: `?autofill=true` loads sample answers from `@/lib/mock/questionnaire` (not the question list). */
  useEffect(() => {
    if (typeof window !== 'undefined' && window.location.search.includes('autofill=true')) {
      void import('@/lib/mock/questionnaire').then((m) => {
        setResponses(m.default);
        console.log('🧪 Questionnaire responses auto-filled (mock answers only)');
      });
    }
  }, []);

  const getCurrentQuestions = () => {
    const start = currentStep * questionsPerStep;
    const end = start + questionsPerStep;
    return questions.slice(start, end);
  };

  const getQuestionsBySection = () => {
    const groupedQuestions = questions.reduce((acc, question) => {
      if (!acc[question.section]) {
        acc[question.section] = [];
      }
      acc[question.section].push(question);
      return acc;
    }, {} as Record<string, QuestionnaireQuestion[]>);
    
    return groupedQuestions;
  };

  const handleResponseChange = (questionId: string, value: any) => {
    setResponses(prev => ({
      ...prev,
      [questionId]: value
    }));
    
    // Clear error for this question
    if (errors[questionId]) {
      setErrors(prev => {
        const newErrors = { ...prev };
        delete newErrors[questionId];
        return newErrors;
      });
    }
  };

  const validateStep = () => {
    const currentQuestions = getCurrentQuestions();
    const newErrors: Record<string, string> = {};

    currentQuestions.forEach(question => {
      const value = responses[question.id];
      
      // Required field validation
      if (question.required && (!value || value === '')) {
        newErrors[question.id] = 'This field is required';
        return;
      }
      
      // Email format validation
      if (question.type === 'email' && value) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(value)) {
          newErrors[question.id] = 'Please enter a valid email address';
        }
      }
      
      // Phone format validation
      if (question.type === 'phone' && value) {
        const phoneRegex = /^[\d\s()+-]{6,}$/;
        if (!phoneRegex.test(value)) {
          newErrors[question.id] = 'Please enter a valid phone number';
        }
      }
      
      // Number validation
      if (question.type === 'number' && value) {
        if (isNaN(parseFloat(value))) {
          newErrors[question.id] = 'Please enter a valid number';
        }
      }
    });

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleNext = () => {
    if (validateStep()) {
      setCurrentStep(prev => Math.min(prev + 1, totalSteps - 1));
    }
  };

  const handlePrevious = () => {
    setCurrentStep(prev => Math.max(prev - 1, 0));
  };

  const handleSubmit = async () => {
    if (!validateStep()) {
      return;
    }

    setIsSubmitting(true);
    try {
      await onSubmit(responses);
    } catch (error) {
      console.error('Failed to submit questionnaire:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  const renderQuestion = (question: QuestionnaireQuestion) => {
    const value = responses[question.id];
    const error = errors[question.id];

    switch (question.type) {
      case 'text':
      case 'email':
      case 'phone':
      case 'date':
        return (
          <div key={question.id} className="space-y-2">
            <Label htmlFor={question.id} className="text-sm font-medium">
              {question.question}
              {question.required && <span className="text-red-500 ml-1">*</span>}
            </Label>
            <Input
              id={question.id}
              type={question.type}
              value={value || ''}
              onChange={(e) => handleResponseChange(question.id, e.target.value)}
              className={error ? 'border-red-500' : ''}
            />
            {question.helpText && (
              <p className="text-xs text-gray-500">{question.helpText}</p>
            )}
            {error && (
              <p className="text-xs text-red-500">{error}</p>
            )}
          </div>
        );

      case 'number':
        return (
          <div key={question.id} className="space-y-2">
            <Label htmlFor={question.id} className="text-sm font-medium">
              {question.question}
              {question.required && <span className="text-red-500 ml-1">*</span>}
            </Label>
            <Input
              id={question.id}
              type="number"
              min={question.min}
              max={question.max}
              value={value || ''}
              onChange={(e) => handleResponseChange(question.id, parseFloat(e.target.value))}
              className={error ? 'border-red-500' : ''}
            />
            {question.helpText && (
              <p className="text-xs text-gray-500">{question.helpText}</p>
            )}
            {error && (
              <p className="text-xs text-red-500">{error}</p>
            )}
          </div>
        );

      case 'dropdown':
        return (
          <div key={question.id} className="space-y-2">
            <Label htmlFor={question.id} className="text-sm font-medium">
              {question.question}
              {question.required && <span className="text-red-500 ml-1">*</span>}
            </Label>
            <Select
              value={value || ''}
              onValueChange={(val) => handleResponseChange(question.id, val)}
            >
              <SelectTrigger className={error ? 'border-red-500' : ''}>
                <SelectValue placeholder="Select an option" />
              </SelectTrigger>
              <SelectContent>
                {question.options?.map((option) => (
                  <SelectItem key={option} value={option}>
                    {option}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
            {question.helpText && (
              <p className="text-xs text-gray-500">{question.helpText}</p>
            )}
            {error && (
              <p className="text-xs text-red-500">{error}</p>
            )}
          </div>
        );

      case 'slider':
        // Ensure slider always has a defined value (prevent uncontrolled → controlled warning)
        const defaultSliderValue = Math.floor(((question.min || 1) + (question.max || 10)) / 2);
        const sliderValue = Array.isArray(value) ? value[0] : (value ?? defaultSliderValue);
        
        return (
          <div key={question.id} className="space-y-2">
            <Label htmlFor={question.id} className="text-sm font-medium">
              {question.question}
              {question.required && <span className="text-red-500 ml-1">*</span>}
            </Label>
            <div className="px-3">
              <Slider
                min={question.min || 1}
                max={question.max || 10}
                step={1}
                value={[sliderValue]}
                onValueChange={(val) => handleResponseChange(question.id, val[0])}
                className="w-full"
              />
              <div className="flex justify-between text-xs text-gray-500 mt-1">
                {question.labels && (
                  <>
                    <span>{question.labels[String(question.min || 1)]}</span>
                    <span>{question.labels[String(question.max || 10)]}</span>
                  </>
                )}
              </div>
              <div className="text-center mt-2">
                <span className="text-lg font-semibold">{sliderValue}</span>
              </div>
            </div>
            {question.helpText && (
              <p className="text-xs text-gray-500">{question.helpText}</p>
            )}
            {error && (
              <p className="text-xs text-red-500">{error}</p>
            )}
          </div>
        );

      case 'checkbox':
        return (
          <div key={question.id} className="space-y-2">
            <Label className="text-sm font-medium">
              {question.question}
              {question.required && <span className="text-red-500 ml-1">*</span>}
            </Label>
            <div className="space-y-2">
              {question.options?.map((option) => (
                <div key={option} className="flex items-center space-x-2">
                  <Checkbox
                    id={`${question.id}-${option}`}
                    checked={Array.isArray(value) && value.includes(option)}
                    onCheckedChange={(checked) => {
                      const currentValues = Array.isArray(value) ? value : [];
                      if (checked) {
                        handleResponseChange(question.id, [...currentValues, option]);
                      } else {
                        handleResponseChange(question.id, currentValues.filter(v => v !== option));
                      }
                    }}
                  />
                  <Label htmlFor={`${question.id}-${option}`} className="text-sm">
                    {option}
                  </Label>
                </div>
              ))}
            </div>
            {question.helpText && (
              <p className="text-xs text-gray-500">{question.helpText}</p>
            )}
            {error && (
              <p className="text-xs text-red-500">{error}</p>
            )}
          </div>
        );

      case 'group':
        return (
          <div key={question.id} className="space-y-2">
            <Label className="text-sm font-medium">
              {question.question}
              {question.required && <span className="text-red-500 ml-1">*</span>}
            </Label>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {question.fields?.map((field) => (
                <div key={field.label} className="space-y-1">
                  <Label htmlFor={`${question.id}-${field.label}`} className="text-xs">
                    {field.label}
                  </Label>
                  <Input
                    id={`${question.id}-${field.label}`}
                    type={field.type}
                    min={field.min}
                    max={field.max}
                    value={value?.[field.label] || ''}
                    onChange={(e) => {
                      const newValue = {
                        ...value,
                        [field.label]: field.type === 'number' ? parseFloat(e.target.value) : e.target.value
                      };
                      handleResponseChange(question.id, newValue);
                    }}
                  />
                </div>
              ))}
            </div>
            {question.helpText && (
              <p className="text-xs text-gray-500">{question.helpText}</p>
            )}
            {error && (
              <p className="text-xs text-red-500">{error}</p>
            )}
          </div>
        );

      default:
        return (
          <div key={question.id} className="space-y-2">
            <Label htmlFor={question.id} className="text-sm font-medium">
              {question.question}
              {question.required && <span className="text-red-500 ml-1">*</span>}
            </Label>
            <Textarea
              id={question.id}
              value={value || ''}
              onChange={(e) => handleResponseChange(question.id, e.target.value)}
              className={error ? 'border-red-500' : ''}
            />
            {question.helpText && (
              <p className="text-xs text-gray-500">{question.helpText}</p>
            )}
            {error && (
              <p className="text-xs text-red-500">{error}</p>
            )}
          </div>
        );
    }
  };

  if (loadingQuestions) {
    return (
      <div className="flex items-center justify-center p-8">
        <Loader2 className="h-8 w-8 animate-spin" />
        <span className="ml-2">Loading questionnaire...</span>
      </div>
    );
  }

  if (schemaLoadError) {
    return (
      <div className="max-w-4xl mx-auto p-6 space-y-4">
        <Alert className="border-red-200 bg-red-50">
          <AlertCircle className="h-4 w-4 text-red-600" />
          <AlertDescription className="text-red-800">
            <strong>Could not load questionnaire.</strong> {schemaLoadError}
          </AlertDescription>
        </Alert>
        <Button type="button" onClick={() => void loadQuestions()} variant="outline">
          Retry
        </Button>
      </div>
    );
  }

  if (questions.length === 0) {
    return (
      <div className="max-w-4xl mx-auto p-6">
        <Alert>
          <AlertDescription>No questionnaire questions were returned from the server.</AlertDescription>
        </Alert>
      </div>
    );
  }

  const progress = ((currentStep + 1) / totalSteps) * 100;

  return (
    <div className="max-w-4xl mx-auto p-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <CheckCircle className="h-5 w-5 text-green-500" />
            Health Assessment Questionnaire
          </CardTitle>
          <CardDescription>
            Please complete all required fields to get personalized health insights.
            Step {currentStep + 1} of {totalSteps}
          </CardDescription>
          <Progress value={progress} className="w-full" />
        </CardHeader>
        <CardContent className="space-y-6">
          {Object.entries(getQuestionsBySection()).map(([sectionName, sectionQuestions]) => (
            <div key={sectionName} className="space-y-4">
              <h3 className="text-lg font-semibold text-gray-900 capitalize">
                {sectionName.replace(/_/g, ' ')}
              </h3>
              <div className="space-y-4 pl-4">
                {sectionQuestions.map(renderQuestion)}
              </div>
            </div>
          ))}
          
          <div className="flex justify-between pt-6">
            <Button
              variant="outline"
              onClick={currentStep === 0 ? onCancel : handlePrevious}
              disabled={isSubmitting}
            >
              {currentStep === 0 ? 'Cancel' : 'Previous'}
            </Button>
            
            <div className="flex gap-2">
              {currentStep < totalSteps - 1 ? (
                <Button onClick={handleNext} disabled={isSubmitting}>
                  Next
                </Button>
              ) : (
                <Button 
                  onClick={handleSubmit} 
                  disabled={isSubmitting}
                  className="bg-green-600 hover:bg-green-700"
                >
                  {isSubmitting ? (
                    <>
                      <Loader2 className="h-4 w-4 animate-spin mr-2" />
                      Submitting...
                    </>
                  ) : (
                    'Complete Assessment'
                  )}
                </Button>
              )}
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
