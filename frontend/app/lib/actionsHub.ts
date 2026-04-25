import { firstSentence } from '@/lib/primaryFindingShaping';

/** At most two sentences for action card body (readability; DTO text unchanged in model). */
export function twoSentenceExcerpt(text: string): string {
  const t = text.trim();
  if (!t) return '';
  const s1 = firstSentence(t);
  let rest = t.slice(s1.length).trim();
  if (!rest) return s1;
  const s2 = firstSentence(rest);
  return s2 ? `${s1} ${s2}` : s1;
}
