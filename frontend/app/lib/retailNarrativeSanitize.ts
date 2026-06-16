/**
 * LC-S6 — presentation-only narrative cleanup for retail surfaces.
 * Strips markdown decorators and replaces known internal vocabulary; does not change analytical data.
 */

import { scrubKnownInternalPatternNames } from '@/lib/cardEvidenceConsumerCopy';

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
  [/\bCardiovascular\s+\d+\s+Biomarkers\b/gi, 'cardiovascular markers on this panel'],
  [/\bcardiovascular_4_biomarkers\b/gi, 'cardiovascular markers on this panel'],
  [/\bdeterministic\s+narrative\s+compiler\b/gi, 'structured clinical rules'],
  [/\bdeterministic\s+arbitration\b/gi, 'clinical prioritisation on this panel'],
  [/\bdeterministic\s+system\s+snapshot\b/gi, 'structured snapshot of this panel'],
  [/\bgoverned\s+capacity\s+score\b/gi, 'confidence score'],
  [/\bgoverned\s+functional\s+titles\b/gi, 'interpretation themes'],
  [/\bexpected_biomarker_effect\b/gi, 'expected marker pattern'],
  [/\bdirection\s*=\s*lower\b/gi, 'expected direction: lower'],
  [/\bPRIMARY_CONCERN_AND_RANKED_AMBIGUITY_POLICY[^\s]*\b/gi, 'ordering policy'],
  [/\bsupporting\s+clinical\s+context\s+intervention\s+annotation\b/gi, 'medication context note'],
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

/** Fix common UTF-8 mojibake sequences in persisted narrative text. */
export function scrubMojibakeArtifacts(text: string): string {
  return text
    .replace(/\uFFFD/g, '')
    .replace(/â€./g, '—')
    .replace(/â€™/g, "'")
    .replace(/â€œ/g, '"')
    .replace(/\s*â\s*(?=[,.;:!?]|$)/g, '')
    .replace(/\s{2,}/g, ' ')
    .trim();
}
/** FE-R6A — retail-only strips for fresh UAT defects (presentation layer). */
export function scrubFeR6aRetailSurfacePhrases(text: string): string {
  let s = text;
  s = s.replace(
    /This is used only to adjust how systems are weighted in the analytical model\s*[—–-]\s*not to alter the lab values on this panel\.?/gi,
    'Your lifestyle inputs can add context when we interpret how different areas of health relate on this panel.'
  );
  s = s.replace(/\s*\(interpretation confidence for this read:[^)]*\)/gi, '');
  s = s.replace(/\s*interpretation confidence for this read:\s*[^\s.)]+/gi, '');
  s = s.replace(/Suggested follow-up themes:\s*/gi, '');
  return s.replace(/\s{2,}/g, ' ').trim();
}

export function scrubConsumerRetailNarrative(text: string): string {
  const stripped = stripSimpleMarkdownDecorators(text);
  let s = scrubInternalArchitecturePhrases(stripped);
  s = scrubFeR6aRetailSurfacePhrases(s);
  s = scrubMojibakeArtifacts(s);
  s = scrubKnownInternalPatternNames(s);
  s = s.replace(/\bsignal_homocysteine_elevation_context\b/gi, 'homocysteine-related pattern');
  s = s.replace(/\bhcy_b12_pattern_v1\b/gi, 'B12–homocysteine pattern');
  return s;
}
