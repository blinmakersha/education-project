from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from webapp.schema.file.file import FileRead


class LessonBase(BaseModel):
    title: str = Field(..., example='Введение в Python')
    content: str = Field(..., example='Этот урок познакомит вас с основами Python.')
    order: int = Field(..., example=1)

    model_config = ConfigDict(from_attributes=True)


class LessonCreate(LessonBase):
    course_id: int = Field(..., example=1)


class LessonRead(LessonBase):
    id: int
    uploaded_at: datetime
    files: Optional[List[FileRead]] = []

    class Config:
        orm_mode = True
