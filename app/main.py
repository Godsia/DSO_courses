"""
Simple FastAPI application for DAST scanning with OWASP ZAP.
"""
from fastapi import FastAPI

app = FastAPI(title="DSO Courses API", version="1.0.0")


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "DSO Courses API", "status": "ok"}


@app.get("/healthz")
async def healthz():
    """Health check endpoint for CI/CD."""
    return {"status": "healthy"}


@app.get("/api/v1/info")
async def info():
    """API info endpoint."""
    return {
        "service": "DSO Courses",
        "version": "1.0.0",
        "endpoints": ["/", "/healthz", "/api/v1/info"]
    }

