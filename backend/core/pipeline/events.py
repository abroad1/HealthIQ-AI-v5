import asyncio
import json
import time
from typing import AsyncIterator, Dict, List

PHASES: List[str] = ["ingest", "normalize", "scoring", "clustering", "insights", "complete"]

def _sse(event: str, payload: Dict) -> bytes:
    # Proper SSE framing: event + data + blank line
    return f"event: {event}\ndata: {json.dumps(payload, separators=(',', ':'))}\n\n".encode("utf-8")

async def stream_status(analysis_id: str) -> AsyncIterator[bytes]:
    # Emit status phases
    n = len(PHASES)
    for i, phase in enumerate(PHASES, 1):
        chunk = _sse("analysis_status", {
            "analysis_id": analysis_id,
            "phase": phase,
            "progress": i / n,
            "updated_at": int(time.time())
        })
        yield chunk
        await asyncio.sleep(0.35)
    # Keep-alive heartbeats so some browsers/devtools don't prematurely close:
    for _ in range(3):
        yield b": heartbeat\n\n"
        await asyncio.sleep(10)
