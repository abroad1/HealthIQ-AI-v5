'use client';

import React, { useEffect, useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import {
  BarChart3,
  TrendingUp,
  AlertCircle,
  CheckCircle,
  RefreshCw,
  Download,
  Share2,
  Eye,
  EyeOff,
} from 'lucide-react';
import { useAnalysisStore } from '../state/analysisStore';
import { useClusterStore } from '../state/clusterStore';
import { InsightsPanel } from '@/components/insights/InsightsPanel';
import { InsightPanel } from '@/components/insights/InsightPanel';
import BiomarkerDials from '@/components/biomarkers/BiomarkerDials';
import ClusterSummary from '@/components/clusters/ClusterSummary';
import ClinicianReportRenderer from '@/components/results/ClinicianReportRenderer';
import PipelineStatus from '@/components/pipeline/PipelineStatus';
import { useRouter, useSearchParams } from 'next/navigation';
import { useAnalysisResult } from '../queries/analysisResult';

export default function ResultsPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const analysisIdFromUrl = searchParams.get('analysis_id');

  const currentAnalysis = useAnalysisStore((state) => state.currentAnalysis);
  const currentAnalysisId = useAnalysisStore((state) => state.currentAnalysisId);
  const isAnalyzing = useAnalysisStore((state) => state.isLoading);
  const analysisError = useAnalysisStore((state) => state.error);
  const retryAnalysis = useAnalysisStore((state) => state.retryAnalysis);
  const clearAnalysis = useAnalysisStore((state) => state.clearAnalysis);
  const setCurrentAnalysisId = useAnalysisStore((state) => state.setCurrentAnalysisId);

  const {
    clusters: clusterStoreClusters,
    isLoading: clustersLoading,
    loadClusters,
  } = useClusterStore();

  const [activeDetailTab, setActiveDetailTab] = useState('overview');
  const [showDetails, setShowDetails] = useState(false);

  const idToFetch = currentAnalysisId || analysisIdFromUrl;
  const { isLoading: isResultLoading } = useAnalysisResult(idToFetch || null);
  const isFetchingFromUrl = !!idToFetch && isResultLoading;

  const insights = currentAnalysis?.insights ?? [];
  const biomarkers = currentAnalysis?.biomarkers ?? [];
  const clusters = currentAnalysis?.clusters ?? [];
  const clinicianReport = currentAnalysis?.clinician_report_v1;
  const { created_at, completed_at } = currentAnalysis || {};

  useEffect(() => {
    if (analysisIdFromUrl && analysisIdFromUrl !== currentAnalysisId) {
      setCurrentAnalysisId(analysisIdFromUrl);
    }
  }, [analysisIdFromUrl, currentAnalysisId, setCurrentAnalysisId]);

  useEffect(() => {
    if (!currentAnalysis && !isAnalyzing && !analysisIdFromUrl && !isFetchingFromUrl) {
      router.push('/upload');
      return;
    }

    if (currentAnalysis && !clusterStoreClusters.length && !clustersLoading) {
      loadClusters(currentAnalysis.analysis_id);
    }
  }, [
    currentAnalysis,
    isAnalyzing,
    clusterStoreClusters.length,
    clustersLoading,
    loadClusters,
    router,
    analysisIdFromUrl,
    isFetchingFromUrl,
  ]);

  const handleRetry = () => {
    if (currentAnalysis) {
      retryAnalysis();
    }
  };

  const handleNewAnalysis = () => {
    clearAnalysis();
    router.push('/upload');
  };

  const handleExportResults = () => {
    if (!currentAnalysis) return;

    const dataStr = JSON.stringify(currentAnalysis, null, 2);
    const dataUri = 'data:application/json;charset=utf-8,' + encodeURIComponent(dataStr);

    const exportFileDefaultName = `healthiq-analysis-${new Date().toISOString().split('T')[0]}.json`;

    const linkElement = document.createElement('a');
    linkElement.setAttribute('href', dataUri);
    linkElement.setAttribute('download', exportFileDefaultName);
    linkElement.click();
  };

  const handleShareResults = () => {
    if (navigator.share && currentAnalysis) {
      navigator.share({
        title: 'HealthIQ Analysis Results',
        text: 'Check out my health analysis results from HealthIQ AI',
        url: window.location.href,
      });
    } else {
      navigator.clipboard.writeText(window.location.href);
    }
  };

  if (isAnalyzing || isFetchingFromUrl) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <Card className="w-full max-w-md">
          <CardContent className="pt-6">
            <div className="text-center">
              <RefreshCw className="h-16 w-16 text-blue-500 mx-auto mb-4 animate-spin" />
              <h2 className="text-2xl font-bold text-gray-900 mb-2">
                {isFetchingFromUrl ? 'Loading Your Results' : 'Analyzing Your Data'}
              </h2>
              <p className="text-gray-600 mb-4">
                {isFetchingFromUrl
                  ? 'Fetching your analysis results from the server...'
                  : 'Our AI is processing your biomarker data and generating personalized insights. This may take a few moments.'}
              </p>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div className="bg-blue-600 h-2 rounded-full animate-pulse" style={{ width: '60%' }}></div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  if (analysisError) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <Card className="w-full max-w-md">
          <CardContent className="pt-6">
            <div className="text-center">
              <AlertCircle className="h-16 w-16 text-red-500 mx-auto mb-4" />
              <h2 className="text-2xl font-bold text-gray-900 mb-2">Analysis Failed</h2>
              <p className="text-gray-600 mb-4">{analysisError?.message || 'An unknown error occurred'}</p>
              <div className="space-y-2">
                <Button onClick={handleRetry} className="w-full">
                  <RefreshCw className="h-4 w-4 mr-2" />
                  Try Again
                </Button>
                <Button onClick={handleNewAnalysis} variant="outline" className="w-full">
                  Start New Analysis
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  if (!currentAnalysis) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <Card className="w-full max-w-md">
          <CardContent className="pt-6">
            <div className="text-center">
              <AlertCircle className="h-16 w-16 text-gray-400 mx-auto mb-4" />
              <h2 className="text-2xl font-bold text-gray-900 mb-2">No Analysis Found</h2>
              <p className="text-gray-600 mb-4">Please complete an analysis first.</p>
              <Button onClick={handleNewAnalysis} className="w-full">
                Start New Analysis
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  const biomarkerDialData: Record<string, {
    value: number;
    unit: string;
    status?: string;
    score?: number;
    interpretation?: string;
    referenceRange?: {
      min?: number;
      max?: number;
      unit: string;
      source?: string;
    };
    date?: string;
  }> = {};

  biomarkers
    .filter((b) => b.biomarker_name && b.value != null && typeof b.value === 'number')
    .forEach((biomarker) => {
      biomarkerDialData[biomarker.biomarker_name] = {
        value: biomarker.value as number,
        unit: biomarker.unit,
        status: biomarker.status ?? undefined,
        score: biomarker.score ?? undefined,
        interpretation: biomarker.interpretation ?? undefined,
        referenceRange: biomarker.reference_range
          ? {
              min: biomarker.reference_range.min ?? undefined,
              max: biomarker.reference_range.max ?? undefined,
              unit: biomarker.reference_range.unit,
              source: biomarker.reference_range.source ?? undefined,
            }
          : undefined,
        date: created_at,
      };
    });

  const clusterSummaries = clusters.map((cluster, idx) => ({
    id: String(cluster.cluster_id || cluster.id || `cluster-${idx}`),
    name: cluster.name?.trim() ? cluster.name : 'Health pattern',
    category: cluster.category || 'other',
    score: typeof cluster.score === 'number' ? cluster.score : cluster.confidence ? cluster.confidence * 100 : 0,
    confidence: typeof cluster.confidence === 'number' ? cluster.confidence : 0.85,
    biomarkers: cluster.biomarkers || cluster.biomarkers_involved || [],
    description: cluster.description || cluster.summary || '',
    recommendations: cluster.recommendations || [],
    severity: (() => {
      const sev = cluster.severity;
      if (sev === 'normal' || sev === 'mild' || sev === 'low') return 'low' as const;
      if (sev === 'medium' || sev === 'moderate') return 'moderate' as const;
      if (sev === 'high') return 'high' as const;
      if (sev === 'critical') return 'critical' as const;
      return 'moderate' as const;
    })(),
    trend: 'stable' as const,
  }));

  const overallPercent =
    currentAnalysis.overall_score != null && currentAnalysis.overall_score <= 1
      ? Math.round(currentAnalysis.overall_score * 100)
      : currentAnalysis.overall_score != null
        ? Math.round(currentAnalysis.overall_score)
        : null;

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="container mx-auto px-4 max-w-6xl">
        <div className="mb-8">
          <div className="flex flex-col gap-4 md:flex-row md:items-start md:justify-between mb-4">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-1">Your results</h1>
              <p className="text-gray-600 max-w-2xl">
                Interpretation first, then how your body systems cluster, then marker-level detail. Deeper structured
                reporting stays available below.
              </p>
            </div>
            <div className="flex flex-wrap items-center gap-2">
              <Button variant="outline" size="sm" onClick={() => setShowDetails(!showDetails)}>
                {showDetails ? <EyeOff className="h-4 w-4 mr-2" /> : <Eye className="h-4 w-4 mr-2" />}
                {showDetails ? 'Hide technical detail' : 'Show technical detail'}
              </Button>
              <Button variant="outline" size="sm" onClick={handleExportResults}>
                <Download className="h-4 w-4 mr-2" />
                Export
              </Button>
              <Button variant="outline" size="sm" onClick={handleShareResults}>
                <Share2 className="h-4 w-4 mr-2" />
                Share
              </Button>
            </div>
          </div>

          {showDetails ? (
            <Card className="mb-6 border-dashed">
              <CardContent className="pt-4">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm text-gray-600">
                  <div>
                    <span className="text-gray-500 block text-xs uppercase tracking-wide">Completed</span>
                    <p>{completed_at ? new Date(completed_at).toLocaleString() : 'N/A'}</p>
                  </div>
                  <div>
                    <span className="text-gray-500 block text-xs uppercase tracking-wide">Markers analysed</span>
                    <p>{biomarkers.length}</p>
                  </div>
                  <div>
                    <span className="text-gray-500 block text-xs uppercase tracking-wide">Analysis reference</span>
                    <p className="font-mono text-xs break-all">{currentAnalysis.analysis_id}</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          ) : (
            <p className="text-sm text-gray-500 mb-2">
              {completed_at ? `Completed ${new Date(completed_at).toLocaleDateString()}` : null}
              {completed_at && biomarkers.length ? ' · ' : ''}
              {biomarkers.length ? `${biomarkers.length} markers` : null}
            </p>
          )}
        </div>

        <div className="space-y-10">
          {/* 1 Hero interpretation */}
          <section aria-labelledby="hero-interpretation">
            <h2 id="hero-interpretation" className="sr-only">
              Primary interpretation
            </h2>
            <InsightPanel report={clinicianReport} />
          </section>

          {/* 2 Trust / data quality */}
          <section aria-labelledby="trust-layer">
            <h2 id="trust-layer" className="sr-only">
              Data quality
            </h2>
            <PipelineStatus
              dataQuality={clinicianReport?.data_quality}
              confirmatoryTests={clinicianReport?.sections?.confirmatory_tests}
            />
          </section>

          {/* 3 Body systems / clusters */}
          <section className="space-y-3" aria-labelledby="cluster-heading">
            <h2 id="cluster-heading" className="text-xl font-semibold text-gray-900">
              Body systems &amp; patterns
            </h2>
            <p className="text-sm text-gray-600">
              How your markers group into biological patterns. Names describe the pattern, not internal IDs.
            </p>
            <ClusterSummary
              clusters={clusterSummaries}
              isLoading={clustersLoading}
              showDetails={showDetails}
            />
          </section>

          {/* 4 Biomarker supporting layer */}
          <section aria-labelledby="biomarkers-heading">
            <h2 id="biomarkers-heading" className="sr-only">
              Biomarker detail
            </h2>
            <BiomarkerDials biomarkers={biomarkerDialData} showDetails={showDetails} />
          </section>

          {/* Optional reserved: symptom relevance (dormant) */}
          <section aria-hidden="true" className="opacity-60">
            <Card className="border-dashed border-gray-300 bg-gray-50/50">
              <CardHeader className="py-3">
                <CardTitle className="text-sm font-medium text-gray-500">Symptom relevance</CardTitle>
                <CardDescription className="text-xs">Reserved for a future release — no personalised content yet.</CardDescription>
              </CardHeader>
            </Card>
          </section>

          {/* 5 Deeper disclosure: overview, insights list, clinician */}
          <section className="space-y-4" aria-labelledby="more-detail">
            <h2 id="more-detail" className="text-xl font-semibold text-gray-900">
              Additional detail
            </h2>
            <Tabs value={activeDetailTab} onValueChange={setActiveDetailTab} className="w-full">
              <TabsList className="grid w-full grid-cols-3 mb-6">
                <TabsTrigger value="overview" className="flex items-center gap-2 text-xs sm:text-sm">
                  <BarChart3 className="h-4 w-4 shrink-0" />
                  Overview
                </TabsTrigger>
                <TabsTrigger value="insights" className="flex items-center gap-2 text-xs sm:text-sm">
                  <TrendingUp className="h-4 w-4 shrink-0" />
                  All insights
                </TabsTrigger>
                <TabsTrigger value="clinician" className="flex items-center gap-2 text-xs sm:text-sm">
                  <CheckCircle className="h-4 w-4 shrink-0" />
                  Clinician report
                </TabsTrigger>
              </TabsList>

              <TabsContent value="overview" className="space-y-6">
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  <Card>
                    <CardHeader>
                      <CardTitle className="flex items-center gap-2">
                        <CheckCircle className="h-5 w-5 text-green-500" />
                        Overall score
                      </CardTitle>
                      <CardDescription>Summary metric from the analysis engine — supporting context, not a clinical diagnosis.</CardDescription>
                    </CardHeader>
                    <CardContent>
                      <div className="text-center">
                        <div className="text-5xl font-bold text-green-600 mb-2">
                          {overallPercent != null ? overallPercent : 'N/A'}
                        </div>
                        {overallPercent != null ? <p className="text-gray-600 text-sm">Normalised display score</p> : null}
                        <div className="mt-4 w-full bg-gray-200 rounded-full h-3">
                          <div
                            className="bg-green-500 h-3 rounded-full transition-all duration-1000"
                            style={{ width: `${Math.min(100, overallPercent ??  0)}%` }}
                          ></div>
                        </div>
                      </div>
                    </CardContent>
                  </Card>

                  <Card>
                    <CardHeader>
                      <CardTitle>Risk summary</CardTitle>
                      <CardDescription>From the engine risk assessment object, when present.</CardDescription>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-4">
                        {currentAnalysis.risk_assessment &&
                        typeof currentAnalysis.risk_assessment === 'object' &&
                        !Array.isArray(currentAnalysis.risk_assessment) ? (
                          Object.entries(currentAnalysis.risk_assessment).map(([category, score]) => (
                            <div key={category} className="flex justify-between items-center">
                              <span className="capitalize text-sm font-medium text-gray-700">
                                {category.replace(/([A-Z])/g, ' $1').trim()}
                              </span>
                              <div className="flex items-center gap-2">
                                {typeof score === 'number' ? (
                                  <>
                                    <div className="w-20 bg-gray-200 rounded-full h-2">
                                      <div
                                        className="bg-blue-500 h-2 rounded-full"
                                        style={{ width: `${Math.min(100, Math.max(0, score))}%` }}
                                      ></div>
                                    </div>
                                    <span className="text-sm font-semibold w-8">{Math.round(score)}</span>
                                  </>
                                ) : (
                                  <span className="text-sm text-gray-700">{String(score)}</span>
                                )}
                              </div>
                            </div>
                          ))
                        ) : (
                          <p className="text-sm text-gray-500">No structured risk breakdown for this result.</p>
                        )}
                      </div>
                    </CardContent>
                  </Card>
                </div>

                {insights && insights.length > 0 ? (
                  <Alert>
                    <AlertDescription>
                      {insights.length} engine insight{insights.length === 1 ? '' : 's'} available — open the &quot;All
                      insights&quot; tab for the full list.
                    </AlertDescription>
                  </Alert>
                ) : null}
              </TabsContent>

              <TabsContent value="insights" className="space-y-6">
                {insights && insights.length > 0 ? (
                  <InsightsPanel insights={insights} />
                ) : (
                  <Card>
                    <CardContent className="pt-6">
                      <div className="text-center py-8">
                        <TrendingUp className="h-12 w-12 text-gray-300 mx-auto mb-4" />
                        <p className="text-gray-500">No insights available yet.</p>
                        <p className="text-sm text-gray-400">Complete your analysis to generate personalised insights.</p>
                      </div>
                    </CardContent>
                  </Card>
                )}
              </TabsContent>

              <TabsContent value="clinician" className="space-y-6">
                <ClinicianReportRenderer report={clinicianReport} />
              </TabsContent>
            </Tabs>
          </section>
        </div>

        <div className="mt-10 flex justify-center gap-4">
          <Button onClick={handleNewAnalysis} variant="outline">
            Start New Analysis
          </Button>
          <Button onClick={handleExportResults}>
            <Download className="h-4 w-4 mr-2" />
            Export Results
          </Button>
        </div>
      </div>
    </div>
  );
}
