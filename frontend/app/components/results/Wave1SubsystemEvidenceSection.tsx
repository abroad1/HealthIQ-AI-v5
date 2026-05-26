import React from 'react';
import type { SubsystemEvidenceV1 } from '@/types/analysis';
import { wave1ConfidenceMarkerDisplayLabel } from '@/lib/wave1ConfidenceMarkerLabels';

type Props = {
  subsystems: SubsystemEvidenceV1[];
};

function isConsumerSafeSourceTrace(value: string | null | undefined): boolean {
  if (!value) return false;
  const trimmed = value.trim();
  if (!trimmed) return false;
  if (trimmed.includes('_') || trimmed.includes('/')) return false;
  return /^[A-Za-z0-9 ,.\-()]+$/.test(trimmed);
}

export function Wave1SubsystemEvidenceSection({ subsystems }: Props) {
  if (!subsystems.length) return null;

  return (
    <section className="space-y-3" data-testid="wave1-subsystems-section">
      <p className="text-xs font-semibold text-slate-500 uppercase tracking-wide">Evidence by subsystem</p>
      <div className="space-y-3">
        {subsystems.map((subsystem) => (
          <article
            key={subsystem.subsystem_id}
            className="rounded-lg border border-slate-200 bg-slate-50/40 p-3 space-y-2"
            data-testid={`wave1-subsystem-${subsystem.subsystem_id}`}
          >
            <div className="flex flex-wrap items-center gap-2">
              <h4 className="text-sm font-semibold text-slate-900">{subsystem.subsystem_label}</h4>
              {subsystem.status_label ? (
                <span
                  className="inline-flex items-center rounded-full border border-indigo-200 bg-indigo-50 px-2 py-0.5 text-[11px] font-medium text-indigo-800"
                  data-testid="wave1-subsystem-status"
                >
                  {subsystem.status_label}
                </span>
              ) : null}
            </div>

            {subsystem.included_marker_ids.length > 0 ? (
              <div className="space-y-1.5">
                <p className="text-[11px] font-semibold text-slate-500 uppercase tracking-wide">Included markers</p>
                <ul className="flex flex-wrap gap-1.5 list-none p-0 m-0" data-testid="wave1-subsystem-included">
                  {subsystem.included_marker_ids.map((markerId) => (
                    <li key={markerId}>
                      <span className="inline-flex items-center rounded-full border border-emerald-200 bg-emerald-50 px-2 py-0.5 text-xs text-emerald-800">
                        {wave1ConfidenceMarkerDisplayLabel(markerId)}
                      </span>
                    </li>
                  ))}
                </ul>
              </div>
            ) : null}

            {subsystem.missing_marker_ids.length > 0 ? (
              <div className="space-y-1.5">
                <p className="text-[11px] font-semibold text-slate-500 uppercase tracking-wide">Missing markers</p>
                <ul className="flex flex-wrap gap-1.5 list-none p-0 m-0" data-testid="wave1-subsystem-missing">
                  {subsystem.missing_marker_ids.map((markerId) => (
                    <li key={markerId}>
                      <span className="inline-flex items-center gap-1 rounded-full border border-slate-300 bg-slate-100 px-2 py-0.5 text-xs text-slate-600">
                        <span>{wave1ConfidenceMarkerDisplayLabel(markerId)}</span>
                        <span className="text-[10px] uppercase tracking-wide">Not uploaded</span>
                      </span>
                    </li>
                  ))}
                </ul>
              </div>
            ) : null}

            {isConsumerSafeSourceTrace(subsystem.source_trace) ? (
              <p className="text-xs text-slate-500" data-testid="wave1-subsystem-source-trace">
                Source: {subsystem.source_trace}
              </p>
            ) : null}
          </article>
        ))}
      </div>
    </section>
  );
}
