from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from datetime import datetime

from app.config import settings
from app.database import init_db
from app.routes import scanner, admin

# Initialize database
init_db()

app = FastAPI(
    title=settings.APP_NAME,
    description=settings.DESCRIPTION,
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    redirect_slashes=True
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

static_dir = Path(__file__).parent.parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Restoring your actual routing modules cleanly
app.include_router(scanner.router)
app.include_router(admin.router)

@app.get("/admin.html", include_in_schema=False)
async def redirect_admin_extension():
    return RedirectResponse(url="/admin/")

@app.get("/index.html", include_in_schema=False)
async def redirect_index_extension():
    return RedirectResponse(url="/")

@app.get("/")
async def root():
    templates_dir = Path(__file__).parent.parent / "templates"
    index_file = templates_dir / "index.html"
    if index_file.exists():
        return FileResponse(str(index_file), media_type="text/html")

@app.get("/admin/")
async def admin_dashboard():
    templates_dir = Path(__file__).parent.parent / "templates"
    admin_file = templates_dir / "admin.html"
    if admin_file.exists():
        return FileResponse(str(admin_file), media_type="text/html")

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "timestamp": datetime.now().isoformat(),
        "database": "operational"
    }