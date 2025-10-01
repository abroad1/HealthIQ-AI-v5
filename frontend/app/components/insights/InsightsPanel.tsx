"use client";

import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from '@/components/ui/collapsible';
import { ChevronDown, ChevronRight, Filter, BarChart3, TrendingUp } from 'lucide-react';
import { InsightCard, Insight } from './InsightCard';

interface InsightsPanelProps {
  insights: Insight[];
  className?: string;
}

const categoryLabels = {
  metabolic: 'Metabolic Health',
  cardiovascular: 'Cardiovascular Health',
  inflammatory: 'Inflammatory Health',
  organ: 'Organ Health',
  nutritional: 'Nutritional Health',
  hormonal: 'Hormonal Health'
};

const severityOrder = {
  critical: 3,
  warning: 2,
  info: 1
};

export function InsightsPanel({ insights, className = '' }: InsightsPanelProps) {
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [selectedSeverity, setSelectedSeverity] = useState<string>('all');
  const [expandedCategories, setExpandedCategories] = useState<Set<string>>(new Set());

  // Group insights by category
  const insightsByCategory = insights.reduce((acc, insight) => {
    if (!acc[insight.category]) {
      acc[insight.category] = [];
    }
    acc[insight.category].push(insight);
    return acc;
  }, {} as Record<string, Insight[]>);

  // Sort insights within each category by severity and confidence
  Object.keys(insightsByCategory).forEach(category => {
    insightsByCategory[category].sort((a, b) => {
      const severityDiff = severityOrder[b.severity] - severityOrder[a.severity];
      if (severityDiff !== 0) return severityDiff;
      return b.confidence - a.confidence;
    });
  });

  // Filter insights based on selected filters
  const filteredInsights = insights.filter(insight => {
    const categoryMatch = selectedCategory === 'all' || insight.category === selectedCategory;
    const severityMatch = selectedSeverity === 'all' || insight.severity === selectedSeverity;
    return categoryMatch && severityMatch;
  });

  // Get unique categories and severities for filters
  const categories = Array.from(new Set(insights.map(i => i.category)));
  const severities = Array.from(new Set(insights.map(i => i.severity)));

  // Calculate summary statistics
  const totalInsights = insights.length;
  const criticalInsights = insights.filter(i => i.severity === 'critical').length;
  const warningInsights = insights.filter(i => i.severity === 'warning').length;
  const averageConfidence = insights.reduce((sum, i) => sum + i.confidence, 0) / totalInsights || 0;

  const toggleCategory = (category: string) => {
    const newExpanded = new Set(expandedCategories);
    if (newExpanded.has(category)) {
      newExpanded.delete(category);
    } else {
      newExpanded.add(category);
    }
    setExpandedCategories(newExpanded);
  };

  const clearFilters = () => {
    setSelectedCategory('all');
    setSelectedSeverity('all');
  };

  if (totalInsights === 0) {
    return (
      <Card className={className}>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <BarChart3 className="h-5 w-5" />
            Health Insights
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-center py-8 text-gray-500">
            <TrendingUp className="h-12 w-12 mx-auto mb-4 text-gray-300" />
            <p>No insights available yet.</p>
            <p className="text-sm">Complete your biomarker analysis to generate personalized health insights.</p>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className={className}>
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="flex items-center gap-2">
            <BarChart3 className="h-5 w-5" />
            Health Insights
          </CardTitle>
          <div className="flex items-center gap-2">
            <Badge variant="outline" className="text-sm">
              {totalInsights} insights
            </Badge>
            {criticalInsights > 0 && (
              <Badge variant="destructive" className="text-sm">
                {criticalInsights} critical
              </Badge>
            )}
          </div>
        </div>

        {/* Summary Statistics */}
        <div className="grid grid-cols-3 gap-4 pt-4">
          <div className="text-center">
            <div className="text-2xl font-bold text-gray-900">{totalInsights}</div>
            <div className="text-sm text-gray-500">Total Insights</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-red-600">{criticalInsights + warningInsights}</div>
            <div className="text-sm text-gray-500">Need Attention</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-blue-600">{Math.round(averageConfidence * 100)}%</div>
            <div className="text-sm text-gray-500">Avg Confidence</div>
          </div>
        </div>
      </CardHeader>

      <CardContent className="space-y-6">
        {/* Filters */}
        <div className="flex flex-wrap gap-4 items-center">
          <div className="flex items-center gap-2">
            <Filter className="h-4 w-4 text-gray-500" />
            <span className="text-sm font-medium text-gray-700">Filters:</span>
          </div>
          
          <select
            value={selectedCategory}
            onChange={(e) => setSelectedCategory(e.target.value)}
            className="px-3 py-1 border border-gray-300 rounded-md text-sm"
          >
            <option value="all">All Categories</option>
            {categories.map(category => (
              <option key={category} value={category}>
                {categoryLabels[category as keyof typeof categoryLabels] || category}
              </option>
            ))}
          </select>

          <select
            value={selectedSeverity}
            onChange={(e) => setSelectedSeverity(e.target.value)}
            className="px-3 py-1 border border-gray-300 rounded-md text-sm"
          >
            <option value="all">All Severities</option>
            {severities.map(severity => (
              <option key={severity} value={severity}>
                {severity.charAt(0).toUpperCase() + severity.slice(1)}
              </option>
            ))}
          </select>

          {(selectedCategory !== 'all' || selectedSeverity !== 'all') && (
            <Button
              variant="outline"
              size="sm"
              onClick={clearFilters}
              className="text-xs"
            >
              Clear Filters
            </Button>
          )}
        </div>

        {/* Insights by Category */}
        <Tabs value={selectedCategory} onValueChange={setSelectedCategory}>
          <TabsList className="grid w-full grid-cols-7">
            <TabsTrigger value="all" className="text-xs">All</TabsTrigger>
            {categories.map(category => (
              <TabsTrigger key={category} value={category} className="text-xs">
                {categoryLabels[category as keyof typeof categoryLabels] || category}
              </TabsTrigger>
            ))}
          </TabsList>

          <TabsContent value="all" className="space-y-4">
            {Object.entries(insightsByCategory).map(([category, categoryInsights]) => (
              <Collapsible
                key={category}
                open={expandedCategories.has(category)}
                onOpenChange={() => toggleCategory(category)}
              >
                <CollapsibleTrigger asChild>
                  <Button
                    variant="ghost"
                    className="w-full justify-between p-4 h-auto"
                  >
                    <div className="flex items-center gap-2">
                      {expandedCategories.has(category) ? (
                        <ChevronDown className="h-4 w-4" />
                      ) : (
                        <ChevronRight className="h-4 w-4" />
                      )}
                      <span className="font-medium">
                        {categoryLabels[category as keyof typeof categoryLabels] || category}
                      </span>
                      <Badge variant="outline" className="text-xs">
                        {categoryInsights.length}
                      </Badge>
                    </div>
                  </Button>
                </CollapsibleTrigger>
                <CollapsibleContent className="space-y-4 pl-6">
                  {categoryInsights.map(insight => (
                    <InsightCard key={insight.id} insight={insight} />
                  ))}
                </CollapsibleContent>
              </Collapsible>
            ))}
          </TabsContent>

          {categories.map(category => (
            <TabsContent key={category} value={category} className="space-y-4">
              {insightsByCategory[category]?.map(insight => (
                <InsightCard key={insight.id} insight={insight} />
              ))}
            </TabsContent>
          ))}
        </Tabs>
      </CardContent>
    </Card>
  );
}
