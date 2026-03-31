from fastapi import APIRouter, status, HTTPException, Request, Response
from fastapi.responses import RedirectResponse
from service import get_url_by_slug
from exceptions import NoSuchSlugError
from settings import config
from kafka_producer import send_link_ckick
from schemas import RedirectInfo
from datetime import datetime
from aiohttp import ClientSession


router = APIRouter()

@router.get('/links/{slug}')
async def redirect_to_url(request: Request, slug: str):
    try:
        url = await get_url_by_slug(slug)
    except NoSuchSlugError as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Нет такого slug-а')

    try:
        send_link_ckick(RedirectInfo(slug=slug, time=datetime.now(), userinfo=request.headers.get('user-agent')))
        return RedirectResponse(url, status_code=status.HTTP_302_FOUND)
    except NoSuchSlugError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Нет такого url')
    

@router.get('/health/{short}')
async def check_slug_health(slug: str):
    try:
        url = await get_url_by_slug(slug)
    except NoSuchSlugError as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Нет такого slug-а')

    async with ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return Response("Ссылка рабочая", status_code=status.HTTP_200_OK)
            else:
                return Response(f"Ответ пришел с кодом {response.status}", status_code=status.HTTP_200_OK)