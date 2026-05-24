'use client';

import type { ClinicianConfirmatoryTestItem } from '@/types/analysis';
import { ClipboardList } from 'lucide-react';

export interface ConfirmatoryTestsNextStepsProps {
  tests: ClinicianConfirmatoryTestItem[] | null | undefined;
  maxVisible?: number;
  className?: string;
}

/**
 * FE-R3 — confirmatory tests with rationale in the retail "What to do next" journey section.
 */
export function ConfirmatoryTestsNextSteps({
  tests,
  maxVisible = 6,
  className = '',
}: ConfirmatoryTestsNextStepsProps) {
  const rows = (tests || []).filter((t) => (t.display_name || '').trim() && (t.rationale || '').trim());
  if (rows.length === 0) return null;

  const visible = rows.slice(0, maxVisible);

  return (
    <div className={className} data-testid="fe-r3-confirmatory-next-steps">
      <h3 className="text-sm font-semibold text-slate-800 mb-2 flex items-center gap-2">
        <ClipboardList className="h-4 w-4 text-slate-600" aria-hidden />
        Tests to discuss with your clinician
      </h3>
      <ul className="space-y-3 list-none p-0 m-0">
        {visible.map((t) => (
          <li key={t.test_id} className="text-sm border border-slate-200 rounded-md p-3 bg-white shadow-sm">
            <p className="font-medium text-slate-900">{t.display_name}</p>
            <p className="text-slate-700 mt-1 leading-relaxed">{t.rationale}</p>
          </li>
        ))}
      </ul>
      {rows.length > maxVisible ? (
        <p className="text-xs text-slate-500 mt-2">
          Additional tests are listed in the clinician summary when you need the full handoff view.
        </p>
      ) : null}
    </div>
  );
}
