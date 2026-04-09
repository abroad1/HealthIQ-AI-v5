'use client'

/**
 * FE-PAGES-B — Saved analysis entry (gateway).
 *
 * Role: stable authenticated URL for a persisted analysis id. Verifies the result is
 * readable for the current session, then hands off to the governed results surface
 * at `/results?analysis_id=` (no duplicated results UX here).
 */

import { useEffect, useMemo, useState } from 'react'
import Link from 'next/link'
import { useParams, useRouter } from 'next/navigation'
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Loader2, AlertCircle } from 'lucide-react'
import { AnalysisService } from '@/services/analysis'
import { useAuthStore } from '@/state/authStore'

const UUID_RE =
  /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i

function classifyError(message: string): 'auth' | 'forbidden' | 'not_found' | 'invalid' | 'generic' {
  const m = message.toLowerCase()
  if (m.includes('invalid analysis_id')) return 'invalid'
  if (m.includes('401') || m.includes('authentication required') || m.includes('missing bearer'))
    return 'auth'
  if (m.includes('403') || m.includes('not allowed')) return 'forbidden'
  if (m.includes('404') || m.includes('not found')) return 'not_found'
  return 'generic'
}

export default function AnalysisDetailGatewayPage() {
  const params = useParams()
  const router = useRouter()
  const initialized = useAuthStore((s) => s.initialized)

  const rawId = params?.id
  const analysisId = typeof rawId === 'string' ? rawId : Array.isArray(rawId) ? rawId[0] : ''

  const idValid = useMemo(() => UUID_RE.test(analysisId), [analysisId])

  const [fetchError, setFetchError] = useState<{
    kind: 'auth' | 'forbidden' | 'not_found' | 'invalid' | 'generic'
    message: string
  } | null>(null)

  useEffect(() => {
    if (!initialized) return
    if (!analysisId) {
      setFetchError({
        kind: 'invalid',
        message: 'Missing analysis id.',
      })
      return
    }
    if (!idValid) {
      setFetchError({
        kind: 'invalid',
        message: 'This link does not look like a valid analysis id.',
      })
      return
    }

    let cancelled = false
    setFetchError(null)

    void (async () => {
      const res = await AnalysisService.getAnalysisResult(analysisId)
      if (cancelled) return
      if (res.success && res.data) {
        router.replace(`/results?analysis_id=${encodeURIComponent(analysisId)}`)
        return
      }
      const msg = res.error || 'Could not load this analysis.'
      setFetchError({ kind: classifyError(msg), message: msg })
    })()

    return () => {
      cancelled = true
    }
  }, [analysisId, idValid, initialized, router])

  if (!initialized) {
    return (
      <div className="container max-w-lg py-16 flex flex-col items-center gap-3 text-muted-foreground">
        <Loader2 className="h-8 w-8 animate-spin" aria-hidden />
        <p className="text-sm">Preparing your analysis…</p>
      </div>
    )
  }

  if (!fetchError) {
    return (
      <div className="container max-w-lg py-16 flex flex-col items-center gap-4">
        <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" aria-hidden />
        <Card className="w-full border-dashed">
          <CardHeader>
            <CardTitle className="text-base">Opening saved analysis</CardTitle>
            <CardDescription>
              Verifying access and loading your results — you&apos;ll be taken to the full results
              view.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-xs font-mono text-muted-foreground break-all">{analysisId}</p>
          </CardContent>
        </Card>
      </div>
    )
  }

  const loginNext = analysisId ? `/analysis/${encodeURIComponent(analysisId)}` : '/analysis'
  const errorKind = fetchError.kind

  return (
    <div className="container max-w-lg py-10 space-y-6">
      <Alert variant="destructive">
        <AlertCircle className="h-4 w-4" />
        <AlertTitle>
          {errorKind === 'not_found' && 'Analysis not found'}
          {errorKind === 'forbidden' && 'Access denied'}
          {errorKind === 'auth' && 'Sign in required'}
          {errorKind === 'invalid' && 'Invalid link'}
          {errorKind === 'generic' && 'Something went wrong'}
        </AlertTitle>
        <AlertDescription className="mt-2 space-y-3">
          <p>{fetchError.message}</p>
          {errorKind === 'auth' ? (
            <Button asChild size="sm" variant="secondary">
              <Link href={`/login?next=${encodeURIComponent(loginNext)}`}>Sign in</Link>
            </Button>
          ) : null}
          <div className="flex flex-wrap gap-2 pt-1">
            <Button asChild size="sm" variant="outline">
              <Link href="/reports">Back to reports</Link>
            </Button>
            <Button asChild size="sm" variant="outline">
              <Link href="/dashboard">Dashboard</Link>
            </Button>
          </div>
        </AlertDescription>
      </Alert>
    </div>
  )
}
