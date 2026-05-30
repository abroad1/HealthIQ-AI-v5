'use client';

import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { AlertCircle } from 'lucide-react';
import type { ResultVersioningMetadataV1 } from '@/types/analysis';

type Props = {
  versioning: ResultVersioningMetadataV1 | null | undefined;
};

export function StaleResultBanner({ versioning }: Props) {
  if (!versioning || versioning.result_status !== 'stale') {
    return null;
  }

  const message =
    versioning.user_message ||
    'This result was generated with an older analysis engine. Marker counts and labels may differ from current HealthIQ rules.';

  return (
    <Alert
      variant="default"
      className="border-amber-200 bg-amber-50/90 text-amber-950"
      data-testid="stale-result-banner"
    >
      <AlertCircle className="h-4 w-4 text-amber-700" />
      <AlertTitle className="text-amber-900">Generated using an older engine</AlertTitle>
      <AlertDescription className="text-sm text-amber-900/90 leading-relaxed">
        {message}
        {versioning.regeneration_available
          ? ' You can regenerate this panel with the latest engine as a new result version (coming soon).'
          : ' Re-run analysis on the same upload to create a new result version when regeneration is enabled.'}
      </AlertDescription>
    </Alert>
  );
}
