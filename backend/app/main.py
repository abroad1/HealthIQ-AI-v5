"""
HealthIQ-AI v5 Backend - FastAPI Application
Main application entry point with CORS configuration and API routing.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.routes import health, analysis

# Create FastAPI application
app = FastAPI(
    title="HealthIQ-AI v5",
    description="AI-powered biomarker analysis platform",
    version="5.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS for localhost development
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
        "http://127.0.0.1:8080",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes with /api prefix
app.include_router(health.router, prefix="/api", tags=["health"])
app.include_router(analysis.router, prefix="/api", tags=["analysis"])


@app.get("/")
async def root():
    """Root endpoint for basic health check."""
    return JSONResponse(
        content={
            "message": "HealthIQ-AI v5 Backend",
            "version": "5.0.0",
            "docs": "/docs",
            "api_prefix": "/api"
        }
    )


@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Custom 404 handler for API routes."""
    return JSONResponse(
        status_code=404,
        content={"error": "Not found", "message": "API endpoint not found"}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

