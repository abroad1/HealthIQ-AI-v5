# 🌿 BRANCHING_MODEL.md

## Purpose

Single source of truth for which branches are **active** vs **archived/read-only** in this repo.

---

## Definitions

- **Trunk:** `origin/main` (default branch; all sprint PRs target this unless explicitly stated).
- **Release branches:** `origin/release/*` (optional stabilisation or milestone lines).
- **Active work branches:** `origin/sprint*/...`, `origin/docs/...`.
- **Archived / read-only:** `origin/backup/*`, `origin/restore/*`, `origin/test/*`, and old `origin/feature/*` unless explicitly reactivated.

---

## Rules

- Always branch from `main` unless a release branch is explicitly required.
- Never branch from `backup/*` for new work.
- Do not delete branches as part of normal work; deletion is optional housekeeping after merge or tag.

---

## Current Classification

**Active now**
- `origin/main`
- `origin/release/pre-sprint15-stable`
- `origin/sprint16/cluster-engine-v2`
- `origin/sprint17/prompt-builder-v2`
- `origin/docs/streamlined-backup-governance`

**Archived / read-only**
- `origin/backup-2025-09-21`
- `origin/backup/parsing-sprint-2025-10-05`
- `origin/backup/pre-sprint1`
- `origin/backup/sprint1-2-validated`
- `origin/backup/sprint14-fallback-verified`
- `origin/backup/sprint3-validated`
- `origin/backup/sprint6-validated`
- `origin/backup/sprint7-ready`
- `origin/backup/v5.10-multimodal-stable`
- `origin/feature/sprint16-validation`
- `origin/protection-test`
- `origin/restore/v5.14.0-functional`
- `origin/sprint9d-backup`
- `origin/test/insight-engine-validation`

---

## How to Reactivate an Archived Branch

Create a new branch from `main`, then cherry-pick specific commits. Do not resurrect `backup/*` as a base branch.

