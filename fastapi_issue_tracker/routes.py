import typing

from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

from fastapi_issue_tracker.data import crud, models, schemas


def get_router(get_db: typing.Callable) -> APIRouter:
    router = APIRouter()

    @router.get("/")
    async def index() -> RedirectResponse:
        return RedirectResponse("/openapi.json")

    @router.get("/projects/{project_id}", response_model=schemas.Project)
    def get_project(
        project_id: int = Path(..., ge=1), db: Session = Depends(get_db)
    ) -> models.Project:
        return crud.get_project(db, project_id)

    @router.get("/projects", response_model=typing.List[schemas.Project])
    def get_projects(db: Session = Depends(get_db)) -> typing.List:
        return crud.get_projects(db, 0, 100)

    @router.post("/projects", response_model=schemas.Project)
    def create_project(
        project: schemas.ProjectCreate, db: Session = Depends(get_db)
    ) -> models.Project:
        return crud.create_project(db, project)

    @router.post("/projects/{project_id}", response_model=schemas.Project)
    def update_project(
        project: schemas.ProjectUpdate, db: Session = Depends(get_db)
    ) -> models.Project:
        return crud.update_project(db, project)

    @router.delete("/projects/{project_id}", response_model=schemas.Project)
    def delete_project(
        project_id: int = Path(..., ge=1),
        db: Session = Depends(get_db),
    ) -> models.Project:
        return crud.delete_project(db, project_id)

    @router.get("/labels/{label_id}", response_model=schemas.Label)
    def get_label(
        label_id: int = Path(..., ge=1), db: Session = Depends(get_db)
    ) -> models.Label:
        return crud.get_label(db, label_id)

    @router.get("/labels", response_model=typing.List[schemas.Label])
    def get_labels(db: Session = Depends(get_db)) -> typing.List:
        return crud.get_labels(db, 0, 100)

    @router.post("/labels", response_model=schemas.Label)
    def create_label(
        label: schemas.LabelCreate, db: Session = Depends(get_db)
    ) -> models.Label:
        return crud.create_label(db, label)

    @router.post("/labels/{label_id}", response_model=schemas.Label)
    def update_label(
        label: schemas.LabelUpdate, db: Session = Depends(get_db)
    ) -> models.Label:
        return crud.update_label(db, label)

    @router.delete("/labels/{label_id}", response_model=schemas.Label)
    def delete_label(
        label_id: int = Path(..., ge=1), db: Session = Depends(get_db)
    ) -> models.Label:
        return crud.delete_label(db, label_id)

    @router.get("/issues/{issue_id}", response_model=schemas.Issue)
    def get_issue(
        issue_id: int = Path(..., ge=1), db: Session = Depends(get_db)
    ) -> models.Issue:
        return crud.get_issue(db, issue_id)

    @router.get("/issues", response_model=typing.List[schemas.Issue])
    def get_issues(db: Session = Depends(get_db)) -> typing.List:
        return crud.get_issues(db, 0, 100)

    @router.post("/issues", response_model=schemas.Issue)
    def create_issue(
        issue: schemas.IssueCreate, db: Session = Depends(get_db)
    ) -> models.Issue:
        return crud.create_issue(db, issue)

    @router.post("/issues/{issue_id}", response_model=schemas.Issue)
    def update_issue(
        issue: schemas.IssueUpdate, db: Session = Depends(get_db)
    ) -> models.Issue:
        return crud.update_issue(db, issue)

    @router.delete("/issues/{issue_id}", response_model=schemas.Issue)
    def delete_issue(
        issue_id: int = Path(..., ge=1), db: Session = Depends(get_db)
    ) -> models.Issue:
        return crud.delete_issue(db, issue_id)

    return router
