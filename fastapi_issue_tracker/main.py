import uvicorn

from fastapi_issue_tracker.app_manager import AppManager
from fastapi_issue_tracker.config import settings


def start() -> None:
    app_manager = AppManager()
    app_manager.prepare_db_structure()
    app_manager.prepare_db_data()
    app_manager.prepare_app()

    uvicorn.run(
        app_manager.app,
        host=settings.API_HOST,
        port=settings.API_PORT,
        log_level=settings.API_LOG_LEVEL,
    )


if __name__ == "__main__":
    start()
