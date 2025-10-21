from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import analysis, upload, health

app = FastAPI(title="HealthIQ-AI")

# --- CORS setup ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    print("[INIT] Running HealthIQ-AI in fixture-only mode (no database required)")

# --- Router registration ---
app.include_router(health.router, prefix="/api")
app.include_router(upload.router, prefix="/api/upload")
app.include_router(analysis.router, prefix="/api/analysis")
