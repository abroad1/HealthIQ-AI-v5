/**
 * Display-only billing copy (Sprint 7). Price is finalized in Stripe Checkout.
 * Set NEXT_PUBLIC_BILLING_PRICE_LABEL in env for customer-facing text, e.g. "£12 / month".
 */

export const BILLING_PLAN_NAME =
  process.env.NEXT_PUBLIC_BILLING_PLAN_NAME?.trim() || 'HealthIQ Unlimited analyses';

/** Shown on /pricing; use env to avoid inventing a currency amount. */
export const BILLING_PRICE_LABEL =
  process.env.NEXT_PUBLIC_BILLING_PRICE_LABEL?.trim() || 'Price shown at checkout';

export const BILLING_FREE_SUMMARY =
  process.env.NEXT_PUBLIC_BILLING_FREE_SUMMARY?.trim() ||
  'Your first completed analysis is included. Subscribe for unlimited further analyses.';
