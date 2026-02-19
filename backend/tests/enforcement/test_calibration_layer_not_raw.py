"""
v5.3 Sprint 5 - Enforcement: calibration layer must remain raw-free.
"""

from pathlib import Path
import re


def test_calibration_engine_and_registry_no_forbidden_raw_tokens():
    files = [
        Path(__file__).parent.parent.parent / "core" / "analytics" / "calibration_engine.py",
        Path(__file__).parent.parent.parent / "core" / "analytics" / "calibration_registry.py",
    ]
    forbidden_patterns = [
        r"\bbiomarker_panel\b",
        r"\braw_biomarkers\b",
        r"\['value'\]",
        r"['\"]value['\"]\s*:",
        r"\['unit'\]",
        r"['\"]unit['\"]\s*:",
        r"\bmmol\b",
        r"\bmg/dl\b",
        r"\breference_range\b",
        r"\blab_range\b",
        r"['\"]lower['\"]\s*:",
        r"['\"]upper['\"]\s*:",
    ]
    offenders = []
    for file_path in files:
        text = file_path.read_text(encoding="utf-8", errors="ignore").lower()
        for pattern in forbidden_patterns:
            if re.search(pattern, text):
                offenders.append(f"{file_path.name}:{pattern}")
    assert not offenders, "Forbidden raw token(s) found:\n" + "\n".join(offenders)
