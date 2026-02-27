# AB Panel Post-Migration Verification

**Date:** 2026-02-25  
**Scope:** Testosterone ratio classification; SGPT/SGOT alias correctness

---

## 1) Testosterone Ratio (primary vs derived)

### Locations

| File | Line(s) | Definition |
|------|---------|------------|
| `backend/ssot/biomarkers.yaml` | 1161–1173 | Canonical biomarker with `unit: ratio`, `system: hormonal` |
| `backend/ssot/biomarker_alias_registry.yaml` | 620–621 | `canonical_id: testosterone_free_testosterone_ratio` |
| `backend/ssot/scoring_policy.yaml` | 269, 307–312 | In `derived_ratios` list; `derived_ratio_policy_bounds` entry |
| `backend/core/analytics/ratio_registry.py` | 28, 42, 217–230 | In `DERIVED_IDS`; inputs `["testosterone", "free_testosterone"]`; lab-supplied vs computed logic |

### A) Lab supplies ratio with lab range

**Fixture:** Panel with `testosterone`, `free_testosterone`, and `testosterone_free_testosterone_ratio: 0.04`.

**Output:** Ratio appears in `derived_markers.derived` (not primary biomarkers). Lab value is preserved with `source: "lab"`.

```json
{
  "derived": {
    "testosterone_free_testosterone_ratio": {
      "value": 0.04,
      "unit": "ratio",
      "source": "lab",
      "bounds_applied": false,
      "inputs_used": []
    }
  }
}
```

**Note:** The ratio is always in `derived_markers`, never in primary biomarkers. Lab-supplied values are kept with `source: "lab"` and `inputs_used: []`.

### B) Lab does not supply ratio; testosterone and free_testosterone exist

**Fixture:** Panel with `testosterone: 10.96`, `free_testosterone: 277.93` only.

**Output:** Ratio is computed and stored in `derived_markers.derived` with `source: "computed"` and `inputs_used` set.

```json
{
  "derived": {
    "testosterone_free_testosterone_ratio": {
      "value": 0.039,
      "unit": "ratio",
      "source": "computed",
      "bounds_applied": false,
      "inputs_used": [
        "testosterone",
        "free_testosterone"
      ]
    }
  }
}
```

**Provenance:** `source: "computed"` and `inputs_used` clearly indicate the ratio was derived from inputs.

### Verdict: **PASS**

- Lab-supplied ratio is preserved with `source: "lab"` and not overwritten.
- Computed ratio has `source: "computed"` and `inputs_used`.
- Unit tests: `test_testosterone_free_testosterone_ratio_lab_supplied_wins`, `test_testosterone_free_testosterone_ratio_computed_when_inputs_present` both pass.

---

## 2) SGPT/SGOT Alias Correctness

### Standard medical mapping

- **SGPT** = Serum Glutamic Pyruvic Transaminase = **ALT** (Alanine Aminotransferase)
- **SGOT** = Serum Glutamic Oxaloacetic Transaminase = **AST** (Aspartate Aminotransferase)

### Current runtime mapping

| Source | File | Line(s) | Mapping |
|--------|------|---------|---------|
| biomarkers.yaml | `backend/ssot/biomarkers.yaml` | 281 | `alt` aliases include `sgot` |
| biomarkers.yaml | `backend/ssot/biomarkers.yaml` | 297 | `ast` aliases include `sgpt` |
| common_aliases | `backend/core/canonical/alias_registry_service.py` | 236, 239 | `sgot` → `alt`, `sgpt` → `ast` |
| migration script | `backend/scripts/migrate_ab_staging_to_runtime.py` | 96 | `COMMON_ALIASES = {"sgpt": "ast", "sgot": "alt"}` |

### Evidence snippets

**biomarkers.yaml (lines 277–298):**
```yaml
  alt:
    aliases:
    - alt
    - alanine_aminotransferase
    - sgot          # ← WRONG: SGOT = AST
    ...
  ast:
    aliases:
    - aspartate_aminotransferase
    - sgpt          # ← WRONG: SGPT = ALT
```

**alias_registry_service.py (lines 231–239):**
```python
            # Liver
            'alt': 'alt',
            'alanine_aminotransferase': 'alt',
            'sgot': 'alt',      # ← WRONG: SGOT = AST
            'ast': 'ast',
            'aspartate_aminotransferase': 'ast',
            'sgpt': 'ast',      # ← WRONG: SGPT = ALT
```

### Alignment with standard usage

**No.** Current mapping is reversed:

- Current: `sgot` → `alt`, `sgpt` → `ast`
- Correct: `sgot` → `ast`, `sgpt` → `alt`

### Proposed minimal fix (consistent with collision rules)

1. **`backend/ssot/biomarkers.yaml`**
   - `alt`: remove `sgot`, add `sgpt`
   - `ast`: remove `sgpt`, add `sgot`

2. **`backend/core/canonical/alias_registry_service.py`** (`_add_common_aliases`)
   - Change `'sgot': 'alt'` → `'sgot': 'ast'`
   - Change `'sgpt': 'ast'` → `'sgpt': 'alt'`

3. **`backend/scripts/migrate_ab_staging_to_runtime.py`** (if kept)
   - Change `COMMON_ALIASES = {"sgpt": "ast", "sgot": "alt"}` → `{"sgpt": "alt", "sgot": "ast"}`

**Collision:** No new collision. Both aliases map to a single canonical each; only the target canonical changes.

### Verdict: **FAIL**

Current SGPT/SGOT mapping does not match standard usage (SGPT=ALT, SGOT=AST). The proposed fix above corrects it.
