from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from datetime import datetime

from app.config import settings
from app.database import db, init_db
from app.routes import scanner, admin

# Initialize database
init_db()

# Create FastAPI application with native slash redirection enabled
app = FastAPI(
    title=settings.APP_NAME,
    description=settings.DESCRIPTION,
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    redirect_slashes=True  # Natively handles matching /admin and /admin/
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
static_dir = Path(__file__).parent.parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Include routers (Ensure API endpoints load first)
app.include_router(scanner.router)
app.include_router(admin.router)

# ==================== Extension Typo Catchers ====================

@app.get("/admin.html", include_in_schema=False)
async def redirect_admin_extension():
    return RedirectResponse(url="/admin/")

@app.get("/index.html", include_in_schema=False)
async def redirect_index_extension():
    return RedirectResponse(url="/")

# ==================== Core UI Routes ====================

@app.get("/")
async def root():
    """Serve main scanner interface"""
    templates_dir = Path(__file__).parent.parent / "templates"
    index_file = templates_dir / "index.html"
    
    if index_file.exists():
        return FileResponse(str(index_file), media_type="text/html")
    
    return HTMLResponse("""
    <html>
        <head>
            <title>Crop Disease Detection</title>
            <style>
                body { font-family: system-ui; background: #0B0F19; color: #fff; 
                       display: flex; justify-content: center; align-items: center; 
                       height: 100vh; margin: 0; }
                .container { text-align: center; }
                h1 { font-size: 2.5rem; margin: 0; color: #10B981; }
                p { font-size: 1.1rem; color: #888; }
                a { color: #34D399; text-decoration: none; font-weight: 600; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🌾 Crop Disease Detection</h1>
                <p>Premium Agricultural Diagnostic System</p>
                <p><a href="/">Open Scanner →</a></p>
                <p><a href="/admin/">Admin Dashboard →</a></p>
                <p><a href="/docs">API Documentation →</a></p>
            </div>
        </body>
    </html>
    """)

@app.get("/admin/")
async def admin_dashboard():
    """Serve admin dashboard interface"""
    templates_dir = Path(__file__).parent.parent / "templates"
    admin_file = templates_dir / "admin.html"
    
    if admin_file.exists():
        return FileResponse(str(admin_file), media_type="text/html")
        
    return HTMLResponse("""
    <html>
        <head>
            <title>Admin Dashboard - Crop Disease Detection</title>
            <style>
                body { font-family: system-ui; background: #0B0F19; color: #fff; padding: 20px; }
                .container { max-width: 1200px; margin: 0 auto; }
                h1 { color: #10B981; }
                a { color: #34D399; text-decoration: none; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>📊 Admin Dashboard</h1>
                <p>Analytics command center loading...</p>
                <p><a href="/">← Back to Scanner</a></p>
            </div>
        </body>
    </html>
    """)

# ==================== Health Check ====================

@app.get("/health")
async def health_check():
    """System health check endpoint"""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "timestamp": datetime.now().isoformat(),
        "database": "operational"
    }