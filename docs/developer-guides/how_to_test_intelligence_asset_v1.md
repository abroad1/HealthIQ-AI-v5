# How to Test an Intelligence Asset v1

## Unit tests

- Place under `backend/tests/unit/`
- Test pure functions and validators in isolation

## Regression tests

- Place under `backend/tests/regression/`
- Mark with `@pytest.mark.regression`
- Name: `test_lc_sXX_<topic>.py`

## Fixture tests

- Panels: `backend/tests/fixtures/panels/`
- Persisted results: `backend/tests/fixtures/persisted_results/`

## DTO contract checks

- `frontend_contract_v1.FRONTEND_CONSUMED_ROOT_KEYS`
- `persisted_replay_contract_v1` compatibility helpers

## Sentinel pack updates

- Register defect class in `sentinel/packs/escaped_defects_v1.json`
- Point to active deterministic test file — no placeholders

## Proving harness use

When orchestrator output assembly changes:

```powershell
python backend/tools/launch_core_proving_harness.py
```

Do not commit metadata-only harness artefacts unless fingerprint change is approved.

## Before/after fingerprint expectations

- Capture SHA256 of stable output subset (signals, domain scores, root-cause IDs)
- Store in `docs/audit-papers/` when behaviour-preserving refactors land

## Standing maintenance

Future KB-WAVE or scaffold sprints must update this document if they introduce or change the relevant architectural pattern.
