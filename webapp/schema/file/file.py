from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class File(BaseModel):
    lesson_id: int = Field(..., example=1)
    type: str = Field(..., example='video')
    description: str = Field(..., example='Видеоурок по основам Python.')
    content_type: str = Field(..., example='video/mp4')
    size: int = Field(..., example=2048)


class FileCreate(File):
    pass

    model_config = ConfigDict(from_attributes=True)


class FileRead(File):
    id: int
    minio_path: str = Field(..., example='path/to/basics-video.mp4')
    uploaded_at: datetime

    model_config = ConfigDict(from_attributes=True)
