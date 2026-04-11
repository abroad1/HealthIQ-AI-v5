import Link from 'next/link'
import type { Metadata } from 'next'
import { PUBLIC_SUPPORT_EMAIL } from '../lib/publicContact'

export const metadata: Metadata = {
  title: 'Terms of use — HealthIQ AI',
  description: 'Terms governing use of the HealthIQ AI interpretation product.',
}

export default function TermsPage() {
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
        <h1 className="mb-2 text-3xl font-bold tracking-tight">Terms of use</h1>
        <p className="mb-8 text-sm text-muted-foreground">Last updated: April 2026 · UK-first B2C launch baseline</p>

        <div className="space-y-8 text-sm leading-relaxed text-muted-foreground">
          <section className="space-y-3">
            <h2 className="text-lg font-semibold text-foreground">The service</h2>
            <p>
              HealthIQ AI offers structured interpretation of blood test results you provide. Outputs are for information
              and discussion with a qualified clinician — they are not a diagnosis, prescription, or emergency service.
            </p>
          </section>

          <section className="space-y-3">
            <h2 className="text-lg font-semibold text-foreground">Eligibility</h2>
            <p>
              You must use accurate information and keep your credentials secure. The Phase 1 product is aimed at adults
              using the service for themselves in the UK market context described in our launch posture.
            </p>
          </section>

          <section className="space-y-3">
            <h2 className="text-lg font-semibold text-foreground">Not medical advice</h2>
            <p>
              Nothing in the app replaces professional medical advice. Seek urgent care if you have an emergency. Use
              HealthIQ as a companion to — not a substitute for — clinical judgement.
            </p>
          </section>

          <section className="space-y-3">
            <h2 className="text-lg font-semibold text-foreground">Accounts and acceptable use</h2>
            <p>
              You agree not to misuse the platform, attempt to break security, or use the service in any unlawful way. We
              may suspend access where necessary to protect users or the service.
            </p>
          </section>

          <section className="space-y-3">
            <h2 className="text-lg font-semibold text-foreground">Liability</h2>
            <p>
              To the extent permitted by law, the service is provided as-is for Phase 1. Nothing in these terms excludes
              liability that cannot legally be excluded. Specific limits may be refined as commercial terms evolve.
            </p>
          </section>

          <section className="space-y-3">
            <h2 className="text-lg font-semibold text-foreground">Governing law</h2>
            <p>
              These terms are framed for users in the United Kingdom. Disputes are intended to be resolved under English
              law and the courts of England and Wales, subject to mandatory consumer protections.
            </p>
          </section>

          <section className="space-y-3">
            <h2 className="text-lg font-semibold text-foreground">Contact</h2>
            <p>
              Questions about these terms:{' '}
              <a className="text-primary underline-offset-4 hover:underline" href={`mailto:${PUBLIC_SUPPORT_EMAIL}`}>
                {PUBLIC_SUPPORT_EMAIL}
              </a>{' '}
              or <Link href="/contact">Contact</Link>.
            </p>
          </section>
        </div>
      </main>
    </div>
  )
}
