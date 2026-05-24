'use client';

import React, { useEffect, useMemo, useRef, useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { AlertCircle, ArrowRight, RefreshCw, Download, Share2, Eye, EyeOff } from 'lucide-react';
import { useAnalysisStore } from '@/state/analysisStore';
import { useClusterStore } from '@/state/clusterStore';
import { InsightsPanel } from '@/components/insights/InsightsPanel';
import { InsightPanel } from '@/components/insights/InsightPanel';
import BiomarkerDials, { type BiomarkerDialEntry } from '@/components/biomarkers/BiomarkerDials';
import UploadedPanelFidelity from '@/components/biomarkers/UploadedPanelFidelity';
import { buildUploadedPanelFidelityRows } from '@/lib/uploadPanelFidelity';
import ClusterSummary from '@/components/clusters/ClusterSummary';
import ClinicianReportRenderer from '@/components/results/ClinicianReportRenderer';
import { BalancedSystemsSummary } from '@/components/results/BalancedSystemsSummary';
import { PrimaryFindingAndWhy } from '@/components/results/PrimaryFindingAndWhy';
import { WhyThisLeadWonSection } from '@/components/results/WhyThisLeadWonSection';
import { SystemUnderstandingSection } from '@/components/results/SystemUnderstandingSection';
import { LayerCInsightSection } from '@/components/results/LayerCInsightSection';
import { InterpretationPatternsSection } from '@/components/results/InterpretationPatternsSection';
import { selectSafeIdlPatternRecords } from '@/lib/feR5aIdlPatternGuards';
import { ResultsInvestigationSpine } from '@/components/results/ResultsInvestigationSpine';
import {
  NarrativeLeadAndSupportingSections,
  NarrativeLongitudinalAndNextSteps,
} from '@/components/results/DeterministicNarrativeSurface';
import { ResultsBodyOverview } from '@/components/results/ResultsBodyOverview';
import { ResultsDisclosureSection } from '@/components/results/ResultsDisclosureSection';
import {
  ResultsActionCardsBlock,
  ResultsDrivingSignals,
  ResultsPrimaryHero,
  triggerBrowserDownload,
} from '@/components/results/ResultsHeroBlocks';
import { Wave1DomainCards } from '@/components/results/Wave1DomainCards';
import { ConfirmatoryTestsNextSteps } from '@/components/results/ConfirmatoryTestsNextSteps';
import {
  dedupeActionCardsAgainstNarrative,
  hasGovernedConfirmatoryTests,
} from '@/lib/feR3NextStepsLayout';
import { filterNarrativeNextStepsForConfirmatoryDedup } from '@/lib/feR6aRetailCopy';
import { parseNarrativeNextStepParagraphs } from '@/lib/resultsPageLayout';
import { AnalysisService } from '@/services/analysis';
import PipelineStatus from '@/components/pipeline/PipelineStatus';
import { useRouter, useSearchParams } from 'next/navigation';
import { useAnalysisResult } from '@/queries/analysisResult';
import type { Cluster, ClinicianReportV1, Wave1AlignedDriversV1 } from '@/types/analysis';
import type { LayerCFeatureBundleV1 } from '@/types/layerCFeatures';
import Link from 'next/link';
import { extractNarrativeRuntimeMeta } from '@/lib/narrativeRuntimePresentation';
import { emitWedgeEvent } from '@/lib/wedgeAnalytics';
import { derivePatternRelevanceLine } from '@/lib/biomarkerPatternRelevance';
import { filterConsumerInsights, legacyInsightsDebugEnabled } from '@/lib/legacyInsightsVisibility';
import { LC_S4_MOCK_MODE_HONESTY_DISCLOSURE } from '@/lib/lcS4ResultsCopy';
import {
  buildActionCardModels,
  buildPrimaryHeroSummary,
  getFirstIdlRecord,
  pickHeroAlignedPrimaryDriver,
  pickPhenotypeLabel,
  pickBiomarkersByWave1Keys,
  pickTopDriverBiomarkers,
  resolvePrimaryFindingSeverity,
  resolveHeroPrimaryStory,
} from '@/lib/resultsPageLayout';
import { FE_R2_RESULTS_JOURNEY_SECTION_TEST_IDS } from '@/lib/feR2ResultsJourneyOrder';

const BIOMARKER_DIALS_SECTION_ID = 'section-biomarker-dials';

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

function clusterById(clusters: Cluster[], id: string): Cluster | undefined {
  return clusters.find((c) => String(c.cluster_id || c.id) === id);
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

  const [showDetails, setShowDetails] = useState(false);
  const [pdfDownloadPending, setPdfDownloadPending] = useState(false);
  const [pdfDownloadError, setPdfDownloadError] = useState<string | null>(null);
  const resultsViewedForId = useRef<string | null>(null);
  const clinicianWedgeSentRef = useRef(false);

  const idToFetch = currentAnalysisId || analysisIdFromUrl;
  const {
    isLoading: isResultLoading,
    isError: isResultFetchError,
    error: resultFetchError,
  } = useAnalysisResult(idToFetch || null);
  const isFetchingFromUrl = !!idToFetch && isResultLoading;

  const insights = currentAnalysis?.insights ?? [];
  const consumerInsights = useMemo(() => filterConsumerInsights(insights), [insights]);
  const biomarkers = currentAnalysis?.biomarkers ?? [];
  const clusters = currentAnalysis?.clusters ?? [];
  const clinicianReport = currentAnalysis?.clinician_report_v1;
  const balancedSystems = currentAnalysis?.balanced_systems_v1;
  const narrativeReport = currentAnalysis?.narrative_report_v1;
  const { created_at, completed_at } = currentAnalysis || {};

  const narrativeRuntime = useMemo(
    () => extractNarrativeRuntimeMeta(currentAnalysis?.meta),
    [currentAnalysis?.meta]
  );

  const firstIdl = useMemo(
    () => getFirstIdlRecord(currentAnalysis?.interpretation_display_layer_v1),
    [currentAnalysis?.interpretation_display_layer_v1]
  );

  const primaryDriver = useMemo(() => pickHeroAlignedPrimaryDriver(clusters, firstIdl), [clusters, firstIdl]);
  const primaryCluster = useMemo(
    () => (primaryDriver ? clusterById(clusters, primaryDriver.id) : undefined),
    [clusters, primaryDriver]
  );
  const missingChapterLine = useMemo(
    () => computeMissingChapterLine(clinicianReport, primaryDriver),
    [clinicianReport, primaryDriver]
  );

  const keyFindingsOverflow = clinicianReport?.sections?.page1?.key_findings?.slice(1) ?? [];

  const retailIdlPatternRecords = useMemo(
    () => selectSafeIdlPatternRecords(currentAnalysis?.interpretation_display_layer_v1?.records),
    [currentAnalysis?.interpretation_display_layer_v1]
  );

  const showRetailIdlPatterns = retailIdlPatternRecords.length > 0;

  const firstIdlRetailLabel = useMemo(() => {
    return retailIdlPatternRecords[0]?.retail_display_label?.trim() ?? null;
  }, [retailIdlPatternRecords]);

  const phenotypeLabel = useMemo(
    () => pickPhenotypeLabel(clinicianReport, firstIdl, primaryDriver),
    [clinicianReport, firstIdl, primaryDriver]
  );

  const heroSummary = useMemo(
    () => buildPrimaryHeroSummary(narrativeReport?.retail_summary, clinicianReport, firstIdl),
    [narrativeReport?.retail_summary, clinicianReport, firstIdl]
  );

  const heroStory = useMemo(
    () => resolveHeroPrimaryStory(clinicianReport, phenotypeLabel, firstIdl),
    [clinicianReport, phenotypeLabel, firstIdl]
  );

  const heroSeverity = useMemo(
    () => resolvePrimaryFindingSeverity(firstIdl, primaryCluster),
    [firstIdl, primaryCluster]
  );

  const wave1DriverKeys = (currentAnalysis?.meta as { wave1_aligned_drivers?: Wave1AlignedDriversV1 } | undefined)
    ?.wave1_aligned_drivers?.biomarker_keys;

  const topDriverMarkers = useMemo(() => {
    const aligned = pickBiomarkersByWave1Keys(biomarkers, wave1DriverKeys);
    if (aligned.length > 0) return aligned;
    return pickTopDriverBiomarkers(biomarkers, primaryDriver);
  }, [biomarkers, primaryDriver, wave1DriverKeys]);

  const narrativeNextStepsText = narrativeReport?.next_steps_narrative ?? null;

  const confirmatoryTestsForJourney = clinicianReport?.sections?.confirmatory_tests ?? [];

  const showConfirmatoryInNextSteps = hasGovernedConfirmatoryTests(confirmatoryTestsForJourney);

  const narrativeNextStepsParagraphs = useMemo(() => {
    const raw = narrativeNextStepsText?.trim();
    if (!raw) return [] as string[];
    const names = confirmatoryTestsForJourney.map((t) => t.display_name || '');
    return filterNarrativeNextStepsForConfirmatoryDedup(
      parseNarrativeNextStepParagraphs(raw),
      names
    );
  }, [narrativeNextStepsText, confirmatoryTestsForJourney]);

  const actionCards = useMemo(() => {
    const built = buildActionCardModels(clusters, currentAnalysis?.recommendations, {
      maxItems: 5,
      narrativeNextStepsNarrative: narrativeNextStepsText,
      omitNarrativeNextStepsFromCards: Boolean((narrativeNextStepsText || '').trim().length > 0),
    });
    return dedupeActionCardsAgainstNarrative(built, narrativeNextStepsText);
  }, [clusters, currentAnalysis?.recommendations, narrativeNextStepsText]);

  const showInsightsPanelSection = legacyInsightsDebugEnabled() || consumerInsights.length > 0;

  const handleDownloadReport = React.useCallback(async () => {
    const id = currentAnalysis?.analysis_id;
    if (!id) return;
    setPdfDownloadPending(true);
    setPdfDownloadError(null);
    const res = await AnalysisService.downloadSummaryPdf(id);
    setPdfDownloadPending(false);
    if ('error' in res) {
      setPdfDownloadError(res.error);
      return;
    }
    triggerBrowserDownload(res.blob, res.filename);
    emitWedgeEvent({
      event_name: 'wedge_results_pdf_downloaded',
      timestamp: new Date().toISOString(),
      route: '/results',
      analysis_id: id,
    });
  }, [currentAnalysis?.analysis_id]);

  const handleAdvancedOpen = (open: boolean) => {
    if (!open || !currentAnalysis?.analysis_id || clinicianWedgeSentRef.current) return;
    clinicianWedgeSentRef.current = true;
    emitWedgeEvent({
      event_name: 'wedge_clinician_report_viewed',
      timestamp: new Date().toISOString(),
      route: '/results',
      analysis_id: currentAnalysis.analysis_id,
    });
  };

  useEffect(() => {
    clinicianWedgeSentRef.current = false;
  }, [currentAnalysis?.analysis_id]);

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
      void retryAnalysis();
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
                  : 'We are processing your biomarker data and structured analysis. This may take a few moments.'}
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
      const relatedSystemGroupNames = relatedGroupNamesFor(biomarker.biomarker_name);
      const hasContributionFactual = !!biomarker.contribution_context?.factual_statement?.trim();
      const patternRelevanceLine = derivePatternRelevanceLine({
        biomarkerKey: biomarker.biomarker_name,
        primaryDriver,
        hasContributionFactual,
        relatedSystemGroupNames,
      });
      const shownValue =
        typeof biomarker.display_value === 'number' ? biomarker.display_value : (biomarker.value as number);
      const shownUnit = (biomarker.display_unit || biomarker.unit || '').trim();
      const shownRef = biomarker.display_reference_range ?? biomarker.reference_range;

      const displayLabel = biomarker.display_label?.trim() || undefined;

      biomarkerDialData[biomarker.biomarker_name] = {
        value: shownValue,
        unit: shownUnit,
        displayLabel,
        status: biomarker.status ?? undefined,
        score: biomarker.score ?? undefined,
        interpretation: biomarker.interpretation ?? undefined,
        referenceRange: shownRef
          ? {
              min: shownRef.min ?? undefined,
              max: shownRef.max ?? undefined,
              unit: shownRef.unit,
              source: shownRef.source ?? undefined,
            }
          : undefined,
        date: created_at,
        educationalExplainer: expl?.body ? { title: expl.title, body: expl.body } : null,
        contributionContext: biomarker.contribution_context?.factual_statement
          ? { factual_statement: biomarker.contribution_context.factual_statement }
          : null,
        relatedSystemGroupNames,
        patternRelevanceLine,
      };
    });

  const uploadPanelFidelityRows = buildUploadedPanelFidelityRows(
    currentAnalysis.meta?.upload_panel_observations as Record<string, unknown> | undefined,
    currentAnalysis.meta?.display_unit_policy,
    biomarkers
  );

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

  const insightGraph = currentAnalysis.meta?.insight_graph as { layer_c_features?: LayerCFeatureBundleV1 } | undefined;
  const layerCFeatures: LayerCFeatureBundleV1 | null = insightGraph?.layer_c_features ?? null;

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="container mx-auto px-4 max-w-6xl">
        <div className="mb-8">
          <div className="flex flex-col gap-4 md:flex-row md:items-start md:justify-between mb-4">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-1">Your results</h1>
              <p className="text-gray-600 max-w-2xl">
                This page walks through your results in order: whole-body context, what looks stable, your main finding,
                uncertainty, marker evidence, and follow-up — with a separate clinician summary below.
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

        <div className="space-y-8">
          {narrativeRuntime?.synthesizer_allow_llm_resolved === false ? (
            <Alert className="border-slate-200 bg-slate-50/80" data-testid="mock-mode-narrative-disclosure">
              <AlertDescription className="text-slate-800 text-sm">{LC_S4_MOCK_MODE_HONESTY_DISCLOSURE}</AlertDescription>
            </Alert>
          ) : null}

          {/* FE-R2 Phase 1 journey — section order must match FE_R2_RESULTS_JOURNEY_SECTION_TEST_IDS */}
          <section
            className="space-y-6"
            aria-labelledby="fe-r2-body-overview-heading"
            data-testid={FE_R2_RESULTS_JOURNEY_SECTION_TEST_IDS[0]}
          >
            <ResultsPrimaryHero
              phenotypeLabel={heroStory.heroTitle}
              summary={heroSummary}
              rankedSignalSecondaryLine={heroStory.bridgeExplanation}
              systemContextLine={heroStory.systemContextLine}
              severityLabel={heroSeverity.label}
              severityTone={heroSeverity.tone}
              onDownloadReport={
                currentAnalysis?.status === 'completed' && currentAnalysis.analysis_id
                  ? handleDownloadReport
                  : undefined
              }
              downloadPending={pdfDownloadPending}
              downloadError={pdfDownloadError}
              downloadDisabledReason="Complete an analysis to download your PDF summary."
            />
            <ResultsBodyOverview
              clinicianReport={clinicianReport}
              clusters={clusters}
              compiledBodyOverview={narrativeReport?.body_overview}
              showPatternGroupBuckets={showDetails}
              sectionHeading="Your body overview"
            />
            <p className="text-sm text-slate-600 leading-relaxed max-w-3xl border-l-2 border-slate-200 pl-3">
              Sections below build on each other: what looks stable, your main finding and why it led, how confident we
              are, patterns across your body when available, marker evidence, and suggested follow-up.
            </p>
          </section>

          <section
            aria-labelledby="fe-r2-working-well-heading"
            data-testid={FE_R2_RESULTS_JOURNEY_SECTION_TEST_IDS[1]}
          >
            <h2 id="fe-r2-working-well-heading" className="sr-only">
              What&apos;s working well
            </h2>
            <BalancedSystemsSummary
              balanced={balancedSystems}
              sectionTitle="What's working well"
              initialVisibleCount={6}
              expandBeyondInitial
              maxItems={4}
            />
          </section>

          <div data-testid={FE_R2_RESULTS_JOURNEY_SECTION_TEST_IDS[2]}>
            <PrimaryFindingAndWhy
              report={clinicianReport}
              omitIntroDuplicate
              omitConfirmatoryInClarify={showConfirmatoryInNextSteps}
              leadPatternLabel={heroStory.heroTitle}
              showTechnicalDetail={showDetails}
            />
          </div>

          <section
            className="space-y-4"
            aria-labelledby="fe-r2-uncertainty-heading"
            data-testid={FE_R2_RESULTS_JOURNEY_SECTION_TEST_IDS[3]}
          >
            <h2 id="fe-r2-uncertainty-heading" className="sr-only">
              Why this lead won and uncertainty
            </h2>
            <WhyThisLeadWonSection report={clinicianReport} />
            <PipelineStatus
              dataQuality={clinicianReport?.data_quality}
              confirmatoryTests={confirmatoryTestsForJourney}
              hideConfirmatoryTests={showConfirmatoryInNextSteps}
              missingChapterLine={missingChapterLine}
            />
          </section>

          {showRetailIdlPatterns ? (
            <section
              className="space-y-4"
              aria-labelledby="fe-r5a-patterns-heading"
              data-testid={FE_R2_RESULTS_JOURNEY_SECTION_TEST_IDS[4]}
            >
              <h2 id="fe-r5a-patterns-heading" className="text-xl font-semibold text-gray-900">
                Patterns across your body
              </h2>
              <InterpretationPatternsSection
                bundle={currentAnalysis?.interpretation_display_layer_v1}
                embedInJourney
              />
            </section>
          ) : null}

          <section
            id={BIOMARKER_DIALS_SECTION_ID}
            className="space-y-4"
            aria-labelledby="biomarkers-heading"
            data-testid={FE_R2_RESULTS_JOURNEY_SECTION_TEST_IDS[5]}
          >
            <h2 id="biomarkers-heading" className="text-xl font-semibold text-gray-900">
              Marker-level evidence
            </h2>
            <p className="text-sm text-gray-600">
              Values and reference ranges from your uploaded panel. Expand a marker for brief context when available.
            </p>
            <ResultsDrivingSignals markers={topDriverMarkers} biomarkerSectionId={BIOMARKER_DIALS_SECTION_ID} />
            <BiomarkerDials biomarkers={biomarkerDialData} sectionTitle="All markers on this run" />
            <UploadedPanelFidelity rows={uploadPanelFidelityRows} />
          </section>

          <section
            className="space-y-4"
            aria-labelledby="fe-r2-next-steps-heading"
            data-testid={FE_R2_RESULTS_JOURNEY_SECTION_TEST_IDS[6]}
          >
            <h2 id="fe-r2-next-steps-heading" className="text-xl font-semibold text-gray-900">
              What to do next
            </h2>
            <NarrativeLongitudinalAndNextSteps
              narrative={narrativeReport}
              nextStepsParagraphs={narrativeNextStepsParagraphs}
            />
            {showConfirmatoryInNextSteps ? (
              <ConfirmatoryTestsNextSteps tests={confirmatoryTestsForJourney} />
            ) : null}
            <div className="space-y-4">
              <p className="text-sm text-slate-700">
                <Link
                  href="/actions"
                  className="font-semibold text-indigo-700 hover:text-indigo-900 underline-offset-2 hover:underline inline-flex items-center gap-1"
                >
                  Open Actions hub
                  <ArrowRight className="h-4 w-4" aria-hidden />
                </Link>
                <span className="text-slate-600">
                  {' '}
                  for the full set of follow-ups (up to eight) from your most recent completed analysis.
                </span>
              </p>
              <ResultsActionCardsBlock actions={actionCards} />
            </div>
          </section>

          <ResultsDisclosureSection
            title="Health domains"
            description="High-level domain scores — supplementary to the main journey above."
            data-testid="section-patterns-secondary"
            defaultOpen={false}
          >
            <Wave1DomainCards domains={currentAnalysis?.consumer_domain_scores} />
          </ResultsDisclosureSection>

          <ResultsDisclosureSection
            title="Additional interpretation context"
            description="Orientation helpers and longer narrative detail when you want more depth."
            data-testid="section-interpretation-context"
            defaultOpen={false}
          >
            <ResultsInvestigationSpine crossBodyPatternLabel={firstIdlRetailLabel} />
            <SystemUnderstandingSection
              balanced={balancedSystems}
              clusters={clusters}
              primaryDriver={primaryDriver}
              idlRetailLabel={firstIdlRetailLabel}
            />
            <NarrativeLeadAndSupportingSections narrative={narrativeReport} />
          </ResultsDisclosureSection>

          <ResultsDisclosureSection
            title="Clinician summary"
            description="Professional handoff, export-oriented synthesis, and technical detail for clinical review."
            data-testid={FE_R2_RESULTS_JOURNEY_SECTION_TEST_IDS[7]}
            defaultOpen={false}
          >
            <ClinicianReportRenderer
              report={clinicianReport}
              balancedSystems={balancedSystems}
              deterministicClinicianSynthesis={narrativeReport?.clinician_synthesis}
              showTechnicalDetail={showDetails}
            />
          </ResultsDisclosureSection>

          <ResultsDisclosureSection
            title="Advanced analysis"
            description="Overall score, system groups, optional narrative summaries, and extended technical views."
            data-testid="section-advanced"
            defaultOpen={false}
            onOpenChange={handleAdvancedOpen}
          >
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

            {consumerInsights.length > 0 ? (
              <Alert>
                <AlertDescription>
                  {consumerInsights.length} short narrative summar{consumerInsights.length === 1 ? 'y' : 'ies'}{' '}
                  available in the &quot;Narrative&quot; list below. These complement the clinical interpretation; they
                  are not the primary structured report.
                </AlertDescription>
              </Alert>
            ) : null}

            <div className="space-y-2">
              <h3 className="text-sm font-semibold text-slate-800">Clinical interpretation</h3>
              <InsightPanel
                report={clinicianReport}
                primaryDriverSystemGroupName={primaryDriver?.name ?? null}
                contextOnly
              />
            </div>

            <LayerCInsightSection bundle={layerCFeatures} />

            <section className="space-y-3" aria-labelledby="cluster-heading">
              <h2 id="cluster-heading" className="text-xl font-semibold text-gray-900">
                System groups
              </h2>
              <p className="text-sm text-gray-600">
                How your markers group into biological patterns. Names describe the pattern in plain language.
              </p>
              <ClusterSummary clusters={clusterSummaries} isLoading={clustersLoading} showDetails={showDetails} />
            </section>

            {showInsightsPanelSection ? (
              <div className="space-y-2">
                <h3 className="text-sm font-semibold text-slate-800">Narrative summaries</h3>
                <InsightsPanel insights={consumerInsights} narrativeRuntime={narrativeRuntime} />
              </div>
            ) : null}
          </ResultsDisclosureSection>
        </div>

        <div className="mt-10 flex justify-center gap-4">
          <Button onClick={handleNewAnalysis} variant="outline">
            Start New Analysis
          </Button>
          <Button onClick={handleExportResults}>
            <Download className="h-4 w-4 mr-2" />
            Export results
          </Button>
        </div>
      </div>
    </div>
  );
}
