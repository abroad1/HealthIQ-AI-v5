/**
 * Upload → review → analysis helpers for reference ranges (BE-W1-PR1).
 * Keeps parse fidelity, one-sided bounds, and payload shape aligned with backend normalize.py.
 */

export type RangeAttention = 'none' | 'partial' | 'missing';

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
}

function _num(v: unknown): number | undefined {
  if (v === null || v === undefined || v === '') return undefined;
  const n = typeof v === 'number' ? v : parseFloat(String(v));
  return Number.isFinite(n) ? n : undefined;
}

/**
 * Build structured range + optional raw text from a single parser biomarker row.
 */
export function buildReferenceRangeFromParserRow(b: Record<string, unknown>): ReferenceRangeFromParseResult {
  const unit = typeof b.unit === 'string' ? b.unit : '';

  let referenceText: string | undefined;
  if (typeof b.reference === 'string' && b.reference.trim()) {
    referenceText = b.reference.trim();
  }
  if (typeof b.referenceRange === 'string' && b.referenceRange.trim()) {
    referenceText = (referenceText ? `${referenceText}; ` : '') + b.referenceRange.trim();
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
      };
    }
  }

  if (referenceText) {
    return { referenceText };
  }
  return {};
}

/**
 * Attention state for review UX: missing numeric bounds vs one-sided vs complete.
 */
export function rangeAttentionLevel(b: {
  unit: string;
  referenceRange?: ParsedReferenceRange;
  referenceText?: string;
}): RangeAttention {
  const r = b.referenceRange;
  const hasMin = r?.min != null && Number.isFinite(r.min);
  const hasMax = r?.max != null && Number.isFinite(r.max);
  const hasText = !!(b.referenceText && b.referenceText.trim());
  if (hasMin && hasMax) return 'none';
  if (hasMin || hasMax || hasText) return 'partial';
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

export function formatReferenceRangeDisplay(b: {
  referenceRange?: ParsedReferenceRange;
  referenceText?: string;
}): string {
  const r = b.referenceRange;
  if (r && (r.min != null || r.max != null)) {
    const u = (r.unit || '').trim();
    if (r.min != null && r.max != null) return `${r.min}–${r.max}${u ? ` ${u}` : ''}`;
    if (r.min != null) return `≥ ${r.min}${u ? ` ${u}` : ''}`;
    if (r.max != null) return `≤ ${r.max}${u ? ` ${u}` : ''}`;
  }
  if (b.referenceText && b.referenceText.trim()) return b.referenceText.trim();
  return '—';
}
