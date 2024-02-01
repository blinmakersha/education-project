from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from webapp.models.sirius.course import Course
from webapp.schema.education.course import CourseCreate, CourseRead


async def create_course(session: AsyncSession, course_data: CourseCreate) -> CourseRead:
    new_course = Course(**course_data.model_dump_json())
    session.add(new_course)
    await session.commit()
    await session.refresh(new_course)
    return CourseRead.model_validate(new_course)


async def get_course_by_id(session: AsyncSession, course_id: int) -> CourseRead | None:
    result = await session.execute(select(Course).where(Course.id == course_id))
    course = result.scalars().first()
    if course:
        return CourseRead.model_validate(course)
    return None


async def update_course(session: AsyncSession, course_id: int, course_data: CourseCreate) -> CourseRead | None:
    result = await session.execute(select(Course).where(Course.id == course_id))
    course = result.scalars().first()
    if course:
        for var, value in vars(course_data).items():
            setattr(course, var, value) if value else None
        await session.commit()
        await session.refresh(course)
        return CourseRead.model_validate(course)
    return None


async def delete_course(session: AsyncSession, course_id: int) -> (True | None):
    result = await session.execute(select(Course).where(Course.id == course_id))
    course = result.scalars().first()
    if course:
        await session.delete(course)
        await session.commit()
        return True
