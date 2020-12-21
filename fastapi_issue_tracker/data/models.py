from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Table,
    func,
)
from sqlalchemy.orm import relationship

from fastapi_issue_tracker.data.database import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    id = Column(Integer, autoincrement=True, primary_key=True, unique=True, index=True)
    full_name = Column(String, index=True, nullable=False)
    email = Column(String, index=True, nullable=True)
    username = Column(String, index=True, nullable=False)
    password = Column(String, index=True, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, server_default=str(True), nullable=False)


class Project(BaseModel):
    __tablename__ = "projects"

    id = Column(Integer, autoincrement=True, primary_key=True, unique=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, server_default=str(True), nullable=False)


class Label(BaseModel):
    __tablename__ = "labels"

    id = Column(Integer, autoincrement=True, primary_key=True, unique=True, index=True)
    name = Column(String, index=True, nullable=False)
    color_hex_code = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, server_default=str(True), nullable=False)


issues_labels = Table(
    "issues_labels",
    BaseModel.metadata,
    Column("label_id", Integer, ForeignKey("labels.id")),
    Column("issue_id", Integer, ForeignKey("issues.id")),
)


class Issue(BaseModel):
    __tablename__ = "issues"

    id = Column(Integer, autoincrement=True, primary_key=True, unique=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String, nullable=False)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, server_default=str(True), nullable=False)

    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    project = relationship("Project")

    labels = relationship("Label", secondary=issues_labels)
