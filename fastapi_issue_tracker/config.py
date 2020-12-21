from pydantic import BaseSettings

from fastapi_issue_tracker import ENV_FILE_PATH


class Settings(BaseSettings):
    API_DEBUG: bool = False
    API_TITLE: str = "Issue Tracker"
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 3000
    API_LOG_LEVEL: str = "info"
    DB_HOST: str = ""
    DB_NAME: str = "fait"
    DB_USER: str = ""
    DB_PASSWORD: str = ""
    DEFAULT_USER_NAME: str = ""
    DEFAULT_USER_EMAIL: str = ""
    DEFAULT_USER_USERNAME: str = ""
    DEFAULT_USER_PASSWORD: str = ""
    AUTH_SECRET_KEY: str = ""
    AUTH_ALGORITHM: str = "HS256"
    AUTH_ACCESS_TOKEN_EXPIRE_IN_MIN: int = 60

    class Config:
        env_prefix = "FASTAPI_ISSUE_TRACKER_"
        env_file = ENV_FILE_PATH
        case_sensitive = True


settings = Settings()
