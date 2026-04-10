'use client'

import Link from 'next/link'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { FileUp, FileText, Loader2 } from 'lucide-react'
import { useAuthStore } from '../../state/authStore'
import { useHistory } from '../../hooks/useHistory'
import { friendlyHistoryError, savedAnalysisPrimaryLabel } from '@/lib/historyErrors'

function formatScore(s: number | null | undefined): string {
  if (s == null) return '—'
  if (s <= 1) return `${Math.round(s * 100)}%`
  return String(s)
}

export default function DashboardPage() {
  const user = useAuthStore((s) => s.user)
  const displayName = user?.name?.trim() || user?.email?.split('@')[0] || 'there'
  const {
    analyses,
    loading,
    error,
    total,
  } = useHistory({ limit: 5, page: 1, autoFetch: true })

  return (
    <div className="container max-w-4xl py-8 space-y-8">
      <div>
        <h1 className="text-4xl font-bold tracking-tight">Dashboard</h1>
        <p className="text-muted-foreground mt-2">
          Hi {displayName} — start a new upload or open a saved analysis.
        </p>
      </div>

      <div className="grid gap-4 sm:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-lg">
              <FileUp className="h-5 w-5" />
              New analysis
            </CardTitle>
            <CardDescription>Upload or paste a lab file, then run a structured analysis.</CardDescription>
          </CardHeader>
          <CardContent>
            <Button asChild className="w-full sm:w-auto">
              <Link href="/upload">Go to upload</Link>
            </Button>
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-lg">
              <FileText className="h-5 w-5" />
              All reports
            </CardTitle>
            <CardDescription>View the full history and open any result.</CardDescription>
          </CardHeader>
          <CardContent>
            <Button asChild variant="secondary" className="w-full sm:w-auto">
              <Link href="/reports">View reports</Link>
            </Button>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <div>
            <CardTitle className="text-lg">Recent analyses</CardTitle>
            <CardDescription>
              {total > 0 ? `${total} saved in your account` : 'No saved analyses yet'}
            </CardDescription>
          </div>
          {total > 5 ? (
            <Button asChild variant="outline" size="sm">
              <Link href="/reports">See all</Link>
            </Button>
          ) : null}
        </CardHeader>
        <CardContent>
          {loading ? (
            <div className="flex items-center gap-2 text-muted-foreground py-6">
              <Loader2 className="h-4 w-4 animate-spin" />
              Loading history…
            </div>
          ) : error ? (
            <Alert variant="destructive">
              <AlertDescription>
                <span className="font-semibold block mb-1">Could not load recent analyses</span>
                {friendlyHistoryError(error)}
              </AlertDescription>
            </Alert>
          ) : analyses.length === 0 ? (
            <p className="text-sm text-muted-foreground py-4">
              When you complete an upload, your saved runs will appear here.{' '}
              <Link href="/upload" className="text-primary underline underline-offset-4">
                Go to upload
              </Link>
              .
            </p>
          ) : (
            <ul className="divide-y rounded-md border">
              {analyses.map((row) => (
                <li key={row.id} className="flex flex-wrap items-center justify-between gap-2 px-4 py-3 text-sm">
                  <div className="min-w-0">
                    <p className="font-medium truncate" title={row.id}>
                      {savedAnalysisPrimaryLabel(row.id).line}
                    </p>
                    <p className="text-muted-foreground text-xs">
                      {new Date(row.created_at).toLocaleString()} · {row.status}
                    </p>
                  </div>
                  <div className="flex items-center gap-3 shrink-0">
                    <span className="text-muted-foreground tabular-nums">
                      Score {formatScore(row.overall_score)}
                    </span>
                    <Button asChild size="sm" variant="default">
                      <Link href={`/analysis/${encodeURIComponent(row.id)}`}>Open</Link>
                    </Button>
                  </div>
                </li>
              ))}
            </ul>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
