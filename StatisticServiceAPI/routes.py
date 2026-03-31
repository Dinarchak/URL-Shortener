from fastapi import APIRouter
from service import get_all_events
from typing import List
from schemas import RedirectEventSchema

router = APIRouter(prefix='')

@router.get('/redirects/all')
async def get_all_redirects() -> List[RedirectEventSchema]:
    events: List[RedirectEventSchema] = await get_all_events()
    # тут я сначала вручную перевел SQLAlchemy экземпляры в Pydantic экземпляры а потом в json обьъекты
    # хотя можно было оставить и SQLAlchemy экземпляры, fastAPI сам бы все сделал
    #(вообще я еще и в json переводи Pydantic, короче куча того, что можно не писать, в том числе этот комментарий))))
    return events 

