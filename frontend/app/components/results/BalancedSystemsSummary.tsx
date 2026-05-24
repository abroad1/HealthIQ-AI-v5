'use client';

import { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { CheckCircle2 } from 'lucide-react';
import { scrubBalancedSystemsEvidenceLine } from '@/lib/feR6aRetailCopy';

export interface BalancedSystemsV1 {
  intro_line: string;
  items: Array<{
    system_topic: string;
    evidence_line: string;
    capacity_note?: string;
  }>;
  context_line: string;
}

interface BalancedSystemsSummaryProps {
  balanced: BalancedSystemsV1 | null | undefined;
  /** When set with showMore, shows this many items before “Show more”. */
  initialVisibleCount?: number;
  /** When true and more items exist than `initialVisibleCount`, reveal the rest on demand. */
  expandBeyondInitial?: boolean;
  /** FE-R1 — cap list when not using expand (default 4). */
  maxItems?: number;
  /** Optional heading override; default matches results journey Section 2. */
  sectionTitle?: string;
}

const EMPTY_STABLE_COPY =
  "No clearly stable systems are highlighted in this panel — we'll guide you through the key findings below.";

/**
 * BE-W2-RQ3 — Surfaces deterministic “stable / reassuring” system groups from runtime meta
 * (system_states + optional capacity / supporting context). Not a second clinical authority.
 */
export function BalancedSystemsSummary({
  balanced,
  maxItems = 4,
  initialVisibleCount = 6,
  expandBeyondInitial = false,
  sectionTitle = "What's working well",
}: BalancedSystemsSummaryProps) {
  const [showAll, setShowAll] = useState(false);
  const all = balanced?.items?.length ? balanced.items : [];
  const items = expandBeyondInitial
    ? all.slice(0, showAll ? all.length : Math.min(initialVisibleCount, all.length))
    : all.slice(0, maxItems);
  const canShowMore = expandBeyondInitial && all.length > initialVisibleCount && !showAll;

  if (!balanced || !balanced.items?.length) {
    return (
      <Card
        className="border-emerald-100 bg-emerald-50/30 shadow-sm"
        data-testid="balanced-systems-summary-empty"
      >
        <CardHeader className="pb-2">
          <CardTitle className="text-lg font-semibold text-emerald-950 flex items-center gap-2">
            <CheckCircle2 className="h-5 w-5 text-emerald-700 shrink-0" aria-hidden />
            {sectionTitle}
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-emerald-950/90 leading-relaxed">{EMPTY_STABLE_COPY}</p>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="border-emerald-100 bg-emerald-50/40 shadow-sm" data-testid="balanced-systems-summary">
      <CardHeader className="pb-2">
        <CardTitle className="text-lg font-semibold text-emerald-950 flex items-center gap-2">
          <CheckCircle2 className="h-5 w-5 text-emerald-700 shrink-0" aria-hidden />
          {sectionTitle}
        </CardTitle>
        <CardDescription className="text-emerald-900/90">{balanced.intro_line}</CardDescription>
      </CardHeader>
      <CardContent className="space-y-4 text-sm text-emerald-950">
        <ul className="space-y-3">
          {items.map((it, idx) => (
            <li key={`${it.system_topic}-${idx}`} className="border-l-2 border-emerald-200 pl-3 max-w-prose">
              <p className="font-medium text-emerald-950">{it.system_topic}</p>
              <p className="text-emerald-900/90 mt-0.5 leading-relaxed">
                {scrubBalancedSystemsEvidenceLine(it.evidence_line)}
              </p>
              {it.capacity_note ? (
                <p className="text-emerald-800/80 text-xs mt-1">{it.capacity_note}</p>
              ) : null}
            </li>
          ))}
        </ul>
        {balanced.context_line ? (
          <p className="text-sm text-emerald-900 leading-relaxed border-t border-emerald-100 pt-3">
            {balanced.context_line}
          </p>
        ) : null}
        {canShowMore ? (
          <Button type="button" variant="ghost" className="px-0 text-emerald-900" onClick={() => setShowAll(true)}>
            Show more
          </Button>
        ) : null}
      </CardContent>
    </Card>
  );
}
