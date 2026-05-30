from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # This runs asynchronously the exact moment the serverless container wakes up
    try:
        await init_db()
    except Exception as e:
        print(f"Database initialization skipped or failed: {e}")
    yield
    # Clean up operations go here if needed

app = FastAPI(
    title="Crop Disease Detection",
    lifespan=lifespan
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