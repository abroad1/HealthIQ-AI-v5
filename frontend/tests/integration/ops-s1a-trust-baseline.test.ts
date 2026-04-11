/**
 * OPS-S1A — targeted regression: UK B2C trust baseline on launch-facing surfaces.
 * Static source checks keep scope minimal (no full content-management suite).
 */

import fs from 'fs'
import path from 'path'

const appDir = path.join(__dirname, '../../app')

describe('OPS-S1A trust baseline (launch surfaces)', () => {
  it('landing page removes misaligned HIPAA / bank / medical-grade claims and placeholder legal anchors', () => {
    const landing = fs.readFileSync(path.join(appDir, 'page.tsx'), 'utf8')
    expect(landing).not.toMatch(/HIPAA/i)
    expect(landing).not.toMatch(/Bank-Level/i)
    expect(landing).not.toMatch(/Medical-Grade/i)
    expect(landing).not.toMatch(/href="#"/)
  })

  it('exposes real Privacy, Terms, Contact routes', () => {
    expect(fs.existsSync(path.join(appDir, 'privacy/page.tsx'))).toBe(true)
    expect(fs.existsSync(path.join(appDir, 'terms/page.tsx'))).toBe(true)
    expect(fs.existsSync(path.join(appDir, 'contact/page.tsx'))).toBe(true)
  })

  it('shared footer links to legal surfaces', () => {
    const footer = fs.readFileSync(path.join(appDir, 'components/layout/Footer.tsx'), 'utf8')
    expect(footer).toContain('href="/privacy"')
    expect(footer).toContain('href="/terms"')
    expect(footer).toContain('href="/contact"')
    expect(footer).not.toMatch(/href="#"/)
  })

  it('login page does not expose developer-only backend implementation string', () => {
    const login = fs.readFileSync(path.join(appDir, '(auth)/login/page.tsx'), 'utf8')
    expect(login).not.toMatch(/FastAPI/)
    expect(login).not.toMatch(/\/api\/auth/)
  })
})
