'use client';

import { Suspense, useEffect, useState } from 'react';
import Link from 'next/link';
import { useSearchParams } from 'next/navigation';
import { Check, CreditCard, Loader2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { BILLING_FREE_SUMMARY, BILLING_PLAN_NAME, BILLING_PRICE_LABEL } from '@/lib/billingConfig';
import { BillingService } from '@/services/billing';
import { AuthService } from '@/services/auth';
import { useAuthStore } from '@/state/authStore';

const INCLUDED = [
  'Unlimited structured blood test analyses while subscribed',
  'Full results journey, trends, and PDF summary (where enabled)',
  'Secure history — past completed analyses stay available',
];

function PricingContent() {
  const searchParams = useSearchParams();
  const user = useAuthStore((s) => s.user);
  const [checkoutLoading, setCheckoutLoading] = useState(false);
  const [checkoutError, setCheckoutError] = useState<string | null>(null);
  const [refreshNote, setRefreshNote] = useState<string | null>(null);

  useEffect(() => {
    const c = searchParams.get('checkout');
    if (c === 'success') {
      setRefreshNote('Payment received. Refreshing your account…');
      void AuthService.getCurrentUserFromServer().then((r) => {
        if (r.success) {
          const u = AuthService.getCurrentUser();
          if (u) useAuthStore.setState({ user: u });
          setRefreshNote(
            'Your subscription status will update in a moment. If it still shows as free, wait a few seconds and refresh this page.'
          );
        } else {
          setRefreshNote('Could not refresh session automatically. Please reload the page.');
        }
      });
    } else if (c === 'cancelled') {
      setRefreshNote('Checkout was cancelled. You can subscribe any time from this page.');
    }
  }, [searchParams]);

  const handleSubscribe = async () => {
    setCheckoutError(null);
    setCheckoutLoading(true);
    try {
      const res = await BillingService.createCheckoutSession();
      if (!res.success || !res.data?.url) {
        setCheckoutError(res.error || 'Checkout could not be started. Is billing configured on the server?');
        return;
      }
      window.location.href = res.data.url;
    } finally {
      setCheckoutLoading(false);
    }
  };

  const sub = user?.subscription_status ?? '—';

  return (
    <div className="container max-w-3xl py-10 space-y-8">
      <div>
        <div className="flex items-center gap-2 text-indigo-700 mb-1">
          <CreditCard className="h-6 w-6" aria-hidden />
          <span className="text-sm font-semibold uppercase tracking-wide">Pricing</span>
        </div>
        <h1 className="text-3xl font-bold tracking-tight">HealthIQ subscription</h1>
        <p className="text-muted-foreground mt-2 max-w-prose">
          {BILLING_FREE_SUMMARY} Past results you already generated remain available without a subscription.
        </p>
      </div>

      {refreshNote ? (
        <Alert>
          <AlertDescription>{refreshNote}</AlertDescription>
        </Alert>
      ) : null}

      {checkoutError ? (
        <Alert variant="destructive">
          <AlertDescription>{checkoutError}</AlertDescription>
        </Alert>
      ) : null}

      <Card>
        <CardHeader>
          <CardTitle className="text-xl">{BILLING_PLAN_NAME}</CardTitle>
          <CardDescription>
            <span className="text-2xl font-semibold text-foreground">{BILLING_PRICE_LABEL}</span>
            <span className="block mt-2 text-sm font-normal text-muted-foreground">
              Commercial wording and currency should be confirmed for your market — the amount is finalized in Stripe
              Checkout (test mode in development).
            </span>
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          <div>
            <p className="text-sm font-medium text-muted-foreground mb-2">Included</p>
            <ul className="space-y-2">
              {INCLUDED.map((line) => (
                <li key={line} className="flex gap-2 text-sm">
                  <Check className="h-4 w-4 shrink-0 text-emerald-600 mt-0.5" aria-hidden />
                  <span>{line}</span>
                </li>
              ))}
            </ul>
          </div>

          <div className="rounded-md border bg-muted/30 px-3 py-2 text-xs text-muted-foreground">
            Current account status: <strong className="text-foreground">{sub}</strong>
          </div>

          <div className="flex flex-wrap gap-3">
            <Button type="button" onClick={() => void handleSubscribe()} disabled={checkoutLoading}>
              {checkoutLoading ? (
                <>
                  <Loader2 className="h-4 w-4 mr-2 animate-spin" aria-hidden />
                  Opening checkout…
                </>
              ) : (
                <>
                  <CreditCard className="h-4 w-4 mr-2" aria-hidden />
                  Subscribe with Stripe
                </>
              )}
            </Button>
            <Button asChild variant="outline">
              <Link href="/dashboard">Back to dashboard</Link>
            </Button>
          </div>

          <p className="text-xs text-muted-foreground">
            Manage or cancel from <Link href="/settings">Settings</Link> → Billing (Stripe Customer Portal) once you
            have an active subscription.
          </p>
        </CardContent>
      </Card>

      <p className="text-xs text-muted-foreground">
        HealthIQ is for information and education only. It is not a medical diagnosis. Subscription does not replace
        advice from a qualified clinician.
      </p>
    </div>
  );
}

export default function PricingPage() {
  return (
    <Suspense
      fallback={
        <div className="container max-w-3xl py-16 flex items-center gap-2 text-muted-foreground">
          <Loader2 className="h-5 w-5 animate-spin" aria-hidden />
          Loading…
        </div>
      }
    >
      <PricingContent />
    </Suspense>
  );
}
