"use client";

import React from 'react';
import { Card } from '@/components/ui/card';

interface Insight {
  id: string;
  insight_id?: string;
  category?: string;
  summary?: string;
  severity?: string;
  confidence?: number;
  recommendations?: string[];
  biomarkers_involved?: string[];
  source?: string;
}

interface InsightPanelProps {
  insights?: Insight[];
  className?: string;
}

export default function InsightPanel({ insights, className = '' }: InsightPanelProps) {
  return (
    <div className={`space-y-4 ${className}`}>
      <h3 className="text-lg font-semibold text-gray-900">Modular Insights</h3>
      
      {insights?.length ? (
        insights.map((insight, index) => (
          <Card key={insight.id || insight.insight_id || index} className="mb-2 p-3">
            <div className="space-y-2">
              <p className="font-semibold text-gray-900">
                {insight.insight_id || insight.id || `Insight ${index + 1}`}
              </p>
              
              <div className="flex items-center gap-2">
                <span className="text-sm text-gray-600">Severity:</span>
                <span className={`text-sm font-medium px-2 py-1 rounded ${
                  insight.severity === 'critical' ? 'bg-red-100 text-red-800' :
                  insight.severity === 'warning' ? 'bg-yellow-100 text-yellow-800' :
                  insight.severity === 'high' ? 'bg-orange-100 text-orange-800' :
                  insight.severity === 'moderate' ? 'bg-blue-100 text-blue-800' :
                  insight.severity === 'mild' ? 'bg-green-100 text-green-800' :
                  'bg-gray-100 text-gray-800'
                }`}>
                  {insight.severity || "unknown"}
                </span>
              </div>

              {insight.confidence !== undefined && (
                <div className="flex items-center gap-2">
                  <span className="text-sm text-gray-600">Confidence:</span>
                  <span className="text-sm font-medium">
                    {Math.round(insight.confidence * 100)}%
                  </span>
                </div>
              )}

              {insight.category && (
                <div className="flex items-center gap-2">
                  <span className="text-sm text-gray-600">Category:</span>
                  <span className="text-sm font-medium">{insight.category}</span>
                </div>
              )}

              {insight.source && (
                <div className="flex items-center gap-2">
                  <span className="text-sm text-gray-600">Source:</span>
                  <span className="text-sm font-medium">{insight.source}</span>
                </div>
              )}

              {insight.recommendations?.length ? (
                <div className="space-y-1">
                  <p className="text-sm font-medium text-gray-700">Recommendations:</p>
                  <ul className="list-disc list-inside text-sm text-gray-600 space-y-1">
                    {insight.recommendations.map((rec, idx) => (
                      <li key={idx}>{rec}</li>
                    ))}
                  </ul>
                </div>
              ) : (
                <p className="text-sm italic text-gray-500">No recommendations available.</p>
              )}

              {insight.biomarkers_involved?.length && (
                <div className="space-y-1">
                  <p className="text-sm font-medium text-gray-700">Biomarkers:</p>
                  <div className="flex flex-wrap gap-1">
                    {insight.biomarkers_involved.map((biomarker, idx) => (
                      <span key={idx} className="text-xs bg-gray-100 text-gray-700 px-2 py-1 rounded">
                        {biomarker}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </Card>
        ))
      ) : (
        <Card className="p-4">
          <p className="text-sm italic text-gray-500">
            No insights detected yet. Run an analysis to generate results.
          </p>
        </Card>
      )}
    </div>
  );
}
