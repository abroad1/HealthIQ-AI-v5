import type { ClinicianReportV1, PrimaryConcernModeV1 } from '@/types/analysis';

function trim(s: string | undefined | null): string {
  return (s || '').trim();
}

export function isCloseCallMode(mode: PrimaryConcernModeV1 | undefined): boolean {
  return mode === 'near_tie_ambiguity' || mode === 'technical_tiebreak_lead';
}

/**
 * Case 4 — omit Section 4 when no meaningful deterministic uncertainty assets exist.
 */
export function shouldRenderWhyThisLeadWonSection(report: ClinicianReportV1 | null | undefined): boolean {
  if (!report?.sections?.page1 || !report.data_quality) return false;

  const p1 = report.sections.page1;
  const dq = report.data_quality;

  const runnerWhy = trim(p1.runner_up_why_not_lead_line);
  const runnerTopic = trim(p1.runner_up_topic_line);
  const conf = trim(p1.confidence_and_missing_data);
  const caveat = trim(dq.confidence_caveat);
  const mode = p1.primary_concern_mode;
  const tie = isCloseCallMode(mode);
  const hasCo = (p1.co_primary_signal_ids?.filter(Boolean).length ?? 0) > 0;

  if (runnerWhy || runnerTopic) return true;
  if (conf) return true;
  if (caveat) return true;
  if (tie || (hasCo && tie)) return true;

  return false;
}

export interface ConfidenceMergeForSection4 {
  /** Interpretation-level confidence / missing-data line (page1). */
  interpretationLimits: string;
  /** Panel-level caveat — omitted when trust strip already surfaces the same failure prominently. */
  panelCaveatOrPointer: string | null;
}

/**
 * Merges page1 confidence text with data_quality.confidence_caveat without duplicating PipelineStatus.
 */
export function buildConfidenceBlocksForSection4(report: ClinicianReportV1): ConfidenceMergeForSection4 {
  const p1 = report.sections.page1;
  const dq = report.data_quality;
  const conf = trim(p1.confidence_and_missing_data);
  const caveat = trim(dq.confidence_caveat);
  const checksPassed = dq.data_quality_passed === true;

  let panelCaveatOrPointer: string | null = null;

  if (caveat) {
    if (checksPassed) {
      panelCaveatOrPointer = caveat;
    } else {
      panelCaveatOrPointer =
        'Panel-level quality caveats are summarised in the trust strip above — they affect how strongly you should lean on the headline.';
    }
  }

  return {
    interpretationLimits: conf,
    panelCaveatOrPointer,
  };
}
