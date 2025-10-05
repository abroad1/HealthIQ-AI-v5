"use client";

import React, { useState } from 'react';

interface ClusterData {
  cluster_id: string;
  name: string;
  biomarkers: string[];
  description: string;
  severity: string;
  confidence: number;
}

interface ClusterInsightPanelProps {
  clusters: ClusterData[];
  biomarkerScores?: Record<string, number>;
  className?: string;
}

const ClusterInsightPanel: React.FC<ClusterInsightPanelProps> = ({
  clusters,
  biomarkerScores = {},
  className = ""
}) => {
  const [selectedCluster, setSelectedCluster] = useState<string | null>(null);

  // Get severity styling
  const getSeverityStyle = (severity: string) => {
    const styles = {
      critical: {
        bg: 'bg-red-50',
        border: 'border-red-200',
        text: 'text-red-800',
        badge: 'bg-red-100 text-red-800',
        icon: '🔴'
      },
      high: {
        bg: 'bg-orange-50',
        border: 'border-orange-200',
        text: 'text-orange-800',
        badge: 'bg-orange-100 text-orange-800',
        icon: '🟠'
      },
      moderate: {
        bg: 'bg-yellow-50',
        border: 'border-yellow-200',
        text: 'text-yellow-800',
        badge: 'bg-yellow-100 text-yellow-800',
        icon: '🟡'
      },
      mild: {
        bg: 'bg-blue-50',
        border: 'border-blue-200',
        text: 'text-blue-800',
        badge: 'bg-blue-100 text-blue-800',
        icon: '🔵'
      },
      normal: {
        bg: 'bg-green-50',
        border: 'border-green-200',
        text: 'text-green-800',
        badge: 'bg-green-100 text-green-800',
        icon: '🟢'
      }
    };
    return styles[severity as keyof typeof styles] || styles.normal;
  };

  // Get confidence level
  const getConfidenceLevel = (confidence: number) => {
    if (confidence >= 0.8) return { level: 'High', color: 'text-green-600' };
    if (confidence >= 0.6) return { level: 'Medium', color: 'text-yellow-600' };
    return { level: 'Low', color: 'text-red-600' };
  };

  // Get biomarker insights
  const getBiomarkerInsights = (biomarkers: string[]) => {
    return biomarkers.map(biomarker => {
      const score = biomarkerScores[biomarker] || 0;
      return {
        name: biomarker,
        score,
        status: score >= 80 ? 'optimal' : score >= 60 ? 'good' : score >= 40 ? 'moderate' : 'needs_attention'
      };
    });
  };

  // Get clinical recommendations
  const getClinicalRecommendations = (cluster: ClusterData) => {
    const recommendations = [];
    
    if (cluster.severity === 'critical' || cluster.severity === 'high') {
      recommendations.push('Immediate medical attention recommended');
    }
    
    if (cluster.confidence < 0.6) {
      recommendations.push('Additional testing may be needed for accurate assessment');
    }
    
    // Add specific recommendations based on cluster type
    if (cluster.name.toLowerCase().includes('metabolic')) {
      recommendations.push('Consider lifestyle modifications for metabolic health');
      recommendations.push('Monitor blood glucose levels regularly');
    }
    
    if (cluster.name.toLowerCase().includes('cardiovascular')) {
      recommendations.push('Focus on heart-healthy diet and exercise');
      recommendations.push('Regular cardiovascular monitoring recommended');
    }
    
    if (cluster.name.toLowerCase().includes('inflammatory')) {
      recommendations.push('Anti-inflammatory lifestyle modifications may help');
      recommendations.push('Consider stress management techniques');
    }
    
    if (cluster.name.toLowerCase().includes('nutritional')) {
      recommendations.push('Nutritional supplementation may be beneficial');
      recommendations.push('Consult with a nutritionist for dietary guidance');
    }
    
    return recommendations;
  };

  const selectedClusterData = selectedCluster 
    ? clusters.find(c => c.cluster_id === selectedCluster)
    : clusters[0];

  if (clusters.length === 0) {
    return (
      <div className={`bg-white rounded-lg border border-gray-200 p-6 ${className}`}>
        <div className="text-center text-gray-500">
          <div className="text-lg font-medium mb-2">No Clusters Available</div>
          <div className="text-sm">Run biomarker analysis to generate cluster insights</div>
        </div>
      </div>
    );
  }

  return (
    <div className={`bg-white rounded-lg border border-gray-200 ${className}`}>
      {/* Header */}
      <div className="p-4 border-b border-gray-200">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-lg font-semibold text-gray-900">Cluster Insights</h3>
            <p className="text-sm text-gray-600">
              Detailed analysis of biomarker clusters
            </p>
          </div>
          <div className="text-sm text-gray-500">
            {clusters.length} cluster{clusters.length !== 1 ? 's' : ''}
          </div>
        </div>
      </div>

      {/* Cluster Selection */}
      {clusters.length > 1 && (
        <div className="p-4 border-b border-gray-200">
          <div className="flex flex-wrap gap-2">
            {clusters.map((cluster) => {
              const severityStyle = getSeverityStyle(cluster.severity);
              return (
                <button
                  key={cluster.cluster_id}
                  onClick={() => setSelectedCluster(cluster.cluster_id)}
                  className={`px-3 py-1 rounded-full text-sm font-medium transition-colors ${
                    selectedCluster === cluster.cluster_id
                      ? severityStyle.badge
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  {cluster.name}
                </button>
              );
            })}
          </div>
        </div>
      )}

      {/* Selected Cluster Details */}
      {selectedClusterData && (
        <div className="p-6">
          {/* Cluster Overview */}
          <div className={`rounded-lg p-4 mb-6 ${getSeverityStyle(selectedClusterData.severity).bg} ${getSeverityStyle(selectedClusterData.severity).border} border`}>
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-2">
                  <span className="text-xl">{getSeverityStyle(selectedClusterData.severity).icon}</span>
                  <h4 className={`text-lg font-semibold ${getSeverityStyle(selectedClusterData.severity).text}`}>
                    {selectedClusterData.name}
                  </h4>
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${getSeverityStyle(selectedClusterData.severity).badge}`}>
                    {selectedClusterData.severity.toUpperCase()}
                  </span>
                </div>
                <p className={`text-sm ${getSeverityStyle(selectedClusterData.severity).text} mb-3`}>
                  {selectedClusterData.description}
                </p>
                <div className="flex items-center gap-4 text-sm">
                  <div>
                    <span className="font-medium">Confidence: </span>
                    <span className={getConfidenceLevel(selectedClusterData.confidence).color}>
                      {getConfidenceLevel(selectedClusterData.confidence).level} ({Math.round(selectedClusterData.confidence * 100)}%)
                    </span>
                  </div>
                  <div>
                    <span className="font-medium">Biomarkers: </span>
                    <span className="text-gray-600">{selectedClusterData.biomarkers.length}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Biomarker Details */}
          <div className="mb-6">
            <h5 className="text-md font-semibold text-gray-900 mb-3">Biomarker Analysis</h5>
            <div className="grid gap-3">
              {getBiomarkerInsights(selectedClusterData.biomarkers).map((biomarker) => (
                <div key={biomarker.name} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div className="flex items-center gap-3">
                    <div className="w-2 h-2 rounded-full bg-gray-400"></div>
                    <span className="font-medium text-gray-900 capitalize">
                      {biomarker.name.replace(/_/g, ' ')}
                    </span>
                  </div>
                  <div className="flex items-center gap-2">
                    <div className="text-sm text-gray-600">
                      Score: {biomarker.score.toFixed(1)}
                    </div>
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                      biomarker.status === 'optimal' ? 'bg-green-100 text-green-800' :
                      biomarker.status === 'good' ? 'bg-blue-100 text-blue-800' :
                      biomarker.status === 'moderate' ? 'bg-yellow-100 text-yellow-800' :
                      'bg-red-100 text-red-800'
                    }`}>
                      {biomarker.status.replace('_', ' ')}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Clinical Recommendations */}
          <div>
            <h5 className="text-md font-semibold text-gray-900 mb-3">Clinical Recommendations</h5>
            <div className="space-y-2">
              {getClinicalRecommendations(selectedClusterData).map((recommendation, index) => (
                <div key={index} className="flex items-start gap-3 p-3 bg-blue-50 rounded-lg">
                  <div className="w-5 h-5 rounded-full bg-blue-200 flex items-center justify-center flex-shrink-0 mt-0.5">
                    <span className="text-xs text-blue-800">•</span>
                  </div>
                  <p className="text-sm text-blue-800">{recommendation}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ClusterInsightPanel;
