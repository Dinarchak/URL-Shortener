from database import async_session_maker
from models import RedirectEvent, CreateEvent
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
import typing as tp


async def add_redirect_event_record(
        slug: str,
        time: datetime,
        userinfo: str
) -> None:
    async with async_session_maker() as session:
        re = RedirectEvent(
            time=time,
            slug=slug,
            userinfo=userinfo
        )

        session.add(re)
        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        

async def get_all_redirect_event_records():
    async with async_session_maker() as session:
        query = select(RedirectEvent)
        result = await session.execute(query)

        return result.scalars().all()
    

async def add_create_event_record(
        slug: str,
        time: datetime,
        userinfo: str,
        user_id: int
) -> None:
    async with async_session_maker() as session:
        cr = CreateEvent(
            time=time,
            slug=slug,
            userinfo=userinfo,
            user_id=user_id
        )

        session.add(cr)
        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e


async def get_all_create_event_records(**filter):
    async with async_session_maker() as session:
        query = select(CreateEvent).filter_by(**filter)
        result = await session.execute(query)

        return result.scalars().all()
