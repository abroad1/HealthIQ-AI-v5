# 🔐 BACKUP_STRATEGY.md

This document defines the **canonical backup and versioning strategy** for HealthIQ AI v5. It ensures all architectural decisions, implementation milestones, and context alignments are safely preserved and traceable across all environments.

---

## 📦 Canonical GitHub Repository

All production-authoritative code is stored in:

https://github.com/abroad1/HealthIQ-AI-v5

This is the **source of truth** for all development history, tags, and official context.

---

## 🌲 Branching Strategy

| Branch         | Purpose                                            |
|----------------|----------------------------------------------------|
| `main`         | ✅ Stable, production-tracked builds               |
| `dev`          | 🔄 Active feature and architectural development    |
| `feature/*`    | 🔧 Feature-specific or refactor-specific branches  |

> All experimental branches must eventually be merged to `dev`, and then to `main` via PR with contextual justification.

---

## 🪢 Tagging Policy

Tags must be created at all key milestones for traceability.

| Tag Example                     | When to Use                                             |
|--------------------------------|----------------------------------------------------------|
| `v5.0-architecture-finalized`  | After context refactor, frontend decision, and scaffold |
| `v5.1-insight-engine-milestone`| After core engine integration milestone                 |
| `v5.2-alpha-release`           | First end-to-end demo deployment                        |

> Tags must be annotated (`-a`) with a meaningful description.

---

## 🔁 Forking Guidelines

- Experimental forks are allowed but must follow naming convention: `feature/<purpose>-fork`
- All forks must be short-lived and either:
  - Merged into `dev`
  - Or explicitly archived with a reference tag (e.g., `v5.0-fork-experiment-diagnostics`)

Forks must include a README with a summary of:
- Purpose
- Divergence point (commit SHA or tag)
- Key architectural assumptions

---

## ⚡ Fast Path: Routine Sprint Backups (default)

Purpose: quickly back work up to GitHub with traceability.

**Developer steps**

1) Commit and push your sprint branch:

   ```bash
   git push -u origin sprintNN/<short-name>
   ```

2. Open a PR into `dev` using the Sprint PR template.

3. Let CI run the guardrails. **Do not paste logs** into the PR.

**CI guardrails (must be green to merge)**

* SSOT validator passes.

* Upload two-line smoke returns 200 (empty upload returns 400).

* "No fallback parser" grep finds 0 matches.

**Outputs**

* CI artifacts contain validator/smoke outputs.

* PR shows pass/fail status; no manual evidence required.

**Scope**

* No tags; no annotated milestone messages. This is backup, not a release.

---

## 🏷️ Milestone/Tag Backups (governed)

Use this section for **stable milestones only** (e.g., after a sprint merges to `dev`). Create an **annotated tag** and ensure traceability.

**Tag workflow**

1) Merge PR to `dev` with CI green.

2) Create annotated tag and push:

   ```bash
   git tag -a vX.Y-sprintNN -m "Sprint NN: <summary>"
   git push origin vX.Y-sprintNN
   ```

3. Verify tag appears under Releases. CI artifacts on the milestone PR serve as evidence.

## 🛡️ Backup Verification Checklist

✅ Run `git tag` to confirm your milestone tag exists  
✅ Run `git branch --show-current` to confirm you are on `main`  
✅ Push tag with `git push origin <tag>`  
✅ Verify on GitHub → "Releases" tab or use `git ls-remote --tags origin`  
✅ Confirm that **tag content matches committed project state**

---

## 🔄 Backup Frequency

- **Manual backups** must occur after:
  - Major architectural decisions
  - Context-wide documentation updates
  - Frontend or backend scaffolding

- **Optional automation**:
  - Use GitHub Actions to trigger a backup tag on successful PR to `main` with `#backup` label

---

## 🧪 Non-production Environments

### Test Database and Local Containers

**Exclusion Policy**: The following environments are **explicitly excluded** from backup strategies and may be destroyed after each test cycle:

- **Local Test Database**: `healthiq_testdb` PostgreSQL container (port 5433)
- **Docker Test Containers**: Any containers created for testing purposes
- **Temporary Test Data**: Data generated during integration, performance, or security tests
- **Local Development Databases**: Any local database instances used for development

### Rationale

- **Test Isolation**: Test databases contain synthetic data and destructive operations
- **Resource Management**: Prevents accumulation of test containers and data
- **Security**: Test environments may contain sensitive test data that should not persist
- **Performance**: Regular cleanup prevents resource leaks and performance degradation

### Cleanup Procedures

- **Nightly Teardown**: Test containers are automatically destroyed after test completion
- **Manual Cleanup**: Developers can run `docker system prune` to clean up test resources
- **CI/CD Integration**: Build pipelines include automatic cleanup of test environments

### Backup Exclusions

The following are **never backed up**:
- Test database containers and volumes
- Temporary test files and logs
- Local development database snapshots
- Test-specific environment configurations

---

## 📘 Related Files

- `PROJECT_STRUCTURE.md` → for canonical folder layout  
- `CURSOR_RULES.md` → for Cursor development constraints  
- `IMPLEMENTATION_PLAN.md` → for milestone definitions  
- `ARCHITECTURE_REVIEW_REPORT.md` → for current stack audit summary  
- `docs/sprints/SPRINT_11_TEST_ISOLATION_AND_SECURITY_VALIDATION.md` → for test isolation details

---

## 🧪 CI guardrails (reference)

The pipeline enforces:

- SSOT validator

- Upload smokes (two-line → 200; empty → 400)

- Repo grep: no fallback/dummy parsers

If any guardrail fails, PRs cannot merge.

---

Maintaining this backup policy ensures that **no architectural context or milestone is ever lost**, even across experimental branches or major refactors, while properly managing test environments.
