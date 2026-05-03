'use client';

import React, { useState, useEffect, useRef, useCallback } from 'react';
import { Card, CardContent } from '@/components/ui/card';
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
import Link from 'next/link';
import { emitWedgeEvent } from '@/lib/wedgeAnalytics';
import {
  analysisBiomarkerKey,
  buildReferenceRangeFromParserRow,
  numericPartForAnalysisPayload,
  rangeAttentionLevel,
  referenceRangeToPayload,
} from '@/lib/uploadReferenceRange';
import type { BiomarkerValue } from '@/types/analysis';
import type { ParsedBiomarker } from '@/types/parsed';

type AnalysisBiomarkerEntry = BiomarkerValue & {
  reference_range?: NonNullable<ReturnType<typeof referenceRangeToPayload>>;
};

function isRecord(v: unknown): v is Record<string, unknown> {
  return v !== null && typeof v === 'object' && !Array.isArray(v);
}

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

  const handleBiomarkerEdit = (index: number, biomarker: ParsedBiomarker) => {
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

  const handleQuestionnaireFromUpload = async (questionnaireData: Record<string, unknown>) => {
    if (isAnalyzing) {
      return;
    }

    try {
      const biomarkersObject: Record<string, AnalysisBiomarkerEntry> = {};
      for (const biomarker of parsedData) {
        const key = analysisBiomarkerKey(biomarker.name);
        const numericValue = numericPartForAnalysisPayload(biomarker.value);
        if (!Number.isFinite(numericValue)) {
          setSubmitError(
            `Cannot start analysis: biomarker "${biomarker.name}" has a value that is not a usable number. Edit the value in review (e.g. clear any stray text).`
          );
          return;
        }
        biomarkersObject[key] = {
          value: numericValue,
          unit: biomarker.unit,
          timestamp: new Date().toISOString(),
          reference_range: referenceRangeToPayload(biomarker.referenceRange),
        };
      }

      let heightInCm = 180;
      const h = questionnaireData.height;
      if (h !== undefined) {
        if (typeof h === 'number') {
          heightInCm = h;
        } else if (isRecord(h)) {
          if ('cm' in h && (typeof h.cm === 'string' || typeof h.cm === 'number')) {
            heightInCm = parseFloat(String(h.cm));
          } else if ('Feet' in h || 'Inches' in h) {
            const feet = parseFloat(String(h.Feet ?? 0));
            const inches = parseFloat(String(h.Inches ?? 0));
            heightInCm = (feet * 12 + inches) * 2.54;
          }
        }
      }

      let weightInKg = 75;
      const w = questionnaireData.weight;
      if (w !== undefined) {
        if (typeof w === 'number') {
          weightInKg = w;
        } else if (isRecord(w)) {
          if ('kg' in w && (typeof w.kg === 'string' || typeof w.kg === 'number')) {
            weightInKg = parseFloat(String(w.kg));
          } else if ('lbs' in w && (typeof w.lbs === 'string' || typeof w.lbs === 'number')) {
            weightInKg = parseFloat(String(w.lbs)) * 0.453592;
          }
        }
      }

      let sex: 'male' | 'female' | 'other' = 'male';
      const bio = questionnaireData.biological_sex;
      if (typeof bio === 'string') {
        const s = bio.toLowerCase();
        if (s === 'male' || s === 'female' || s === 'other') sex = s;
      } else {
        const sx = questionnaireData.sex;
        if (typeof sx === 'string') {
          const t = sx.toLowerCase();
          if (t === 'male' || t === 'female' || t === 'other') sex = t;
        }
      }

      let age = 35;
      const dobRaw = questionnaireData.date_of_birth;
      if (typeof dobRaw === 'string' || dobRaw instanceof Date) {
        const dob = new Date(dobRaw);
        const today = new Date();
        age = today.getFullYear() - dob.getFullYear();
        const monthDiff = today.getMonth() - dob.getMonth();
        if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < dob.getDate())) {
          age--;
        }
      } else if (questionnaireData.age !== undefined) {
        age = parseFloat(String(questionnaireData.age));
      }

      const uidRaw = questionnaireData.user_id;
      const resolvedUserId =
        (typeof uidRaw === 'string' && uidRaw.trim() ? uidRaw.trim() : null) || sessionUser?.id;
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
      const transformed = parsed_data.biomarkers.map((b: ParsedBiomarker) => {
        const row = b as unknown as Record<string, unknown>;
        const {
          referenceRange,
          referenceText,
          contextRangeOptions,
          referenceType,
          labelledBands,
          matchedLabelledBand,
        } = buildReferenceRangeFromParserRow(row);
        const v = b.value;
        const bExt = b as ParsedBiomarker & { id?: string; biomarker_name?: string };
        return {
          name: String(bExt.name ?? bExt.id ?? bExt.biomarker_name ?? ''),
          value: (typeof v === 'number' || typeof v === 'string' ? v : Number(v)) as number | string,
          unit: String(b.unit ?? ''),
          status: 'raw' as const,
          referenceRange,
          referenceText,
          ...(contextRangeOptions?.length ? { contextRangeOptions } : {}),
          ...(referenceType ? { referenceType } : {}),
          ...(labelledBands?.length ? { labelledBands } : {}),
          ...(matchedLabelledBand ? { matchedLabelledBand } : {}),
        };
      });

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
          <Alert
            className={
              analysisError.code === 'UPGRADE_REQUIRED'
                ? 'mb-6 border-amber-200 bg-amber-50'
                : 'mb-6 border-red-200 bg-red-50'
            }
          >
            <AlertCircle
              className={
                analysisError.code === 'UPGRADE_REQUIRED' ? 'h-4 w-4 text-amber-700' : 'h-4 w-4 text-red-600'
              }
            />
            <AlertDescription
              className={analysisError.code === 'UPGRADE_REQUIRED' ? 'text-amber-950' : 'text-red-800'}
            >
              {analysisError.code === 'UPGRADE_REQUIRED' ? (
                <>
                  <strong>Subscription required.</strong>{' '}
                  {analysisError.message || 'Subscribe to run further analyses. Your past results stay available.'}{' '}
                  <Link href="/pricing" className="font-semibold underline underline-offset-4">
                    View pricing
                  </Link>
                  .
                </>
              ) : (
                <>
                  <strong>Could not start analysis:</strong> {analysisError.message || 'Validation failed'}
                </>
              )}
              {analysisError.details && analysisError.code !== 'UPGRADE_REQUIRED' ? (
                <details className="mt-2">
                  <summary className="cursor-pointer text-sm font-semibold">Technical details</summary>
                  <pre className="mt-2 text-xs bg-white p-2 rounded overflow-auto max-h-40">
                    {JSON.stringify(analysisError.details, null, 2)}
                  </pre>
                </details>
              ) : null}
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
              {parsedData.some((b) => {
                if (!b.unit?.trim()) return true;
                const att = rangeAttentionLevel({
                  unit: b.unit,
                  referenceRange: b.referenceRange,
                  referenceText: b.referenceText,
                  contextRangeOptions: b.contextRangeOptions,
                  referenceType: b.referenceType,
                  matchedLabelledBand: b.matchedLabelledBand,
                });
                if (
                  att === 'none' ||
                  att === 'one-sided' ||
                  att === 'no-lab-range-supplied' ||
                  att === 'labelled-bands-resolved'
                ) {
                  return false;
                }
                return true;
              }) && (
                <Alert className="mb-4 border-amber-200 bg-amber-50">
                  <AlertCircle className="h-4 w-4 text-amber-800" />
                  <AlertDescription className="text-amber-950">
                    Some markers are missing a unit, need you to choose which lab reference band applies (multiple
                    contextual ranges), or need review for reference text. Edit those rows before analysis so
                    lab-interval context is complete where your report provides it.
                  </AlertDescription>
                </Alert>
              )}
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

              <div className="overflow-hidden rounded-2xl border border-border/60 bg-background shadow-[0_40px_100px_-48px_rgba(0,0,0,0.35)] ring-1 ring-primary/[0.07]">
                <QuestionnaireForm
                  onSubmit={handleQuestionnaireFromUpload}
                  isLoading={isAnalyzing}
                />
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
