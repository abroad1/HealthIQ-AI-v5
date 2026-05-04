# Sprint 14: Missing Ranges and Biomarkers Diagnostic Report

**Date:** 2025-10-18  
**Issue:** Only 3 biomarkers appear in `/upload?autofill=true` view with missing reference ranges  
**Expected:** 6 biomarkers with complete reference range display  

## Executive Summary

The issue stems from a **mismatch between seeded data and API response logic**. The seeded database contains 6 biomarkers with complete metadata, but the API returns only 3 biomarkers from a hardcoded fallback stub. The frontend correctly displays reference ranges when available, but the API is not returning the seeded data.

## Root Cause Analysis

### 1. **API Fallback Logic Issue** 
**Location:** `backend/app/routes/analysis.py:217-258`

The `/api/analysis/result` endpoint has a fallback mechanism that returns hardcoded stub data when no analysis results are found in the database:

```python
if not result:
    # Fallback to stub result if not found in database
    result = {
        "analysis_id": analysis_id,
        "biomarkers": [
            # Only 3 hardcoded biomarkers: glucose, total_cholesterol, hdl_cholesterol
        ],
        # ... other stub data
    }
```

**Problem:** The seeded analysis exists in the `analyses` table but has no corresponding records in `biomarker_scores` or `analysis_results` tables, triggering the fallback.

### 2. **Missing Analysis Pipeline Execution**
**Location:** `backend/services/storage/persistence_service.py:416-450`

The `get_analysis_result()` method queries:
- `analysis_results` table (empty)
- `biomarker_scores` table (empty) 
- `clusters` table (empty)
- `insights` table (empty)

**Problem:** The seeded analysis was created with `raw_biomarkers` data but never processed through the analysis pipeline to generate scored results.

### 3. **Frontend Data Flow is Correct**
**Location:** `frontend/app/results/page.tsx:417-435`

The frontend correctly maps API response to BiomarkerDials component:

```typescript
<BiomarkerDials 
  biomarkers={biomarkers.reduce((acc, biomarker) => {
    acc[biomarker.biomarker_name] = {
      value: biomarker.value,
      unit: biomarker.unit,
      status: biomarker.status,
      referenceRange: biomarker.reference_range ? {
        min: biomarker.reference_range.min,
        max: biomarker.reference_range.max,
        unit: biomarker.reference_range.unit
      } : undefined,
      date: created_at
    };
    return acc;
  }, {} as Record<string, any>)} 
  showDetails={showDetails}
/>
```

**Status:** ✅ Working correctly - displays reference ranges when present

### 4. **BiomarkerDials Reference Range Display Logic**
**Location:** `frontend/app/components/biomarkers/BiomarkerDials.tsx:273-277, 289-315`

The component correctly renders reference ranges:

```typescript
{data.referenceRange && (
  <div className="text-xs text-gray-500">
    Range: {data.referenceRange.min}-{data.referenceRange.max} {data.referenceRange.unit}
  </div>
)}
```

**Status:** ✅ Working correctly - shows ranges when `referenceRange` is present

## Data Flow Analysis

### Current Flow (Broken)
1. **Seeded Data:** 6 biomarkers in `raw_biomarkers` field ✅
2. **API Query:** `get_analysis_result()` finds analysis but no scored results ❌
3. **Fallback Triggered:** Returns 3 hardcoded biomarkers ❌
4. **Frontend Display:** Shows 3 biomarkers with reference ranges ✅

### Expected Flow (Working)
1. **Seeded Data:** 6 biomarkers in `raw_biomarkers` field ✅
2. **Analysis Pipeline:** Process `raw_biomarkers` → generate `biomarker_scores` ❌
3. **API Query:** `get_analysis_result()` returns scored results ✅
4. **Frontend Display:** Shows 6 biomarkers with reference ranges ✅

## Canonical Name Mismatch Analysis

### Seeded Biomarker Keys vs SSOT Canonical Names

| Seeded Key | SSOT Canonical | Status | Notes |
|------------|----------------|--------|-------|
| `glucose` | `glucose` | ✅ Match | Direct match |
| `hdl` | `hdl_cholesterol` | ❌ Mismatch | Alias vs canonical |
| `ldl` | `ldl_cholesterol` | ❌ Mismatch | Alias vs canonical |
| `triglycerides` | `triglycerides` | ✅ Match | Direct match |
| `cholesterol_total` | `total_cholesterol` | ❌ Mismatch | Different naming |
| `hba1c` | `hba1c` | ✅ Match | Direct match |

**Impact:** The canonical resolver should handle aliases, but the analysis pipeline is not processing the seeded data.

## Evidence Paths

### File Locations and Line References

1. **API Fallback Logic:**
   - `backend/app/routes/analysis.py:217-258`
   - Hardcoded 3 biomarkers in fallback response

2. **Persistence Service:**
   - `backend/services/storage/persistence_service.py:416-450`
   - Queries empty `biomarker_scores` table

3. **Frontend Data Mapping:**
   - `frontend/app/results/page.tsx:417-435`
   - Correctly maps `reference_range` to `referenceRange`

4. **Reference Range Display:**
   - `frontend/app/components/biomarkers/BiomarkerDials.tsx:273-277`
   - Conditional rendering based on `referenceRange` presence

5. **Seeded Data:**
   - `backend/tests/fixtures/seed_test_db.py:26`
   - 6 biomarkers with complete metadata

6. **SSOT Definitions:**
   - `backend/ssot/biomarkers.yaml:1-50`
   - Canonical names and aliases
   - `backend/ssot/ranges.yaml:1-100`
   - Reference range definitions

## Component Filtering Logic

**No filtering occurs in frontend components.** The BiomarkerDials component renders all biomarkers passed to it. The filtering happens at the API level due to the fallback mechanism.

## Recommendations

### Immediate Fix
1. **Process Seeded Data:** Run the seeded analysis through the analysis pipeline to generate `biomarker_scores` records
2. **Fix Canonical Mapping:** Ensure seeded biomarker keys map to SSOT canonical names
3. **Remove Fallback Dependency:** Make the API return actual data instead of falling back to stubs

### Long-term Fix
1. **Complete Analysis Pipeline:** Ensure all analyses go through full processing
2. **Canonical Resolution:** Implement proper alias-to-canonical name mapping
3. **Reference Range Integration:** Connect SSOT ranges to analysis results

## Conclusion

The issue is **not** in the frontend display logic, which works correctly. The problem is that the seeded analysis data is not being processed through the analysis pipeline, causing the API to return hardcoded fallback data instead of the actual seeded biomarkers with their reference ranges.

**Primary Root Cause:** Missing analysis pipeline execution for seeded data  
**Secondary Issue:** Canonical name mismatches between seeded keys and SSOT definitions  
**Frontend Status:** ✅ Working correctly - displays reference ranges when available
