from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from webapp.models.sirius.lesson import Lesson
from webapp.schema.education.lesson import LessonCreate, LessonRead


async def create_lesson(session: AsyncSession, course_id: int, lesson_data: LessonCreate) -> LessonRead:
    new_lesson = Lesson(course_id=course_id, **lesson_data.model_dump())
    session.add(new_lesson)
    await session.commit()
    await session.refresh(new_lesson)
    return LessonRead.model_validate(new_lesson)


async def get_lessons_all_by_course_id(session: AsyncSession, course_id: int) -> List[LessonRead] | None:
    result = await session.execute(select(Lesson).where(Lesson.course_id == course_id))
    all_lessons = result.scalars().all()
    if all_lessons:
        return [LessonRead.model_validate(lesson) for lesson in all_lessons]
    return None


async def get_lesson_by_id(session: AsyncSession, course_id: int, lesson_id: int) -> LessonRead | None:
    result = await session.execute(select(Lesson).where(Lesson.id == lesson_id, Lesson.course_id == course_id))
    lesson = result.scalars().first()
    if lesson:
        return LessonRead.model_validate(lesson)
    return None


async def update_lesson(
    session: AsyncSession, course_id: int, lesson_id: int, lesson_data: LessonCreate
) -> LessonRead | None:
    result = await session.execute(select(Lesson).where(Lesson.id == lesson_id, Lesson.course_id == course_id))
    lesson = result.scalars().first()
    if lesson:
        for var, value in lesson_data.dict(exclude_unset=True).items():
            setattr(lesson, var, value)
        await session.commit()
        await session.refresh(lesson, attribute_names=['files'])
        return LessonRead.model_validate(lesson)
    return None


async def delete_lesson(session: AsyncSession, course_id: int, lesson_id: int) -> bool:
    result = await session.execute(select(Lesson).where(Lesson.id == lesson_id, Lesson.course_id == course_id))
    lesson = result.scalars().first()
    if lesson:
        await session.delete(lesson)
        await session.commit()
        return True
    return False
