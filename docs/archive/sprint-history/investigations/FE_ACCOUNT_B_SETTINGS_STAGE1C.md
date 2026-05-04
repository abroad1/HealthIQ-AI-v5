# FE-ACCOUNT-B — Stage 1C Settings Preflight (mandatory)

**work_id:** FE-ACCOUNT-B  
**date:** 2026-04-08  
**SOP:** Automation Bus v1.3.1

## 1. Baseline verification

| Check | Result |
|--------|--------|
| `docs/investigations/FE_ACCOUNT_PREFLIGHT.md` exists | **Yes** |
| FE-ACCOUNT-A: `/profile` is real My Account shell | **Yes** — `frontend/app/(app)/profile/page.tsx` |
| `/settings` still placeholder before this sprint | **Yes** — stub only in `settings/page.tsx` |
| `useUIStore` `preferences` / theme persisted locally | **Yes** — `frontend/app/state/uiStore.ts` + `persist` |
| Server-backed settings/profile customer APIs | **Not exposed** |
| Theme in live shell | **`next-themes`** — `ThemeProvider` in `providers.tsx` (`storageKey: healthiq-theme`), **Header** toggles via `useTheme()` |

## 2. What is genuinely real vs not (§4)

| Candidate | Verdict | Evidence |
|-----------|---------|----------|
| **Appearance (light/dark)** | **Surface** | Same mechanism as Header; persisted in browser by `next-themes`. |
| **`uiStore.theme` / `toggleTheme`** | **Do not surface** | Not connected to `next-themes` DOM; only **DevApiProbe** uses it. Surfacing would **conflict** with real theme. |
| **Notification toggles in `preferences.notifications`** | **Omit** | No product code reads these for email/push/alerts behaviour outside dev tooling. |
| **Language / date / time format in `preferences`** | **Omit** | No i18n or formatters consume them in audited app surfaces. |
| **Accessibility flags (`highContrast`, `reducedMotion`, `fontSize`)** | **Omit** | Defined in store only; **no** global CSS/components wired. |

## 3. Sprint boundaries

No backend sync, no profile/password/billing, no fake toggles, no auth IA redesign.

## 4. Implementation choice

- **Appearance section** uses **`useTheme` from `next-themes`** only (aligned with **Header**).
- **Copy:** state clearly that these choices apply **on this browser/device** and are **not** synced to the HealthIQ account.
- **Related:** link to **My account** (`/profile`) only; no new account features.
