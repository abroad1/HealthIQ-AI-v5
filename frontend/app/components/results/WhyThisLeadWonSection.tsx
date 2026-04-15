'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import type { ClinicianReportV1 } from '@/types/analysis';
import {
  buildConfidenceBlocksForSection4,
  isCloseCallMode,
  shouldRenderWhyThisLeadWonSection,
} from '@/lib/leadUncertaintySection';

export interface WhyThisLeadWonSectionProps {
  report: ClinicianReportV1 | null | undefined;
}

/**
 * FE-R3 Section 4 — Why this lead won / uncertainty (clinician_report deterministic fields only).
 */
export function WhyThisLeadWonSection({ report }: WhyThisLeadWonSectionProps) {
  if (!shouldRenderWhyThisLeadWonSection(report) || !report) {
    return null;
  }

  const p1 = report.sections.page1;
  const mode = p1.primary_concern_mode;
  const tie = isCloseCallMode(mode);
  const hasCo = (p1.co_primary_signal_ids?.filter(Boolean).length ?? 0) > 0;

  const runnerWhy = (p1.runner_up_why_not_lead_line || '').trim();
  const runnerTopic = (p1.runner_up_topic_line || '').trim();
  const showRunnerUpBlock = Boolean(runnerTopic) && tie;

  const { interpretationLimits, panelCaveatOrPointer } = buildConfidenceBlocksForSection4(report);

  const showWhyWon = Boolean(runnerWhy);
  const showCompeting = showRunnerUpBlock;
  const showConfidenceBlock = Boolean(interpretationLimits || panelCaveatOrPointer);

  /** Avoid repeating “close call” prose when the competing-finding block already carries the story. */
  const showTieCoPrimaryNote = tie && (!showCompeting || hasCo);

  if (!showWhyWon && !showCompeting && !showConfidenceBlock && !showTieCoPrimaryNote) {
    return null;
  }

  return (
    <section aria-labelledby="why-lead-won-heading" data-testid="why-this-lead-won-section">
      <Card className="border-violet-100 bg-white shadow-sm">
        <CardHeader className="pb-2">
          <CardTitle id="why-lead-won-heading" className="text-xl font-semibold text-gray-900">
            Why this lead won · uncertainty
          </CardTitle>
          <p className="text-sm text-gray-600 pt-1">
            How the headline was chosen, what else was close, and how much room for doubt remains on this panel.
          </p>
        </CardHeader>
        <CardContent className="space-y-6 text-sm text-gray-800">
          {showWhyWon ? (
            <div>
              <p className="text-xs font-semibold uppercase tracking-wide text-violet-900/80 mb-1">Why this lead won</p>
              <p className="leading-relaxed text-gray-900">{runnerWhy}</p>
            </div>
          ) : null}

          {showCompeting ? (
            <div className="rounded-md border border-violet-100 bg-violet-50/50 px-3 py-2">
              <p className="text-xs font-semibold uppercase tracking-wide text-violet-900/90 mb-1">Closest alternative</p>
              <p className="leading-relaxed">{runnerTopic}</p>
            </div>
          ) : null}

          {showTieCoPrimaryNote ? (
            <div className="rounded-md border border-slate-200 bg-slate-50/90 px-3 py-2 text-slate-800">
              <p className="text-xs font-semibold uppercase tracking-wide text-slate-600 mb-1">Close call</p>
              <p className="leading-relaxed">
                {hasCo
                  ? 'Several findings were similarly important on this panel; we still surface one lead first so the story has a clear starting point.'
                  : 'Two or more findings were close in strength; the sections above explain how focus was set.'}
              </p>
            </div>
          ) : null}

          {showConfidenceBlock ? (
            <div className="space-y-3 rounded-md border border-amber-100/80 bg-amber-50/30 px-3 py-3">
              <p className="text-xs font-semibold uppercase tracking-wide text-amber-950/90">Confidence and limits</p>
              {interpretationLimits ? (
                <p className="leading-relaxed text-amber-950/95 border-l-2 border-amber-300 pl-3">{interpretationLimits}</p>
              ) : null}
              {panelCaveatOrPointer ? (
                <p className="leading-relaxed text-amber-950/90 text-sm">{panelCaveatOrPointer}</p>
              ) : null}
            </div>
          ) : null}
        </CardContent>
      </Card>
    </section>
  );
}
