'use client';

import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { 
  TrendingUp, 
  TrendingDown, 
  AlertTriangle, 
  CheckCircle, 
  Info
} from 'lucide-react';

interface BiomarkerValue {
  value: number;
  unit: string;
  date?: string;
  score?: number;
  interpretation?: string | null;
  referenceRange?: {
    min?: number;
    max?: number;
    unit: string;
    source?: string;
  };
  status?: 'optimal' | 'normal' | 'elevated' | 'low' | 'critical' | string;
}

interface BiomarkerDialsProps {
  biomarkers: Record<string, BiomarkerValue>;
  showDetails?: boolean;
  /** Softer section heading when used as a supporting layer */
  sectionTitle?: string;
}

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

const calculateDialValue = (
  value: number,
  referenceRange?: { min?: number; max?: number; unit: string; source?: string },
  score?: number
): number => {
  // 1) Prefer backend score if provided (0–1 → 0–100)
  if (typeof score === 'number' && !Number.isNaN(score)) {
    const clamped = Math.min(1, Math.max(0, score));
    return Math.round(clamped * 100);
  }

  // 2) Fallback to reference range if min/max defined and range > 0
  if (
    referenceRange &&
    typeof referenceRange.min === 'number' &&
    typeof referenceRange.max === 'number'
  ) {
    const range = referenceRange.max - referenceRange.min;
    if (range > 0) {
      const raw = ((value - referenceRange.min) / range) * 100;
      return Math.max(0, Math.min(100, raw));
    }
  }

  // 3) Last resort default
  return 50;
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
    <div className={`${sizeClasses[size]} relative flex-shrink-0`}>
      <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100" preserveAspectRatio="xMidYMid meet">
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

const renderBiomarkerCard = (
  biomarkerKey: string,
  data: BiomarkerValue,
  dialValue: number,
  showDetails: boolean = false
) => {
  return (
    <Card className="hover:shadow-md transition-shadow w-full h-full border-gray-200 bg-white">
      <CardContent className="pt-4 min-h-[180px]">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h4 className="font-semibold text-gray-900">
              {BIOMARKER_NAMES[biomarkerKey as keyof typeof BIOMARKER_NAMES] || biomarkerKey}
            </h4>
            <p className="text-sm text-gray-500">{data.unit}</p>
          </div>
          <Badge className={getStatusColor(data.status)}>
            {getStatusIcon(data.status)}
            <span className="ml-1">{getStatusLabel(data.status)}</span>
          </Badge>
        </div>

        <div className="flex items-center justify-between gap-4">
          <div className="flex-1 min-w-0">
            <div className="text-2xl font-bold text-gray-900 mb-1">
              {typeof data.value === 'number' ? data.value.toFixed(1) : 'N/A'}
            </div>
            {data.referenceRange && 
             typeof data.referenceRange.min === 'number' && 
             typeof data.referenceRange.max === 'number' && (
              <div className="text-xs text-gray-500">
                Range: {data.referenceRange.min}-{data.referenceRange.max} {data.referenceRange.unit}
              </div>
            )}
            {data.date && (
              <div className="text-xs text-gray-500 mt-1">
                {new Date(data.date).toLocaleDateString()}
              </div>
            )}
          </div>
          <div className="ml-4 flex-shrink-0 w-24 h-24">
            {renderDial(dialValue, data.status, 'md')}
          </div>
        </div>

        {showDetails && data.interpretation ? (
          <p className="mt-3 text-xs text-gray-600 leading-relaxed border-t border-gray-100 pt-3">
            {data.interpretation}
          </p>
        ) : null}

        {showDetails && data.referenceRange && 
         typeof data.referenceRange.min === 'number' && 
         typeof data.referenceRange.max === 'number' && (
          <div className="mt-4 pt-4 border-t border-gray-100">
            <div className="flex items-center justify-between text-sm">
              <span className="text-gray-600">Your value</span>
              <span className="font-medium text-gray-900">{data.value}</span>
            </div>
            <div className="flex items-center justify-between text-sm">
              <span className="text-gray-600">Reference range</span>
              <span className="font-medium text-gray-900">
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

export default function BiomarkerDials({
  biomarkers,
  showDetails = false,
  sectionTitle = 'Your markers',
}: BiomarkerDialsProps) {
  const biomarkerEntries = Object.entries(biomarkers || {});

  if (!biomarkerEntries.length) {
    return (
      <div className="text-sm text-gray-500">
        No biomarker data available.
      </div>
    );
  }

  return (
    <div className="w-full space-y-4">
      <div className="mb-2">
        <h2 className="text-lg font-semibold text-gray-800">{sectionTitle}</h2>
        <p className="text-sm text-gray-500">
          Marker values support the interpretation above — details and lab wording come from your results payload.
        </p>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6 w-full">
        {biomarkerEntries.map(([name, data]) => {
          const d = data as BiomarkerValue | undefined;
          
          // More robust check: we want to render if we have at least a score OR a value
          // Score 0 is valid and must NOT be treated as "falsy" for hiding
          const hasScore = typeof d?.score === 'number' && !Number.isNaN(d.score);
          const hasValue = typeof d?.value === 'number' && !Number.isNaN(d.value);
          
          if (!hasScore && !hasValue) {
            return null;
          }

          // Use value 0 as fallback if score exists but value doesn't, or vice versa
          const value = hasValue ? d.value : (hasScore ? 0 : 0);
          const dialValue = calculateDialValue(
            value,
            d?.referenceRange,
            d?.score
          );

          return (
            <div key={name} className="min-h-[200px]">
              {renderBiomarkerCard(name, { ...d, value } as BiomarkerValue, dialValue, showDetails)}
            </div>
          );
        })}
      </div>
    </div>
  );
}
