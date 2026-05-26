'use client';

import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { ChevronDown, ChevronUp } from 'lucide-react';
import type { ConsumerDomainScoreV1 } from '@/types/analysis';
import { wave1ConfidenceMarkerDisplayLabel } from '@/lib/wave1ConfidenceMarkerLabels';
import {
  wave1BandLabelDisplay,
  wave1EvidenceCompletenessLine,
  wave1ScoreReliabilityLabel,
} from '@/lib/wave1HealthSystemCardDisplay';

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
      <div className="grid gap-4 md:grid-cols-1 lg:grid-cols-3">
        {ordered.map((d) => {
          const expanded = !!open[d.domain_id];
          const scorePct = Math.round(Math.max(0, Math.min(1, d.score)) * 100);
          const descriptor = d.plain_english_descriptor?.trim();
          const shortExpl = descriptor || d.headline_sentence || d.contributor_sentence;
          const num = d.evidence_completeness_numerator ?? 0;
          const den = d.evidence_completeness_denominator ?? 0;

          return (
            <Card key={d.domain_id} className="border-slate-200 shadow-sm" data-testid={`wave1-card-${d.domain_id}`}>
              <CardHeader className="pb-2">
                <CardTitle className="text-base font-semibold text-slate-900">{d.consumer_label}</CardTitle>
                {descriptor ? (
                  <p className="text-xs text-slate-500 mt-0.5" data-testid="wave1-plain-english-descriptor">
                    {descriptor}
                  </p>
                ) : null}
                <CardDescription className="text-xs text-slate-600 line-clamp-3">{shortExpl}</CardDescription>
                {d.evidence_anchor_sentence ? (
                  <p className="text-xs text-slate-500 mt-1.5 border-l-2 border-indigo-200 pl-2">
                    {d.evidence_anchor_sentence}
                  </p>
                ) : null}
              </CardHeader>
              <CardContent className="space-y-3 pt-0">
                <div className="flex flex-wrap items-baseline gap-2">
                  <span className="text-3xl font-bold text-indigo-700 tabular-nums">{scorePct}</span>
                  <span className="text-sm text-slate-500">/ 100</span>
                  <span
                    className="ml-auto text-sm font-medium text-slate-700"
                    data-testid="wave1-band-label"
                  >
                    {wave1BandLabelDisplay(d.band_label)}
                  </span>
                </div>
                <p className="text-xs font-medium text-slate-600" data-testid="wave1-score-reliability">
                  {wave1ScoreReliabilityLabel(d.confidence_tier)}
                </p>
                <p className="text-xs text-slate-600" data-testid="wave1-evidence-completeness">
                  {wave1EvidenceCompletenessLine(num, den)}
                </p>
                <p className="text-sm text-slate-800 border-t border-slate-100 pt-2">{d.headline_sentence}</p>
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
                    {d.missing_marker_ids.length > 0 ? (
                      <div>
                        <p className="text-xs font-semibold text-slate-500 uppercase tracking-wide">
                          What would improve confidence
                        </p>
                        <ul className="list-disc pl-4 space-y-1">
                          {d.missing_marker_ids.map((m) => (
                            <li key={m} className="text-sm text-slate-700">
                              {wave1ConfidenceMarkerDisplayLabel(m)}
                            </li>
                          ))}
                        </ul>
                      </div>
                    ) : null}
                    {d.caveat_flags.length > 0 ? (
                      <p className="text-xs text-amber-800 bg-amber-50 rounded px-2 py-1">
                        {d.caveat_flags.join(' · ')}
                      </p>
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
