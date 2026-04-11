/**
 * Phase 1 wedge event emission (WEDGE-METRICS-B).
 * First-party POST to backend `/api/wedge-events` — see docs/product/WEDGE_EVENT_CONTRACT_AND_GOVERNANCE_PHASE1.md
 */

import { API_BASE, getApiAuthHeaders } from './api'

export type WedgeEnv = 'development' | 'staging' | 'production'

export type WedgeEventPayload = {
  event_name: string
  timestamp: string
  env?: WedgeEnv
  route?: string
  analysis_id?: string
  entry?: 'fresh' | 'from_url' | 'from_history'
  source?: 'file' | 'paste'
  error_class?: string
  phase?: string
}

export function getWedgeEnv(): WedgeEnv {
  const v = process.env.NEXT_PUBLIC_VERCEL_ENV || process.env.NODE_ENV
  if (v === 'production') return 'production'
  if (v === 'preview' || v === 'staging') return 'staging'
  return 'development'
}

const onceEmitted = new Set<string>()

/**
 * Fire-and-forget first-party analytics. Never includes health payloads (callers must not pass them).
 */
export function emitWedgeEvent(payload: WedgeEventPayload): void {
  if (typeof window === 'undefined') return
  if (process.env.NEXT_PUBLIC_WEDGE_EVENTS_DISABLED === '1') return

  const body: WedgeEventPayload = {
    ...payload,
    timestamp: payload.timestamp || new Date().toISOString(),
    env: payload.env ?? getWedgeEnv(),
  }

  void fetch(`${API_BASE}/api/wedge-events`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', ...getApiAuthHeaders() },
    body: JSON.stringify(body),
    keepalive: true,
    credentials: 'omit',
  }).catch(() => {
    /* intentionally silent — analytics must not break UX */
  })
}

/** Dedupe high-churn events (e.g. SSE calling complete twice) within this tab session. */
export function emitWedgeEventOnce(dedupeKey: string, payload: WedgeEventPayload): void {
  if (onceEmitted.has(dedupeKey)) return
  onceEmitted.add(dedupeKey)
  emitWedgeEvent(payload)
}
