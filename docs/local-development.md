# Local development (backend + frontend)

Use this for end-to-end smoke testing on your machine. **Do not commit real secrets** — copy the example files to ignored env files and fill in values from your own Google AI / Supabase projects.

## Canonical dependency install (backend)

```bash
cd backend
pip install -e .
```

Dependency declarations live in `backend/pyproject.toml`.

## Environment files (inspected / expected)

| Location | Purpose |
|----------|---------|
| `backend/.env` | Loaded by `python-dotenv` (`config/settings.py`, `config/env.py`). **Gitignored** — create from `backend/env.example`. |
| `frontend/.env.local` | Next.js public env. **Gitignored** — create from `frontend/env.local.example`. |

There is **no** committed repo-root `.env` in this project; local env is per-app.

## Minimum variables

### Backend — process must start (`uvicorn`)

- **`GEMINI_API_KEY`** — Required. `backend/config/ai.py` validates the Gemini provider at import unless you are running under pytest. Without it, the API process exits during startup.

### Backend — optional: clean startup without Postgres

- **`DATABASE_URL`** — If **unset** or empty, the API runs without DB persistence (`config/database.py`). Analysis can still use in-memory routes; authenticated persistence and history need a working Postgres URL.
- If **`DATABASE_URL` is set to an invalid URL** (wrong tenant, revoked password, etc.), startup logs a **warning** during engine warmup but the server keeps running. For a **quiet** local run, **remove** `DATABASE_URL` from `backend/.env` or comment it out until you have a valid local or cloud database.

### Backend — login/register and `/api/auth/*`

- **`SUPABASE_URL`**
- **`SUPABASE_ANON_KEY`** — Used by `core/supabase_anon.py` (GoTrue). Must match a real Supabase project.

`SUPABASE_SERVICE_ROLE_KEY` is required for code paths that use the **service-role** client (`services/storage/supabase_client.py`), e.g. some storage/export flows — not for the anon-key auth routes above.

### Frontend

- **`NEXT_PUBLIC_API_BASE`** — Defaults to `http://127.0.0.1:8000` in code if unset (`frontend/app/lib/api.ts`). Set explicitly if your API runs on another host/port.

## Commands

**Terminal 1 — API**

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 — web**

```bash
cd frontend
npm install
npm run dev
```

**Browser**

- App: `http://localhost:3000`
- API docs: `http://127.0.0.1:8000/docs`
- Health: `http://127.0.0.1:8000/api/health`

## Database schema (canonical bootstrap)

**Authority:** [Alembic](https://alembic.sqlalchemy.org/) migrations under `backend/migrations/versions/`, with `target_metadata` from `core.models.database.Base` in `backend/migrations/env.py`. Do **not** create HealthIQ tables manually in the Supabase SQL editor unless you have no other option — use migrations.

With `DATABASE_URL` set in `backend/.env` (Supabase Postgres connection string):

```bash
cd backend
alembic current    # shows revision if alembic_version exists; empty DB may error until upgraded
alembic upgrade head
```

`migrations/env.py` loads **`backend/.env` with `override=True`** so the file wins over a stale `DATABASE_URL` in your shell (e.g. a test DB on `localhost:5433`). To target a different URL for a one-off migration, use `alembic -x url=postgresql://...` (see `migrations/env.py`).

**Check applied revision:**

```bash
alembic current
```

**Core application tables** (from `core/models/database.py`; created/updated by migrations, not an exhaustive list of every index/policy migration):

- `profiles` — user profile / FK anchor for auth user id  
- `analyses`, `analysis_results` — analysis runs and results (history)  
- `biomarker_scores`, `clusters`, `insights` — structured outputs  
- `exports`, `consents`, `audit_logs`, `deletion_requests`, `profiles_pii` — compliance / export / audit  

Supabase **Auth** users live in Supabase’s own `auth` schema; HealthIQ app tables live in the `public` schema (default migration path).

## What you can test without a database

- Health, OpenAPI, and **in-memory** analysis flows that do not require saving rows.
- **Auth** only if real Supabase env vars are set.

## What needs a valid `DATABASE_URL`

- Saving analyses, profile rows, and **history** continuity that depend on SQLAlchemy persistence.
