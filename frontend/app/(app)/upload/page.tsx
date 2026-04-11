'use client';

import React, { useState, useEffect, useRef, useCallback } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { AlertCircle, CheckCircle, FileUp, FileText, Type } from 'lucide-react';
import QuestionnaireForm from '@/components/forms/QuestionnaireForm';
import FileDropzone from '@/components/upload/FileDropzone';
import PasteInput from '@/components/upload/PasteInput';
import ParsedTable from '@/components/preview/ParsedTable';
import { useAnalysisStore } from '@/state/analysisStore';
import { useUploadStore, useUploadStatus, useParsedData } from '@/state/upload';
import { useParseUpload } from '@/queries/parsing';
import { useAnalysisResult } from '@/queries/analysisResult';
import { useAuthStore } from '@/state/authStore';
import { useRouter } from 'next/navigation';
import { emitWedgeEvent } from '@/lib/wedgeAnalytics';

export default function UploadPage() {
  const [submitError, setSubmitError] = useState<string | null>(null);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  const { startAnalysis, isLoading: isAnalyzing, currentPhase, currentAnalysisId, error: analysisError } =
    useAnalysisStore();
  const sessionUser = useAuthStore((s) => s.user);
  const router = useRouter();

  useAnalysisResult(currentPhase === 'completed' && currentAnalysisId ? currentAnalysisId : null);

  const uploadStatus = useUploadStatus();
  const parsedData = useParsedData();
  const { setParsedResults, updateBiomarker, confirmAll, setError, setStatus } = useUploadStore();

  const parseUpload = useParseUpload();

  const confirmAllOnceRef = useRef(false);
  const parseCompleteEmittedFor = useRef<string | null>(null);

  const handleFileUpload = async (file: File) => {
    setError(null);
    emitWedgeEvent({
      event_name: 'wedge_upload_started',
      timestamp: new Date().toISOString(),
      route: '/upload',
      source: 'file',
    });
    parseUpload.mutate({ file });
    setSelectedFile(null);
  };

  const handleTextPaste = async (text: string) => {
    setError(null);
    emitWedgeEvent({
      event_name: 'wedge_upload_started',
      timestamp: new Date().toISOString(),
      route: '/upload',
      source: 'paste',
    });
    parseUpload.mutate({ text });
  };

  const handleBiomarkerEdit = (index: number, biomarker: any) => {
    updateBiomarker(index, biomarker);
  };

  const handleConfirmAll = useCallback(() => {
    if (confirmAllOnceRef.current) {
      return;
    }
    confirmAllOnceRef.current = true;
    confirmAll();
    setStatus('questionnaire');
  }, [confirmAll, setStatus]);

  const handleQuestionnaireFromUpload = async (questionnaireData: any) => {
    if (isAnalyzing) {
      return;
    }

    try {
      const biomarkersObject: Record<string, any> = {};
      parsedData.forEach((biomarker) => {
        const key = biomarker.name.toLowerCase().replace(/\s+/g, '_');
        biomarkersObject[key] = {
          value: parseFloat(biomarker.value.toString()),
          unit: biomarker.unit,
          timestamp: new Date().toISOString(),
          reference_range: biomarker.referenceRange
            ? {
                min: biomarker.referenceRange.min,
                max: biomarker.referenceRange.max,
                unit: biomarker.referenceRange.unit,
                source: 'lab',
              }
            : null,
        };
      });

      let heightInCm = 180;
      if (questionnaireData?.height) {
        if (typeof questionnaireData.height === 'number') {
          heightInCm = questionnaireData.height;
        } else if (typeof questionnaireData.height === 'object') {
          if ('cm' in questionnaireData.height) {
            heightInCm = parseFloat(questionnaireData.height.cm);
          } else if ('Feet' in questionnaireData.height || 'Inches' in questionnaireData.height) {
            const feet = parseFloat(questionnaireData.height.Feet || 0);
            const inches = parseFloat(questionnaireData.height.Inches || 0);
            heightInCm = (feet * 12 + inches) * 2.54;
          }
        }
      }

      let weightInKg = 75;
      if (questionnaireData?.weight) {
        if (typeof questionnaireData.weight === 'number') {
          weightInKg = questionnaireData.weight;
        } else if (typeof questionnaireData.weight === 'object') {
          if ('kg' in questionnaireData.weight) {
            weightInKg = parseFloat(questionnaireData.weight.kg);
          } else if ('lbs' in questionnaireData.weight) {
            weightInKg = parseFloat(questionnaireData.weight.lbs) * 0.453592;
          }
        }
      }

      let sex: 'male' | 'female' | 'other' = 'male';
      if (questionnaireData?.biological_sex) {
        sex = questionnaireData.biological_sex.toLowerCase() as 'male' | 'female' | 'other';
      } else if (questionnaireData?.sex) {
        sex = questionnaireData.sex.toLowerCase() as 'male' | 'female' | 'other';
      }

      let age = 35;
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

      const resolvedUserId =
        (typeof questionnaireData?.user_id === 'string' && questionnaireData.user_id.trim()
          ? questionnaireData.user_id.trim()
          : null) || sessionUser?.id;
      if (!resolvedUserId) {
        setSubmitError(
          'Your signed-in account could not be resolved. Please sign out and sign in again before starting an analysis.'
        );
        return;
      }

      const payload = {
        biomarkers: biomarkersObject,
        user: {
          user_id: resolvedUserId,
          chronological_age: age,
          sex: sex,
          height_cm: heightInCm,
          weight_kg: weightInKg,
        },
        questionnaire_data: questionnaireData,
      };

      emitWedgeEvent({
        event_name: 'wedge_questionnaire_submitted',
        timestamp: new Date().toISOString(),
        route: '/upload',
      });

      await startAnalysis(payload);

      const storeState = useAnalysisStore.getState();
      if (storeState.error) {
        setError({
          code: storeState.error.code,
          message: storeState.error.message,
        });
        return;
      }

      setStatus('confirmed');
    } catch (error) {
      setError({
        code: 'ANALYSIS_START_FAILED',
        message: error instanceof Error ? error.message : 'Failed to start analysis',
      });
    }
  };

  useEffect(() => {
    if (currentPhase === 'completed' && uploadStatus === 'confirmed' && currentAnalysisId) {
      const t = setTimeout(() => {
        router.push(`/results?analysis_id=${currentAnalysisId}`);
      }, 500);
      return () => clearTimeout(t);
    }
  }, [currentPhase, uploadStatus, currentAnalysisId, router]);

  useEffect(() => {
    if (parseUpload.isSuccess && parseUpload.data) {
      const aid = parseUpload.data.analysis_id as string | undefined;
      if (aid && parseCompleteEmittedFor.current !== aid) {
        parseCompleteEmittedFor.current = aid;
        emitWedgeEvent({
          event_name: 'wedge_upload_parse_completed',
          timestamp: new Date().toISOString(),
          route: '/upload',
          analysis_id: aid,
        });
      }
      const { parsed_data } = parseUpload.data;
      const transformed = parsed_data.biomarkers.map((b: any) => ({
        name: b.name ?? b.id ?? b.biomarker_name,
        value: b.value,
        unit: b.unit,
        status: 'raw' as const,
        referenceRange:
          b.ref_low != null && b.ref_high != null
            ? { min: Number(b.ref_low), max: Number(b.ref_high), unit: b.unit }
            : b.referenceRange && typeof b.referenceRange === 'object'
              ? b.referenceRange
              : undefined,
      }));

      confirmAllOnceRef.current = false;
      setParsedResults(transformed, parseUpload.data.analysis_id, parsed_data.metadata);
    } else if (parseUpload.isError && parseUpload.error) {
      emitWedgeEvent({
        event_name: 'wedge_upload_parse_failed',
        timestamp: new Date().toISOString(),
        route: '/upload',
        error_class: 'parse_error',
      });
      setError({
        code: 'PARSE_ERROR',
        message: parseUpload.error.message || 'Failed to parse upload',
      });
    }
  }, [parseUpload.isSuccess, parseUpload.isError, parseUpload.data, parseUpload.error, setParsedResults, setError]);

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="container mx-auto px-4 max-w-6xl">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">Upload lab results</h1>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Parse a lab file or paste results, confirm your markers, then add health context. We run a structured
            metabolic analysis — not a quick generic summary.
          </p>
        </div>

        {submitError && (
          <Alert className="mb-6 border-red-200 bg-red-50">
            <AlertCircle className="h-4 w-4 text-red-600" />
            <AlertDescription className="text-red-800">{submitError}</AlertDescription>
          </Alert>
        )}

        {analysisError && (
          <Alert className="mb-6 border-red-200 bg-red-50">
            <AlertCircle className="h-4 w-4 text-red-600" />
            <AlertDescription className="text-red-800">
              <strong>Could not start analysis:</strong> {analysisError.message || 'Validation failed'}
              {analysisError.details && (
                <details className="mt-2">
                  <summary className="cursor-pointer text-sm font-semibold">Technical details</summary>
                  <pre className="mt-2 text-xs bg-white p-2 rounded overflow-auto max-h-40">
                    {JSON.stringify(analysisError.details, null, 2)}
                  </pre>
                </details>
              )}
            </AlertDescription>
          </Alert>
        )}

        <div className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div>
              <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                <FileUp className="h-5 w-5" />
                Upload lab report
              </h3>
              <FileDropzone
                onFileSelect={setSelectedFile}
                onError={(error) => setError({ code: 'UPLOAD_ERROR', message: error })}
                disabled={parseUpload.isLoading}
              />

              {selectedFile && !parseUpload.isLoading && (
                <div className="mt-4 p-4 border rounded-lg bg-gray-50">
                  <div className="flex items-center justify-between mb-4">
                    <div>
                      <p className="font-medium">{selectedFile.name}</p>
                      <p className="text-sm text-gray-500">{(selectedFile.size / 1024).toFixed(2)} KB</p>
                    </div>
                  </div>

                  <div className="flex gap-3">
                    <Button onClick={() => handleFileUpload(selectedFile)} className="flex-1">
                      <FileText className="h-4 w-4 mr-2" />
                      Parse document
                    </Button>

                    <Button onClick={() => setSelectedFile(null)} variant="outline">
                      Remove file
                    </Button>
                  </div>
                </div>
              )}
            </div>

            <div>
              <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                <Type className="h-5 w-5" />
                Paste lab results
              </h3>
              <PasteInput
                onTextSubmit={handleTextPaste}
                onError={(error) => setError({ code: 'PASTE_ERROR', message: error })}
                disabled={parseUpload.isLoading}
              />
            </div>
          </div>

          {parseUpload.isLoading && (
            <Card>
              <CardContent className="p-6 text-center">
                <div className="flex items-center justify-center space-x-3">
                  <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600"></div>
                  <span className="text-lg font-medium">Reading your lab results…</span>
                </div>
              </CardContent>
            </Card>
          )}

          {uploadStatus === 'ready' && parsedData.length > 0 && (
            <div>
              <h3 className="text-lg font-semibold mb-4">Review parsed markers</h3>
              <ParsedTable
                biomarkers={parsedData}
                onBiomarkerEdit={handleBiomarkerEdit}
                onConfirmAll={handleConfirmAll}
                isLoading={false}
                error={submitError}
              />
            </div>
          )}

          {(parseUpload.isError || submitError) && (
            <Alert className="border-red-200 bg-red-50">
              <AlertCircle className="h-4 w-4 text-red-600" />
              <AlertDescription className="text-red-800">
                {parseUpload.error?.message || submitError}
              </AlertDescription>
            </Alert>
          )}

          {uploadStatus === 'questionnaire' && parsedData.length > 0 && (
            <div className="space-y-6 mt-6">
              <Card className="border-green-200 bg-green-50">
                <CardContent className="pt-6">
                  <div className="flex items-center gap-3">
                    <CheckCircle className="h-5 w-5 text-green-600" />
                    <div>
                      <h3 className="font-semibold text-green-900">Markers confirmed ({parsedData.length})</h3>
                      <p className="text-sm text-green-700 mt-1">
                        Complete the short health questionnaire so your results can use the right context.
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <FileText className="h-5 w-5" />
                    Health questionnaire
                  </CardTitle>
                  <CardDescription>
                    Context for interpretation (age, sex, lifestyle) — used with your lab values, not for generic
                    advice alone.
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <QuestionnaireForm
                    onSubmit={handleQuestionnaireFromUpload}
                    isLoading={isAnalyzing}
                  />
                </CardContent>
              </Card>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
