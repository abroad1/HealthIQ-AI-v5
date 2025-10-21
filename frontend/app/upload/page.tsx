'use client';

import React, { useState, useEffect, useRef, useCallback } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Upload, FileText, Database, AlertCircle, CheckCircle, FileUp, Type } from 'lucide-react';
import BiomarkerForm from '@/components/forms/BiomarkerForm';
import QuestionnaireForm from '@/components/forms/QuestionnaireForm';
import FileDropzone from '../components/upload/FileDropzone';
import PasteInput from '../components/upload/PasteInput';
import ParsedTable from '../components/preview/ParsedTable';
import { useAnalysisStore } from '../state/analysisStore';
import { useUploadStore, useUploadStatus, useParsedData } from '../state/upload';
import { useParseUpload } from '../queries/parsing';
import { useRouter, useSearchParams } from 'next/navigation';

export default function UploadPage() {
  const [activeTab, setActiveTab] = useState('upload');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);
  const [submitSuccess, setSubmitSuccess] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  
  const { startAnalysis, isLoading: isAnalyzing, currentPhase, currentAnalysisId, error: analysisError } = useAnalysisStore();
  const router = useRouter();
  const searchParams = useSearchParams();
  const isFixtureMode = searchParams.get('fixture') === 'true';
  
  // Upload workflow state
  const uploadStatus = useUploadStatus();
  const parsedData = useParsedData();
  const { setParsedResults, updateBiomarker, confirmAll, setError, setStatus } = useUploadStore();

  // Helper function to handle parsed data from fixture
  const handleParsedData = useCallback((analysisData: any) => {
    if (!analysisData?.biomarkers) return;
    const analysisId = 'fixture-0001'; // fixture test ID
    const transformed = analysisData.biomarkers.map((b: any) => ({
      name: b.biomarker_name ?? b.name ?? b.id,
      value: b.value,
      unit: b.unit,
      status: b.status ?? 'parsed',
      referenceRange: b.reference_range,
    }));
    const metadata = {
      analysis_id: analysisId,
      timestamp: new Date().toISOString(),
      source_type: 'unknown' as const,
      source_name: 'test-fixture',
    };
    setParsedResults(transformed, analysisId, metadata);
    setStatus('ready');
    console.log(`✅ Fetched ${transformed.length} biomarkers from ${process.env.NEXT_PUBLIC_API_BASE || 'http://127.0.0.1:8000'}/api/analysis/fixture`);
  }, [setParsedResults, setStatus]);
  const parseUpload = useParseUpload();
  
  // Idempotent guard for handleConfirmAll
  const confirmAllOnceRef = useRef(false);

  // DEBUG: Log state changes
  useEffect(() => {
    console.log('🎯 Upload page state:', {
      uploadStatus,
      parsedDataLength: parsedData.length,
      shouldRenderTable: (uploadStatus === 'ready' || uploadStatus === 'confirmed') && parsedData.length > 0,
      parseSuccess: parseUpload.isSuccess,
      hasParseData: !!parseUpload.data
    });
  }, [uploadStatus, parsedData, parseUpload.isSuccess, parseUpload.data]);

  // Dual-path upload logic: fixture mode vs manual mode
  useEffect(() => {
    async function loadData() {
      try {
        // if (isFixtureMode) {
        //   console.log("📦 Fixture mode active — fetching static test data...");
        //   const data = await fetchFixtureAnalysis();
        //   handleParsedData(data);
        // } else {
          console.log("📤 Manual mode active — waiting for user input...");
          // Manual upload logic remains unchanged
        // }
      } catch (err) {
        console.error("❌ Fixture backend fetch failed:", err);
      }
    }

    loadData();
  }, [isFixtureMode, handleParsedData]);

  // Handle file upload parsing
  const handleFileUpload = async (file: File) => {
    setError(null);
    parseUpload.mutate({ file });
    setSelectedFile(null); // Clear after starting parse
  };

  // Handle text paste parsing
  const handleTextPaste = async (text: string) => {
    setError(null);
    parseUpload.mutate({ text });
  };

  // Handle biomarker edit in parsed table
  const handleBiomarkerEdit = (index: number, biomarker: any) => {
    updateBiomarker(index, biomarker);
  };

  // Handle confirm all biomarkers
  const handleConfirmAll = useCallback(() => {
    // Idempotent guard - prevent double execution
    if (confirmAllOnceRef.current) {
      console.warn("⚠️ handleConfirmAll already executed, ignoring duplicate call");
      return;
    }
    
    console.log("🧭 handleConfirmAll triggered. uploadStatus =", uploadStatus);
    console.log("🧭 parsedData length:", parsedData.length);
    
    // Mark as executed
    confirmAllOnceRef.current = true;
    
    // Mark biomarkers as confirmed
    confirmAll();
    
    // Transition to questionnaire step (DO NOT start analysis yet)
    setStatus('questionnaire');
    
    console.log("✅ Biomarkers confirmed — awaiting questionnaire");
  }, [uploadStatus, parsedData.length, confirmAll, setStatus]);

  // Handle questionnaire submission from Upload & Parse flow (AFTER biomarker confirmation)
  const handleQuestionnaireFromUpload = async (questionnaireData: any) => {
    console.log("📝 Questionnaire submitted with data:", questionnaireData);
    
    // Guard against duplicate analysis starts
    if (isAnalyzing) {
      console.warn('⚠️ Analysis already in progress, ignoring duplicate start.');
      return;
    }
    
    try {
      // Convert biomarkers array to object format
      const biomarkersObject: Record<string, any> = {};
      parsedData.forEach((biomarker) => {
        const key = biomarker.name.toLowerCase().replace(/\s+/g, '_');
        biomarkersObject[key] = {
          value: parseFloat(biomarker.value.toString()),
          unit: biomarker.unit,
          timestamp: new Date().toISOString()
        };
      });
      
      console.log("🚀 Preparing to start analysis with", parsedData.length, "biomarkers");
      console.log("🔍 Biomarkers object keys:", Object.keys(biomarkersObject));
      console.log("📋 Questionnaire data keys:", Object.keys(questionnaireData || {}));
      
      // Convert height object to number (if group field with Feet/Inches)
      let heightInCm = 180; // default
      if (questionnaireData?.height) {
        if (typeof questionnaireData.height === 'number') {
          heightInCm = questionnaireData.height;
        } else if (typeof questionnaireData.height === 'object') {
          // Handle group field: {Feet: 6, Inches: 2} OR {cm: 180}
          if ('cm' in questionnaireData.height) {
            heightInCm = parseFloat(questionnaireData.height.cm);
          } else if ('Feet' in questionnaireData.height || 'Inches' in questionnaireData.height) {
            const feet = parseFloat(questionnaireData.height.Feet || 0);
            const inches = parseFloat(questionnaireData.height.Inches || 0);
            heightInCm = (feet * 12 + inches) * 2.54; // Convert to cm
          }
        }
      }
      
      // Convert weight object to number (if group field with lbs/kg)
      let weightInKg = 75; // default
      if (questionnaireData?.weight) {
        if (typeof questionnaireData.weight === 'number') {
          weightInKg = questionnaireData.weight;
        } else if (typeof questionnaireData.weight === 'object') {
          // Handle group field: {lbs: 165} OR {kg: 75}
          if ('kg' in questionnaireData.weight) {
            weightInKg = parseFloat(questionnaireData.weight.kg);
          } else if ('lbs' in questionnaireData.weight) {
            weightInKg = parseFloat(questionnaireData.weight.lbs) * 0.453592; // Convert to kg
          }
        }
      }
      
      // Convert biological_sex to lowercase sex
      let sex: 'male' | 'female' | 'other' = 'male';
      if (questionnaireData?.biological_sex) {
        sex = questionnaireData.biological_sex.toLowerCase() as 'male' | 'female' | 'other';
      } else if (questionnaireData?.sex) {
        sex = questionnaireData.sex.toLowerCase() as 'male' | 'female' | 'other';
      }
      
      // Calculate age from date_of_birth if provided
      let age = 35; // default
      if (questionnaireData?.date_of_birth) {
        const dob = new Date(questionnaireData.date_of_birth);
        const today = new Date();
        age = today.getFullYear() - dob.getFullYear();
        const monthDiff = today.getMonth() - dob.getMonth();
        if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < dob.getDate())) {
          age--;
        }
      } else if (questionnaireData?.age) {
        age = parseFloat(questionnaireData.age);
      }
      
      console.log("🔄 Converted user data:", { age, sex, height: heightInCm, weight: weightInKg });
      
      // Prepare analysis payload WITH questionnaire data
      const payload = {
        biomarkers: biomarkersObject,
        user: {
          user_id: questionnaireData?.user_id || "5029514b-f7fd-4dff-8d60-4fb8b7f90dd4",
          age: age,
          sex: sex,
          height: heightInCm,
          weight: weightInKg
        },
        questionnaire: questionnaireData  // ✅ GOOD - Include questionnaire data
      };
      
      console.log("📦 Analysis payload prepared:", payload);
      console.log("🔍 Biomarkers validation check:", Object.keys(payload.biomarkers));
      console.log("🔍 User validation check:", payload.user);
      console.log("🎬 Calling startAnalysis()...");
      
      await startAnalysis(payload);
      
      // Check if validation failed silently in store
      const storeState = useAnalysisStore.getState();
      if (storeState.error) {
        console.error("❌ startAnalysis validation error:", storeState.error);
        setError({
          code: storeState.error.code,
          message: storeState.error.message
        });
        return;  // Don't proceed to confirmed state
      }
      
      console.log("✅ startAnalysis() resolved successfully");
      
      // Mark as confirmed
      setStatus('confirmed');
      
      console.log("⏳ Waiting for analysis to complete via SSE...");
      console.log("🔔 Will navigate when phase === 'completed'");
      
      // Navigation will happen automatically via useEffect watching currentPhase
    } catch (error) {
      console.error("❌ Analysis failed:", error);
      setError({ 
        code: 'ANALYSIS_START_FAILED', 
        message: error instanceof Error ? error.message : 'Failed to start analysis'
      });
    }
  };

  // Auto-navigate when analysis completes
  useEffect(() => {
    console.log("🔔 Phase changed to:", currentPhase);
    
    if (currentPhase === 'completed' && uploadStatus === 'confirmed' && currentAnalysisId) {
      console.log("✅ Analysis completed! Navigating to results...");
      console.log("📍 Analysis ID:", currentAnalysisId);
      
      setTimeout(() => {
        console.log("➡️ Navigating to results for", currentAnalysisId);
        console.log("🔀 Executing router.push(\"/results\")");
        router.push(`/results?analysis_id=${currentAnalysisId}`);
      }, 500);
    }
  }, [currentPhase, uploadStatus, currentAnalysisId, router]);

  // Handle parse upload success/error
  useEffect(() => {
    if (parseUpload.isSuccess && parseUpload.data) {
      console.log('📥 Parse upload success! Raw data:', parseUpload.data);
      const { parsed_data } = parseUpload.data;
      console.log('📊 Extracted parsed_data:', parsed_data);
      console.log('🧬 Biomarkers array:', parsed_data.biomarkers, 'Length:', parsed_data.biomarkers?.length);
      
      // Transform biomarkers to include referenceRange object
      const transformed = parsed_data.biomarkers.map((b: any) => ({
        name: b.name ?? b.id ?? b.biomarker_name,
        value: b.value,
        unit: b.unit,
        status: 'raw' as const,
        referenceRange: (b.ref_low != null && b.ref_high != null)
          ? { min: Number(b.ref_low), max: Number(b.ref_high), unit: b.unit }
          : (b.referenceRange && typeof b.referenceRange === 'object')
            ? b.referenceRange
            : undefined,
      }));

      setParsedResults(transformed, parseUpload.data.analysis_id, parsed_data.metadata);
    } else if (parseUpload.isError && parseUpload.error) {
      console.error('❌ Parse upload error:', parseUpload.error);
      setError({
        code: 'PARSE_ERROR',
        message: parseUpload.error.message || 'Failed to parse upload'
      });
    }
  }, [parseUpload.isSuccess, parseUpload.isError, parseUpload.data, parseUpload.error, setParsedResults, setError]);

  // LEGACY HANDLERS REMOVED - These were causing duplicate EventSource connections
  // All analysis should now go through handleQuestionnaireFromUpload only
  // 
  // const handleBiomarkerSubmit = async (biomarkerData: any) => { ... }
  // const handleQuestionnaireSubmit = async (questionnaireData: any) => { ... }
  // const handleCombinedSubmit = async (data: { biomarkers: any; questionnaire: any }) => { ... }

  if (submitSuccess) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <Card className="w-full max-w-md">
          <CardContent className="pt-6">
            <div className="text-center">
              <CheckCircle className="h-16 w-16 text-green-500 mx-auto mb-4" />
              <h2 className="text-2xl font-bold text-gray-900 mb-2">Analysis Started!</h2>
              <p className="text-gray-600 mb-4">
                Your health analysis is being processed. You&apos;ll be redirected to your results shortly.
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

        {analysisError && (
          <Alert className="mb-6 border-red-200 bg-red-50">
            <AlertCircle className="h-4 w-4 text-red-600" />
            <AlertDescription className="text-red-800">
              <strong>Analysis Error:</strong> {analysisError.message || 'Validation failed'}
              {analysisError.details && (
                <details className="mt-2">
                  <summary className="cursor-pointer text-sm font-semibold">View Details</summary>
                  <pre className="mt-2 text-xs bg-white p-2 rounded overflow-auto">{JSON.stringify(analysisError.details, null, 2)}</pre>
                </details>
              )}
            </AlertDescription>
          </Alert>
        )}

        <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
          <TabsList className="grid w-full grid-cols-4 mb-8">
            <TabsTrigger value="upload" className="flex items-center gap-2">
              <FileUp className="h-4 w-4" />
              Upload & Parse
            </TabsTrigger>
            <TabsTrigger value="biomarkers" className="flex items-center gap-2">
              <Database className="h-4 w-4" />
              Manual Entry
            </TabsTrigger>
            <TabsTrigger value="questionnaire" className="flex items-center gap-2">
              <FileText className="h-4 w-4" />
              Questionnaire
            </TabsTrigger>
            <TabsTrigger value="combined" className="flex items-center gap-2">
              <Upload className="h-4 w-4" />
              Combined
            </TabsTrigger>
          </TabsList>

          <TabsContent value="upload">
            <div className="space-y-6">
              {/* Upload Methods */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div>
                  <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                    <FileUp className="h-5 w-5" />
                    Upload Lab Report
                  </h3>
                  <FileDropzone
                    onFileSelect={setSelectedFile}
                    onError={(error) => setError({ code: 'UPLOAD_ERROR', message: error })}
                    disabled={parseUpload.isLoading}
                  />
                  
                  {/* File Preview Section */}
                  {selectedFile && !parseUpload.isLoading && (
                    <div className="mt-4 p-4 border rounded-lg bg-gray-50">
                      <div className="flex items-center justify-between mb-4">
                        <div>
                          <p className="font-medium">{selectedFile.name}</p>
                          <p className="text-sm text-gray-500">
                            {(selectedFile.size / 1024).toFixed(2)} KB
                          </p>
                        </div>
                      </div>
                      
                      <div className="flex gap-3">
                        <Button
                          onClick={() => handleFileUpload(selectedFile)}
                          className="flex-1"
                        >
                          <FileText className="h-4 w-4 mr-2" />
                          Parse Document
                        </Button>
                        
                        <Button
                          onClick={() => setSelectedFile(null)}
                          variant="outline"
                        >
                          Remove File
                        </Button>
                      </div>
                    </div>
                  )}
                </div>
                
                <div>
                  <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                    <Type className="h-5 w-5" />
                    Paste Lab Results
                  </h3>
                  <PasteInput
                    onTextSubmit={handleTextPaste}
                    onError={(error) => setError({ code: 'PASTE_ERROR', message: error })}
                    disabled={parseUpload.isLoading}
                  />
                </div>
              </div>

              {/* Parsing Status */}
              {parseUpload.isLoading && (
                <Card>
                  <CardContent className="p-6 text-center">
                    <div className="flex items-center justify-center space-x-3">
                      <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600"></div>
                      <span className="text-lg font-medium">Parsing your lab results...</span>
                    </div>
                  </CardContent>
                </Card>
              )}

              {/* Parsed Results */}
              {uploadStatus === 'ready' && parsedData.length > 0 && (
                <div>
                  <h3 className="text-lg font-semibold mb-4">Review Parsed Results</h3>
                  <ParsedTable
                    biomarkers={parsedData}
                    onBiomarkerEdit={handleBiomarkerEdit}
                    onConfirmAll={handleConfirmAll}
                    isLoading={isSubmitting}
                    error={submitError}
                  />
                </div>
              )}

              {/* Error Display */}
              {(parseUpload.isError || submitError) && (
                <Alert className="border-red-200 bg-red-50">
                  <AlertCircle className="h-4 w-4 text-red-600" />
                  <AlertDescription className="text-red-800">
                    {parseUpload.error?.message || submitError}
                  </AlertDescription>
                </Alert>
              )}

              {/* Questionnaire Stage - shown after biomarker confirmation */}
              {uploadStatus === 'questionnaire' && parsedData.length > 0 && (
                <div className="space-y-6 mt-6">
                  {/* Confirmation Success Message */}
                  <Card className="border-green-200 bg-green-50">
                    <CardContent className="pt-6">
                      <div className="flex items-center gap-3">
                        <CheckCircle className="h-5 w-5 text-green-600" />
                        <div>
                          <h3 className="font-semibold text-green-900">
                            Biomarkers Confirmed ({parsedData.length})
                          </h3>
                          <p className="text-sm text-green-700 mt-1">
                            Please complete the health questionnaire below to start your analysis.
                          </p>
                        </div>
                      </div>
                    </CardContent>
                  </Card>

                  {/* Questionnaire Form */}
                  <Card>
                    <CardHeader>
                      <CardTitle className="flex items-center gap-2">
                        <FileText className="h-5 w-5" />
                        Health Assessment Questionnaire
                      </CardTitle>
                      <CardDescription>
                        Complete this questionnaire to provide context for your biomarker analysis.
                      </CardDescription>
                    </CardHeader>
                    <CardContent>
                      <QuestionnaireForm
                        onSubmit={handleQuestionnaireFromUpload}
                        isLoading={isSubmitting || isAnalyzing}
                      />
                    </CardContent>
                  </Card>
                </div>
              )}
            </div>
          </TabsContent>

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
                  onSubmit={() => {
                    console.warn('⚠️ BiomarkerForm tab is deprecated. Please use the Upload & Parse flow instead.');
                    alert('This tab is deprecated. Please use the "Upload & Parse" tab for biomarker analysis.');
                  }}
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
                  onSubmit={() => {
                    console.warn('⚠️ QuestionnaireForm tab is deprecated. Please use the Upload & Parse flow instead.');
                    alert('This tab is deprecated. Please use the "Upload & Parse" tab for questionnaire analysis.');
                  }}
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
                  onSubmit={() => {
                    console.warn('⚠️ CombinedAnalysisForm tab is deprecated. Please use the Upload & Parse flow instead.');
                    alert('This tab is deprecated. Please use the "Upload & Parse" tab for combined analysis.');
                  }}
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
      {/* Deprecation Notice */}
      <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
        <div className="flex items-center">
          <AlertCircle className="h-5 w-5 text-yellow-600 mr-2" />
          <div>
            <h3 className="text-sm font-medium text-yellow-800">This tab is deprecated</h3>
            <p className="text-sm text-yellow-700 mt-1">
              Please use the "Upload & Parse" tab for biomarker analysis. This provides the same functionality with improved workflow.
            </p>
          </div>
        </div>
      </div>
      
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