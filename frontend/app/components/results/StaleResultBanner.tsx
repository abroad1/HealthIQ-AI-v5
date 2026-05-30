'use client';

import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { AlertCircle } from 'lucide-react';
import type { ResultVersioningMetadataV1 } from '@/types/analysis';

type Props = {
  versioning: ResultVersioningMetadataV1 | null | undefined;
};

export function StaleResultBanner({ versioning }: Props) {
  const status = versioning?.result_status;
  if (!versioning || (status !== 'stale' && status !== 'incompatible')) {
    return null;
  }

  const isIncompatible = status === 'incompatible';
  const title = isIncompatible
    ? 'This saved result uses an older format'
    : 'Generated using an older engine';

  const message =
    versioning.user_message ||
    (isIncompatible
      ? 'This saved result cannot be displayed with the current results page contract. Some sections may be missing or out of date.'
      : 'This result was generated with an older analysis engine. Marker counts and labels may differ from current HealthIQ rules.');

  return (
    <Alert
      variant="default"
      className="border-amber-200 bg-amber-50/90 text-amber-950"
      data-testid="stale-result-banner"
    >
      <AlertCircle className="h-4 w-4 text-amber-700" />
      <AlertTitle className="text-amber-900">{title}</AlertTitle>
      <AlertDescription className="text-sm text-amber-900/90 leading-relaxed">
        {message}
        {versioning.regeneration_available
          ? ' You can regenerate this panel with the latest engine as a new result version (coming soon).'
          : ' Re-run analysis on the same upload to create a new result version when regeneration is enabled.'}
      </AlertDescription>
    </Alert>
  );
}
