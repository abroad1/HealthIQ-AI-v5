/**
 * LC-S6 — presentation-only narrative cleanup for retail surfaces.
 * Strips markdown decorators and replaces known internal vocabulary; does not change analytical data.
 */

export function stripSimpleMarkdownDecorators(text: string): string {
  if (!text) return '';
  let s = text;
  for (let i = 0; i < 12; i += 1) {
    const next = s
      .replace(/\*\*([^*]+)\*\*/g, '$1')
      .replace(/\*([^*]+)\*/g, '$1')
      .replace(/__([^_]+)__/g, '$1')
      .replace(/`([^`]+)`/g, '$1');
    if (next === s) break;
    s = next;
  }
  return s.replace(/`+/g, '');
}

/** Very long snake_case tokens (bridge / internal codes) → plain placeholder. */
export function scrubLongInternalSlugs(text: string): string {
  return text.replace(/\b[a-z][a-z0-9_]{38,}\b/g, (token) => {
    const segments = token.split('_').filter(Boolean);
    if (segments.length >= 6) return 'this related pattern';
    return token;
  });
}

const EXACT_TOKEN_REPLACEMENTS: Array<[RegExp, string]> = [
  [/\bcardiovascular_4_biomarkers\b/gi, 'cardiovascular markers on this panel'],
  [/\bdeterministic\s+narrative\s+compiler\b/gi, 'structured clinical rules'],
  [/\bdeterministic\s+arbitration\b/gi, 'clinical prioritisation on this panel'],
  [/\bdeterministic\s+system\s+snapshot\b/gi, 'structured snapshot of this panel'],
  [/\bgoverned\s+capacity\s+score\b/gi, 'confidence score'],
  [/\bLayer\s+B\b/gi, 'supporting clinical context'],
  [/\bLayer\s+C\b/gi, 'follow-up guidance'],
  [/\bIDL\b/g, 'display layer'],
  [/\bruntime\b/gi, 'analysis run'],
  [/\bmanifest\b/gi, 'report layout'],
  [/\bpayload\b/gi, 'report data'],
  [/\bcompiler\b/gi, 'report builder'],
  [/\bchain_(\d+)\b/gi, 'evidence chain'],
];

export function scrubInternalArchitecturePhrases(text: string): string {
  let s = text;
  for (const [re, rep] of EXACT_TOKEN_REPLACEMENTS) {
    s = s.replace(re, rep);
  }
  return scrubLongInternalSlugs(s);
}

/** Full pipeline for default consumer narrative blocks. */
export function scrubConsumerRetailNarrative(text: string): string {
  const stripped = stripSimpleMarkdownDecorators(text);
  return scrubInternalArchitecturePhrases(stripped);
}
