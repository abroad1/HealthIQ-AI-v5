"""
v5.3 Sprint 7 - Enforcement: arbitration/conflict/causal-edge engines are raw-free.
"""

import re
from pathlib import Path


def test_arbitration_depth_modules_no_raw_tokens():
    files = [
        Path(__file__).parent.parent.parent / "core" / "analytics" / "conflict_detector.py",
        Path(__file__).parent.parent.parent / "core" / "analytics" / "causal_edge_engine.py",
        Path(__file__).parent.parent.parent / "core" / "analytics" / "arbitration_engine.py",
        Path(__file__).parent.parent.parent / "core" / "analytics" / "conflict_registry.py",
        Path(__file__).parent.parent.parent / "core" / "analytics" / "arbitration_registry.py",
    ]
    forbidden = [
        r"\bbiomarker_panel\b",
        r"\braw_biomarkers\b",
        r"\breference_range\b",
        r"\blab_range\b",
        r"['\"]value['\"]\s*:",
        r"['\"]unit['\"]\s*:",
        r"\bmmol\b",
        r"\bmg/dl\b",
    ]
    offenders = []
    for p in files:
        text = p.read_text(encoding="utf-8", errors="ignore").lower()
        for pattern in forbidden:
            if re.search(pattern, text):
                offenders.append(f"{p.name}:{pattern}")
    assert not offenders, "Forbidden raw token(s) found:\n" + "\n".join(offenders)
