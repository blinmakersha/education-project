from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from pydantic import BaseModel, ConfigDict, Field

if TYPE_CHECKING:
    from webapp.schema.login.user import UserRead


class Course(BaseModel):
    title: str = Field(..., example='Introduction to Python')
    description: str = Field(..., example='Learn the basics of Python.')
    author: str = Field(..., example='Jane Doe')
    category: str = Field(..., example='Programming')
    difficulty: str = Field(..., example='Beginner')
    status: str = Field(..., example='Active')


class CourseCreate(Course):
    pass


class CourseRead(Course):
    id: int
    subscribers: Optional[List[UserRead]] = []

    model_config = ConfigDict(from_attributes=True)
