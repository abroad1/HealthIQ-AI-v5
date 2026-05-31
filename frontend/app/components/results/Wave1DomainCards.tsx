'use client';

import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { ChevronDown, ChevronUp } from 'lucide-react';
import type { ConsumerDomainScoreV1 } from '@/types/analysis';
import {
  wave1EvidenceCompletenessLine,
  wave1IsPartialEvidenceState,
  wave1IsZeroEvidenceState,
  wave1ScoreQualificationLine,
  wave1ScoreReliabilityLabel,
} from '@/lib/wave1HealthSystemCardDisplay';
import { Wave1HealthSystemScoreVisual } from './Wave1HealthSystemScoreVisual';
import { Wave1SubsystemEvidenceSection } from './Wave1SubsystemEvidenceSection';
import { Wave1FlatDomainEvidenceSection } from './Wave1FlatDomainEvidenceSection';

const WAVE1_ORDER: readonly string[] = [
  'wave1_cardiovascular',
  'wave1_blood_sugar',
  'wave1_liver',
];

type Props = {
  domains: ConsumerDomainScoreV1[] | null | undefined;
  /** When true, render as main-journey section with primary heading */
  embedInJourney?: boolean;
};

export function Wave1DomainCards({ domains, embedInJourney = false }: Props) {
  const [open, setOpen] = useState<Record<string, boolean>>({});

  if (!domains || domains.length === 0) {
    return null;
  }

  const byId = new Map(domains.map((d) => [d.domain_id, d]));
  const ordered: ConsumerDomainScoreV1[] = [];
  for (const id of WAVE1_ORDER) {
    const row = byId.get(id);
    if (row) ordered.push(row);
  }
  if (ordered.length === 0) {
    return null;
  }

  const headingId = embedInJourney ? 'fe-domain-ux1a-health-systems-heading' : 'wave1-domain-cards-heading';

  return (
    <section
      aria-labelledby={headingId}
      className="space-y-4"
      data-testid="fe-domain-ux1a-health-systems-cards"
    >
      <div>
        <h2
          id={headingId}
          className={
            embedInJourney ? 'text-xl font-semibold text-gray-900' : 'text-lg font-semibold text-slate-900'
          }
        >
          Your health systems
        </h2>
        <p className="text-sm text-slate-600 mt-1">
          How three focus areas look on your panel — scores from your markers, not a diagnosis. Open a card for
          detail.
        </p>
      </div>
      <div className="grid gap-4 sm:grid-cols-1 lg:grid-cols-3">
        {ordered.map((d) => {
          const expanded = !!open[d.domain_id];
          const descriptor = d.plain_english_descriptor?.trim();
          const shortExpl = descriptor || d.headline_sentence || d.contributor_sentence;
          const num = d.evidence_completeness_numerator ?? 0;
          const den = d.evidence_completeness_denominator ?? 0;
          const isZeroEvidence = wave1IsZeroEvidenceState(num, den);
          const isPartialEvidence = wave1IsPartialEvidenceState(num, den);
          const scorePct = Math.round(Math.max(0, Math.min(1, d.score)) * 100);
          const scoreReliability = wave1ScoreReliabilityLabel(d.confidence_tier);
          const evidenceCompleteness = wave1EvidenceCompletenessLine(num, den);
          const limitedCoverage =
            isPartialEvidence || d.confidence_tier === 'low' || scoreReliability === 'Limited reliability';
          const scoreQualification = wave1ScoreQualificationLine(scorePct, limitedCoverage, d.confidence_tier);

          return (
            <Card
              key={d.domain_id}
              className={`border shadow-sm overflow-hidden ${
                isZeroEvidence
                  ? 'border-amber-200/80 bg-gradient-to-b from-amber-50/40 to-white'
                  : isPartialEvidence
                    ? 'border-slate-200 bg-gradient-to-b from-slate-50/80 to-white'
                    : 'border-slate-200 bg-white'
              }`}
              data-testid={`wave1-card-${d.domain_id}`}
            >
              <CardHeader className="pb-3 space-y-1">
                <CardTitle className="text-base font-semibold text-slate-900 leading-snug">
                  {d.consumer_label}
                </CardTitle>
                {descriptor ? (
                  <p className="text-xs text-slate-500" data-testid="wave1-plain-english-descriptor">
                    {descriptor}
                  </p>
                ) : null}
                {d.evidence_anchor_sentence ? (
                  <p className="text-xs text-slate-500 border-l-2 border-indigo-200 pl-2 line-clamp-2">
                    {d.evidence_anchor_sentence}
                  </p>
                ) : null}
              </CardHeader>
              <CardContent className="space-y-3 pt-0">
                {isZeroEvidence ? (
                  <div
                    className="rounded-lg border border-amber-200 bg-amber-50/90 px-3 py-3 space-y-1"
                    data-testid="wave1-insufficient-data-state"
                  >
                    <p className="text-sm font-semibold text-amber-900">Not enough data</p>
                    <p className="text-xs text-amber-800 leading-relaxed">
                      This area needs more marker evidence before HealthIQ can score it meaningfully.
                    </p>
                  </div>
                ) : (
                  <div className="space-y-1">
                    <Wave1HealthSystemScoreVisual
                      scorePct={scorePct}
                      bandLabel={d.band_label}
                      limitedCoverage={limitedCoverage}
                    />
                    {scoreQualification ? (
                      <p
                        className="text-[11px] text-amber-800 leading-snug"
                        data-testid="wave1-score-qualification"
                      >
                        {scoreQualification}
                      </p>
                    ) : null}
                  </div>
                )}

                <div
                  className={`rounded-lg border px-3 py-2.5 grid grid-cols-1 sm:grid-cols-2 gap-3 ${
                    limitedCoverage && !isZeroEvidence
                      ? 'border-amber-100 bg-amber-50/30'
                      : 'border-slate-100 bg-slate-50/50'
                  }`}
                  data-testid="wave1-coverage-panel"
                >
                  <div className="space-y-0.5">
                    <p className="text-[10px] font-semibold text-slate-500 uppercase tracking-wide">
                      Score reliability
                    </p>
                    <p className="text-xs font-medium text-slate-800" data-testid="wave1-score-reliability">
                      {scoreReliability}
                    </p>
                  </div>
                  <div className="space-y-0.5">
                    <p className="text-[10px] font-semibold text-slate-500 uppercase tracking-wide">
                      Evidence completeness
                    </p>
                    <p className="text-xs text-slate-800" data-testid="wave1-evidence-completeness">
                      {evidenceCompleteness}
                    </p>
                  </div>
                </div>

                <p className="text-sm text-slate-800 leading-relaxed">{d.headline_sentence}</p>

                <Button
                  type="button"
                  variant="ghost"
                  size="sm"
                  className="w-full justify-between text-indigo-700 hover:text-indigo-900"
                  onClick={() =>
                    setOpen((o) => ({
                      ...o,
                      [d.domain_id]: !o[d.domain_id],
                    }))
                  }
                  aria-expanded={expanded}
                >
                  {expanded ? 'Show less' : 'More detail'}
                  {expanded ? <ChevronUp className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />}
                </Button>
                {expanded ? (
                  <div className="space-y-3 text-sm text-slate-700 border-t border-slate-100 pt-3">
                    <CardDescription className="text-xs text-slate-600">{shortExpl}</CardDescription>
                    <div>
                      <p className="text-xs font-semibold text-slate-500 uppercase tracking-wide">Why this score</p>
                      <p>{d.contributor_sentence}</p>
                    </div>
                    <div>
                      <p className="text-xs font-semibold text-slate-500 uppercase tracking-wide">Confidence</p>
                      <p>{d.confidence_sentence}</p>
                    </div>
                    <div>
                      <p className="text-xs font-semibold text-slate-500 uppercase tracking-wide">What this may mean</p>
                      <p>{d.consequence_sentence}</p>
                    </div>
                    <div>
                      <p className="text-xs font-semibold text-slate-500 uppercase tracking-wide">What to do next</p>
                      <p>{d.next_step_sentence}</p>
                    </div>
                    {d.caveat_flags.length > 0 ? (
                      <p className="text-xs text-amber-800 bg-amber-50 rounded px-2 py-1">
                        {d.caveat_flags.join(' · ')}
                      </p>
                    ) : null}
                    {d.subsystems && d.subsystems.length > 0 ? (
                      <Wave1SubsystemEvidenceSection subsystems={d.subsystems} />
                    ) : null}
                    {d.flat_domain_evidence ? (
                      <Wave1FlatDomainEvidenceSection evidence={d.flat_domain_evidence} />
                    ) : null}
                  </div>
                ) : null}
              </CardContent>
            </Card>
          );
        })}
      </div>
    </section>
  );
}
