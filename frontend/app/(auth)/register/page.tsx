'use client'

import { useState } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { useAuthStore } from '../../state/authStore'
import { Button } from '../../components/ui/button'
import { Input } from '../../components/ui/input'
import { Label } from '../../components/ui/label'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../components/ui/card'
import { Alert, AlertDescription } from '../../components/ui/alert'

export default function RegisterPage() {
  const router = useRouter()
  const register = useAuthStore((s) => s.register)
  const loading = useAuthStore((s) => s.loading)
  const error = useAuthStore((s) => s.error)
  const clearError = useAuthStore((s) => s.clearError)

  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [info, setInfo] = useState<string | null>(null)

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault()
    clearError()
    setInfo(null)
    const out = await register(email, password)
    if (!out.ok) return
    if (out.needsEmailConfirm) {
      setInfo(out.message)
      return
    }
    router.replace('/dashboard')
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Create account</CardTitle>
        <CardDescription>Password must be at least 8 characters (backend rule).</CardDescription>
      </CardHeader>
      <form onSubmit={onSubmit}>
        <CardContent className="space-y-4">
          {error ? (
            <Alert variant="destructive">
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          ) : null}
          {info ? (
            <Alert>
              <AlertDescription>{info}</AlertDescription>
            </Alert>
          ) : null}
          <div className="space-y-2">
            <Label htmlFor="email">Email</Label>
            <Input
              id="email"
              type="email"
              autoComplete="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="password">Password</Label>
            <Input
              id="password"
              type="password"
              autoComplete="new-password"
              required
              minLength={8}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>
        </CardContent>
        <div className="flex flex-col gap-3 px-6 pb-6">
          <Button type="submit" className="w-full" disabled={loading}>
            {loading ? 'Creating account…' : 'Register'}
          </Button>
          <p className="text-sm text-muted-foreground text-center">
            Already have an account?{' '}
            <Link href="/login" className="text-primary underline-offset-4 hover:underline">
              Sign in
            </Link>
          </p>
        </div>
      </form>
    </Card>
  )
}
