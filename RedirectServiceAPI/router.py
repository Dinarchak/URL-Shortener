from fastapi import APIRouter, status, HTTPException, Request
from fastapi.responses import RedirectResponse
from service import get_url_by_slug
from exceptions import NoSuchSlugError
from settings import config
from kafka_producer import send_link_ckick
from schemas import RedirectInfo
from datetime import datetime


router = APIRouter()

@router.get('/links/{slug}')
async def redirect_to_url(request: Request, slug: str):
    try:
        url = await get_url_by_slug(slug)
    except NoSuchSlugError as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Нет такого slug-а')

    try:
        send_link_ckick(RedirectInfo(slug=slug, time=datetime.now(), userinfo=request.headers.get('user-agent')))

        print(f'Сработало событие переадресации: {slug}')

        return RedirectResponse(url, status_code=status.HTTP_302_FOUND)
    except NoSuchSlugError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Нет такого url')