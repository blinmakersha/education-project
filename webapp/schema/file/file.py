from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class FileBase(BaseModel):
    type: str = Field(..., example='video')
    description: str = Field(..., example='Видеоурок по основам Python.')
    minio_path: str = Field(..., example='path/to/basics-video.mp4')
    content_type: str = Field(..., example='video/mp4')
    size: int = Field(..., example=2048)


class FileCreate(FileBase):
    lesson_id: int = Field(..., example=1, description='The ID of the lesson this file is associated with.')


class FileRead(FileBase):
    id: int
    uploaded_at: datetime

    model_config = ConfigDict(from_attributes=True)
