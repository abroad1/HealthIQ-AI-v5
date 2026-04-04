/**
 * Authentication API — FE-FOUNDATION-A FastAPI contract only.
 * Uses NEXT_PUBLIC_API_BASE + /api/auth/* (not Supabase JS session — avoids competing flows).
 */

import { User } from '../types/user'
import { ApiResponse } from '../types/api'
import type { AuthSessionResponse, BackendUserIdentity, MeResponse } from '../types/auth'
import { API_BASE } from '../lib/api'
import {
  setAccessTokenCookie,
  clearAccessTokenCookie,
  readAccessTokenCookie,
} from '../lib/auth-cookies'

const AUTH_API_ROOT = `${API_BASE}/api/auth`

const TOKEN_KEY = 'healthiq_auth_token'
const USER_KEY = 'healthiq_user_data'

function parseFastApiDetail(payload: unknown): string {
  if (!payload || typeof payload !== 'object') return 'Request failed'
  const detail = (payload as { detail?: unknown }).detail
  if (typeof detail === 'string') return detail
  if (Array.isArray(detail)) {
    return detail.map((d) => (typeof d === 'object' && d && 'msg' in d ? String((d as { msg: string }).msg) : String(d))).join('; ')
  }
  return 'Request failed'
}

function identityToUser(u: BackendUserIdentity): User {
  return {
    id: u.id,
    email: u.email ?? '',
  }
}

function persistSession(session: AuthSessionResponse['session'], user: BackendUserIdentity): void {
  localStorage.setItem(TOKEN_KEY, session.access_token)
  localStorage.setItem(USER_KEY, JSON.stringify(identityToUser(user)))
  setAccessTokenCookie(session.access_token, session.expires_in)
}

export class AuthService {
  static async login(credentials: { email: string; password: string }): Promise<ApiResponse<AuthSessionResponse>> {
    try {
      const response = await fetch(`${AUTH_API_ROOT}/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(credentials),
      })

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(parseFastApiDetail(errorData))
      }

      const result = (await response.json()) as AuthSessionResponse
      persistSession(result.session, result.user)

      return {
        data: result,
        success: true,
        message: 'Login successful',
      }
    } catch (error) {
      return {
        data: null as unknown as AuthSessionResponse,
        success: false,
        error: error instanceof Error ? error.message : 'Login failed',
      }
    }
  }

  static async logout(): Promise<ApiResponse<{ logged_out: boolean }>> {
    try {
      const token = this.getToken()
      if (token) {
        try {
          await fetch(`${AUTH_API_ROOT}/logout`, {
            method: 'POST',
            headers: {
              Authorization: `Bearer ${token}`,
              'Content-Type': 'application/json',
            },
          })
        } catch {
          /* local logout even if server call fails */
        }
      }
      localStorage.removeItem(TOKEN_KEY)
      localStorage.removeItem(USER_KEY)
      clearAccessTokenCookie()
      return { data: { logged_out: true }, success: true, message: 'Logout successful' }
    } catch (error) {
      return {
        data: { logged_out: false },
        success: false,
        error: error instanceof Error ? error.message : 'Logout failed',
      }
    }
  }

  static getCurrentUser(): User | null {
    try {
      const userData = localStorage.getItem(USER_KEY)
      if (!userData) return null
      return JSON.parse(userData) as User
    } catch {
      return null
    }
  }

  static async getCurrentUserFromServer(): Promise<ApiResponse<User>> {
    try {
      const token = this.getToken()
      if (!token) {
        return { data: null as unknown as User, success: false, error: 'No authentication token found' }
      }

      const response = await fetch(`${AUTH_API_ROOT}/me`, {
        method: 'GET',
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      })

      if (!response.ok) {
        if (response.status === 401) {
          this.clearAuthData()
          return { data: null as unknown as User, success: false, error: 'Authentication expired' }
        }
        const errorData = await response.json().catch(() => ({}))
        throw new Error(parseFastApiDetail(errorData))
      }

      const result = (await response.json()) as MeResponse
      const user = identityToUser(result.user)
      localStorage.setItem(USER_KEY, JSON.stringify(user))

      return { data: user, success: true, message: 'User data retrieved successfully' }
    } catch (error) {
      return {
        data: null as unknown as User,
        success: false,
        error: error instanceof Error ? error.message : 'Failed to get current user',
      }
    }
  }

  static isAuthenticated(): boolean {
    return !!(this.getToken() && this.getCurrentUser())
  }

  static getToken(): string | null {
    if (typeof window === 'undefined') return null
    const fromStorage = localStorage.getItem(TOKEN_KEY)
    if (fromStorage) return fromStorage
    const fromCookie = readAccessTokenCookie()
    if (fromCookie) {
      localStorage.setItem(TOKEN_KEY, fromCookie)
      return fromCookie
    }
    return null
  }

  static clearAuthData(): void {
    localStorage.removeItem(TOKEN_KEY)
    localStorage.removeItem(USER_KEY)
    clearAccessTokenCookie()
  }

  static async register(userData: {
    email: string
    password: string
    name?: string
    role?: 'user' | 'admin' | 'researcher'
  }): Promise<ApiResponse<AuthSessionResponse | null>> {
    try {
      const response = await fetch(`${AUTH_API_ROOT}/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: userData.email, password: userData.password }),
      })

      if (response.status === 202) {
        const body = await response.json().catch(() => ({}))
        return {
          data: null,
          success: true,
          message: parseFastApiDetail(body) || 'Confirm your email, then sign in.',
        }
      }

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(parseFastApiDetail(errorData))
      }

      const result = (await response.json()) as AuthSessionResponse
      persistSession(result.session, result.user)

      return {
        data: result,
        success: true,
        message: 'Registration successful',
      }
    } catch (error) {
      return {
        data: null,
        success: false,
        error: error instanceof Error ? error.message : 'Registration failed',
      }
    }
  }

  static async updateProfile(_profileData: Partial<import('../types/user').UserProfile>): Promise<ApiResponse<User>> {
    return {
      data: null as unknown as User,
      success: false,
      error: 'Profile update is out of scope for the current backend auth contract (FE-ACCOUNT / FE-PAGES).',
    }
  }

  static async changePassword(_passwordData: {
    currentPassword: string
    newPassword: string
  }): Promise<ApiResponse<{ changed: boolean }>> {
    return {
      data: null as unknown as { changed: boolean },
      success: false,
      error: 'Password change is not exposed on the FE-FOUNDATION-A auth API.',
    }
  }

  static async refreshToken(): Promise<ApiResponse<{ token: string }>> {
    return {
      data: null as unknown as { token: string },
      success: false,
      error: 'Token refresh is not implemented for the FastAPI auth contract',
    }
  }
}
