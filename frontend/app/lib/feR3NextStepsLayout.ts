/**
 * FE-R3 — deterministic next-step / action deduplication (no new clinical logic).
 */

import type { ResultActionCardModel } from '@/lib/resultsPageLayout';
import { parseNarrativeNextStepParagraphs } from '@/lib/resultsPageLayout';

export function normalizeFeR3DedupeKey(text: string): string {
  return text
    .toLowerCase()
    .replace(/\s+/g, ' ')
    .replace(/[^a-z0-9\s]/g, '')
    .trim()
    .slice(0, 200);
}

/** Drop action cards whose paragraph already appears in governed narrative next steps. */
export function dedupeActionCardsAgainstNarrative(
  cards: ResultActionCardModel[],
  narrativeNextStepsNarrative: string | null | undefined
): ResultActionCardModel[] {
  const narrative = (narrativeNextStepsNarrative || '').trim();
  if (!narrative.length || cards.length === 0) return cards;
  const narrativeKeys = new Set(
    parseNarrativeNextStepParagraphs(narrative).map((p) => normalizeFeR3DedupeKey(p))
  );
  if (narrativeKeys.size === 0) return cards;
  return cards.filter((c) => !narrativeKeys.has(normalizeFeR3DedupeKey(c.paragraph)));
}

export function hasGovernedConfirmatoryTests(
  tests: { test_id?: string; display_name?: string; rationale?: string }[] | null | undefined
): boolean {
  return (tests || []).some((t) => (t.display_name || '').trim() && (t.rationale || '').trim());
}
