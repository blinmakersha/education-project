from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class Lesson(BaseModel):
    title: str = Field(..., example='Введение в Python')
    content: str = Field(..., example='Этот урок познакомит вас с основами Python.')
    order: int = Field(..., example=1)

    model_config = ConfigDict(from_attributes=True)


class LessonCreate(Lesson):
    pass

    model_config = ConfigDict(from_attributes=True)


class LessonRead(Lesson):
    id: int
    course_id: int
    uploaded_at: datetime

    model_config = ConfigDict(from_attributes=True)
