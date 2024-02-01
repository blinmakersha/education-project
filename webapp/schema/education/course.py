from pydantic import BaseModel, ConfigDict, Field


class CourseBase(BaseModel):
    title: str = Field(..., example='Introduction to Python')
    description: str = Field(..., example='Learn the basics of Python.')
    author: str = Field(..., example='Jane Doe')
    category: str = Field(..., example='Programming')
    difficulty: str = Field(..., example='Beginner')
    status: str = Field(..., example='Active')


class CourseCreate(CourseBase):
    pass


class CourseRead(CourseBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
