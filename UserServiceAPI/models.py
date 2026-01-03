from fastapi_users.db import (
    SQLAlchemyBaseUserTable,
    SQLAlchemyUserDatabase
)

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import Base, get_async_session

class User(SQLAlchemyBaseUserTable[int], Base):
    pass


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)