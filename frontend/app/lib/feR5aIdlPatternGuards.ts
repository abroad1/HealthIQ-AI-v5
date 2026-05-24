/**
 * FE-R5A — guards for limited IDL pattern surfacing (no cluster/signal labels).
 */

import type { InterpretationDisplayRecordV1, InterpretationScientificClassV1 } from '@/types/analysis';

const GENERIC_SUPPORTING_SUMMARY = 'key pattern signals for this interpretation';

const UNSAFE_LABEL_PATTERNS: RegExp[] = [
  /\bfunctional\s+read\s*[—–-]/i,
  /cardiovascular\s+\d+\s+biomarkers/i,
  /\bph_[a-z0-9_]+/i,
  /\bsignal_[a-z0-9_]+/i,
  /\b\d\.\d{2}\s+vs\s+\d\.\d{2}\b/,
];

export function isUnsafePatternRetailLabel(label: string | null | undefined): boolean {
  const t = (label || '').trim();
  if (!t.length) return true;
  return UNSAFE_LABEL_PATTERNS.some((re) => re.test(t));
}

export function isGenericIdlSupportingSummary(summary: string | null | undefined): boolean {
  const t = (summary || '').trim().toLowerCase();
  if (!t.length) return true;
  return t === GENERIC_SUPPORTING_SUMMARY || t.startsWith('key pattern signals');
}

export function formatScientificClassChipLabel(
  scientificClass: InterpretationScientificClassV1 | null | undefined
): string | null {
  switch (scientificClass) {
    case 'phenotype':
      return 'Phenotype';
    case 'risk_construct':
      return 'Risk pattern';
    case 'organ_pattern':
      return 'Organ pattern';
    case 'syndrome_state':
      return 'Health pattern';
    default:
      return null;
  }
}

export function selectSafeIdlPatternRecords(
  records: InterpretationDisplayRecordV1[] | null | undefined
): InterpretationDisplayRecordV1[] {
  if (!records?.length) return [];
  return [...records]
    .filter(
      (r) =>
        r.enabled_for_frontend === true &&
        r.frontend_allowed_term !== 'clinical_only' &&
        !isUnsafePatternRetailLabel(r.retail_display_label)
    )
    .sort((a, b) => a.display_order_priority - b.display_order_priority);
}
