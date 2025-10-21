"use client";

import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { AlertTriangle, Info, CheckCircle, XCircle } from 'lucide-react';

export interface Insight {
  id: string;
  category: string;
  summary?: string;
  description?: string;
  evidence?: Record<string, any>;
  confidence?: number;
  severity?: 'info' | 'warning' | 'critical';
  recommendations?: string[];
  biomarkers_involved?: string[];
  lifestyle_factors?: string[];
  created_at?: string;
}

interface InsightCardProps {
  insight: Insight;
  className?: string;
}

const severityConfig = {
  info: {
    icon: Info,
    color: 'bg-blue-100 text-blue-800',
    borderColor: 'border-blue-200',
    bgColor: 'bg-blue-50'
  },
  warning: {
    icon: AlertTriangle,
    color: 'bg-yellow-100 text-yellow-800',
    borderColor: 'border-yellow-200',
    bgColor: 'bg-yellow-50'
  },
  critical: {
    icon: XCircle,
    color: 'bg-red-100 text-red-800',
    borderColor: 'border-red-200',
    bgColor: 'bg-red-50'
  }
};

const categoryColors = {
  metabolic: 'bg-green-100 text-green-800',
  cardiovascular: 'bg-red-100 text-red-800',
  inflammatory: 'bg-orange-100 text-orange-800',
  organ: 'bg-purple-100 text-purple-800',
  nutritional: 'bg-blue-100 text-blue-800',
  hormonal: 'bg-pink-100 text-pink-800'
};

export function InsightCard({ insight, className = '' }: InsightCardProps) {

  // Null-safe array reads
  const recs = insight?.recommendations ?? [];
  const biomarkers = insight?.biomarkers_involved ?? [];
  const lifestyleFactors = insight?.lifestyle_factors ?? [];
  const desc = insight?.description ?? '';
  const summary = insight?.summary ?? '';
  const confidence = insight?.confidence ?? 0;
  const severity = insight?.severity ?? 'info';
  const evidence = insight?.evidence ?? {};
  const created_at = insight?.created_at ?? new Date().toISOString();

  const severityConfig_item = severityConfig[severity];
  const SeverityIcon = severityConfig_item.icon;
  const categoryColor = categoryColors[insight?.category as keyof typeof categoryColors] || 'bg-gray-100 text-gray-800';

  const formatConfidence = (confidence: number) => {
    return Math.round(confidence * 100);
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  return (
    <Card className={`${className} ${severityConfig_item.borderColor} ${severityConfig_item.bgColor}`}>
      <CardHeader className="pb-3">
        <div className="flex items-start justify-between">
          <div className="flex items-center gap-2">
            <SeverityIcon className="h-5 w-5 text-gray-600" />
            <CardTitle className="text-lg font-semibold text-gray-900">
              {summary}
            </CardTitle>
          </div>
          <div className="flex flex-col items-end gap-2">
            <Badge className={categoryColor}>
              {insight?.category}
            </Badge>
            <Badge className={severityConfig_item.color}>
              {severity}
            </Badge>
          </div>
        </div>
      </CardHeader>

      <CardContent className="space-y-4">
        {/* Confidence Score */}
        <div className="space-y-2">
          <div className="flex items-center justify-between text-sm">
            <span className="font-medium text-gray-700">Confidence</span>
            <span className="text-gray-600">{formatConfidence(confidence)}%</span>
          </div>
          <Progress 
            value={confidence * 100} 
            className="h-2"
          />
        </div>

        {/* Biomarkers Involved */}
        {(biomarkers?.length ?? 0) > 0 && (
          <div className="space-y-2">
            <h4 className="text-sm font-medium text-gray-700">Biomarkers Involved</h4>
            <div className="flex flex-wrap gap-1">
              {biomarkers.map((biomarker) => (
                <Badge key={biomarker} variant="outline" className="text-xs">
                  {biomarker}
                </Badge>
              ))}
            </div>
          </div>
        )}

        {/* Lifestyle Factors */}
        {(lifestyleFactors?.length ?? 0) > 0 && (
          <div className="space-y-2">
            <h4 className="text-sm font-medium text-gray-700">Lifestyle Factors</h4>
            <div className="flex flex-wrap gap-1">
              {lifestyleFactors.map((factor) => (
                <Badge key={factor} variant="secondary" className="text-xs">
                  {factor}
                </Badge>
              ))}
            </div>
          </div>
        )}

        {/* Recommendations */}
        {(recs?.length ?? 0) > 0 && (
          <div className="space-y-2">
            <h4 className="text-sm font-medium text-gray-700">Recommendations</h4>
            <ul className="space-y-1">
              {recs.map((recommendation, index) => (
                <li key={index} className="flex items-start gap-2 text-sm text-gray-600">
                  <CheckCircle className="h-4 w-4 text-green-500 mt-0.5 flex-shrink-0" />
                  <span>{recommendation}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Evidence Summary */}
        {evidence && Object.keys(evidence).length > 0 && (
          <div className="space-y-2">
            <h4 className="text-sm font-medium text-gray-700">Evidence Summary</h4>
            <div className="text-sm text-gray-600 bg-white p-3 rounded-md border">
              <pre className="whitespace-pre-wrap text-xs">
                {JSON.stringify(evidence, null, 2)}
              </pre>
            </div>
          </div>
        )}

        {/* Footer */}
        <div className="pt-2 border-t border-gray-200">
          <div className="flex items-center justify-between text-xs text-gray-500">
            <span>Generated on {formatDate(created_at)}</span>
            <span>ID: {insight?.id}</span>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
