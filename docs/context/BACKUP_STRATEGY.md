# 🔐 BACKUP_STRATEGY.md

This document defines the **backup and release governance strategy** for HealthIQ AI v5. It keeps sprint work lightweight while preserving the ability to cut verified, stable milestones.

---

## 📦 Canonical GitHub Repository

All production-authoritative code is stored in:

https://github.com/abroad1/HealthIQ-AI-v5

This is the **source of truth** for all history, tags, and official context.

---

## 🌿 Branch Model

If you are unsure which branch to use as a base, read `BRANCHING_MODEL.md`; default is `main`.

---

## 🌲 Branch Model (Current)

- `main` is the trunk and integration branch; `origin/HEAD` points to `origin/main`.
- `sprintXX/*` for compute-only sprint work.
- `docs/*` for docs-only work.
- `release/*` is optional for stabilisation before a milestone.
- `backup/*` branches are historical; do not create new ones unless an explicit archival snapshot is required.

---

## ⚡ Fast Path (Default) — Sprint and Compute-Only Work

**Definition of backup:** work is considered safe once it is pushed to `origin` **and** a PR to `main` exists (draft PR is OK).

**Steps**
1. Create a branch from `main`: `sprintXX/<topic>` or `docs/<topic>`.
2. Commit small, coherent changes.
3. Push to `origin` early (even WIP).
4. Open a PR to `main` using the sprint PR template.
5. CI green = verification.

**What not to do**
- Do not use detached HEAD for real work.
- Do not keep important docs only locally.
- Do not run `git fsck` as standard backup validation (forensics only).

---

## 🏁 Release Path — Stable Line or Milestone Only

**When to use**
- After a set of sprints, before an external demo, before deployment, or when creating a stable tag.

**Steps**
1. Ensure `main` is green.
2. Optionally create or update a `release/*` branch (e.g. `release/pre-sprint15-stable`).
3. Tag the release (use the established naming pattern).
4. Run heavier checks (smoke scripts, SSOT validation, key endpoint smoke).
5. Document release notes and link the tag and PR.

**Important:** the release path is not required for every sprint.

---

## ✅ Verification (Automation-First)

- CI on the PR is the source of truth for verification.
- Optional quick checks (keep minimal):
  - `python backend/scripts/validate_manifest.py`
  - `python backend/scripts/smoke_cluster_engine_v2.py` (if present in the sprint branch)
  - `python backend/scripts/smoke_prompt_v2.py` (if present in the sprint branch)
  - Upload parse smoke (two-line, when the upload route is wired):
    ```
    curl -s -X POST http://localhost:8000/api/upload/parse -F "text_content=Hemoglobin 13.2 g/dL" > /tmp/upload_parse.json
    python -m json.tool < /tmp/upload_parse.json
    ```
  - Accidental deletion check:
    ```
    git diff --name-status origin/main...HEAD | findstr "^D"
    ```
    If this prints anything, review deletions before PR.

---

## 🧾 Protected Assets (Docs Safety)

These files are considered critical context and should not be deleted or moved without an explicit reason in the PR:
- `docs/context/INSIGHTS.md`
- `docs/context/SPRINT_PLAN_SPRINTS_15_25.md`
- `docs/context/INTELLIGENCE_LIFECYCLE.md`
- `docs/context/BACKUP_STRATEGY.md`

**Policy:** changes to these files should be called out in the PR summary. Enforcement should be automated later via CI (no code changes in this update).

---

## 🪢 Tagging Policy (Simplified)

- Tags are for releases and milestones, not every sprint.
- Tags must be annotated (`-a`) with a meaningful description.
- Sprint branches are backed up by push + PR, not by tags.

---

## 🧪 Non-production Environments

### Test Database and Local Containers

**Exclusion Policy**: The following environments are **explicitly excluded** from backup strategies and may be destroyed after each test cycle:

- **Local Test Database**: `healthiq_testdb` PostgreSQL container (port 5433)
- **Docker Test Containers**: Any containers created for testing purposes
- **Temporary Test Data**: Data generated during integration, performance, or security tests
- **Local Work Databases**: Any local database instances used for day-to-day work

### Rationale

- **Test Isolation**: Test databases contain synthetic data and destructive operations
- **Resource Management**: Prevents accumulation of test containers and data
- **Security**: Test environments may contain sensitive test data that should not persist
- **Performance**: Regular cleanup prevents resource leaks and performance degradation

### Cleanup Procedures

- **Nightly Teardown**: Test containers are automatically destroyed after test completion
- **Manual Cleanup**: Contributors can run `docker system prune` to clean up test resources
- **CI/CD Integration**: Build pipelines include automatic cleanup of test environments

### Backup Exclusions

The following are **never backed up**:
- Test database containers and volumes
- Temporary test files and logs
- Local database snapshots
- Test-specific environment configurations

---

## 📘 Related Files

- `PROJECT_STRUCTURE.md` → for canonical folder layout  
- `CURSOR_RULES.md` → for Cursor work constraints  
- `IMPLEMENTATION_PLAN.md` → for milestone definitions  
- `ARCHITECTURE_REVIEW_REPORT.md` → for current stack audit summary  
- `docs/sprints/SPRINT_11_TEST_ISOLATION_AND_SECURITY_VALIDATION.md` → for test isolation details

---

Maintaining this policy ensures that **no architectural context or milestone is lost**, while keeping backup steps fast for sprint work.

