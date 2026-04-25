/**
 * Longitudinal biomarker comparison from two analysis result DTOs (Sprint 6).
 * No analytical interpretation — numeric delta only.
 */

import type { AnalysisHistoryItem, AnalysisResult, BiomarkerResult } from '@/types/analysis';
import { humanizeStatus } from '@/lib/resultsPageLayout';

export type TrendArrow = 'up' | 'down' | 'flat' | 'unknown';

export interface BiomarkerTrendRow {
  biomarkerName: string;
  recentDisplay: string;
  previousDisplay: string;
  deltaDisplay: string;
  arrow: TrendArrow;
  rangeStatusLabel: string;
  /** For sorting: abs delta when both numeric; -1 when not comparable */
  sortAbsDelta: number;
  /** True when both runs have a numeric value for this marker */
  hasComparableDelta: boolean;
}

export function biomarkerTrendKey(name: string): string {
  return name.trim().toLowerCase();
}

function formatMarkerValue(b: BiomarkerResult): string {
  if (b.value == null || typeof b.value !== 'number' || Number.isNaN(b.value)) {
    return '—';
  }
  const v = b.value;
  const abs = Math.abs(v);
  const decimals = abs >= 100 ? 1 : abs >= 10 ? 2 : 3;
  const rounded = Math.round(v * 10 ** decimals) / 10 ** decimals;
  const unit = (b.unit || '').trim();
  const num = String(rounded);
  return unit ? `${num} ${unit}` : num;
}

function biomarkerMap(list: BiomarkerResult[]): Map<string, BiomarkerResult> {
  const m = new Map<string, BiomarkerResult>();
  for (const b of list) {
    if (!b?.biomarker_name?.trim()) continue;
    m.set(biomarkerTrendKey(b.biomarker_name), b);
  }
  return m;
}

/**
 * Build table rows: union of marker names from both panels.
 * "Current range status" uses the most recent panel when the marker exists there; otherwise "—".
 */
export function buildBiomarkerTrendRows(
  recent: AnalysisResult,
  previous: AnalysisResult
): BiomarkerTrendRow[] {
  const recentList = Array.isArray(recent.biomarkers) ? recent.biomarkers : [];
  const prevList = Array.isArray(previous.biomarkers) ? previous.biomarkers : [];
  const recentByKey = biomarkerMap(recentList);
  const prevByKey = biomarkerMap(prevList);

  const keys = new Set<string>();
  for (const b of recentList) {
    if (b?.biomarker_name?.trim()) keys.add(biomarkerTrendKey(b.biomarker_name));
  }
  for (const b of prevList) {
    if (b?.biomarker_name?.trim()) keys.add(biomarkerTrendKey(b.biomarker_name));
  }

  const rows: BiomarkerTrendRow[] = [];
  for (const key of Array.from(keys)) {
    const rb = recentByKey.get(key);
    const pb = prevByKey.get(key);
    const name = (rb ?? pb)!.biomarker_name;
    rows.push(buildOneRow(name, rb, pb));
  }

  return sortTrendRows(rows);
}

function buildOneRow(
  name: string,
  recentB: BiomarkerResult | undefined,
  prevB: BiomarkerResult | undefined
): BiomarkerTrendRow {
  const recentDisplay = recentB ? formatMarkerValue(recentB) : '—';
  const previousDisplay = prevB ? formatMarkerValue(prevB) : '—';

  const rv = recentB?.value;
  const pv = prevB?.value;
  const ru = (recentB?.unit || '').trim();
  const pu = (prevB?.unit || '').trim();
  const unit = ru || pu;

  let deltaDisplay = '—';
  let arrow: TrendArrow = 'unknown';
  let sortAbsDelta = -1;
  let hasComparableDelta = false;

  if (
    typeof rv === 'number' &&
    !Number.isNaN(rv) &&
    typeof pv === 'number' &&
    !Number.isNaN(pv)
  ) {
    hasComparableDelta = true;
    const delta = rv - pv;
    sortAbsDelta = Math.abs(delta);
    const absD = Math.abs(delta);
    const decimals = absD >= 100 ? 1 : absD >= 10 ? 2 : 3;
    const rounded = Math.round(delta * 10 ** decimals) / 10 ** decimals;
    const sign = rounded > 0 ? '+' : '';
    deltaDisplay = unit ? `${sign}${rounded} ${unit}` : `${sign}${rounded}`;
    if (rounded > 0) arrow = 'up';
    else if (rounded < 0) arrow = 'down';
    else arrow = 'flat';
  }

  const rangeStatusLabel = recentB ? humanizeStatus(recentB.status) : '—';

  return {
    biomarkerName: name,
    recentDisplay,
    previousDisplay,
    deltaDisplay,
    arrow,
    rangeStatusLabel,
    sortAbsDelta,
    hasComparableDelta,
  };
}

export function sortTrendRows(rows: BiomarkerTrendRow[]): BiomarkerTrendRow[] {
  return [...rows].sort((a, b) => {
    const ac = a.hasComparableDelta ? 1 : 0;
    const bc = b.hasComparableDelta ? 1 : 0;
    if (ac !== bc) return bc - ac;
    if (a.hasComparableDelta && b.hasComparableDelta) {
      if (b.sortAbsDelta !== a.sortAbsDelta) return b.sortAbsDelta - a.sortAbsDelta;
    }
    return a.biomarkerName.localeCompare(b.biomarkerName, undefined, { sensitivity: 'base' });
  });
}

/** Most recent completed analyses first (by `created_at`). */
export function sortCompletedHistoryNewestFirst(items: AnalysisHistoryItem[]): AnalysisHistoryItem[] {
  return [...items].filter((h) => h.status === 'completed').sort((a, b) => {
    const ta = new Date(a.created_at).getTime();
    const tb = new Date(b.created_at).getTime();
    return tb - ta;
  });
}

export function topMovementRows(rows: BiomarkerTrendRow[], n: number): BiomarkerTrendRow[] {
  const comparable = rows.filter((r) => r.hasComparableDelta);
  return comparable.slice(0, n);
}
