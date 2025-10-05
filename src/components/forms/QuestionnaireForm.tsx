'use client';

import React, { useState, useEffect } from 'react';
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

interface QuestionnaireQuestion {
  id: string;
  section: string;
  question: string;
  type: string;
  required: boolean;
  options?: string[];
  fields?: Array<{
    label: string;
    type: string;
    min?: number;
    max?: number;
  }>;
  alternativeUnit?: {
    label: string;
    type: string;
    min?: number;
    max?: number;
  };
  label?: string;
  min?: number;
  max?: number;
  helpText?: string;
  allowOther?: boolean;
  labels?: Record<string, string>;
  conditionalDisplay?: {
    dependsOn: string;
    showWhen: string[];
  };
}

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

  const questionsPerStep = 5; // Show 5 questions per step
  const totalSteps = Math.ceil(questions.length / questionsPerStep);

  useEffect(() => {
    loadQuestions();
  }, []);

  const loadQuestions = async () => {
    try {
      // In a real implementation, this would fetch from the backend
      // For now, we'll use a mock structure based on the questionnaire.json
      const mockQuestions: QuestionnaireQuestion[] = [
        {
          id: "full_name",
          section: "demographics",
          question: "Full Name",
          type: "text",
          required: true
        },
        {
          id: "email_address",
          section: "demographics",
          question: "Email Address",
          type: "email",
          required: true
        },
        {
          id: "phone_number",
          section: "demographics",
          question: "Phone Number",
          type: "phone",
          required: true
        },
        {
          id: "country",
          section: "demographics",
          question: "Country",
          type: "dropdown",
          options: ["United Kingdom", "United States", "Canada", "Australia", "Other"],
          required: true
        },
        {
          id: "state_province",
          section: "demographics",
          question: "State/Province",
          type: "text",
          required: false
        },
        {
          id: "date_of_birth",
          section: "demographics",
          question: "Date of Birth",
          type: "date",
          required: true
        },
        {
          id: "biological_sex",
          section: "demographics",
          question: "Biological Sex",
          type: "dropdown",
          options: ["Male", "Female", "Intersex"],
          required: true
        },
        {
          id: "height",
          section: "demographics",
          question: "Height",
          type: "group",
          fields: [
            { label: "Feet", type: "number", min: 3, max: 8 },
            { label: "Inches", type: "number", min: 0, max: 11 }
          ],
          alternativeUnit: {
            label: "Height (cm)",
            type: "number",
            min: 100,
            max: 250
          },
          required: true
        },
        {
          id: "weight",
          section: "demographics",
          question: "Weight",
          type: "number",
          label: "Weight (lbs)",
          alternativeUnit: {
            label: "Weight (kg)",
            type: "number",
            min: 30,
            max: 300
          },
          required: true
        },
        {
          id: "sleep_hours_nightly",
          section: "lifestyle",
          question: "How many hours of sleep do you typically get per night?",
          type: "dropdown",
          options: ["Less than 5 hours", "5-6 hours", "7-8 hours", "9+ hours"],
          required: true
        },
        {
          id: "sleep_quality_rating",
          section: "lifestyle",
          question: "Rate your sleep quality (1-10)",
          type: "slider",
          min: 1,
          max: 10,
          labels: {
            "1": "Wake up exhausted",
            "5": "Somewhat rested",
            "10": "Always refreshed"
          },
          required: true
        },
        {
          id: "alcohol_drinks_weekly",
          section: "lifestyle",
          question: "How many alcoholic drinks do you consume per week?",
          type: "dropdown",
          options: ["None", "1-3 drinks", "4-7 drinks", "8-14 drinks", "15+ drinks"],
          helpText: "1 drink = 12oz beer, 5oz wine, or 1.5oz spirits",
          required: true
        },
        {
          id: "tobacco_use",
          section: "lifestyle",
          question: "Do you currently use tobacco products?",
          type: "dropdown",
          options: ["Never used", "Former user quit >1 year", "Former user quit <1 year", "Occasional use", "Daily use"],
          required: true
        },
        {
          id: "stress_level_rating",
          section: "lifestyle",
          question: "Rate your average stress level (1-10)",
          type: "slider",
          min: 1,
          max: 10,
          labels: {
            "1": "Very low stress",
            "5": "Moderate stress",
            "10": "Overwhelming stress"
          },
          required: true
        },
        {
          id: "vigorous_exercise_days",
          section: "lifestyle",
          question: "How many days per week do you do vigorous exercise (20+ min)?",
          type: "dropdown",
          options: ["0 days", "1 day", "2 days", "3 days", "4+ days"],
          helpText: "Vigorous = hard breathing and sweating",
          required: true
        },
        {
          id: "current_medications",
          section: "medical_history",
          question: "Are you currently taking any prescription medications?",
          type: "dropdown",
          options: ["None", "1-2 medications", "3-5 medications", "6+ medications", "Prefer not to say"],
          required: true
        },
        {
          id: "long_term_medications",
          section: "medical_history",
          question: "Are you currently taking any of the following long-term medications?",
          type: "checkbox",
          options: ["None", "Corticosteroids", "Atypical antipsychotics", "HIV/AIDS treatments"],
          required: true,
          helpText: "These medications can affect cardiovascular risk assessment"
        },
        {
          id: "chronic_conditions",
          section: "medical_history",
          question: "Do you have any diagnosed chronic conditions?",
          type: "checkbox",
          options: ["None", "High blood pressure", "High cholesterol", "Diabetes Type 1", "Diabetes Type 2", "Heart disease", "Thyroid disorder", "Autoimmune condition", "Liver disease", "Kidney disease", "Other"],
          allowOther: true,
          required: true
        },
        {
          id: "medical_conditions",
          section: "medical_history",
          question: "Have you ever been diagnosed with any of the following medical conditions?",
          type: "checkbox",
          options: ["None", "Atrial fibrillation", "Rheumatoid arthritis", "Systemic lupus erythematosus (SLE)"],
          required: true,
          helpText: "These conditions can affect cardiovascular risk assessment"
        },
        {
          id: "current_symptoms",
          section: "symptoms",
          question: "Do you have any current symptoms affecting your daily life?",
          type: "checkbox",
          options: ["None", "Fatigue", "Brain fog", "Joint pain", "Digestive issues", "Sleep problems", "Mood changes", "Other"],
          allowOther: true,
          required: true
        },
        {
          id: "regular_migraines",
          section: "symptoms",
          question: "Do you suffer from regular migraines?",
          type: "dropdown",
          options: ["Yes", "No", "Not sure"],
          required: true,
          helpText: "Migraines can be associated with cardiovascular risk factors"
        }
      ];

      setQuestions(mockQuestions);
      setLoadingQuestions(false);
    } catch (error) {
      console.error('Failed to load questions:', error);
      setLoadingQuestions(false);
    }
  };

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
      if (question.required && (!responses[question.id] || responses[question.id] === '')) {
        newErrors[question.id] = 'This field is required';
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
                value={value || (question.min || 1)}
                onValueChange={(val) => handleResponseChange(question.id, val)}
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
                <span className="text-lg font-semibold">{value || (question.min || 1)}</span>
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

  const currentQuestions = getCurrentQuestions();
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
