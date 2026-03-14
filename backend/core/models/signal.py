"""
Signal evaluation runtime model.
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class SignalResult(BaseModel):
    signal_id: str
    system: str
    signal_state: str
    signal_value: float
    confidence: Optional[float] = None
    confidence_reasons: Optional[List[str]] = None
    primary_metric: str
    lab_normal_but_flagged: bool = False
    supporting_markers: List[str] = Field(default_factory=list)
    explanation: Optional[Dict[str, Any]] = None

