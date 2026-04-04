import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'
import { AUTH_ACCESS_COOKIE_NAME } from './app/lib/auth-constants'

const PROTECTED_PREFIXES = ['/dashboard', '/analysis', '/reports', '/settings', '/profile'] as const

function isProtectedPath(pathname: string): boolean {
  return PROTECTED_PREFIXES.some((p) => pathname === p || pathname.startsWith(`${p}/`))
}

function hasAuthCookie(request: NextRequest): boolean {
  const token = request.cookies.get(AUTH_ACCESS_COOKIE_NAME)?.value
  return !!(token && token.length >= 10)
}

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl
  const authed = hasAuthCookie(request)

  if (pathname.startsWith('/login') || pathname.startsWith('/register')) {
    if (authed) {
      return NextResponse.redirect(new URL('/dashboard', request.url))
    }
    return NextResponse.next()
  }

  if (isProtectedPath(pathname) && !authed) {
    const login = new URL('/login', request.url)
    login.searchParams.set('next', pathname)
    return NextResponse.redirect(login)
  }

  return NextResponse.next()
}

export const config = {
  matcher: [
    '/login',
    '/login/:path*',
    '/register',
    '/register/:path*',
    '/dashboard',
    '/dashboard/:path*',
    '/analysis',
    '/analysis/:path*',
    '/reports',
    '/reports/:path*',
    '/settings',
    '/settings/:path*',
    '/profile',
    '/profile/:path*',
  ],
}
