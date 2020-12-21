import typing

from fastapi import APIRouter, Depends, HTTPException, Path
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import RedirectResponse

from fastapi_issue_tracker import auth
from fastapi_issue_tracker.data import crud, models, schemas
from fastapi_issue_tracker.data.database import Database
from fastapi_issue_tracker.data.schemas import Token

router = APIRouter()


@router.get("/")
async def index() -> RedirectResponse:
    return RedirectResponse("/openapi.json")


@router.post("/auth", response_model=schemas.Token)
def get_auth_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(Database.get_db),
) -> schemas.Token:
    user = auth.verify_user_credentials(form_data.username, form_data.password, db)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username or password not valid.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = auth.generate_token(user.username)

    return Token(access_token=access_token, token_type="bearer")


@router.get(
    "/users/{user_id}",
    response_model=schemas.User,
    dependencies=[Depends(auth.get_current_user)],
)
def get_user(
    user_id: int = Path(..., ge=1), db: Session = Depends(Database.get_db)
) -> models.User:
    return crud.get_user(db, user_id)


@router.get("/users", dependencies=[Depends(auth.get_current_user)])
def get_users(db: Session = Depends(Database.get_db)) -> typing.List:
    return crud.get_users(db, 0, 100)


@router.post(
    "/users",
    response_model=schemas.User,
    dependencies=[Depends(auth.get_current_user)],
)
def create_user(
    user: schemas.UserCreate, db: Session = Depends(Database.get_db)
) -> models.User:
    user.password = auth.AUTH_CRYPT_CONTEXT.hash(user.password)
    return crud.create_user(db, user)


@router.post(
    "/users/{user_id}",
    response_model=schemas.User,
    dependencies=[Depends(auth.get_current_user)],
)
def update_user(
    user: schemas.UserUpdate, db: Session = Depends(Database.get_db)
) -> models.User:
    user.password = auth.AUTH_CRYPT_CONTEXT.hash(user.password)
    return crud.update_user(db, user)


@router.delete(
    "/users/{user_id}",
    response_model=schemas.User,
    dependencies=[Depends(auth.get_current_user)],
)
def delete_user(
    user_id: int = Path(..., ge=1),
    db: Session = Depends(Database.get_db),
) -> models.User:
    return crud.delete_user(db, user_id)


@router.get("/projects/{project_id}", response_model=schemas.Project)
def get_project(
    project_id: int = Path(..., ge=1), db: Session = Depends(Database.get_db)
) -> models.Project:
    return crud.get_project(db, project_id)


@router.get("/projects")
def get_projects(db: Session = Depends(Database.get_db)) -> typing.List:
    return crud.get_projects(db, 0, 100)


@router.post(
    "/projects",
    response_model=schemas.Project,
    dependencies=[Depends(auth.get_current_user)],
)
def create_project(
    project: schemas.ProjectCreate, db: Session = Depends(Database.get_db)
) -> models.Project:
    return crud.create_project(db, project)


@router.post(
    "/projects/{project_id}",
    response_model=schemas.Project,
    dependencies=[Depends(auth.get_current_user)],
)
def update_project(
    project: schemas.ProjectUpdate, db: Session = Depends(Database.get_db)
) -> models.Project:
    return crud.update_project(db, project)


@router.delete(
    "/projects/{project_id}",
    response_model=schemas.Project,
    dependencies=[Depends(auth.get_current_user)],
)
def delete_project(
    project_id: int = Path(..., ge=1),
    db: Session = Depends(Database.get_db),
) -> models.Project:
    return crud.delete_project(db, project_id)


@router.get("/labels/{label_id}", response_model=schemas.Label)
def get_label(
    label_id: int = Path(..., ge=1), db: Session = Depends(Database.get_db)
) -> models.Label:
    return crud.get_label(db, label_id)


@router.get("/labels", response_model=typing.List[schemas.Label])
def get_labels(db: Session = Depends(Database.get_db)) -> typing.List:
    return crud.get_labels(db, 0, 100)


@router.post(
    "/labels",
    response_model=schemas.Label,
    dependencies=[Depends(auth.get_current_user)],
)
def create_label(
    label: schemas.LabelCreate, db: Session = Depends(Database.get_db)
) -> models.Label:
    return crud.create_label(db, label)


@router.post(
    "/labels/{label_id}",
    response_model=schemas.Label,
    dependencies=[Depends(auth.get_current_user)],
)
def update_label(
    label: schemas.LabelUpdate, db: Session = Depends(Database.get_db)
) -> models.Label:
    return crud.update_label(db, label)


@router.delete(
    "/labels/{label_id}",
    response_model=schemas.Label,
    dependencies=[Depends(auth.get_current_user)],
)
def delete_label(
    label_id: int = Path(..., ge=1), db: Session = Depends(Database.get_db)
) -> models.Label:
    return crud.delete_label(db, label_id)


@router.get("/issues/{issue_id}", response_model=schemas.Issue)
def get_issue(
    issue_id: int = Path(..., ge=1), db: Session = Depends(Database.get_db)
) -> models.Issue:
    return crud.get_issue(db, issue_id)


@router.get("/issues", response_model=typing.List[schemas.Issue])
def get_issues(db: Session = Depends(Database.get_db)) -> typing.List:
    return crud.get_issues(db, 0, 100)


@router.post(
    "/issues",
    response_model=schemas.Issue,
    dependencies=[Depends(auth.get_current_user)],
)
def create_issue(
    issue: schemas.IssueCreate, db: Session = Depends(Database.get_db)
) -> models.Issue:
    return crud.create_issue(db, issue)


@router.post(
    "/issues/{issue_id}",
    response_model=schemas.Issue,
    dependencies=[Depends(auth.get_current_user)],
)
def update_issue(
    issue: schemas.IssueUpdate, db: Session = Depends(Database.get_db)
) -> models.Issue:
    return crud.update_issue(db, issue)


@router.delete(
    "/issues/{issue_id}",
    response_model=schemas.Issue,
    dependencies=[Depends(auth.get_current_user)],
)
def delete_issue(
    issue_id: int = Path(..., ge=1), db: Session = Depends(Database.get_db)
) -> models.Issue:
    return crud.delete_issue(db, issue_id)
