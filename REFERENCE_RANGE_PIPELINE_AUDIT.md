# Reference Range Pipeline Audit Report

## Executive Summary

This audit reveals a **critical data loss issue** in the HealthIQ AI pipeline: **user-supplied reference ranges are completely stripped out during frontend-to-backend data transmission**. The system currently violates the "lab-as-source" policy by discarding all user-provided reference range data and relying entirely on hard-coded ranges from static configuration files.

## 1. Reference Range Entry Points

### 1.1 LLM Parser (`backend/services/parsing/llm_parser.py`)
- **Lines 27-30**: ParsedBiomarker model includes `reference` (string), `ref_low`, `ref_high` fields
- **Lines 161-188**: `_parse_reference_range()` method extracts numeric limits from reference range strings
- **Lines 222-242**: Reference ranges are parsed and stored in ParsedBiomarker objects
- **Lines 338-342**: Output includes `referenceRange` (camelCase) with parsed min/max values

### 1.2 Upload API (`backend/app/routes/upload.py`)
- **Lines 24-115**: `/api/upload/parse` endpoint processes LLM parser output
- **Lines 90-98**: Returns parsed data with biomarkers containing reference range information

### 1.3 Frontend Upload Processing (`frontend/app/upload/page.tsx`)
- **Lines 289-300**: Converts LLM parser output to frontend format
- **Lines 295-299**: **CRITICAL ISSUE**: Converts `ref_low`/`ref_high` to `referenceRange` object but only for display
- **Lines 140-154**: **DATA LOSS**: When starting analysis, only `name`, `value`, `unit`, `timestamp` are sent to backend

## 2. Reference Range Flow Diagram (Textual)

```
User Upload → LLM Parser → Upload API → Frontend Upload Store
     ↓              ↓           ↓              ↓
  Lab Report → ParsedBiomarker → ParseResponse → ParsedBiomarker[]
     ↓              ↓           ↓              ↓
  "70-100 mg/dL" → ref_low: 70 → referenceRange → referenceRange: {min: 70, max: 100}
     ↓              ref_high: 100   (camelCase)    (camelCase)
     ↓              ↓           ↓              ↓
  Reference Range → String Parse → API Response → Frontend Display
     ↓              ↓           ↓              ↓
  **DATA LOSS** ← **STRIPPED** ← **NOT SENT** ← Analysis Start
     ↓              ↓           ↓              ↓
  Hard-coded → Context Factory → Orchestrator → API Response
     ↓              ↓           ↓              ↓
  ranges.yaml → reference_range: None → reference_range: None → Empty Ranges
```

## 3. Reference Range Mutation Points

### 3.1 Data Loss Point 1: Frontend Analysis Start (`frontend/app/upload/page.tsx:140-154`)
```typescript
const biomarkersObject = parsedData.reduce((acc, biomarker) => {
  acc[biomarker.name] = {
    value: parseFloat(biomarker.value.toString()),
    unit: biomarker.unit,
    timestamp: new Date().toISOString()
    // ❌ referenceRange is completely omitted!
  };
  return acc;
}, {});
```

### 3.2 Data Loss Point 2: Context Factory Input (`backend/core/context/context_factory.py:246`)
```python
reference_range = raw_biomarker.get('reference_range')  # Always None!
```

### 3.3 Hard-coded Injection: Orchestrator (`backend/core/pipeline/orchestrator.py:685,709`)
```python
reference_range=None,  # Always None for all biomarkers
```

### 3.4 Hard-coded Fallback: Analysis API (`backend/app/routes/analysis.py:107-117`)
```python
"reference_range": {
    "min": b.reference_range.get("min") if b.reference_range else None,
    "max": b.reference_range.get("max") if b.reference_range else None,
    "unit": b.reference_range.get("unit", b.unit) if b.reference_range else b.unit,
    "source": b.reference_range.get("source", "lab") if b.reference_range else "lab"
} if b.reference_range else {
    "min": None,
    "max": None,
    "unit": b.unit,
    "source": "lab"
}
```

## 4. Hard-coded Range Detection

### 4.1 Static Range Files
- **`backend/ssot/ranges.yaml`**: Contains hard-coded reference ranges for all biomarkers
- **`backend/ssot/biomarkers.yaml`**: Contains biomarker definitions and units
- **`backend/tools/validation/validate_aliases_and_ranges.py`**: Validates static ranges

### 4.2 Hard-coded Range Usage
- **`backend/core/services/reference_range_service.py`**: Service to lookup ranges from YAML files
- **`backend/core/pipeline/orchestrator.py:682-683`**: **REMOVED**: Was injecting hard-coded ranges
- **`backend/app/routes/analysis.py:107-117`**: Provides fallback empty ranges when user data is missing

### 4.3 Test Fixtures with Hard-coded Ranges
- **`backend/tests/fixtures/sample_analysis.py`**: Contains hard-coded reference ranges
- **`backend/tests/integration/test_persistence_flow.py`**: Uses hard-coded ranges in tests

## 5. Policy Compliance Assessment

### 5.1 Current Violations
1. **Data Loss**: User-supplied reference ranges are completely discarded
2. **Hard-coded Injection**: System relies on static YAML files instead of lab data
3. **No Lab-as-Source**: No mechanism to preserve lab-provided ranges
4. **Silent Failure**: No warnings when user ranges are lost

### 5.2 Expected Behavior
- User uploads lab report with reference ranges
- LLM parser extracts ranges from lab report
- Ranges are preserved through entire pipeline
- Frontend displays lab-provided ranges, not hard-coded ones

### 5.3 Actual Behavior
- User uploads lab report with reference ranges
- LLM parser extracts ranges correctly
- **Ranges are discarded in frontend**
- Backend receives no reference range data
- System falls back to hard-coded ranges (currently None)
- Frontend displays empty ranges

## 6. Downstream System Interactions

### 6.1 Scoring System
- **Impact**: Scoring algorithms receive no reference range data
- **Result**: Cannot perform proper percentile calculations
- **Files**: `backend/core/pipeline/orchestrator.py:678-687`

### 6.2 Clustering System
- **Impact**: Clustering algorithms cannot use reference range context
- **Result**: Reduced clustering accuracy
- **Files**: `backend/core/pipeline/orchestrator.py:726-750`

### 6.3 Insights Generation
- **Impact**: Insights cannot reference normal ranges
- **Result**: Generic insights without range context
- **Files**: `backend/core/pipeline/orchestrator.py:750-800`

### 6.4 Frontend Display
- **Impact**: BiomarkerDials cannot show proper ranges
- **Result**: Empty or incorrect range displays
- **Files**: `frontend/app/results/page.tsx:441-445`

## 7. Recommended Safeguards

### 7.1 Immediate Fixes
1. **Fix Frontend Data Loss** (`frontend/app/upload/page.tsx:140-154`)
   ```typescript
   const biomarkersObject = parsedData.reduce((acc, biomarker) => {
     acc[biomarker.name] = {
       value: parseFloat(biomarker.value.toString()),
       unit: biomarker.unit,
       timestamp: new Date().toISOString(),
       reference_range: biomarker.referenceRange  // ✅ Add this line
     };
     return acc;
   }, {});
   ```

2. **Add Reference Range Validation** (`backend/core/context/context_factory.py:246`)
   ```python
   reference_range = raw_biomarker.get('reference_range')
   if reference_range:
       # Validate and preserve user-supplied ranges
       reference_range = self._validate_reference_range(reference_range)
   ```

3. **Update Orchestrator** (`backend/core/pipeline/orchestrator.py:685,709`)
   ```python
   reference_range=biomarker_score.get('reference_range'),  # Use actual data
   ```

### 7.2 Policy Enforcement
1. **Add Data Loss Warnings**: Log when user ranges are discarded
2. **Source Attribution**: Always preserve `source: "lab"` for user ranges
3. **Validation**: Ensure reference ranges are not silently lost
4. **Testing**: Add tests for reference range preservation

### 7.3 Long-term Improvements
1. **Reference Range Service**: Use for fallbacks only, not primary source
2. **Data Lineage**: Track reference range sources through pipeline
3. **User Feedback**: Show users when their ranges are used vs. defaults
4. **Audit Trail**: Log all reference range transformations

## 8. Critical Findings Summary

| Issue | Severity | Impact | Files Affected |
|-------|----------|--------|----------------|
| Complete data loss of user reference ranges | **CRITICAL** | High | `frontend/app/upload/page.tsx:140-154` |
| Hard-coded range injection | **HIGH** | Medium | `backend/core/pipeline/orchestrator.py` |
| Silent failure mode | **HIGH** | Medium | Multiple files |
| Policy violation | **CRITICAL** | High | Entire pipeline |
| No validation | **MEDIUM** | Low | `backend/core/context/context_factory.py` |

## 9. Conclusion

The HealthIQ AI pipeline currently **completely discards user-supplied reference ranges** and relies on hard-coded fallbacks. This violates the core principle of using lab data as the source of truth and significantly impacts the accuracy of health analysis results. Immediate action is required to fix the data loss in the frontend and ensure reference ranges are preserved throughout the entire pipeline.

**Priority**: Fix the frontend data loss issue immediately, as this is the root cause of all downstream problems.
