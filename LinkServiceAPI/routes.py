from fastapi import APIRouter, HTTPException, status, Cookie, Request
from schemas import SlugSchema, NewSlugSchemaEvent
from service import create_slug, get_url_by_slug
from exceptions import NotUrlFindError, SlugAlreadyExistsError, EventSendingError
from kafka_producer import send_slug_creation
from jose import jwt, JWTError, ExpiredSignatureError
from settings import config
from datetime import datetime


router = APIRouter(prefix='/linksAPI')

@router.post('/add', summary='Создать ссылку')
async def add_link(request: Request, link: str, jwt_token=Cookie(alias='fastapiusersauth', default=None)) -> SlugSchema:
    try:
        slug = await create_slug(url=link)
    except SlugAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Сокращение уже занято')

    try:
        payload = jwt.decode(token=jwt_token, key=config.jwt.token, audience=config.jwt.aud, algorithms=['HS256'])
    except ExpiredSignatureError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'Пользователь не авторизован\n{e}')
    except JWTError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Что-то пошло не так\n{e}')


    try:
        send_slug_creation(NewSlugSchemaEvent(
            slug=slug.slug,
            url=slug.url,
            user_id=int(payload['sub']),
            time=datetime.now(),
            userinfo=request.headers.get('user-agent')
        ))
    except EventSendingError as e:
        print('Ошибка продюсера сообщений:\n', e, end='\n\n')
    return slug


@router.get('/{short_id}', summary='Получить ссылку')
async def get_link(short_id: str) -> SlugSchema:
    try:
        return await get_url_by_slug(slug=short_id)
    except NotUrlFindError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Такое сокращение не найдено')
