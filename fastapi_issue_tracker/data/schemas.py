import typing
from datetime import datetime

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class ItemBase(BaseModel):
    created_at: datetime
    updated_at: typing.Optional[datetime] = None
    is_active: bool


class UserBase(BaseModel):
    full_name: str
    email: str
    username: str
    password: str


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    id: int


class User(ItemBase, UserBase):
    id: int

    class Config:
        orm_mode = True


class ProjectBase(BaseModel):
    name: str
    description: typing.Optional[str] = None


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(ProjectBase):
    id: int


class Project(ItemBase, ProjectBase):
    id: int

    class Config:
        orm_mode = True


class LabelBase(BaseModel):
    name: str
    color_hex_code: typing.Optional[str] = None


class LabelCreate(LabelBase):
    pass


class LabelUpdate(LabelBase):
    id: int


class Label(ItemBase, LabelBase):
    id: int

    class Config:
        orm_mode = True


class IssueBase(BaseModel):
    title: str
    description: str
    status: int


class IssueCreate(IssueBase):
    project_id: int
    labels: typing.List[int] = []


class IssueUpdate(IssueBase):
    id: int
    labels: typing.List[int] = []


class Issue(ItemBase, IssueBase):
    id: int
    project_id: int
    project: Project
    labels: typing.List[Label] = []

    class Config:
        orm_mode = True
