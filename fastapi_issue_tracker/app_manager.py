import typing

from fastapi import FastAPI

from fastapi_issue_tracker import auth
from fastapi_issue_tracker.config import settings
from fastapi_issue_tracker.data import crud, models, schemas
from fastapi_issue_tracker.data.database import Database
from fastapi_issue_tracker.routes import router


class AppManager:
    def __init__(self) -> None:
        self._app: typing.Optional[FastAPI] = None

    @staticmethod
    def prepare_db_structure() -> None:
        models.BaseModel.metadata.create_all(bind=Database.ENGINE)

    @staticmethod
    def prepare_db_data() -> None:
        db = Database.get_db_now()
        if crud.get_user_by_username(db, settings.DEFAULT_USER_USERNAME) is None:
            user = schemas.UserCreate(
                full_name=settings.DEFAULT_USER_NAME,
                email=settings.DEFAULT_USER_EMAIL,
                username=settings.DEFAULT_USER_USERNAME,
                password=auth.AUTH_CRYPT_CONTEXT.hash(settings.DEFAULT_USER_PASSWORD),
            )
            crud.create_user(db, user)
        db.close()

    def prepare_app(self) -> None:
        self._app = FastAPI(
            debug=settings.API_DEBUG,
            title=settings.API_TITLE,
            docs_url=None,
            redoc_url=None,
        )

        self._app.include_router(router)

    @property
    def app(self) -> typing.Optional[FastAPI]:
        return self._app
