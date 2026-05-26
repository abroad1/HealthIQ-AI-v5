/**
 * Presentational display maps for Wave 1 Health Systems Cards (DOMAIN-UX1A).
 * Fixed Wave 1 domain IDs only — not interpretation logic.
 */

export function wave1ScoreReliabilityLabel(tier: string): string {
  if (tier === 'high') return 'Good reliability';
  if (tier === 'medium') return 'Moderate reliability';
  return 'Limited reliability';
}

export function wave1BandLabelDisplay(band: string): string {
  const m: Record<string, string> = {
    strong: 'Strong',
    stable: 'Stable',
    watch: 'Worth watching',
    review: 'Needs attention',
  };
  return m[band] ?? band;
}

export function wave1EvidenceCompletenessLine(numerator: number, denominator: number): string {
  if (denominator <= 0) {
    return '0 of 0 expected markers included';
  }
  return `${numerator} of ${denominator} expected markers included`;
}

export function wave1IsZeroEvidenceState(numerator: number, denominator: number): boolean {
  return denominator > 0 && numerator === 0;
}

/** Partial evidence: some markers present but not full expected set (DTO fields only). */
export function wave1IsPartialEvidenceState(numerator: number, denominator: number): boolean {
  return denominator > 0 && numerator > 0 && numerator < denominator;
}
