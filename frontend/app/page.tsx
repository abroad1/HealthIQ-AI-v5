'use client'

import Link from 'next/link'
import { ArrowRight, Shield, Zap, Activity, CheckCircle2, Moon, Sun } from 'lucide-react'
import { Button } from './components/ui/button'
import { Card } from './components/ui/card'
import { useTheme } from 'next-themes'

export default function LandingPage() {
  const { theme, setTheme } = useTheme()

  return (
    <div className="min-h-screen bg-background">
      {/* Minimal Header */}
      <header className="sticky top-0 z-50 w-full border-b border-border bg-background/95 backdrop-blur">
        <div className="container flex h-16 items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary">
              <span className="text-lg font-bold text-primary-foreground">H</span>
            </div>
            <span className="text-xl font-bold">HealthIQ AI</span>
          </div>
          <Button
            variant="ghost"
            size="icon"
            onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
          >
            <Sun className="h-5 w-5 rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
            <Moon className="absolute h-5 w-5 rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
          </Button>
        </div>
      </header>

      {/* Hero Section */}
      <section className="container px-4 py-24 md:py-32">
        <div className="mx-auto max-w-4xl text-center">
          <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-primary/20 bg-primary/10 px-4 py-2">
            <Activity className="h-4 w-4 text-primary" />
            <span className="text-sm font-medium text-primary">Advanced Health Intelligence</span>
          </div>
          
          <h1 className="mb-6 text-4xl font-bold tracking-tight sm:text-5xl md:text-6xl lg:text-7xl">
            Transform Your Blood Tests Into{' '}
            <span className="bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
              Actionable Insights
            </span>
          </h1>
          
          <p className="mx-auto mb-8 max-w-2xl text-lg text-muted-foreground md:text-xl">
            Stop wondering what your numbers mean. Get personalized health insights powered by advanced AI analysis in minutes, not days.
          </p>
          
          <div className="flex flex-col items-center justify-center gap-4 sm:flex-row">
            <Button asChild size="lg" className="gap-2 text-lg">
              <Link href="/upload">
                Get Your Analysis
                <ArrowRight className="h-5 w-5" />
              </Link>
            </Button>
            <Button asChild variant="outline" size="lg">
              <Link href="/dashboard">View Demo</Link>
            </Button>
          </div>

          <div className="mt-12 flex flex-wrap items-center justify-center gap-8 text-sm text-muted-foreground">
            <div className="flex items-center gap-2">
              <CheckCircle2 className="h-5 w-5 text-status-excellent" />
              <span>HIPAA Compliant</span>
            </div>
            <div className="flex items-center gap-2">
              <CheckCircle2 className="h-5 w-5 text-status-excellent" />
              <span>Bank-Level Security</span>
            </div>
            <div className="flex items-center gap-2">
              <CheckCircle2 className="h-5 w-5 text-status-excellent" />
              <span>Instant Results</span>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="border-t border-border bg-muted/30 py-24">
        <div className="container px-4">
          <div className="mx-auto max-w-4xl">
            <div className="mb-12 text-center">
              <h2 className="mb-4 text-3xl font-bold md:text-4xl">How It Works</h2>
              <p className="text-lg text-muted-foreground">Three simple steps to better health understanding</p>
            </div>

            <div className="grid gap-8 md:grid-cols-3">
              <Card className="border-2 p-6 transition-all hover:border-primary/50 hover:shadow-lg">
                <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-lg bg-primary/10">
                  <span className="text-xl font-bold text-primary">1</span>
                </div>
                <h3 className="mb-2 text-xl font-bold">Upload Results</h3>
                <p className="text-muted-foreground">Upload your blood test PDF or paste the data directly. We support all major lab formats.</p>
              </Card>

              <Card className="border-2 p-6 transition-all hover:border-primary/50 hover:shadow-lg">
                <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-lg bg-primary/10">
                  <span className="text-xl font-bold text-primary">2</span>
                </div>
                <h3 className="mb-2 text-xl font-bold">AI Analysis</h3>
                <p className="text-muted-foreground">Our advanced AI analyzes your biomarkers across 6 health systems in seconds.</p>
              </Card>

              <Card className="border-2 p-6 transition-all hover:border-primary/50 hover:shadow-lg">
                <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-lg bg-primary/10">
                  <span className="text-xl font-bold text-primary">3</span>
                </div>
                <h3 className="mb-2 text-xl font-bold">Get Insights</h3>
                <p className="text-muted-foreground">Receive personalized recommendations and track your health journey over time.</p>
              </Card>
            </div>
          </div>
        </div>
      </section>

      {/* Trust Signals */}
      <section className="py-24">
        <div className="container px-4">
          <div className="mx-auto max-w-4xl">
            <div className="mb-12 text-center">
              <h2 className="mb-4 text-3xl font-bold md:text-4xl">Built on Trust & Science</h2>
              <p className="text-lg text-muted-foreground">Your health data deserves the highest standards of care</p>
            </div>

            <div className="grid gap-8 md:grid-cols-3">
              <div className="text-center">
                <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-primary/10">
                  <Shield className="h-8 w-8 text-primary" />
                </div>
                <h3 className="mb-2 text-lg font-bold">Medical-Grade Security</h3>
                <p className="text-sm text-muted-foreground">HIPAA compliant with end-to-end encryption. Your data is always private.</p>
              </div>

              <div className="text-center">
                <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-primary/10">
                  <Zap className="h-8 w-8 text-primary" />
                </div>
                <h3 className="mb-2 text-lg font-bold">Evidence-Based AI</h3>
                <p className="text-sm text-muted-foreground">Trained on peer-reviewed research and validated clinical guidelines.</p>
              </div>

              <div className="text-center">
                <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-primary/10">
                  <Activity className="h-8 w-8 text-primary" />
                </div>
                <h3 className="mb-2 text-lg font-bold">Continuous Monitoring</h3>
                <p className="text-sm text-muted-foreground">Track biomarker trends and receive alerts when action is needed.</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="border-t border-border bg-muted/30 py-24">
        <div className="container px-4">
          <div className="mx-auto max-w-2xl text-center">
            <h2 className="mb-4 text-3xl font-bold md:text-4xl">Ready to Understand Your Health?</h2>
            <p className="mb-8 text-lg text-muted-foreground">
              Join thousands who&apos;ve taken control of their health journey with data-driven insights.
            </p>
            <Button asChild size="lg" className="gap-2 text-lg">
              <Link href="/upload">
                Start Your Analysis
                <ArrowRight className="h-5 w-5" />
              </Link>
            </Button>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-border bg-background">
        <div className="container py-8">
          <div className="flex flex-col items-center justify-between gap-4 md:flex-row">
            <p className="text-sm text-muted-foreground">
              © {new Date().getFullYear()} HealthIQ AI. All rights reserved.
            </p>
            <div className="flex gap-6 text-sm text-muted-foreground">
              <a href="#" className="transition-colors hover:text-foreground">Privacy</a>
              <a href="#" className="transition-colors hover:text-foreground">Terms</a>
              <a href="#" className="transition-colors hover:text-foreground">Contact</a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}
