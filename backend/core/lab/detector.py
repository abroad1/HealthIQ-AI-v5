"""
Deterministic lab origin detection.

Sprint 2 - No LLM, no OCR, no external calls.
Scans text headers/footers and filename for known lab markers.
"""

import re
from pathlib import Path
from typing import Optional, Dict, Any, Tuple

from core.models.lab_origin import LabOrigin, lab_origin_unknown


# Scan first/last N lines of text
_HEADER_LINES = 40
_FOOTER_LINES = 40

# Confidence by method
_CONF_HEADER = 0.9
_CONF_FOOTER = 0.7
_CONF_FILENAME = 0.4
_CONF_UNKNOWN = 0.0


def _load_registry() -> Dict[str, Any]:
    """Load labs.yaml registry."""
    ssot_path = Path(__file__).parent.parent.parent / "ssot" / "labs.yaml"
    if not ssot_path.exists():
        return {}
    import yaml
    with open(ssot_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data.get("labs", {})


def _match_registry(
    text: str,
    lab_id: str,
    lab_def: Dict[str, Any],
    method: str,
) -> Optional[Tuple[str, float, Optional[str]]]:
    """
    Check if any pattern for lab_id matches text.
    Returns (lab_id, confidence, raw_evidence) or None.
    """
    patterns_def = lab_def.get("patterns", {})
    pattern_list = patterns_def.get(method, [])
    if not pattern_list:
        return None
    conf_map = {
        "header_regex": _CONF_HEADER,
        "footer_regex": _CONF_FOOTER,
        "filename_regex": _CONF_FILENAME,
    }
    conf = conf_map.get(method, _CONF_FILENAME)
    for pat in pattern_list:
        m = re.search(pat, text)
        if m:
            evidence = m.group(0).strip()[:80]
            return (lab_id, conf, evidence)
    return None


def detect_lab_origin(
    text: Optional[str] = None,
    filename: Optional[str] = None,
) -> LabOrigin:
    """
    Detect lab provider from text and/or filename. Deterministic.

    Logic:
    - If text: scan first 40 + last 40 lines, apply header/footer regex.
    - Else if filename: apply filename regex.
    - Else: unknown.

    Returns LabOrigin with method and confidence.
    """
    registry = _load_registry()
    if not registry:
        return lab_origin_unknown()

    best_match: Optional[Tuple[str, float, Optional[str], str]] = None

    if text and text.strip():
        lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
        header_text = "\n".join(lines[:_HEADER_LINES])
        footer_text = "\n".join(lines[-_FOOTER_LINES:]) if len(lines) > _HEADER_LINES else ""

        # Header first (highest confidence)
        for lab_id, lab_def in registry.items():
            m = _match_registry(header_text, lab_id, lab_def, "header_regex")
            if m:
                lid, conf, ev = m
                best_match = (lid, conf, ev, "header_regex")
                break

        # Footer if no header match
        if best_match is None:
            for lab_id, lab_def in registry.items():
                m = _match_registry(footer_text, lab_id, lab_def, "footer_regex")
                if m:
                    lid, conf, ev = m
                    best_match = (lid, conf, ev, "footer_regex")
                    break

    if best_match:
        lab_id, conf, evidence, method = best_match
        lab_def = registry.get(lab_id, {})
        return LabOrigin(
            lab_provider_id=lab_id,
            lab_provider_name=lab_def.get("display_name"),
            detection_method=method,
            detection_confidence=conf,
            raw_evidence=evidence,
        )

    # Filename fallback
    if filename and filename.strip():
        fname = filename.strip()
        for lab_id, lab_def in registry.items():
            m = _match_registry(fname, lab_id, lab_def, "filename_regex")
            if m:
                lid, conf, ev = m
                lab_def = registry.get(lab_id, {})
                return LabOrigin(
                    lab_provider_id=lid,
                    lab_provider_name=lab_def.get("display_name"),
                    detection_method="filename",
                    detection_confidence=conf,
                    raw_evidence=ev,
                )

    return lab_origin_unknown()
