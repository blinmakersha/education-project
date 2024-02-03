from typing import List

from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.education.router import course_router
from webapp.crud.course import create_course, delete_course, get_course_by_id, update_course
from webapp.crud.subscribe import get_subscriptions_for_course
from webapp.db.postgres import get_session
from webapp.schema.education.course import CourseCreate, CourseRead
from webapp.schema.education.subscribe import Subscription
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@course_router.post(
    '/',
    response_model=CourseCreate,
    status_code=status.HTTP_201_CREATED,
    tags=['Courses'],
    response_class=ORJSONResponse,
)
async def create_course_endpoint(course_data: CourseCreate, session: AsyncSession = Depends(get_session)):
    return await create_course(session=session, course_data=course_data)


@course_router.get('/{course_id}', response_model=CourseRead, tags=['Courses'], response_class=ORJSONResponse)
async def get_course_endpoint(
    course_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: JwtTokenT = Depends(jwt_auth.get_current_user),
):
    try:
        response = await get_course_by_id(session=session, course_id=course_id)
        if response is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Course not found')
        return response
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Database error') from e
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e


@course_router.put('/{course_id}', response_model=CourseRead, tags=['Courses'], response_class=ORJSONResponse)
async def update_course_endpoint(
    course_id: int,
    course_data: CourseCreate,
    session: AsyncSession = Depends(get_session),
    current_user: JwtTokenT = Depends(jwt_auth.get_current_user),
):
    if current_user['role'] == 'admin' or 'teacher':
        try:
            response = await update_course(session=session, course_id=course_id, course_data=course_data)
            if response is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Course not found')
            return response
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Database error') from e
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e


@course_router.get('/{course_id}/subscriptions', response_model=List[Subscription], response_class=ORJSONResponse)
async def get_course_subscribers_endpoint(
    course_id: int,
    session: AsyncSession = Depends(get_session),
    surrent_user: JwtTokenT = Depends(jwt_auth.get_current_user),
):
    return await get_subscriptions_for_course(session=session, course_id=course_id)


@course_router.delete(
    '/{course_id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Courses'], response_class=ORJSONResponse
)
async def delete_course_endpoint(
    course_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: JwtTokenT = Depends(jwt_auth.get_current_user),
):
    if current_user['role'] == 'admin' or 'teacher':
        return await delete_course(session=session, course_id=course_id)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Course not found')
