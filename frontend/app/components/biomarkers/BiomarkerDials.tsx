'use client';

import React, { useCallback, useEffect, useState } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { TrendingUp, TrendingDown, AlertTriangle, CheckCircle, Info, ChevronDown, ChevronRight } from 'lucide-react';

/** Per-marker model for retail cards + shared / inline detail (FE-VISUALISATION-B2) */
export interface BiomarkerDialEntry {
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
  educationalExplainer?: { title: string; body: string } | null;
  contributionContext?: { factual_statement: string } | null;
  relatedSystemGroupNames?: string[];
  /** Frontend-derived line connecting this marker to the lead pattern / groups — not a DTO field. */
  patternRelevanceLine?: string | null;
}

interface BiomarkerDialsProps {
  biomarkers: Record<string, BiomarkerDialEntry>;
  /** Softer section heading when used as a supporting layer */
  sectionTitle?: string;
}

const BIOMARKER_NAMES: Record<string, string> = {
  glucose: 'Glucose',
  hba1c: 'HbA1c',
  insulin: 'Insulin',
  c_peptide: 'C-Peptide',
  total_cholesterol: 'Total Cholesterol',
  ldl_cholesterol: 'LDL Cholesterol',
  hdl_cholesterol: 'HDL Cholesterol',
  triglycerides: 'Triglycerides',
  tc_hdl_ratio: 'TC:HDL ratio',
  tg_hdl_ratio: 'TG:HDL ratio',
  ldl_hdl_ratio: 'LDL:HDL ratio',
  non_hdl_cholesterol: 'Non-HDL cholesterol',
  apolipoprotein_b: 'Apolipoprotein B',
  apob: 'ApoB',
  apolipoprotein_a1: 'Apolipoprotein A1',
  apoa1: 'ApoA1',
  homocysteine: 'Homocysteine',
  crp: 'C-Reactive Protein',
  esr: 'Erythrocyte Sedimentation Rate',
  il_6: 'Interleukin-6',
  tnf_alpha: 'TNF-α',
  creatinine: 'Creatinine',
  egfr: 'eGFR',
  bun: 'Blood Urea Nitrogen',
  urea: 'Urea',
  urate: 'Urate',
  alt: 'ALT',
  ast: 'AST',
  ggt: 'GGT',
  alkaline_phosphatase: 'Alkaline Phosphatase',
  hemoglobin: 'Haemoglobin',
  haemoglobin: 'Haemoglobin',
  hematocrit: 'Hematocrit',
  haematocrit: 'Haematocrit',
  mcv: 'MCV',
  mch: 'MCH',
  mchc: 'MCHC',
  wbc: 'White Blood Cell Count',
  white_blood_cells: 'White Blood Cells',
  rbc: 'Red Blood Cell Count',
  platelets: 'Platelet Count',
  tsh: 'TSH',
  fsh: 'FSH',
  lh: 'LH',
  free_t4: 'Free T4',
  free_t3: 'Free T3',
  cortisol: 'Cortisol',
  testosterone: 'Testosterone',
  vitamin_d: 'Vitamin D',
  vitamin_b12: 'Vitamin B12',
  active_b12: 'Active B12',
  folate: 'Folate',
  iron: 'Iron',
  ferritin: 'Ferritin',
};

/** LC-S7 — hide numeric reference band when value vs range units are clearly incompatible (display-only). */
function shouldSuppressReferenceRange(valueUnit?: string | null, rangeUnit?: string | null): boolean {
  const vu = (valueUnit || '').toLowerCase().replace(/\s+/g, '').replace('µ', 'u');
  const ru = (rangeUnit || '').toLowerCase().replace(/\s+/g, '').replace('µ', 'u');
  if (!vu || !ru) return false;
  const valueGdl = vu.includes('g/dl') || vu === 'gdl';
  const rangeGl = ru === 'g/l' || (ru.includes('g/l') && !ru.includes('dl'));
  if (valueGdl && rangeGl) return true;
  const valuePct = vu === '%' || (vu.length <= 5 && vu.endsWith('%'));
  if (valuePct && ru.includes('l/l')) return true;
  const mmolMol = ru.includes('mmol/mol') || ru.includes('mmolmol');
  if (mmolMol && vu.includes('%')) return true;
  if ((vu.includes('mmol/mol') || vu.includes('mmolmol')) && ru.includes('%')) return true;
  return false;
}

const getStatusColor = (status?: string) => {
  switch (status) {
    case 'optimal':
      return 'text-green-600 bg-green-100';
    case 'normal':
      return 'text-blue-600 bg-blue-100';
    case 'elevated':
    case 'suboptimal':
    case 'at_risk':
      return 'text-yellow-600 bg-yellow-100';
    case 'low':
      return 'text-orange-600 bg-orange-100';
    case 'critical':
      return 'text-red-600 bg-red-100';
    default:
      return 'text-gray-600 bg-gray-100';
  }
};

const getStatusIcon = (status?: string) => {
  switch (status) {
    case 'optimal':
      return <CheckCircle className="h-4 w-4" />;
    case 'normal':
      return <CheckCircle className="h-4 w-4" />;
    case 'elevated':
    case 'suboptimal':
    case 'at_risk':
      return <TrendingUp className="h-4 w-4" />;
    case 'low':
      return <TrendingDown className="h-4 w-4" />;
    case 'critical':
      return <AlertTriangle className="h-4 w-4" />;
    default:
      return <Info className="h-4 w-4" />;
  }
};

const getStatusLabel = (status?: string) => {
  switch (status) {
    case 'optimal':
      return 'Optimal';
    case 'normal':
      return 'Normal';
    case 'elevated':
      return 'Elevated';
    case 'suboptimal':
      return 'Suboptimal';
    case 'at_risk':
      return 'At risk';
    case 'low':
      return 'Low';
    case 'critical':
      return 'Critical';
    default:
      return 'Unknown';
  }
};

const calculateDialValue = (
  value: number,
  referenceRange?: { min?: number; max?: number; unit: string; source?: string },
  score?: number
): number => {
  if (typeof score === 'number' && !Number.isNaN(score)) {
    const clamped = Math.min(1, Math.max(0, score));
    return Math.round(clamped * 100);
  }
  if (referenceRange && typeof referenceRange.min === 'number' && typeof referenceRange.max === 'number') {
    const range = referenceRange.max - referenceRange.min;
    if (range > 0) {
      const raw = ((value - referenceRange.min) / range) * 100;
      return Math.max(0, Math.min(100, raw));
    }
  }
  return 50;
};

const getDialColor = (value: number, status?: string) => {
  if (status === 'critical') return 'stroke-red-500';
  if (status === 'elevated' || status === 'low' || status === 'suboptimal' || status === 'at_risk')
    return 'stroke-yellow-500';
  if (status === 'optimal' || status === 'normal') return 'stroke-green-500';
  if (value < 20 || value > 80) return 'stroke-red-500';
  if (value < 30 || value > 70) return 'stroke-yellow-500';
  return 'stroke-green-500';
};

const renderDial = (value: number, status?: string, size: 'sm' | 'md' | 'lg' = 'md') => {
  const sizeClasses = { sm: 'w-16 h-16', md: 'w-24 h-24', lg: 'w-32 h-32' };
  const strokeWidth = size === 'sm' ? 2 : size === 'md' ? 3 : 4;
  const radius = size === 'sm' ? 28 : size === 'md' ? 40 : 56;
  const circumference = 2 * Math.PI * radius;
  const strokeDasharray = circumference;
  const strokeDashoffset = circumference - (value / 100) * circumference;

  return (
    <div className={`${sizeClasses[size]} relative flex-shrink-0`}>
      <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100" preserveAspectRatio="xMidYMid meet">
        <circle cx="50" cy="50" r={radius} stroke="currentColor" strokeWidth={strokeWidth} fill="none" className="text-gray-200" />
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

function BiomarkerDetailZones({
  biomarkerKey,
  data,
}: {
  biomarkerKey: string;
  data: BiomarkerDialEntry;
}) {
  const displayName = BIOMARKER_NAMES[biomarkerKey] || biomarkerKey.replace(/_/g, ' ');
  const layer2Body = data.educationalExplainer?.body?.trim();
  const factual = data.contributionContext?.factual_statement?.trim();
  const patternLine = data.patternRelevanceLine?.trim();
  const hasLayer3 =
    !!(patternLine || factual || (data.relatedSystemGroupNames && data.relatedSystemGroupNames.length > 0));

  return (
    <div className="space-y-4 text-left border-t border-gray-200 pt-4 mt-3">
      <h4 className="text-base font-semibold text-gray-900">{displayName}</h4>

      {layer2Body ? (
        <div>
          <h5 className="text-xs font-semibold uppercase tracking-wide text-gray-500 mb-1">Why this marker matters</h5>
          <p className="text-sm text-gray-800 leading-relaxed whitespace-pre-wrap">{layer2Body}</p>
        </div>
      ) : null}

      {hasLayer3 ? (
        <div className="space-y-3">
          <h5 className="text-xs font-semibold uppercase tracking-wide text-gray-500">How it connects to your wider pattern</h5>
          {patternLine ? (
            <p className="text-sm text-gray-800 leading-relaxed whitespace-pre-wrap">{patternLine}</p>
          ) : null}
          {factual ? (
            <p className="text-sm text-gray-800 leading-relaxed whitespace-pre-wrap">{factual}</p>
          ) : null}
          {data.relatedSystemGroupNames && data.relatedSystemGroupNames.length > 0 ? (
            <ul className="flex flex-wrap gap-2 list-none p-0 m-0">
              {data.relatedSystemGroupNames.map((n) => (
                <li key={n}>
                  <Badge variant="outline" className="font-normal">
                    {n}
                  </Badge>
                </li>
              ))}
            </ul>
          ) : null}
        </div>
      ) : null}
    </div>
  );
}

function hasExpandableLayers(d: BiomarkerDialEntry): boolean {
  return !!(
    (d.educationalExplainer?.body && String(d.educationalExplainer.body).trim()) ||
    (d.contributionContext?.factual_statement && String(d.contributionContext.factual_statement).trim()) ||
    (d.patternRelevanceLine && String(d.patternRelevanceLine).trim()) ||
    (d.relatedSystemGroupNames && d.relatedSystemGroupNames.length > 0)
  );
}

export default function BiomarkerDials({ biomarkers, sectionTitle = 'Biomarker evidence' }: BiomarkerDialsProps) {
  const [selectedKey, setSelectedKey] = useState<string | null>(null);
  const [isDesktop, setIsDesktop] = useState(false);

  useEffect(() => {
    if (typeof window === 'undefined' || typeof window.matchMedia !== 'function') {
      setIsDesktop(false);
      return;
    }
    const mq = window.matchMedia('(min-width: 768px)');
    const update = () => setIsDesktop(mq.matches);
    update();
    mq.addEventListener('change', update);
    return () => mq.removeEventListener('change', update);
  }, []);

  const toggleSelect = useCallback((key: string) => {
    setSelectedKey((cur) => (cur === key ? null : key));
  }, []);

  const biomarkerEntries = Object.entries(biomarkers || {});
  const selectedData = selectedKey && biomarkers[selectedKey] ? biomarkers[selectedKey] : null;

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
          Marker values support the interpretation above. Select a card for more context on larger screens; on mobile,
          details open under the card.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6 w-full">
        {biomarkerEntries.map(([name, raw]) => {
          const d = raw as BiomarkerDialEntry | undefined;
          const hasScore = typeof d?.score === 'number' && !Number.isNaN(d.score);
          const hasValue = typeof d?.value === 'number' && !Number.isNaN(d.value);
          if (!hasScore && !hasValue) return null;

          const value = hasValue ? d!.value : 0;
          const dialValue = calculateDialValue(value, d?.referenceRange, d?.score);
          const isSel = selectedKey === name;
          const displayName = BIOMARKER_NAMES[name] || name.replace(/_/g, ' ');
          const expandable = hasExpandableLayers(d!);
          const hideRange = shouldSuppressReferenceRange(d?.unit, d?.referenceRange?.unit);

          return (
            <div key={name} className="min-h-[120px]">
              <Card
                className={`hover:shadow-md transition-shadow w-full h-full border-gray-200 bg-white ${
                  isSel ? 'ring-2 ring-blue-400 ring-offset-1' : ''
                }`}
              >
                <CardContent className="pt-4">
                  <div className="flex items-center justify-between mb-3 gap-2">
                    <div className="min-w-0">
                      <h4 className="font-semibold text-gray-900 truncate">{displayName}</h4>
                      <p className="text-sm text-gray-500">{d?.unit}</p>
                    </div>
                    <Badge className={getStatusColor(d?.status)}>{getStatusIcon(d?.status)}</Badge>
                  </div>

                  <div className="flex items-center justify-between gap-3">
                    <div className="flex-1 min-w-0">
                      <div className="text-2xl font-bold text-gray-900 mb-1">{value.toFixed(1)}</div>
                      {d?.referenceRange &&
                      typeof d.referenceRange.min === 'number' &&
                      typeof d.referenceRange.max === 'number' &&
                      !hideRange ? (
                        <div className="text-xs text-gray-500">
                          Range: {d.referenceRange.min}–{d.referenceRange.max} {d.referenceRange.unit}
                        </div>
                      ) : null}
                      {hideRange ? (
                        <p className="text-xs text-amber-800/90 mt-1 leading-snug">
                          Reference range not shown here because the lab units differ from the value row — use your
                          original report or ask your clinician.
                        </p>
                      ) : null}
                      {d?.interpretation ? (
                        <p className="text-xs text-gray-700 mt-2 leading-relaxed line-clamp-3">{d.interpretation}</p>
                      ) : null}
                      {d?.date ? (
                        <div className="text-xs text-gray-400 mt-1">{new Date(d.date).toLocaleDateString()}</div>
                      ) : null}
                    </div>
                    <div className="flex flex-col items-end gap-2 flex-shrink-0">
                      {renderDial(dialValue, d?.status, 'md')}
                      {expandable ? (
                        <Button
                          type="button"
                          variant="outline"
                          size="sm"
                          className="text-xs h-8"
                          onClick={() => toggleSelect(name)}
                          aria-expanded={isSel}
                        >
                          {isSel ? (
                            <>
                              <ChevronDown className="h-3 w-3 mr-1" /> Close
                            </>
                          ) : (
                            <>
                              <ChevronRight className="h-3 w-3 mr-1" /> Expand
                            </>
                          )}
                        </Button>
                      ) : null}
                    </div>
                  </div>

                  {!isDesktop && isSel && expandable && d ? <BiomarkerDetailZones biomarkerKey={name} data={d} /> : null}
                </CardContent>
              </Card>
            </div>
          );
        })}
      </div>

      {isDesktop && selectedKey && selectedData && hasExpandableLayers(selectedData) ? (
        <Card className="border-blue-100 bg-white shadow-sm">
          <CardContent className="pt-6">
            <BiomarkerDetailZones biomarkerKey={selectedKey} data={selectedData} />
          </CardContent>
        </Card>
      ) : null}
    </div>
  );
}
