"""
v5.3 Sprint 3 - Enforcement: precedence engine/prompt must stay raw-free.
"""

from pathlib import Path
import re


def test_precedence_engine_has_no_raw_tokens():
    path = Path(__file__).parent.parent.parent / "core" / "analytics" / "precedence_engine.py"
    text = path.read_text(encoding="utf-8", errors="ignore")
    forbidden_patterns = [
        r"['\"]value['\"]\s*:",
        r"\['value'\]",
        r"['\"]reference_range['\"]\s*:",
        r"['\"]unit[s]?['\"]\s*:",
        r"\bbiomarker_panel\b",
        r"\braw_biomarkers\b",
    ]
    offenders = [pattern for pattern in forbidden_patterns if re.search(pattern, text)]
    assert not offenders, "Forbidden raw tokens found in precedence engine: " + ", ".join(offenders)


def test_biological_arbitration_prompt_section_has_no_raw_tokens():
    path = Path(__file__).parent.parent.parent / "core" / "insights" / "prompts.py"
    text = path.read_text(encoding="utf-8", errors="ignore")
    marker = "**Biological Arbitration (code-only):**"
    assert marker in text
    section = text.split(marker, 1)[1].lower()
    forbidden = [
        "reference_range",
        "biomarker_panel",
        "raw_biomarkers",
    ]
    offenders = [token for token in forbidden if token in section]
    assert not offenders, "Forbidden raw tokens found in biological arbitration prompt section: " + ", ".join(offenders)
