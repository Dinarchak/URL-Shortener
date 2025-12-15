from schemas import SlugSchema
from dao import get_url_by_slug_or_none, add_slug_to_db
from exceptions import SlugAlreadyExistsError, NotUrlFindError
from models import Slug
import string
import random

async def get_url_by_slug(slug: str) -> SlugSchema | None:

    slug: Slug | None = await get_url_by_slug_or_none(slug)

    if not slug:
        raise NotUrlFindError()

    return SlugSchema(slug=slug.slug, url=slug.url)


async def create_slug(url: str) -> SlugSchema:
    all_chars = string.ascii_letters + string.digits
    new_slug = ''.join(random.choice(all_chars) for _ in range(6))

    for attempt in range(5):
        try:
            await add_slug_to_db(new_slug, url)
            return SlugSchema(slug=new_slug, url=url)
        except SlugAlreadyExistsError as ex:
            if attempt == 4:
                raise SlugAlreadyExistsError from ex
