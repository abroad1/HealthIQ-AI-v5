'use client';

import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Link2 } from 'lucide-react';
import type { UploadedPanelFidelityRow } from '@/lib/uploadPanelFidelity';

interface UploadedPanelFidelityProps {
  rows: UploadedPanelFidelityRow[];
}

export default function UploadedPanelFidelity({ rows }: UploadedPanelFidelityProps) {
  if (!rows.length) return null;

  return (
    <section
      className="w-full space-y-3"
      aria-labelledby="uploaded-panel-fidelity-heading"
      data-testid="uploaded-panel-fidelity"
    >
      <div className="flex items-center gap-2 mb-1">
        <Link2 className="h-4 w-4 text-slate-600" aria-hidden />
        <h3 id="uploaded-panel-fidelity-heading" className="text-base font-semibold text-slate-900">
          Uploaded panel values
        </h3>
      </div>
      <p className="text-sm text-slate-600 max-w-3xl">
        Original units from your uploaded lab report. Canonical biomarker cards above use the analytical units used
        for interpretation. Values are shown exactly as received — nothing is recalculated in your browser.
      </p>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        {rows.map((row) => (
          <Card
            key={`${row.observationKey}-${row.unit}`}
            className="border-slate-200 bg-slate-50/80 shadow-sm"
          >
            <CardContent className="pt-4 pb-4">
              <div className="flex items-start justify-between gap-2 mb-2">
                <h4 className="font-medium text-slate-900 truncate">{row.displayLabel}</h4>
                {row.isEquivalentObservation ? (
                  <Badge
                    variant="outline"
                    className="text-xs shrink-0 border-violet-300 text-violet-900 bg-violet-50"
                  >
                    Equivalent
                  </Badge>
                ) : (
                  <Badge variant="outline" className="text-xs shrink-0 border-slate-300 text-slate-700">
                    Uploaded unit
                  </Badge>
                )}
              </div>
              <p className="text-2xl font-bold text-slate-900 tabular-nums">
                {row.value}{' '}
                <span className="text-base font-semibold text-slate-600">{row.unit}</span>
              </p>
              {row.equivalenceNote ? (
                <p className="text-xs text-slate-600 mt-2 leading-relaxed">{row.equivalenceNote}</p>
              ) : null}
            </CardContent>
          </Card>
        ))}
      </div>
    </section>
  );
}
