/**
 * Stripe-backed billing API (Checkout + Customer Portal). Server uses test/live keys from env.
 */

import { API_BASE } from '@/lib/api';
import { readAccessTokenCookie } from '@/lib/auth-cookies';
import { ApiResponse } from '@/types/api';

function billingApiRoot(): string {
  const base = API_BASE.replace(/\/$/, '');
  return base.endsWith('/api') ? base : `${base}/api`;
}

function billingAuthHeaders(): Record<string, string> {
  if (typeof window === 'undefined') return {};
  const token =
    readAccessTokenCookie() ||
    (typeof localStorage !== 'undefined' ? localStorage.getItem('healthiq_auth_token') : null);
  if (!token) return {};
  return { Authorization: `Bearer ${token}` };
}

function parseDetail(payload: unknown): string {
  if (!payload || typeof payload !== 'object') return 'Request failed';
  const detail = (payload as { detail?: unknown }).detail;
  if (typeof detail === 'string') return detail;
  if (Array.isArray(detail)) {
    return detail
      .map((d) => (typeof d === 'object' && d && 'msg' in d ? String((d as { msg: string }).msg) : String(d)))
      .join('; ');
  }
  return 'Request failed';
}

export class BillingService {
  static async createCheckoutSession(): Promise<ApiResponse<{ url: string }>> {
    try {
      const res = await fetch(`${billingApiRoot()}/billing/checkout-session`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...billingAuthHeaders(),
        },
      });
      if (!res.ok) {
        const body = await res.json().catch(() => ({}));
        throw new Error(parseDetail(body));
      }
      const data = (await res.json()) as { url: string };
      return { data, success: true, message: 'Checkout session created' };
    } catch (e) {
      return {
        data: null,
        success: false,
        error: e instanceof Error ? e.message : 'Could not start checkout',
      };
    }
  }

  static async createPortalSession(): Promise<ApiResponse<{ url: string }>> {
    try {
      const res = await fetch(`${billingApiRoot()}/billing/portal-session`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...billingAuthHeaders(),
        },
      });
      if (!res.ok) {
        const body = await res.json().catch(() => ({}));
        throw new Error(parseDetail(body));
      }
      const data = (await res.json()) as { url: string };
      return { data, success: true, message: 'Portal session created' };
    } catch (e) {
      return {
        data: null,
        success: false,
        error: e instanceof Error ? e.message : 'Could not open billing portal',
      };
    }
  }
}
