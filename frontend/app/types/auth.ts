/**
 * FE-FOUNDATION-A /auth JSON contract (backend FastAPI).
 * Do not add parallel shapes — keep aligned with backend/app/routes/auth.py.
 */

export interface BackendUserIdentity {
  id: string
  email?: string | null
}

export interface AuthSessionPayload {
  access_token: string
  refresh_token: string
  expires_in: number
  token_type: string
  expires_at?: number | null
}

export interface AuthSessionResponse {
  user: BackendUserIdentity
  session: AuthSessionPayload
}

export interface MeResponse {
  user: BackendUserIdentity
  app_metadata: Record<string, unknown>
  user_metadata: Record<string, unknown>
}
