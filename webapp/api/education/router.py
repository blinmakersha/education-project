from fastapi import APIRouter

course_router = APIRouter(prefix='/courses')
lesson_router = APIRouter(prefix='/lessons')
subscribe_router = APIRouter(prefix='/subscribes')
