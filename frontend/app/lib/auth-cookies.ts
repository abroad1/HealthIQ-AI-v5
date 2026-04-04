'use client'

import { AUTH_ACCESS_COOKIE_NAME } from './auth-constants'

const DEFAULT_MAX_AGE_SEC = 60 * 60 * 24 * 7

export function setAccessTokenCookie(token: string, maxAgeSeconds: number = DEFAULT_MAX_AGE_SEC): void {
  if (typeof document === 'undefined') return
  const secure = process.env.NODE_ENV === 'production' ? '; Secure' : ''
  document.cookie = `${AUTH_ACCESS_COOKIE_NAME}=${encodeURIComponent(token)}; Path=/; Max-Age=${Math.max(60, maxAgeSeconds)}; SameSite=Lax${secure}`
}

export function clearAccessTokenCookie(): void {
  if (typeof document === 'undefined') return
  document.cookie = `${AUTH_ACCESS_COOKIE_NAME}=; Path=/; Max-Age=0; SameSite=Lax`
}

export function readAccessTokenCookie(): string | null {
  if (typeof document === 'undefined') return null
  const prefix = `${AUTH_ACCESS_COOKIE_NAME}=`
  const parts = document.cookie.split(';')
  for (const part of parts) {
    const trimmed = part.trim()
    if (trimmed.startsWith(prefix)) {
      return decodeURIComponent(trimmed.slice(prefix.length))
    }
  }
  return null
}
