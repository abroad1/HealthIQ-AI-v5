# Baseline Testing

Baseline (infra-free deterministic) tests validate core SSOT behaviour without external dependencies.

## Running baseline tests

From the repo root:

```bash
python backend/scripts/run_baseline_tests.py
```

Or from `backend/`:

```bash
python -m pytest tests/enforcement/test_canonical_only.py tests/unit/test_default_golden_fixture_is_collision_free.py -v
```

Exit code 0 on pass; non-zero on failure.

## Scope

The baseline suite includes:

- **Enforcement:** Canonical-only validation, alias resolution, orchestrator behaviour
- **Golden fixture:** Default golden panel is collision-free

These tests require no database, no LLM, and no API keys.

## Full test suite

The full test suite (`python -m pytest -q`) is not currently a gate. It includes:

- DB-dependent tests (connection pooling, RLS policies, GDPR compliance)
- Integration tests (orchestrator, clustering, upload API)
- Provider tests (Gemini, etc.)

These suites require:

- **DB tests:** `HEALTHIQ_ENABLE_DB_TESTS=1` and `DATABASE_URL_TEST`
- **Provider tests:** API keys and optional skip markers
