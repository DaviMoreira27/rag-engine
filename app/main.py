from fastapi import FastAPI
from app.modules.file_uploader.router import router as file_uploader_router
from app.modules.web_scraper.router import router as web_scraper_router

def create_app() -> FastAPI:
    app = FastAPI(title="rag-engine")

    @app.get("/health", tags=["health"])
    async def health_check():
        return {"status": "ok"}

    app.include_router(file_uploader_router, prefix="/file-uploader", tags=["file-uploader"])
    app.include_router(web_scraper_router, prefix="/web-scraper", tags=["web-handler"])
    return app

app = create_app()
