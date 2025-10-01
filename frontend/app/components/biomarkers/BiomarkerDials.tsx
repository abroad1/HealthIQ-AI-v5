'use client';

import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { 
  TrendingUp, 
  TrendingDown, 
  Minus, 
  AlertTriangle, 
  CheckCircle, 
  Info,
  ChevronDown,
  ChevronRight
} from 'lucide-react';

interface BiomarkerValue {
  value: number;
  unit: string;
  date?: string;
  referenceRange?: {
    min: number;
    max: number;
    unit: string;
  };
  status?: 'optimal' | 'normal' | 'elevated' | 'low' | 'critical';
}

interface BiomarkerDialsProps {
  biomarkers: Record<string, BiomarkerValue>;
  showDetails?: boolean;
}

const BIOMARKER_CATEGORIES = {
  metabolic: {
    name: 'Metabolic Health',
    biomarkers: ['glucose', 'hba1c', 'insulin', 'c_peptide'],
    color: 'blue'
  },
  cardiovascular: {
    name: 'Cardiovascular Health',
    biomarkers: ['total_cholesterol', 'ldl_cholesterol', 'hdl_cholesterol', 'triglycerides', 'apolipoprotein_b', 'apolipoprotein_a1'],
    color: 'red'
  },
  inflammatory: {
    name: 'Inflammatory Health',
    biomarkers: ['crp', 'esr', 'il_6', 'tnf_alpha'],
    color: 'orange'
  },
  organ: {
    name: 'Organ Function',
    biomarkers: ['creatinine', 'bun', 'alt', 'ast', 'ggt', 'alkaline_phosphatase'],
    color: 'green'
  },
  cbc: {
    name: 'Complete Blood Count',
    biomarkers: ['hemoglobin', 'hematocrit', 'wbc', 'rbc', 'platelets'],
    color: 'purple'
  },
  hormonal: {
    name: 'Hormonal Health',
    biomarkers: ['tsh', 'free_t4', 'free_t3', 'cortisol', 'testosterone'],
    color: 'pink'
  },
  nutritional: {
    name: 'Nutritional Status',
    biomarkers: ['vitamin_d', 'vitamin_b12', 'folate', 'iron', 'ferritin'],
    color: 'yellow'
  }
};

const BIOMARKER_NAMES = {
  glucose: 'Glucose',
  hba1c: 'HbA1c',
  insulin: 'Insulin',
  c_peptide: 'C-Peptide',
  total_cholesterol: 'Total Cholesterol',
  ldl_cholesterol: 'LDL Cholesterol',
  hdl_cholesterol: 'HDL Cholesterol',
  triglycerides: 'Triglycerides',
  apolipoprotein_b: 'Apolipoprotein B',
  apolipoprotein_a1: 'Apolipoprotein A1',
  crp: 'C-Reactive Protein',
  esr: 'Erythrocyte Sedimentation Rate',
  il_6: 'Interleukin-6',
  tnf_alpha: 'TNF-α',
  creatinine: 'Creatinine',
  bun: 'Blood Urea Nitrogen',
  alt: 'ALT',
  ast: 'AST',
  ggt: 'GGT',
  alkaline_phosphatase: 'Alkaline Phosphatase',
  hemoglobin: 'Hemoglobin',
  hematocrit: 'Hematocrit',
  wbc: 'White Blood Cell Count',
  rbc: 'Red Blood Cell Count',
  platelets: 'Platelet Count',
  tsh: 'TSH',
  free_t4: 'Free T4',
  free_t3: 'Free T3',
  cortisol: 'Cortisol',
  testosterone: 'Testosterone',
  vitamin_d: 'Vitamin D',
  vitamin_b12: 'Vitamin B12',
  folate: 'Folate',
  iron: 'Iron',
  ferritin: 'Ferritin'
};

const getStatusColor = (status?: string) => {
  switch (status) {
    case 'optimal': return 'text-green-600 bg-green-100';
    case 'normal': return 'text-blue-600 bg-blue-100';
    case 'elevated': return 'text-yellow-600 bg-yellow-100';
    case 'low': return 'text-orange-600 bg-orange-100';
    case 'critical': return 'text-red-600 bg-red-100';
    default: return 'text-gray-600 bg-gray-100';
  }
};

const getStatusIcon = (status?: string) => {
  switch (status) {
    case 'optimal': return <CheckCircle className="h-4 w-4" />;
    case 'normal': return <CheckCircle className="h-4 w-4" />;
    case 'elevated': return <TrendingUp className="h-4 w-4" />;
    case 'low': return <TrendingDown className="h-4 w-4" />;
    case 'critical': return <AlertTriangle className="h-4 w-4" />;
    default: return <Info className="h-4 w-4" />;
  }
};

const getStatusLabel = (status?: string) => {
  switch (status) {
    case 'optimal': return 'Optimal';
    case 'normal': return 'Normal';
    case 'elevated': return 'Elevated';
    case 'low': return 'Low';
    case 'critical': return 'Critical';
    default: return 'Unknown';
  }
};

const calculateDialValue = (value: number, referenceRange?: { min: number; max: number }) => {
  if (!referenceRange) return 50; // Default to middle if no reference range
  
  const range = referenceRange.max - referenceRange.min;
  const normalizedValue = Math.max(0, Math.min(100, ((value - referenceRange.min) / range) * 100));
  return normalizedValue;
};

const getDialColor = (value: number, status?: string) => {
  if (status === 'critical') return 'stroke-red-500';
  if (status === 'elevated' || status === 'low') return 'stroke-yellow-500';
  if (status === 'optimal' || status === 'normal') return 'stroke-green-500';
  
  // Default color based on value
  if (value < 20 || value > 80) return 'stroke-red-500';
  if (value < 30 || value > 70) return 'stroke-yellow-500';
  return 'stroke-green-500';
};

export default function BiomarkerDials({ biomarkers, showDetails = false }: BiomarkerDialsProps) {
  const [expandedCategories, setExpandedCategories] = useState<Set<string>>(new Set());
  const [selectedCategory, setSelectedCategory] = useState<string>('all');

  const toggleCategory = (category: string) => {
    const newExpanded = new Set(expandedCategories);
    if (newExpanded.has(category)) {
      newExpanded.delete(category);
    } else {
      newExpanded.add(category);
    }
    setExpandedCategories(newExpanded);
  };

  const getBiomarkersByCategory = () => {
    const result: Record<string, Array<{ id: string; data: BiomarkerValue }>> = {};
    
    Object.entries(biomarkers).forEach(([id, data]) => {
      // Find which category this biomarker belongs to
      const category = Object.entries(BIOMARKER_CATEGORIES).find(([_, cat]) => 
        cat.biomarkers.includes(id)
      )?.[0] || 'other';
      
      if (!result[category]) {
        result[category] = [];
      }
      result[category].push({ id, data });
    });
    
    return result;
  };

  const biomarkersByCategory = getBiomarkersByCategory();
  const categories = Object.keys(biomarkersByCategory);

  const renderDial = (value: number, status?: string, size: 'sm' | 'md' | 'lg' = 'md') => {
    const sizeClasses = {
      sm: 'w-16 h-16',
      md: 'w-24 h-24',
      lg: 'w-32 h-32'
    };
    
    const strokeWidth = size === 'sm' ? 2 : size === 'md' ? 3 : 4;
    const radius = size === 'sm' ? 28 : size === 'md' ? 40 : size === 'lg' ? 56 : 40;
    const circumference = 2 * Math.PI * radius;
    const strokeDasharray = circumference;
    const strokeDashoffset = circumference - (value / 100) * circumference;

    return (
      <div className={`${sizeClasses[size]} relative`}>
        <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
          {/* Background circle */}
          <circle
            cx="50"
            cy="50"
            r={radius}
            stroke="currentColor"
            strokeWidth={strokeWidth}
            fill="none"
            className="text-gray-200"
          />
          {/* Progress circle */}
          <circle
            cx="50"
            cy="50"
            r={radius}
            stroke="currentColor"
            strokeWidth={strokeWidth}
            fill="none"
            strokeDasharray={strokeDasharray}
            strokeDashoffset={strokeDashoffset}
            className={`transition-all duration-1000 ${getDialColor(value, status)}`}
            strokeLinecap="round"
          />
        </svg>
        <div className="absolute inset-0 flex items-center justify-center">
          <span className={`font-bold ${size === 'sm' ? 'text-sm' : size === 'md' ? 'text-lg' : 'text-xl'}`}>
            {Math.round(value)}
          </span>
        </div>
      </div>
    );
  };

  const renderBiomarkerCard = (id: string, data: BiomarkerValue, category: string) => {
    const dialValue = calculateDialValue(data.value, data.referenceRange);
    const categoryInfo = BIOMARKER_CATEGORIES[category as keyof typeof BIOMARKER_CATEGORIES];
    
    return (
      <Card key={id} className="hover:shadow-md transition-shadow">
        <CardContent className="pt-4">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h4 className="font-semibold text-gray-900">
                {BIOMARKER_NAMES[id as keyof typeof BIOMARKER_NAMES] || id}
              </h4>
              <p className="text-sm text-gray-500">{data.unit}</p>
            </div>
            <Badge className={getStatusColor(data.status)}>
              {getStatusIcon(data.status)}
              <span className="ml-1">{getStatusLabel(data.status)}</span>
            </Badge>
          </div>

          <div className="flex items-center justify-between">
            <div className="flex-1">
              <div className="text-2xl font-bold text-gray-900 mb-1">
                {data.value.toFixed(1)}
              </div>
              {data.referenceRange && (
                <div className="text-xs text-gray-500">
                  Range: {data.referenceRange.min}-{data.referenceRange.max} {data.referenceRange.unit}
                </div>
              )}
              {data.date && (
                <div className="text-xs text-gray-400 mt-1">
                  {new Date(data.date).toLocaleDateString()}
                </div>
              )}
            </div>
            <div className="ml-4">
              {renderDial(dialValue, data.status, 'md')}
            </div>
          </div>

          {showDetails && data.referenceRange && (
            <div className="mt-4 pt-4 border-t border-gray-100">
              <div className="flex items-center justify-between text-sm">
                <span className="text-gray-500">Your value</span>
                <span className="font-medium">{data.value}</span>
              </div>
              <div className="flex items-center justify-between text-sm">
                <span className="text-gray-500">Reference range</span>
                <span className="font-medium">
                  {data.referenceRange.min} - {data.referenceRange.max}
                </span>
              </div>
              <div className="mt-2">
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    className={`h-2 rounded-full transition-all duration-1000 ${
                      data.value < data.referenceRange.min ? 'bg-red-500' :
                      data.value > data.referenceRange.max ? 'bg-yellow-500' : 'bg-green-500'
                    }`}
                    style={{ 
                      width: `${Math.min(100, Math.max(0, 
                        ((data.value - data.referenceRange.min) / (data.referenceRange.max - data.referenceRange.min)) * 100
                      ))}%` 
                    }}
                  ></div>
                </div>
              </div>
            </div>
          )}
        </CardContent>
      </Card>
    );
  };

  if (Object.keys(biomarkers).length === 0) {
    return (
      <Card>
        <CardContent className="pt-6">
          <div className="text-center py-8">
            <TrendingUp className="h-12 w-12 text-gray-300 mx-auto mb-4" />
            <p className="text-gray-500">No biomarker data available.</p>
            <p className="text-sm text-gray-400">Complete an analysis to view your biomarker results.</p>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <TrendingUp className="h-5 w-5" />
            Biomarker Analysis
          </CardTitle>
          <CardDescription>
            Your biomarker values with reference ranges and health status indicators
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Tabs value={selectedCategory} onValueChange={setSelectedCategory}>
            <TabsList className="grid w-full grid-cols-8">
              <TabsTrigger value="all">All</TabsTrigger>
              {categories.map(category => (
                <TabsTrigger key={category} value={category}>
                  {BIOMARKER_CATEGORIES[category as keyof typeof BIOMARKER_CATEGORIES]?.name || category}
                </TabsTrigger>
              ))}
            </TabsList>

            <TabsContent value="all" className="space-y-6">
              {categories.map(category => (
                <div key={category}>
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-lg font-semibold text-gray-900">
                      {BIOMARKER_CATEGORIES[category as keyof typeof BIOMARKER_CATEGORIES]?.name || category}
                    </h3>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => toggleCategory(category)}
                    >
                      {expandedCategories.has(category) ? (
                        <ChevronDown className="h-4 w-4" />
                      ) : (
                        <ChevronRight className="h-4 w-4" />
                      )}
                    </Button>
                  </div>
                  
                  {expandedCategories.has(category) && (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                      {biomarkersByCategory[category].map(({ id, data }) => 
                        renderBiomarkerCard(id, data, category)
                      )}
                    </div>
                  )}
                </div>
              ))}
            </TabsContent>

            {categories.map(category => (
              <TabsContent key={category} value={category} className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {biomarkersByCategory[category].map(({ id, data }) => 
                    renderBiomarkerCard(id, data, category)
                  )}
                </div>
              </TabsContent>
            ))}
          </Tabs>
        </CardContent>
      </Card>
    </div>
  );
}
