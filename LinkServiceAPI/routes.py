from fastapi import APIRouter
from schemas import LinkSchema, CreateLinkSchema

router = APIRouter(prefix='/linksAPI')

@router.post('/add', summary='Создать ссылку')
async def add_link(data: CreateLinkSchema):
    pass

@router.get('/{short_id}', summary='Получить ссылку')
async def update_link(short: int) -> LinkSchema:
    pass

@router.delete('/delete/{short_id}', summary='Удалить ссылку')
async def delete_link(short: int) -> LinkSchema:
    pass
