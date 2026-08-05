/**
 * CLIN-PRIORITY presentation authority — sole clinical-priority source when
 * `clinical_concern_set` is present. Frontend must not recompute tier/urgency/lead.
 */

import type {
  AnalysisResult,
  ClinicalFindingV1,
  ClinicalFindingUrgencyV1,
  ConsolidatedConcernSetV1,
} from '@/types/analysis';
import {
  getClinicalConcernSet,
  hasClinicalConcernAuthority,
} from '@/lib/clinicalConcernSet';

export type PresentationAuthoritySource = 'clinical_concern_set' | 'legacy';

export interface ClinicalPresentationAuthority {
  source: PresentationAuthoritySource;
  concernSet: ConsolidatedConcernSetV1 | null;
  leadFindings: ClinicalFindingV1[];
  coLeadFindings: ClinicalFindingV1[];
  presentationMode: ConsolidatedConcernSetV1['presentation_mode'] | null;
  noForcedLead: boolean;
  noConcern: boolean;
  /** Humanised finding label(s) for hero / Primary finding title. */
  primaryTitle: string | null;
  /** Lead “discuss first” sentence from structured concern-set fields only. */
  discussFirstSentence: string | null;
  urgencyPhrase: string | null;
  severityLabel: string | null;
  severityTone: 'rose' | 'amber' | 'slate' | 'emerald';
}

const CONFLICT_LEAD_RE =
  /\b(main pattern|discuss first|centres on|centers on|primary marker|best starting point)\b/i;

function humanizeFindingLabel(f: ClinicalFindingV1): string {
  const raw = (f.label || f.finding_type || '').trim();
  if (!raw) return 'Clinical finding';
  const spaced = raw.replace(/_/g, ' ');
  return spaced.charAt(0).toUpperCase() + spaced.slice(1);
}

export function formatUrgencyPhrase(band: ClinicalFindingUrgencyV1 | string | undefined): string {
  if (!band) return '';
  return String(band).replace(/_/g, ' ');
}

function severityFromFinding(f: ClinicalFindingV1 | undefined): {
  label: string;
  tone: 'rose' | 'amber' | 'slate' | 'emerald';
} {
  if (!f) return { label: 'Summary', tone: 'slate' };
  const urgency = f.urgency_time_band;
  const sev = (f.severity_band || '').toLowerCase();
  if (urgency === 'same_day' || sev === 'extreme' || sev === 'marked') {
    return {
      label: sev ? sev.replace(/_/g, ' ') : formatUrgencyPhrase(urgency),
      tone: urgency === 'same_day' ? 'rose' : 'amber',
    };
  }
  if (urgency === 'within_days') {
    return { label: formatUrgencyPhrase(urgency), tone: 'amber' };
  }
  if (urgency === 'within_weeks') {
    return { label: formatUrgencyPhrase(urgency), tone: 'slate' };
  }
  return { label: formatUrgencyPhrase(urgency) || 'Review in context', tone: 'emerald' };
}

function resolveLeadFindings(set: ConsolidatedConcernSetV1): {
  leads: ClinicalFindingV1[];
  coLeads: ClinicalFindingV1[];
} {
  const byId = new Map(set.findings.map((f) => [f.finding_id, f]));
  const leads = (set.lead_finding_ids || [])
    .map((id) => byId.get(id))
    .filter(Boolean) as ClinicalFindingV1[];
  const coLeads = (set.co_lead_finding_ids || [])
    .map((id) => byId.get(id))
    .filter(Boolean) as ClinicalFindingV1[];
  return { leads, coLeads };
}

function buildPrimaryTitle(
  set: ConsolidatedConcernSetV1,
  leads: ClinicalFindingV1[],
  coLeads: ClinicalFindingV1[]
): string | null {
  if (set.no_concern) {
    return 'No governed clinical concern identified';
  }
  if (set.no_forced_lead || set.presentation_mode === 'no_forced_lead') {
    const peers = [...leads, ...coLeads];
    if (peers.length === 0) {
      return 'Several findings share priority — no single lead is forced';
    }
    return peers.map(humanizeFindingLabel).join('; ');
  }
  if (set.presentation_mode === 'co_lead' && leads.length === 0 && coLeads.length > 0) {
    return coLeads.map(humanizeFindingLabel).join('; ');
  }
  if (leads.length > 0) {
    return humanizeFindingLabel(leads[0]);
  }
  if (coLeads.length > 0) {
    return coLeads.map(humanizeFindingLabel).join('; ');
  }
  return null;
}

function buildDiscussFirstSentence(
  set: ConsolidatedConcernSetV1,
  leads: ClinicalFindingV1[],
  coLeads: ClinicalFindingV1[],
  primaryTitle: string | null
): string | null {
  if (!primaryTitle) return null;
  if (set.no_concern) {
    return 'No governed clinical concern was identified on the markers assessed for this panel.';
  }
  if (set.no_forced_lead || set.presentation_mode === 'no_forced_lead') {
    return `Several findings share the same priority band with no governed distinguisher — no single lead is forced. Findings in view: ${primaryTitle}.`;
  }
  if (set.presentation_mode === 'co_lead' && (leads.length > 1 || (leads.length === 0 && coLeads.length > 1))) {
    return `More than one finding shares lead priority on this panel: ${primaryTitle}.`;
  }
  const lead = leads[0] || coLeads[0];
  const urgency = lead ? formatUrgencyPhrase(lead.urgency_time_band) : '';
  const urgencyClause = urgency ? ` (${urgency})` : '';
  return `Your results highlight ${primaryTitle.toLowerCase()} as the main pattern to discuss first${urgencyClause}.`;
}

/**
 * Canonical presentation-authority selector.
 * When a valid concern set is present it owns hero / primary finding / discuss-first copy.
 */
export function resolveClinicalPresentationAuthority(
  analysis: AnalysisResult | null | undefined
): ClinicalPresentationAuthority {
  const concernSet = getClinicalConcernSet(analysis);
  if (!concernSet || !hasClinicalConcernAuthority(analysis)) {
    return {
      source: 'legacy',
      concernSet: null,
      leadFindings: [],
      coLeadFindings: [],
      presentationMode: null,
      noForcedLead: false,
      noConcern: false,
      primaryTitle: null,
      discussFirstSentence: null,
      urgencyPhrase: null,
      severityLabel: null,
      severityTone: 'slate',
    };
  }

  const { leads, coLeads } = resolveLeadFindings(concernSet);
  // Malformed: claims authority but no usable findings and not no_concern → legacy fallback
  if (
    !concernSet.no_concern &&
    leads.length === 0 &&
    coLeads.length === 0 &&
    concernSet.findings.length === 0
  ) {
    return {
      source: 'legacy',
      concernSet,
      leadFindings: [],
      coLeadFindings: [],
      presentationMode: concernSet.presentation_mode,
      noForcedLead: Boolean(concernSet.no_forced_lead),
      noConcern: false,
      primaryTitle: null,
      discussFirstSentence: null,
      urgencyPhrase: null,
      severityLabel: null,
      severityTone: 'slate',
    };
  }

  const primaryTitle = buildPrimaryTitle(concernSet, leads, coLeads);
  const discussFirstSentence = buildDiscussFirstSentence(
    concernSet,
    leads,
    coLeads,
    primaryTitle
  );
  const lead = leads[0] || coLeads[0];
  const sev = severityFromFinding(lead);

  return {
    source: 'clinical_concern_set',
    concernSet,
    leadFindings: leads,
    coLeadFindings: coLeads,
    presentationMode: concernSet.presentation_mode,
    noForcedLead: Boolean(concernSet.no_forced_lead) || concernSet.presentation_mode === 'no_forced_lead',
    noConcern: Boolean(concernSet.no_concern),
    primaryTitle,
    discussFirstSentence,
    urgencyPhrase: lead ? formatUrgencyPhrase(lead.urgency_time_band) : null,
    severityLabel: sev.label,
    severityTone: sev.tone,
  };
}

/** True when narrative claims a primary/discuss-first lead that may conflict with concern set. */
export function narrativeConflictsWithConcernLead(
  narrative: string | null | undefined,
  authority: ClinicalPresentationAuthority
): boolean {
  if (authority.source !== 'clinical_concern_set') return false;
  const text = (narrative || '').trim();
  if (!text) return false;
  if (!CONFLICT_LEAD_RE.test(text)) return false;

  const lead = authority.leadFindings[0] || authority.coLeadFindings[0];
  if (!lead) return CONFLICT_LEAD_RE.test(text);

  const leadTokens = new Set<string>();
  leadTokens.add((lead.label || '').toLowerCase().replace(/_/g, ' '));
  leadTokens.add((lead.finding_type || '').toLowerCase());
  leadTokens.add(lead.domain.toLowerCase());
  for (const id of lead.constituent_biomarker_ids || []) {
    leadTokens.add(String(id).toLowerCase());
  }
  // Hepatic enzyme lead aliases
  if (lead.domain === 'hepatic' || /hepatic|hepatocellular|alt|enzyme/.test(lead.label)) {
    leadTokens.add('hepatic');
    leadTokens.add('hepatocellular');
    leadTokens.add('alt');
    leadTokens.add('liver');
    leadTokens.add('enzyme');
  }

  // First "main pattern / discuss first" sentence — if it names a non-lead topic, conflict.
  const sentences = text.split(/(?<=[.!?])\s+/);
  for (const s of sentences) {
    if (!CONFLICT_LEAD_RE.test(s)) continue;
    const lower = s.toLowerCase();
    const mentionsLead = Array.from(leadTokens).some((t) => t && lower.includes(t));
    if (!mentionsLead) return true;
  }
  return false;
}

/**
 * Prefer concern-set discuss-first sentence; drop conflicting legacy lead sentences;
 * keep remaining non-conflicting narrative as secondary context.
 */
export function resolveAuthoritativeBodyOverview(
  authority: ClinicalPresentationAuthority,
  compiledBodyOverview: string | null | undefined,
  legacyPrimarySentence: string
): string {
  if (authority.source !== 'clinical_concern_set' || !authority.discussFirstSentence) {
    return (compiledBodyOverview || '').trim() || legacyPrimarySentence;
  }

  const compiled = (compiledBodyOverview || '').trim();
  if (!compiled) return authority.discussFirstSentence;

  if (!narrativeConflictsWithConcernLead(compiled, authority)) {
    // Same lead family — still prefer structured discuss-first as opener, append rest if distinct
    if (compiled.toLowerCase().startsWith(authority.discussFirstSentence.toLowerCase().slice(0, 24))) {
      return compiled;
    }
    return `${authority.discussFirstSentence}\n\n${compiled}`;
  }

  const kept = compiled
    .split(/(?<=[.!?])\s+/)
    .map((s) => s.trim())
    .filter(Boolean)
    .filter((s) => !CONFLICT_LEAD_RE.test(s))
    .join(' ')
    .trim();

  if (!kept) return authority.discussFirstSentence;
  return `${authority.discussFirstSentence}\n\n${kept}`;
}

/**
 * Hero summary when concern set owns priority — never IDL/narrative MCV lead.
 */
export function resolveAuthoritativeHeroSummary(
  authority: ClinicalPresentationAuthority,
  legacySummary: string
): string {
  if (authority.source !== 'clinical_concern_set' || !authority.discussFirstSentence) {
    return legacySummary;
  }
  const parts = [authority.discussFirstSentence];
  if (authority.urgencyPhrase && !authority.discussFirstSentence.includes(authority.urgencyPhrase)) {
    parts.push(`Urgency band: ${authority.urgencyPhrase}.`);
  }
  return parts.join(' ');
}

/**
 * Subordinate broader-context line for IDL/cluster — never labelled as primary finding.
 */
export function broaderContextLineFromLegacyLabel(
  authority: ClinicalPresentationAuthority,
  legacyLabel: string | null | undefined
): string | null {
  if (authority.source !== 'clinical_concern_set') return null;
  const label = (legacyLabel || '').trim();
  if (!label) return null;
  const primary = (authority.primaryTitle || '').toLowerCase();
  if (primary && label.toLowerCase() === primary) return null;
  return `Broader pattern context: ${label}`;
}

/**
 * Lead narrative block: replace conflicting “main pattern / discuss first” with concern-set sentence.
 * Non-conflicting explanatory text may remain as secondary context.
 */
export function resolveAuthoritativeLeadNarrative(
  authority: ClinicalPresentationAuthority,
  legacyLeadNarrative: string | null | undefined
): string | null {
  if (authority.source !== 'clinical_concern_set' || !authority.discussFirstSentence) {
    return (legacyLeadNarrative || '').trim() || null;
  }
  const legacy = (legacyLeadNarrative || '').trim();
  if (!legacy) return authority.discussFirstSentence;
  if (!narrativeConflictsWithConcernLead(legacy, authority)) {
    const titleHint = (authority.primaryTitle || '').toLowerCase().slice(0, 20);
    if (titleHint && legacy.toLowerCase().includes(titleHint)) {
      return legacy;
    }
    return `${authority.discussFirstSentence}\n\n${legacy}`;
  }
  const kept = legacy
    .split(/(?<=[.!?])\s+/)
    .map((s) => s.trim())
    .filter(Boolean)
    .filter((s) => !CONFLICT_LEAD_RE.test(s))
    .join(' ')
    .trim();
  if (!kept) return authority.discussFirstSentence;
  return `${authority.discussFirstSentence}\n\n${kept}`;
}
