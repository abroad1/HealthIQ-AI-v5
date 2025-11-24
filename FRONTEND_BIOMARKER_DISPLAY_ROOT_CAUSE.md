# Frontend Biomarker Display Root Cause Analysis

## Executive Summary

The /results page is not displaying biomarker names or reference-range arcs correctly due to **two critical issues**:

1. **Missing Score Field**: The `score` field from the backend is not being passed to BiomarkerDials, causing dials to calculate values incorrectly
2. **Incorrect Dial Value Calculation**: The dial value is calculated from biomarker value and reference range instead of using the backend-provided score

## Root Cause Analysis

### Issue 1: Missing Score Field in Biomarker Mapping

**File**: `frontend/app/results/page.tsx:435-449`
**Problem**: The biomarker mapping is missing the `score` field from the backend response.

**Current Code**:
```typescript
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
  // ❌ MISSING: score: biomarker.score
};
```

**Impact**: The BiomarkerDials component cannot access the backend-calculated score, forcing it to calculate dial values from raw biomarker values.

### Issue 2: Incorrect Dial Value Calculation

**File**: `frontend/app/components/biomarkers/BiomarkerDials.tsx:145-151`
**Problem**: The `calculateDialValue` function calculates dial values from biomarker value and reference range instead of using the backend score.

**Current Code**:
```typescript
const calculateDialValue = (value: number, referenceRange?: { min: number; max: number }) => {
  if (!referenceRange) return 50; // Default to middle if no reference range
  
  const range = referenceRange.max - referenceRange.min;
  const normalizedValue = Math.max(0, Math.min(100, ((value - referenceRange.min) / range) * 100));
  return normalizedValue;
};
```

**Impact**: This creates incorrect dial percentages that don't reflect the backend's sophisticated scoring algorithm.

### Issue 3: Interface Mismatch

**File**: `frontend/app/components/biomarkers/BiomarkerDials.tsx:19-29`
**Problem**: The `BiomarkerValue` interface doesn't include the `score` field.

**Current Interface**:
```typescript
interface BiomarkerValue {
  value: number;
  unit: string;
  date?: string;
  referenceRange?: {
    min: number;
    max: number;
    unit: string;
  };
  status?: 'optimal' | 'normal' | 'elevated' | 'low' | 'critical';
  // ❌ MISSING: score?: number;
}
```

## Data Flow Analysis

### Current (Broken) Flow:
1. **Backend** → Returns `{biomarker_name, value, unit, status, score, reference_range}`
2. **Results Page** → Maps to `{value, unit, status, referenceRange}` (❌ drops `score`)
3. **BiomarkerDials** → Calculates dial value from `value` and `referenceRange` (❌ ignores backend score)
4. **Display** → Shows incorrect dial percentages

### Expected (Fixed) Flow:
1. **Backend** → Returns `{biomarker_name, value, unit, status, score, reference_range}`
2. **Results Page** → Maps to `{value, unit, status, score, referenceRange}` (✅ includes `score`)
3. **BiomarkerDials** → Uses `score` directly for dial value (✅ respects backend calculation)
4. **Display** → Shows correct dial percentages

## Minimal Fix Required

### Fix 1: Add Score Field to Biomarker Mapping

**File**: `frontend/app/results/page.tsx:435-449`
**Change**: Add `score: biomarker.score` to the biomarker object mapping.

```typescript
acc[biomarker.biomarker_name] = {
  value: biomarker.value,
  unit: biomarker.unit,
  status: biomarker.status,
  score: biomarker.score, // ✅ ADD THIS LINE
  referenceRange: biomarker.reference_range ? {
    min: biomarker.reference_range.min,
    max: biomarker.reference_range.max,
    unit: biomarker.reference_range.unit
  } : undefined,
  date: created_at
};
```

### Fix 2: Update BiomarkerValue Interface

**File**: `frontend/app/components/biomarkers/BiomarkerDials.tsx:19-29`
**Change**: Add `score?: number` to the interface.

```typescript
interface BiomarkerValue {
  value: number;
  unit: string;
  date?: string;
  score?: number; // ✅ ADD THIS LINE
  referenceRange?: {
    min: number;
    max: number;
    unit: string;
  };
  status?: 'optimal' | 'normal' | 'elevated' | 'low' | 'critical';
}
```

### Fix 3: Use Score for Dial Value Calculation

**File**: `frontend/app/components/biomarkers/BiomarkerDials.tsx:145-151`
**Change**: Modify `calculateDialValue` to use the score field when available.

```typescript
const calculateDialValue = (value: number, referenceRange?: { min: number; max: number }, score?: number) => {
  // ✅ Use backend score if available
  if (score !== undefined) {
    return Math.round(score * 100); // Convert 0-1 score to 0-100 percentage
  }
  
  // Fallback to reference range calculation if no score
  if (!referenceRange) return 50;
  
  const range = referenceRange.max - referenceRange.min;
  const normalizedValue = Math.max(0, Math.min(100, ((value - referenceRange.min) / range) * 100));
  return normalizedValue;
};
```

### Fix 4: Update Dial Value Usage

**File**: `frontend/app/components/biomarkers/BiomarkerDials.tsx:254`
**Change**: Pass the score field to `calculateDialValue`.

```typescript
const dialValue = calculateDialValue(data.value, data.referenceRange, data.score);
```

## Verification Steps

After applying these fixes:

1. **Biomarker Names**: Should display correctly using `BIOMARKER_NAMES` mapping
2. **Reference Range Arcs**: Should show proper min/max ranges from backend
3. **Dial Scores**: Should display backend-calculated scores as percentages
4. **Status Indicators**: Should show correct status from backend

## Expected Results

- **Biomarker Names**: "Glucose", "Total Cholesterol", etc. (not raw `biomarker_name`)
- **Reference Ranges**: "70-100 mg/dL" display with proper arc visualization
- **Dial Percentages**: Backend-calculated scores (e.g., 75% for 0.75 score)
- **Status Badges**: Correct status from backend (normal, elevated, etc.)

## Files to Modify

1. `frontend/app/results/page.tsx` (Line 441) - Add score field
2. `frontend/app/components/biomarkers/BiomarkerDials.tsx` (Lines 19-29, 145-151, 254) - Update interface and calculation

## Impact

These minimal changes will restore proper biomarker display functionality without affecting backend logic or data fetching. The fixes ensure that the frontend respects the backend's sophisticated scoring calculations while maintaining proper reference range visualization.
