/**
 * ARCH-CONV-CORRECT-1 — governed static copy for the "How to understand your results" section.
 *
 * These sentences explain how the product structures a panel (grouping, the meaning of the
 * words "stable" and "strain", and how single markers relate to a pattern). They are fixed
 * product copy: the only variable parts are names already decided by Layer B — the governed
 * primary-driver / cluster name, a balanced-systems topic, an IDL retail label, and marker
 * labels.
 *
 * Layer C must not add a cause, severity judgement, risk level or recommendation about the
 * reader here. Every template keeps the non-diagnostic qualifier that Layer B wording uses.
 */

export const SYSTEM_UNDERSTANDING_HEADINGS = {
  section: 'How to understand your results',
  grouping: 'Why your results are grouped',
  stableStrain: 'What “stable” and “strain” mean here',
  biggerPicture: 'How markers connect to the bigger picture',
} as const;

const GROUPING_PREAMBLE =
  'We organise markers into body systems so related results read together instead of in isolation.';

/** Block A — why results are grouped, naming the governed lead system and its markers. */
export function groupingCopy(args: { systemName: string | null; markerLabels: string[] }): string {
  const name = args.systemName?.trim();
  const labels = args.markerLabels.map((l) => l.trim()).filter(Boolean);

  if (!name) {
    return 'We group markers into body systems so related results read as connected signals, not scattered numbers. That structure is what lets a clear headline pattern emerge from the panel.';
  }
  if (labels.length >= 2) {
    return `${GROUPING_PREAMBLE} ${name} brings together markers such as ${labels[0]} and ${labels[1]}, in the same neighbourhood as the headline pattern above.`;
  }
  if (labels.length === 1) {
    return `${GROUPING_PREAMBLE} ${name} combines markers such as ${labels[0]}—near the headline pattern above.`;
  }
  return `${GROUPING_PREAMBLE} ${name} is one of the bundles we use to connect markers to the headline pattern above.`;
}

/** Block B — what "stable" and "strain" mean, naming governed systems only. */
export function stableStrainCopy(args: { stableTopic: string | null; leadName: string | null }): string {
  const topic = args.stableTopic?.trim() || null;
  const lead = args.leadName?.trim() || null;

  if (topic && lead) {
    return `Stable means a system looks broadly within range here; strain means several markers line up and need attention—not a diagnosis on its own. ${topic} appears among the stable systems named earlier, while ${lead} is the pattern our ranking placed first on this panel.`;
  }
  if (topic) {
    return `Stable means broadly within range for this snapshot; strain means several markers align and need attention—not a diagnosis on its own. ${topic} is one of the stable systems named earlier.`;
  }
  if (lead) {
    return `Here, stable means a system looks broadly within range for this snapshot. Strain means several markers align in the same direction, and ${lead} is the pattern our ranking placed first—without implying a diagnosis on its own.`;
  }
  return 'Stable systems are broadly within range for this snapshot. Where we describe strain, several markers are moving together in a way that deserves attention—that is where interpretation tightens, not a diagnosis on its own.';
}

/** Block C — how markers connect to the bigger picture. */
export function biggerPictureCopy(args: { leadName: string | null; idlRetailLabel: string | null }): string {
  const lead = args.leadName?.trim() || null;
  const idl = args.idlRetailLabel?.trim() || null;

  if (lead && idl) {
    return `Individual markers are single signals; the useful story is how they combine across systems. ${lead} organises markers for comparison, while the cross-body read “${idl}” summarises how related signals line up across the panel—both are on this page, answering different layers of the same investigation.`;
  }
  if (lead) {
    return `Individual markers are single signals; the useful story is how they combine across systems. When the evidence lines up, a pattern such as ${lead} can sit at the top—without resting on any one number in isolation.`;
  }
  return 'Individual markers are single signals; the useful story is how they combine across systems. That layered reading is what produces the headline you see first on this page.';
}
