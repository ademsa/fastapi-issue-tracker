import typing

from fastapi import FastAPI

from fastapi_issue_tracker.data import models
from fastapi_issue_tracker.data.database import Database
from fastapi_issue_tracker.routes import get_router


class App:
    def __init__(self, db_host: str, db_name: str, db_user: str, db_password: str):
        self._api: typing.Optional[FastAPI] = None
        self._db: typing.Optional[Database] = None
        self._db_host: str = db_host
        self._db_name: str = db_name
        self._db_user: str = db_user
        self._db_password: str = db_password

    def prepare_db(self) -> None:
        self._db = Database(
            self._db_host, self._db_name, self._db_user, self._db_password
        )

        models.BaseModel.metadata.create_all(bind=self._db.engine)

    def init_api(self) -> None:
        self._api = FastAPI(
            debug=True,
            title="Issue Tracker",
            docs_url=None,
            redoc_url=None,
        )

        if self._db is not None:
            self._api.include_router(get_router(self._db.get_db))

    @property
    def api(self) -> typing.Optional[FastAPI]:
        return self._api
