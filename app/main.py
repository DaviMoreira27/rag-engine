from fastapi import FastAPI, APIRouter
from app.modules.file_uploader.router import router as file_uploader_router
from app.modules.web_scraper.router import router as web_scraper_router
from app.modules.user.router import router as user_router
from app.http.exception_handler import setup_exception_handlers
from app.core.config.service import Config

def create_app() -> FastAPI:
    Config.validate_all()

    app = FastAPI(title="rag-engine")

    # Setup exception handlers
    setup_exception_handlers(app)

    @app.get("/health", tags=["health"])
    async def health_check():
        return {"status": "ok"}

    api_router = APIRouter(prefix="/api")

    api_router.include_router(file_uploader_router, prefix="/file-uploader", tags=["file-uploader"])
    api_router.include_router(web_scraper_router, prefix="/web-scraper", tags=["web-handler"])
    api_router.include_router(user_router, prefix="/user", tags=["user"])

    app.include_router(api_router)

    return app

app = create_app()
