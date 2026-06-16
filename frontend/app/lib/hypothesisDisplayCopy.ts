/**
 * IUAT-001 — render-only hypothesis title neutralisation from existing DTO counter-evidence.
 */

export function neutraliseHypothesisTitleForDisplay(
  title: string,
  evidenceAgainst: { item?: string | null }[] | null | undefined
): string {
  const t = (title || '').trim();
  if (!t) return t;
  const lowTitle = t.toLowerCase();
  if (!lowTitle.includes('b12') || !lowTitle.includes('associated')) return t;
  for (const ev of evidenceAgainst ?? []) {
    const item = (ev.item || '').toLowerCase();
    if (!item.includes('b12')) continue;
    if (
      item.includes('within range') ||
      item.includes('in range') ||
      item.includes('less likely') ||
      item.includes('pulls against') ||
      item.includes('complicates') ||
      item.includes('makes a b12-driven')
    ) {
      return 'Homocysteine-related pattern';
    }
  }
  return t;
}
