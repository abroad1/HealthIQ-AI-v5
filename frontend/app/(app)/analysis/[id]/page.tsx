import { redirect } from 'next/navigation'

/**
 * Canonical entry for reopening a saved analysis: redirects to the results view with the same analysis id.
 * The full interpretation UI remains on `/results` (hero / trust / advanced tabs) — this route removes stub ambiguity.
 */
export default function AnalysisDetailRedirect({ params }: { params: { id: string } }) {
  redirect(`/results?analysis_id=${encodeURIComponent(params.id)}`)
}
