'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import type { ClinicalFindingV1, ConsolidatedConcernSetV1 } from '@/types/analysis';

export interface ClinicalConcernPrioritySectionProps {
  concernSet: ConsolidatedConcernSetV1 | null | undefined;
}

function formatLabel(f: ClinicalFindingV1): string {
  return (f.label || f.finding_type || '').replace(/_/g, ' ');
}

function urgencyLabel(band: string): string {
  return band.replace(/_/g, ' ');
}

/**
 * CLIN-PRIORITY-CORE-1 Checkpoint 5 — render-only clinical priority from server concern set.
 * Does not compute tier, urgency, lead, or ordering.
 */
export function ClinicalConcernPrioritySection({
  concernSet,
}: ClinicalConcernPrioritySectionProps) {
  if (!concernSet) return null;

  if (concernSet.no_concern) {
    return (
      <section
        aria-labelledby="clinical-concern-priority-heading"
        data-testid="clinical-concern-priority-section"
      >
        <Card className="border-emerald-100 bg-white shadow-sm">
          <CardHeader className="pb-2">
            <CardTitle
              id="clinical-concern-priority-heading"
              className="text-xl font-semibold text-gray-900"
            >
              Clinical priority
            </CardTitle>
          </CardHeader>
          <CardContent className="text-sm text-slate-700">
            <p data-testid="clinical-concern-no-concern">
              No governed clinical concern was identified on the markers assessed for this panel.
            </p>
            {(concernSet.no_concern_notes || []).length > 0 ? (
              <ul className="mt-2 list-disc pl-5 text-slate-600">
                {concernSet.no_concern_notes!.map((n) => (
                  <li key={n}>{n.replace(/_/g, ' ')}</li>
                ))}
              </ul>
            ) : null}
          </CardContent>
        </Card>
      </section>
    );
  }

  const byId = new Map(concernSet.findings.map((f) => [f.finding_id, f]));
  const leads = concernSet.lead_finding_ids
    .map((id) => byId.get(id))
    .filter(Boolean) as ClinicalFindingV1[];
  const coLeads = concernSet.co_lead_finding_ids
    .map((id) => byId.get(id))
    .filter(Boolean) as ClinicalFindingV1[];
  const secondary = concernSet.findings.filter(
    (f) =>
      !concernSet.lead_finding_ids.includes(f.finding_id) &&
      !concernSet.co_lead_finding_ids.includes(f.finding_id)
  );

  const mode = concernSet.presentation_mode;
  const modeCopy =
    mode === 'no_forced_lead'
      ? 'Several findings share the same priority band with no governed distinguisher — no single lead is forced.'
      : mode === 'co_lead'
        ? 'More than one finding shares lead priority on this panel.'
        : 'Priority order is supplied by the clinical concern set.';

  return (
    <section
      aria-labelledby="clinical-concern-priority-heading"
      data-testid="clinical-concern-priority-section"
    >
      <Card className="border-teal-100 bg-white shadow-sm">
        <CardHeader className="pb-2">
          <CardTitle
            id="clinical-concern-priority-heading"
            className="text-xl font-semibold text-gray-900"
          >
            Clinical priority
          </CardTitle>
          <p className="text-sm text-slate-600 pt-1" data-testid="clinical-concern-mode">
            {modeCopy}
          </p>
        </CardHeader>
        <CardContent className="space-y-4 text-sm text-gray-800">
          {concernSet.no_forced_lead || mode === 'no_forced_lead' ? (
            <p
              className="rounded-md border border-slate-200 bg-slate-50 px-3 py-2 text-slate-800"
              data-testid="clinical-concern-no-forced-lead"
            >
              No forced lead — co-equal findings are listed without inventing a winner.
            </p>
          ) : null}

          {leads.length > 0 ? (
            <div data-testid="clinical-concern-leads">
              <p className="text-xs font-semibold uppercase tracking-wide text-teal-900/80 mb-1">
                Lead
              </p>
              <ul className="space-y-2">
                {leads.map((f) => (
                  <FindingRow key={f.finding_id} finding={f} />
                ))}
              </ul>
            </div>
          ) : null}

          {coLeads.length > 0 ? (
            <div data-testid="clinical-concern-co-leads">
              <p className="text-xs font-semibold uppercase tracking-wide text-teal-900/80 mb-1">
                {mode === 'co_lead' && leads.length === 0 ? 'Same-day co-equal group' : 'Co-leads'}
              </p>
              <ul className="space-y-2">
                {coLeads.map((f) => (
                  <FindingRow key={f.finding_id} finding={f} />
                ))}
              </ul>
            </div>
          ) : null}

          {secondary.length > 0 ? (
            <div data-testid="clinical-concern-secondary">
              <p className="text-xs font-semibold uppercase tracking-wide text-slate-600 mb-1">
                Other concerns
              </p>
              <ul className="space-y-2">
                {secondary.map((f) => (
                  <FindingRow key={f.finding_id} finding={f} compact />
                ))}
              </ul>
            </div>
          ) : null}
        </CardContent>
      </Card>
    </section>
  );
}

function FindingRow({
  finding,
  compact = false,
}: {
  finding: ClinicalFindingV1;
  compact?: boolean;
}) {
  return (
    <li
      className="rounded-md border border-slate-100 bg-slate-50/80 px-3 py-2"
      data-testid={`clinical-finding-${finding.finding_type}`}
    >
      <p className={compact ? 'text-slate-800' : 'font-medium text-gray-900'}>
        {formatLabel(finding)}
      </p>
      <p className="text-xs text-slate-600 mt-1">
        Tier {finding.concern_tier} · {urgencyLabel(finding.urgency_time_band)}
        {finding.severity_band ? ` · ${finding.severity_band.replace(/_/g, ' ')}` : ''}
      </p>
      {!compact && finding.constituent_activation_keys?.length ? (
        <details className="mt-2 text-xs text-slate-500">
          <summary className="cursor-pointer">Constituent signals</summary>
          <ul className="mt-1 list-disc pl-4">
            {finding.constituent_activation_keys.map((k) => (
              <li key={k}>
                <code className="break-all">{k}</code>
              </li>
            ))}
          </ul>
        </details>
      ) : null}
      {!compact && (finding.caveats || []).length > 0 ? (
        <p className="mt-1 text-xs text-amber-900/90">
          {(finding.caveats || []).slice(0, 3).join(' · ').replace(/_/g, ' ')}
        </p>
      ) : null}
    </li>
  );
}
