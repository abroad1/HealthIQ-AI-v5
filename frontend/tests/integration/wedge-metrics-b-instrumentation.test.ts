/**
 * WEDGE-METRICS-B — instrumentation aligns manifest allowlist, backend validation,
 * and results-page semantics (JSON export vs clinician view — not PDF download).
 */

import fs from 'fs'
import path from 'path'

import { emitWedgeEvent } from '@/lib/wedgeAnalytics'

const repoRoot = path.join(process.cwd(), '..')

function wedgeNamesFromBackendPy(source: string): string[] {
  const names = new Set<string>()
  const re = /"wedge_[a-z0-9_]+"/g
  let m: RegExpExecArray | null
  while ((m = re.exec(source)) !== null) {
    names.add(m[0].slice(1, -1))
  }
  return [...names].sort()
}

describe('WEDGE-METRICS-B instrumentation', () => {
  it('keeps backend ALLOWED_EVENTS identical to manifest event_names', () => {
    const manifestPath = path.join(repoRoot, 'docs/product/wedge_events_phase1.manifest.json')
    const pyPath = path.join(repoRoot, 'backend/app/routes/wedge_events.py')
    const raw = fs.readFileSync(manifestPath, 'utf8')
    const py = fs.readFileSync(pyPath, 'utf8')
    const manifest = JSON.parse(raw) as { event_names: string[] }
    const fromPy = wedgeNamesFromBackendPy(py)
    const fromManifest = [...manifest.event_names].sort()
    expect(fromPy).toEqual(fromManifest)
  })

  it('does not list deferred-only events in manifest live list', () => {
    const manifestPath = path.join(repoRoot, 'docs/product/wedge_events_phase1.manifest.json')
    const raw = fs.readFileSync(manifestPath, 'utf8')
    const manifest = JSON.parse(raw) as {
      event_names: string[]
      deferred_event_names: string[]
    }
    for (const d of manifest.deferred_event_names) {
      expect(manifest.event_names).not.toContain(d)
    }
  })

  it('keeps JSON export and clinician view as distinct events on results page', () => {
    const resultsPath = path.join(repoRoot, 'frontend/app/(app)/results/page.tsx')
    const src = fs.readFileSync(resultsPath, 'utf8')
    expect(src).toMatch(/wedge_results_export_json_clicked/)
    expect(src).toMatch(/wedge_clinician_report_viewed/)
    expect(src).not.toMatch(/wedge_clinician_report_pdf_downloaded/)
  })
})

describe('emitWedgeEvent', () => {
  const originalFetch = global.fetch
  const originalDisabled = process.env.NEXT_PUBLIC_WEDGE_EVENTS_DISABLED

  beforeEach(() => {
    process.env.NEXT_PUBLIC_WEDGE_EVENTS_DISABLED = ''
    global.fetch = jest.fn().mockResolvedValue({ ok: true, status: 204 })
  })

  afterEach(() => {
    global.fetch = originalFetch
    process.env.NEXT_PUBLIC_WEDGE_EVENTS_DISABLED = originalDisabled
  })

  it('POSTs a minimised payload to the first-party wedge-events path', async () => {
    emitWedgeEvent({
      event_name: 'wedge_auth_login_success',
      timestamp: '2026-04-11T12:00:00.000Z',
      route: '/login',
    })
    await Promise.resolve()
    await Promise.resolve()

    expect(global.fetch).toHaveBeenCalled()
    const call = (global.fetch as jest.Mock).mock.calls[0]
    expect(call[0]).toContain('/api/wedge-events')
    expect(call[1].method).toBe('POST')
    expect(call[1].headers['Content-Type']).toBe('application/json')

    const body = JSON.parse(call[1].body as string)
    expect(body.event_name).toBe('wedge_auth_login_success')
    expect(body.timestamp).toBeTruthy()
    expect(body.env).toMatch(/development|staging|production/)
    expect(body).not.toHaveProperty('biomarkers')
    expect(body).not.toHaveProperty('questionnaire')
  })
})
