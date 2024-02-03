from typing import List

from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.login.router import user_router
from webapp.crud.subscribe import get_subscriptions_for_user
from webapp.crud.user import create_user, delete_user, get_user_by_id, update_user
from webapp.db.postgres import get_session
from webapp.schema.education.subscribe import Subscription
from webapp.schema.login.user import User as PydanticUser, UserCreate, UserRead
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@user_router.post('/', response_model=PydanticUser, tags=['Users'], response_class=ORJSONResponse)
async def create_user_endpoint(
    user_data: UserCreate,
    session: AsyncSession = Depends(get_session),
    current_user: JwtTokenT = Depends(jwt_auth.get_current_user),
):
    if current_user['role'] != 'admin':
        raise HTTPException(status_code=403, detail='Нет доступа для выполнения этой операции')
    return await create_user(session=session, user_data=user_data)


@user_router.put('/{user_id}', response_model=PydanticUser, tags=['Users'], response_class=ORJSONResponse)
async def update_user_endpoint(
    user_id: int,
    user_data: UserCreate,
    session: AsyncSession = Depends(get_session),
    current_user: JwtTokenT = Depends(jwt_auth.get_current_user),
):
    if current_user['user_id'] == user_id or current_user['role'] == 'admin':
        return await update_user(session=session, user_id=user_id, user_data=user_data)
    raise HTTPException(status_code=403, detail='Нет доступа для выполнения этой операции')


@user_router.get('/me', response_model=UserRead, tags=['Users'], response_class=ORJSONResponse)
async def get_me_endpoint(
    session: AsyncSession = Depends(get_session),
    current_user: JwtTokenT = Depends(jwt_auth.get_current_user),
):
    user_id: int = current_user['user_id']
    return await get_user_by_id(session=session, user_id=user_id)


@user_router.get('/{user_id}', response_model=UserRead, tags=['Users'], response_class=ORJSONResponse)
async def get_user_by_id_endpoint(
    user_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: JwtTokenT = Depends(jwt_auth.get_current_user),
):
    print(current_user)
    return await get_user_by_id(session=session, user_id=user_id)


@user_router.get(
    '/{user_id}/subscriptions/', response_model=List[Subscription], tags=['Users'], response_class=ORJSONResponse
)
async def get_user_subscriptions_endpoint(
    user_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: JwtTokenT = Depends(jwt_auth.get_current_user),
):
    return await get_subscriptions_for_user(session=session, user_id=user_id)


@user_router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Users'])
async def delete_user_endpoint(
    user_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: JwtTokenT = Depends(jwt_auth.get_current_user),
):
    if current_user['role'] != 'admin':
        raise HTTPException(status_code=403, detail='Нет доступа для выполнения этой операции')
    await delete_user(session=session, user_id=user_id)