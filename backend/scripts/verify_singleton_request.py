#!/usr/bin/env python
"""
Verify that a single request flow shows:
- Registry built once
- No repeated "Registry building complete" or "Loading..." 
"""
import sys
sys.path.insert(0, ".")

# Clear singleton cache to simulate fresh process
from core.canonical.alias_registry_service import get_alias_registry_service
get_alias_registry_service.cache_clear()

# Capture prints
from io import StringIO
import contextlib

buf = StringIO()
with contextlib.redirect_stdout(buf):
    from core.canonical.normalize import normalize_biomarkers_with_metadata, BiomarkerNormalizer

    biomarkers = {
        "hdl": {"value": 45.0, "unit": "mg/dL", "reference_range": {"min": 40, "max": 60, "unit": "mg/dL", "source": "lab"}},
        "ldl": {"value": 120.0, "unit": "mg/dL", "reference_range": {"min": 0, "max": 100, "unit": "mg/dL", "source": "lab"}},
        "total_cholesterol": {"value": 200.0, "unit": "mg/dL", "reference_range": {"min": 0, "max": 200, "unit": "mg/dL", "source": "lab"}},
        "triglycerides": {"value": 150.0, "unit": "mg/dL", "reference_range": {"min": 0, "max": 150, "unit": "mg/dL", "source": "lab"}},
    }

    # Simulate route + orchestrator flow: multiple normalizers share singleton
    normalized = normalize_biomarkers_with_metadata(biomarkers)
    n2 = BiomarkerNormalizer()
    n2.normalize_biomarkers({k: v.get("value", v) for k, v in normalized.items()})
    n3 = BiomarkerNormalizer()
    n3.get_canonical_biomarkers()

output = buf.getvalue()

# Count occurrences
registry_build_count = output.count("Registry built:")
registry_complete_count = output.count("Registry building complete")
loading_count = output.count("Loading SSOT")
loading_biomarkers_count = output.count("Loading aliases from SSOT")

print("=== SINGLE REQUEST LOG VERIFICATION ===")
print(output)
print("=== COUNTS ===")
print(f"  'Registry built:' count: {registry_build_count}")
print(f"  'Registry building complete' count: {registry_complete_count}")
print(f"  'Loading SSOT' count: {loading_count}")
print(f"  'Loading aliases from SSOT' count: {loading_biomarkers_count}")
print()
if registry_build_count <= 1 and registry_complete_count == 0 and loading_count == 0:
    print("OK: Registry built once; no noisy legacy logs.")
else:
    print("FAIL: Registry should be built at most once.")
    sys.exit(1)
