/**
 * WEDGE-METRICS-A — bounded validation: governance artefacts exist and key semantics are explicit.
 * No application instrumentation is tested here (there is none yet).
 */

import fs from 'fs'
import path from 'path'

const repoRoot = path.join(process.cwd(), '..')

describe('WEDGE-METRICS-A event contract artefacts', () => {
  const contractPath = path.join(repoRoot, 'docs/product/WEDGE_EVENT_CONTRACT_AND_GOVERNANCE_PHASE1.md')
  const manifestPath = path.join(repoRoot, 'docs/product/wedge_events_phase1.manifest.json')

  it('creates the governance contract and manifest', () => {
    expect(fs.existsSync(contractPath)).toBe(true)
    expect(fs.existsSync(manifestPath)).toBe(true)
  })

  it('disambiguates JSON export vs clinician PDF (must not mislabel export as clinician download)', () => {
    const md = fs.readFileSync(contractPath, 'utf8')
    expect(md).toMatch(/wedge_results_export_json_clicked/i)
    expect(md).toMatch(/wedge_clinician_report_pdf_downloaded|deferred/i)
    expect(md).not.toMatch(/handleExportResults.*clinician_report_downloaded/i)
  })

  it('manifest JSON parses and lists core funnel events', () => {
    const raw = fs.readFileSync(manifestPath, 'utf8')
    const manifest = JSON.parse(raw) as { event_names: string[] }
    expect(manifest.event_names).toContain('wedge_auth_login_success')
    expect(manifest.event_names).toContain('wedge_analysis_completed')
    expect(manifest.event_names).toContain('wedge_clinician_report_viewed')
  })

  it('documents payload prohibitions', () => {
    const md = fs.readFileSync(contractPath, 'utf8')
    expect(md).toMatch(/Prohibited/i)
    expect(md).toMatch(/biomarker|health|questionnaire/i)
  })
})
