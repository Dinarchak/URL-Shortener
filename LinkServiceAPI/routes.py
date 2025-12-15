from fastapi import APIRouter
from schemas import SlugSchema, CreateLinkSchema
from service import create_slug, get_url_by_slug

router = APIRouter(prefix='/linksAPI')

@router.post('/add', summary='Создать ссылку')
async def add_link(data: CreateLinkSchema) -> SlugSchema:
    return await create_slug(url=data.url)



@router.get('/{short_id}', summary='Получить ссылку')
async def get_link(slug: str) -> SlugSchema:
    return await get_url_by_slug(slug=slug)
