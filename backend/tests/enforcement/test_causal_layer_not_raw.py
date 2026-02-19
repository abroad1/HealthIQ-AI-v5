"""
v5.3 Sprint 4 - Enforcement: causal layer implementation must remain raw-free.
"""

from pathlib import Path
import re


def test_causal_layer_engine_and_registry_no_forbidden_raw_tokens():
    files = [
        Path(__file__).parent.parent.parent / "core" / "analytics" / "causal_layer_engine.py",
        Path(__file__).parent.parent.parent / "core" / "analytics" / "causal_layer_registry.py",
    ]
    forbidden_patterns = [
        r"\bbiomarker_panel\b",
        r"\braw_biomarkers\b",
        r"\['value'\]",
        r"['\"]value['\"]\s*:",
        r"['\"]unit['\"]\s*:",
        r"\bmmol\b",
        r"\bmg/dl\b",
        r"\breference_range\b",
        r"\blab_range\b",
    ]
    offenders = []
    for p in files:
        text = p.read_text(encoding="utf-8", errors="ignore").lower()
        for pattern in forbidden_patterns:
            if re.search(pattern, text):
                offenders.append(f"{p.name}:{pattern}")
    assert not offenders, "Forbidden raw token(s) found:\n" + "\n".join(offenders)
