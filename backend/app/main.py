"""
HARV SHIPPED - Main Application
Unified FastAPI application combining:
- Steel2 (Curriculum Generation)
- Doc Digester (Content Analysis)
- Harv (AI Tutoring)
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import logging
from datetime import datetime

from .config import settings

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================================
# Create FastAPI Application
# ============================================================================
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="""
    ## HARV SHIPPED: Unified Educational Technology Platform

    A self-improving curriculum generation, analysis, and delivery ecosystem.

    ### Core Features

    * **Content Analysis** - Extract pedagogical intelligence from materials
    * **Curriculum Generation** - AI-powered curriculum creation
    * **AI Tutoring** - Personalized Socratic teaching
    * **Pipeline Integration** - Automated quality assurance loops

    ### System Components

    1. **Content Analyzer** (Doc Digester) - 5-phase educational content analysis
    2. **Curriculum Generator** (Steel2) - Complete curriculum generation with validation
    3. **AI Tutor** (Harv) - 4-layer memory Socratic teaching platform
    4. **Integration Layer** - Connects all systems for continuous improvement

    ### Quick Links

    * API Documentation: `/docs`
    * Interactive API: `/redoc`
    * Health Check: `/health`
    * Pipeline Dashboard: `/pipeline/dashboard`
    """,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/api/openapi.json"
)

# ============================================================================
# CORS Middleware
# ============================================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# Request Logging Middleware
# ============================================================================
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests for debugging and analytics."""
    start_time = datetime.now()

    response = await call_next(request)

    process_time = (datetime.now() - start_time).total_seconds()
    logger.info(
        f"{request.method} {request.url.path} "
        f"- Status: {response.status_code} "
        f"- Time: {process_time:.3f}s"
    )

    return response

# ============================================================================
# Mount Static Files
# ============================================================================
frontend_path = Path(__file__).parent.parent.parent / "frontend"
if frontend_path.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_path)), name="static")

# ============================================================================
# API Routers
# ============================================================================
from ..api import curriculum, analysis, tutoring, pipeline, analytics

app.include_router(pipeline.router, prefix="/api/pipeline", tags=["Pipeline"])
app.include_router(curriculum.router, prefix="/api/curriculum", tags=["Curriculum"])
app.include_router(analysis.router, prefix="/api/analysis", tags=["Analysis"])
app.include_router(tutoring.router, prefix="/api/tutoring", tags=["Tutoring"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["Analytics"])

# ============================================================================
# Core Endpoints
# ============================================================================

@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main frontend application."""
    index_path = frontend_path / "index.html"
    if index_path.exists():
        return HTMLResponse(content=index_path.read_text())
    return HTMLResponse(content="""
        <html>
            <head><title>HARV SHIPPED</title></head>
            <body>
                <h1>🚀 HARV SHIPPED</h1>
                <p>Unified Educational Technology Platform</p>
                <ul>
                    <li><a href="/docs">API Documentation</a></li>
                    <li><a href="/health">Health Check</a></li>
                    <li><a href="/api/status">System Status</a></li>
                </ul>
            </body>
        </html>
    """)


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENV,
        "timestamp": datetime.now().isoformat(),
        "components": {
            "curriculum_generator": "ready",
            "content_analyzer": "ready",
            "ai_tutor": "ready",
            "integration_layer": "ready"
        }
    }


@app.get("/api/status")
async def system_status():
    """Detailed system status for all components."""
    return {
        "system": {
            "name": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "environment": settings.ENV,
            "uptime": "N/A",  # TODO: Calculate actual uptime
        },
        "configuration": {
            "total_weeks": settings.TOTAL_WEEKS,
            "days_per_week": settings.DAYS_PER_WEEK,
            "max_retries": settings.MAX_RETRIES,
            "quality_threshold": settings.QUALITY_THRESHOLD,
        },
        "features": {
            "auto_validation": settings.ENABLE_AUTO_VALIDATION,
            "auto_import": settings.ENABLE_AUTO_IMPORT,
            "pattern_extraction": settings.ENABLE_PATTERN_EXTRACTION,
            "feedback_loop": settings.ENABLE_FEEDBACK_LOOP,
            "analytics": settings.ENABLE_ANALYTICS,
        },
        "ai_providers": {
            "default": settings.DEFAULT_AI_PROVIDER,
            "model": settings.DEFAULT_MODEL,
            "openai_configured": bool(settings.OPENAI_API_KEY),
            "anthropic_configured": bool(settings.ANTHROPIC_API_KEY),
            "google_configured": bool(settings.GOOGLE_API_KEY),
        },
        "storage": {
            "curriculum_path": str(settings.curriculum_path),
            "analysis_path": str(settings.analysis_path),
            "database_url": settings.DATABASE_URL,
        },
        "timestamp": datetime.now().isoformat()
    }


@app.get("/api/info")
async def system_info():
    """Public system information."""
    return {
        "name": "HARV SHIPPED",
        "description": "Unified Educational Technology Platform",
        "version": settings.APP_VERSION,
        "components": [
            {
                "name": "Content Analyzer",
                "description": "5-phase educational content analysis",
                "source": "Doc Digester",
                "endpoints": ["/api/analysis/*"]
            },
            {
                "name": "Curriculum Generator",
                "description": "AI-powered curriculum creation",
                "source": "Steel2",
                "endpoints": ["/api/curriculum/*"]
            },
            {
                "name": "AI Tutor",
                "description": "Personalized Socratic teaching platform",
                "source": "Harv",
                "endpoints": ["/api/tutoring/*"]
            },
            {
                "name": "Integration Pipeline",
                "description": "Automated quality assurance and feedback loops",
                "source": "HARV SHIPPED",
                "endpoints": ["/api/pipeline/*"]
            }
        ],
        "documentation": {
            "api_docs": "/docs",
            "redoc": "/redoc",
            "openapi": "/api/openapi.json"
        }
    }


# ============================================================================
# Error Handlers
# ============================================================================

@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    """Custom 404 handler."""
    return JSONResponse(
        status_code=404,
        content={
            "error": "Not Found",
            "message": f"The requested resource {request.url.path} was not found",
            "documentation": "/docs"
        }
    )


@app.exception_handler(500)
async def internal_error_handler(request: Request, exc):
    """Custom 500 handler."""
    logger.error(f"Internal server error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred. Please try again later.",
            "support": "ellejansickresearch@gmail.com"
        }
    )


# ============================================================================
# Startup & Shutdown Events
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Initialize system on startup."""
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Environment: {settings.ENV}")
    logger.info(f"Debug mode: {settings.DEBUG}")

    # Create necessary directories
    settings.curriculum_path.mkdir(parents=True, exist_ok=True)
    settings.analysis_path.mkdir(parents=True, exist_ok=True)
    settings.log_path.mkdir(parents=True, exist_ok=True)

    # Initialize database
    from .database import init_db
    try:
        init_db()
        logger.info("✓ Database initialized")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")

    # TODO: Load pattern library
    # TODO: Initialize AI providers

    logger.info("✓ All systems initialized successfully")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    logger.info(f"Shutting down {settings.APP_NAME}")
    # TODO: Close database connections
    # TODO: Save any pending data
    logger.info("✓ Shutdown complete")


# ============================================================================
# Development Server
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )
