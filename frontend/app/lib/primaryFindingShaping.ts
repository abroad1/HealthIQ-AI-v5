import type { ClinicianReportV1 } from '@/types/analysis';
import { buildBodyOverviewPrimarySentence } from '@/lib/bodyOverviewPrimarySentence';

export function firstSentence(text: string): string {
  const t = text.trim();
  if (!t) return '';
  const cut = t.match(/^(.+?[.!?])(\s|$)/);
  if (cut) return cut[1].trim();
  if (t.length <= 220) return t;
  return `${t.slice(0, 217).trim()}…`;
}

/**
 * Section 3A — lead line: grounded in page1, phrased for depth (must not duplicate Section 1 scan line verbatim).
 */
export function buildSection3LeadStatement(
  page1: ClinicianReportV1['sections']['page1'] | undefined
): string {
  if (!page1) {
    return "We've organised the clearest interpretation available from your report fields below.";
  }

  const section1Scan = buildBodyOverviewPrimarySentence(page1);
  const concern = (page1.primary_concern || '').trim();
  const hyp = (page1.top_hypothesis_line || '').trim();
  const kf0 = (page1.key_findings?.[0] || '').trim();

  if (!concern && !hyp && !kf0) {
    return "We've organised the clearest interpretation available from your report fields below.";
  }

  const chunks: string[] = [];
  if (concern) {
    chunks.push(`Main finding for this panel: ${firstSentence(concern)}`);
  }
  if (hyp) {
    chunks.push(`Leading explanation: ${firstSentence(hyp)}`);
  } else if (!concern && kf0) {
    chunks.push(`Clearest read from your key findings: ${firstSentence(kf0)}`);
  }

  const out = chunks.join(' ');
  if (out.trim() === section1Scan.trim()) {
    return `${out} The sections below spell out how evidence connects and what is still open.`;
  }
  return out;
}

/** Section 3B — deterministic “what this means” block (no new claims). */
export function buildWhatThisMeansBlock(page1: ClinicianReportV1['sections']['page1'] | undefined): string {
  if (!page1) return '';
  const topHyp = (page1.top_hypothesis_line || '').trim();
  const kf0 = (page1.key_findings?.[0] || '').trim();
  if (topHyp && kf0 && topHyp !== kf0) {
    return `${firstSentence(topHyp)} Supporting context: ${firstSentence(kf0)}`;
  }
  if (topHyp) return firstSentence(topHyp);
  if (kf0) return firstSentence(kf0);
  return '';
}
