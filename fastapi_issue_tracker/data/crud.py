import typing
from datetime import datetime

from sqlalchemy.orm import Session

from fastapi_issue_tracker.data import models, schemas


def get_project(
    db: Session, project_id: int
) -> typing.Union[models.Project, typing.Any]:
    return db.query(models.Project).filter(models.Project.id == project_id).first()


def get_projects(
    db: Session, skip: int = 0, limit: int = 100
) -> typing.Union[typing.List, typing.Any]:
    return db.query(models.Project).offset(skip).limit(limit).all()


def create_project(db: Session, project: schemas.ProjectCreate) -> models.Project:
    db_item = models.Project(name=project.name, description=project.description)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_project(db: Session, project: schemas.ProjectUpdate) -> models.Project:
    db_item = get_project(db, project.id)
    db_item.name = project.name
    db_item.description = project.description
    db_item.updated_at = datetime.now()
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def delete_project(db: Session, project_id: int) -> models.Project:
    db_item = get_project(db, project_id)
    db_item.is_active = False
    db_item.updated_at = datetime.now()
    db.add(db_item)
    db.commit()
    return db_item


def get_label(db: Session, label_id: int) -> typing.Union[models.Label, typing.Any]:
    return db.query(models.Label).filter(models.Label.id == label_id).first()


def get_labels(
    db: Session, skip: int = 0, limit: int = 100
) -> typing.Union[typing.List, typing.Any]:
    return db.query(models.Label).offset(skip).limit(limit).all()


def create_label(db: Session, label: schemas.LabelCreate) -> models.Label:
    db_item = models.Label(name=label.name, color_hex_code=label.color_hex_code)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_label(db: Session, label: schemas.LabelUpdate) -> models.Label:
    db_item = get_label(db, label.id)
    db_item.name = label.name
    db_item.color_hex_code = label.color_hex_code
    db_item.updated_at = datetime.now()
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def delete_label(db: Session, label_id: int) -> models.Label:
    db_item = get_label(db, label_id)
    db_item.is_active = False
    db_item.updated_at = datetime.now()
    db.add(db_item)
    db.commit()
    return db_item


def get_issue(db: Session, issue_id: int) -> typing.Union[models.Issue, typing.Any]:
    return db.query(models.Issue).filter(models.Issue.id == issue_id).first()


def get_issues(
    db: Session, skip: int = 0, limit: int = 100
) -> typing.Union[typing.List, typing.Any]:
    return db.query(models.Issue).offset(skip).limit(limit).all()


def create_issue(db: Session, issue: schemas.IssueCreate) -> models.Issue:
    db_item = models.Issue(
        title=issue.title,
        description=issue.description,
        status=issue.status,
        project_id=issue.project_id,
    )
    for label_id in issue.labels:
        db_item.labels.append(get_label(db, label_id))
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_issue(db: Session, issue: schemas.IssueUpdate) -> models.Issue:
    db_item = get_issue(db, issue.id)
    db_item.title = issue.title
    db_item.description = issue.description
    db_item.status = issue.status
    db_item.labels.clear()
    for label_id in issue.labels:
        db_item.labels.append(get_label(db, label_id))
    db_item.updated_at = datetime.now()
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def delete_issue(db: Session, issue_id: int) -> models.Issue:
    db_item = get_issue(db, issue_id)
    db_item.is_active = False
    db_item.updated_at = datetime.now()
    db.add(db_item)
    db.commit()
    return db_item
