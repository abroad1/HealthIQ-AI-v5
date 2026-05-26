'use client';

import React from 'react';
import { wave1BandLabelDisplay } from '@/lib/wave1HealthSystemCardDisplay';

type Props = {
  /** 0–100 from backend DTO score (already rounded by parent). */
  scorePct: number;
  bandLabel: string;
  /** When true, de-emphasise the score ring to avoid overconfidence on thin evidence. */
  limitedCoverage?: boolean;
};

const RING_SIZE = 88;
const STROKE = 7;
const RADIUS = (RING_SIZE - STROKE) / 2;
const CIRCUMFERENCE = 2 * Math.PI * RADIUS;

export function Wave1HealthSystemScoreVisual({ scorePct, bandLabel, limitedCoverage = false }: Props) {
  const clamped = Math.max(0, Math.min(100, scorePct));
  const offset = CIRCUMFERENCE - (clamped / 100) * CIRCUMFERENCE;
  const bandDisplay = wave1BandLabelDisplay(bandLabel);

  return (
    <div
      className={`flex items-center gap-4 ${limitedCoverage ? 'opacity-95' : ''}`}
      data-testid="wave1-score-visual"
    >
      <div className="relative shrink-0" aria-hidden>
        <svg width={RING_SIZE} height={RING_SIZE} className="-rotate-90">
          <circle
            cx={RING_SIZE / 2}
            cy={RING_SIZE / 2}
            r={RADIUS}
            fill="none"
            stroke="currentColor"
            strokeWidth={STROKE}
            className="text-slate-100"
          />
          <circle
            cx={RING_SIZE / 2}
            cy={RING_SIZE / 2}
            r={RADIUS}
            fill="none"
            stroke="currentColor"
            strokeWidth={STROKE}
            strokeLinecap="round"
            strokeDasharray={CIRCUMFERENCE}
            strokeDashoffset={offset}
            className={limitedCoverage ? 'text-indigo-400' : 'text-indigo-600'}
          />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className="text-xl font-bold tabular-nums text-indigo-800 leading-none">{clamped}</span>
          <span className="text-[10px] font-medium text-slate-500 uppercase tracking-wide">/ 100</span>
        </div>
      </div>
      <div className="min-w-0 space-y-0.5">
        <p className="text-sm font-semibold text-slate-800" data-testid="wave1-band-label">
          {bandDisplay}
        </p>
        {limitedCoverage ? (
          <p className="text-xs text-amber-800" data-testid="wave1-limited-coverage-hint">
            Limited marker coverage on this panel
          </p>
        ) : null}
      </div>
    </div>
  );
}
