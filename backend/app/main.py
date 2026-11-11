import logging
import os
import sys
import types

# Ensure 'backend' namespace is mapped when Vercel deploys directly from backend/
_base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _base_dir not in sys.path:
    sys.path.insert(0, _base_dir)

if "backend" not in sys.modules:
    _b = types.ModuleType("backend")
    _b.__path__ = [_base_dir]
    sys.modules["backend"] = _b
else:
    _b = sys.modules["backend"]
    if not hasattr(_b, "__path__"):
        _b.__path__ = [_base_dir]

from backend.app.audit.middleware import CorrelationIdMiddleware
from backend.app.routers import audit, fhir_metadata, health, narrative, patients, smart, ur
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='{"time":"%(asctime)s", "level":"%(levelname)s", "logger":"%(name)s", "message":"%(message)s"}',
)

app = FastAPI(
    title="ClinEfficiency Pro — UR Console API",
    description="Utilization Review Decision Engine & SMART on FHIR Appeal Generator on Google Cloud Platform",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS Configuration - permissive for demo deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# End-to-End Tracing Middleware
app.add_middleware(CorrelationIdMiddleware)

# Root level routes (Liveness and SMART OAuth)
app.include_router(health.router)
app.include_router(smart.router)

# Versioned Routes: Mount under both /api and /api/v1
for prefix in ["/api", "/api/v1"]:
    app.include_router(health.router, prefix=prefix)
    app.include_router(patients.router, prefix=prefix)
    app.include_router(ur.router, prefix=prefix)
    app.include_router(narrative.router, prefix=prefix)
    app.include_router(audit.router, prefix=prefix)
    app.include_router(fhir_metadata.router, prefix=prefix)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)
