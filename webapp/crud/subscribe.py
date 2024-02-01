from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from webapp.models.sirius.subscribe import Subscription


async def create_subscription(session: AsyncSession, user_id: int, course_id: int) -> Subscription:
    new_subscription = Subscription(user_id=user_id, course_id=course_id)
    session.add(new_subscription)
    await session.commit()
    await session.refresh(new_subscription)
    return new_subscription


async def delete_subscription(session: AsyncSession, user_id: int, course_id: int) -> bool:
    result = await session.execute(
        select(Subscription).where(Subscription.user_id == user_id, Subscription.course_id == course_id)
    )
    subscription = result.scalars().first()
    if subscription:
        await session.delete(subscription)
        await session.commit()
        return True
    return False


async def get_subscriptions_for_user(session: AsyncSession, user_id: int) -> List[Subscription]:
    result = await session.execute(select(Subscription).where(Subscription.user_id == user_id))
    subscriptions = result.scalars().all()
    return subscriptions


async def get_subscriptions_for_course(session: AsyncSession, course_id: int) -> List[Subscription]:
    result = await session.execute(select(Subscription).where(Subscription.course_id == course_id))
    subscriptions = result.scalars().all()
    return subscriptions
