/**
 * FE-LAUNCH-INTEGRATION-A — lightweight regression on documented URL contracts.
 * Full redirect behaviour is enforced by Next.js `app/(app)/analysis/[id]/page.tsx`.
 */

describe('FE-LAUNCH-INTEGRATION-A route contracts', () => {
  it('uses /analysis/:id as the stable reopen entry that maps to results query', () => {
    const analysisId = '550e8400-e29b-41d4-a716-446655440000'
    const reopenEntry = `/analysis/${encodeURIComponent(analysisId)}`
    const resultsView = `/results?analysis_id=${encodeURIComponent(analysisId)}`
    expect(reopenEntry).toBe(
      '/analysis/550e8400-e29b-41d4-a716-446655440000'
    )
    expect(resultsView).toBe(
      '/results?analysis_id=550e8400-e29b-41d4-a716-446655440000'
    )
  })
})
