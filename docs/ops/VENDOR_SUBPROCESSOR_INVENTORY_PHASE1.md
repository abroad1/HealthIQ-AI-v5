# Vendor / subprocessor inventory — Phase 1 (launch-relevant)

**Status:** Internal transparency baseline (not a full legal Article 28 register)  
**Scope:** Services **identifiable from repository configuration** and typical deployment of this stack. Add rows when production adds email, observability, billing, or analytics SDKs.

---

## 1. How to read this table

Under UK GDPR, “processor” roles depend on **contractual** facts. This table describes **technical roles** implied by the codebase so privacy and ops can map them to agreements and DPIA.

| Service | Role in launch stack | Categories of data (indicative) | Repo / config evidence | Residency / notes |
|---------|----------------------|---------------------------------|------------------------|-------------------|
| **Supabase** | Auth, database, and (per config) object storage bucket `healthiq-exports` | Account identifiers, session tokens; health data in app DB; exports in storage | `SupabaseConfig` in `backend/config/settings.py`; frontend `NEXT_PUBLIC_SUPABASE_*` | **Must match** chosen project region in Supabase console — **not** fixed in code |
| **Google (Gemini API)** | LLM calls for insight / narrative synthesis when enabled | May include biomarker summaries, insight text, prompts derived from user data | `GeminiConfig`; `core/llm/gemini_client.py`; synthesis path in `core/insights/synthesis.py` | **Vendor’s** infra; routing and DPA depend on Google account settings |
| **GitHub (Actions)** | CI: tests, gates | Code only; **no** production user health data in typical workflows | `.github/workflows/*.yml` | Not a live-data processor for the product; listed for transparency |
| **Application hosting (backend + frontend)** | Runtime for FastAPI and Next.js | All production data in motion/at rest **depending on** where you deploy | **Not pinned** in repo (no `vercel.json` / platform lock-in found) | **Open:** document actual host(s) per environment |

---

## 2. Launch stack summary

- **Primary persistence and auth:** Supabase (as configured by env).
- **Inference (when not in mock/test mode):** Google Gemini per configuration.
- **CI:** GitHub Actions (development assurance, not the live subprocessor for user traffic).

---

## 3. Explicit non-claims

- This inventory is **not** exhaustive for **future** vendors (e.g. error tracking, email provider, payment processor, product analytics).
- **No** SOC 2 / ISO certification is asserted here (excluded as Phase 1 hard gate per launch posture).

---

## 4. Follow-up

1. Add a row when production enables **email**, **payments**, **APM**, or **product analytics**.
2. Attach contract/DPA references in a **restricted** ops store (not necessarily public repo).
