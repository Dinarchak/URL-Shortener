from fastapi import APIRouter, status, HTTPException
from fastapi.responses import RedirectResponse
from service import get_url_by_slug
from exceptions import NoSuchSlugError

router = APIRouter()

@router.get('/links/{slug}')
async def redirect_to_url(slug: str):
    try:
        url = await get_url_by_slug(slug)
        return RedirectResponse(url, status_code=status.HTTP_302_FOUND)
    except NoSuchSlugError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Нет такого url')
