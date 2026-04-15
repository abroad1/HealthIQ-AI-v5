/**
 * Frontend-only pattern relevance line for biomarker expansion (V6 journey).
 * Deterministic; no backend field — see sprint FE-R4-RESULTS-JOURNEY-V6.
 */

function normalizeBiomarkerKey(s: string): string {
  return s.toLowerCase().replace(/_/g, ' ').replace(/\s+/g, ' ').trim();
}

export function derivePatternRelevanceLine(args: {
  biomarkerKey: string;
  primaryDriver: { name: string; biomarkers: string[] } | null | undefined;
  /** True when contribution_context includes a usable factual_statement (same gate as BiomarkerDialEntry mapping). */
  hasContributionFactual: boolean;
  relatedSystemGroupNames: string[];
}): string | null {
  if (!args.hasContributionFactual) return null;
  const pd = args.primaryDriver;
  if (!pd || !pd.name?.trim()) return null;

  const key = normalizeBiomarkerKey(args.biomarkerKey);
  const inDriver = (pd.biomarkers || []).some((b) => normalizeBiomarkerKey(String(b)) === key);

  if (inDriver) {
    return `This marker helped shape the ${pd.name.trim()} pattern—the main pattern highlighted in your interpretation.`;
  }

  const groups = (args.relatedSystemGroupNames || []).map((n) => n.trim()).filter(Boolean);
  if (groups.length === 0) return null;

  if (groups.length === 1) {
    return `This marker aligns more closely with ${groups[0]} than with the highlighted ${pd.name.trim()} pattern.`;
  }
  const last = groups[groups.length - 1];
  const rest = groups.slice(0, -1).join(', ');
  return `This marker aligns more closely with ${rest} and ${last} than with the highlighted ${pd.name.trim()} pattern.`;
}
