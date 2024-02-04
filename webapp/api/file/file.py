from typing import List
from urllib.parse import quote

from fastapi import Depends, File, HTTPException, UploadFile
from fastapi.responses import StreamingResponse
from minio.error import S3Error
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.file.router import file_router
from webapp.crud.file import create_file, delete_file, get_file_by_id, get_files_by_lesson_id
from webapp.db.minio import minio_client
from webapp.db.postgres import get_session
from webapp.schema.file.file import FileCreate, FileRead
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@file_router.post('/upload', response_model=FileRead, tags=['Files'])
async def upload_file_endpoint(
    course_id: int,
    lesson_id: int,
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_session),
    current_user: JwtTokenT = Depends(jwt_auth.get_current_user),
):
    if current_user['role'] not in ['admin', 'teacher']:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Нет доступа для выполнения этой операции')
    try:
        file_data = FileCreate(
            lesson_id=lesson_id,
            type=file.content_type,
            description=file.filename,
            content_type=file.content_type,
            size=len(await file.read()),
        )
        file.file.seek(0)  # Возвращаем указатель в начало файла после его чтения
        return await create_file(
            session=session, file_data=file_data, file=file, course_id=course_id, lesson_id=lesson_id
        )
    except S3Error as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Ошибка хранилища: {str(e)}')
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@file_router.get('/files', response_model=List[FileRead], tags=['Files'])
async def get_files_endpoint(course_id: int, lesson_id: int, session: AsyncSession = Depends(get_session)):
    try:
        result = await get_files_by_lesson_id(session=session, course_id=course_id, lesson_id=lesson_id)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Файлы не найдены')
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@file_router.get('/files/{file_id}', tags=['Files'])
async def download_file_endpoint(
    course_id: int, lesson_id: int, file_id: int, session: AsyncSession = Depends(get_session)
):
    try:
        file_record = await get_file_by_id(session, file_id)
        if not file_record:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Файл не найден')

        file_path = file_record.minio_path
        response = minio_client.get_object(f'course-{course_id}-lesson-{lesson_id}', file_path)
        safe_filename = quote(file_record.description)
        headers = {'Content-Disposition': f'attachment; filename*=utf-8""{safe_filename}'}
        return StreamingResponse(
            response.stream(32 * 1024),
            media_type=file_record.content_type,
            headers=headers,
        )
    except S3Error as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Ошибка хранилища: {str(e)}')
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@file_router.delete('/files/{file_id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Files'])
async def delete_file_endpoint(
    course_id: int,
    lesson_id: int,
    file_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: JwtTokenT = Depends(jwt_auth.get_current_user),
):
    if current_user['role'] not in ['admin', 'teacher']:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Нет доступа для выполнения этой операции')
    try:
        success = await delete_file(session=session, course_id=course_id, lesson_id=lesson_id, file_id=file_id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Файл не найден')
    except S3Error as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Ошибка хранилища: {str(e)}')
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
