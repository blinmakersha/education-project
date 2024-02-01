from fastapi.datastructures import UploadFile
from minio import Minio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from webapp.models.sirius.file import File as SQLAFile
from webapp.schema.file.file import FileCreate, FileRead

minio_client = Minio('minio:9000', access_key='admin', secret_key='admin', secure=False)


async def upload_file_to_minio(file: UploadFile) -> str:
    file_path = f'files/{file.filename}'
    minio_client.put_object('yourbucket', file_path, file.file, file.content_type)
    return file_path


async def create_file(session: AsyncSession, file_data: FileCreate, file: UploadFile) -> FileRead:
    minio_path = await upload_file_to_minio(file)
    new_file = SQLAFile(**file_data.model_dump_json(exclude={'lesson_id'}), minio_path=minio_path)
    session.add(new_file)
    await session.commit()
    await session.refresh(new_file)
    return FileRead.model_validate(new_file)


async def get_file_by_id(session: AsyncSession, file_id: int) -> FileRead | None:
    result = await session.execute(select(SQLAFile).where(SQLAFile.id == file_id))
    file = result.scalars().first()
    if file:
        return FileRead.model_validate(file)
    return None


async def delete_file(session: AsyncSession, file_id: int) -> (True | None):
    result = await session.execute(select(SQLAFile).where(SQLAFile.id == file_id))
    file = result.scalars().first()
    if file:
        minio_client.remove_object('yourbucket', file.minio_path)
        await session.delete(file)
        await session.commit()
        return True
