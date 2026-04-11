import Link from 'next/link'
import type { Metadata } from 'next'
import { PUBLIC_SUPPORT_EMAIL } from '../lib/publicContact'

export const metadata: Metadata = {
  title: 'Privacy notice — HealthIQ AI',
  description: 'How HealthIQ handles personal and health data for UK users.',
}

export default function PrivacyPage() {
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
        <h1 className="mb-2 text-3xl font-bold tracking-tight">Privacy notice</h1>
        <p className="mb-8 text-sm text-muted-foreground">Last updated: April 2026 · UK-first B2C launch baseline</p>

        <div className="space-y-8 text-sm leading-relaxed text-muted-foreground">
          <section className="space-y-3">
            <h2 className="text-lg font-semibold text-foreground">Who we are</h2>
            <p>
              HealthIQ AI provides software that helps you organise and interpret blood test results you already have. This
              notice describes our UK consumer health-data baseline for Phase 1. It is not a substitute for a full
              statutory privacy programme; deeper operational artefacts (for example DPIA, full subprocessor register) are
              tracked separately from product launch surfaces.
            </p>
          </section>

          <section className="space-y-3">
            <h2 className="text-lg font-semibold text-foreground">What data we process</h2>
            <p>
              We process account details (such as email), health information you upload or enter (including lab results),
              and technical data needed to run the service (for example logs and security signals). Health data is treated
              as special-category data under UK GDPR.
            </p>
          </section>

          <section className="space-y-3">
            <h2 className="text-lg font-semibold text-foreground">Why we process it</h2>
            <p>
              We process data to provide the interpretation product you sign up for, to secure your account, to improve
              reliability of the service, and to meet legal obligations. We do not use HealthIQ outputs as a medical
              diagnosis and we do not position the product as a medical device.
            </p>
          </section>

          <section className="space-y-3">
            <h2 className="text-lg font-semibold text-foreground">UK posture</h2>
            <p>
              Phase 1 is intentionally scoped to a UK-first, B2C launch with UK data residency as the direction of
              travel. Specific hosting regions and vendor maps are described in operational documentation as they are
              finalised — this page states the product-facing intent without claiming certifications we have not
              separately published.
            </p>
          </section>

          <section className="space-y-3">
            <h2 className="text-lg font-semibold text-foreground">Security</h2>
            <p>
              We apply encryption in transit, access controls, and other safeguards appropriate to health data. Wording on
              public pages is kept proportional to what is operationally evidenced — we do not claim frameworks (such as
              HIPAA-led posture) that are outside the agreed Phase 1 floor.
            </p>
          </section>

          <section className="space-y-3">
            <h2 className="text-lg font-semibold text-foreground">Your rights</h2>
            <p>
              Under UK GDPR you may have rights including access, rectification, erasure, restriction, objection, and
              data portability, subject to legal exceptions. Contact us using the details below to exercise these rights.
            </p>
          </section>

          <section className="space-y-3">
            <h2 className="text-lg font-semibold text-foreground">Contact</h2>
            <p>
              Privacy questions:{' '}
              <a className="text-primary underline-offset-4 hover:underline" href={`mailto:${PUBLIC_SUPPORT_EMAIL}`}>
                {PUBLIC_SUPPORT_EMAIL}
              </a>
              . You can also use the <Link href="/contact">Contact</Link> page.
            </p>
          </section>
        </div>
      </main>
    </div>
  )
}
