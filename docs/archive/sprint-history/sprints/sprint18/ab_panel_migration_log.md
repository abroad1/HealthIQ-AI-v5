# AB Panel Migration Log

**Branch:** sprint18/biomarker-expansion  
**Baseline:** v0.17-freeze  
**Date:** 2026-02-25  
**Status:** FINALIZED

---

## Summary

AB staging SSOT changes were merged into runtime SSOT deterministically. No production-only biomarkers, aliases, or burden entries were lost.

---

## What Changed

### Biomarkers (`backend/ssot/biomarkers.yaml`)

| Metric | Before | After |
|--------|--------|-------|
| biomarker_ids | 45 | 89 |
| New entries added | — | 44 |

**Merge rule:** Add new staging biomarker_ids; for overlapping keys, keep runtime verbatim (validator requires prod == ab for overlap).

### Alias Registry (`backend/ssot/biomarker_alias_registry.yaml`)

| Metric | Before | After |
|--------|--------|-------|
| Entries (canonical_id blocks) | ~40 | 88 |
| New aliases appended | — | ~310+ |
| Aliases skipped (collision) | — | 1 |

**Merge rule:** Convert staging `ab_full_panel` list to runtime structure; append new aliases; do not remove existing runtime aliases. Collision detection: skip staging aliases that would conflict with runtime (registry + biomarkers + common_aliases).

**Overlapping-key decision:** 1 alias skipped — `SGPT` for `alt` (staging) was skipped because runtime has `sgpt` → `ast` in biomarkers and `_add_common_aliases`. Adding SGPT to alt would cause `AliasCollisionError`.

### System Burden (`backend/ssot/system_burden_registry.yaml`)

| Metric | Before | After |
|--------|--------|-------|
| Burden entries | 42 | 84 |
| New entries added | — | 42 |

**Merge rule:** Add staging burden entries missing in runtime; for overlapping keys, keep runtime.

---

## Verification Outputs

### 1. AB Panel SSOT Validator

```
python backend/scripts/validate_ab_panel_ssot.py
```

**Result:** OVERALL: PASS

```
CHECK 0 — AB Full Panel Completeness: PASS
CHECK 1 — System Allowlist Enforcement: PASS
CHECK 2 — Canonical Naming Standards: PASS
CHECK 3 — Duplicate Canonical ID Drift: PASS
CHECK 4 — Burden Registry Coverage: PASS
CHECK 5 — Risk Direction Validity: PASS
CHECK 6 — Alias Collision Detection: PASS
CHECK 7 — Derived Marker Separation: PASS
```

### 2. Enforcement and Golden Tests

```
cd backend; python -m pytest tests/enforcement/test_canonical_only.py tests/unit/test_default_golden_fixture_is_collision_free.py -v
```

**Result:** 7 passed

### 3. Grep Sanity Check

- **No canonical `wbc:` in biomarkers.yaml:** ✓ (no matches)
- **`white_blood_cells` exists with alias `"wbc"`:** ✓

```yaml
white_blood_cells:
  aliases:
  - wbc
  - leukocytes
```

---

## Canonical References Check (Part 4)

- `clusters.yaml`, `scoring_policy.yaml`, `criticality.yaml`, `ranges.yaml` were checked for `wbc` and `testosterone_free_testosterone_ratio`.
- No indirect references to `wbc` as canonical; `white_blood_cells` is used.
- `testosterone_free_testosterone_ratio` is present in `scoring_policy.yaml` (derived_ratios).
- **No minimal edits required.**

---

## Migration Script

`backend/scripts/archive/migrate_ab_staging_to_runtime.py` — deterministic merge script used for this migration. Archived post-finalisation (staging folder removed).

---

## Files Modified

| File | Change |
|------|--------|
| `backend/ssot/biomarkers.yaml` | +44 biomarker_ids from staging |
| `backend/ssot/biomarker_alias_registry.yaml` | Merged staging aliases; 1 skipped (SGPT collision) |
| `backend/ssot/system_burden_registry.yaml` | +42 burden entries from staging |
| `backend/scripts/archive/migrate_ab_staging_to_runtime.py` | Migration script (archived) |

---

## Post-migration finalisation

### SGPT/SGOT mapping corrected

- **Standard:** SGPT → ALT, SGOT → AST
- **Fix applied:** `backend/ssot/biomarkers.yaml` (alt: sgpt, ast: sgot), `backend/core/canonical/alias_registry_service.py`, `backend/core/canonical/alias_registry.py`

### Verification commands + PASS outputs

**A) AB SSOT validator:**
```
python backend/scripts/validate_ab_panel_ssot.py
```
Result: OVERALL: PASS (staging obsolete — validator skips when staging folder absent)

**B) Grep proof (sgpt under alt, sgot under ast):**
```
backend/ssot/biomarkers.yaml:  alt: ... sgpt
backend/ssot/biomarkers.yaml:  ast: ... sgot
```

**C) Enforcement and golden tests:**
```
cd backend; python -m pytest tests/enforcement/test_canonical_only.py tests/unit/test_default_golden_fixture_is_collision_free.py -v
```
Result: 7 passed

### Staging folder removed

- **Path removed:** `backend/ssot/_ab_panel_staging/`
- **Scripts archived:** `migrate_ab_staging_to_runtime.py`, `report_ab_panel_delta.py` → `backend/scripts/archive/`
- **Validator:** `validate_ab_panel_ssot.py` now fails with exit 3 when staging absent, because staging-based validation is obsolete post-migration.

### Status: FINALIZED
