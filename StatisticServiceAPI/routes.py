from fastapi import APIRouter, Cookie, HTTPException, status
from service import (
    get_all_redirect_events,
    get_all_redirect_events,
    get_all_redirect_events_by_user
)
from typing import List
from schemas import RedirectEventSchema, CreationEventSchema
from settings import config
from jose import jwt, ExpiredSignatureError, JWTError

router = APIRouter(prefix='')

@router.get('/redirects/all')
async def get_all_redirects() -> List[RedirectEventSchema]:
    events: List[RedirectEventSchema] = await get_all_redirect_events()
    # тут я сначала вручную перевел SQLAlchemy экземпляры в Pydantic экземпляры а потом в json обьъекты
    # хотя можно было оставить и SQLAlchemy экземпляры, fastAPI сам бы все сделал
    #(вообще я еще и в json переводи Pydantic, короче куча того, что можно не писать, в том числе этот комментарий))))
    return events 

@router.get('/creations/all')
async def get_all_creations() -> List[CreationEventSchema]:
    creations: List[CreationEventSchema] = await get_all_redirect_events()
    return creations

@router.get('/creations/user-slugs')
async def get_slugs_of_user(jwt_token: str = Cookie(alias='fastapiusersauth', default=None)) -> List[CreationEventSchema]:

    try:
        print(jwt_token)
        payload = jwt.decode(token=jwt_token, key=config.jwt.token, audience=config.jwt.aud, algorithms=['HS256'])
    except ExpiredSignatureError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Пользователь не авторизован')
    except JWTError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Что-то пошло не так\n{e}')
    print(payload)
    creations: List[CreationEventSchema] = await get_all_redirect_events_by_user(user_id=int(payload['sub']))

    return creations
