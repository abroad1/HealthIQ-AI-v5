'use client';

import React, { useEffect, useMemo, useRef, useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import {
  BarChart3,
  TrendingUp,
  AlertCircle,
  RefreshCw,
  Download,
  Share2,
  Eye,
  EyeOff,
  ChevronDown,
  ChevronRight,
} from 'lucide-react';
import { useAnalysisStore } from '@/state/analysisStore';
import { useClusterStore } from '@/state/clusterStore';
import { InsightsPanel } from '@/components/insights/InsightsPanel';
import { InsightPanel } from '@/components/insights/InsightPanel';
import BiomarkerDials, { type BiomarkerDialEntry } from '@/components/biomarkers/BiomarkerDials';
import ClusterSummary from '@/components/clusters/ClusterSummary';
import ClinicianReportRenderer from '@/components/results/ClinicianReportRenderer';
import { BalancedSystemsSummary } from '@/components/results/BalancedSystemsSummary';
import { ResultsBodyOverview } from '@/components/results/ResultsBodyOverview';
import { PrimaryFindingAndWhy } from '@/components/results/PrimaryFindingAndWhy';
import { WhyThisLeadWonSection } from '@/components/results/WhyThisLeadWonSection';
import PipelineStatus from '@/components/pipeline/PipelineStatus';
import { useRouter, useSearchParams } from 'next/navigation';
import { useAnalysisResult } from '@/queries/analysisResult';
import type { Cluster, ClinicianReportV1 } from '@/types/analysis';
import Link from 'next/link';
import { extractNarrativeRuntimeMeta } from '@/lib/narrativeRuntimePresentation';
import { emitWedgeEvent } from '@/lib/wedgeAnalytics';

function pickPrimaryDriverCluster(clusters: Cluster[]): { id: string; name: string; biomarkers: string[] } | null {
  const sevRank: Record<string, number> = { critical: 4, high: 3, moderate: 2, low: 1 };
  let best: { id: string; name: string; biomarkers: string[]; rank: number; score: number } | null = null;
  clusters.forEach((cluster, idx) => {
    const id = String(cluster.cluster_id || cluster.id || `cluster-${idx}`);
    const sev = String(cluster.severity || 'moderate').toLowerCase();
    const rank = sevRank[sev] ?? 2;
    const score = typeof cluster.score === 'number' ? cluster.score : (cluster.confidence ?? 0) * 100;
    const name = cluster.name?.trim() ? cluster.name : 'Health pattern';
    const biomarkers = cluster.biomarkers || cluster.biomarkers_involved || [];
    if (!best || rank > best.rank || (rank === best.rank && score > best.score)) {
      best = { id, name, biomarkers, rank, score };
    }
  });
  if (!best) return null;
  return { id: best.id, name: best.name, biomarkers: best.biomarkers };
}

function computeMissingChapterLine(
  report: ClinicianReportV1 | null | undefined,
  primaryDriver: { biomarkers: string[] } | null
): string | null {
  if (!report?.data_quality) return null;
  const dq = report.data_quality;
  const present = dq.panel_completeness_present ?? 0;
  const expected = dq.panel_completeness_expected ?? 0;
  const downgraded = dq.data_quality_passed === false;
  const labLines = dq.lab_range_quality_by_primary_metric ?? [];
  const missingish = labLines.filter((l) =>
    /missing|not tested|not available|no lab range|no reference|was not tested|not on panel/i.test(l)
  );
  const panelGap = expected > 0 && present < expected;

  if (missingish.length === 0 && !panelGap) return null;

  const page1 = report.sections?.page1;
  const heroBlob = [page1?.primary_concern, ...(page1?.key_findings ?? []), ...(page1?.chains ?? [])]
    .join(' ')
    .toLowerCase();

  const affectsHero = missingish.some((line) => {
    const tokens = line
      .toLowerCase()
      .split(/\s+/)
      .filter((w) => w.length > 3);
    return tokens.some((t) => heroBlob.includes(t.replace(/[^a-z0-9]/g, '')) || heroBlob.includes(t));
  });

  const driverM = primaryDriver?.biomarkers.map((b) => b.toLowerCase()) ?? [];
  const affectsDriver = missingish.some((line) => {
    const low = line.toLowerCase();
    return driverM.some((b) => low.includes(b) || low.includes(b.replace(/_/g, ' ')));
  });

  if (!affectsHero && !affectsDriver && !downgraded) return null;

  return (
    missingish[0] ||
    (panelGap
      ? `Some expected markers are not in this panel yet (${present} of ${expected} present), which can limit how complete the lead story is.`
      : null)
  );
}

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
  const [advancedOpen, setAdvancedOpen] = useState(false);
  const resultsViewedForId = useRef<string | null>(null);

  const idToFetch = currentAnalysisId || analysisIdFromUrl;
  const {
    isLoading: isResultLoading,
    isError: isResultFetchError,
    error: resultFetchError,
  } = useAnalysisResult(idToFetch || null);
  const isFetchingFromUrl = !!idToFetch && isResultLoading;

  const insights = currentAnalysis?.insights ?? [];
  const biomarkers = currentAnalysis?.biomarkers ?? [];
  const clusters = currentAnalysis?.clusters ?? [];
  const clinicianReport = currentAnalysis?.clinician_report_v1;
  const balancedSystems = currentAnalysis?.balanced_systems_v1;
  const { created_at, completed_at } = currentAnalysis || {};

  const narrativeRuntime = useMemo(
    () => extractNarrativeRuntimeMeta(currentAnalysis?.meta),
    [currentAnalysis?.meta]
  );

  const primaryDriver = useMemo(() => pickPrimaryDriverCluster(clusters), [clusters]);
  const missingChapterLine = useMemo(
    () => computeMissingChapterLine(clinicianReport, primaryDriver),
    [clinicianReport, primaryDriver]
  );

  const keyFindingsOverflow = clinicianReport?.sections?.page1?.key_findings?.slice(1) ?? [];

  useEffect(() => {
    if (analysisIdFromUrl && analysisIdFromUrl !== currentAnalysisId) {
      setCurrentAnalysisId(analysisIdFromUrl);
    }
  }, [analysisIdFromUrl, currentAnalysisId, setCurrentAnalysisId]);

  useEffect(() => {
    if (!currentAnalysis || isAnalyzing || isFetchingFromUrl) return;
    if (currentAnalysis.status !== 'completed') return;
    const id = currentAnalysis.analysis_id;
    if (!id || resultsViewedForId.current === id) return;
    resultsViewedForId.current = id;

    let entry: 'fresh' | 'from_url' | 'from_history' = 'fresh';
    if (typeof window !== 'undefined') {
      try {
        if (sessionStorage.getItem('wedge_reopen_flag') === '1') {
          sessionStorage.removeItem('wedge_reopen_flag');
          entry = 'from_history';
        } else if (analysisIdFromUrl) {
          entry = 'from_url';
        }
      } catch {
        if (analysisIdFromUrl) entry = 'from_url';
      }
    } else if (analysisIdFromUrl) {
      entry = 'from_url';
    }

    emitWedgeEvent({
      event_name: 'wedge_results_viewed',
      timestamp: new Date().toISOString(),
      route: '/results',
      analysis_id: id,
      entry,
    });
  }, [currentAnalysis, isAnalyzing, isFetchingFromUrl, analysisIdFromUrl]);

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

    emitWedgeEvent({
      event_name: 'wedge_results_export_json_clicked',
      timestamp: new Date().toISOString(),
      route: '/results',
      analysis_id: currentAnalysis.analysis_id,
    });

    const dataStr = JSON.stringify(currentAnalysis, null, 2);
    const dataUri = 'data:application/json;charset=utf-8,' + encodeURIComponent(dataStr);

    const exportFileDefaultName = `healthiq-analysis-${new Date().toISOString().split('T')[0]}.json`;

    const linkElement = document.createElement('a');
    linkElement.setAttribute('href', dataUri);
    linkElement.setAttribute('download', exportFileDefaultName);
    linkElement.click();
  };

  const handleShareResults = () => {
    if (currentAnalysis) {
      emitWedgeEvent({
        event_name: 'wedge_results_share_link_clicked',
        timestamp: new Date().toISOString(),
        route: '/results',
        analysis_id: currentAnalysis.analysis_id,
      });
    }
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
                  : 'We are processing your biomarker data and structured analysis. Short narrative summaries may appear later under Advanced analysis when available. This may take a few moments.'}
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

  if (
    !isAnalyzing &&
    !isFetchingFromUrl &&
    !!idToFetch &&
    isResultFetchError &&
    !currentAnalysis
  ) {
    const msg =
      resultFetchError instanceof Error ? resultFetchError.message : 'Could not load this analysis.';
    const signInHref = `/login?next=${encodeURIComponent(
      `/results?analysis_id=${encodeURIComponent(idToFetch)}`
    )}`;
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <Card className="w-full max-w-md">
          <CardContent className="pt-6">
            <div className="text-center space-y-3">
              <AlertCircle className="h-16 w-16 text-amber-500 mx-auto mb-2" />
              <h2 className="text-2xl font-bold text-gray-900 mb-2">Could not open this result</h2>
              <p className="text-gray-600 text-sm">{msg}</p>
              <p className="text-gray-500 text-xs">
                Saved analyses are tied to your account. Sign in with the same account you used when you ran the
                analysis, or start a new upload.
              </p>
              <div className="flex flex-col gap-2 pt-2">
                <Button asChild className="w-full">
                  <Link href={signInHref}>Sign in to retry</Link>
                </Button>
                <Button asChild variant="outline" className="w-full">
                  <Link href="/upload">New analysis</Link>
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

  const biomarkerDialData: Record<string, BiomarkerDialEntry> = {};

  const relatedGroupNamesFor = (biomarkerName: string): string[] => {
    return clusters
      .filter((c) => (c.biomarkers || c.biomarkers_involved || []).includes(biomarkerName))
      .map((c) => (c.name?.trim() ? c.name : 'System group'))
      .filter(Boolean);
  };

  biomarkers
    .filter((b) => b.biomarker_name && b.value != null && typeof b.value === 'number')
    .forEach((biomarker) => {
      const expl = biomarker.biomarker_educational_explainer;
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
        educationalExplainer: expl?.body ? { title: expl.title, body: expl.body } : null,
        contributionContext: biomarker.contribution_context?.factual_statement
          ? { factual_statement: biomarker.contribution_context.factual_statement }
          : null,
        relatedSystemGroupNames: relatedGroupNamesFor(biomarker.biomarker_name),
      };
    });

  const clusterSummaries = clusters.map((cluster, idx) => {
    const id = String(cluster.cluster_id || cluster.id || `cluster-${idx}`);
    const expl = cluster.system_educational_explainer;
    return {
      id,
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
      isPrimaryDriver: primaryDriver?.id === id,
      systemEducationalExplainer: expl?.body ? { title: expl.title, body: expl.body } : null,
    };
  });

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
                Start with a body-level overview, then what looks stable, then deeper evidence and markers. Full clinical
                detail stays in Advanced analysis.
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
          <section aria-labelledby="body-overview-section-label">
            <h2 id="body-overview-section-label" className="sr-only">
              Body overview
            </h2>
            <ResultsBodyOverview clinicianReport={clinicianReport} clusters={clusters} />
          </section>

          <section aria-labelledby="whats-working-section-label">
            <h2 id="whats-working-section-label" className="sr-only">
              What is working well
            </h2>
            <BalancedSystemsSummary balanced={balancedSystems} maxItems={4} />
          </section>

          <section aria-labelledby="primary-finding-section-label">
            <h2 id="primary-finding-section-label" className="sr-only">
              Primary finding and why
            </h2>
            <PrimaryFindingAndWhy report={clinicianReport} />
          </section>

          <section aria-labelledby="why-lead-won-section-label">
            <h2 id="why-lead-won-section-label" className="sr-only">
              Why this lead won and uncertainty
            </h2>
            <WhyThisLeadWonSection report={clinicianReport} />
          </section>

          <section aria-labelledby="trust-layer">
            <h2 id="trust-layer" className="sr-only">
              Trust strip
            </h2>
            <PipelineStatus
              dataQuality={clinicianReport?.data_quality}
              confirmatoryTests={clinicianReport?.sections?.confirmatory_tests}
              missingChapterLine={missingChapterLine}
            />
          </section>

          <section aria-labelledby="hero-interpretation">
            <h2 id="hero-interpretation" className="sr-only">
              Clinical interpretation detail
            </h2>
            <InsightPanel
              report={clinicianReport}
              primaryDriverSystemGroupName={primaryDriver?.name ?? null}
              contextOnly
            />
          </section>

          <section className="space-y-3" aria-labelledby="cluster-heading">
            <h2 id="cluster-heading" className="text-xl font-semibold text-gray-900">
              System groups
            </h2>
            <p className="text-sm text-gray-600">
              How your markers group into biological patterns. Names describe the pattern in plain language.
            </p>
            <ClusterSummary clusters={clusterSummaries} isLoading={clustersLoading} showDetails={showDetails} />
          </section>

          <section aria-labelledby="biomarkers-heading">
            <h2 id="biomarkers-heading" className="sr-only">
              Biomarker evidence
            </h2>
            <BiomarkerDials biomarkers={biomarkerDialData} sectionTitle="Biomarker evidence" />
          </section>

          <section aria-labelledby="advanced-analysis-heading">
            <h2 id="advanced-analysis-heading" className="sr-only">
              Advanced analysis
            </h2>
            <Card className="border-slate-200">
              <CardHeader className="pb-2">
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <CardTitle className="text-lg">Advanced analysis</CardTitle>
                  <Button
                    type="button"
                    variant="outline"
                    size="sm"
                    onClick={() => setAdvancedOpen((o) => !o)}
                    aria-expanded={advancedOpen}
                  >
                    {advancedOpen ? (
                      <>
                        <ChevronDown className="h-4 w-4 mr-2" /> Collapse
                      </>
                    ) : (
                      <>
                        <ChevronRight className="h-4 w-4 mr-2" /> Expand
                      </>
                    )}
                  </Button>
                </div>
                <CardDescription>
                  Structured clinician report, readable narrative summaries from your results, and technical context —
                  same page, progressive disclosure.
                </CardDescription>
              </CardHeader>
              {advancedOpen ? (
                <CardContent className="pt-0">
                  <Tabs
                    value={activeDetailTab}
                    onValueChange={(v) => {
                      setActiveDetailTab(v);
                      if (v === 'clinician' && currentAnalysis?.analysis_id) {
                        emitWedgeEvent({
                          event_name: 'wedge_clinician_report_viewed',
                          timestamp: new Date().toISOString(),
                          route: '/results',
                          analysis_id: currentAnalysis.analysis_id,
                        });
                      }
                    }}
                    className="w-full"
                  >
                    <TabsList className="grid w-full grid-cols-3 mb-6">
                      <TabsTrigger value="overview" className="flex items-center gap-2 text-xs sm:text-sm">
                        <BarChart3 className="h-4 w-4 shrink-0" />
                        Overview
                      </TabsTrigger>
                      <TabsTrigger value="insights" className="flex items-center gap-2 text-xs sm:text-sm">
                        <TrendingUp className="h-4 w-4 shrink-0" />
                        Narrative
                      </TabsTrigger>
                      <TabsTrigger value="clinician" className="flex items-center gap-2 text-xs sm:text-sm">
                        <AlertCircle className="h-4 w-4 shrink-0" />
                        Clinician report
                      </TabsTrigger>
                    </TabsList>

                    <TabsContent value="overview" className="space-y-6">
                      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                        <Card>
                          <CardHeader>
                            <CardTitle className="flex items-center gap-2">Overall score</CardTitle>
                            <CardDescription>
                              Summary metric from the analysis engine — supporting context, not a clinical diagnosis.
                            </CardDescription>
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
                                  style={{ width: `${Math.min(100, overallPercent ?? 0)}%` }}
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

                      {keyFindingsOverflow.length > 0 ? (
                        <div>
                          <h3 className="text-sm font-semibold text-gray-800 mb-2">Additional key findings</h3>
                          <ul className="list-disc pl-5 space-y-1 text-sm text-gray-700">
                            {keyFindingsOverflow.map((line, i) => (
                              <li key={i}>{line}</li>
                            ))}
                          </ul>
                        </div>
                      ) : null}

                      {insights && insights.length > 0 ? (
                        <Alert>
                          <AlertDescription>
                            {insights.length} short narrative summar{insights.length === 1 ? 'y' : 'ies'} available —
                            open the &quot;Narrative&quot; tab for the full list. These summaries complement the
                            clinical interpretation; they are not the primary structured report.
                          </AlertDescription>
                        </Alert>
                      ) : null}
                    </TabsContent>

                    <TabsContent value="insights" className="space-y-6">
                      <InsightsPanel insights={insights} narrativeRuntime={narrativeRuntime} />
                    </TabsContent>

                    <TabsContent value="clinician" className="space-y-6">
                      <ClinicianReportRenderer report={clinicianReport} balancedSystems={balancedSystems} />
                    </TabsContent>
                  </Tabs>
                </CardContent>
              ) : null}
            </Card>
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
