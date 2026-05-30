/**
 * LAUNCH-CORE-1 — consumer-safe presentation for compiled card evidence marker roles.
 * Maps backend enum values only; does not infer clinical meaning from marker ids.
 */

const CONSUMER_MARKER_ROLE_LABELS: Record<string, string> = {
  score_contributor: 'Used in this score',
  confidence_contributor: 'Supports confidence',
  contextual_marker: 'Context marker',
  mechanism_marker: 'Helps explain mechanism',
  differential_marker: 'Helps distinguish causes',
  exclusion_marker: 'Helps rule out alternatives',
  missing_for_confidence: 'Missing for confidence',
  optional_deeper_marker: 'Optional deeper marker',
};

export function consumerMarkerRoleLabel(markerRole: string | null | undefined): string | null {
  const role = (markerRole || '').trim();
  if (!role) return null;
  return CONSUMER_MARKER_ROLE_LABELS[role] ?? null;
}

/** Interim scrub for known compiler/package display names that leak engineering vocabulary. */
export function scrubKnownInternalPatternNames(text: string): string {
  let s = text;
  s = s.replace(/\bHomocysteine Elevation Context\b/gi, 'Raised homocysteine pattern');
  s = s.replace(/\bhomocysteine elevation context\b/g, 'raised homocysteine pattern');
  return s;
}
