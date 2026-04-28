/**
 * D-7 — User-safe display labels for Wave 1 "What would improve confidence" (missing marker ids).
 * Deterministic mapping; no raw snake_case / internal ids in UI.
 */
const CANONICAL_ID_TO_LABEL: Record<string, string> = {
  alt: 'ALT (alanine aminotransferase)',
  ast: 'AST (aspartate aminotransferase)',
  ggt: 'GGT (gamma-glutamyl transferase)',
  alp: 'ALP (alkaline phosphatase)',
  alkaline_phosphatase: 'Alkaline phosphatase',
  albumin: 'Albumin',
  globulin: 'Globulin',
  total_protein: 'Total protein',
  total_bilirubin: 'Total bilirubin',
  bilirubin: 'Bilirubin',
};

/**
 * Maps backend missing_marker_ids (canonical biomarker keys) to short readable labels.
 */
export function wave1ConfidenceMarkerDisplayLabel(canonicalId: string): string {
  const k = canonicalId.trim().toLowerCase();
  if (CANONICAL_ID_TO_LABEL[k]) return CANONICAL_ID_TO_LABEL[k];
  if (!k.includes('_')) return canonicalId.trim();
  return k
    .split('_')
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(' ');
}
