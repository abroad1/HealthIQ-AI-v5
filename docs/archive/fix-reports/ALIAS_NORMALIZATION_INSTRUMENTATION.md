# Alias Normalization Path Instrumentation

**Date**: 2025-01-XX  
**Purpose**: Debug why canonical biomarker keys are being incorrectly prefixed as `unmapped_` inside the backend alias resolver

## Summary

Added comprehensive debug logging to trace the alias normalization flow from input to output. This will help identify exactly where and why biomarker keys fail to resolve to their canonical names.

## Changes Made

### 1. `backend/core/canonical/normalize.py`

**Location**: `normalize_biomarkers()` method

**Added**:
- Start-of-function logging: Count and list of all incoming biomarker keys
- Per-key resolution logging: Each biomarker key being processed
- Resolution result logging: Shows the canonical key returned from the alias service
- Warnings for unmapped keys: Clear indication when a key fails to map
- Handling for already-flagged keys: Logs when skipping `unmapped_*` keys

**Sample Output**:
```
[TRACE] --- Alias Normalization Debug Start ---
[TRACE] Processing 5 biomarkers
[TRACE] Incoming key: 'triglycerides'
[TRACE] Incoming key: 'lipoprotein_(a)'
[TRACE] Incoming key: 'c-reactive_protein_crp'
[TRACE] Incoming key: 'magnesium_(venous)'
[TRACE] --- Alias Normalization Debug End ---

[TRACE] Resolving alias for key: 'triglycerides'
[TRACE] Registry lookup result: 'triglycerides'

[TRACE] Resolving alias for key: 'magnesium_(venous)'
[TRACE] Registry lookup result: 'unmapped_magnesium_(venous)'
[WARN] Key 'magnesium_(venous)' failed to map to canonical name → unmapped_magnesium_(venous)
```

### 2. `backend/core/canonical/alias_registry_service.py`

**Location**: `resolve()` method and registry loading

**Added**:
- Registry loading logs: Path and count of loaded entries
- Resolution entry logging: Each key being resolved
- Direct lookup result: Success or failure of direct lookup
- Fuzzy matching logs: When fuzzy matching is used and what it finds
- Final result logging: Shows the final canonical name or unmapped result
- Registry building summary: Total aliases mapped and sample keys

**Sample Output**:
```
[TRACE] [AliasRegistryService] Loading v4 registry from: backend/v4_reference/biomarker_alias_registry.yaml
[TRACE] [AliasRegistryService] Loaded 150 entries from v4 registry
[TRACE] [AliasRegistryService] Registry building complete: 450 aliases mapped
[TRACE] [AliasRegistryService] Sample mappings: ['triglycerides', 'trig', 'triglyceride', ...]

[TRACE] [AliasRegistryService] Resolving: 'triglycerides'
[TRACE] [AliasRegistryService] Direct lookup found: 'triglycerides'

[TRACE] [AliasRegistryService] Resolving: 'magnesium_(venous)'
[TRACE] [AliasRegistryService] Direct lookup failed for: 'magnesium_(venous)'
[TRACE] [AliasRegistryService] No match found, returning: 'unmapped_magnesium_(venous)'
```

### 3. `backend/core/pipeline/orchestrator.py`

**Location**: `create_analysis_context()` method

**Added**:
- Pre-normalization logging: Input biomarker count and keys
- Post-normalization logging: Output biomarker count and keys
- Unmapped keys logging: List of keys that failed to normalize

**Sample Output**:
```
[TRACE] [Orchestrator] Starting normalization in create_analysis_context
[TRACE] [Orchestrator] Input biomarkers count: 5
[TRACE] [Orchestrator] Input biomarker keys: ['triglycerides', 'lipoprotein_(a)', ...]

[TRACE] --- Alias Normalization Debug Start ---
[... normalization logs ...]

[TRACE] [Orchestrator] Normalization complete
[TRACE] [Orchestrator] Output biomarker keys: ['triglycerides', 'lipoprotein_a', ...]
[TRACE] [Orchestrator] Unmapped keys: []
```

## What This Will Reveal

1. **Registry Loading**: Whether the v4 alias registry loads successfully
2. **Registry Contents**: How many aliases are available and what they map to
3. **Input Keys**: Exact biomarker keys coming into the normalization process
4. **Resolution Process**: Step-by-step resolution for each key (direct lookup → fuzzy match → unmapped)
5. **Failed Mappings**: Which specific keys fail and why
6. **Output Keys**: Final canonical names produced after normalization

## Expected Diagnostic Output

When running an analysis with problematic biomarker keys, you'll see output like:

```
[TRACE] [Orchestrator] Starting normalization in create_analysis_context
[TRACE] [Orchestrator] Input biomarkers count: 5
[TRACE] [Orchestrator] Input biomarker keys: ['triglycerides', 'lipoprotein_(a)', 'c-reactive_protein_crp', 'magnesium_(venous)', 'vitamin_d']

[TRACE] --- Alias Normalization Debug Start ---
[TRACE] Processing 5 biomarkers
[TRACE] Incoming key: 'triglycerides'
[TRACE] Incoming key: 'lipoprotein_(a)'
[TRACE] Incoming key: 'c-reactive_protein_crp'
[TRACE] Incoming key: 'magnesium_(venous)'
[TRACE] Incoming key: 'vitamin_d'
[TRACE] --- Alias Normalization Debug End ---

[TRACE] Resolving alias for key: 'triglycerides'
[TRACE] [AliasRegistryService] Resolving: 'triglycerides'
[TRACE] [AliasRegistryService] Direct lookup found: 'triglycerides'
[TRACE] Registry lookup result: 'triglycerides'

[TRACE] Resolving alias for key: 'magnesium_(venous)'
[TRACE] [AliasRegistryService] Resolving: 'magnesium_(venous)'
[TRACE] [AliasRegistryService] Direct lookup failed for: 'magnesium_(venous)'
[TRACE] [AliasRegistryService] No match found, returning: 'unmapped_magnesium_(venous)'
[TRACE] Registry lookup result: 'unmapped_magnesium_(venous)'
[WARN] Key 'magnesium_(venous)' failed to map to canonical name → unmapped_magnesium_(venous)

[TRACE] [Orchestrator] Normalization complete
[TRACE] [Orchestrator] Output biomarker keys: ['triglycerides', 'lipoprotein_a', 'crp', 'unmapped_magnesium_(venous)', 'vitamin_d']
[TRACE] [Orchestrator] Unmapped keys: ['magnesium_(venous)']
```

## Next Steps

1. **Run the backend** with a test analysis that includes problematic biomarker keys
2. **Examine the console output** to see the complete normalization flow
3. **Identify the root cause**:
   - Are keys missing from the registry?
   - Is the resolver logic re-running and double-prefixing?
   - Are the input keys in an unexpected format?
4. **Fix the issue** based on what the logs reveal

## Testing

To test this instrumentation:

```bash
# Start the backend
cd backend
python -m uvicorn app.main:app --reload

# Upload a blood panel with various biomarker keys (including some that might fail)
# Watch the console output for the detailed trace logs
```

## Notes

- All debug logging uses the `[TRACE]` prefix for easy filtering
- Warnings use `[WARN]` prefix
- Errors use `[ERROR]` prefix
- This instrumentation is temporary and should be removed after identifying the root cause
