from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import analysis, upload, health, alias_api, questionnaire, auth, wedge_events
from config.database import get_database_url, log_database_config_on_startup, warmup_engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    log_database_config_on_startup()
    if get_database_url():
        try:
            warmup_engine()
            print("[INIT] Database engine warmed up (DATABASE_URL configured).")
        except Exception as exc:
            print(f"[INIT] WARNING: Database warmup failed: {exc}")
    else:
        print("[INIT] DATABASE_URL not set — API runs without DB persistence until configured.")
    yield


app = FastAPI(title="HealthIQ-AI", lifespan=lifespan)

# --- CORS setup ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Router registration ---
app.include_router(health.router, prefix="/api")
app.include_router(upload.router, prefix="/api/upload")
app.include_router(analysis.router, prefix="/api/analysis")
app.include_router(alias_api.router, prefix="/api/biomarker-aliases")
app.include_router(questionnaire.router, prefix="/api/questionnaire")
app.include_router(auth.router, prefix="/api")
app.include_router(wedge_events.router, prefix="/api/wedge-events")
