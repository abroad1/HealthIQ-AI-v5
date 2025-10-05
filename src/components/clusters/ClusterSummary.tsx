'use client';

import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { 
  BarChart3, 
  TrendingUp, 
  AlertTriangle, 
  CheckCircle, 
  Info,
  ChevronDown,
  ChevronRight,
  Loader2
} from 'lucide-react';

interface Cluster {
  id: string;
  name: string;
  category: string;
  score: number;
  confidence: number;
  biomarkers: string[];
  description: string;
  recommendations: string[];
  severity: 'low' | 'moderate' | 'high' | 'critical';
  trend?: 'improving' | 'stable' | 'declining';
}

interface ClusterSummaryProps {
  clusters: Cluster[];
  isLoading?: boolean;
  showDetails?: boolean;
}

const CATEGORY_COLORS = {
  metabolic: 'bg-blue-100 text-blue-800 border-blue-200',
  cardiovascular: 'bg-red-100 text-red-800 border-red-200',
  inflammatory: 'bg-orange-100 text-orange-800 border-orange-200',
  organ: 'bg-green-100 text-green-800 border-green-200',
  cbc: 'bg-purple-100 text-purple-800 border-purple-200',
  hormonal: 'bg-pink-100 text-pink-800 border-pink-200',
  nutritional: 'bg-yellow-100 text-yellow-800 border-yellow-200'
};

const SEVERITY_COLORS = {
  low: 'text-green-600 bg-green-100',
  moderate: 'text-yellow-600 bg-yellow-100',
  high: 'text-orange-600 bg-orange-100',
  critical: 'text-red-600 bg-red-100'
};

const SEVERITY_ICONS = {
  low: <CheckCircle className="h-4 w-4" />,
  moderate: <Info className="h-4 w-4" />,
  high: <AlertTriangle className="h-4 w-4" />,
  critical: <AlertTriangle className="h-4 w-4" />
};

const TREND_COLORS = {
  improving: 'text-green-600',
  stable: 'text-blue-600',
  declining: 'text-red-600'
};

const TREND_ICONS = {
  improving: <TrendingUp className="h-4 w-4" />,
  stable: <BarChart3 className="h-4 w-4" />,
  declining: <TrendingUp className="h-4 w-4 transform rotate-180" />
};

const getScoreColor = (score: number) => {
  if (score >= 80) return 'text-green-600';
  if (score >= 60) return 'text-yellow-600';
  if (score >= 40) return 'text-orange-600';
  return 'text-red-600';
};

const getScoreBarColor = (score: number) => {
  if (score >= 80) return 'bg-green-500';
  if (score >= 60) return 'bg-yellow-500';
  if (score >= 40) return 'bg-orange-500';
  return 'bg-red-500';
};

export default function ClusterSummary({ clusters, isLoading = false, showDetails = false }: ClusterSummaryProps) {
  const [expandedClusters, setExpandedClusters] = useState<Set<string>>(new Set());
  const [selectedSeverity, setSelectedSeverity] = useState<string>('all');

  const toggleCluster = (clusterId: string) => {
    const newExpanded = new Set(expandedClusters);
    if (newExpanded.has(clusterId)) {
      newExpanded.delete(clusterId);
    } else {
      newExpanded.add(clusterId);
    }
    setExpandedClusters(newExpanded);
  };

  const filteredClusters = selectedSeverity === 'all' 
    ? clusters 
    : clusters.filter(cluster => cluster.severity === selectedSeverity);

  const severityCounts = clusters.reduce((acc, cluster) => {
    acc[cluster.severity] = (acc[cluster.severity] || 0) + 1;
    return acc;
  }, {} as Record<string, number>);

  const averageScore = clusters.length > 0 
    ? clusters.reduce((sum, cluster) => sum + cluster.score, 0) / clusters.length 
    : 0;

  if (isLoading) {
    return (
      <Card>
        <CardContent className="pt-6">
          <div className="flex items-center justify-center py-8">
            <Loader2 className="h-8 w-8 animate-spin text-blue-500 mr-3" />
            <span className="text-gray-600">Loading health clusters...</span>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (clusters.length === 0) {
    return (
      <Card>
        <CardContent className="pt-6">
          <div className="text-center py-8">
            <BarChart3 className="h-12 w-12 text-gray-300 mx-auto mb-4" />
            <p className="text-gray-500">No health clusters available.</p>
            <p className="text-sm text-gray-400">Complete an analysis to view your health cluster analysis.</p>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="space-y-6">
      {/* Summary Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="pt-4">
            <div className="text-center">
              <div className="text-2xl font-bold text-gray-900">{clusters.length}</div>
              <div className="text-sm text-gray-500">Health Clusters</div>
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardContent className="pt-4">
            <div className="text-center">
              <div className={`text-2xl font-bold ${getScoreColor(averageScore)}`}>
                {Math.round(averageScore)}
              </div>
              <div className="text-sm text-gray-500">Average Score</div>
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardContent className="pt-4">
            <div className="text-center">
              <div className="text-2xl font-bold text-red-600">
                {severityCounts.critical || 0}
              </div>
              <div className="text-sm text-gray-500">Critical Issues</div>
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardContent className="pt-4">
            <div className="text-center">
              <div className="text-2xl font-bold text-yellow-600">
                {severityCounts.high || 0}
              </div>
              <div className="text-sm text-gray-500">High Priority</div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Filters */}
      <Card>
        <CardContent className="pt-4">
          <div className="flex items-center gap-4 mb-4">
            <span className="text-sm font-medium text-gray-700">Filter by severity:</span>
            <div className="flex gap-2">
              <Button
                variant={selectedSeverity === 'all' ? 'default' : 'outline'}
                size="sm"
                onClick={() => setSelectedSeverity('all')}
              >
                All ({clusters.length})
              </Button>
              <Button
                variant={selectedSeverity === 'critical' ? 'default' : 'outline'}
                size="sm"
                onClick={() => setSelectedSeverity('critical')}
                className="text-red-600 border-red-200 hover:bg-red-50"
              >
                Critical ({severityCounts.critical || 0})
              </Button>
              <Button
                variant={selectedSeverity === 'high' ? 'default' : 'outline'}
                size="sm"
                onClick={() => setSelectedSeverity('high')}
                className="text-orange-600 border-orange-200 hover:bg-orange-50"
              >
                High ({severityCounts.high || 0})
              </Button>
              <Button
                variant={selectedSeverity === 'moderate' ? 'default' : 'outline'}
                size="sm"
                onClick={() => setSelectedSeverity('moderate')}
                className="text-yellow-600 border-yellow-200 hover:bg-yellow-50"
              >
                Moderate ({severityCounts.moderate || 0})
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Clusters List */}
      <div className="space-y-4">
        {filteredClusters.map((cluster) => (
          <Card key={cluster.id} className="hover:shadow-md transition-shadow">
            <CardContent className="pt-4">
              <div className="flex items-start justify-between mb-4">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <h3 className="text-lg font-semibold text-gray-900">
                      {cluster.name}
                    </h3>
                    <Badge className={SEVERITY_COLORS[cluster.severity]}>
                      {SEVERITY_ICONS[cluster.severity]}
                      <span className="ml-1 capitalize">{cluster.severity}</span>
                    </Badge>
                    {cluster.trend && (
                      <Badge variant="outline" className={TREND_COLORS[cluster.trend]}>
                        {TREND_ICONS[cluster.trend]}
                        <span className="ml-1 capitalize">{cluster.trend}</span>
                      </Badge>
                    )}
                  </div>
                  
                  <p className="text-gray-600 text-sm mb-3">
                    {cluster.description}
                  </p>
                  
                  <div className="flex items-center gap-4 text-sm">
                    <div className="flex items-center gap-2">
                      <span className="text-gray-500">Score:</span>
                      <span className={`font-semibold ${getScoreColor(cluster.score)}`}>
                        {Math.round(cluster.score)}/100
                      </span>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="text-gray-500">Confidence:</span>
                      <span className="font-semibold text-blue-600">
                        {Math.round(cluster.confidence * 100)}%
                      </span>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="text-gray-500">Biomarkers:</span>
                      <span className="font-semibold text-gray-700">
                        {cluster.biomarkers.length}
                      </span>
                    </div>
                  </div>
                </div>
                
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => toggleCluster(cluster.id)}
                >
                  {expandedClusters.has(cluster.id) ? (
                    <ChevronDown className="h-4 w-4" />
                  ) : (
                    <ChevronRight className="h-4 w-4" />
                  )}
                </Button>
              </div>

              {/* Score Bar */}
              <div className="mb-4">
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    className={`h-2 rounded-full transition-all duration-1000 ${getScoreBarColor(cluster.score)}`}
                    style={{ width: `${cluster.score}%` }}
                  ></div>
                </div>
              </div>

              {/* Expanded Details */}
              {expandedClusters.has(cluster.id) && (
                <div className="border-t border-gray-100 pt-4 space-y-4">
                  {/* Biomarkers */}
                  <div>
                    <h4 className="text-sm font-semibold text-gray-700 mb-2">Biomarkers Analyzed</h4>
                    <div className="flex flex-wrap gap-2">
                      {cluster.biomarkers.map((biomarker) => (
                        <Badge 
                          key={biomarker} 
                          variant="outline"
                          className="text-xs"
                        >
                          {biomarker.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                        </Badge>
                      ))}
                    </div>
                  </div>

                  {/* Recommendations */}
                  {cluster.recommendations && cluster.recommendations.length > 0 && (
                    <div>
                      <h4 className="text-sm font-semibold text-gray-700 mb-2">Recommendations</h4>
                      <ul className="space-y-1">
                        {cluster.recommendations.map((recommendation, index) => (
                          <li key={index} className="text-sm text-gray-600 flex items-start gap-2">
                            <span className="text-blue-500 mt-1">•</span>
                            <span>{recommendation}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {/* Category */}
                  <div>
                    <h4 className="text-sm font-semibold text-gray-700 mb-2">Category</h4>
                    <Badge 
                      className={CATEGORY_COLORS[cluster.category as keyof typeof CATEGORY_COLORS] || 'bg-gray-100 text-gray-800'}
                    >
                      {cluster.category.replace(/([A-Z])/g, ' $1').trim()}
                    </Badge>
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        ))}
      </div>

      {/* No Results Message */}
      {filteredClusters.length === 0 && selectedSeverity !== 'all' && (
        <Card>
          <CardContent className="pt-6">
            <div className="text-center py-8">
              <Info className="h-12 w-12 text-gray-300 mx-auto mb-4" />
              <p className="text-gray-500">No clusters found for the selected severity level.</p>
              <Button 
                variant="outline" 
                onClick={() => setSelectedSeverity('all')}
                className="mt-2"
              >
                Show All Clusters
              </Button>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
