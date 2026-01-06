import aiohttp
from settings import config
from fastapi import status
from exceptions import NoSuchSlugError

async def get_url_by_slug(slug: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get('/'.join([config.get_url_by_slug_path, slug])) as response:
            if response.status == status.HTTP_200_OK:
                data = await response.json()
                return data['url']
            elif response.status == status.HTTP_404_NOT_FOUND:
                raise NoSuchSlugError()
