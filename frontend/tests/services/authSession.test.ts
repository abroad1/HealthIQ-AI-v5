/**
 * AuthService stale-session behaviour: 401 clears session; 500 does not.
 */

import { AuthService } from '@/services/auth'

describe('AuthService session resilience', () => {
  const originalFetch = global.fetch

  beforeEach(() => {
    localStorage.clear()
    document.cookie = 'healthiq_access_token=; Max-Age=0; path=/'
    // Reset private static via logout path
    void AuthService.logout()
    localStorage.setItem('healthiq_auth_token', 'stale-token')
    localStorage.setItem('healthiq_user_data', JSON.stringify({ id: 'u1', email: 'a@b.c' }))
  })

  afterEach(() => {
    global.fetch = originalFetch
    localStorage.clear()
  })

  it('clears session on /auth/me 401 and stops repeat probes', async () => {
    let calls = 0
    global.fetch = jest.fn(async () => {
      calls += 1
      return {
        ok: false,
        status: 401,
        json: async () => ({ detail: 'Invalid or expired token' }),
      } as Response
    }) as unknown as typeof fetch

    const first = await AuthService.getCurrentUserFromServer()
    expect(first.success).toBe(false)
    expect(first.error).toBe('Authentication expired')
    expect(AuthService.getToken()).toBeNull()
    expect(AuthService.wasSessionClearedForAuthFailure()).toBe(true)

    const second = await AuthService.getCurrentUserFromServer()
    expect(second.success).toBe(false)
    expect(second.error).toBe('Authentication expired')
    // Second call must not hit the network again.
    expect(calls).toBe(1)
  })

  it('does not clear session on /auth/me 500', async () => {
    global.fetch = jest.fn(async () => {
      return {
        ok: false,
        status: 500,
        json: async () => ({ detail: 'Failed to load profile' }),
      } as Response
    }) as unknown as typeof fetch

    const res = await AuthService.getCurrentUserFromServer()
    expect(res.success).toBe(false)
    expect(AuthService.getToken()).toBe('stale-token')
    expect(AuthService.wasSessionClearedForAuthFailure()).toBe(false)
  })
})
