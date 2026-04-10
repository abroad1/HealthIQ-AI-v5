/**
 * User-facing copy for history/list API failures (FE-LAUNCH-INTEGRATION-B).
 * Does not hide real failures — only reframes common cases calmly.
 */
export function friendlyHistoryError(raw: string): string {
  const m = raw.trim()
  if (!m) return 'Something went wrong loading your saved analyses. Please try again.'
  if (/401|unauthorized|not authenticated/i.test(m)) {
    return 'Your session may have expired. Sign out and sign in again, then retry.'
  }
  if (/503|service unavailable|database|Database_URL|persistence/i.test(m)) {
    return 'Saved history is temporarily unavailable. Please try again shortly.'
  }
  if (/403|forbidden|not allowed/i.test(m)) {
    return 'You do not have access to this list right now. If this persists, sign in again.'
  }
  return 'We could not load your saved analyses. Please try again.'
}

/** Primary title for a saved analysis row — consistent across dashboard and reports. */
export function savedAnalysisPrimaryLabel(id: string): { line: string; fullId: string } {
  const fullId = id.trim()
  if (!fullId) return { line: 'Analysis', fullId: '' }
  const line = fullId.length > 12 ? `Analysis ${fullId.slice(0, 8)}…` : `Analysis ${fullId}`
  return { line, fullId }
}
