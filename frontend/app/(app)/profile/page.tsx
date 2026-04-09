'use client'

/**
 * FE-ACCOUNT-A — My Account shell. Read-only identity from `/api/auth/me`.
 * Editable profile and preferences belong to future sprints (contracts / FE-ACCOUNT-B).
 */

import { useEffect, useState } from 'react'
import Link from 'next/link'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import {
  LayoutDashboard,
  FileText,
  FileUp,
  Settings,
  LogOut,
  Loader2,
  UserCircle,
} from 'lucide-react'
import { useAuthStore } from '@/state/authStore'
import { AuthService } from '@/services/auth'
import type { MeResponse } from '@/types/auth'

function metadataNonEmpty(meta: Record<string, unknown> | undefined): boolean {
  return !!(meta && typeof meta === 'object' && Object.keys(meta).length > 0)
}

export default function ProfilePage() {
  const user = useAuthStore((s) => s.user)
  const initialized = useAuthStore((s) => s.initialized)
  const authLoading = useAuthStore((s) => s.loading)
  const logout = useAuthStore((s) => s.logout)

  const [me, setMe] = useState<MeResponse | null>(null)
  const [meLoading, setMeLoading] = useState(true)
  const [meError, setMeError] = useState<string | null>(null)

  useEffect(() => {
    if (!initialized) return
    let cancelled = false
    setMeLoading(true)
    setMeError(null)
    void (async () => {
      const res = await AuthService.fetchMe()
      if (cancelled) return
      if (res.success && res.data) {
        setMe(res.data)
      } else {
        setMeError(res.error ?? 'Could not load account details.')
        setMe(null)
      }
      setMeLoading(false)
    })()
    return () => {
      cancelled = true
    }
  }, [initialized])

  const email = me?.user.email ?? user?.email ?? ''
  const userId = me?.user.id ?? user?.id ?? ''

  const showAppMeta = metadataNonEmpty(me?.app_metadata)
  const showUserMeta = metadataNonEmpty(me?.user_metadata as Record<string, unknown>)

  if (!initialized) {
    return (
      <div className="container max-w-2xl py-16 flex flex-col items-center gap-3 text-muted-foreground">
        <Loader2 className="h-8 w-8 animate-spin" aria-hidden />
        <p className="text-sm">Loading session…</p>
      </div>
    )
  }

  if (meLoading) {
    return (
      <div className="container max-w-2xl py-16 flex flex-col items-center gap-3 text-muted-foreground">
        <Loader2 className="h-8 w-8 animate-spin" aria-hidden />
        <p className="text-sm">Loading your account…</p>
      </div>
    )
  }

  return (
    <div className="container max-w-2xl py-8 space-y-8">
      <div className="flex flex-col gap-2 sm:flex-row sm:items-start sm:justify-between">
        <div className="flex items-start gap-3">
          <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-full bg-muted">
            <UserCircle className="h-7 w-7 text-muted-foreground" aria-hidden />
          </div>
          <div>
            <h1 className="text-3xl font-bold tracking-tight">My account</h1>
            <p className="text-muted-foreground text-sm mt-1 max-w-prose">
              Signed-in identity for HealthIQ. This page is read-only; editing account fields is not
              available in the product yet.
            </p>
          </div>
        </div>
      </div>

      {meError ? (
        <Card className="border-destructive/50">
          <CardHeader className="pb-2">
            <CardTitle className="text-base text-destructive">Could not refresh account</CardTitle>
            <CardDescription>{meError}</CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground mb-3">
              Showing cached session where available. Try again or sign back in.
            </p>
            <Button asChild variant="outline" size="sm">
              <Link href="/login">Sign in</Link>
            </Button>
          </CardContent>
        </Card>
      ) : null}

      <Card>
        <CardHeader>
          <CardTitle className="text-lg">Identity</CardTitle>
          <CardDescription>From your current sign-in session (read-only).</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4 text-sm">
          <div>
            <p className="text-xs font-medium text-muted-foreground uppercase tracking-wide">Email</p>
            <p className="font-medium mt-1 break-all">{email || '—'}</p>
          </div>
          <div>
            <p className="text-xs font-medium text-muted-foreground uppercase tracking-wide">User id</p>
            <p className="font-mono text-xs mt-1 text-muted-foreground break-all">{userId || '—'}</p>
          </div>
        </CardContent>
      </Card>

      {(showAppMeta || showUserMeta) && (
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Sign-in provider data</CardTitle>
            <CardDescription>
              Read-only metadata supplied by your auth provider. Not used for medical analysis.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {showAppMeta ? (
              <div>
                <p className="text-xs font-medium text-muted-foreground mb-2">App metadata</p>
                <pre className="text-xs bg-muted rounded-md p-3 overflow-x-auto max-h-40 whitespace-pre-wrap break-all">
                  {JSON.stringify(me?.app_metadata, null, 2)}
                </pre>
              </div>
            ) : null}
            {showUserMeta ? (
              <div>
                <p className="text-xs font-medium text-muted-foreground mb-2">User metadata</p>
                <pre className="text-xs bg-muted rounded-md p-3 overflow-x-auto max-h-40 whitespace-pre-wrap break-all">
                  {JSON.stringify(me?.user_metadata, null, 2)}
                </pre>
              </div>
            ) : null}
          </CardContent>
        </Card>
      )}

      <Card>
        <CardHeader>
          <CardTitle className="text-lg">Go to</CardTitle>
          <CardDescription>Other areas of your account product.</CardDescription>
        </CardHeader>
        <CardContent className="flex flex-col gap-2 sm:flex-row sm:flex-wrap">
          <Button asChild variant="outline" size="sm" className="justify-start">
            <Link href="/dashboard">
              <LayoutDashboard className="h-4 w-4 mr-2" />
              Dashboard
            </Link>
          </Button>
          <Button asChild variant="outline" size="sm" className="justify-start">
            <Link href="/reports">
              <FileText className="h-4 w-4 mr-2" />
              Reports
            </Link>
          </Button>
          <Button asChild variant="outline" size="sm" className="justify-start">
            <Link href="/upload">
              <FileUp className="h-4 w-4 mr-2" />
              Upload
            </Link>
          </Button>
          <Button asChild variant="outline" size="sm" className="justify-start">
            <Link href="/settings">
              <Settings className="h-4 w-4 mr-2" />
              Settings
            </Link>
          </Button>
        </CardContent>
      </Card>

      <div className="h-px w-full bg-border" aria-hidden />

      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <p className="text-sm text-muted-foreground">
          To end your session on this device, sign out.
        </p>
        <Button
          variant="secondary"
          disabled={authLoading}
          onClick={() => {
            void logout().then(() => {
              window.location.href = '/login'
            })
          }}
        >
          <LogOut className="h-4 w-4 mr-2" />
          Sign out
        </Button>
      </div>
    </div>
  )
}
