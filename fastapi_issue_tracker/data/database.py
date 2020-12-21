from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

from fastapi_issue_tracker.config import settings

BaseModel = declarative_base()


class Database:
    URL = (
        f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}"
        f"@{settings.DB_HOST}/{settings.DB_NAME}"
    )
    ENGINE = create_engine(URL)
    SESSION_LOCAL = sessionmaker(autocommit=False, autoflush=False, bind=ENGINE)

    @staticmethod
    def get_db() -> Session:
        db = Database.SESSION_LOCAL()
        try:
            yield db
        finally:
            db.close()

    @staticmethod
    def get_db_now() -> Session:
        return Database.SESSION_LOCAL()
