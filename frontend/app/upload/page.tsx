'use client';

import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Upload, FileText, Database, AlertCircle, CheckCircle } from 'lucide-react';
import BiomarkerForm from '@/components/forms/BiomarkerForm';
import QuestionnaireForm from '@/components/forms/QuestionnaireForm';
import { useAnalysisStore } from '../state/analysisStore';
import { useRouter } from 'next/navigation';

export default function UploadPage() {
  const [activeTab, setActiveTab] = useState('biomarkers');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);
  const [submitSuccess, setSubmitSuccess] = useState(false);
  
  const { startAnalysis, isLoading: isAnalyzing } = useAnalysisStore();
  const router = useRouter();

  const handleBiomarkerSubmit = async (biomarkerData: any) => {
    setIsSubmitting(true);
    setSubmitError(null);
    
    try {
      // Start analysis with biomarker data
      await startAnalysis({
        biomarkers: biomarkerData,
        user: {
          age: 35,
          sex: 'male' as const,
          height: 180,
          weight: 75
        },
        questionnaire: null
      });
      
      setSubmitSuccess(true);
      // Redirect to results page after a short delay
      setTimeout(() => {
        router.push('/results');
      }, 2000);
    } catch (error) {
      console.error('Analysis failed:', error);
      setSubmitError('Failed to start analysis. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleQuestionnaireSubmit = async (questionnaireData: any) => {
    setIsSubmitting(true);
    setSubmitError(null);
    
    try {
      // Start analysis with questionnaire data
      await startAnalysis({
        biomarkers: {},
        user: {
          age: 35,
          sex: 'male' as const,
          height: 180,
          weight: 75
        },
        questionnaire: questionnaireData
      });
      
      setSubmitSuccess(true);
      // Redirect to results page after a short delay
      setTimeout(() => {
        router.push('/results');
      }, 2000);
    } catch (error) {
      console.error('Analysis failed:', error);
      setSubmitError('Failed to start analysis. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleCombinedSubmit = async (data: { biomarkers: any; questionnaire: any }) => {
    setIsSubmitting(true);
    setSubmitError(null);
    
    try {
      // Start analysis with both biomarker and questionnaire data
      await startAnalysis({
        biomarkers: data.biomarkers,
        user: {
          age: 35,
          sex: 'male' as const,
          height: 180,
          weight: 75
        },
        questionnaire: data.questionnaire
      });
      
      setSubmitSuccess(true);
      // Redirect to results page after a short delay
      setTimeout(() => {
        router.push('/results');
      }, 2000);
    } catch (error) {
      console.error('Analysis failed:', error);
      setSubmitError('Failed to start analysis. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  if (submitSuccess) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <Card className="w-full max-w-md">
          <CardContent className="pt-6">
            <div className="text-center">
              <CheckCircle className="h-16 w-16 text-green-500 mx-auto mb-4" />
              <h2 className="text-2xl font-bold text-gray-900 mb-2">Analysis Started!</h2>
              <p className="text-gray-600 mb-4">
                Your health analysis is being processed. You'll be redirected to your results shortly.
              </p>
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-green-500 mx-auto"></div>
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="container mx-auto px-4 max-w-6xl">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Health Analysis Upload
          </h1>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Upload your biomarker data or complete our health questionnaire to get personalized AI-powered health insights.
          </p>
        </div>

        {submitError && (
          <Alert className="mb-6 border-red-200 bg-red-50">
            <AlertCircle className="h-4 w-4 text-red-600" />
            <AlertDescription className="text-red-800">
              {submitError}
            </AlertDescription>
          </Alert>
        )}

        <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
          <TabsList className="grid w-full grid-cols-3 mb-8">
            <TabsTrigger value="biomarkers" className="flex items-center gap-2">
              <Database className="h-4 w-4" />
              Biomarker Data
            </TabsTrigger>
            <TabsTrigger value="questionnaire" className="flex items-center gap-2">
              <FileText className="h-4 w-4" />
              Health Questionnaire
            </TabsTrigger>
            <TabsTrigger value="combined" className="flex items-center gap-2">
              <Upload className="h-4 w-4" />
              Combined Analysis
            </TabsTrigger>
          </TabsList>

          <TabsContent value="biomarkers">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Database className="h-5 w-5" />
                  Biomarker Data Entry
                </CardTitle>
                <CardDescription>
                  Enter your biomarker values manually or upload a CSV file. We support all major biomarkers including metabolic, cardiovascular, and inflammatory markers.
                </CardDescription>
              </CardHeader>
              <CardContent>
                <BiomarkerForm
                  onSubmit={handleBiomarkerSubmit}
                  isLoading={isSubmitting || isAnalyzing}
                />
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="questionnaire">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <FileText className="h-5 w-5" />
                  Health Assessment Questionnaire
                </CardTitle>
                <CardDescription>
                  Complete our comprehensive 58-question health assessment to get personalized insights based on your lifestyle, medical history, and health patterns.
                </CardDescription>
              </CardHeader>
              <CardContent>
                <QuestionnaireForm
                  onSubmit={handleQuestionnaireSubmit}
                  isLoading={isSubmitting || isAnalyzing}
                />
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="combined">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Upload className="h-5 w-5" />
                  Combined Analysis
                </CardTitle>
                <CardDescription>
                  For the most comprehensive analysis, provide both biomarker data and complete the health questionnaire. This gives our AI the most complete picture of your health.
                </CardDescription>
              </CardHeader>
              <CardContent>
                <CombinedAnalysisForm
                  onSubmit={handleCombinedSubmit}
                  isLoading={isSubmitting || isAnalyzing}
                />
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
}

// Combined Analysis Form Component
function CombinedAnalysisForm({ 
  onSubmit, 
  isLoading 
}: { 
  onSubmit: (data: { biomarkers: any; questionnaire: any }) => void;
  isLoading: boolean;
}) {
  const [biomarkerData, setBiomarkerData] = useState<any>(null);
  const [questionnaireData, setQuestionnaireData] = useState<any>(null);
  const [currentStep, setCurrentStep] = useState<'biomarkers' | 'questionnaire' | 'review'>('biomarkers');

  const handleBiomarkerSubmit = (data: any) => {
    setBiomarkerData(data);
    setCurrentStep('questionnaire');
  };

  const handleQuestionnaireSubmit = (data: any) => {
    setQuestionnaireData(data);
    setCurrentStep('review');
  };

  const handleFinalSubmit = () => {
    if (biomarkerData && questionnaireData) {
      onSubmit({ biomarkers: biomarkerData, questionnaire: questionnaireData });
    }
  };

  const canProceed = () => {
    switch (currentStep) {
      case 'biomarkers':
        return biomarkerData !== null;
      case 'questionnaire':
        return questionnaireData !== null;
      case 'review':
        return biomarkerData !== null && questionnaireData !== null;
      default:
        return false;
    }
  };

  return (
    <div className="space-y-6">
      {/* Progress Indicator */}
      <div className="flex items-center justify-center space-x-4">
        <div className={`flex items-center ${currentStep === 'biomarkers' ? 'text-blue-600' : biomarkerData ? 'text-green-600' : 'text-gray-400'}`}>
          <div className={`w-8 h-8 rounded-full flex items-center justify-center ${currentStep === 'biomarkers' ? 'bg-blue-100' : biomarkerData ? 'bg-green-100' : 'bg-gray-100'}`}>
            {biomarkerData ? <CheckCircle className="h-4 w-4" /> : '1'}
          </div>
          <span className="ml-2 text-sm font-medium">Biomarkers</span>
        </div>
        <div className="w-8 h-0.5 bg-gray-200"></div>
        <div className={`flex items-center ${currentStep === 'questionnaire' ? 'text-blue-600' : questionnaireData ? 'text-green-600' : 'text-gray-400'}`}>
          <div className={`w-8 h-8 rounded-full flex items-center justify-center ${currentStep === 'questionnaire' ? 'bg-blue-100' : questionnaireData ? 'bg-green-100' : 'bg-gray-100'}`}>
            {questionnaireData ? <CheckCircle className="h-4 w-4" /> : '2'}
          </div>
          <span className="ml-2 text-sm font-medium">Questionnaire</span>
        </div>
        <div className="w-8 h-0.5 bg-gray-200"></div>
        <div className={`flex items-center ${currentStep === 'review' ? 'text-blue-600' : 'text-gray-400'}`}>
          <div className={`w-8 h-8 rounded-full flex items-center justify-center ${currentStep === 'review' ? 'bg-blue-100' : 'bg-gray-100'}`}>
            3
          </div>
          <span className="ml-2 text-sm font-medium">Review</span>
        </div>
      </div>

      {/* Step Content */}
      {currentStep === 'biomarkers' && (
        <div>
          <h3 className="text-lg font-semibold mb-4">Step 1: Enter Biomarker Data</h3>
          <BiomarkerForm
            onSubmit={handleBiomarkerSubmit}
            isLoading={isLoading}
            showSubmitButton={true}
          />
        </div>
      )}

      {currentStep === 'questionnaire' && (
        <div>
          <h3 className="text-lg font-semibold mb-4">Step 2: Complete Health Questionnaire</h3>
          <QuestionnaireForm
            onSubmit={handleQuestionnaireSubmit}
            isLoading={isLoading}
          />
        </div>
      )}

      {currentStep === 'review' && (
        <div>
          <h3 className="text-lg font-semibold mb-4">Step 3: Review and Submit</h3>
          <div className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle className="text-base">Biomarker Data</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-gray-600">
                  {Object.keys(biomarkerData || {}).length} biomarkers entered
                </p>
              </CardContent>
            </Card>
            
            <Card>
              <CardHeader>
                <CardTitle className="text-base">Questionnaire Data</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-gray-600">
                  Health questionnaire completed
                </p>
              </CardContent>
            </Card>

            <div className="flex justify-between pt-4">
              <Button
                variant="outline"
                onClick={() => setCurrentStep('questionnaire')}
                disabled={isLoading}
              >
                Back to Questionnaire
              </Button>
              <Button
                onClick={handleFinalSubmit}
                disabled={isLoading || !canProceed()}
                className="bg-green-600 hover:bg-green-700"
              >
                {isLoading ? 'Starting Analysis...' : 'Start Combined Analysis'}
              </Button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
