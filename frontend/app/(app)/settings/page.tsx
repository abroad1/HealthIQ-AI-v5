'use client'

/**
 * FE-ACCOUNT-B — Preferences / settings (local, truthful).
 * Appearance uses next-themes (same contract as Header). No server sync.
 */

import { useEffect, useState } from 'react'
import Link from 'next/link'
import { useTheme } from 'next-themes'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Sun, Moon, UserCircle, CreditCard, Loader2 } from 'lucide-react'
import { BillingService } from '@/services/billing'

export default function SettingsPage() {
  const { theme, setTheme, resolvedTheme } = useTheme()
  const [mounted, setMounted] = useState(false)
  const [portalLoading, setPortalLoading] = useState(false)
  const [portalError, setPortalError] = useState<string | null>(null)

  useEffect(() => {
    setMounted(true)
  }, [])

  const active = (resolvedTheme || theme || 'dark') as string

  return (
    <div className="container max-w-2xl py-8 space-y-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Settings</h1>
        <p className="text-muted-foreground text-sm mt-2 max-w-prose">
          Preferences for how HealthIQ looks on this device. Account details and sign-in stay under{' '}
          <Link href="/profile" className="text-primary underline underline-offset-4">
            My account
          </Link>
          .
        </p>
      </div>

      <p className="text-xs text-muted-foreground rounded-md border border-dashed bg-muted/30 px-3 py-2">
        These settings apply in <strong className="font-medium text-foreground">this browser only</strong> and are{' '}
        <strong className="font-medium text-foreground">not synced</strong> to your HealthIQ account or other devices.
      </p>

      <Card>
        <CardHeader>
          <CardTitle className="text-lg">Appearance</CardTitle>
          <CardDescription>
            Light or dark interface. Matches the theme control in the header.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {!mounted ? (
            <p className="text-sm text-muted-foreground">Loading appearance…</p>
          ) : (
            <div className="flex flex-wrap gap-2">
              <Button
                type="button"
                variant={active === 'light' ? 'default' : 'outline'}
                size="sm"
                className="gap-2"
                onClick={() => setTheme('light')}
              >
                <Sun className="h-4 w-4" aria-hidden />
                Light
              </Button>
              <Button
                type="button"
                variant={active === 'dark' ? 'default' : 'outline'}
                size="sm"
                className="gap-2"
                onClick={() => setTheme('dark')}
              >
                <Moon className="h-4 w-4" aria-hidden />
                Dark
              </Button>
            </div>
          )}
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="text-lg">Account</CardTitle>
          <CardDescription>Identity and session — not edited here.</CardDescription>
        </CardHeader>
        <CardContent>
          <Button asChild variant="outline" size="sm" className="gap-2">
            <Link href="/profile">
              <UserCircle className="h-4 w-4" aria-hidden />
              Open My account
            </Link>
          </Button>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="text-lg flex items-center gap-2">
            <CreditCard className="h-5 w-5" aria-hidden />
            Billing
          </CardTitle>
          <CardDescription>Subscribe or open the Stripe customer portal to cancel or update payment details.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-3">
          {portalError ? (
            <p className="text-sm text-destructive">{portalError}</p>
          ) : null}
          <div className="flex flex-wrap gap-2">
            <Button asChild size="sm">
              <Link href="/pricing">Pricing & subscribe</Link>
            </Button>
            <Button
              type="button"
              variant="outline"
              size="sm"
              disabled={portalLoading}
              onClick={() => {
                setPortalError(null)
                setPortalLoading(true)
                void BillingService.createPortalSession().then((r) => {
                  setPortalLoading(false)
                  if (r.success && r.data?.url) {
                    window.location.href = r.data.url
                  } else {
                    setPortalError(r.error || 'Could not open billing portal.')
                  }
                })
              }}
            >
              {portalLoading ? (
                <>
                  <Loader2 className="h-4 w-4 mr-2 animate-spin" aria-hidden />
                  Opening…
                </>
              ) : (
                'Manage subscription (Stripe)'
              )}
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
