from typing import List

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.login.router import user_router
from webapp.crud.subscribe import get_subscriptions_for_user
from webapp.crud.user import (create_user, delete_user, get_user_by_id,
                              update_user)
from webapp.db.postgres import get_session
from webapp.schema.education.subscribe import Subscription
from webapp.schema.login.user import User as PydanticUser
from webapp.schema.login.user import UserCreate
from webapp.utils.auth.user import get_current_user


@user_router.post('/users/', response_model=PydanticUser)
async def create_user_endpoint(user_data: UserCreate, current_user: PydanticUser = Depends(get_current_user)):
    return await create_user(user_data)


@user_router.put('/users/{user_id}', response_model=PydanticUser)
async def update_user_endpoint(
    user_id: int, user_data: UserCreate, current_user: PydanticUser = Depends(get_current_user)
):
    if current_user.id != user_id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail='Нет доступа для выполнения этой операции')
    return await update_user(user_id, user_data)


@user_router.get('/users/{user_id}', response_model=PydanticUser)
async def get_user_by_id_endpoint(user_id: int, current_user: PydanticUser = Depends(get_current_user)):
    if current_user.id != user_id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail='Нет доступа для выполнения этой операции')
    return await get_user_by_id(user_id)


@user_router.get('/users/{user_id}/subscriptions/', response_model=List[Subscription])
async def get_user_subscriptions_endpoint(
    user_id: int, session: AsyncSession = Depends(get_session), current_user: PydanticUser = Depends(get_current_user)
):
    subscriptions = await get_subscriptions_for_user(session, user_id)
    return subscriptions


@user_router.delete('/users/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_endpoint(user_id: int, current_user: PydanticUser = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail='Нет доступа для выполнения этой операции')
    await delete_user(user_id)
