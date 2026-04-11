'use client'

import { create } from 'zustand'
import type { User } from '../types/user'
import { AuthService } from '../services/auth'
import { setAccessTokenCookie } from '../lib/auth-cookies'
import { emitWedgeEvent } from '../lib/wedgeAnalytics'

export type RegisterOutcome =
  | { ok: true; needsEmailConfirm: false }
  | { ok: true; needsEmailConfirm: true; message: string }
  | { ok: false; message: string }

type AuthState = {
  user: User | null
  initialized: boolean
  loading: boolean
  error: string | null
  clearError: () => void
  initialize: () => void
  login: (email: string, password: string) => Promise<boolean>
  register: (email: string, password: string) => Promise<RegisterOutcome>
  logout: () => Promise<void>
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  initialized: false,
  loading: false,
  error: null,

  clearError: () => set({ error: null }),

  initialize: () => {
    if (typeof window === 'undefined') return
    const token = AuthService.getToken()
    const user = AuthService.getCurrentUser()
    if (token && user) {
      setAccessTokenCookie(token, 60 * 60 * 24 * 7)
      set({ user, initialized: true })
      void AuthService.getCurrentUserFromServer().then((r) => {
        if (r.success && r.data) set({ user: r.data })
      })
      return
    }
    if (token && !user) {
      set({ initialized: true })
      void AuthService.getCurrentUserFromServer().then((r) => {
        if (r.success && r.data) set({ user: r.data })
        else {
          AuthService.clearAuthData()
          set({ user: null })
        }
      })
      return
    }
    set({ user: null, initialized: true })
  },

  login: async (email, password) => {
    set({ loading: true, error: null })
    const res = await AuthService.login({ email, password })
    set({ loading: false })
    if (!res.success) {
      set({ error: res.error || 'Login failed' })
      emitWedgeEvent({
        event_name: 'wedge_auth_login_failed',
        timestamp: new Date().toISOString(),
        route: '/login',
        error_class: 'auth_failed',
      })
      return false
    }
    set({ user: AuthService.getCurrentUser() })
    emitWedgeEvent({
      event_name: 'wedge_auth_login_success',
      timestamp: new Date().toISOString(),
      route: '/login',
    })
    return true
  },

  register: async (email, password) => {
    set({ loading: true, error: null })
    const res = await AuthService.register({ email, password })
    set({ loading: false })
    if (!res.success) {
      const msg = res.error || 'Registration failed'
      set({ error: msg })
      emitWedgeEvent({
        event_name: 'wedge_auth_register_failed',
        timestamp: new Date().toISOString(),
        route: '/register',
        error_class: 'registration_failed',
      })
      return { ok: false, message: msg }
    }
    if (!res.data) {
      set({ error: null })
      emitWedgeEvent({
        event_name: 'wedge_auth_register_completed',
        timestamp: new Date().toISOString(),
        route: '/register',
        phase: 'pending_email_confirm',
      })
      return {
        ok: true,
        needsEmailConfirm: true,
        message: res.message || 'Check your email to confirm registration, then sign in.',
      }
    }
    set({ user: AuthService.getCurrentUser() })
    emitWedgeEvent({
      event_name: 'wedge_auth_register_completed',
      timestamp: new Date().toISOString(),
      route: '/register',
    })
    return { ok: true, needsEmailConfirm: false }
  },

  logout: async () => {
    set({ loading: true })
    await AuthService.logout()
    set({ user: null, loading: false, error: null })
  },
}))
