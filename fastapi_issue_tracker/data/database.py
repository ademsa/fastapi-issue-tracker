from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

BaseModel = declarative_base()


class Database:
    def __init__(self, db_host: str, db_name: str, db_user: str, db_password: str):
        self._url = f"postgresql://{db_user}:{db_password}@{db_host}/{db_name}"
        self._engine = create_engine(self._url)
        self._session_local = sessionmaker(
            autocommit=False, autoflush=False, bind=self._engine
        )

    @property
    def engine(self) -> Engine:
        return self._engine

    def get_db(self) -> Session:
        db = self._session_local()
        try:
            yield db
        finally:
            db.close()
