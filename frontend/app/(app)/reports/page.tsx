'use client'

import Link from 'next/link'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Loader2 } from 'lucide-react'
import { useHistory } from '../../hooks/useHistory'
import { friendlyHistoryError, savedAnalysisPrimaryLabel } from '@/lib/historyErrors'

function formatScore(s: number | null | undefined): string {
  if (s == null) return '—'
  if (s <= 1) return `${Math.round(s * 100)}%`
  return String(s)
}

export default function ReportsPage() {
  const { analyses, loading, error, total, page, limit, nextPage, prevPage } = useHistory({
    limit: 10,
    page: 1,
    autoFetch: true,
  })

  const totalPages = Math.max(1, Math.ceil(total / limit))

  return (
    <div className="container max-w-4xl py-8 space-y-6">
      <div>
        <h1 className="text-4xl font-bold tracking-tight">Reports</h1>
        <p className="text-muted-foreground mt-2">
          Saved analyses for your account. Open a row for the full interpretation and report.
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="text-lg">Analysis history</CardTitle>
          <CardDescription>
            {total} {total === 1 ? 'report' : 'reports'} total
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {loading ? (
            <div className="flex items-center gap-2 text-muted-foreground py-8 justify-center">
              <Loader2 className="h-4 w-4 animate-spin" />
              Loading…
            </div>
          ) : error ? (
            <Alert variant="destructive">
              <AlertDescription>
                <span className="font-semibold block mb-1">Could not load reports</span>
                {friendlyHistoryError(error)}
              </AlertDescription>
            </Alert>
          ) : analyses.length === 0 ? (
            <p className="text-sm text-muted-foreground py-6">
              No saved analyses yet.{' '}
              <Link href="/upload" className="text-primary underline underline-offset-4">
                Upload lab results
              </Link>{' '}
              to create your first run.
            </p>
          ) : (
            <>
              <ul className="divide-y rounded-md border">
                {analyses.map((row) => (
                  <li
                    key={row.id}
                    className="flex flex-wrap items-center justify-between gap-3 px-4 py-3 text-sm"
                  >
                    <div className="min-w-0">
                      <p className="font-medium text-sm truncate" title={row.id}>
                        {savedAnalysisPrimaryLabel(row.id).line}
                      </p>
                      <p className="text-muted-foreground text-xs">
                        {new Date(row.created_at).toLocaleString()} · {row.status}
                      </p>
                    </div>
                    <div className="flex items-center gap-3 shrink-0">
                      <span className="text-muted-foreground tabular-nums text-sm">
                        {formatScore(row.overall_score)}
                      </span>
                      <Button asChild size="sm">
                        <Link href={`/analysis/${encodeURIComponent(row.id)}`}>View results</Link>
                      </Button>
                    </div>
                  </li>
                ))}
              </ul>
              {totalPages > 1 ? (
                <div className="flex items-center justify-between pt-2">
                  <Button variant="outline" size="sm" onClick={prevPage} disabled={page <= 1}>
                    Previous
                  </Button>
                  <span className="text-xs text-muted-foreground tabular-nums">
                    Page {page} of {totalPages}
                  </span>
                  <Button variant="outline" size="sm" onClick={nextPage} disabled={page >= totalPages}>
                    Next
                  </Button>
                </div>
              ) : null}
            </>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
