from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from webapp.models.sirius.user import User as SQLAUser
from webapp.schema.login.user import User as PydanticUser, UserCreate, UserLogin, UserRead
from webapp.utils.auth.password import hash_password


async def create_user(session: AsyncSession, user_data: UserCreate) -> PydanticUser:
    hashed_password = hash_password(user_data.password)
    new_user = SQLAUser(
        username=user_data.username,
        hashed_password=hashed_password,
        email=user_data.email,
        role=user_data.role,
        additional_info=user_data.additional_info,
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return PydanticUser.model_validate(new_user)


async def update_user(session: AsyncSession, user_id: int, user_data: UserCreate) -> PydanticUser | None:
    user = await session.get(SQLAUser, user_id)
    if user:
        user.username = user_data.username
        user.hashed_password = hash_password(user_data.password)
        user.email = user_data.email
        user.role = user_data.role
        user.additional_info = user_data.additional_info
        await session.commit()
        await session.refresh(user)
        return PydanticUser.model_validate(user)
    return None


async def get_user(session: AsyncSession, user_info: UserLogin) -> SQLAUser | None:
    return (
        await session.scalars(
            select(SQLAUser).where(
                SQLAUser.username == user_info.username,
                SQLAUser.hashed_password == hash_password(user_info.password),
            )
        )
    ).one_or_none()


async def get_user_by_id(session: AsyncSession, user_id: int) -> UserRead | None:
    result = await session.execute(
        select(SQLAUser).where(SQLAUser.id == user_id).options(joinedload(SQLAUser.subscriptions))
    )
    user = result.scalars().first()
    if user:
        return UserRead.model_validate(user)
    return None


async def delete_user(session: AsyncSession, user_id: int) -> bool:
    user = await session.get(SQLAUser, user_id)
    if user:
        await session.delete(user)
        await session.commit()
        return True
    return False
