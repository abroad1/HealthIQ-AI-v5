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
  EyeOff
} from 'lucide-react';
import { useAnalysisStore } from '../state/analysisStore';
import { useClusterStore } from '../state/clusterStore';
import { InsightsPanel } from '@/components/insights/InsightsPanel';
import BiomarkerDials from '@/components/biomarkers/BiomarkerDials';
import ClusterSummary from '@/components/clusters/ClusterSummary';
import { useRouter } from 'next/navigation';

export default function ResultsPage() {
  const { 
    currentAnalysis, 
    isLoading: isAnalyzing, 
    error: analysisError, 
    retryAnalysis,
    clearAnalysis 
  } = useAnalysisStore();
  
  const { 
    clusters, 
    isLoading: clustersLoading,
    loadClusters 
  } = useClusterStore();
  
  const [activeTab, setActiveTab] = useState('overview');
  const [showDetails, setShowDetails] = useState(false);
  const router = useRouter();

  useEffect(() => {
    // If no analysis data, redirect to upload
    if (!currentAnalysis && !isAnalyzing) {
      router.push('/upload');
      return;
    }

    // Fetch clusters if we have analysis data
    if (currentAnalysis && !clusters.length && !clustersLoading) {
      loadClusters(currentAnalysis.analysis_id);
    }
  }, [currentAnalysis, isAnalyzing, clusters.length, clustersLoading, loadClusters, router]);

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
    const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr);
    
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
        url: window.location.href
      });
    } else {
      // Fallback: copy to clipboard
      navigator.clipboard.writeText(window.location.href);
      // You could add a toast notification here
    }
  };

  if (isAnalyzing) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <Card className="w-full max-w-md">
          <CardContent className="pt-6">
            <div className="text-center">
              <RefreshCw className="h-16 w-16 text-blue-500 mx-auto mb-4 animate-spin" />
              <h2 className="text-2xl font-bold text-gray-900 mb-2">Analyzing Your Data</h2>
              <p className="text-gray-600 mb-4">
                Our AI is processing your biomarker data and generating personalized insights. This may take a few moments.
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
              <p className="text-gray-600 mb-4">
                {analysisError?.message || 'An unknown error occurred'}
              </p>
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
              <p className="text-gray-600 mb-4">
                Please complete an analysis first.
              </p>
              <Button onClick={handleNewAnalysis} className="w-full">
                Start New Analysis
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  const { results, created_at, completed_at } = currentAnalysis;
  const insights = results?.insights || [];
  const metadata = {
    analysisId: currentAnalysis.analysis_id,
    completedAt: completed_at,
    biomarkerCount: results?.biomarkers?.length || 0,
    confidence: 0.85 // This would need to be calculated from actual data
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="container mx-auto px-4 max-w-7xl">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h1 className="text-4xl font-bold text-gray-900 mb-2">
                Your Health Analysis Results
              </h1>
              <p className="text-lg text-gray-600">
                AI-powered insights from your biomarker data
              </p>
            </div>
            <div className="flex items-center gap-2">
              <Button
                variant="outline"
                size="sm"
                onClick={() => setShowDetails(!showDetails)}
              >
                {showDetails ? <EyeOff className="h-4 w-4 mr-2" /> : <Eye className="h-4 w-4 mr-2" />}
                {showDetails ? 'Hide Details' : 'Show Details'}
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={handleExportResults}
              >
                <Download className="h-4 w-4 mr-2" />
                Export
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={handleShareResults}
              >
                <Share2 className="h-4 w-4 mr-2" />
                Share
              </Button>
            </div>
          </div>

          {/* Analysis Metadata */}
          <Card className="mb-6">
            <CardContent className="pt-4">
              <div className="grid grid-cols-1 md:grid-cols-4 gap-4 text-sm">
                <div>
                  <span className="text-gray-500">Analysis ID:</span>
                  <p className="font-mono text-xs">{metadata?.analysisId || 'N/A'}</p>
                </div>
                <div>
                  <span className="text-gray-500">Completed:</span>
                  <p>{metadata?.completedAt ? new Date(metadata.completedAt).toLocaleString() : 'N/A'}</p>
                </div>
                <div>
                  <span className="text-gray-500">Biomarkers:</span>
                  <p>{metadata?.biomarkerCount || 0} analyzed</p>
                </div>
                <div>
                  <span className="text-gray-500">Confidence:</span>
                  <p>{metadata?.confidence ? `${Math.round(metadata.confidence * 100)}%` : 'N/A'}</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Main Content Tabs */}
        <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
          <TabsList className="grid w-full grid-cols-4 mb-8">
            <TabsTrigger value="overview" className="flex items-center gap-2">
              <BarChart3 className="h-4 w-4" />
              Overview
            </TabsTrigger>
            <TabsTrigger value="biomarkers" className="flex items-center gap-2">
              <TrendingUp className="h-4 w-4" />
              Biomarkers
            </TabsTrigger>
            <TabsTrigger value="clusters" className="flex items-center gap-2">
              <BarChart3 className="h-4 w-4" />
              Health Clusters
            </TabsTrigger>
            <TabsTrigger value="insights" className="flex items-center gap-2">
              <TrendingUp className="h-4 w-4" />
              AI Insights
            </TabsTrigger>
          </TabsList>

          <TabsContent value="overview" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Health Score Summary */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <CheckCircle className="h-5 w-5 text-green-500" />
                    Overall Health Score
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-center">
                    <div className="text-6xl font-bold text-green-600 mb-2">
                      {results?.overall_score ? Math.round(results.overall_score) : 'N/A'}
                    </div>
                    <p className="text-gray-600">out of 100</p>
                    <div className="mt-4">
                      <div className="w-full bg-gray-200 rounded-full h-3">
                        <div 
                          className="bg-green-500 h-3 rounded-full transition-all duration-1000"
                          style={{ width: `${results?.overall_score || 0}%` }}
                        ></div>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Key Metrics */}
              <Card>
                <CardHeader>
                  <CardTitle>Key Health Metrics</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {results?.risk_assessment && Object.entries(results.risk_assessment).map(([category, score]) => (
                      <div key={category} className="flex justify-between items-center">
                        <span className="capitalize text-sm font-medium">
                          {category.replace(/([A-Z])/g, ' $1').trim()}
                        </span>
                        <div className="flex items-center gap-2">
                          <div className="w-20 bg-gray-200 rounded-full h-2">
                            <div 
                              className="bg-blue-500 h-2 rounded-full"
                              style={{ width: `${score}%` }}
                            ></div>
                          </div>
                          <span className="text-sm font-semibold w-8">{Math.round(score)}</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Quick Insights */}
            {insights && insights.length > 0 && (
              <Card>
                <CardHeader>
                  <CardTitle>Quick Insights</CardTitle>
                  <CardDescription>
                    Key findings from your analysis
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {insights.slice(0, 6).map((insight, index) => (
                      <div key={index} className="p-4 border rounded-lg">
                        <div className="flex items-start gap-2">
                          <div className={`w-2 h-2 rounded-full mt-2 ${
                            insight.severity === 'critical' ? 'bg-red-500' :
                            insight.severity === 'warning' ? 'bg-yellow-500' : 'bg-blue-500'
                          }`}></div>
                          <div>
                            <p className="text-sm font-medium text-gray-900 mb-1">
                              {insight.category?.replace(/([A-Z])/g, ' $1').trim()}
                            </p>
                            <p className="text-xs text-gray-600 line-clamp-2">
                              {insight.summary}
                            </p>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            )}
          </TabsContent>

          <TabsContent value="biomarkers" className="space-y-6">
            <BiomarkerDials 
              biomarkers={results?.biomarkers?.reduce((acc, biomarker) => {
                acc[biomarker.biomarker_name] = {
                  value: biomarker.value,
                  unit: biomarker.unit,
                  status: biomarker.status,
                  referenceRange: biomarker.reference_range ? {
                    min: biomarker.reference_range.min,
                    max: biomarker.reference_range.max,
                    unit: biomarker.reference_range.unit
                  } : undefined,
                  date: created_at
                };
                return acc;
              }, {} as Record<string, any>) || {}} 
              showDetails={showDetails}
            />
          </TabsContent>

          <TabsContent value="clusters" className="space-y-6">
            <ClusterSummary 
              clusters={clusters.map(cluster => ({
                id: cluster.id,
                name: cluster.name,
                category: cluster.category,
                score: cluster.score,
                confidence: 0.85, // Default confidence
                biomarkers: cluster.biomarkers,
                description: cluster.description,
                recommendations: cluster.recommendations,
                severity: cluster.risk_level === 'low' ? 'low' : 
                         cluster.risk_level === 'medium' ? 'moderate' :
                         cluster.risk_level === 'high' ? 'high' : 'critical',
                trend: 'stable' as const
              }))} 
              isLoading={clustersLoading}
              showDetails={showDetails}
            />
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
                    <p className="text-sm text-gray-400">Complete your analysis to generate personalized insights.</p>
                  </div>
                </CardContent>
              </Card>
            )}
          </TabsContent>
        </Tabs>

        {/* Action Buttons */}
        <div className="mt-8 flex justify-center gap-4">
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
