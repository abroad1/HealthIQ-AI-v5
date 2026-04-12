/**
 * Upload → review → analysis helpers for reference ranges (BE-W1-PR1).
 * Keeps parse fidelity, one-sided bounds, and payload shape aligned with backend normalize.py.
 */

import type { ContextRangeOption } from '@/types/parsed';

export type { ContextRangeOption };

/** Review attention: one-sided thresholds are valid lab intervals, not "incomplete". */
export type RangeAttention =
  | 'none'
  | 'one-sided'
  | 'partial'
  | 'missing'
  | 'context-selection-required';

export interface ParsedReferenceRange {
  min?: number;
  max?: number;
  /** Unit for the reference interval (often matches the marker unit). */
  unit: string;
}

export interface ReferenceRangeFromParseResult {
  referenceRange?: ParsedReferenceRange;
  /** Raw lab text when the parser supplied a string (context only; not a substitute for numeric bounds). */
  referenceText?: string;
  /** Structured contextual intervals when the lab lists multiple bands (BE-W1-PR4). */
  contextRangeOptions?: ContextRangeOption[];
}

function _num(v: unknown): number | undefined {
  if (v === null || v === undefined || v === '') return undefined;
  const n = typeof v === 'number' ? v : parseFloat(String(v));
  return Number.isFinite(n) ? n : undefined;
}

function _hasAnyRefBound(r: ParsedReferenceRange | undefined): boolean {
  if (!r) return false;
  const lo = r.min != null && Number.isFinite(r.min);
  const hi = r.max != null && Number.isFinite(r.max);
  return lo || hi;
}

/**
 * Parse `contextRangeOptions` / `context_range_options` from an API biomarker row.
 */
export function parseContextRangeOptionsFromRow(b: Record<string, unknown>): ContextRangeOption[] {
  const raw = b.contextRangeOptions ?? b.context_range_options;
  if (!Array.isArray(raw) || raw.length === 0) return [];
  const out: ContextRangeOption[] = [];
  for (const item of raw) {
    if (!item || typeof item !== 'object') continue;
    const o = item as Record<string, unknown>;
    const label = String(o.contextLabel ?? o.context_label ?? '').trim() || 'Reference';
    const unit = typeof o.unit === 'string' ? o.unit.trim() : '';
    const sn =
      typeof o.sourceSnippet === 'string'
        ? o.sourceSnippet.trim()
        : typeof o.source_snippet === 'string'
          ? o.source_snippet.trim()
          : undefined;
    out.push({
      contextLabel: label,
      min: _num(o.min),
      max: _num(o.max),
      unit,
      sourceSnippet: sn || undefined,
    });
  }
  return out;
}

/**
 * Build structured range + optional raw text from a single parser biomarker row.
 */
export function buildReferenceRangeFromParserRow(b: Record<string, unknown>): ReferenceRangeFromParseResult {
  const unit = typeof b.unit === 'string' ? b.unit : '';
  const contextRangeOptions = parseContextRangeOptionsFromRow(b);

  let referenceText: string | undefined;
  if (typeof b.rawReferenceText === 'string' && b.rawReferenceText.trim()) {
    referenceText = b.rawReferenceText.trim();
  }
  if (typeof b.reference === 'string' && b.reference.trim()) {
    referenceText = referenceText
      ? `${referenceText}\n\n${b.reference.trim()}`
      : b.reference.trim();
  }
  if (typeof b.referenceRange === 'string' && b.referenceRange.trim()) {
    referenceText = (referenceText ? `${referenceText}\n\n` : '') + b.referenceRange.trim();
  }

  if (contextRangeOptions.length > 1) {
    const low = _num(b.ref_low);
    const high = _num(b.ref_high);
    const hasLow = low !== undefined;
    const hasHigh = high !== undefined;
    if (hasLow || hasHigh) {
      return {
        referenceRange: {
          min: hasLow ? low : undefined,
          max: hasHigh ? high : undefined,
          unit,
        },
        referenceText,
        contextRangeOptions,
      };
    }
    return { referenceText, contextRangeOptions };
  }

  if (contextRangeOptions.length === 1) {
    const o0 = contextRangeOptions[0];
    if (_hasAnyRefBound({ min: o0.min, max: o0.max, unit: o0.unit || unit })) {
      const ru = (o0.unit || unit).trim();
      return {
        referenceRange: {
          min: o0.min,
          max: o0.max,
          unit: ru || unit,
        },
        referenceText,
        contextRangeOptions,
      };
    }
  }

  const low = _num(b.ref_low);
  const high = _num(b.ref_high);
  const hasLow = low !== undefined;
  const hasHigh = high !== undefined;

  if (hasLow || hasHigh) {
    return {
      referenceRange: {
        min: hasLow ? low : undefined,
        max: hasHigh ? high : undefined,
        unit,
      },
      referenceText,
      contextRangeOptions: contextRangeOptions.length ? contextRangeOptions : undefined,
    };
  }

  if (b.referenceRange && typeof b.referenceRange === 'object' && b.referenceRange !== null) {
    const o = b.referenceRange as Record<string, unknown>;
    const min = _num(o.min);
    const max = _num(o.max);
    const u = typeof o.unit === 'string' && o.unit.trim() ? o.unit : unit;
    if (min !== undefined || max !== undefined) {
      return {
        referenceRange: {
          min: min !== undefined ? min : undefined,
          max: max !== undefined ? max : undefined,
          unit: u,
        },
        referenceText,
        contextRangeOptions: contextRangeOptions.length ? contextRangeOptions : undefined,
      };
    }
  }

  if (referenceText) {
    return { referenceText, contextRangeOptions: contextRangeOptions.length ? contextRangeOptions : undefined };
  }
  return { contextRangeOptions: contextRangeOptions.length ? contextRangeOptions : undefined };
}

/**
 * Attention state for review UX: missing numeric bounds vs one-sided vs complete.
 */
export function rangeAttentionLevel(b: {
  unit: string;
  referenceRange?: ParsedReferenceRange;
  referenceText?: string;
  contextRangeOptions?: ContextRangeOption[];
}): RangeAttention {
  const opts = b.contextRangeOptions;
  if (opts && opts.length > 1 && !_hasAnyRefBound(b.referenceRange)) {
    return 'context-selection-required';
  }
  const r = b.referenceRange;
  const hasMin = r?.min != null && Number.isFinite(r.min);
  const hasMax = r?.max != null && Number.isFinite(r.max);
  const hasText = !!(b.referenceText && b.referenceText.trim());
  if (hasMin && hasMax) return 'none';
  if ((hasMin && !hasMax) || (!hasMin && hasMax)) return 'one-sided';
  if (hasText) return 'partial';
  return 'missing';
}

/**
 * Payload fragment for POST /analysis/start — matches backend normalize.py (min/max nullable).
 */
export function referenceRangeToPayload(
  r: ParsedReferenceRange | undefined
): { min: number | null; max: number | null; unit: string; source: 'lab' } | null {
  if (!r) return null;
  const hasMin = r.min != null && Number.isFinite(r.min);
  const hasMax = r.max != null && Number.isFinite(r.max);
  if (!hasMin && !hasMax) return null;
  return {
    min: hasMin ? r.min! : null,
    max: hasMax ? r.max! : null,
    unit: (r.unit || '').trim(),
    source: 'lab',
  };
}

/**
 * Stable biomarker key for analysis payload. Aligns with backend alias normalisation
 * (spaces → underscores). Maps known frontend slug variants to canonical IDs.
 */
export function analysisBiomarkerKey(displayName: string): string {
  const base = displayName.trim().toLowerCase().replace(/\s+/g, '_');
  // Backend SSOT aliases include `apolipoprotein_ratio` and normalized "Apolipoprotein ratio (Venous)".
  if (base === 'apolipoprotein_ratio_(venous)' || base === 'apolipoprotein_ratio_venous') {
    return 'apob_apoa1_ratio';
  }
  return base;
}

/** Match a single numeric token (lab-style quantitative value). */
const BIOMARKER_VALUE_TOKEN_RE =
  /^\s*([<>≤≥])?\s*([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)\s*$/;

function _numStringVariants(n: number): string[] {
  const s = String(n);
  const out = [s];
  if (Number.isInteger(n)) out.push(`${n}.0`);
  return out;
}

/** Avoid matching `5` inside `45` when locating a bound value in free text. */
function _isStandaloneNumberAt(t: string, idx: number, ns: string): boolean {
  if (t.substring(idx, idx + ns.length) !== ns) return false;
  const before = idx > 0 ? t[idx - 1] : '';
  const after = idx + ns.length < t.length ? t[idx + ns.length] : '';
  const beforeOk = idx === 0 || !/\d/.test(before);
  const afterOk = idx + ns.length >= t.length || !/\d/.test(after);
  return beforeOk && afterOk;
}

/**
 * If reference text places a strict or weak inequality immediately before the bound value, return it.
 * Otherwise return default (≥ for lower, ≤ for upper).
 */
function _comparatorBeforeBound(
  refText: string | undefined,
  bound: number,
  edge: 'lower' | 'upper'
): '>' | '≥' | '<' | '≤' | null {
  const t = refText || '';
  if (!t.trim()) return null;
  const seen = new Set<number>();
  for (const ns of _numStringVariants(bound)) {
    let from = 0;
    while (from <= t.length) {
      const idx = t.indexOf(ns, from);
      if (idx === -1) break;
      if (!_isStandaloneNumberAt(t, idx, ns)) {
        from = idx + 1;
        continue;
      }
      if (seen.has(idx)) {
        from = idx + 1;
        continue;
      }
      seen.add(idx);
      let i = idx - 1;
      while (i >= 0 && /\s/.test(t[i])) i--;
      if (i >= 0) {
        const ch = t[i];
        if (edge === 'upper') {
          if (ch === '<') return '<';
          if (ch === '≤') return '≤';
        } else {
          if (ch === '>') return '>';
          if (ch === '≥') return '≥';
        }
      }
      from = idx + 1;
    }
  }
  return null;
}

function _inferLowerComparator(refText: string | undefined, bound: number): '>' | '≥' {
  const c = _comparatorBeforeBound(refText, bound, 'lower');
  if (c === '>') return '>';
  return '≥';
}

function _inferUpperComparator(refText: string | undefined, bound: number): '<' | '≤' {
  const c = _comparatorBeforeBound(refText, bound, 'upper');
  if (c === '<') return '<';
  return '≤';
}

/**
 * Parse review-stage value input: plain number or inequality + number (e.g. "&lt;0.05").
 * Display may keep a string when an inequality prefix is present; analysis payload uses the numeric part only.
 */
export function parseBiomarkerValueForReview(raw: string):
  | { ok: true; display: number | string; numericForPayload: number }
  | { ok: false; message: string } {
  const t = raw.trim();
  if (!t) return { ok: false, message: 'Value is required' };
  const m = t.match(BIOMARKER_VALUE_TOKEN_RE);
  if (!m) {
    return { ok: false, message: 'Enter a number or inequality + number (e.g. <0.05)' };
  }
  const comp = m[1];
  const n = parseFloat(m[2]);
  if (!Number.isFinite(n)) return { ok: false, message: 'Invalid number' };
  const display: number | string = comp ? t : n;
  return { ok: true, display, numericForPayload: n };
}

/** Single numeric for POST /analysis/start — BiomarkerValue accepts numeric measurements. */
export function numericPartForAnalysisPayload(value: number | string): number {
  if (typeof value === 'number' && Number.isFinite(value)) return value;
  const p = parseBiomarkerValueForReview(String(value));
  return p.ok ? p.numericForPayload : NaN;
}

export function formatReferenceRangeDisplay(b: {
  referenceRange?: ParsedReferenceRange;
  referenceText?: string;
}): string {
  const r = b.referenceRange;
  const refText = b.referenceText;
  if (r && (r.min != null || r.max != null)) {
    const u = (r.unit || '').trim();
    if (r.min != null && r.max != null) return `${r.min}–${r.max}${u ? ` ${u}` : ''}`;
    if (r.min != null) {
      const sym = _inferLowerComparator(refText, r.min);
      return `${sym} ${r.min}${u ? ` ${u}` : ''}`;
    }
    if (r.max != null) {
      const sym = _inferUpperComparator(refText, r.max);
      return `${sym} ${r.max}${u ? ` ${u}` : ''}`;
    }
  }
  if (b.referenceText && b.referenceText.trim()) return b.referenceText.trim();
  return '—';
}
