"""
Analysis event streaming - implements async SSE generator for analysis phases.
"""

import asyncio
import json
from datetime import datetime
from typing import AsyncGenerator, Dict, Any

from core.models.context import AnalysisEvent


class AnalysisEventStream:
    """Server-Sent Events stream for analysis progress."""
    
    # Analysis phases with their descriptions
    PHASES = [
        ("ingest", "Ingesting biomarker data"),
        ("normalize", "Normalizing biomarker names"),
        ("scoring", "Calculating biomarker scores"),
        ("clustering", "Identifying biomarker clusters"),
        ("insights", "Generating health insights"),
        ("complete", "Analysis complete")
    ]
    
    def __init__(self, analysis_id: str):
        """
        Initialize the event stream.
        
        Args:
            analysis_id: Analysis identifier for events
        """
        self.analysis_id = analysis_id
    
    async def generate_events(self) -> AsyncGenerator[str, None]:
        """
        Generate SSE events for analysis progress.
        
        Yields:
            str: SSE-formatted event strings
        """
        total_phases = len(self.PHASES)
        
        for i, (phase, description) in enumerate(self.PHASES):
            # Calculate progress percentage
            progress = (i / (total_phases - 1)) * 100 if total_phases > 1 else 100
            
            # Create analysis event
            event = AnalysisEvent(
                analysis_id=self.analysis_id,
                phase=phase,
                progress=progress,
                status="running" if phase != "complete" else "complete",
                message=description,
                updated_at=datetime.utcnow().isoformat()
            )
            
            # Format as SSE event
            event_data = event.model_dump()
            sse_event = self._format_sse_event("analysis_status", event_data)
            
            yield sse_event
            
            # Add small delay between phases (except for the last one)
            if phase != "complete":
                await asyncio.sleep(1.0)  # 1 second delay between phases
    
    def _format_sse_event(self, event_name: str, data: Dict[str, Any]) -> str:
        """
        Format data as Server-Sent Event.
        
        Args:
            event_name: Name of the SSE event
            data: Event data dictionary
            
        Returns:
            str: Formatted SSE event string
        """
        # Convert data to JSON
        json_data = json.dumps(data, ensure_ascii=False)
        
        # Format as SSE event
        sse_lines = [
            f"event: {event_name}",
            f"data: {json_data}",
            "",  # Empty line to end the event
        ]
        
        return "\n".join(sse_lines)
    
    async def generate_error_event(self, error_message: str) -> str:
        """
        Generate an error event.
        
        Args:
            error_message: Error message to include
            
        Returns:
            str: Formatted SSE error event
        """
        event = AnalysisEvent(
            analysis_id=self.analysis_id,
            phase="error",
            progress=0.0,
            status="error",
            message=error_message,
            updated_at=datetime.utcnow().isoformat()
        )
        
        return self._format_sse_event("analysis_status", event.model_dump())
