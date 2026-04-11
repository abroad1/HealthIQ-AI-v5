/**
 * OPS-S1B — bounded regression: required operational/compliance artefacts exist on disk.
 */

import fs from 'fs'
import path from 'path'

/** Jest cwd is `frontend/` — repo root is one level up */
const repoRoot = path.join(process.cwd(), '..')

const REQUIRED_PATHS = [
  'docs/ops/README.md',
  'docs/ops/UK_HOSTING_AND_RESIDENCY_PHASE1.md',
  'docs/ops/VENDOR_SUBPROCESSOR_INVENTORY_PHASE1.md',
  'docs/ops/OPERATIONAL_CONTROLS_BASELINE_PHASE1.md',
  'docs/ops/OPEN_ITEMS_AND_PHASE1_BOUNDARIES.md',
  'docs/ops/WEDGE_METRICS_GOVERNANCE_NOTE_PHASE1.md',
  'docs/compliance/README.md',
  'docs/compliance/PRIVACY_RISK_REVIEW_PHASE1_EQUIVALENT.md',
  'docs/compliance/DATA_FLOW_LAUNCH_PRODUCT_PHASE1.md',
]

describe('OPS-S1B operational artefacts', () => {
  it.each(REQUIRED_PATHS)('exists: %s', (rel) => {
    const full = path.join(repoRoot, rel)
    if (!fs.existsSync(full)) {
      throw new Error(`Missing required artefact: ${rel} (looked in ${full})`)
    }
    expect(fs.existsSync(full)).toBe(true)
  })

  it('hosting artefact does not assert repo-enforced UK region (honesty string)', () => {
    const hosting = fs.readFileSync(
      path.join(repoRoot, 'docs/ops/UK_HOSTING_AND_RESIDENCY_PHASE1.md'),
      'utf8'
    )
    expect(hosting).toMatch(/no UK region is enforced|not.*repo.*enforce/i)
  })

  it('privacy risk review is labelled DPIA-equivalent / internal, not regulator-filed', () => {
    const dpi = fs.readFileSync(
      path.join(repoRoot, 'docs/compliance/PRIVACY_RISK_REVIEW_PHASE1_EQUIVALENT.md'),
      'utf8'
    )
    expect(dpi).toMatch(/DPIA-equivalent|equivalent/i)
  })
})
