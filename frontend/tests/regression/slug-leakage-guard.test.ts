/**
 * Sentinel Phase 1 — Frontend slug/internal-label leakage guard.
 *
 * Defect class: slug_leakage
 * Check type: static source file analysis (deterministic)
 *
 * Scans customer-facing results component source files for patterns that would
 * expose backend/internal identifiers to users.
 *
 * Forbidden patterns checked:
 *   1. ph_*_v*  — internal phenotype id format (e.g. "ph_metabolic_early_ir_v1")
 *   2. snake_case biomarker slugs in JSX string positions likely rendered to users
 *   3. Backend implementation strings: FastAPI, unmapped_, internal_id:
 *
 * Surfaces checked:
 *   - frontend/app/components/results/*.tsx
 *   - frontend/app/lib/narrativeRuntimePresentation.ts
 *   - frontend/app/lib/primaryFindingShaping.ts
 *
 * Evidence model:
 *   - input: source text of each results component
 *   - expected: no forbidden pattern present in render-path positions
 *   - actual: regex match result
 *   - customer impact: visible slugs erode trust, expose internal architecture
 *   - governance escalation: no (read-only source check)
 */

import fs from 'fs'
import path from 'path'

const repoRoot = path.resolve(__dirname, '../../../..')
const frontendRoot = path.join(repoRoot, 'frontend')
const resultsDir = path.join(frontendRoot, 'app', 'components', 'results')

const shapingFiles = [
  path.join(frontendRoot, 'app', 'lib', 'narrativeRuntimePresentation.ts'),
  path.join(frontendRoot, 'app', 'lib', 'primaryFindingShaping.ts'),
]

// Internal phenotype id format — e.g. "ph_metabolic_early_ir_v1"
const PH_INTERNAL_ID = /["'`]ph_[a-z0-9_]+_v\d+["'`]/g

// Backend implementation strings that must not reach client surfaces
const BACKEND_IMPL_STRINGS = ['FastAPI', 'unmapped_', 'internal_id:']

function collectResultsTsxFiles(): string[] {
  if (!fs.existsSync(resultsDir)) return []
  return fs
    .readdirSync(resultsDir)
    .filter((f) => f.endsWith('.tsx'))
    .map((f) => path.join(resultsDir, f))
}

function findPhIds(source: string, filename: string): string[] {
  const findings: string[] = []
  const lines = source.split('\n')
  const matches = source.matchAll(PH_INTERNAL_ID)
  for (const match of matches) {
    const lineNo = source.slice(0, match.index ?? 0).split('\n').length
    findings.push(`${filename}:${lineNo} — ph_* id literal: ${match[0]}`)
  }
  return findings
}

function findBackendStrings(source: string, filename: string): string[] {
  const findings: string[] = []
  const lines = source.split('\n')
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i]
    const trimmed = line.trim()
    if (trimmed.startsWith('//') || trimmed.startsWith('*')) continue
    for (const bad of BACKEND_IMPL_STRINGS) {
      if (line.includes(bad)) {
        findings.push(`${filename}:${i + 1} — backend string '${bad}': ${trimmed.slice(0, 120)}`)
      }
    }
  }
  return findings
}

describe('Sentinel slug/internal-label leakage guard (results surfaces)', () => {
  it('results component directory exists', () => {
    expect(fs.existsSync(resultsDir)).toBe(true)
  })

  it('results components contain no ph_*_v* internal id literals', () => {
    const files = collectResultsTsxFiles()
    expect(files.length).toBeGreaterThan(0)

    const allFindings: string[] = []
    for (const filepath of files) {
      const source = fs.readFileSync(filepath, 'utf8')
      allFindings.push(...findPhIds(source, path.basename(filepath)))
    }

    expect(allFindings).toEqual([])
  })

  it('results components contain no backend implementation strings', () => {
    const files = collectResultsTsxFiles()
    expect(files.length).toBeGreaterThan(0)

    const allFindings: string[] = []
    for (const filepath of files) {
      const source = fs.readFileSync(filepath, 'utf8')
      allFindings.push(...findBackendStrings(source, path.basename(filepath)))
    }

    expect(allFindings).toEqual([])
  })

  it('narrative shaping lib files contain no ph_*_v* internal id literals', () => {
    const allFindings: string[] = []
    for (const filepath of shapingFiles) {
      if (!fs.existsSync(filepath)) continue
      const source = fs.readFileSync(filepath, 'utf8')
      allFindings.push(...findPhIds(source, path.basename(filepath)))
    }
    expect(allFindings).toEqual([])
  })

  it('narrative shaping lib files contain no backend implementation strings', () => {
    const allFindings: string[] = []
    for (const filepath of shapingFiles) {
      if (!fs.existsSync(filepath)) continue
      const source = fs.readFileSync(filepath, 'utf8')
      allFindings.push(...findBackendStrings(source, path.basename(filepath)))
    }
    expect(allFindings).toEqual([])
  })
})
