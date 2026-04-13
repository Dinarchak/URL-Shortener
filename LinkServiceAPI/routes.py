from fastapi import APIRouter, HTTPException, status
from schemas import SlugSchema, CreateLinkSchema
from service import create_slug, get_url_by_slug
from exceptions import NotUrlFindError, SlugAlreadyExistsError, EventSendingError
from kafka_producer import send_slug_creation

router = APIRouter(prefix='/linksAPI')

@router.post('/add', summary='Создать ссылку')
async def add_link(data: CreateLinkSchema) -> SlugSchema:
    try:
        slug = await create_slug(url=data.url)
    except SlugAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Сокращение уже занято')

    try:
        send_slug_creation(slug)
    except EventSendingError as e:
        print('Ошибка продюсера сообщений:\n', e, end='\n\n')
    return slug



@router.get('/{short_id}', summary='Получить ссылку')
async def get_link(short_id: str) -> SlugSchema:
    try:
        return await get_url_by_slug(slug=short_id)
    except NotUrlFindError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Такое сокращение не найдено')
