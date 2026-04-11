'use client'

import { useEffect } from 'react'
import { useParams, useRouter } from 'next/navigation'
import { emitWedgeEvent } from '@/lib/wedgeAnalytics'

/**
 * Canonical reopen entry: emit reopen event, flag results page for `entry: from_history`, then navigate.
 */
export default function AnalysisReopenRedirect() {
  const params = useParams()
  const router = useRouter()
  const raw = params?.id
  const id = typeof raw === 'string' ? raw : Array.isArray(raw) ? raw[0] : ''

  useEffect(() => {
    if (!id) return
    emitWedgeEvent({
      event_name: 'wedge_analysis_reopened_from_history',
      timestamp: new Date().toISOString(),
      route: '/analysis/[id]',
      analysis_id: id,
    })
    try {
      sessionStorage.setItem('wedge_reopen_flag', '1')
    } catch {
      /* ignore private mode */
    }
    router.replace(`/results?analysis_id=${encodeURIComponent(id)}`)
  }, [id, router])

  return (
    <div className="flex min-h-[40vh] items-center justify-center text-sm text-muted-foreground">
      Opening your results…
    </div>
  )
}
