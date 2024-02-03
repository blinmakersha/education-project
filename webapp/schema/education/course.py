from pydantic import BaseModel, ConfigDict, Field


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
    id: int = Field(..., example=1)

    model_config = ConfigDict(from_attributes=True)
