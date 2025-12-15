from database import async_session_maker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from models import Slug

async def add_slug_to_db(
        slug: str,
        url: str):
    async with async_session_maker() as session:
        new_slug = Slug(slug=slug, url=url)
        session.add(new_slug)
        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e

async def get_url_by_slug_or_none(slug: str) -> str | None:
    async with async_session_maker() as session:
        query = select(Slug).filter_by(slug=slug)
        res = await session.execute(query)
        return res.scalar_one_or_none()
    
