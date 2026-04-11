import Link from 'next/link'
import type { Metadata } from 'next'
import { PUBLIC_SUPPORT_EMAIL } from '../lib/publicContact'

export const metadata: Metadata = {
  title: 'Contact — HealthIQ AI',
  description: 'How to reach HealthIQ AI for privacy, product, and support enquiries.',
}

export default function ContactPage() {
  return (
    <div className="min-h-screen bg-background">
      <header className="sticky top-0 z-50 w-full border-b border-border bg-background/95 backdrop-blur">
        <div className="container flex h-16 items-center justify-between">
          <Link href="/" className="flex items-center gap-2 text-sm font-medium text-muted-foreground hover:text-foreground">
            ← Back to HealthIQ AI
          </Link>
        </div>
      </header>
      <main className="container max-w-3xl px-4 py-12">
        <h1 className="mb-2 text-3xl font-bold tracking-tight">Contact</h1>
        <p className="mb-8 text-sm text-muted-foreground">UK-first B2C launch — minimum credible contact path</p>

        <div className="space-y-6 text-sm leading-relaxed text-muted-foreground">
          <p>
            For privacy questions, product feedback, and account-related enquiries, email us at{' '}
            <a className="font-medium text-primary underline-offset-4 hover:underline" href={`mailto:${PUBLIC_SUPPORT_EMAIL}`}>
              {PUBLIC_SUPPORT_EMAIL}
            </a>
            . We read every message; response times depend on volume and priority.
          </p>
          <p>
            This contact path is the product-facing baseline for Phase 1. Full operational support tiers, ticketing, and
            published SLAs are out of scope for this launch surface and may arrive in later operational readiness work.
          </p>
          <p>
            Read our <Link href="/privacy">Privacy notice</Link> and <Link href="/terms">Terms of use</Link>.
          </p>
        </div>
      </main>
    </div>
  )
}
