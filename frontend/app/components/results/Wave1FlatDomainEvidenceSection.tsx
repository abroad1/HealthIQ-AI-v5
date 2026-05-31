'use client';

import React from 'react';
import type { DomainFlatEvidenceV1 } from '@/types/analysis';
import { consumerMarkerRoleLabel } from '@/lib/cardEvidenceConsumerCopy';

type Props = {
  evidence: DomainFlatEvidenceV1;
};

export function Wave1FlatDomainEvidenceSection({ evidence }: Props) {
  return (
    <section className="space-y-3" data-testid="wave1-flat-domain-evidence">
      <p className="text-xs font-semibold text-slate-500 uppercase tracking-wide">Panel evidence</p>
      <div className="rounded-lg border border-slate-200 bg-slate-50/40 p-3 space-y-2">
        {evidence.domain_summary_line ? (
          <p className="text-xs text-slate-600" data-testid="wave1-flat-domain-summary">
            {evidence.domain_summary_line}
          </p>
        ) : null}
        {evidence.mechanism_line ? (
          <p className="text-xs text-slate-600" data-testid="wave1-flat-domain-mechanism">
            {evidence.mechanism_line}
          </p>
        ) : null}
        {evidence.evidence_limitations_line ? (
          <p className="text-xs text-slate-500 italic" data-testid="wave1-flat-domain-limitations">
            {evidence.evidence_limitations_line}
          </p>
        ) : null}
        {evidence.included_marker_ids.length > 0 ? (
          <div className="space-y-1.5">
            <p className="text-[11px] font-semibold text-slate-500 uppercase tracking-wide">
              Included markers
            </p>
            <ul className="space-y-2 list-none p-0 m-0" data-testid="wave1-flat-domain-included">
              {(evidence.marker_evidence ?? [])
                .filter((m) => evidence.included_marker_ids.includes(m.marker_id))
                .map((marker) => {
                  const roleLabel = consumerMarkerRoleLabel(marker.marker_role);
                  return (
                    <li key={marker.marker_id} className="text-xs text-slate-700">
                      <span className="font-medium text-slate-900">{marker.display_label}</span>
                      {roleLabel ? (
                        <span className="ml-1 text-[10px] uppercase tracking-wide text-emerald-700">
                          {roleLabel}
                        </span>
                      ) : null}
                      {marker.rationale_short ? (
                        <p className="text-[11px] text-slate-600 mt-0.5 leading-snug">
                          {marker.rationale_short}
                        </p>
                      ) : null}
                    </li>
                  );
                })}
            </ul>
          </div>
        ) : null}
        {evidence.missing_marker_ids.length > 0 ? (
          <div className="space-y-1">
            {evidence.missing_policy_line ? (
              <p className="text-[11px] text-slate-500" data-testid="wave1-flat-domain-missing-policy">
                {evidence.missing_policy_line}
              </p>
            ) : null}
            <p className="text-[11px] font-semibold text-slate-500 uppercase tracking-wide">
              Not on this panel
            </p>
            <ul className="flex flex-wrap gap-1.5 list-none p-0 m-0" data-testid="wave1-flat-domain-missing">
              {(evidence.missing_markers ?? evidence.missing_marker_ids.map((id) => ({
                id,
                display_label: id,
              }))).map((marker) => (
                <li key={marker.id}>
                  <span className="inline-flex rounded-full border border-slate-200 bg-white px-2 py-0.5 text-xs text-slate-600">
                    {marker.display_label}
                  </span>
                </li>
              ))}
            </ul>
          </div>
        ) : null}
      </div>
    </section>
  );
}
