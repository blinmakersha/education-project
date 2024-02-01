from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from webapp.models.sirius.lesson import Lesson
from webapp.schema.education.lesson import LessonCreate, LessonRead


async def create_lesson(session: AsyncSession, lesson_data: LessonCreate) -> LessonRead:
    new_lesson = Lesson(**lesson_data.model_dump_json())
    session.add(new_lesson)
    await session.commit()
    await session.refresh(new_lesson)
    return LessonRead.model_validate(new_lesson)


async def get_lesson_by_id(session: AsyncSession, lesson_id: int) -> LessonRead | None:
    result = await session.execute(select(Lesson).where(Lesson.id == lesson_id))
    lesson = result.scalars().first()
    if lesson:
        return LessonRead.model_validate(lesson)
    return None


async def update_lesson(session: AsyncSession, lesson_id: int, lesson_data: LessonCreate) -> LessonRead | None:
    result = await session.execute(select(Lesson).where(Lesson.id == lesson_id))
    lesson = result.scalars().first()
    if lesson:
        for var, value in vars(lesson_data).items():
            setattr(lesson, var, value) if value else None
        await session.commit()
        await session.refresh(lesson)
        return LessonRead.model_validate(lesson)
    return None


async def delete_lesson(session: AsyncSession, lesson_id: int) -> (True | None):
    result = await session.execute(select(Lesson).where(Lesson.id == lesson_id))
    lesson = result.scalars().first()
    if lesson:
        await session.delete(lesson)
        await session.commit()
        return True
