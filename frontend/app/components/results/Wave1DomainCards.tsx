'use client';

import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { ChevronDown, ChevronUp } from 'lucide-react';
import type { ConsumerDomainScoreV1 } from '@/types/analysis';

const WAVE1_ORDER: readonly string[] = [
  'wave1_cardiovascular',
  'wave1_blood_sugar',
  'wave1_liver',
];

function bandLabelDisplay(band: string): string {
  const m: Record<string, string> = {
    strong: 'Strong',
    stable: 'Stable',
    watch: 'Worth watching',
    review: 'Needs review',
  };
  return m[band] ?? band;
}

function tierLabel(t: string): string {
  if (t === 'high') return 'High confidence';
  if (t === 'medium') return 'Medium confidence';
  return 'Limited confidence';
}

type Props = {
  domains: ConsumerDomainScoreV1[] | null | undefined;
};

export function Wave1DomainCards({ domains }: Props) {
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

  return (
    <section aria-labelledby="wave1-domain-cards-heading" className="space-y-4">
      <div>
        <h2 id="wave1-domain-cards-heading" className="text-lg font-semibold text-slate-900">
          Your health domains (Wave 1)
        </h2>
        <p className="text-sm text-slate-600 mt-1">
          High-level scores for three focus areas. Open a card for detail — not a diagnosis.
        </p>
      </div>
      <div className="grid gap-4 md:grid-cols-1 lg:grid-cols-3">
        {ordered.map((d) => {
          const expanded = !!open[d.domain_id];
          const scorePct = Math.round(Math.max(0, Math.min(1, d.score)) * 100);
          const shortExpl = d.contributor_sentence
            ? d.contributor_sentence.length > 140
              ? `${d.contributor_sentence.slice(0, 137)}…`
              : d.contributor_sentence
            : d.clinical_label;

          return (
            <Card key={d.domain_id} className="border-slate-200 shadow-sm">
              <CardHeader className="pb-2">
                <CardTitle className="text-base font-semibold text-slate-900">{d.consumer_label}</CardTitle>
                <CardDescription className="text-xs text-slate-600 line-clamp-3">{shortExpl}</CardDescription>
              </CardHeader>
              <CardContent className="space-y-3 pt-0">
                <div className="flex flex-wrap items-baseline gap-2">
                  <span className="text-3xl font-bold text-indigo-700 tabular-nums">{scorePct}</span>
                  <span className="text-sm text-slate-500">/ 100</span>
                  <span className="ml-auto text-sm font-medium text-slate-700">{bandLabelDisplay(d.band_label)}</span>
                </div>
                <p className="text-xs font-medium text-slate-600">{tierLabel(d.confidence_tier)}</p>
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
                            <li key={m} className="font-mono text-xs">
                              {m}
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
