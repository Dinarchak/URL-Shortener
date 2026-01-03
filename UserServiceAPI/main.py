
from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi_users import FastAPIUsers
from models import User
from authentication.user_manager import get_user_manager
from authentication.auth import auth_backend
from schemas import UserReadSchema, UserCreateSchema
from database import engine, Base


"""
    TODO:
    Добавить ручку для просмотра всех пользователей
    Добавить роли админа и права админа
    Добавить возможность удалить пользователя
    Упростить тело запроса в ручках
    Придумать им нормальное описание
"""


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend]
)


app = FastAPI(lifespan=lifespan)
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserReadSchema, UserCreateSchema),
    prefix="/register",
    tags=["auth"],
)
