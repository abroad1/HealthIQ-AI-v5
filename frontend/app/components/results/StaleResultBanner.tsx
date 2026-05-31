'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { Button } from '@/components/ui/button';
import { AlertCircle } from 'lucide-react';
import type { ResultVersioningMetadataV1 } from '@/types/analysis';

type Props = {
  versioning: ResultVersioningMetadataV1 | null | undefined;
  analysisId?: string | null;
};

export function StaleResultBanner({ versioning, analysisId }: Props) {
  const router = useRouter();
  const [pending, setPending] = useState(false);
  const [error, setError] = useState<string | null>(null);

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

  const handleRegenerate = async () => {
    if (!analysisId || pending) return;
    setPending(true);
    setError(null);
    try {
      const res = await fetch(`/api/analysis/${encodeURIComponent(analysisId)}/regenerate`, {
        method: 'POST',
        credentials: 'include',
      });
      const body = await res.json().catch(() => ({}));
      if (!res.ok) {
        const msg =
          (body?.detail && typeof body.detail === 'object' && body.detail.message) ||
          body?.detail ||
          'Regeneration failed';
        setError(typeof msg === 'string' ? msg : 'Regeneration failed');
        return;
      }
      const newId = body?.analysis_id;
      if (typeof newId === 'string' && newId.trim()) {
        router.push(`/results?analysis_id=${encodeURIComponent(newId.trim())}`);
        return;
      }
      setError('Regeneration succeeded but no new analysis id was returned.');
    } catch {
      setError('Regeneration failed. Please try again or upload the panel again.');
    } finally {
      setPending(false);
    }
  };

  return (
    <Alert
      variant="default"
      className="border-amber-200 bg-amber-50/90 text-amber-950"
      data-testid="stale-result-banner"
    >
      <AlertCircle className="h-4 w-4 text-amber-700" />
      <AlertTitle className="text-amber-900">{title}</AlertTitle>
      <AlertDescription className="text-sm text-amber-900/90 leading-relaxed space-y-3">
        <p>{message}</p>
        {versioning.regeneration_available && analysisId ? (
          <div className="flex flex-wrap items-center gap-2">
            <Button
              type="button"
              size="sm"
              variant="outline"
              className="border-amber-300 bg-white text-amber-950 hover:bg-amber-100"
              disabled={pending}
              onClick={handleRegenerate}
              data-testid="regenerate-result-button"
            >
              {pending ? 'Regenerating…' : 'Regenerate with latest engine'}
            </Button>
          </div>
        ) : (
          <p className="text-xs text-amber-800/90">
            {versioning.regeneration_unavailable_reason ||
              'Upload the panel again to create a new result with the latest engine.'}
          </p>
        )}
        {error ? <p className="text-xs text-red-800">{error}</p> : null}
      </AlertDescription>
    </Alert>
  );
}
