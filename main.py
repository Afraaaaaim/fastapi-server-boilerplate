import uvicorn
from app.core.config import get_settings
import os

def _is_docker() -> bool:
    return os.path.exists("/.dockerenv")

if __name__ == "__main__":
    settings = get_settings()
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=settings.port,
        workers=settings.workers,
        reload=settings.is_development and not _is_docker(),
    )