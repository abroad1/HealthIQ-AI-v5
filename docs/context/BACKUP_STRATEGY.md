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

## 📘 Related Files

- `PROJECT_STRUCTURE.md` → for canonical folder layout  
- `CURSOR_RULES.md` → for Cursor development constraints  
- `IMPLEMENTATION_PLAN.md` → for milestone definitions  
- `ARCHITECTURE_REVIEW_REPORT.md` → for current stack audit summary  

---

Maintaining this backup policy ensures that **no architectural context or milestone is ever lost**, even across experimental branches or major refactors.
