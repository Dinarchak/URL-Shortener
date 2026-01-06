from fastapi import APIRouter, HTTPException, status
from schemas import SlugSchema, CreateLinkSchema
from service import create_slug, get_url_by_slug
from exceptions import NotUrlFindError

router = APIRouter(prefix='/linksAPI')

@router.post('/add', summary='Создать ссылку')
async def add_link(data: CreateLinkSchema) -> SlugSchema:
    return await create_slug(url=data.url)



@router.get('/{short_id}', summary='Получить ссылку')
async def get_link(short_id: str) -> SlugSchema:
    try:
        return await get_url_by_slug(slug=short_id)
    except NotUrlFindError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Такое сокращение не найдено')
