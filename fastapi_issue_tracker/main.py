import os

import uvicorn
from starlette.config import Config

from fastapi_issue_tracker import ENV_FILE_PATH
from fastapi_issue_tracker.app import App


def start() -> None:
    if not os.path.exists(ENV_FILE_PATH):
        print(f"Missing .env file at {ENV_FILE_PATH}")
        return

    config = Config(ENV_FILE_PATH)

    api_host = config("FASTAPI_ISSUE_TRACKER_API_HOST", cast=str, default="127.0.0.1")
    api_port = config("FASTAPI_ISSUE_TRACKER_API_PORT", cast=int, default=7777)
    api_log_level = config(
        "FASTAPI_ISSUE_TRACKER_API_LOG_LEVEL", cast=str, default="info"
    )
    db_host = config("FASTAPI_ISSUE_TRACKER_DB_HOST", cast=str, default=None)
    db_name = config("FASTAPI_ISSUE_TRACKER_DB_NAME", cast=str, default=None)
    db_user = config("FASTAPI_ISSUE_TRACKER_DB_USER", cast=str, default=None)
    db_password = config("FASTAPI_ISSUE_TRACKER_DB_PASSWORD", cast=str, default=None)

    app = App(db_host, db_name, db_user, db_password)
    app.prepare_db()
    app.init_api()

    uvicorn.run(app.api, host=api_host, port=api_port, log_level=api_log_level)


if __name__ == "__main__":
    start()
