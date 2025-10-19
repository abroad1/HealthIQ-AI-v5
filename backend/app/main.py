from fastapi import FastAPI
from app.routes import analysis

app = FastAPI(title="HealthIQ-AI")

@app.on_event("startup")
async def startup_event():
    print("[INIT] Running HealthIQ-AI in fixture-only mode (no database required)")

app.include_router(analysis.router, prefix="/api/analysis")