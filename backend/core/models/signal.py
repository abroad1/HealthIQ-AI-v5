"""
Signal evaluation runtime model.
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class SignalResult(BaseModel):
    signal_id: str
    activation_key: str
    source_spec_id: str
    package_id: str
    provenance_status: str = "LEGACY_INFERRED"
    system: str
    signal_state: str
    signal_value: float
    confidence: Optional[float] = None
    confidence_reasons: Optional[List[str]] = None
    primary_metric: str
    lab_normal_but_flagged: bool = False
    supporting_markers: List[str] = Field(default_factory=list)
    explanation: Optional[Dict[str, Any]] = None
    # ARCH-CONV-E2: ranked Pass 3 hypothesis id selected for this emission (optional).
    selected_hypothesis_id: Optional[str] = None

