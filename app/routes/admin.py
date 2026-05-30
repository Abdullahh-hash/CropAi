# app/routes/admin.py
from fastapi import APIRouter
from app.database import db

router = APIRouter(prefix="/api/admin", tags=["Admin Dashboard Metrics"])

@router.get("/metrics")
async def get_system_metrics():
    return {
        "total_scans_logged": len(db.history),
        "engine_load_status": "nominal",
        "active_definitions_count": len(db.diseases)
    }